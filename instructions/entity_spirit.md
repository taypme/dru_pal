# Entity: Spirit

Spirit is a spiritual, religious, faith, belief, practice, and meaning-domain row-oriented JSON entity. It has the same row storage and mutation semantics as Pal while remaining a distinct entity type. Canonical storage is `entities/spirit/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Use `Spirit new <bucket>` or `Spirit create <bucket>` for new Spirit buckets. Bucket commands use the standard global row commands.

Every Spirit row contains `type: "spirit"` after processing.
