# Cluster

`Cluster` is a concrete name-keyed Dru entity type for grouped, timestamped JSON-object logs. A Cluster bucket stores one row per name. The row `name` is the grouping key and the row `value` MUST be an ordered JSON array of objects. Every object in that array MUST contain a `timestamp` in ISO 8601 form.

The default object fields are `value` (string or scalar observation), `intensity` (integer when supplied by the command), and `timestamp` (the current timestamp in ISO 8601 form). Additional fields may be preserved when migrating existing data. A Cluster observation must never be committed as a bare scalar value.

The default implicit syntax is `<bucket> <name> <intensity> <value>`. Parse the first argument as the row name, the second as an integer intensity, and the remaining text as the exact string value. Create `{"value": <value>, "intensity": <intensity>, "timestamp": <current timestamp>}`. If the named row exists, append the object to its `value` array in order; otherwise queue an add for a new row `{"name": <name>, "value": [<object>]}`.

For generic mutations, imports, migrations, or legacy writes that supply a Cluster row without the canonical array/object shape, Dru MUST normalize it before committing: wrap a bare `value` as an observation object, wrap a single observation object in an array, and automatically add the current ISO 8601 timestamp to every observation that lacks one. Never require the caller to generate the timestamp manually.

`names` lists the committed row names. `categories` is not a Cluster command. `view <name>` renders that named row. Normal Dru mutation commands remain available.
