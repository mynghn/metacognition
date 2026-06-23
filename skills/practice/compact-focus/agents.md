<compaction>
Compaction is the highest-stakes context-engineering moment in a session — apply
the knowledge-base's own operations to it. When you compact, or recommend the
user run `/compact`, propose a *session-tailored* compaction focus (you
cannot run it yourself — the user applies it):
- Summarize, don't truncate; preserve meaning, compress form.
- Keep the working set: current goal, key decisions + rationale, live
  constraints, open threads / next steps.
- Keep must-not-lose instructions and the task statement verbatim, at the top or
  bottom — never buried mid-summary.
- Replace bulk with reloadable references (paths, commit SHAs, entry slugs, URLs).
- Drop resolved tangents, dead ends, verbose tool output, superseded attempts.
- Smallest high-signal summary that still lets the work continue.
Auto-compaction takes no instructions, so offer the focus when the user signals a
compact or before a long task, and re-establish the working set by these rules
after one happens. The `compact-focus` skill emits a tailored focus on demand.
Why: these mirror knowledge/{compaction-vs-eviction, context-as-working-set,
lost-in-the-middle, jit-loading, structured-note-taking, distractor-sensitivity};
the KB earns its keep only if it governs the session's own compaction.
</compaction>
