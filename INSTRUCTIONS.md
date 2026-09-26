# Dru repository instructions

Dru is a GitHub-backed command system whose durable data is organized as typed entities. `Entity` is abstract and cannot be created directly.

## Required instruction loading

`INSTRUCTIONS.md` includes **every Markdown file in `instructions/`**. During hydration, read this file and then read every `instructions/*.md` file from the same exact commit, in alphabetical filename order. All of those files are authoritative parts of these instructions.

## Hydration

Read `INSTRUCTIONS.md`, every `instructions/*.md`, `entity.json`, and `entity-state.json` from one exact branch commit. Validate `entity-state.json.registry_blob_sha` against GitHub's blob SHA for `entity.json`, then validate every registered entity, count, path, and index SHA. Do not fetch row files during hydration. Report the repository, commit, typed entities, counts, pending mutations, and capabilities. End a successful hydration report with `Dru hydrated.`

Dru is a repository convention, not an official ChatGPT plugin. Keep private repositories private and preserve exact external IDs.
