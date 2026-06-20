# config/

The **thin per-sibling config** the [`engine/`](../engine) consumes — one entry per sibling capturing exactly what varies between them: `{ topic stem, ENV prefix, INDEX section heading, tier }`. The observed variation across the shipped siblings is this fixed token set, not a templating language (DESIGN Decision-3, rationale: YAGNI).

A sibling's whole surface is `{ template + config + description }` (DESIGN Decision-8) — this directory holds the `config` half.

DESIGN Decision-3 (shared-operations-engine). The field schema lives in [`../templates/sibling-config.schema.md`](../templates/sibling-config.schema.md) (added in E1). The three shipped siblings' instances are authored here in D1 (the installer + engine consume them); M2 does the live cutover (retiring the old per-sibling scripts/adapters), and the generator (`0005`) instantiates new ones. Each sibling's discovery `description` lives alongside in [`../wiring/`](../wiring).
