# Trello

> **Best for:** keeping a readable Dru mirror of Trello boards, lists, and cards.

Trello is different from the other Dru entities because its data comes from an external board. Dru keeps a local JSON mirror so you can inspect the board through normal conversation commands without contacting Trello for every read.

## Example

Imagine a board named `projects` with two lists:

```text
Projects
├── To Do
│   ├── Build landing page
│   └── Write documentation
└── Done
    └── Create repository
```

## How Trello stores it

A whole board is stored together in one JSON file. A simplified example looks like:

```json
{
  "type": "trello",
  "name": "projects",
  "board_id": "external-board-id",
  "lists": [
    {
      "name": "To Do",
      "list_id": "external-list-id"
    }
  ],
  "cards": [
    {
      "name": "Build landing page",
      "card_id": "external-card-id",
      "list_id": "external-list-id"
    }
  ]
}
```

The IDs come from Trello and are preserved exactly. Dru does not invent replacements for them.

## Listing names

For a Trello board, the standard `names` view lists the committed card names:

```text
projects names
```

Expected output:

```markdown
- Build landing page
- Create repository
- Write documentation
```

You can also use Trello-specific commands when you want board structure rather than a simple name index:

```text
Trello lists
Trello projects cards
```

## Viewing one name

```text
projects view Build landing page
```

Expected output:

```markdown
### Build landing page

| Field | Value |
| --- | --- |
| Board | projects |
| List | To Do |
| Card | Build landing page |
```

Other useful card fields, such as description or due date, should be shown when they exist. External IDs are implementation details and do not need to dominate the normal user-facing view.

## Synchronizing

```text
Trello sync
```

Synchronizes accessible boards into Dru.

To synchronize one board:

```text
Trello projects sync
```

Reads such as `names`, `view`, `lists`, and `cards` use the committed Dru mirror. This keeps normal reads fast and predictable.

## When to use Trello

Use Trello when the source of truth is a Trello board and you want Dru to understand its lists and cards. For information created directly inside Dru, choose one of the native entities such as [Pal](pal.md), [Mate](mate.md), [Cluster](cluster.md), or [Hoard](hoard.md).
