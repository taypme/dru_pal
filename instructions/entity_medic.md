# Entity: Medic

Medic is a medical-domain row-oriented JSON entity. It has the same row storage and mutation semantics as Pal while remaining a distinct entity type. Canonical storage is `entities/medic/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Use `Medic new <bucket>` or `Medic create <bucket>` for new Medic buckets. Bucket commands use the standard global row commands.

Every Medic row contains `type: "medic"` after processing.
