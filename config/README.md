# config/

The **thin per-sibling config** the [`engine/`](../engine) consumes — one entry per sibling capturing exactly what varies between them: `{ topic stem, ENV prefix, INDEX section heading, tier }`. The observed variation across the shipped siblings is this fixed token set, not a templating language (rationale: YAGNI).

A sibling's whole surface is `{ template + config + description }` — this directory holds the `config` half.

The shared operations engine consumes these configs. The field schema lives in [`../templates/sibling-config.schema.md`](../templates/sibling-config.schema.md); the installer + engine consume the per-sibling instances, and a future generator instantiates new ones. Each sibling's discovery `description` lives alongside in [`../wiring/`](../wiring).
