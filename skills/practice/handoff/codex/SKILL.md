---
name: handoff
description: Generate a goal-scoped handoff brief (+ a fresh-session kickoff line) so work crosses a session boundary cleanly, in the context-engineering-knowledge-base spirit. Use at an explore→execute / plan→impl boundary, after a major pivot, or when a long session should depart for an explicit NEW goal in a fresh context. Distinct from compact-focus, which leans the SAME session in place.
metadata:
  short-description: Emit a goal-scoped fresh-session handoff
compatibility: Designed for Codex
---

Produce a durable handoff brief for a FRESH session departing toward an explicit new goal — NOT a summary of this session. Ground it in the KB (load `@VAULT@/context-engineering/knowledge/explore-execute-boundary.md` and its siblings if you need the full reasoning).

**First, decide whether to hand off at all — settle this before building anything.** The new goal is the organizing input: infer it from the user's request, or ask for it (selection is meaningless without a destination). Then gate on whether a fresh frame beats staying — hand off only if execution needs a cold load this session lacks, the session has rotted, or it is a clean explore→execute boundary. If the "new goal" is really "keep doing the same thing," or everything the goal needs is already warm and near-continuous, say so, recommend staying / the `compact-focus` skill, and stop — don't manufacture a handoff. Otherwise, build the brief.

**Select against the goal, not the session.** Carry ONLY what the new goal consumes — the test is "does the destination need this?", never "was this important here?". Drop the rest, however central it was. Carry volume scales with goal-proximity (near-continuous → carries the plan; sharp departure → almost nothing). A faithful session recap is wrong: it re-imports this session's noise into the clean frame.

Write the brief to a durable file (a handoff trapped in chat is lost across the boundary), as labeled blocks, one directive per line:

- **Goal**: the explicit destination, verbatim.
- **Carry**: locked decisions + load-bearing rationale, live constraints, the artifacts/paths the goal builds on.
- **Negatives**: rejected paths + why — the guardrail that stops the fresh session re-wandering. A summary drops these; a handoff must keep them.
- **First moves**: what to load/do first in the fresh session.
- **Refs**: paths, SHAs, entry slugs, URLs — reloadable, JIT, not inlined.
- **Drop**: what the goal does not need (named, so the omission is deliberate).

Bracket the brief with its highest-stakes actionable blocks: **Goal** leads at the top and **First moves** comes last among the actionable blocks (just before the reference-only **Refs**/**Drop**), so neither sits mid-document where a fresh session's recall is weakest (lost-in-the-middle).

Then emit a ready-to-paste fresh-session kickoff: reference the brief file by its PATH at the FRONT (material), the action/instruction at the END (recency); load heavy refs just-in-time rather than pasting them inline (lost-in-the-middle, prefix-cache-economics).

<example>
Brief file — e.g. scratchpad/handoff-<topic>.md:
Goal: <the new goal, verbatim>
Carry: <the locked decision the goal builds on> + <why it's locked>
Negatives: <rejected path> — <why>, so the fresh session won't re-try it
First moves: <what to load / do first>
Refs: <path>, <SHA>, <slug> (reloadable, JIT — not inlined)
Drop: <what the goal does not need>

Kickoff — paste into the fresh session (brief path at the front, action at the end):
scratchpad/handoff-<topic>.md — <one-sentence action to start>
</example>

Write prose in the language the user uses in their own prompts; keep technical anchors — paths, identifiers, slugs, SHAs — verbatim. Output: the brief's file path, then the kickoff line in a code block, then one sentence telling the user to open a fresh session (you cannot do it for them). If you surfaced this proactively, add one line on why now (e.g. boundary reached, session length).
