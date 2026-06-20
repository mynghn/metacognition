# config/

The **thin per-sibling config** the [`engine/`](../engine) consumes — one entry per sibling capturing exactly what varies between them: `{ topic stem, ENV prefix, INDEX section heading, tier }`. The observed variation across the shipped siblings is this fixed token set, not a templating language (DESIGN Decision-3, rationale: YAGNI).

A sibling's whole surface is `{ template + config + description }` (DESIGN Decision-8) — this directory holds the `config` half.

DESIGN Decision-3 (shared-operations-engine). The field schema lives in [`../templates/sibling-config.schema.md`](../templates/sibling-config.schema.md) (added in E1); per-sibling instances are authored in M2 (the three shipped siblings) and by the generator (`0005`).
