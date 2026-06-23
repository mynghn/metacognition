# 0005-kb-capture-merit-gate — Research

## Engine capture/refresh contract (engine/kb-engine)

The shared `kb-engine` is the sole writer for every sibling, parameterized by a thin per-sibling config. Evidence (`engine/kb-engine:1-28`, `engine/sources.py`):

- Operations: `capture` (refuses an existing slug → create), `refresh` (refuses an absent slug → update), plus `remove` and `locate`.
- Form-gate (frontmatter): `name` == slug, non-empty `description`, `last_refreshed` present, `sources` present; kebab-case slug only.
- Writes the entry and upserts the slug-sorted INDEX under the configured heading, then records exactly one commit in the vault repo's own history. Verbatim: "Validation, write, and commit all live here, so nothing bypasses them."
- `engine/sources.py` holds the SOURCES.md authority-policy logic, shared with the health-check — an existing, narrower source check than the gate's per-claim authority assessment (B-3). It checks *hosts, not whether a citation supports its claim*; the comment at `engine/kb-engine:369-371` states citation resolve+support is "the skill's envelope, not this deterministic host check."

## Engine affordances the gate reuses

Evidence (`engine/kb-engine`):
- `--trailer KEY:VALUE` (repeatable) on `capture`/`refresh` (`:440-444`) — records a git trailer on the single vault commit; `metacognition-maintenance` already uses it for `Heal-*` provenance.
- `degraded:` frontmatter marker (`:294-297`, `:374-386`) — the deliberate exemption past the source-authority gate; the entry is admitted but down-ranked with a `⚠` prefix in the INDEX, not rejected.
- Entry markdown is read from **stdin** (a TTY is rejected, `:355-356`); the CLI surface is `kb-engine --config <file> [--vault <root>] capture|refresh|remove|locate <slug>`. No pre-write hook / plugin / callback exists — `write_entry()` is one linear function.

## Install model — three lanes, one installer (install, ARCHITECTURE.md)

Evidence (`install`, `ARCHITECTURE.md`, `templates/`):
- **KB siblings** — author-once: shared body `templates/skill-body.md` + per-sibling `config/<stem>` + `wiring/<stem>` (description); `render_adapter()` (`install:75-117`) bakes `@TITLE@ @TOPIC@ @NOUN@ @INDEX@ @KNOWLEDGE@ @ENGINE@` and writes the **byte-identical** string to both `.claude` and `.codex` (`install:451-462`). Divergence is structurally impossible.
- **Practice skills** — hand-authored `skills/practice/<name>/`; shared-by-default, per-vendor by exception (fenced by a `vendor-divergence` golden snapshot in `install-selftest`); deployed by `deploy_practice_skill` (`install:361`).
- **Maintenance skill** — hand-authored multi-file `skills/metacognition-maintenance/` (SKILL.md + `references/`); `deploy_maintenance` (`install:236`) copies to both providers and bakes 8 tokens via `maintenance_tokens()` (`install:219-233`), including `@ENGINE_BIN@` + `@CONFIG_DIR@`; self-prunes orphan reference files. **This is the precedent for the `metacognition-capture` deploy lane (D-1).**
- Install is additive: it does not prune adapters for removed/renamed siblings (`install:36-37`) except the maintenance multi-file deploy.

## Family INDEX — orthogonality reference (vault repo)

Evidence (`/Users/admin/.local/share/metacognition-vault/<stem>/INDEX.md`, `engine/kb-engine:315-341`):
- One INDEX per sibling, in the **vault** repo, engine-maintained (`_upsert_index`), slug-sorted lines: `- [<slug>](knowledge/<slug>.md) — <one-line description>`. The line's description text *is* the entry's frontmatter `description`; a degraded entry is prefixed `⚠`.
- The orthogonality check (B-2) compares a candidate against these one-line descriptions in the target topic's INDEX. `concise-not-compressed` overlaps `literal-vs-latent-matching` (line 23 of `context-engineering/INDEX.md`).

## Sibling boundary clarification

- `metacognition-freshness` checks **framework-install currency** (tooling+vault repos vs remotes, adapter parity) — *not* per-entry staleness. Per-entry decay detection is the read-only `health-check` binary, consumed by `metacognition-maintenance`. (So the gate's "not staleness" boundary is against health-check+maintenance; freshness is a different concern entirely.)
