# 0006-vault-reference-integrity — Deferrals

## Defer-1: check-surface-scope (resolved -> Spec#C-1-coverage-framework-surfaces)

**Owning stage**: Spec

**Question** — which consumer surfaces does the reference check cover? It surfaced now because the Outcome says "all consumer surfaces," but the concrete set spans different homes and lifecycles: framework-deployed skills (`handoff`, `compact-focus`, and any other installed skill) versus the personal global-instruction blocks (chezmoi-managed, not framework-owned). Whether the check reaches into surfaces the framework does not own is a real boundary decision, not a wording detail.

**Forces** — broader coverage catches more real dangling pointers (the `CLAUDE.md` operating-frame blocks do enumerate vault entries), but a tooling-repo check that reads personal, chezmoi-managed config crosses an ownership boundary and couples the framework to a surface it can neither install nor guarantee. How the check *discovers* the consumer→entry references (scan-for-pattern vs. a declared consumer registry) also bears on how cheaply a new surface is brought into scope.

**Option seen (not chosen)** — restrict to framework-owned surfaces first and leave personal config out of scope. Recorded only as a candidate for Spec to weigh against its then-current option space, not a decision.
