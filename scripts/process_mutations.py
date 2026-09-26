#!/usr/bin/env python3
"""Apply mutations and regenerate typed entity read artifacts."""
from __future__ import annotations
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"
STATE_PATH = ROOT / "entity-state.json"
MUTATIONS_ROOT = ROOT / "mutations"
EXPECTED_KEYS = {"action", "selector", "json"}
SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
MAX_FILENAME_BYTES = 240


class MutationError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MutationError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def safe_path(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise MutationError(f"invalid {label}")
    return ROOT / path


def encode_name(name: str) -> str:
    return name.replace("%", "%25").replace("/", "%2F").replace("\\", "%5C")


def safe_row_name(name: str) -> bool:
    return name not in {"", ".", ".."} and "\x00" not in name and len(encode_name(name).encode("utf-8")) <= MAX_FILENAME_BYTES


def load_registry() -> dict[str, dict[str, Any]]:
    registry = load_json(REGISTRY_PATH)
    if not isinstance(registry, dict) or not isinstance(registry.get("entities"), list):
        raise MutationError("entity.json must contain an entities list")
    result: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for item in registry["entities"]:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not isinstance(item.get("type"), str):
            raise MutationError("every entity needs string type and name")
        entity_type = item["type"].strip().lower()
        name = item["name"].strip().lower()
        if entity_type not in {"pal", "mate", "trello"} or not SAFE_NAME.fullmatch(name):
            raise MutationError(f"invalid entity: {entity_type}/{name}")
        if name in names:
            raise MutationError(f"duplicate bucket name across entity types: {name}")
        names.add(name)
        key = f"{entity_type}/{name}"
        if entity_type == "trello":
            result[key] = {"type": entity_type, "name": name, "entity_path": safe_path(item["entity_path"], f"entity path for {key}")}
        else:
            result[key] = {"type": entity_type, "name": name, "data_dir": safe_path(item["data_dir"], f"data path for {key}"), "index_path": safe_path(item["index_path"], f"index path for {key}"), "pack_path": safe_path(item["pack_path"], f"pack path for {key}")}
    return result


def load_rows(data_dir: Path) -> list[dict[str, Any]]:
    if not data_dir.exists():
        return []
    rows = []
    for path in sorted(data_dir.glob("*.json")):
        row = load_json(path)
        if not isinstance(row, dict):
            raise MutationError(f"{relative(path)} must contain a JSON object")
        rows.append(row)
    return rows


def generated_name(bucket: str, row: dict[str, Any], ordinal: int) -> str:
    timestamp = re.sub(r"[^a-z0-9]+", "_", str(row.get("timestamp", "")).lower()).strip("_")
    base = f"{bucket}_{timestamp}" if timestamp else f"{bucket}_{hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:12]}"
    return base if ordinal == 0 else f"{base}_{ordinal + 1}"


def normalize_names(entity: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    used: set[str] = set()
    for ordinal, row in enumerate(rows):
        row["type"] = entity["type"]
        name = str(row.get("name", "")).strip()
        if not safe_row_name(name):
            name = generated_name(entity["name"], row, ordinal)
        candidate, suffix = name, 2
        while candidate in used or not safe_row_name(candidate):
            candidate = f"{name}_{suffix}"
            suffix += 1
        row["name"] = candidate
        used.add(candidate)


def selector(value: Any, path: Path) -> tuple[str, re.Pattern[str]]:
    if not isinstance(value, dict):
        raise MutationError(f"{relative(path)} selector must be an object")
    if set(value) == {"field", "regex"}:
        field, expression = value.get("field"), value.get("regex")
    elif len(value) == 1:
        field, expression = next(iter(value.items()))
    else:
        raise MutationError(
            f"{relative(path)} selector must contain field and regex"
        )
    if not isinstance(field, str) or not field or not isinstance(expression, str):
        raise MutationError(f"invalid selector in {relative(path)}")
    try:
        return field, re.compile(expression)
    except re.error as exc:
        raise MutationError(f"invalid regex in {relative(path)}: {exc}") from exc


def matches(row: dict[str, Any], field: str, pattern: re.Pattern[str]) -> bool:
    value = row.get(field)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    elif value is None:
        value = "null"
    elif isinstance(value, bool):
        value = "true" if value else "false"
    return value is not None and pattern.search(str(value)) is not None


def validate_mutation(path: Path) -> dict[str, Any]:
    mutation = load_json(path)
    if not isinstance(mutation, dict) or set(mutation) != EXPECTED_KEYS:
        raise MutationError(f"{relative(path)} must contain exactly action, selector, and json")
    action = mutation.get("action")
    if action not in {"add", "update", "remove", "move"}:
        raise MutationError(f"{relative(path)} has an unsupported action")
    if action == "add" and (mutation.get("selector") is not None or not isinstance(mutation.get("json"), dict)):
        raise MutationError(f"invalid add mutation in {relative(path)}")
    if action == "update" and (not isinstance(mutation.get("json"), dict) or not mutation["json"]):
        raise MutationError(f"invalid update mutation in {relative(path)}")
    if action == "remove" and mutation.get("json") is not None:
        raise MutationError(f"remove json must be null in {relative(path)}")
    if action in {"update", "remove", "move"}:
        selector(mutation.get("selector"), path)
    if action == "move" and not isinstance(mutation.get("json"), dict):
        raise MutationError(f"invalid move mutation in {relative(path)}")
    return mutation


def apply_mutation(source: str, rows: dict[str, list[dict[str, Any]]], mutation: dict[str, Any], path: Path, registry: dict[str, dict[str, Any]]) -> None:
    source_rows = rows[source]
    if mutation["action"] == "add":
        source_rows.append(dict(mutation["json"]))
        return
    field, pattern = selector(mutation["selector"], path)
    found = [row for row in source_rows if matches(row, field, pattern)]
    if not found:
        raise MutationError(f"{relative(path)} matched zero rows")
    if mutation["action"] == "remove":
        rows[source] = [row for row in source_rows if not matches(row, field, pattern)]
    elif mutation["action"] == "update":
        for row in found:
            row.update(mutation["json"])
    else:
        payload = mutation["json"]
        destination = f"{payload.get('type', 'pal').strip().lower()}/{payload.get('bucket', payload.get('pal', '')).strip().lower()}"
        if destination not in registry or destination == source or destination not in rows:
            raise MutationError(f"{relative(path)} has an invalid move destination")
        names = {str(row.get("name")) for row in rows[destination]}
        moved = {str(row.get("name")) for row in found if row.get("name") is not None}
        if names & moved:
            raise MutationError(f"{relative(path)} would collide on {', '.join(sorted(names & moved))}")
        rows[source] = [row for row in source_rows if not matches(row, field, pattern)]
        rows[destination].extend(dict(row) for row in found)


def write_bucket(entity: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    normalize_names(entity, rows)
    ordered = sorted(rows, key=lambda row: row["name"])
    temporary = entity["data_dir"].with_name(entity["data_dir"].name + ".tmp")
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True, exist_ok=True)
    filenames = []
    for row in ordered:
        filename = f"{encode_name(row['name'])}.json"
        filenames.append(filename)
        (temporary / filename).write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if entity["data_dir"].exists():
        shutil.rmtree(entity["data_dir"])
    temporary.replace(entity["data_dir"])
    entity["index_path"].parent.mkdir(parents=True, exist_ok=True)
    entity["index_path"].write_text(json.dumps(filenames, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    entity["pack_path"].parent.mkdir(parents=True, exist_ok=True)
    entity["pack_path"].write_text(json.dumps(ordered, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def write_state(registry: dict[str, dict[str, Any]]) -> None:
    state: dict[str, Any] = {"version": 2, "registry_blob_sha": blob_sha(REGISTRY_PATH), "total_rows": 0, "entities": {}}
    for key, entity in registry.items():
        if entity["type"] == "trello":
            value = load_json(entity["entity_path"])
            count = len(value.get("cards", [])) if isinstance(value, dict) else 0
            state["entities"][key] = {"type": "trello", "bucket": entity["name"], "entity_path": relative(entity["entity_path"]), "count": count}
        else:
            index = json.loads(entity["index_path"].read_text(encoding="utf-8"))
            state["entities"][key] = {"type": entity["type"], "bucket": entity["name"], "data_dir": relative(entity["data_dir"]), "index_path": relative(entity["index_path"]), "pack_path": relative(entity["pack_path"]), "count": len(index), "index_blob_sha": blob_sha(entity["index_path"])}
        state["total_rows"] += state["entities"][key]["count"]
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> None:
    registry = load_registry()
    rows = {key: load_rows(entity["data_dir"]) for key, entity in registry.items() if entity["type"] != "trello"}
    files = sorted(path for path in MUTATIONS_ROOT.glob("*/*/*.json") if path.is_file())
    for path in files:
        source = f"{path.parent.parent.name.lower()}/{path.parent.name.lower()}"
        if source not in rows:
            raise MutationError(f"{relative(path)} targets an unregistered or non-bucket entity")
        apply_mutation(source, rows, validate_mutation(path), path, registry)
    for key, bucket_rows in rows.items():
        write_bucket(registry[key], bucket_rows)
    write_state(registry)
    for path in files:
        path.unlink()
    print(f"processed {len(files)} mutation(s); {sum(len(items) for items in rows.values())} bucket row(s) across {len(registry)} entities")


if __name__ == "__main__":
    try:
        main()
    except MutationError as exc:
        raise SystemExit(f"Dru mutation error: {exc}")
