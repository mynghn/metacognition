---
name: compact-focus
description: Generate a session-tailored compaction focus so manual compaction keeps the working set and drops noise, in the context-engineering-knowledge-base spirit. Use when the user asks to compact, clear, or condense the session, before a long context-heavy task, or to hand the user a focused compaction directive. The user runs /compact; you cannot.
metadata:
  short-description: Produce a focused session compaction directive
compatibility: Designed for Codex
---

Produce a session-tailored compaction *focus* for THIS conversation. Ground it in the context-engineering knowledge base's compaction discipline — load `@VAULT@/context-engineering/knowledge/compaction-vs-eviction.md` and its siblings for the full reasoning (that KB entry is the authority, not any one session's global-instructions block). Codex's `/compact` does not reliably take a focus argument, so the focus rides in a normal message the user sends *before* running `/compact` — never as an argument on the `/compact` line itself.

Tailor it to the actual session — name the real items, do not emit a generic template:

- **Keep** (only what would otherwise be *lost*): goal, live decisions + their load-bearing rationale, constraints, open threads / next steps. Anything reloadable — rationale already in a doc, shipped code, file:line facts — goes under **Refs**, not restated here.
- **Verbatim**: any must-not-lose instructions and the task statement — tell the summarizer to place these at the very top or bottom of the resulting summary, never buried mid-stack (lost-in-the-middle).
- **Refs**: not payloads — replace bulky content with file paths, commit SHAs, entry slugs, URLs.
- **Drop** (especially the near-relevant): resolved tangents, dead ends, verbose tool output, superseded attempts — and above all any superseded-but-still-on-topic material (a decision since reversed, a near-miss approach since abandoned), which competes with the live answer for attention and is a worse distractor than plainly irrelevant filler.
- Smallest high-signal focus that still lets the work continue.

Lay it out as labeled blocks — `Keep:` / `Verbatim:` / `Refs:` / `Drop:`, each on its own line(s), one directive per line — split any `;`-chained facts, since a packed `Keep:` line is the run-on wall in disguise. Terse content, explicit structure: a clearly delimited focus is followed more reliably by the summarizer (a dense paragraph forces it to infer section boundaries and risks dropping directives), and stays sanity-checkable at a glance.

Write the prose in the language the user uses in their own prompts (not the session aggregate — model output, loaded docs, and code skew English); keep technical anchors — paths, identifiers, code, SHAs, proto names — verbatim.

The complete paste-able message looks like this (content illustrative — name the real items of the session):

<example>
When compacting, preserve the following and drop the rest:
Keep: goal = ship the 0002 v2 fix pass (skill fixes + divergence gate + docs).
Keep: decision = golden-divergence snapshot over composition — cheaper for a two-skill set.
Keep: open = re-author commits as socar-nio, then force-push PR #1.
Verbatim: "all commits authored socar-nio <nio@socar.kr>".
Refs: gate design → docs/features/0002-ship-practice-skills/design.md#D-1.
Refs: skill sources → skills/practice/*/{claude,codex}/SKILL.md.
Drop: the rejected templating/composition path.
Drop: verbose install-selftest logs.
</example>

Output the focus as a single message the user pastes *before* compacting: a leading line `When compacting, preserve the following and drop the rest:` followed by the `Keep:` / `Verbatim:` / `Refs:` / `Drop:` blocks verbatim — then one sentence telling the user to send it and then run `/compact` (you cannot run `/compact` yourself). If you surfaced this proactively rather than on request, add a short note on why now (e.g. session length, before a heavy task). For durable behavior across many compactions, point them at `compact_prompt` / `experimental_compact_prompt_file` in `~/.codex/config.toml` instead.
