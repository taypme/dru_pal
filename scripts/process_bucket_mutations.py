#!/usr/bin/env python3
"""Apply structural Dru bucket mutations before row mutations."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"
MUTATIONS_ROOT = ROOT / "bucket_mutations"


def encode_name(name: str) -> str:
    return name.replace("%", "%25").replace("/", "%2F").replace("\\", "%5C")


def main() -> None:
    files = sorted(path for path in MUTATIONS_ROOT.glob("*.json") if path.is_file())
    if not files:
        print("processed 0 bucket mutation(s)")
        return

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    entities = registry.get("entities")
    if not isinstance(entities, list):
        raise SystemExit("Dru bucket mutation error: entity.json must contain an entities list")

    deleted = 0
    for path in files:
        mutation = json.loads(path.read_text(encoding="utf-8"))
        if set(mutation) != {"action", "type", "name"} or mutation.get("action") != "delete":
            raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")

        entity_type = str(mutation.get("type", "")).strip().lower()
        name = str(mutation.get("name", "")).strip().lower()
        matches = [
            item for item in entities
            if str(item.get("type", "")).strip().lower() == entity_type
            and str(item.get("name", "")).strip().lower() == name
        ]
        if len(matches) != 1:
            raise SystemExit(
                f"Dru bucket mutation error: expected exactly one registered {entity_type}/{name}"
            )

        entity = matches[0]
        entities.remove(entity)

        if entity_type == "trello":
            entity_path = ROOT / str(entity["entity_path"])
            if entity_path.exists():
                entity_path.unlink()
        else:
            bucket_dir = ROOT / "entities" / entity_type / name
            if bucket_dir.exists():
                shutil.rmtree(bucket_dir)

        if entity_type == "pal":
            context_row = ROOT / "entities" / "mate" / "context" / "data" / f"{encode_name(name)}.json"
            if context_row.exists():
                context_row.unlink()

        path.unlink()
        deleted += 1

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"processed {deleted} bucket mutation(s)")


if __name__ == "__main__":
    main()
