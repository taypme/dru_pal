# Hoard

> **Best for:** a simple collection of strings where every item stands on its own.

Hoard is Dru's simplest collection type. There are no separate name/value records. The string itself is the item and its name.

## Example

A `groceries` bucket might contain:

```text
groceries apples
groceries coffee
groceries rice
```

Conceptually, it is simply:

```text
apples
coffee
rice
```

## How Hoard stores it

The entire bucket is one JSON array:

```json
[
  "apples",
  "coffee",
  "rice"
]
```

There is no object around each item and no separate `name` or `value` field. This keeps simple collections simple.

## Listing names

```text
groceries names
```

Expected output:

```markdown
- apples
- coffee
- rice
```

For Hoard, `names` is effectively the collection itself because every string is its own name.

## Viewing one name

```text
groceries view coffee
```

Expected output:

```markdown
### coffee

coffee
```

There is no hidden value behind `coffee`; the string itself is the stored value.

## Common commands

```text
Hoard new <bucket>
<bucket> <name>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> delete <name>
```

## When to use Hoard

Use Hoard for things like vocabulary, tags, queues, shopping items, short reminders, or any collection where a plain string is enough.

If every name needs a separate description or value, use [Pal](pal.md). If one name should collect several values, use [Mate](mate.md).
