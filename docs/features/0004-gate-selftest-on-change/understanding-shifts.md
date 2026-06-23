# 0004-gate-selftest-on-change — Understanding Shifts

## Delta-1: staged-deletes-remain-relevant

Staged deletion records for relevant source paths are part of the local relevance check. The earlier `Design#D-1-selftest-gate-runner` command shape filtered staged paths to additions, copies, modifications, and renames, which excluded deletions even though `Design#D-4-source-relevance-classifier` requires deleted relevant paths to remain relevant. Scope of impact: `Design#D-1-selftest-gate-runner`, `Design#D-4-source-relevance-classifier`.
