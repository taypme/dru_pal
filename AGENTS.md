# AGENTS.md

Dru is a GitHub-backed repository-hydrated command system, not an official
ChatGPT plugin. `Entity` is an abstract base; only `Pal`, `Mate`, and `Trello`
are concrete entity types.

Entity and bucket names are case-insensitive, stored lowercase, and globally
unique. The registry is `entity.json`; generated state is `entity-state.json`.

Canonical storage is `entities/<type>/<bucket>/data/<row>.json` for Pal and
Mate buckets and `entities/trello/<board>.json` for Trello boards. Generated
indexes and packs live alongside bucket data. Pending mutations live under
`mutations/<type>/<bucket>/<uuid>.json` and contain exactly `action`, `selector`,
and `json`.

Trello IDs must come from the connector and are never synthesized. Trello sync
mirrors external non-archived lists and cards into the local board entity.
Trello read commands use committed JSON only.

After changes, update the runtime documentation and registry, run
`python3 scripts/process_mutations.py`, validate every JSON file, and inspect
both Git worktrees. Keep the template empty and do not add personal records to
it.
