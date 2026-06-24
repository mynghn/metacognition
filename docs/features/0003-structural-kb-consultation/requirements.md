# 0003-structural-kb-consultation — Make KB consultation structural at authoring time

## Problem

Metacognition's knowledge-base skills encode the practices an agent should use to manage its own work, but they can still be missed at the exact moments they matter most. In a recent LeanPlan round, Requirements and Design prose depended on context curation and prompt composition, yet the agent did not consult the context-engineering or prompt-engineering KBs until the operator intervened. The current framework gives each KB a discovery description and, for Everyday siblings, an always-loaded reminder block; both paths still depend on the agent recognizing the hidden metacognitive shape of the task while absorbed in a different workflow.

The cost is quiet degradation. Artifacts are weaker than the framework knows how to make them, the operator has to notice and name the missed KB by hand, and each report of "the skill did not pick up" becomes a one-off correction rather than a system improvement. The gap is not that Metacognition lacks knowledge. The gap is that consultation is recognition-dependent where the needed recognition is suppressed.

## Outcome

Metacognition makes KB consultation part of authoring and curation workflows instead of a hoped-for self-reminder. When work reaches a prompt-writing, context-curation, skill-design, or agent-practice authoring point, the relevant KB is surfaced or explicitly considered before decisions harden, while ordinary coding and non-KB-shaped work remain uninterrupted. The confirming signal is a realistic no-cue authoring scenario that would miss today: after the change, the relevant KB is consulted or the non-consultation is reviewable, without broad false surfacing on unrelated scenarios.

User stories:

- **Authoring moment caught** — When an agent writes or revises artifact prose that turns on context, prompt, skill, or agent-practice judgment, the relevant KB consultation is brought into the workflow. The agent no longer has to infer that the visible task is also a prompt/context-engineering moment.
- **Scoped silence elsewhere** — When a turn is ordinary implementation, local investigation, or user-visible work with no KB-shaped decision, the framework stays out of the way. Precision matters because noisy reminders become ignored.
- **Consumer workflows can opt in** — A workflow such as LeanPlan can declare where KB consultation belongs without copying Metacognition policy or becoming the source of truth for it.
- **Misses are reviewable** — When a KB-shaped moment is passed over, there is enough evidence to diagnose whether the surfacing point was absent, mis-scoped, or ignored.

## Guarantee

- **Framework ownership** — Metacognition owns the consultation policy and source artifacts. Consuming workflows may expose adoption points, but they should not fork or hand-maintain the rule.
- **Provider-neutral shape** — The behavior is defined in terms both Claude and Codex can consume, with runtime-specific gaps made explicit rather than hidden.
- **JIT knowledge use** — Surfacing a KB means loading the index and fitting entries, not dumping whole vaults into every turn. The framework preserves the small working set it teaches.
- **Evidence before promotion** — A plausible wording change does not count as a fix until it is checked against realistic misses and false-surfacing risk.

## Non-goals

- **A global "consider every skill" ritual** — This round is not to add a broad every-turn checklist that trains the agent to ignore the framework.
- **A LeanPlan-only patch** — LeanPlan is the observed failure and first adopter candidate, not the owner of the mechanism.
- **Whole-library self-activation** — This feature is about KB consultation at authoring and curation moments, not every installed skill.

## Upstream

- `docs/plans/kb-skill-activation-handoff.md`
- `docs/features/0001-self-initiated-skill-activation`
- `.claude/worktrees/0001-self-initiated-skill-activation/configs/VERDICT.md`
- KB entries consulted: `context-engineering/context-as-working-set`, `context-engineering/jit-loading`, `context-engineering/literal-vs-latent-matching`, `prompt-engineering/explicit-instruction`, `prompt-engineering/role-and-system-framing`, `prompt-engineering/delimiters-and-structure`, `skill-design/description-as-activation-trigger`, `skill-design/skill-evaluation`
