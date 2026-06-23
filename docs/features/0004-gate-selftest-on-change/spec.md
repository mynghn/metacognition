# 0004-gate-selftest-on-change — Spec

## Behavior

### B-1: guarded-change-produces-selftest-result
When a relevant framework source change enters the guarded review path, the repository automatically runs the framework selftest and attaches a pass/fail result to that change before the change can be read as healthy. The result names the checked source state and the selftest command surface it evaluated.

### B-2: failing-selftest-blocks-healthy-signal
When the automatic selftest fails or cannot complete, the change-associated result is failing and no healthy enforcement signal exists for that source state. The failure report includes enough output for a maintainer to identify the failed selftest check and rerun the same check after fixing the source.

### B-3: local-guard-can-be-enabled
When a maintainer enables the repository's local guard, relevant source changes in the local change path run the same selftest-backed check before handoff to review. A local failure stops the local handoff or requires an explicit bypass, while the guarded review path remains the authoritative enforcement signal.

## Constraint

### C-1: relevant-source-coverage
Every source location whose changes can alter selftest-backed framework invariants is inside the automatic enforcement scope. That includes the installer, selftest entry points, framework configuration and wiring, shipped skills, practice-skill sources, and committed divergence snapshots.

### C-2: current-pass-required-for-health
A relevant change has a healthy enforcement state only when the latest result for that exact source state passed. Stale, missing, skipped, cancelled, timed-out, and failing results are not healthy.

### C-3: framework-homes-have-equivalent-enforcement
The development repository and imported repository expose equivalent enforcement semantics for relevant changes: the same source-change classes are guarded, the same verdict classes are visible, and a missing setup in either home is reported as an enforcement gap rather than accepted as healthy.

### C-4: enforcement-is-verdict-only
Automatic enforcement never rewrites source, regenerates golden divergence snapshots, or repairs generated artifacts. Any re-bless or repair remains a deliberate maintainer action whose resulting source changes are then checked.

### C-5: review-signal-is-clean-checkout-reproducible
The guarded review-path signal is reproducible from the repository source without private maintainer state. Personal vaults, local hooks, or uncommitted files are not required to produce the authoritative result.

## Non-goals

- **Changing selftest verdicts.** The existing selftest-backed invariants are inputs; this spec does not redefine what the installer, practice-skill, maintenance, or divergence checks consider passing.
- **Judging intentional divergence.** A deliberate divergence re-bless remains a reviewer decision. Enforcement proves that the source state is explicit and current; it does not decide whether the new divergence is desirable.
- **Scheduling broader vault maintenance.** This feature may selftest framework maintenance tools, but it does not turn vault health or reconciliation audits into unattended recurring work.
