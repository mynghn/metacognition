# 0006-vault-reference-integrity — Vault reference integrity

## Problem

When the vault's knowledge evolves — an entry renamed, retired, or re-homed as a topic is re-derived — the surfaces that point *into* the vault are silently left dangling. The `handoff` and `compact-focus` skills, and the operating-frame blocks in personal global instructions, each point at one *specific* vault entry "for the full reasoning." Those pointers are real dependencies, but nothing watches them: when the entry they name moves or disappears, the pointer rots in place — no error, no warning, no signal.

The framework treats these consumers as *independent* of the vault. They are not: each carries the hard-coded location of a specific entry. **The independence is false.** The cost lands twice. The maintainer evolving the vault gets no feedback that an edit just broke a downstream pointer, so broken links silently accrue. The agent that later follows a rotted pointer at runtime silently loses the deeper reasoning it was promised, keeping only its thinner inline fallback.

The vault has a rich *inbound* story — capture, refresh, heal, health-check, no-net-loss all keep entries sound as they change. It has **no outbound story**: nothing verifies that the surfaces pointing *at* the vault still resolve after it changes.

## Outcome

The consumer→vault dependency becomes named and watched, without becoming rigid. The relationship is documented as a deliberate, *soft* contract: each consumer keeps a self-sufficient inline floor that works even with the vault absent, plus an optional pointer into a single canonical entry for depth. And the framework can report, on demand, when any such pointer no longer resolves.

User stories:

- **Maintainer sees broken pointers** — when I evolve the vault (rename, retire, or re-home an entry), I run one check and learn whether any consumer now points at something that no longer exists, getting back the offending consumer and its missing target.
- **Documented contract** — a maintainer reading the architecture finds the consumer→vault reference relationship described as an intentional layered design, so new consumers are built to that shape instead of re-inventing the coupling.

A single check reports every dangling consumer→vault pointer across all consumer surfaces — naming the consumer and its unresolved target — and reports zero against an intact vault. The contract is written where the two-repo rationale already lives.

## Guarantee

- **Soft references only** — the consumer→vault link stays a soft, externally-checked pointer, never a hard import a consumer cannot run without. Why it matters: a hard dependency would make every vault rename break its consumers, *raising* the cost of evolving the vault — the opposite of the goal. Vault evolution must stay cheap; the check is what makes the soft link safe to keep.

## Non-goals

- **Drift / staleness detection** — catching when a consumer's inline floor has fallen *out of sync* with the entry it mirrors (as opposed to the entry being gone). Deferred to a later round.
- **Installer empty-vault guard** — the install-before-clone footgun that materializes a throwaway vault the engine then commits into. Deferred to a later round.
- **Changing the two-repo structure** or how the vault is located / swapped. The separate-repo layout is load-bearing (mutation isolation) and stays; submodule and subtree are rejected.
