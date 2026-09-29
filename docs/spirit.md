# Spirit

> **Best for:** spirituality, religion, faith, practices, beliefs, meaning, and values understood in a spiritual context.

Spirit gives spiritual material its own semantic space in Dru. It uses named records so beliefs, practices, passages, principles, or other spiritual material can be found by name.

## Example

```text
Spirit new practices
practices add gratitude Write down three things I am grateful for
practices add reflection Spend ten quiet minutes reviewing the day
```

Conceptually:

| Name | Value |
| --- | --- |
| `gratitude` | Write down three things I am grateful for |
| `reflection` | Spend ten quiet minutes reviewing the day |

## How Spirit stores it

A simple Spirit record looks like:

```json
{
  "name": "gratitude",
  "value": "Write down three things I am grateful for",
  "type": "spirit"
}
```

A Spirit bucket can carry more fields when its subject requires them, while keeping the same name-based way of finding records.

## Listing names

```text
practices names
```

Expected output:

```markdown
- gratitude
- reflection
```

## Viewing one name

```text
practices view gratitude
```

Expected output:

```markdown
### gratitude

Write down three things I am grateful for
```

More structured records should still be rendered as readable Markdown rather than raw JSON.

## Why Spirit exists separately from Pal

The storage mechanics are familiar, but the semantic boundary matters. Spirit tells Dru that these records concern spirituality, faith, religious practice, or meaning. Specialized Spirit behavior can therefore evolve independently from general records.

## Common commands

```text
Spirit new <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> update <name> <value>
<bucket> delete <name>
```

Use Spirit when the information is primarily spiritual or religious in meaning. Use [Mind](mind.md) for primarily cognitive ideas and [Heart](heart.md) for primarily affective material.
