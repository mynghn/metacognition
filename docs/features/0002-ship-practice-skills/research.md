# 0002-ship-practice-skills — Research

Evidence only. Interpretation belongs in `design-rationale.md`.

## Skill + activation deployment surface (installer)

`install` deploys each KB sibling's rendered `SKILL.md` into `<dest>/<provider>/skills/<name>/` for every provider in `PROVIDERS` (Claude Code → `~/.claude/`, Codex → `~/.codex/`); `--dest` defaults to `~` (`install:300-331`). Activation lives in a single shared `AGENTS.md` at `<dest>/AGENTS.md`, which both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` symlink to (`install:319`, `wiring/README.md:6`). Per sibling, when a trigger `block` exists, `upsert_agents_block(agents_path, block)` writes it (`install:332-334`).

## Activation is a surgical, tier-gated upsert

The installer wraps a sibling's `wiring/<sibling>.agents.md` body in a `<tag>…</tag>` span whose tag is the `stem` with hyphens→underscores (`context-engineering` → `<context_engineering>`). The upsert "replaces only its own `<tag>…</tag>` span and leaves every other block in the shared file byte-for-byte untouched, idempotent on re-run; it never rewrites the file" (`wiring/README.md:8`). Split ownership is explicit: "each sibling's named span is managed by the installer; everything else (the user's operating frame) is the user's" (`wiring/README.md:14`). Activation blocks are emitted only for `tier = everyday` siblings; Common/Situational siblings get description-only discovery, no `.agents.md` (`wiring/README.md:6,10`).

## Authored-skill precedent: `metacognition-maintenance` (special-cased)

A family-level authored skill (`MAINTENANCE = "metacognition-maintenance"`, `install:43`) is deployed by a dedicated `deploy_maintenance(dest, vault)` lane (`install:228-281`), distinct from the sibling render loop. It ships the authored multi-file skill (`SKILL.md` + `references/`) **as-is, not template-rendered** (`install:16-18`), byte-identical to BOTH providers. It emits **no** activation/scheduler artifact — "discovery is the `SKILL.md` description alone" (`install:18,231-232`). A full run or `--only metacognition-maintenance` deploys it; a surgical `--only <sibling>` leaves it alone (`install:316-318,341-344`). No generalized authored-skill lane exists — maintenance is hard-named.

## Generalization via @-token baking

The vault is normalized once to a single absolute path, then baked into every consumer: KB adapters (`@INDEX@`/`@KNOWLEDGE@`), the maintenance skill (`@VAULT@`), and the engine-recorded location (`install:307-311`). `maintenance_tokens(vault)` supplies the absolute `@`-tokens (`install:211-227`); `deploy_maintenance` substitutes them into every shipped file and **raises `SystemExit` if any token is left unbaked** (`install:239-254`). So a deployed artifact is machine-specific while its source stays generic — the existing realization of "no personal paths in shipped skills."

## The practice skills as they exist today (outside the framework)

Extracted from the live personal config (sub-agent sweep of `~/.claude`, `~/.codex`, `~/.local/share/chezmoi`).

- **Shape.** Both `handoff` and `compact-focus` are **single-file** skills (`SKILL.md` only — no `references/`). Contrast maintenance's multi-file tree.
- **Where.** Deployed (Claude only): `~/.claude/skills/{handoff,compact-focus}/SKILL.md`. Chezmoi source: `dot_claude/skills/<n>/SKILL.md.tmpl` + `dot_codex/skills/<n>/SKILL.md.tmpl`, both pulling a shared `.chezmoitemplates/<n>-body.md`. **Codex deploys neither today** (absent from `~/.codex/skills/`).
- **Divergent bodies.** The deployed Claude body ≠ the chezmoi-source body. Deployed = rich, KB-grounded, carries the vault reference. Chezmoi-source = terser, restructured, **no vault reference, no personal content**. `chezmoi apply` would overwrite the rich copies with the terse ones. They are materially different — one must be chosen as canonical.
- **Lone personal element = the vault path.** A full sweep for `nio|socar|/Users/|admin|metacognition|chezmoi|my|username` across all eight skill files returned exactly two hits, both an *optional* "load … if you need the full reasoning" reference: `handoff` → `~/.local/share/metacognition-vault/context-engineering/knowledge/explore-execute-boundary.md`; `compact-focus` → `~/.local/share/metacognition-vault/context-engineering/knowledge/compaction-vs-eviction.md`. No names/emails/org/usernames/first-person phrasing anywhere. No parameterization in place today (raw literal path).
- **Activation blocks live in the shared `~/AGENTS.md`.** Tag `<handoff>` (lines 70–97) drives handoff; tag `<compaction>` (lines 49–68) drives compact-focus — note `<compaction>` ≠ the skill name `compact-focus`. Both blocks reference knowledge by **slug** (`knowledge/{explore-execute-boundary, …}`), not by path — so the activation blocks carry no personal content and need no baking. The deployed `~/AGENTS.md` also diverges in size from its chezmoi source.
- **Provider-specific frontmatter (in chezmoi source).** Claude `.tmpl`: `name`, `description`, `argument-hint`, `allowed-tools: AskUserQuestion`. Codex `.tmpl`: `name`, `description`, `metadata.short-description`, `compatibility: Designed for Codex` (no `argument-hint`). The deployed Claude copies carry only `name`/`description`(/`argument-hint` for handoff).

## `generate` is sibling-only

`generate` scaffolds a new KB **sibling** from `FAMILY.md` (writes `config/<stem>`, `wiring/<stem>`, vault `INDEX.md`, draft `wiring/<stem>.agents.md`) then invokes `install --only <stem>` (`generate:1-36`). It has no bearing on authored practice skills — the practice-skill lane does not touch `generate`.

## Codex runtime facts (2026-06-23, OpenAI Codex docs)

Queried via the OpenAI Codex docs helper; sources: `developers.openai.com/codex/skills`, `/codex/plugins/build`, and the CLI slash-command / configuration / hooks manual sections.

- **Compaction.** Codex `/compact` summarizes the visible conversation. `/compact <focus>` (a focus argument) is **not** reliable — don't depend on it without local testing. Documented patterns: (a) one-off — send a normal message ("When compacting, preserve X/Y/Z and drop A/B/C"), *then* run `/compact`; (b) durable — set `compact_prompt` (inline in `config.toml`) or `experimental_compact_prompt_file`. `PreCompact` / `PostCompact` hooks can run around compaction. → A Codex `compact-focus` must emit a focus *message* + `/compact`, not a `/compact <focus>` command line.
- **Skills home.** Official Codex skills location is `.agents/skills` — repo-scoped `.agents/skills`, user-scoped `~/.agents/skills`. Plugin marketplace files live at `.agents/plugins/marketplace.json` / `~/.agents/plugins/marketplace.json`. Codex config/state stays under `~/.codex` (`config.toml`). `.agents` is **not** deprecated; the skill folder is `.agents/skills` (`.agents` alone is not). **Verdict: `~/.agents/skills` is the more official path than `~/.codex/skills`.**
- **Local state (this machine).** `~/.codex/skills/` is currently populated (the installer's `PROVIDERS` target) and holds Codex's *own* system skills under `.system/` with a `.codex-system-skills.marker` (`skill-creator`, `skill-installer`, `openai-docs`, `imagegen`). `~/.agents/` exists but is empty. Whether current Codex still reads `~/.codex/skills/` as a fallback is unverified — hence the framework-wide path migration is its own issue.
- **Per-provider skill conventions.** Codex frontmatter: `compatibility: Designed for Codex` + `metadata.short-description`, no `argument-hint`. `$ARGUMENTS` is a Claude-Code substitution; Codex does not expand it. `compact_prompt` in `config.toml` confirms Codex's configured-compaction model.
