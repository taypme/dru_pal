# Dru repository instructions

Dru is a GitHub-backed command system whose durable data is organized as typed entities. `Entity` is abstract and cannot be created directly.

## Required instruction loading

`INSTRUCTIONS.md` includes **every Markdown file in `instructions/`**. During hydration, read this file and then read every `instructions/*.md` file from the same exact commit, in alphabetical filename order. All of those files are authoritative parts of these instructions.

## Entity creation

`Dru new <entity>` creates a new concrete entity type named `<entity>`. Add the entity type to the registry, create `instructions/entity_<entity>.md`, and update the mutation and structural-mutation processors so the new entity can store buckets and use normal Dru commands. Keep the implementation generic so adding an entity does not require hard-coded changes in unrelated entity definitions.

## Hydration

Read `INSTRUCTIONS.md`, every `instructions/*.md`, `entity.json`, and `entity-state.json` from one exact branch commit. Validate `entity-state.json.registry_blob_sha` against GitHub's blob SHA for `entity.json`, then validate every registered entity, count, path, and index SHA. Do not fetch row files during hydration.

On every successful hydration, the user-visible hydration report MUST explicitly list every typed entity, every bucket belonging to each entity, and the row count for every bucket. This entity → bucket → row-count listing is mandatory and MUST NOT be omitted, summarized away, or replaced by only aggregate entity counts. Also report the repository, commit, pending mutations, and capabilities. End the report with `Dru hydrated.`

## Bare Dru command after hydration

When the user's entire message, after trimming whitespace, is exactly `Dru` and it is not the first message in the conversation, output the current Dru status in the same entity → bucket → row-count format required by the hydration report: one Markdown heading per concrete entity type and one Markdown table beneath it containing only `Bucket` and `Rows`, including every registered bucket of that type and its current `entity-state.json` row count. Also report the active repository, exact commit, total row count, pending mutations, and capabilities, and end with `Dru hydrated.` Refresh from the active repository first when necessary so the report reflects the current committed state. Do not replace this output with a short acknowledgment such as "Dru context remains hydrated" or "ready for the next operation."

Dru is a repository convention, not an official ChatGPT plugin. Keep private repositories private and preserve exact external IDs.
