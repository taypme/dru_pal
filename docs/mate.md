# Mate

> **Best for:** one stable name that should collect multiple values over time.

Mate is an append-oriented entity. Instead of creating a new record every time something happens, Mate keeps one name and adds values to its list.

## Example

Imagine a `notes` bucket where you want several notes about the same project:

```text
Mate new notes
notes garden Buy tomato seeds
notes garden Add drip irrigation
notes garden Plant basil near tomatoes
```

Conceptually, Dru stores one `garden` name with three values:

```text
garden
├── Buy tomato seeds
├── Add drip irrigation
└── Plant basil near tomatoes
```

## How Mate stores it

A Mate name is stored once. Its values are kept in order in an array:

```json
{
  "name": "garden",
  "value": [
    "Buy tomato seeds",
    "Add drip irrigation",
    "Plant basil near tomatoes"
  ],
  "type": "mate"
}
```

This is the important difference from Pal: **Pal normally gives each item its own name; Mate lets many values live under one name.**

## Listing names

```text
notes names
```

Expected output:

```markdown
- garden
- website
- workshop
```

The values are not repeated here. `names` is a quick index of the keys available in the bucket.

## Viewing one name

```text
notes view garden
```

Expected output:

```markdown
### garden

1. Buy tomato seeds
2. Add drip irrigation
3. Plant basil near tomatoes
```

The values should be displayed in their stored order.

## Adding another value

```text
notes garden Check soil moisture every morning
```

That appends another value to `garden`; it does not replace the earlier values.

## Common commands

```text
Mate new <bucket>
<bucket> <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> delete <name>
```

## When to use Mate

Use Mate for **grouped lists that grow**: notes about a topic, facts collected about a subject, context attached to a name, or a running list of related values. Use [Cluster](cluster.md) when each addition also needs time-oriented observation data such as a timestamp or intensity.
