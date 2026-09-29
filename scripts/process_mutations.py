#!/usr/bin/env python3
"""Apply Dru row and aggregate mutations and regenerate read artifacts."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"
STATE_PATH = ROOT / "entity-state.json"
MUTATIONS_ROOT = ROOT / "mutations"
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

def safe_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise MutationError(f"invalid repository path: {value}")
    return ROOT / path

def encode_name(name: str) -> str:
    return name.replace("%", "%25").replace("/", "%2F").replace("\\", "%5C")

def safe_row_name(name: str) -> bool:
    return name not in {"", ".", ".."} and "\x00" not in name and len(encode_name(name).encode("utf-8")) <= MAX_FILENAME_BYTES

def load_registry() -> dict[str, dict[str, Any]]:
    doc = load_json(REGISTRY_PATH)
    types = doc.get("entity_types", {})
    entities = doc.get("entities", [])
    if not isinstance(types, dict) or not isinstance(entities, list):
        raise MutationError("entity.json must contain entity_types and entities")
    result: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for item in entities:
        entity_type = str(item.get("type", "")).strip().lower()
        name = str(item.get("name", "")).strip().lower()
        definition = types.get(entity_type)
        if not isinstance(definition, dict) or definition.get("concrete") is not True or not SAFE_NAME.fullmatch(name):
            raise MutationError(f"invalid entity {entity_type}/{name}")
        if name in names:
            raise MutationError(f"duplicate bucket name: {name}")
        names.add(name)
        storage = str(definition.get("storage", "rows"))
        key = f"{entity_type}/{name}"
        if entity_type == "trello" or storage == "string_array":
            result[key] = {"type": entity_type, "name": name, "storage": storage, "entity_path": safe_path(str(item["entity_path"]))}
        else:
            result[key] = {"type": entity_type, "name": name, "storage": "rows", "data_dir": safe_path(str(item["data_dir"])), "index_path": safe_path(str(item["index_path"])), "pack_path": safe_path(str(item["pack_path"]))}
    return result

def load_rows(data_dir: Path) -> list[dict[str, Any]]:
    if not data_dir.exists():
        return []
    rows = []
    for path in sorted(data_dir.glob("*.json")):
        row = load_json(path)
        if not isinstance(row, dict):
            raise MutationError(f"{relative(path)} must contain an object")
        rows.append(row)
    return rows

def normalize_rows(entity: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    used: set[str] = set()
    timestamp = datetime.now(timezone.utc).isoformat()
    for ordinal, row in enumerate(rows):
        row["type"] = entity["type"]
        name = str(row.get("name", "")).strip()
        if not safe_row_name(name):
            payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            name = f"{entity['name']}_{hashlib.sha256(payload).hexdigest()[:12]}_{ordinal + 1}"
        candidate, suffix = name, 2
        while candidate in used:
            candidate = f"{name}_{suffix}"
            suffix += 1
        row["name"] = candidate
        used.add(candidate)
        if entity["type"] == "cluster":
            raw = row.get("value", [])
            values = raw if isinstance(raw, list) else [raw]
            normalized = []
            for value in values:
                observation = dict(value) if isinstance(value, dict) else {"value": value}
                if not isinstance(observation.get("timestamp"), str) or not observation["timestamp"].strip():
                    observation["timestamp"] = timestamp
                normalized.append(observation)
            row["value"] = normalized

def write_bucket(entity: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    normalize_rows(entity, rows)
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
        elif entity["storage"] == "string_array":
            value = load_json(entity["entity_path"])
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise MutationError(f"{relative(entity['entity_path'])} must be an array of strings")
            count = len(value)
            state["entities"][key] = {"type": entity["type"], "bucket": entity["name"], "entity_path": relative(entity["entity_path"]), "count": count, "entity_blob_sha": blob_sha(entity["entity_path"])}
        else:
            index = load_json(entity["index_path"])
            count = len(index)
            state["entities"][key] = {"type": entity["type"], "bucket": entity["name"], "data_dir": relative(entity["data_dir"]), "index_path": relative(entity["index_path"]), "pack_path": relative(entity["pack_path"]), "count": count, "index_blob_sha": blob_sha(entity["index_path"])}
        state["total_rows"] += count
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

def main() -> None:
    registry = load_registry()
    rows = {key: load_rows(entity["data_dir"]) for key, entity in registry.items() if entity["storage"] == "rows" and entity["type"] != "trello"}
    hoards = {key: load_json(entity["entity_path"]) for key, entity in registry.items() if entity["storage"] == "string_array"}
    files = sorted(path for path in MUTATIONS_ROOT.glob("*/*/*.json") if path.is_file())
    if files:
        raise MutationError("template mutation processing requires hydration before queued mutations are committed")
    for key, bucket_rows in rows.items():
        write_bucket(registry[key], bucket_rows)
    for key, values in hoards.items():
        if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
            raise MutationError(f"{key} must contain strings")
        registry[key]["entity_path"].write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_state(registry)
    print(f"generated empty/read state for {len(registry)} registered entities")

if __name__ == "__main__":
    try:
        main()
    except MutationError as exc:
        raise SystemExit(f"Dru mutation error: {exc}")
