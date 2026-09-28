# Commands

The exact bare command `Dru` outputs one separate Markdown table for each concrete entity type, in this order: `Pal`, `Mate`, `Medic`, `Mind`, `Heart`, `Spirit`, `Trello`. Never combine multiple entity types into one table. Precede each table with that entity type as a Markdown heading. Each table contains only the columns `Bucket` and `Rows`, includes only buckets of that entity type, and sorts buckets alphabetically by normalized bucket name. Even when an entity type has no registered buckets, preserve the per-entity separation rather than collapsing entity types into a shared table.

`<entity> buckets` outputs one Markdown table with columns `Bucket` and `Rows` for the named concrete entity type. Entity names are case-insensitive. Include only registered buckets whose type matches the requested entity, sort buckets alphabetically by normalized bucket name, and use `entity-state.json` counts. If the entity type is unknown or abstract, report a concise error.

Entity and bucket names are case-insensitive and stored lowercase. Bucket names are globally unique across entity types.

Global bucket commands are `names`, `data`, `view`, `add`, `update`, `delete`, `move`, `pull`, `push`, `mutations`, and `behavior`. `Dru command <command> '<semantic>'` creates or replaces a global command.

Ordinary writes queue `mutations/{{ type }}/{{ bucket }}/{{ uuid }}.json`. Each mutation contains exactly `action`, `selector`, and `json`. `add` uses a null selector. `update`, `remove`, and `move` use the canonical selector `{"field":"<field>","regex":"<regular expression>"}`. Legacy one-key selectors may be read for backward compatibility but must not be generated.

Structural changes queue files under `bucket_mutations/` and run before row mutations. The processors regenerate indexes, packs, and `entity-state.json`; successful mutations are removed. Malformed mutations, unknown buckets, unsafe paths, zero-match updates/removes, and collisions fail without silently discarding the queue.

Run locally with:

```bash
python3 scripts/process_bucket_mutations.py
python3 scripts/process_mutations.py
```
