# Entity: Pal

Pal is a general-purpose row-oriented JSON bucket. Canonical storage is `entities/pal/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Commands include `Pal new <bucket>`, `Pal create <bucket>`, `<bucket> add <name> <value>`, `<bucket> names`, `<bucket> data`, and `<bucket> view <name>`. `Pal new` aliases `Pal create`.

Every Pal row contains `type: "pal"` after processing.
