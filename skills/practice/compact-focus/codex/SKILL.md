---
name: compact-focus
description: Generate a session-tailored compaction focus so manual compaction keeps the working set and drops noise, in the context-engineering-knowledge-base spirit. Use when the user asks to compact, clear, or condense the session, before a long context-heavy task, or to hand the user a focused compaction directive. The user runs /compact; you cannot.
metadata:
  short-description: Produce a focused session compaction directive
compatibility: Designed for Codex
---

Produce a session-tailored compaction *focus* for THIS conversation, following the `<compaction>` policy in the global instructions (load `@VAULT@/context-engineering/knowledge/compaction-vs-eviction.md` and its siblings if you need the full reasoning). Codex's `/compact` does not reliably take a focus argument, so the focus rides in a normal message the user sends *before* running `/compact` — not in a `/compact <focus>` command.

Tailor it to the actual session — name the real items, do not emit a generic template:

- **Keep** (only what would otherwise be *lost*): goal, live decisions + their load-bearing rationale, constraints, open threads / next steps. Anything reloadable — rationale already in a doc, shipped code, file:line facts — goes under **Refs**, not restated here.
- **Verbatim**: any must-not-lose instructions and the task statement.
- **Refs not payloads**: replace bulky content with file paths, commit SHAs, entry slugs, URLs.
- **Drop**: resolved tangents, dead ends, verbose tool output, superseded attempts.
- Smallest high-signal focus that still lets the work continue.

Lay it out as labeled blocks — `Keep:` / `Verbatim:` / `Refs:` / `Drop:`, each on its own line(s), one directive per line — split any `;`-chained facts, since a packed `Keep:` line is the run-on wall in disguise. Terse content, explicit structure: a clearly delimited focus is followed more reliably (a dense paragraph forces the summarizer to infer section boundaries and risks dropping directives).

Write the prose in the language the user uses in their own prompts (not the session aggregate — model output, loaded docs, and code skew English); keep technical anchors — paths, identifiers, code, SHAs, proto names — verbatim.

Output the focus as a single message the user pastes *before* compacting — a `When compacting, preserve … / drop …` directive carrying the labeled blocks — then one sentence telling the user to send it and then run `/compact` (you cannot run `/compact` yourself). If you surfaced this proactively rather than on request, add a short note on why now (e.g. session length, before a heavy task). For durable behavior across many compactions, point them at `compact_prompt` / `experimental_compact_prompt_file` in `~/.codex/config.toml` instead.
