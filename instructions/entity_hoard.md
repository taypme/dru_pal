# Hoard

`Hoard` is a concrete aggregate Dru entity type. Each Hoard bucket is stored as one JSON array of strings at `entities/hoard/<bucket>.json`; it has no per-value row files, indexes, or packs.

Each string is the value and is addressed by Dru as its `name`. The default implicit syntax is `<bucket> <name>` and appends that exact string. `names` returns the committed strings. `data` renders the array. `view <name>` resolves the matching string. `add`, `update`, `delete`, and `move` use the normal Dru mutation envelope with selectors using `field=name`.

Use `Hoard new <bucket>` or `Hoard create <bucket>` for new Hoard buckets.
