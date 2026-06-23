# 0005-kb-capture-merit-gate — Understanding Shifts

## Delta-1: test-case-candidate-is-a-pushed-branch

The `concise-not-compressed` test-case candidate lives on the branch
`context-engineering/concise-not-compressed` (vault commit `a0de939`) that is **pushed to origin**,
not a local-only/unpushed commit. Reconciliation must therefore supersede a *pushed* branch — fold
its content into `literal-vs-latent-matching` and delete the branch on origin once that lands — not
merely "avoid pushing a local commit". The round also gains a capstone dogfood task that runs the
**deployed** gate end-to-end on this real branch candidate as integrated acceptance, after the gate
is built, shipped, and routed, and after the entry is reconciled.

- **Kills** the prior premise that `a0de939` is "currently local-only / unpushed" and that
  reconciliation need only "not push as-is" — the branch is already on origin, so deleting it is a
  real, owned obligation.
- **Why**: a maintainer-supplied fact (the candidate is a pushed origin branch) plus a maintainer
  scope addition (an end-to-end deployed-gate dogfood as the round's capstone). Recorded at intake
  from the maintainer's asserted drift; not a contested judgment.
- **Scope-of-impact**: `Tasks#T:V2`, `Tasks#T:D1`. The Requirements `## Upstream` test-case note is
  the factual root corrected. No Spec/Design change — the dogfood validates existing behaviors
  (`Spec#B-2-orthogonality-classifies-new-refresh-reject`,
  `Spec#B-3-authority-mapped-per-claim`, `Spec#C-1-every-create-or-update-is-gated`,
  `Spec#C-2-writes-only-through-the-engine`) on a real case; no new contract.
