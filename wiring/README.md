# wiring/

The **discovery-wiring source** — one source per sibling, two files:

- `wiring/<sibling>` — flat `key = value`; its `description` is rendered into **both** provider adapters' frontmatter, always.
- `wiring/<sibling>.agents.md` — the verbatim body of a named trigger block, upserted into the shared `AGENTS.md` (which both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` symlink to) **only for Everyday-tier siblings**. Present iff the sibling is `tier = everyday`.

The installer wraps the `.agents.md` body in a `<tag>…</tag>` whose tag is the `stem` with hyphens as underscores (`context-engineering` → `<context_engineering>`): the tag is single-sourced from the stem, the body from this file. The block is **upserted surgically** — the installer replaces only its own `<tag>…</tag>` span and leaves every other block in the shared file byte-for-byte untouched, idempotent on re-run; it never rewrites the file.

Common / Situational siblings get description-only discovery (no `.agents.md`) — they cost nothing in an agent turn until the work matches. `tier` comes from the per-sibling [`config/`](../config). This consolidates today's hand-maintained, 6×-duplicated wiring.

Discovery wiring is emitted tier-gated. The per-sibling `description` is single-sourced (rendered into both adapters); the tier-gated `AGENTS.md` block is emitted from the same source.

> **Shared file, split ownership.** The shared `AGENTS.md` is only *partly* installer-owned: each sibling's named span is managed by the installer; everything else (the user's operating frame) is the user's. On a personal machine that file may still be chezmoi-managed; until the chezmoi source drops the two sibling spans (so the installer is their sole owner), run the installer against a `--dest` sandbox — not the live `~/AGENTS.md`.
