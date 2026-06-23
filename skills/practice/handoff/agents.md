<handoff>
Handing off to a fresh session is the cross-boundary sibling of compaction:
at an explore→execute / plan→implement boundary, after a major pivot, or when
a long session should depart for an explicit new goal, prefer a clean fresh
frame over in-place compaction — but only when a fresh frame's clean slate
beats the cost of re-acquiring what is already warm (execution needs a cold
load this session lacks, or the session has rotted; else compact in place or
continue). A handoff is goal-first, not a session summary:
- Lead from the new goal; carry only what that goal consumes. The test is
  "what does the destination need?", not "what happened here?" — drop the
  rest, however central. A faithful summary re-imports the old session's
  noise into the fresh frame, the very thing the fresh frame sheds.
- Keep the load-bearing decisions + rationale, live constraints, and the
  rejected paths + why (the negatives a summary drops but the fresh session
  needs to avoid re-wandering). Replace bulk with reloadable references.
- Carry volume scales with goal-proximity: near-continuous (plan→impl, same
  feature) carries the plan; a sharp departure carries almost nothing.
- Externalize the goal-scoped brief to a durable file (it survives the
  boundary); order the kickoff material-first / instruction-last, and JIT
  the bulk rather than dumping it.
Keep the planning spine (requirement→spec→design→plan) continuous in one warm
session; make the hard cut before execution. The `handoff` skill emits a
tailored brief + kickoff on demand.
Why: mirrors knowledge/{explore-execute-boundary, explore-then-compact-handoff,
compaction-vs-eviction, structured-note-taking, lost-in-the-middle,
prefix-cache-economics}; the boundary is where a session's accumulated rot is
cheapest to shed.
</handoff>
