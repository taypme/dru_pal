# Commands

The exact bare command `Dru` MUST group buckets by concrete entity type. Use this entity order: `Pal`, `Mate`, `Cluster`, `Hoard`, `Medic`, `Mind`, `Heart`, `Spirit`, `Trello`. Output one Markdown heading per entity type followed by one Markdown table containing only `Bucket` and `Rows`. Include only buckets belonging to that entity type, sort them alphabetically by normalized bucket name, and use current `entity-state.json` counts. Preserve the heading and an empty `Bucket | Rows` table for entity types with no registered buckets. NEVER output one combined `Type | Bucket | Rows` table and NEVER mix buckets from different entity types in one table.

`<entity> buckets` outputs one Markdown table with columns `Bucket` and `Rows` for the named concrete entity type. Entity names are case-insensitive. Include only registered buckets whose type matches the requested entity, sort buckets alphabetically by normalized bucket name, and use `entity-state.json` counts. If the entity type is unknown or abstract, report a concise error.

Entity and bucket names are case-insensitive and stored lowercase. Bucket names are globally unique across entity types.

Global bucket commands are `names`, `data`, `view`, `add`, `update`, `delete`, `move`, `pull`, `push`, `mutations`, and `behavior`. `Dru command <command> '<semantic>'` creates or replaces a global command. `categories` is not a command; use `<bucket> names` for grouped names/keys.

## User-facing read output

`<bucket> names` is a quick human-readable index, not a raw JSON response. Output committed names as a Markdown bullet list sorted by normalized name. For Mate and Cluster, list each grouping key once. For Hoard, each stored string is its own name. Trello follows its entity-specific card-name behavior.

`<bucket> view <name>` is a human-readable detail view. Start with `### <name>`. For a simple `{name, value}` row, render the value directly beneath the heading. For arrays, structured objects, or rows with additional useful fields, use Markdown lists, sections, or tables so the user does not need to interpret raw JSON. Preserve all meaningful committed information; formatting for readability must not alter stored data. Cluster and Trello use their entity-specific view formats.

`<bucket> data` may expose the complete committed bucket, but should still prefer readable Markdown when a clear human representation exists.

Row-oriented writes queue `mutations/{{ type }}/{{ bucket }}/{{ uuid }}.json`. Each mutation contains exactly `action`, `selector`, and `json`. `add` uses a null selector. `update`, `remove`, and `move` use the canonical selector `{"field":"<field>","regex":"<regular expression>"}`. Legacy one-key selectors may be read for backward compatibility but must not be generated.

Hoard buckets are aggregate string arrays stored at `entities/hoard/{{ bucket }}.json`. Each array element is itself the bucket value and is addressed as its `name` by Dru commands. `<hoard-bucket> <name>` appends that exact string. `<hoard-bucket> names` outputs the committed strings. Hoard mutations still use the normal mutation envelope; selectors use `field=name`.

Structural changes queue files under `bucket_mutations/` and run before row mutations. The schema normalizer then enforces canonical `name`/`value` grouped rows before mutations are applied. The processors regenerate row indexes/packs where applicable and `entity-state.json`; successful mutations are removed. Malformed mutations, unknown buckets, unsafe paths, zero-match updates/removes, and collisions fail without silently discarding the queue.

Run locally with:

```bash
python3 scripts/rewrite_dru_command.py
python3 scripts/process_bucket_mutations.py
python3 scripts/normalize_name_value_schema.py
python3 scripts/process_append_mutations.py
python3 scripts/process_mutations.py
```
