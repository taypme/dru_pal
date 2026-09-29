# Heart

> **Best for:** emotions, attachment, desires, dreams, love, regret, and other affective or personally felt material.

Heart gives feeling-oriented information a clear home in Dru. Like Pal, it uses named records, but the entity itself communicates that the information is about emotional or affective experience.

## Example

```text
Heart new dreams
dreams add ocean_house Living near the ocean in a quiet house
dreams add play_music Perform an original album live
```

Conceptually:

| Name | Value |
| --- | --- |
| `ocean_house` | Living near the ocean in a quiet house |
| `play_music` | Perform an original album live |

## How Heart stores it

A simple Heart record looks like:

```json
{
  "name": "ocean_house",
  "value": "Living near the ocean in a quiet house",
  "type": "heart"
}
```

Heart buckets may use additional fields when the subject calls for them. The important part for the user is that each named item remains easy to list and open.

## Listing names

```text
dreams names
```

Expected output:

```markdown
- ocean_house
- play_music
```

## Viewing one name

```text
dreams view ocean_house
```

Expected output:

```markdown
### ocean_house

Living near the ocean in a quiet house
```

If a Heart record contains more structure, `view` should present it with readable headings, lists, or tables instead of exposing raw storage details.

## Why Heart exists separately from Pal

Heart and Pal can both store named records. Heart adds **meaning**: Dru knows the bucket belongs to the emotional, relational, desire, dream, or regret domain. That separation allows Heart-specific behavior without complicating ordinary Pal data.

## Common commands

```text
Heart new <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> update <name> <value>
<bucket> delete <name>
```

Use Heart when the information is primarily **felt or desired**, rather than simply factual or cognitive.
