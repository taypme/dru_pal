#!/usr/bin/env python3
"""Apply structural Dru entity/bucket mutations before row mutations."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"
MUTATIONS_ROOT = ROOT / "bucket_mutations"
SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


def encode_name(name: str) -> str:
    return name.replace("%", "%25").replace("/", "%2F").replace("\\", "%5C")


def row_types(registry: dict) -> set[str]:
    result = set()
    for name, definition in registry.get("entity_types", {}).items():
        if name != "trello" and isinstance(definition, dict) and definition.get("concrete") is True:
            result.add(str(name).lower())
    return result


def create_entity_type(registry: dict, mutation: dict) -> None:
    if set(mutation) != {"action", "type", "description"}:
        raise SystemExit("Dru bucket mutation error: invalid create_type mutation")
    entity_type = str(mutation["type"]).strip().lower()
    if not SAFE_NAME.fullmatch(entity_type) or entity_type == "trello":
        raise SystemExit(f"Dru bucket mutation error: invalid row entity type {entity_type}")
    types = registry.setdefault("entity_types", {})
    if entity_type in types:
        raise SystemExit(f"Dru bucket mutation error: entity type already exists: {entity_type}")
    label = entity_type[:1].upper() + entity_type[1:]
    types[entity_type] = {"description": str(mutation["description"]), "concrete": True, "new": f"{label} new <bucket>"}


def create_bucket(registry: dict, entities: list, mutation: dict) -> None:
    allowed = ({"action", "type", "name"}, {"action", "type", "name", "commands"})
    if set(mutation) not in allowed:
        raise SystemExit("Dru bucket mutation error: invalid create mutation")
    entity_type = str(mutation["type"]).strip().lower()
    name = str(mutation["name"]).strip().lower()
    if entity_type not in row_types(registry) or not SAFE_NAME.fullmatch(name):
        raise SystemExit(f"Dru bucket mutation error: invalid bucket {entity_type}/{name}")
    if any(str(item.get("name", "")).lower() == name for item in entities):
        raise SystemExit(f"Dru bucket mutation error: bucket name already exists: {name}")
    target = ROOT / "entities" / entity_type / name
    data = target / "data"
    data.mkdir(parents=True, exist_ok=False)
    (target / "index.json").write_text("[]\n", encoding="utf-8")
    (target / "pack.json").write_text("[]\n", encoding="utf-8")
    entity = {"name": name, "data_dir": f"entities/{entity_type}/{name}/data", "index_path": f"entities/{entity_type}/{name}/index.json", "pack_path": f"entities/{entity_type}/{name}/pack.json", "type": entity_type}
    if "commands" in mutation:
        if not isinstance(mutation["commands"], list):
            raise SystemExit("Dru bucket mutation error: commands must be a list")
        entity["commands"] = mutation["commands"]
    entities.append(entity)


def migrate_row_bucket(registry: dict, entity: dict, target_type: str) -> None:
    source_type = str(entity["type"]).lower()
    name = str(entity["name"]).lower()
    rows = row_types(registry)
    if source_type not in rows or target_type not in rows:
        raise SystemExit(f"Dru bucket mutation error: unsupported migration {source_type}->{target_type}")
    source_dir = ROOT / "entities" / source_type / name
    target_dir = ROOT / "entities" / target_type / name
    if target_dir.exists():
        raise SystemExit(f"Dru bucket mutation error: target already exists: {target_type}/{name}")
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if source_dir.exists():
        shutil.move(str(source_dir), str(target_dir))
    data_dir = target_dir / "data"
    for row_path in sorted(data_dir.glob("*.json")) if data_dir.exists() else []:
        row = json.loads(row_path.read_text(encoding="utf-8"))
        row["type"] = target_type
        row_path.write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    entity["type"] = target_type
    entity["data_dir"] = f"entities/{target_type}/{name}/data"
    entity["index_path"] = f"entities/{target_type}/{name}/index.json"
    entity["pack_path"] = f"entities/{target_type}/{name}/pack.json"


def migrate_pal_to_mate(entity: dict, strip_prefix: str) -> None:
    name = str(entity["name"]).lower()
    if str(entity["type"]).lower() != "pal":
        raise SystemExit(f"Dru bucket mutation error: pal_to_mate requires pal/{name}")
    data_dir = ROOT / str(entity["data_dir"])
    grouped: dict[str, list[object]] = {}
    for row_path in sorted(data_dir.glob("*.json")):
        row = json.loads(row_path.read_text(encoding="utf-8"))
        key = str(row.get("name", ""))
        if strip_prefix and key.startswith(strip_prefix):
            key = key[len(strip_prefix):]
        grouped.setdefault(key, []).append(row.get("value"))
    source_dir = ROOT / "entities" / "pal" / name
    target_dir = ROOT / "entities" / "mate" / name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    data = target_dir / "data"
    data.mkdir(parents=True, exist_ok=True)
    filenames, rows = [], []
    for key in sorted(grouped):
        row = {"name": key, "value": grouped[key], "type": "mate"}
        filename = f"{encode_name(key)}.json"
        filenames.append(filename)
        rows.append(row)
        (data / filename).write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target_dir / "index.json").write_text(json.dumps(filenames, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target_dir / "pack.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    if source_dir.exists():
        shutil.rmtree(source_dir)
    entity["type"] = "mate"
    entity["data_dir"] = f"entities/mate/{name}/data"
    entity["index_path"] = f"entities/mate/{name}/index.json"
    entity["pack_path"] = f"entities/mate/{name}/pack.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    entities = registry.get("entities")
    if not isinstance(entities, list):
        raise SystemExit("Dru bucket mutation error: entity.json must contain an entities list")
    files = sorted(path for path in MUTATIONS_ROOT.glob("*.json") if path.is_file())
    processed = 0
    for path in files:
        mutation = json.loads(path.read_text(encoding="utf-8"))
        action = str(mutation.get("action", "")).strip().lower()
        if action == "create_type":
            create_entity_type(registry, mutation)
        elif action == "create":
            create_bucket(registry, entities, mutation)
        else:
            entity_type = str(mutation.get("type", "")).strip().lower()
            name = str(mutation.get("name", "")).strip().lower()
            matches = [item for item in entities if str(item.get("type", "")).lower() == entity_type and str(item.get("name", "")).lower() == name]
            if len(matches) != 1:
                raise SystemExit(f"Dru bucket mutation error: expected exactly one registered {entity_type}/{name}")
            entity = matches[0]
            if action == "delete":
                if set(mutation) != {"action", "type", "name"}:
                    raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
                entities.remove(entity)
                target = ROOT / str(entity["entity_path"]) if entity_type == "trello" else ROOT / "entities" / entity_type / name
                if target.exists():
                    target.unlink() if target.is_file() else shutil.rmtree(target)
            elif action == "migrate":
                if set(mutation) != {"action", "type", "name", "target_type"}:
                    raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
                migrate_row_bucket(registry, entity, str(mutation["target_type"]).strip().lower())
            elif action == "pal_to_mate":
                allowed = ({"action", "type", "name"}, {"action", "type", "name", "strip_prefix"})
                if set(mutation) not in allowed:
                    raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
                migrate_pal_to_mate(entity, str(mutation.get("strip_prefix", "")))
            else:
                raise SystemExit(f"Dru bucket mutation error: unsupported action in {path.relative_to(ROOT)}")
        path.unlink()
        processed += 1
    if processed:
        entities.sort(key=lambda item: str(item.get("name", "")).lower())
        REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"processed {processed} bucket mutation(s)")


if __name__ == "__main__":
    main()
