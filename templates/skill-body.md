# @TITLE@

A personal, version-controlled store of distilled **@TOPIC@** knowledge. Use it to **retrieve** a @NOUN@ on demand, **capture** a new distilled lesson, or **refresh** an entry against current state-of-the-art.

The corpus is provider-neutral and shared; this skill is a thin entry point into it. The store lives in the knowledge vault:

- Index:   `@INDEX@`
- Entries: `@KNOWLEDGE@`

**One mutation channel.** Read entries directly, but never hand-edit them to change the store. Every write goes through the shared engine, which validates the entry's frontmatter, writes it into the vault, upserts the INDEX, and records the change as exactly one commit in the vault repo's own history — so each change is one recoverable commit and the store stays self-consistent. New lessons and refreshes reach that engine through the `metacognition-capture` merit gate (see **Capture** / **Refresh** below), never by calling the engine from here; nothing mutates the store automatically or on a schedule.

## Retrieve (the default action)

Progressive disclosure — load the smallest relevant slice, never the whole corpus:

1. Read `INDEX.md`. Each line is `- [<slug>](knowledge/<slug>.md) — <one-line trigger>`; a line prefixed `⚠ ` is **degraded** (a cited source fell below the authority bar — the entry is preserved but flagged for review).
2. Match the question against the trigger lines; pick the one entry (or few) that fit. **Down-rank a `⚠` degraded entry** — prefer a healthy sibling, and treat a degraded entry's specifics with caution until it is healed.
3. Read only those `knowledge/<slug>.md` file(s). Each entry is self-contained — you do not need its neighbours. Follow a `Related: [[other-slug]]` link only if the question genuinely needs it.

Do not read the entire `knowledge/` directory. The INDEX exists so you load one entry, not all of them.

## Capture (add a new distilled lesson)

When a reusable @TOPIC@ insight is worth keeping, **route it through the `metacognition-capture` gate** — the family's admission front door — rather than writing it from here. This skill never calls the engine's write path directly; every new entry is admitted through the gate.

Hand the candidate lesson to `metacognition-capture` for the **@TOPIC@** topic. Naming the topic lets the gate read this topic's `INDEX.md` for its orthogonality check and target this topic's engine config. The gate then assesses the candidate's merit, surfaces a verdict for your decision, and — only on your approval — makes the single engine write itself: a new entry, or a refresh if the candidate overlaps an existing one (check `INDEX.md` first; the gate steers an overlap to a refresh rather than a duplicate).

A good entry is distilled (not a transcript), self-contained, grounded in ≥1 authoritative source, and dated — exactly what the gate's assessment checks before admission.

## Refresh (reconcile an entry against current SOTA)

Refresh is manual and explicit — there is no automatic staleness check; the decision to refresh is always yours. A refresh is a vault write, so it **routes through the same `metacognition-capture` gate**, not a direct engine call:

1. Pick the target `<slug>` from `INDEX.md`, and research current state-of-the-art **with citations** (web search, or the `deep-research` skill).
2. Distill and **reconcile in place**: rewrite the single canonical entry so it supersedes stale claims — do not append a competing view. Restamp `last_refreshed`; refresh `sources`.
3. Hand the reconciled entry to `metacognition-capture` for the **@TOPIC@** topic as a refresh of `<slug>`. The gate assesses it and, on your decision, issues the `refresh` write — slug stable, the one canonical entry superseded (never a duplicate), the prior version recoverable from git history.
