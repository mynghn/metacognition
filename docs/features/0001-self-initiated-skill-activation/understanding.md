# 0001-self-initiated-skill-activation — UNDERSTANDING

## Delta-1: baseline-now-ships-trigger-first-wiring

The eval baseline (`C0` = current state) already carries the **trigger-first** KB wiring descriptions. So `C0` is no longer the capability-first state the candidate matrix implicitly contrasted against, and the trigger-first-vs-capability-first question is no longer an untested candidate to *introduce* — it is a shipped change to *adjudicate*.

Kills the prior assumption that trigger-first ordering is an unshipped candidate. metacognition main has already adopted it — on a plausibility rationale ("a skill's description is its activation signal, so leading with the trigger sharpens auto-invocation"), the exact unevidenced claim this project exists to settle.

Why (disturbance + verification verdict): external — `29c45d0 refactor(wiring): lead KB descriptions with the activation trigger` landed on `origin/main` and is in HEAD (`merge-base --is-ancestor 29c45d0 HEAD` → true; repo in sync, behind 0 ahead 0). Verified, not inferred: `wiring/tool-design` and both providers' installed adapters now read "Use when …". Evidence archived in research.md#baseline-reflects-shipped-trigger-first-wiring.

Scope of impact (bare anchors — no restatement):
- DESIGN#Decision-1-eval-gated-mechanism-slot — `C0` baseline is trigger-first; the `C3` description-variant arm must add the **capability-first** contrast so the matrix adjudicates whether `29c45d0` earned its keep (keep or revert, with data).
- TASK#Task:R1 — the baseline captured on `C0` now records the trigger-first state.
- TASK#Task:R2 — the candidate matrix's description-variant arm gains the capability-first contrast.
