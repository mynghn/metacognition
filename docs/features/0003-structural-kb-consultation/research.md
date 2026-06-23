# 0003-structural-kb-consultation — Research

## Current Installer And Wiring Surface

- `install` renders KB sibling adapters into both providers and upserts Everyday sibling `.agents.md` blocks into the shared `AGENTS.md` with `upsert_agents_block()`.
- `install` also ships practice skills through a family-level lane: each skill ships **one shared `SKILL.md` by default, or per-vendor `<provider>/SKILL.md` only when a runtime primitive forces the bodies apart**, plus one provider-neutral `agents.md` span upserted into `AGENTS.md` via `upsert_agents_block()`. A `vendor-divergence` golden snapshot enforced by `install-selftest` holds each per-vendor split to its forced minimum; the shared-default / per-vendor-exception principle is documented in `skills/practice/README.md`.
- The shipped practice bodies are KB-grounded: each cites the context-engineering KB entry it loads as its authority rather than a personal global-instructions block — "activation triggers; the skill self-grounds" (`skills/practice/README.md`, `0002` Delta-2).
- `wiring/README.md` defines split ownership for `AGENTS.md`: installer-owned named spans are replaced surgically; all surrounding user operating-frame content is preserved.
- `wiring/context-engineering.agents.md` and `wiring/prompt-engineering.agents.md` currently rely on "Reach for the ... skill" instructions. The context-engineering block explicitly says the trigger is manual because a strained context may not notice itself.

## 0001 Skill Activation Prior

- The `0001-self-initiated-skill-activation` design in current docs frames the activation mechanism as an eval-gated slot, not a preselected fix.
- The separate `.claude/worktrees/0001-self-initiated-skill-activation/configs/VERDICT.md` records a measured result: a standing skill-consultation checkpoint lifted no-cue handoff self-activation from `0.09` baseline to `0.39 / 0.58` across two runs with `0.00 / 0.00` false-fire.
- The same verdict records that trigger-first scoped-skill descriptions scored `0.00` self-use in that corpus, worse than baseline. The verdict cautions that this measured handoff / compact-focus skills, not KB siblings directly.
- The `0001` scenario corpus and scorer make misses reviewable by joining labeled scenarios, run manifests, and transcript evidence into miss / false-fire worklists plus rates.

## KB Entries Consulted For This Design

- `context-engineering/jit-loading` supports loading indexes first and entries only on demand.
- `skill-design/description-as-activation-trigger` supports treating descriptions as necessary but insufficient Level-1 activation signals.
- `skill-design/skill-evaluation` supports baseline-first, observed-behavior evaluation instead of plausibility-only skill changes.
- `prompt-engineering/role-and-system-framing` and `prompt-engineering/explicit-instruction` support concise standing behavior in the shared operating frame.
