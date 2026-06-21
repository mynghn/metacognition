# @TITLE@

A personal, version-controlled store of distilled **@TOPIC@** knowledge. Use it to **retrieve** a @NOUN@ on demand, **capture** a new distilled lesson, or **refresh** an entry against current state-of-the-art.

The corpus is provider-neutral and shared; this skill is a thin entry point into it. The store lives in the knowledge vault:

- Index:   `@INDEX@`
- Entries: `@KNOWLEDGE@`

**One mutation channel.** Read entries directly, but never hand-edit them to change the store. Every write goes through the shared engine, which validates the entry's frontmatter, writes it into the vault, upserts the INDEX, and records the change as exactly one commit in the vault repo's own history — so each change is one recoverable commit and the store stays self-consistent. The store changes only when you invoke the engine; nothing mutates it automatically or on a schedule.

## Retrieve (the default action)

Progressive disclosure — load the smallest relevant slice, never the whole corpus:

1. Read `INDEX.md`. Each line is `- [<slug>](knowledge/<slug>.md) — <one-line trigger>`; a line prefixed `⚠ ` is **degraded** (a cited source fell below the authority bar — the entry is preserved but flagged for review).
2. Match the question against the trigger lines; pick the one entry (or few) that fit. **Down-rank a `⚠` degraded entry** — prefer a healthy sibling, and treat a degraded entry's specifics with caution until it is healed.
3. Read only those `knowledge/<slug>.md` file(s). Each entry is self-contained — you do not need its neighbours. Follow a `Related: [[other-slug]]` link only if the question genuinely needs it.

Do not read the entire `knowledge/` directory. The INDEX exists so you load one entry, not all of them.

## Capture (add a new distilled lesson)

When a reusable @TOPIC@ insight is worth keeping:

1. Pick a kebab-case `<slug>`. Check `INDEX.md` first — if the @NOUN@ already exists, **refresh** it instead of adding a duplicate.
2. Author the entry and pipe it to the engine on stdin:

   ```sh
   @ENGINE@ capture <slug> <<'EOF'
   ---
   name: <slug>
   description: <one line — a retrieval trigger: "load when…">
   last_refreshed: <YYYY-MM-DD>
   sources:
     - <citation or url>
   ---

   <distilled, self-contained explanation — usable without any other entry>

   Related: [[<other-slug>]]
   EOF
   ```

3. The engine validates the frontmatter (it refuses an entry with no `sources` or `last_refreshed`), writes the entry into the vault, upserts the INDEX line, and records one commit. The entry is now retrievable by the steps above.

A good entry is distilled (not a transcript), self-contained, grounded in ≥1 authoritative source, and dated.

## Refresh (reconcile an entry against current SOTA)

Refresh is manual and explicit — there is no automatic staleness check; the decision to refresh is always yours.

1. Pick the target `<slug>` from `INDEX.md`.
2. Research current state-of-the-art **with citations** (web search, or the `deep-research` skill).
3. Distill and **reconcile in place**: rewrite the single canonical entry so it supersedes stale claims — do not append a competing view. Restamp `last_refreshed`; refresh `sources`.
4. Apply via the engine (it requires the entry to already exist):

   ```sh
   @ENGINE@ refresh <slug> < updated-entry.md
   ```

`refresh` overwrites the one canonical entry, keeping the slug stable, and commits. There is never a duplicate, and the prior version stays recoverable from git history.
