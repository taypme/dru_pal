# Dru Pal

Dru Pal is the clean starter template for **Dru**, a simple way to give ChatGPT persistent, organized data backed by GitHub.

Instead of keeping important information only inside one conversation, Dru lets you use short commands such as:

```text
ideas names
ideas view modular_ui
ideas add modular_ui Build interface features as replaceable modules
Dru push
```

The durable copy lives in GitHub, so your information can survive new chats, keep a Git history, and remain readable outside ChatGPT.

> **Dru Pal contains structure, not user data.** The examples in this README and the entity guides are documentation only. They are not inserted into the template.

## The basic idea

Dru organizes information in three levels:

```text
Dru
└── Entity        what kind of information this is
    └── Bucket    a named collection
        └── Data  the names and values inside that collection
```

For example:

```text
Mind
└── ideas
    ├── modular_ui
    └── local_first
```

You do **not** need to understand JSON or Git internals to use normal Dru commands.

## Quick start

Create a new GitHub repository from this template and name it `dru`.

Add this to your ChatGPT custom instructions:

```text
When I say "Dru" with an argument, interpret that argument as a GitHub repository. Fetch that repository and hydrate the conversation using INSTRUCTIONS.md. If it's a string with no / character, assume the vendor "{{ username }}" and that the string is the repo name from that vendor. If no repo is specified and the command is just "Dru" assume the repo {{ vendor }}/dru.
```

Replace `{{ username }}` and `{{ vendor }}` with your GitHub username or organization.

Then start a conversation with:

```text
Dru
```

Dru loads the repository and shows the available entities and starter buckets. They begin empty; as you add information, they become your own persistent data.

## Everyday commands

```text
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> add <name> <value>
<bucket> update <name> <value>
<bucket> delete <name>
Dru pull
Dru push
```

### See what is in a bucket

```text
ideas names
```

Typical output:

```markdown
- local_first
- modular_ui
```

### Open one item

```text
ideas view modular_ui
```

Typical output:

```markdown
### modular_ui

Build interface features as replaceable modules
```

### Save changes

```text
Dru push
```

`Dru push` commits pending Dru changes to the repository and refreshes generated state.

Use:

```text
Dru pull
```

to refresh from the newest committed repository data.

## Choosing an entity

An **entity** describes the kind of information a bucket contains. Choose the entity whose behavior best matches what you want to store.

| Entity | Think of it as | Good for |
| --- | --- | --- |
| **[Pal](docs/pal.md)** | One name → one record | General notes and records |
| **[Mate](docs/mate.md)** | One name → growing list | Context, grouped notes, accumulated values |
| **[Cluster](docs/cluster.md)** | One name → observation history | Mood, measurements, intensity, changes over time |
| **[Hoard](docs/hoard.md)** | A simple collection of strings | Queues, vocabulary, tags, short lists |
| **[Medic](docs/medic.md)** | Named medical records | Medications, diagnoses, supplements, health documents |
| **[Mind](docs/mind.md)** | Named cognitive records | Ideas, knowledge, psychology, opinions, reasoning |
| **[Heart](docs/heart.md)** | Named affective records | Emotions, dreams, desires, love, regret |
| **[Spirit](docs/spirit.md)** | Named spiritual records | Faith, religion, practices, beliefs, meaning |
| **[Trello](docs/trello.md)** | A mirrored external board | Trello boards, lists, and cards |

Each guide explains:

- what the entity is for;
- how its data differs from the other entities;
- what the stored data looks like;
- how to add data;
- what `<bucket> names` should return;
- how to use `<bucket> view <name>`;
- what that view should look like for a normal user.

## Creating buckets

Create a bucket by choosing its entity:

```text
Pal new places
Mate new notes
Cluster new focus
Hoard new groceries
Mind new ideas
Heart new dreams
Spirit new practices
Medic new supplements
```

New entity types can also be added with:

```text
Dru new <entity>
```

## How the entities differ

The entity types intentionally store information in different ways:

### Pal

A normal named record:

```text
library → Quiet place to work and read
```

### Mate

One name with a growing ordered list:

```text
garden
├── Buy tomato seeds
├── Add drip irrigation
└── Plant basil
```

### Cluster

One name with a history of timestamped observations:

```text
coding
├── intensity 8 → Deep concentration
└── intensity 5 → More distracted after lunch
```

### Hoard

A flat collection of strings:

```text
apples
coffee
rice
```

### Medic, Mind, Heart, and Spirit

These use named records like Pal, but the entity gives the information a clear semantic home so domain-specific behavior can evolve independently.

### Trello

A Trello bucket mirrors a whole board, including lists and cards, while normal reads come from committed Dru data.

## What this template contains

Dru Pal intentionally includes **structure without user content**:

- all nine standard entity types;
- the current standard bucket placeholders;
- empty row indexes and packs;
- empty Hoard arrays;
- empty Trello board placeholders with no real external IDs;
- command and mutation processors;
- generated state tracking;
- the same user-facing entity documentation as Dru.

It intentionally does **not** include copied:

- personal records;
- medical records;
- observations;
- source-repository metadata;
- Trello cards;
- external board, list, or card IDs;
- working-Dru values.

## Documentation examples are not template data

Examples throughout these docs use harmless sample topics such as places, groceries, projects, ideas, and practices.

For example:

```text
places add library Quiet place to work
places names
places view library
Dru push
```

If **you** run those commands and push them, they become data in your repository. Nothing from the examples is added automatically.

## Where the data lives

Dru saves durable data as JSON in the GitHub repository. GitHub is the persistent copy; the conversation is the interface you use to work with it.

That means your data can:

- survive between conversations;
- keep a Git history of changes;
- be restored from older commits;
- be inspected without ChatGPT;
- be cloned or backed up like a normal repository;
- be extended with new entity types and commands.

You generally do not need to care about storage details during everyday use. The entity guides explain them visually when you want to understand the differences.

## Dru Pal vs. Dru

**Dru Pal** is the reusable starter template.

**Dru** is what the template becomes once it is being used as a real persistent data repository.

The goal is to keep the two aligned in behavior and documentation while keeping Dru Pal free of a particular user's data.

Dru Pal's goal is simple: **make it easy to start a clean Dru and use persistent structured data through ordinary conversation.**
