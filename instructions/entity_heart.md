# Entity: Heart

Heart is an emotion, attachment, desire, dream, and regret-domain row-oriented JSON entity. It has the same row storage and mutation semantics as Pal while remaining a distinct entity type. Canonical storage is `entities/heart/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Use `Heart new <bucket>` or `Heart create <bucket>` for new Heart buckets. Bucket commands use the standard global row commands.

Every Heart row contains `type: "heart"` after processing.
