# Pal

> **Best for:** ordinary named information that does not need a more specialized Dru entity.

Pal is Dru's general-purpose entity. Think of a Pal bucket as a small collection of named notes or records. Each name points to one value.

## Example

Suppose you create a bucket for favorite places:

```text
Pal new places
places add library Quiet place to work and read
places add canyon Good place for an evening walk
```

Conceptually, Dru now knows:

| Name | Value |
| --- | --- |
| `library` | Quiet place to work and read |
| `canyon` | Good place for an evening walk |

## How Pal stores it

Pal keeps each named item as its own JSON record. You do not need to work with the JSON directly, but a record looks roughly like this:

```json
{
  "name": "library",
  "value": "Quiet place to work and read",
  "type": "pal"
}
```

This makes Pal a good fit when every item has its own stable name and should be independently viewed, changed, moved, or deleted.

## Listing names

```text
places names
```

Expected output:

```markdown
- canyon
- library
```

`names` shows the committed names in the bucket. It does not dump the full values.

## Viewing one name

```text
places view library
```

Expected output:

```markdown
### library

Quiet place to work and read
```

If the record contains additional fields, `view` should show them clearly rather than hiding them.

## Common commands

```text
Pal new <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> update <name> <value>
<bucket> delete <name>
```

## When to use Pal

Use Pal when you mainly need **a name and a value**. If repeated values should accumulate under the same name, use [Mate](mate.md). If observations should accumulate over time with timestamps and intensity, use [Cluster](cluster.md). If you only need a simple collection of strings, use [Hoard](hoard.md).
