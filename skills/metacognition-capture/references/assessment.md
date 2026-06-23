# The five-dimension merit assessment

Run this **before any engine call** — when it is shown, no vault write has happened yet. Assess the
candidate across all five dimensions, then hand the maintainer the full read plus a *recommended*
verdict. The recommendation is advice; the maintainer decides (see `engine-write.md`).

The candidate is the full entry markdown — frontmatter (`name`, `description`, `last_refreshed`,
`sources`) plus the distilled body. The orthogonality and home/slug dimensions read the target
topic's index at `@VAULT@/<stem>/INDEX.md`; each line there is
`- [<slug>](knowledge/<slug>.md) — <one-line trigger>`, and a `⚠ ` prefix marks an already-degraded
entry.

## 1. Orthogonality — classifies new / refresh / reject

Compare the candidate against the existing index and yield **one** classification:

- **new** — no existing entry covers this ground; admit as a fresh slug.
- **refresh of a named entry** — the candidate overlaps an existing entry's ground. **Name that
  entry** and recommend refreshing it in place rather than adding a near-duplicate. The vault holds
  one canonical entry per concept; a second entry on the same ground is the orthogonality failure
  this dimension exists to catch.
- **reject** — the candidate is redundant with an existing entry and adds nothing, or is out of
  scope for the topic.

Read the index trigger lines, not the whole corpus — match the candidate's concept against them and
pick the overlap, if any.

> **Worked instance.** `concise-not-compressed` overlaps `literal-vs-latent-matching` (both concern
> how retrieval matches surface form vs. meaning). Classification: **refresh of
> `literal-vs-latent-matching`**, not a new entry.

## 2. Per-claim source authority — layers ABOVE the engine host-check

Map **each major claim** in the candidate — the headline especially — to an authoritative source,
or mark it explicitly **synthesized** (the author's own distillation, no external source claimed).
Then **flag any headline claim whose only cited source actually backs a different, supporting
sub-claim** — a citation present in `sources` but supporting a side point, not the entry's main
assertion, leaves the headline effectively uncited.

This is the **judgment layer above** the engine's deterministic gate, not a replacement for it:

- The engine's host-allowlist gate (`sources.authority_violation`) runs underneath every write. It
  is *sole-support-below-bar* and *per-entry*: it refuses an entry only when **no** cited host clears
  the allowlist. An entry with one allow-listed citation passes it — even if that citation supports
  only a sub-claim and the headline is unsupported.
- That per-entry host check therefore **cannot** catch a headline backed only by a sub-claim
  citation; the per-claim source→claim mapping is exactly the gap it defers to the skill's envelope.
  This dimension is that envelope. Do not touch or reimplement the engine's host check — judge claim
  authority above it.

> **Worked instance.** `concise-not-compressed`'s headline is backed only by a citation for a
> supporting sub-claim, so its sole host clears the engine's allowlist (the entry passes the
> deterministic gate) while the headline itself is unsupported. Flag it: **synthesized headline,
> sub-claim-only citation — lacks authority.**

A flag here does not block the write (law 2). It feeds the maintainer's decision, and an
accept-despite-the-flag routes through the `degraded:` marker (see `engine-write.md`).

## 3. Distillation

Is the candidate a *distilled* lesson, not a transcript or a dump? It should state the reusable
insight and be **self-contained** — usable without reading any other entry. Flag a body that is a
narrative of how the insight was reached rather than the insight itself, or that depends on context
no future reader will have.

## 4. Durability

Is the lesson worth keeping — a durable, reusable principle rather than an ephemeral,
situation-specific note that will not generalize or will not still be true later? Flag a candidate
whose value is tied to a one-off context.

## 5. Home / slug fit

- **Topic (home):** does the candidate belong in this `<stem>`, or is its real home another topic?
- **Slug:** is the slug kebab-case and does it name the concept? Check the create-vs-update rule
  against the index — a slug that already exists must be a **refresh**, not a capture (the engine
  enforces this too, but catching it here keeps the verdict honest with dimension 1).

## Output of the assessment

A recommended verdict the maintainer can act on:

- the **orthogonality classification** (new / refresh-of-`<named-entry>` / reject),
- any **authority flags** (headline-vs-sub-claim, unsourced major claims),
- any **distillation / durability / home-slug concerns**.

Surface all of it, then defer to the maintainer's decision.
