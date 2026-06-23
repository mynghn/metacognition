# 0002-ship-practice-skills — Design Rationale

## D-1: practice-skill-lane

The forcing function is `Spec#B-1`'s set-keying — "a later-added practice skill deploys the same way without bespoke per-skill steps." Two existing patterns each fail half of that:

- **Hard-named, like `MAINTENANCE`.** The maintenance lane is a single named constant with its own `deploy_maintenance`. Cloning that per practice skill means every new skill edits `install` — the opposite of set-keyed. Rejected.
- **Config sibling, like the KB family.** Siblings are *rendered* from `config/` + `templates/` against the engine (INDEX, knowledge, `@ENGINE@`). Practice skills have none of that — they are authored prose, not generated adapters. Forcing them through `config/`/`generate` would fabricate engine structure they don't use. Rejected.

Chosen: a dedicated `skills/practice/<name>/` home discovered by directory scan (`practice_skills()` mirroring `siblings()` over `config/`). Authored + self-contained + drop-in: a new skill is a new directory, no code change. This is the genuinely new capability the issue's "authored-skill lane" calls for — distinct from maintenance because it is a *set*, not a constant.

Invalidation: if a practice skill ever needs per-skill install logic beyond bake → deploy → activate, the uniform scan breaks and a per-skill descriptor (a small manifest in the skill dir) would be the next step.

## D-2: canonical-body-and-vault-generalization

The live fork: **two divergent body versions exist** (research: "The practice skills as they exist today"). The deployed Claude bodies are rich and KB-grounded and carry an optional vault reference; the chezmoi-source bodies are terser and carry no vault reference at all.

- Chose the **rich, hand-tuned** bodies as canonical — what the issue calls "the most valuable, in-action pieces." They were the deployed Claude copies (the author's later, richer thinking); the terser chezmoi-source versions had diverged silently and are less battle-tested. **Confirmed under fire:** mid-implementation a `chezmoi apply` reverted the live deployed copies to the terse versions — captured just-in-time into the framework before they were lost, and the author confirmed rich as canonical. That reversion is the feature's thesis in miniature: while these skills live in personal config they are one `chezmoi apply` from regressing, and the framework is now their protected home.
- Given the rich body, the lone machine-specific element is one optional reference line per skill — a `metacognition-vault`-rooted path. Generalize it with the **existing** `@VAULT@` token + the **unbaked-token guard** (`re.findall(r"@[A-Z_]+@", …)` → `SystemExit`), exactly as `deploy_maintenance` does. No new mechanism; `@VAULT@` is the only token a practice body needs today.

This decision is an **author judgment call**, flagged for review: if the author instead prefers the terse chezmoi bodies, they carry no vault path, so `Spec#B-3` and `Spec#C-2` become trivially satisfied and D-2's baking is unnecessary. Invalidation: author picks the terse bodies, or the optional vault-escalation reference is dropped from the rich ones.

## D-3: activation-via-surgical-upsert

`Spec#C-1` (never disturb the adopter's operating frame) and `Spec#B-2` (activation present) are already solved for siblings by `upsert_agents_block` — surgical, idempotent, full-line-matched, writes only on change. Reuse it unchanged; building a second emitter would risk the byte-for-byte guarantee the existing one already proves.

The real decision is the **tag**. Siblings derive the tag from the stem (`context-engineering` → `<context_engineering>`). That derivation fails for practice skills on two counts:

- `compact-focus`'s activation tag is `<compaction>` — the *moment*, not the skill name. A name-derived `<compact_focus>` would be wrong.
- The adopter **already has** hand-managed `<handoff>` and `<compaction>` spans in their `~/AGENTS.md`. Authoring the framework's blocks under those same tags makes the upsert **replace them in place** — a clean takeover. A name-derived tag would instead orphan the user's existing block and append a second one (duplication, and a contradiction of the clean-ownership intent).

So the practice-skill activation source is the **complete authored `<tag>…</tag>` block**, passed straight to `upsert_agents_block` (bypassing the sibling-only `agents_block()` wrapper). Tags are authored, not derived.

Invalidation: if another consumer (e.g. the self-initiated-skill-activation feature, 0001) pins a different tag name for these moments, the authored tag must match it.

Deployment caveat (not framework code, so not a Decision): on a personal machine whose chezmoi source still emits these spans, a later `chezmoi apply` re-asserts the personal copy — install against a `--dest` sandbox until the chezmoi source drops them, exactly as `wiring/README.md` already notes for the sibling spans.

## D-4: byte-identical-frontmatter (retired)

**Retired — superseded by `D-5-per-provider-frontmatter`** (`Understanding#Delta-1-codex-needs-per-provider-not-byte-identical`). The invalidation trigger below fired: Codex's `compatibility`/`metadata.short-description` conventions and the `$ARGUMENTS` / `/compact <focus>` mismatches proved load-bearing, not minor. Original reasoning kept for reconstructability.

The chezmoi source diverges per provider (Claude `argument-hint`/`allowed-tools`; Codex `metadata.short-description`/`compatibility`). The framework's stated invariant is the opposite — `install`'s docstring: "the two providers never diverge" — and both shipped lanes (KB adapters, maintenance) deploy byte-identical to both providers.

Chose **byte-identical**: `name`, `description`, and `argument-hint` where the skill has one. `argument-hint` is useful on Claude and inert on Codex; the Codex-only `compatibility`/`short-description` niceties are dropped. This keeps the practice skills consistent with every other shipped skill and avoids a per-provider frontmatter assembler for a low-value divergence.

This is the second **author judgment call** flagged for review — the per-provider niceties are real, just minor. Invalidation: a provider rejecting a foreign frontmatter key, or a provider-specific key (e.g. Codex `compatibility`) proving load-bearing for discovery → revisit per-provider frontmatter (a shared body + provider-specific frontmatter wrapper, the shape chezmoi already used).

## D-5: per-provider-frontmatter

Reality caught up with the byte-identical premise (Delta-1). The adopter's own chezmoi source already carried per-provider frontmatter — Claude `argument-hint`, Codex `compatibility: Designed for Codex` + `metadata.short-description` — because each runtime reads different keys. Shipping Claude's `argument-hint` to Codex (and dropping Codex's `compatibility`) is not the inert nicety D-4 assumed: `compatibility` is a Codex discovery signal, and `argument-hint` is meaningless there.

The "never diverge" ethos holds for KB siblings — their content is provider-neutral *knowledge* — but not for these UX-coupled practice skills. Alternative: keep byte-identical with only `name`/`description`, stripping each runtime's conventions — rejected as strictly worse than matching them. Chosen: per-provider frontmatter, authored as separate `<provider>/SKILL.md` files (`D-1` layout). Invalidation: if the two runtimes' frontmatter conventions converge, collapse back to one file.

## D-6: per-provider-body-divergence

The deeper Codex divergence is the *body*, not just frontmatter (Delta-1). `compact-focus`'s whole output — a `/compact <focus>` line to paste — depends on Claude Code accepting a focus argument to `/compact`. Codex's `/compact` does not reliably take one; the documented Codex pattern is a normal pre-compaction *message* stating what to keep/drop, then plain `/compact` (or a durable `compact_prompt`). A byte-identical body would hand a Codex user an instruction that does not work — the exact `Spec#C-3` violation. So the Codex `compact-focus` body emits the focus *message* + directs `/compact`; the Codex `handoff` body drops the Claude-only `$ARGUMENTS`. This also corrects the adopter's *current* Codex `compact-focus`, which naively emits the unreliable `/compact <focus>` form.

Alternatives weighed: (a) one shared body with provider-conditional sections — rejected, a templating layer not worth it for a two-skill set; (b) a Codex "set `compact_prompt`" helper instead of a per-session skill — rejected, `compact-focus` is intentionally one-off/per-session, which the message-then-`/compact` pattern serves. The duplication risk (the `claude/` and `codex/` bodies drifting) is accepted for a small curated set and mitigated by the shared labeled-block structure + the source scan. Invalidation: if Codex `/compact` gains a reliable focus argument, the two bodies reconverge.
