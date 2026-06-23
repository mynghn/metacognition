# Handoff — Implement 0004 Gate/Selftest Auto-Trigger, T:G1

Goal:
Implement `T: G1` for `0004-gate-selftest-on-change`: land the shared root executable `selftest-gate` so CI and the opt-in local hook can invoke one maintained gate runner.

Carry:
- Work in `/Users/admin/.local/share/metacognition/.worktrees/0004-gate-selftest-on-change` on branch `leanplan/0004-gate-selftest-on-change`; git identity there is `mynghn <l.mynghn@gmail.com>`.
- Planning artifacts are untracked under `docs/features/0004-gate-selftest-on-change/`; main checkout is on `main` and should stay untouched.
- `G1` owns `Design#D-1-selftest-gate-runner`, `Design#D-4-source-relevance-classifier`, and `Design#D-5-gate-contract-selfcheck`.
- Runner contract: `./selftest-gate --all`, `./selftest-gate --staged`, `./selftest-gate --install-pre-commit`; fixed suite is `install-selftest`, `generate-selftest`, `maintenance-selftest`, `health-check-selftest`, `no-net-loss-selftest`, `engine/selftest`.
- Completion for `G1`: clean `--all`, failing-suite simulation, staged relevant/irrelevant path cases, and no source rewrite except intentional implementation files.

Negatives:
- Do not implement CI or the local hook in `G1` except enough scaffolding for runner-owned commands; those are `C1` and `L1`.
- Do not call `install-selftest --update-divergence` from automatic enforcement.
- Do not add path filters to CI; Design deliberately keeps CI always-on.
- Do not depend on private vaults, local hooks, GitHub credentials, repository secrets, or account-specific remote state for the authoritative gate.

First moves:
- Re-read `tasks.md` `T: G1`, then `design.md` `D-1`, `D-4`, `D-5`.
- Inspect current selftest command behavior and repo path conventions before coding.
- Implement `selftest-gate` with stdlib-only Python and focused selftests or scripted verification for the runner modes.
- Run `python3 ~/.local/share/leanplan/scripts/validate.py docs/features/0004-gate-selftest-on-change --stage tasks` plus the `G1` completion checks.

Refs:
- `docs/features/0004-gate-selftest-on-change/tasks.md`
- `docs/features/0004-gate-selftest-on-change/design.md`
- `docs/features/0004-gate-selftest-on-change/spec.md`
- `docs/features/0004-gate-selftest-on-change/research.md`
- Existing command surfaces: `install-selftest`, `generate-selftest`, `maintenance-selftest`, `health-check-selftest`, `no-net-loss-selftest`, `engine/selftest`

Drop:
- Earlier LeanPlan stage chatter and allocator/rename history.
- 0002 implementation detail; this feature starts from the finished selftest/gate surface.
- External GitHub docs prose beyond the archived facts in `research.md`.
