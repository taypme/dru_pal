# Dru Pal

Dru Pal is the reusable template for building a Dru repository: a repository-backed command system for storing, organizing, retrieving, and changing structured data through conversational commands.

It starts intentionally empty. Instead of providing a predefined dataset, it provides the command model, entity model, mutation workflow, validation behavior, and repository conventions needed to create a new Dru-backed system.

For a populated real-world implementation, see `taypme/dru`.

## What Dru provides

Dru turns a Git repository into a durable command-driven data layer.

Commands resolve to typed entities and buckets. Writes become explicit mutations. Processors apply those mutations and regenerate derived state. Git records the resulting history.

A Dru-based repository can:

- store structured records in named buckets;
- organize buckets by entity type;
- list, view, add, update, delete, and move data through commands;
- define bucket-specific command semantics;
- support append-only key/value data;
- introduce domain-specific entity types;
- synchronize external systems such as Trello;
- queue and inspect mutations before committing them;
- regenerate indexes and state automatically;
- validate committed data and generated state;
- use Git as a durable audit trail.

Dru Pal contains this behavior without assuming what data your instance should store.

## Command model

The exact command:

```text
Dru
```

hydrates the active repository and renders its registered buckets grouped by entity type.

Once buckets exist, they can be addressed directly:

```text
example names
example data
example view item
example add item "value"
example update item "new value"
example delete item
```

Global commands include:

```text
names
data
view
add
update
delete
move
pull
push
mutations
behavior
```

`Dru pull` refreshes the active repository state.

`Dru push` commits queued changes, processes mutations, regenerates derived state, and refreshes the hydrated view.

Command semantics can also be stored in the repository. A bucket can therefore expose domain-specific behavior rather than functioning only as a generic JSON collection.

## Entity model

An Entity defines how a class of buckets behaves.

Dru Pal includes reusable definitions for several entity types.

### Pal

Pal is the general-purpose row-oriented entity.

Use it when each item should be stored as an independent structured record.

Create a bucket with:

```text
Pal new <bucket>
```

### Mate

Mate is an append-oriented key/value entity.

Each key stores an array of values. This is useful when multiple observations, statements, events, or values belong under one stable key.

Typical usage:

```text
example key "value"
```

### Medic

Medic is a row-oriented entity intended for medical and health-related domains.

It behaves like a specialized Pal while preserving a distinct entity type.

### Mind

Mind is a row-oriented entity intended for cognition, psychology, knowledge, ideas, vocabulary, and related information.

### Heart

Heart is a row-oriented entity intended for emotion, attachment, desire, dreams, and regret.

### Trello

Trello represents synchronized Trello boards as durable local entities.

Useful commands include:

```text
Trello boards
Trello sync
Trello lists
Trello <board> cards
Trello <board> sync
```

A template user does not need to use every entity type. They are building blocks.

## Durable storage

Dru is designed around one principle:

**the repository is the durable source of truth.**

Conversation state can disappear. The committed data remains.

That makes a Dru repository:

- persistent;
- version-controlled;
- inspectable;
- portable;
- scriptable;
- auditable;
- recoverable;
- automation-friendly.

Data can be read or processed by normal tools without requiring ChatGPT.

Generated indexes and state allow a conversation to hydrate the structure and counts of a large repository efficiently without loading every row first.

## Mutations

Dru normally queues changes as mutations before applying them.

A typical lifecycle is:

1. hydrate the repository;
2. issue commands;
3. queue changes;
4. inspect pending mutations if needed;
5. run `Dru push`;
6. process structural mutations;
7. process row mutations;
8. regenerate indexes and state;
9. commit the resulting data.

This approach is safer than directly rewriting generated data because the requested change is represented explicitly and can be validated before becoming canonical state.

Structural mutations support operations such as migrating an entire bucket between entity types.

## Building a Dru repository from this template

Dru Pal is intended to be copied or used as a template repository.

A new instance can decide:

- what data it stores;
- which buckets exist;
- which entity type owns each bucket;
- which commands should be global;
- which commands should be bucket-specific;
- whether new entity types are needed;
- which external systems should be integrated;
- what validation and automation should run after changes.

A typical system grows from a few simple buckets into a domain-specific command interface.

The reusable architecture is:

```text
conversation command
        ↓
Dru command semantics
        ↓
typed entity + bucket
        ↓
mutation
        ↓
processor
        ↓
durable repository data
        ↓
generated state
```

The interface can remain terse even when the backing data model becomes large.

## Example directions

A Dru Pal template could become:

- a personal knowledge system;
- a structured journal;
- a research memory store;
- a project command system;
- a CRM;
- a health-data organizer;
- a writing database;
- a task/workflow engine;
- a domain-specific AI memory layer;
- a synchronized external-data cache.

Entity types and command semantics can evolve with the domain rather than forcing all data into one generic schema.

## Purpose

Dru Pal exists to make it easy to create a persistent conversational data system without starting from scratch.

It provides the reusable foundation:

- command language;
- typed entities;
- structured storage;
- mutations;
- processors;
- generated state;
- validation;
- Git history;
- integration points.

The purpose is not merely to provide a repository layout. It is to provide a pattern for turning a Git repository into a programmable, version-controlled data backend that can be operated naturally through short commands.
