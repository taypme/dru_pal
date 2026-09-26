#!/usr/bin/env python3
"""Keep registry and mutation processor aware of all concrete Dru entity types."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "entity.json"
PROCESSOR = ROOT / "scripts" / "process_mutations.py"

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
types = registry.setdefault("entity_types", {})
types["medic"] = {"description": "A medical-domain row-oriented JSON bucket.", "concrete": True, "new": "Medic new <bucket>"}
types["mind"] = {"description": "A cognition, psychology, knowledge, and ideas-domain row-oriented JSON bucket.", "concrete": True, "new": "Mind new <bucket>"}
REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

source = PROCESSOR.read_text(encoding="utf-8")
old = 'entity_type not in {"pal", "mate", "trello"}'
new = 'entity_type not in {"pal", "mate", "medic", "mind", "trello"}'
if old in source:
    source = source.replace(old, new)
elif new not in source:
    raise SystemExit("Dru upgrade error: process_mutations.py entity-type guard not found")
PROCESSOR.write_text(source, encoding="utf-8")
