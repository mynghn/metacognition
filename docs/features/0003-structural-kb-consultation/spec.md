# 0003-structural-kb-consultation — Spec

## Behavior

### B-1: declared-authoring-checkpoint-surfaces-kb
When a supported workflow reaches a declared authoring or curation checkpoint, the agent is presented with the relevant Metacognition KB skill names and the consultation action expected for that checkpoint before the workflow's authoring decision is finalized.

### B-2: relevant-entry-consulted-before-authoring-decision
When a surfaced checkpoint names a KB and the agent proceeds with the authoring decision, the agent consults that KB by reading its index and the fitting entry or entries, or records that the consultation was skipped.

### B-3: nonmatching-work-stays-quiet
When the current turn is ordinary implementation, local investigation, or user-visible work with no declared authoring or curation checkpoint, no Metacognition KB consultation is surfaced by this feature.

### B-4: consumer-workflow-adopts-policy-by-reference
When a consuming workflow opts into structural KB consultation, the workflow declares checkpoint intent and the Metacognition-owned consultation policy supplies the KB-selection and consultation behavior.

### B-5: passed-over-checkpoint-is-reviewable
When a declared checkpoint completes without the expected KB consultation, the missed checkpoint, expected KB, and workflow moment are available for later review.

## Constraint

### C-1: framework-owned-consultation-policy
Metacognition remains the canonical source for consultation policy, KB-selection rules, and shipped consultation wording; consumer workflows expose adoption points without copying or redefining that policy.

### C-2: provider-neutral-contract
The consultation contract is consumable by both supported agent runtimes. Any runtime-specific gap is visible in the feature artifacts and does not silently weaken the other runtime's behavior.

### C-3: jit-kb-loading
Structural surfacing does not preload whole KB corpora. Consultation loads the KB index first and only the fitting entries needed for the checkpoint.

### C-4: evidence-gated-promotion
A candidate consultation mechanism is promoted only after realistic no-cue authoring scenarios show improved relevant-KB consultation over baseline while false surfacing remains within the accepted bound.

### C-5: kb-authoring-specialization-of-0001
This feature remains scoped to KB consultation at authoring and curation checkpoints. It may reuse evidence patterns from `0001-self-initiated-skill-activation`, but it does not claim general no-cue activation for every installed skill.

## Non-goals

- General whole-library self-activation remains outside this feature.
- The feature does not make a consuming workflow the owner of Metacognition's KB-consultation policy.
