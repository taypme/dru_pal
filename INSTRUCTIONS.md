# Dru repository instructions

Dru is a GitHub-backed command system whose durable data is organized as typed
entities. `Entity` is the abstract base concept and cannot be created directly.
The concrete entity types are `Pal`, `Mate`, and `Trello`.

## Hydration

Read `INSTRUCTIONS.md`, `entity.json`, and `entity-state.json` from one exact
branch commit. Validate `entity-state.json.registry_blob_sha` against GitHub's
blob SHA for `entity.json`, then validate every registered entity, count, path,
and index
SHA. Do not fetch row files during hydration. Report the repository, commit,
typed entities, counts, pending mutations, and capabilities. End a successful
hydration report with `Dru hydrated.`

The exact bare command `Dru` outputs a Markdown table with `Type`, `Bucket`, and
`Rows` for every registered entity, sorted by normalized bucket name. `Dru
command <command> '<semantic>'` creates or replaces a global command that
operates on any bucket. Ordinary global commands are invoked without a `Dru`
prefix.

## Entity and bucket model

Entity and bucket names are case-insensitive and stored lowercase. Bucket names
must be unique across all entity types. A bucket-specific command therefore
uses its bucket directly, for example `emotion names` or `context names`.

Canonical storage is:

```text
entities/pal/{{ bucket }}/data/{{ encoded_name }}.json
entities/mate/{{ bucket }}/data/{{ encoded_name }}.json
entities/trello/{{ board }}.json
```

Pal and Mate buckets also have generated `index.json` and `pack.json` files.
Trello board files are aggregate JSON entities and contain `type`, `name`,
`board_id`, `lists`, and `cards`; every list and card retains its stable
external IDs, and every card has `type: "trello"`.

Every ordinary entity row contains its entity `type`.

## Commands

Global commands operate on any bucket: `names`, `data`, `view`, `add`,
`update`, `delete`, `move`, `pull`, `push`, `mutations`, and `behavior`.

Pal commands operate only on Pal buckets:

```text
Pal new <bucket>
Pal create <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> data
<bucket> view <name>
```

`Pal new` is an alias for `Pal create`, and create is idempotent only when the
bucket does not already exist. `Pal command <command> '<semantic>'` defines a
Pal-specific command system entry.

Mate commands operate only on Mate buckets:

```text
Mate new <bucket>
Mate create <bucket>
<bucket> <key> <string-or-int-value>
<bucket> names
```

Mate values are append-only arrays grouped by key. `context names` is a bucket
command; `Mate names` is not a command. `Mate command <command> '<semantic>'`
defines a Mate-specific command system entry.

## Trello

Trello boards are local entities; creating one never creates an external board.
`Trello new <board>` and `Trello board <board>` create a local board entity only
if it does not already exist. The board name is the UI and command namespace;
the exact external `board_id` is stored with board, list, and card data.

```text
Trello boards
Trello board <board>
Trello <board> sync
Trello sync
Trello lists
Trello <board> cards
```

`Trello sync` mirrors all accessible non-archived boards into the committed
JSON. It removes local board entities for boards that are deleted or archived;
a board sync mirrors the selected board and removes lists/cards no longer
present.
`Trello boards` lists local board entities. `Trello lists` renders all local
lists grouped by board in a table. `Trello <board> cards` renders that board's
cards grouped by list in a table. These reads use committed JSON only;
synchronization is the operation that contacts Trello.

## Mutations and generated state

Ordinary writes queue mutations under
`mutations/{{ type }}/{{ bucket }}/{{ uuid }}.json`. The processor applies
mutations atomically, regenerates indexes, packs, and `entity-state.json`, and
then removes successfully processed mutation files. It rejects malformed
mutations, unknown buckets, duplicate bucket names, unsafe paths, and name
collisions without purging the queue.

Run locally with:

```bash
python3 scripts/process_mutations.py
```

Dru is a repository convention, not an official ChatGPT plugin. Keep private
repositories private and preserve exact external IDs; never synthesize Trello
IDs.
