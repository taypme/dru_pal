# Entity: Mate

Mate is an append-only key/value entity. Canonical storage is `entities/mate/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

A Mate row is `{name, value, type}` where `value` is an array. `<bucket> <key> <value>` appends one value to that key. `Mate new <bucket>` and `Mate create <bucket>` create Mate buckets.

Every Mate row contains `type: "mate"` after processing.
