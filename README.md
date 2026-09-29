# Dru Pal

Dru Pal is the empty template for Dru, a GitHub-backed ChatGPT data system.

The template contains Dru's entity and bucket schema with empty placeholder storage. It contains no user records, medical records, synchronized board contents, or copied data from a working Dru repository.

## Setup

Create a GitHub repository named `dru` from this template.

Add this to your ChatGPT custom instructions:

```text
When I say "Dru" with an argument, interpret that argument as a GitHub repository. Fetch that repository and hydrate the conversation using INSTRUCTIONS.md. If it's a string with no / character, assume the vendor "{{ username }}" and that the string is the repo name from that vendor. If no repo is specified and the command is just "Dru" assume the repo {{ vendor }}/dru.
```

Replace `{{ username }}` and `{{ vendor }}` with your GitHub username or organization.

## Commands

```text
Dru
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

## Entities

- **[Pal](docs/pal.md)** — general-purpose records.
- **[Mate](docs/mate.md)** — keys with ordered value lists.
- **[Cluster](docs/cluster.md)** — grouped progressing observation logs.
- **[Hoard](docs/hoard.md)** — aggregate string collections.
- **[Medic](docs/medic.md)** — medical-domain records.
- **[Mind](docs/mind.md)** — cognition, knowledge, and ideas.
- **[Heart](docs/heart.md)** — emotions, dreams, desires, and regrets.
- **[Spirit](docs/spirit.md)** — spiritual, religious, faith, and meaning records.
- **[Trello](docs/trello.md)** — synchronized external boards.

## Placeholder schema

Dru Pal registers the same bucket names as the working Dru schema, but every placeholder starts empty. Bucket names define structure only; no row values, source metadata, medical contents, personal observations, Trello cards, or other working-repository data are copied into the template.

## Storage

Row-oriented entities use `entities/<type>/<bucket>/data/` with generated `index.json` and `pack.json`. Hoard buckets use one JSON string array. Trello buckets use one board JSON document.

The repository remains the canonical copy of the data. Git provides persistence and history between chats.
