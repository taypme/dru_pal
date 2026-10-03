#!/usr/bin/env python3
"""Purge and rewrite the canonical bare Dru command definition."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "entity.json"

DRU_SEMANTIC = (
    "When the entire user message is exactly Dru after trimming whitespace, render the current Dru status grouped by concrete entity type. "
    "Use entity type order Pal, Mate, Cluster, Hoard, Medic, Mind, Heart, Spirit, Trello. "
    "For each entity type, output a Markdown heading with the entity type name followed by a Markdown table containing only Bucket and Rows. "
    "Include every registered bucket of that type, sorted alphabetically by normalized bucket name, using entity-state.json counts. "
    "Never output one combined Type | Bucket | Rows table and never mix buckets from different entity types. "
    "Preserve a heading and an empty Bucket | Rows table even when an entity type has no registered buckets. "
    "Also report the active repository, exact commit, total row count, pending mutations, and capabilities, and end with Dru hydrated."
)


def main() -> None:
    registry: Any = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(registry, dict):
        raise SystemExit("Dru command rewrite error: entity.json must contain an object")

    commands = registry.get("global_commands")
    if not isinstance(commands, list):
        commands = []

    remaining = [
        command
        for command in commands
        if not (
            isinstance(command, dict)
            and str(command.get("machine", "")).strip().lower() == "dru"
        )
    ]
    removed = len(commands) - len(remaining)
    registry["global_commands"] = [
        {"machine": "dru", "semantic": DRU_SEMANTIC},
        *remaining,
    ]
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"purged {removed} bare Dru command definition(s); wrote 1 canonical grouped definition")


if __name__ == "__main__":
    main()
