# Entity: Mind

Mind is a cognition, psychology, knowledge, and ideas-domain row-oriented JSON entity. It has the same row storage and mutation semantics as Pal while remaining a distinct entity type. Canonical storage is `entities/mind/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Use `Mind new <bucket>` or `Mind create <bucket>` for new Mind buckets. Bucket commands use the standard global row commands.

Every Mind row contains `type: "mind"` after processing.
