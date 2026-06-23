# 0005-kb-capture-merit-gate — Spec

## Behavior

### B-1: assessment-precedes-write
When a capture is initiated for a lesson, the gate produces and surfaces a merit assessment covering all five dimensions — orthogonality against the existing index, per-claim source authority, distillation, durability, and home/slug fit — to the maintainer before the engine is invoked. No vault write has occurred at the point the assessment is shown.

### B-2: orthogonality-classifies-new-refresh-reject
The orthogonality dimension compares the candidate against the existing index and yields one classification: new entry, refresh of a named existing entry, or reject. When the candidate overlaps an existing entry, the assessment names that entry and recommends a refresh over a new entry. Worked instance: `concise-not-compressed` is flagged as overlapping `literal-vs-latent-matching` and recommended as a refresh.

### B-3: authority-mapped-per-claim
The source-authority dimension maps each major claim in the candidate to an authoritative source or explicitly marks it synthesized, and flags any headline claim whose only cited source backs a different, supporting point. Worked instance: `concise-not-compressed`'s headline — backed only by a citation for a supporting sub-claim — is flagged as lacking authority.

### B-4: decision-routes-to-engine-operation
When the maintainer decides on a candidate, the decision routes to exactly one outcome: accept-as-new invokes the engine's create operation, accept-as-refresh invokes the engine's update operation against the named entry, and reject invokes no engine operation and leaves the vault unchanged.

## Constraint

### C-1: every-create-or-update-is-gated
Every vault create or update originating from a lesson passes through the gate's assessment before the engine is invoked; no create or update reaches the engine without a preceding assessment.

### C-2: writes-only-through-the-engine
An accepted candidate reaches the vault only through the existing engine, which still applies its own form-gate (frontmatter validity, create-vs-update slug rule, single commit). The gate never writes to the vault directly and never bypasses or reimplements the engine.

### C-3: gate-records-but-never-blocks
The gate records its merit verdict but never mechanically rejects or hard-blocks a candidate; the maintainer's approval is the sole admission decision. A candidate the maintainer accepts despite recorded concerns still proceeds to the engine.

## Non-goals
- Curation of already-admitted entries (the maintenance sibling's role). C-1 gates a write at the moment a lesson is admitted — including a refresh that lesson triggers — not periodic re-curation of the existing corpus.
