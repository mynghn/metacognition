# 0002-ship-practice-skills — Understanding

## Delta-1: codex-needs-per-provider-not-byte-identical

The practice skills require **per-provider** treatment, not byte-identical dual-provider deployment. Codex differs from Claude Code in three ways the original design missed:

- **Compaction focus is a different mechanism.** Codex `/compact` summarizes, but `/compact <focus>` (with an argument) is not reliable; the documented pattern is a normal pre-compaction *message* stating what to keep/drop, then `/compact` — or a durable `compact_prompt` / `experimental_compact_prompt_file`. So `compact-focus`'s Claude shape (emit `/compact <focus>` to paste) does not work on Codex.
- **Frontmatter conventions differ.** Codex uses `compatibility: Designed for Codex` + `metadata.short-description`; Claude uses `argument-hint`. `$ARGUMENTS` is a Claude-Code substitution, not expanded by Codex.
- **The official Codex skills home is `~/.agents/skills/`**, not `~/.codex/skills/` (which the installer uses for every skill today).

This kills the assumption that dual-provider deployment is byte-identical (the original `Design#D-4-byte-identical-frontmatter`, and the single-shared-body premise inside `Design#D-2-canonical-body-and-vault-generalization`). The shared `AGENTS.md` is read by both runtimes, so activation content must be provider-neutral too.

Why: authoritative Codex docs, queried via the OpenAI Codex docs helper on 2026-06-23 — `/compact` slash behavior, configuration prompt overrides, hooks, and the "Agent Skills"/"Build plugins" path convention. Evidence archived in `research.md`.

Scope decision (planner, option **c**): 0002 absorbs per-provider frontmatter + the Codex `compact-focus` body, but **defers** the `~/.agents/skills/` home migration to a separate framework-wide issue (it also fixes sibling/maintenance discovery). 0002 deploys Codex skills via the installer's existing path for now.

Scope-of-impact: `Spec#C-3-deployed-skill-matches-its-runtime` (new), `Design#D-1-practice-skill-lane`, `Design#D-2-canonical-body-and-vault-generalization`, `Design#D-4-byte-identical-frontmatter` (retired), `Design#D-5-per-provider-frontmatter` (new), `Design#D-6-per-provider-body-divergence` (new), `Tasks#T:S1`, `Tasks#T:I1`.
