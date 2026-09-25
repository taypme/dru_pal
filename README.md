# Dru

Dru is a GitHub-backed command system for typed entities. The abstract `Entity`
base is not user-creatable. The concrete types are `Pal`, `Mate`, and `Trello`.

## Repository shape

```text
INSTRUCTIONS.md
entity.json
entity-state.json
entities/pal/<bucket>/data/<row>.json
entities/mate/<bucket>/data/<row>.json
entities/trello/<board>.json
mutations/<type>/<bucket>/<uuid>.json
scripts/process_mutations.py
```

Names are interpreted case-insensitively and normalized to lowercase. Bucket
names are globally unique across Pal, Mate, and Trello.

Pal buckets store ordinary named JSON rows. Mate buckets append string or
integer values to arrays grouped by key. Trello board files store a board,
its stable `board_id`, lists, and cards, including stable list and card IDs.

Use `Dru command <command> '<semantic>'` for a global command. Use `Pal
new/create <bucket>` or `Mate new/create <bucket>` to create buckets. Bucket
commands omit the type, for example `emotion names` and `context names`.

Trello commands are `Trello boards`, `Trello board <board>`, `Trello <board>
sync`, `Trello sync`, `Trello lists`, and `Trello <board> cards`. Trello reads
use committed JSON; sync mirrors accessible non-archived boards, removes
deleted or archived board entities, and removes lists/cards deleted externally.
Creating a local board never creates an external Trello board.

Run the local processor with:

```bash
python3 scripts/process_mutations.py
```

This checkout contains populated typed entity data and its normal provenance
metadata.
