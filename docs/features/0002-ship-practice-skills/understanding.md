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

## Delta-2: per-vendor-is-the-exception-shared-is-default

A v2 review of the *shipped* practice-skill prose against the context-engineering and prompt-engineering knowledge bases reframed the lane: **shared is the default; per-vendor is the exception a skill earns**, not the per-provider-for-everything layout `Design#D-1-practice-skill-lane` originally fixed. Per-vendor bodies are debt — two prose copies to keep in sync — so a skill diverges only where a runtime primitive forces it, and no further. Delta-1 established that some practice skills *must* diverge; Delta-2 establishes that most *must not*, and bounds the rest.

Three changes follow:

- **The lane generalizes to shared-or-per-vendor.** `deploy_practice_skill` accepts either one shared `<name>/SKILL.md` deployed byte-identical to both providers (default) or per-vendor `<name>/<provider>/SKILL.md` (exception). A shared file and a per-vendor dir together is an authoring ambiguity, not a merge — a clean error.
- **A divergence gate enforces minimization.** Each per-vendor skill ships a golden `vendor-divergence` snapshot (content-not-position — the sorted set of provider-unique lines); `install-selftest` asserts the live divergence equals it, so drift in either direction fails until intentionally re-snapshotted, and a semantic check forbids a Claude-only primitive (`$ARGUMENTS`, `/compact <focus>`) in a Codex body. Principle + gate are documented in `skills/practice/README.md`.
- **The bodies ground in the KB, not a personal global block.** The shipped `compact-focus` body cited "the `<compaction>` policy in the global instructions" — the adopter's own operating-frame block, which a clean adopter may not have. It now cites the context-engineering KB entry it loads (`compaction-vs-eviction.md`) as the authority, so a deployed skill is self-grounding and portable — a correction adjacent to `Spec#C-2-shipped-skills-carry-no-author-personal-content`: the discipline rides in the framework's own KB, not in author-specific global instructions.

`handoff` and `compact-focus` stay per-vendor — their divergence (the `/compact <focus>` vs pre-compaction-message delivery, `$ARGUMENTS`, `@`-mention vs plain path) is genuinely runtime-forced (`Design#D-6-per-provider-body-divergence`). Delta-2 does not collapse them; it reframes per-vendor as exception-earned, adds the gate that holds their divergence to the minimum, and grounds their prose in the KB.

Why: the KB review on the shipped SKILL.md prose surfaced both the personal-global-block coupling and a set of distractor/output-format fixes; applying them while still treating per-provider as free divergence would have shipped debt the framework cannot see. The gate makes that divergence visible and bounded.

Scope-of-impact: `Design#D-1-practice-skill-lane` (layout = shared-or-per-vendor + gate), `Design#D-2-canonical-body-and-vault-generalization` (KB-grounding), `Design#D-3-activation-via-surgical-upsert` (skill self-grounds; activation only triggers), `Tasks#T:S1`, `Tasks#T:I1`, and the new principle doc `skills/practice/README.md`.
