# Entity: Medic

Medic is a medical-domain row-oriented JSON entity. It has the same row storage and mutation semantics as Pal while remaining a distinct entity type. Canonical storage is `entities/medic/{{ bucket }}/data/{{ encoded_name }}.json`, with generated `index.json` and `pack.json`.

Use `Medic new <bucket>` or `Medic create <bucket>` for new Medic buckets. Bucket commands use the standard global row commands.

Every Medic row contains `type: "medic"` after processing.

## Doc bucket

The `doc` bucket is a Google Drive-backed document index. The actual document file MUST be stored in the Google Drive folder `My Drive/medical/dru` with folder ID `1LiDi4rk_DD2SCcvkrzeieCHbKLjz-9gx`.

For every new Doc:
1. Store or create the actual document in that Google Drive folder first.
2. When the user supplies a Doc name, rename the Drive file to `<doc_name><original_extension>`: the supplied Doc name MUST replace the source basename, while the source file extension MUST be preserved exactly. Example: adding `report.pdf` as `Doc taylor_synopsis` stores the Drive file as `taylor_synopsis.pdf`.
3. Do not append the old basename, change the extension, or infer a different file format merely from the Doc name.
4. Read back the final Drive metadata after any rename/move.
5. Store the exact final Drive filename in the row field `file`.
6. Store the exact Google Drive file ID in `google_drive_file_id`.
7. The Dru row name is the supplied human Dru key and does not replace either Drive reference.
8. Never create a Doc row containing only a local filename or conversation attachment reference.
9. When an auxiliary/OCR Drive document is referenced, store both its exact filename in `google_drive_ocr_file` and its Drive ID in `google_drive_ocr_file_id`.
10. Treat Drive metadata as authoritative when reconciling filename drift for a known Drive ID.

Renaming the Drive folder does not change its ID; use the folder ID as the durable destination locator.
