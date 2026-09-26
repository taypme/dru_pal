#!/usr/bin/env python3
"""Apply structural Dru entity/bucket mutations before row mutations."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"
MUTATIONS_ROOT = ROOT / "bucket_mutations"
ROW_TYPES = {"pal", "mate", "medic", "mind"}


def encode_name(name: str) -> str:
    return name.replace("%", "%25").replace("/", "%2F").replace("\\", "%5C")


def ensure_entity_types(registry: dict) -> bool:
    types = registry.setdefault("entity_types", {})
    changed = False
    definitions = {
        "medic": {"description": "A medical-domain row-oriented JSON bucket.", "concrete": True, "new": "Medic new <bucket>"},
        "mind": {"description": "A cognition, psychology, knowledge, and ideas-domain row-oriented JSON bucket.", "concrete": True, "new": "Mind new <bucket>"},
    }
    for name, definition in definitions.items():
        if types.get(name) != definition:
            types[name] = definition
            changed = True
    return changed


def migrate_row_bucket(entity: dict, target_type: str) -> None:
    source_type = str(entity["type"]).lower()
    name = str(entity["name"]).lower()
    if source_type not in ROW_TYPES or target_type not in ROW_TYPES:
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
    changed = ensure_entity_types(registry)
    files = sorted(path for path in MUTATIONS_ROOT.glob("*.json") if path.is_file())
    processed = 0
    for path in files:
        mutation = json.loads(path.read_text(encoding="utf-8"))
        action = str(mutation.get("action", "")).strip().lower()
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
            migrate_row_bucket(entity, str(mutation["target_type"]).strip().lower())
        elif action == "pal_to_mate":
            allowed = ({"action", "type", "name"}, {"action", "type", "name", "strip_prefix"})
            if set(mutation) not in allowed:
                raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
            migrate_pal_to_mate(entity, str(mutation.get("strip_prefix", "")))
        else:
            raise SystemExit(f"Dru bucket mutation error: unsupported action in {path.relative_to(ROOT)}")
        path.unlink()
        processed += 1
        changed = True
    if changed:
        REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"processed {processed} bucket mutation(s)")


if __name__ == "__main__":
    main()
