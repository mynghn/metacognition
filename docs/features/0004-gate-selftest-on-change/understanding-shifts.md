# 0004-gate-selftest-on-change — Understanding Shifts

## Delta-1: staged-deletes-remain-relevant

Staged deletion records for relevant source paths are part of the local relevance check. The earlier `Design#D-1-selftest-gate-runner` command shape filtered staged paths to additions, copies, modifications, and renames, which excluded deletions even though `Design#D-4-source-relevance-classifier` requires deleted relevant paths to remain relevant. Scope of impact: `Design#D-1-selftest-gate-runner`, `Design#D-4-source-relevance-classifier`.

## Delta-2: local-hook-install-is-additive

Installing the local guard into a repository that already has a pre-commit hook preserves the existing hook behavior and adds the gate behavior instead of refusing or deleting the hook content. The earlier local-hook design protected unmanaged hooks by declining to edit them, but the local guard must be enableable without asking maintainers to hand-edit hook scripts. Scope of impact: `Design#D-3-local-pre-commit-hook`, `Tasks#T:L1`.

## Delta-3: install-surfaces-local-guard

The local guard needs a setup-time discovery path because the low-level hook installer is easy to miss. The `install` command remains non-surprising by skipping hook setup in non-interactive runs unless an explicit flag requests it, while interactive full installs can offer the hook as an opt-in local convenience. Scope of impact: `Design#D-3-local-pre-commit-hook`, `Tasks#T:L1`.
