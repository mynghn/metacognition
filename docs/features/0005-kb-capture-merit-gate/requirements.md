# 0005-kb-capture-merit-gate — A merit gate in front of KB capture

## Problem

The vault admits a new entry on the engine's **form-gate alone** — valid frontmatter, a non-empty `sources`, a `last_refreshed` date, a unique slug — which checks an entry's *structure*, never its *merit*. So a structurally clean but low-merit entry can join the vault unreviewed, and one did: `concise-not-compressed` was admitted on form alone when on merit it should not have been —

- **not orthogonal** — it overlapped an existing entry (`literal-vs-latent-matching`) so heavily it belonged as a refresh of that entry, not a new concept;
- **unauthoritative at its headline** — its lone citation backed only a supporting sub-claim, lending false authority to a headline that was actually synthesized in conversation;
- **weakly approved** — a bundled "yes" plus the standing "capture durable lessons" directive, with no merit check by anyone.

The maintainer feels this: vault quality erodes as overlapping, under-sourced, or session-local entries accumulate, because nothing sits between a lightweight "yes" and a permanent entry. The engine is form-only *by design* — it is the vault's sole writer and validates structure, not judgment. The gap is a merit checkpoint *in front of* it.

## Outcome

Before any entry is created or updated in the vault, the capture clears a **merit assessment** that the maintainer reviews and decides on — a soft gate whose verdict is recorded, never one that mechanically blocks. The maintainer is the gate; the engine stays the sole writer, and every accepted entry still flows through it.

User stories:

- **See merit before the write** — capturing a lesson surfaces a merit assessment — orthogonality against the existing index, per-claim source authority, distillation, durability, and home/slug fit — before anything is written, so admission turns on merit, not just form.
- **Decide register / refresh / reject** — the maintainer makes the admission call from that assessment; an orthogonality overlap steers the decision toward refreshing the overlapped entry rather than minting a new one, and the accepted decision is routed to the engine's create or update path.
- **Guards updates, not just new entries** — the assessment runs for any create *or* update, so a change to an existing entry is reviewed on merit the same way a first-time capture is.

The gate proves itself on the live failure: applied to `concise-not-compressed`, it surfaces the orthogonality overlap with `literal-vs-latent-matching` (steering to a refresh) and the headline's missing authority — catching what the form-gate let through. The success signal is that every admitted entry carries a maintainer-reviewed merit verdict, and no structurally-valid-but-low-merit entry lands without its merit concerns shown first.

## Guarantee

- **Soft, not hard** — merit, orthogonality, and authority are judgment, not deterministically checkable; the gate guides the check and records the verdict but never mechanically blocks. The maintainer's approval is the admission decision.
- **Engine stays the sole writer** — the gate is a pre-engine checkpoint, not a replacement; the form-gate still runs, and every accepted entry reaches the vault only through the engine, as one recorded write. The gate never bypasses or reimplements it.
- **Authority is per-claim** — each major claim maps to an authoritative source or is explicitly marked synthesized, and a source that backs only a supporting point may not stand in as authority for the headline.

## Non-goals

- **No automated rejection** — the gate does not hard-block or auto-reject; it surfaces concerns and records a verdict for the maintainer to act on.
- **Not curation of admitted entries** — healing or evolving entries already in the vault is the maintenance sibling's role; this gate adjudicates incoming lessons at the moment of admission, including those that land as a refresh.
- **Not staleness detection** — finding and refreshing entries that have gone stale is the freshness sibling's role.

## Upstream

- Originating handoff — `docs/plans/kb-capture-merit-gate-handoff.md` (the merit-gate-vs-form-gate framing and the load-bearing constraints).
- First test case — vault entry `concise-not-compressed` on the pushed branch `context-engineering/concise-not-compressed` (vault commit `a0de939`, on origin): the worked instance the gate must catch; reconcile into `literal-vs-latent-matching` or re-source, and supersede the branch (delete it on origin once reconciled) rather than merging it as-is (`UnderstandingShifts#Delta-1-test-case-candidate-is-a-pushed-branch`).
