# 0004-gate-selftest-on-change — Research

## Current Automation Surface

- `.github/` is absent in the checked-out repository; no workflow files were present.
- No repository `Makefile` or pre-commit configuration file was found at depth two or above.

## Current Selftest Surface

- `install-selftest` includes installer, maintenance-skill, practice-skill, and vendor-divergence checks.
- `install-selftest --update-divergence` regenerates the committed `skills/practice/<name>/vendor-divergence` snapshots for per-vendor practice skills.
- Other selftest entry points present at the repository root include `maintenance-selftest`, `no-net-loss-selftest`, `generate-selftest`, `health-check-selftest`, and `engine/selftest`.

## GitHub Actions Semantics

- GitHub workflow files must live under `.github/workflows/` and can trigger on one or more events through `on`: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- `push` and `pull_request` support `paths` filters, but a workflow skipped by path filtering leaves associated required checks in a pending state: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore
- The `actions/checkout` repository currently documents Checkout v7, with v4 still described as checking the repository out under `$GITHUB_WORKSPACE`: https://github.com/actions/checkout
