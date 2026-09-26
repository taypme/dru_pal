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
        action = str(mutation.get("action", "")).strip().lower()
        if action == "delete":
            if set(mutation) != {"action", "type", "name"}:
                raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
        elif action == "pal_to_mate":
            if set(mutation) not in (
                {"action", "type", "name"},
                {"action", "type", "name", "strip_prefix"},
            ):
                raise SystemExit(f"Dru bucket mutation error: invalid mutation {path.relative_to(ROOT)}")
        else:
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

        if action == "pal_to_mate":
            if entity_type != "pal":
                raise SystemExit(
                    f"Dru bucket mutation error: pal_to_mate requires pal/{name}"
                )
            data_dir = ROOT / str(entity["data_dir"])
            grouped: dict[str, list[object]] = {}
            strip_prefix = str(mutation.get("strip_prefix", ""))
            for row_path in sorted(data_dir.glob("*.json")):
                row = json.loads(row_path.read_text(encoding="utf-8"))
                row_name = str(row.get("name", ""))
                key = row_name
                if strip_prefix and key.startswith(strip_prefix):
                    key = key[len(strip_prefix):]
                grouped.setdefault(key, []).append(row.get("value"))

            entities.remove(entity)
            mate_dir = ROOT / "entities" / "mate" / name
            mate_data = mate_dir / "data"
            if mate_dir.exists():
                shutil.rmtree(mate_dir)
            mate_data.mkdir(parents=True, exist_ok=True)

            filenames = []
            rows = []
            for key in sorted(grouped):
                mate_row = {"name": key, "value": grouped[key], "type": "mate"}
                filename = f"{encode_name(key)}.json"
                filenames.append(filename)
                rows.append(mate_row)
                (mate_data / filename).write_text(
                    json.dumps(mate_row, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            (mate_dir / "index.json").write_text(
                json.dumps(filenames, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            (mate_dir / "pack.json").write_text(
                json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            entities.append(
                {
                    "name": name,
                    "data_dir": f"entities/mate/{name}/data",
                    "index_path": f"entities/mate/{name}/index.json",
                    "pack_path": f"entities/mate/{name}/pack.json",
                    "type": "mate",
                }
            )
            pal_dir = ROOT / "entities" / "pal" / name
            if pal_dir.exists():
                shutil.rmtree(pal_dir)
        else:
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
