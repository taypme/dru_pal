# Medic

> **Best for:** health and medical information that should stay clearly separated from general notes.

Medic uses Dru's named-record model, like Pal, but gives health-related data its own semantic home. A Medic bucket might represent medications, diagnoses, supplements, documents, measurements, or another medical category.

## Example

```text
Medic new supplements
supplements add magnesium Taken in the evening
supplements add vitamin_d Taken with breakfast
```

Conceptually:

| Name | Value |
| --- | --- |
| `magnesium` | Taken in the evening |
| `vitamin_d` | Taken with breakfast |

## How Medic stores it

Each name is stored as an independent record:

```json
{
  "name": "magnesium",
  "value": "Taken in the evening",
  "type": "medic"
}
```

A particular Medic bucket may define additional fields when its subject needs more structure. For example, a medication record can include dosage and frequency. `view` should show those fields in a readable form.

## Listing names

```text
supplements names
```

Expected output:

```markdown
- magnesium
- vitamin_d
```

## Viewing one name

```text
supplements view magnesium
```

Expected output:

```markdown
### magnesium

Taken in the evening
```

For a richer medical record, a view can look like:

```markdown
### example_medication

| Field | Value |
| --- | --- |
| Dosage | 10 mg |
| Frequency | Once daily |
| PRN | No |
```

## Why Medic exists separately from Pal

The storage style is intentionally familiar, but the entity tells Dru **what kind of information it is handling**. That lets medical buckets gain medical-specific commands and behavior without turning every general-purpose Pal bucket into a medical system.

## Common commands

```text
Medic new <bucket>
<bucket> add <name> <value>
<bucket> names
<bucket> view <name>
<bucket> data
<bucket> update <name> <value>
<bucket> delete <name>
```

Use Medic for medical-domain data. Use [Pal](pal.md) when the information has no medical meaning.
