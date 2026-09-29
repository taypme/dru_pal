# Mind

> **Best for:** thoughts, ideas, knowledge, reasoning, psychology, opinions, and other cognitive material.

Mind gives thinking-oriented information its own place in Dru. It uses named records, so each idea or concept can be listed and opened directly.

## Example

```text
Mind new ideas
ideas add modular_ui Build interface features as replaceable modules
ideas add local_first Keep the user's durable data outside the conversation
```

Conceptually:

| Name | Value |
| --- | --- |
| `modular_ui` | Build interface features as replaceable modules |
| `local_first` | Keep the user's durable data outside the conversation |

## How Mind stores it

A simple Mind record looks like:

```json
{
  "name": "modular_ui",
  "value": "Build interface features as replaceable modules",
  "type": "mind"
}
```

Mind buckets can add fields when needed. An `idea` bucket, for example, might include relationships to other ideas. Users should see those fields through `view` without needing to inspect JSON.

## Listing names

```text
ideas names
```

Expected output:

```markdown
- local_first
- modular_ui
```

## Viewing one name

```text
ideas view modular_ui
```

Expected output:

```markdown
### modular_ui

Build interface features as replaceable modules
```

A record with extra fields should use a readable table or sections:

```markdown
### modular_ui

**Idea:** Build interface features as replaceable modules.

**Related ideas:** plugins, events, composition
```

## Why Mind exists separately from Pal

Mind uses the same dependable named-record foundation as Pal, but its meaning is different. Keeping cognitive information under Mind makes it possible to add reasoning-, idea-, or psychology-specific behavior later without affecting unrelated records.

## Common commands

```text
Mind new <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> update <name> <value>
<bucket> delete <name>
```

Use Mind when the information primarily represents **something thought, known, reasoned, believed intellectually, or invented**.
