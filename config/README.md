# config/

The **thin per-sibling config** the [`engine/`](../engine) consumes — one entry per sibling capturing exactly what varies between them: `{ topic stem, ENV prefix, INDEX section heading, tier }`. The observed variation across the shipped siblings is this fixed token set, not a templating language (DESIGN Decision-3, rationale: YAGNI).

A sibling's whole surface is `{ template + config + description }` (DESIGN Decision-8) — this directory holds the `config` half.

DESIGN Decision-3 (shared-operations-engine). Populated by feature `0004`, tasks E1 (schema) / M2 (the three shipped siblings); extended by the generator (`0005`).
