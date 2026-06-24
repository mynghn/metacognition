# 0001-self-initiated-skill-activation — UNDERSTANDING

## Delta-1: baseline-now-ships-trigger-first-wiring

The eval baseline (`C0` = current state) already carries the **trigger-first** KB wiring descriptions. So `C0` is no longer the capability-first state the candidate matrix implicitly contrasted against, and the trigger-first-vs-capability-first question is no longer an untested candidate to *introduce* — it is a shipped change to *adjudicate*.

Kills the prior assumption that trigger-first ordering is an unshipped candidate. metacognition main has already adopted it — on a plausibility rationale ("a skill's description is its activation signal, so leading with the trigger sharpens auto-invocation"), the exact unevidenced claim this project exists to settle.

Why (disturbance + verification verdict): external — `29c45d0 refactor(wiring): lead KB descriptions with the activation trigger` landed on `origin/main` and is in HEAD (`merge-base --is-ancestor 29c45d0 HEAD` → true; repo in sync, behind 0 ahead 0). Verified, not inferred: `wiring/tool-design` and both providers' installed adapters now read "Use when …". Evidence archived in research.md#baseline-reflects-shipped-trigger-first-wiring.

Scope of impact (bare anchors — no restatement):
- DESIGN#Decision-1-eval-gated-mechanism-slot — `C0` baseline is trigger-first; the `C3` description-variant arm must add the **capability-first** contrast so the matrix adjudicates whether `29c45d0` earned its keep (keep or revert, with data).
- TASK#Task:R1 — the baseline captured on `C0` now records the trigger-first state.
- TASK#Task:R2 — the candidate matrix's description-variant arm gains the capability-first contrast.

## Delta-3: scoped-skills-stay-capability-first

`29c45d0`'s trigger-first reordering covered the five **KB-wiring** skills only. The eval's **scoped** skills — `handoff` and `compact-focus` — are chezmoi-managed, were outside that commit, and **remain capability-first**: each description leads with the capability ("Generate a … brief / `/compact` line"), then a "Use when / at …" trigger clause second. So for what this eval actually measures, `C0` is the **capability-first** state, and trigger-first ordering of the scoped skills is a genuine **unshipped candidate**, not a shipped change to keep-or-revert.

Refines `UNDERSTANDING#Delta-1-baseline-now-ships-trigger-first-wiring`: Delta-1 is right that `29c45d0` shipped trigger-first KB wiring on plausibility, but wrong where it inferred that `C0`'s eval-relevant state is trigger-first and that `C3` must therefore add a *capability-first* contrast — that contrast would only duplicate `C0`. The correct contrast is the reverse: **`C3` is the trigger-first variant of the scoped skills**, against the capability-first `C0`. The eval adjudicates the trigger-first *theory* as applied to the scoped skills; it informs `29c45d0`'s keep/revert question by extension but does not directly measure the KB-wiring skills (out of scope, `SPEC#INV-3-scope-and-measurement-binding`).

Why (disturbance + verification verdict): impl-time inspection of the installed scoped skills at R2 entry. Verified, not inferred: `~/.claude/skills/handoff/SKILL.md` and `~/.claude/skills/compact-focus/SKILL.md` both lead with the capability and place the "Use when/at …" clause second (capability-first). This matches `research.md#baseline-reflects-shipped-trigger-first-wiring` ("compact-focus / handoff … remain capability-first"), the authoritative fact Delta-1's inference had drifted from. The `C0` baseline number is unaffected — `C0` is current state however its descriptions are ordered.

Scope of impact (bare anchors — no restatement):
- UNDERSTANDING#Delta-1-baseline-now-ships-trigger-first-wiring — its KB-wiring fact stands; its `C0`/`C3` scoped-skill inference is corrected here.
- DESIGN#Decision-1-eval-gated-mechanism-slot — `C3` is the trigger-first scoped-skill variant contrasted against the capability-first `C0`.
- TASK#Task:R1 — the recorded baseline is `C0` = capability-first scoped skills (the number stands; only the "trigger-first state" wording was inaccurate).
- TASK#Task:R2 — the description-variant arm is trigger-first, not capability-first.

## Delta-2: corpus-setups-are-not-replayable-turns

A scenario's `setup` is a **third-person description** of the triggering condition, not the **first-person user turn** the agent receives. Fed to the headless driver as the prompt, the agent reasons *about* the scenario instead of *being in* it — so the scoped skill never becomes a live option and the run scores a miss for a replay-fidelity reason, not a behavioral one. Compounding it, a fresh headless process has none of the accumulated state that makes a condition real (compact-focus's "context is heavy" cannot exist one-shot), so most scenarios are not headlessly reproducible at all.

Kills the assumption that "seed the scenario's `setup`" yields a faithful replay. It does not: the baseline it would produce is ~0% self-use across the board — a too-easy, invalid measurement — which the corpus-discrimination invalidation cue forbids trusting.

Why (disturbance + verification verdict): a live pilot of `run-scenarios` on `cf-01` and `ho-01` under `C0` (the live path itself validated: driver → `claude -p` → transcript discovery → scorer all work). Verified, not inferred: in the `cf-01` transcript the agent, handed the description, correctly judged "this is the right moment to compact" and *offered to hand-write a `/compact` line itself* — the exact target failure — yet the compact-focus skill never fired; both scenarios scored 0/1.

Resolution (chosen): each scenario carries a replayable first-person no-cue **`prompt`** the driver injects verbatim, plus a per-scenario **`reproducible`** marker; the driver primes minimal context where feasible and **drops + logs** the scenarios that still cannot be reproduced (the stateful ones), rather than faking a green result.

Scope of impact (bare anchors — no restatement):
- DESIGN#Decision-3-labeled-no-cue-corpus — the schema gains `prompt` (the verbatim replayable turn) and `reproducible` (bool); `setup` stays as the analyst-facing description.
- DESIGN#Decision-4-replayed-headless-driver — the driver injects `prompt`, not `setup`; the reproducibility boundary becomes a per-scenario `reproducible` marker the driver enforces (drop + log), with optional minimal priming.
- TASK#Task:B1 — scenarios carry `prompt` + `reproducible`; reproducible scenarios' prompts are genuine no-cue turns.
- TASK#Task:B4 — the driver injects `prompt` and drops `reproducible:false` scenarios, logged.
