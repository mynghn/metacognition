# wiring/

The **discovery-wiring source** — one source per sibling, from which the installer emits:

- the `SKILL.md` `description` into **both** provider adapters, always; and
- a named trigger block appended to the shared `AGENTS.md` (which both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` symlink to) **only for Everyday-tier siblings**.

Common / Situational siblings get description-only discovery — they cost nothing in an agent turn until the work matches. `tier` comes from the per-sibling [`config/`](../config). This consolidates today's hand-maintained, 6×-duplicated wiring.

DESIGN Decision-5 (discovery-wiring-emitted-tier-gated). Populated by feature `0004`, task D2.
