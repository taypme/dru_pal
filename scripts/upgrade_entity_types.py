#!/usr/bin/env python3
"""Keep the Dru registry aware of built-in concrete row entity types."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "entity.json"

DEFINITIONS = {
    "medic": {
        "description": "A medical-domain row-oriented JSON bucket.",
        "concrete": True,
        "new": "Medic new <bucket>",
    },
    "mind": {
        "description": "A cognition, psychology, knowledge, and ideas-domain row-oriented JSON bucket.",
        "concrete": True,
        "new": "Mind new <bucket>",
    },
    "heart": {
        "description": "An emotion, attachment, desire, dream, and regret-domain row-oriented JSON bucket.",
        "concrete": True,
        "new": "Heart new <bucket>",
    },
}

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
types = registry.setdefault("entity_types", {})
for name, definition in DEFINITIONS.items():
    types[name] = definition
REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
