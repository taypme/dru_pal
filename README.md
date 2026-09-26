# Dru Pal

Dru Pal is an empty template for a simple ChatGPT data plugin called Dru.

You type short commands. Dru stores the data in GitHub so it is still there in a new chat. Git also keeps a history of changes.

Use this repo as a template when you want to make a new Dru.

## Commands

Start with:

```text
Dru
```

This loads Dru and shows its data groups.

Common commands are:

```text
Dru pull
Dru push
Dru new <entity>
<entity> new <bucket>
<bucket> names
<bucket> data
<bucket> view <name>
<bucket> add <name> <value>
<bucket> update <name> <value>
<bucket> delete <name>
<bucket> move <name> <bucket>
```

`Dru pull` gets the newest data from GitHub.

`Dru push` saves pending changes and updates Dru.

`Dru new <entity>` adds a new kind of data group.

Commands can also be taught special behavior for a bucket.

## Entities

An entity is a kind of data. A bucket is a named group inside it.

The template includes:

- **Pal** — normal records.
- **Mate** — a key with a list of values.
- **Medic** — medical data.
- **Mind** — thoughts, knowledge, and ideas.
- **Heart** — feelings, dreams, wants, and regrets.
- **Trello** — saved Trello boards, lists, and cards.

You can use these or add another entity with `Dru new <entity>`.

## Storage

Dru saves data as JSON in GitHub. The repo is the main copy of the data, not the chat.

This means the data can:

- stay between chats;
- be pulled on another computer;
- be read without ChatGPT;
- keep a Git history;
- be restored from older commits.

Dru checks and processes changes before saving its updated state.

## Using the template

Copy this repo, connect ChatGPT to the new repo, and start adding entities and buckets.

The template starts without your personal data. It gives you the command system, storage system, and included entity types.

Dru Pal's purpose is simple: **make it easy to give ChatGPT commands that store data outside the chat.**
