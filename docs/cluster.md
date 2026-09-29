# Cluster

> **Best for:** repeated observations about the same named thing, especially when **time** and **intensity** matter.

Cluster is Dru's observation-log entity. A Cluster bucket has stable names, and each name can collect a chronological series of observations.

## Example

Imagine tracking how focused you feel:

```text
Cluster new focus
focus coding 8 Deep concentration while building the API
focus coding 5 More distracted after lunch
focus reading 7 Easy to stay engaged with the chapter
```

There are only two names here—`coding` and `reading`—even though `coding` has two observations.

## How Cluster stores it

Each name owns an ordered list of observation objects. Dru adds the timestamp automatically:

```json
{
  "name": "coding",
  "value": [
    {
      "value": "Deep concentration while building the API",
      "intensity": 8,
      "timestamp": "2026-09-29T10:15:00+00:00"
    },
    {
      "value": "More distracted after lunch",
      "intensity": 5,
      "timestamp": "2026-09-29T13:40:00+00:00"
    }
  ],
  "type": "cluster"
}
```

You provide the name, intensity, and observation. Dru handles the timestamp.

## Listing names

```text
focus names
```

Expected output:

```markdown
- coding
- reading
```

`names` lists the subjects being tracked, not every individual observation.

## Viewing one name

```text
focus view coding
```

Expected output:

```markdown
### coding

| Intensity | Observation | Time |
| ---: | --- | --- |
| 8 | Deep concentration while building the API | 2026-09-29 10:15 UTC |
| 5 | More distracted after lunch | 2026-09-29 13:40 UTC |
```

The human-facing output should emphasize the observation history. Users should not need to interpret raw JSON.

## Adding observations

The normal shorthand is:

```text
<bucket> <name> <intensity> <value>
```

For example:

```text
focus coding 9 Finished a difficult debugging session without switching tasks
```

That adds a new observation to the existing `coding` name.

## When to use Cluster

Use Cluster when the question is **"How has this named thing changed over time?"** Good examples include mood, focus, pain, energy, habits, symptoms, confidence, performance, or repeated measurements.

Use [Mate](mate.md) when you only need an ordered list of values and do not need observation metadata. Use [Pal](pal.md) when each name normally represents one record.
