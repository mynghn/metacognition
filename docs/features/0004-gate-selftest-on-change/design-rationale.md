# 0004-gate-selftest-on-change — Design Rationale

## D-1: selftest-gate-runner

Use a source-controlled runner instead of duplicating raw shell commands in CI and the local hook. The core force is drift: the moment CI and a hook carry separate command lists, one can stop representing the actual gate while still looking plausible in review.

The rejected alternatives were a workflow-only command list and calling `install-selftest` directly. Workflow-only leaves no reusable local guard. Calling only `install-selftest` misses the other existing selftest entry points recorded in Research. The fixed suite is intentionally blunt: it spends seconds to buy a single verdict surface and avoids premature per-path test selection. If the suite later becomes slow enough to harm routine review, split profiles inside `selftest-gate` while preserving the same CLI as the stable call point.

## D-2: github-actions-authoritative-gate

Make CI always run the gate instead of relying on GitHub path filters. GitHub supports `paths` filters, but its own workflow documentation warns that skipped required checks can remain pending; that is the wrong failure mode for a check meant to be the health signal.

The rejected alternative was a path-filtered workflow keyed only to framework source paths. It would reduce CI runs, but it also moves correctness into GitHub's skip semantics and branch-protection configuration. Running the gate on every PR and branch push is simpler, visible, and still cheap for this repository's stdlib-only selftests. If the cost changes, the safer follow-up is an internal fast-pass result emitted by `selftest-gate`, not a required workflow skipped by path filters.

## D-3: local-pre-commit-hook

Install the local hook as an opt-in convenience, not as the authority. Local hooks catch mistakes earlier, but they are intentionally bypassable and machine-local. CI remains the source of review truth.

The hook installer refuses to overwrite an unknown hook because hook files are executable scripts, not declarative config. Appending blindly can land after an existing `exit`, and replacing blindly can delete a user's local checks. A sentinel-managed block gives idempotence for the hook this feature owns while keeping unrelated local policy outside the framework's ownership.

## D-5: gate-contract-selfcheck

Check the gate's own source-level contract inside the runner because source can verify committed files, but it cannot verify every repository's remote branch-protection settings without credentials. The contract check catches the source-level failures that matter most: the workflow disappears, stops running on PR or branch push, stops calling the shared runner, starts using path filters, or loses executable mode.

The rejected alternative was a GitHub API doctor that checks branch protection in both remotes. That would introduce account-specific authentication and recreate the mynghn/socar split the feature is trying to avoid. If repository-admin enforcement becomes part of the desired contract, it should be a separate authenticated audit command rather than part of the stdlib, clean-checkout gate.
