# AGENTS.md

Dru is a GitHub-backed repository-hydrated command system, not an official ChatGPT plugin. `Entity` is abstract; `Pal`, `Mate`, `Medic`, `Mind`, and `Trello` are concrete entity types.

Entity and bucket names are case-insensitive, stored lowercase, and globally unique. The registry is `entity.json`; generated state is `entity-state.json`. Runtime instructions are `INSTRUCTIONS.md` plus every `instructions/*.md` file.

Canonical row storage is `entities/<type>/<bucket>/data/<row>.json` for Pal, Mate, Medic, and Mind. Trello uses `entities/trello/<board>.json`. Row-oriented entities have generated indexes and packs alongside their data. Pending row mutations live under `mutations/<type>/<bucket>/<uuid>.json`; structural mutations live under `bucket_mutations/`.

Trello IDs must come from the connector and are never synthesized. Trello sync mirrors external non-archived lists and cards into the local board entity. Trello read commands use committed JSON only.

After changes, update runtime documentation and registry, run `python3 scripts/upgrade_entity_types.py`, `python3 scripts/process_bucket_mutations.py`, and `python3 scripts/process_mutations.py`, validate every JSON file, and inspect the worktree. This repository is the empty template: never add personal records to it.
