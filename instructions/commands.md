# Commands

The exact bare command `Dru` outputs one Markdown table for each concrete entity type, in this order: `Pal`, `Mate`, `Medic`, `Mind`, `Trello`. Each table contains `Bucket` and `Rows`, includes only buckets of that type, and sorts buckets alphabetically by normalized bucket name.

Entity and bucket names are case-insensitive and stored lowercase. Bucket names are globally unique across entity types.

Global bucket commands are `names`, `data`, `view`, `add`, `update`, `delete`, `move`, `pull`, `push`, `mutations`, and `behavior`. `Dru command <command> '<semantic>'` creates or replaces a global command.

Ordinary writes queue `mutations/{{ type }}/{{ bucket }}/{{ uuid }}.json`. Each mutation contains exactly `action`, `selector`, and `json`. `add` uses a null selector. `update`, `remove`, and `move` use the canonical selector `{"field":"<field>","regex":"<regular expression>"}`. Legacy one-key selectors may be read for backward compatibility but must not be generated.

Structural changes queue files under `bucket_mutations/` and run before row mutations. The processors regenerate indexes, packs, and `entity-state.json`; successful mutations are removed. Malformed mutations, unknown buckets, unsafe paths, zero-match updates/removes, and collisions fail without silently discarding the queue.

Run locally with:

```bash
python3 scripts/process_bucket_mutations.py
python3 scripts/process_mutations.py
```
