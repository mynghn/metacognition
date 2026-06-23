<kb_consultation>
Structural KB consultation turns a declared authoring checkpoint into a
deterministic knowledge-base consult — the structural complement to ambient
recognition, which fires only when you happen to notice mid-task that a step is
prompt-, skill-, or context-shaped. A consuming workflow marks the step; this
block — the framework's single source for the policy — expands that mark into the
mapped Metacognition KB skill, a just-in-time consult, and a reviewable marker.
Consumers declare intent only; the skill names, the mappings, and this wording
live here, never copied into the workflow.

Act only on a declared checkpoint. When a workflow step carries a
`KB-CHECKPOINT[<intent>, ...]` marker, run the protocol below before that step's
authoring or curation decision is finalized. With no such marker, surface
nothing — ordinary implementation, investigation, and user-facing work draw no KB
from this block.

Intent registry — the only intents this block resolves:
- `context-curation` -> context-engineering-knowledge-base
- `prompt-authoring` -> prompt-engineering-knowledge-base
- `skill-authoring` -> skill-design-knowledge-base
- `tool-contract` -> tool-design-knowledge-base
- `agent-flow` -> agent-architectures-knowledge-base
- `agent-runtime` -> agent-runtime-knowledge-base
- `eval-observability` -> evaluation-observability-knowledge-base

For each intent the checkpoint lists, in its listed order:
1. Resolve it to its KB skill via the registry. An intent the registry does not
   list is reported, not guessed: emit
   `KB-SKIPPED[<intent>]: unknown checkpoint intent` and invent no mapping.
2. Consult the mapped KB skill index-first — read its INDEX, then load only the
   entries that fit the checkpoint; never the whole vault.
3. Emit one marker for that intent, verbatim on its own line, starting with the
   literal `KB-CONSULTED[` or `KB-SKIPPED[` token (never reworded into prose) — in
   the turn transcript, not the authored artifact (unless the workflow asks for
   artifact-local provenance), before or alongside the authoring output:
   - consulted, fitting entries read — `KB-CONSULTED[<intent> -> <skill>: <slug>, ...]`
   - consulted, index held no fitting entry — `KB-CONSULTED[<intent> -> <skill>: INDEX-only]`
   - deliberately not consulted — `KB-SKIPPED[<intent> -> <skill>]: <reason>`

Marker grammar. `<skill>` is the mapped skill name; each `<slug>` is a consulted
entry's slug (its vault filename without `.md`). Intents, skills, and slugs are
lowercase-hyphen tokens free of the marker delimiters (`:`, `,`, `]`, `->`), so
the bracketed `[...]` head alone classifies a marker: `KB-SKIPPED[<intent>]` with
no `-> <skill>` is the unknown-intent case above, distinct from a deliberate
`KB-SKIPPED[<intent> -> <skill>]` whatever its free-text `<reason>`. `INDEX-only`
and `unknown checkpoint intent` are exact reserved phrases; spacing around `,` and
`->` is not significant. A multi-intent checkpoint emits its markers together, one
line per intent — e.g. `KB-CHECKPOINT[prompt-authoring, skill-authoring]` produces:
`KB-CONSULTED[prompt-authoring -> prompt-engineering-knowledge-base: explicit-instruction, positive-instruction]`
`KB-CONSULTED[skill-authoring -> skill-design-knowledge-base: INDEX-only]`

The marker is the review surface: a consulted checkpoint names the entries that
shaped the decision, a skipped one states why — so a passed-over checkpoint stays
auditable instead of silent. This block carries only the routing and the
procedure; the KB skills it routes to self-ground when consulted.
Why: structural checkpoints close the recognition-dependent gap that ambient KB
triggers leave open — a step a workflow declares prompt- or skill-shaped consults
the KB whether or not the agent thought to, and the marker turns each
consult-or-skip into a reviewable signal.
</kb_consultation>
