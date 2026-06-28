# 0006-vault-reference-integrity — Spec

## Behavior

### B-1: dangling-reference-reported
When the check runs and a covered consumer carries a baked vault reference whose target entry does not exist in the vault, the check reports that consumer together with the unresolved target, and signals failure. Every dangling reference found in one run is reported, not just the first.

### B-2: intact-references-pass-clean
When the check runs and every baked vault reference across the covered surfaces resolves to an existing vault entry, the check reports zero danglers and signals success.

## Constraint

### C-1: coverage-framework-surfaces
The check covers exactly the consumer surfaces the framework deploys — the rendered skills into which the installer bakes vault references. Coverage is complete by construction, not by a hand-maintained list that can silently fall behind: a newly deployed consumer carrying a vault reference is covered without a separate registration step, so coverage cannot drift out of sync with what is actually deployed. Surfaces the framework does not own — e.g. the personal global-instruction `CLAUDE.md` operating-frame blocks, authored and managed outside the installer — are outside the check's contract. (Resolves Deferrals#Defer-1-check-surface-scope.)

### C-2: soft-reference-integrity
Every covered consumer→vault reference is a soft pointer, never a hard dependency. A consumer's inline floor stays fully functional when its referenced entry is missing — renamed, retired, or re-homed as the vault evolves — degrading only the optional depth, never the consumer's own output. The check is the sole asserter of reference resolution: it reports a broken reference but never causes a consumer to fail at runtime. This is the observable form of the soft-reference contract whose intent Requirements owns (`Understanding#Delta-1-entry-churn-not-vault-absence`).

### C-3: read-only-on-demand
The check only reads and reports. It never mutates a consumer, the vault, or any repository, and runs only when explicitly invoked — no scheduler, no automatic run. A run leaves every repository's working tree and history untouched.
