# Architecture

Metacognition is a knowledge base an LLM agent keeps about **itself** — how it thinks, where it degrades, and the practices that work around its own limits. The knowledge lives as small, distilled, sourced entries; the machinery in this repo lets both Claude Code and Codex retrieve, capture, and refresh that knowledge on demand, and records every change to its own version history.

This document is the durable design overview — the shape of the system and the load-bearing decisions behind it. For the sibling roadmap see [`FAMILY.md`](./FAMILY.md); each component directory carries its own `README.md`.

## Two repositories

The family is two independent, separately-published git repos:

- **`metacognition`** (this repo) — the **tooling**: the shared operations engine, the thin per-sibling config, single-sourced pattern templates, the discovery-wiring source, the family registry (`FAMILY.md`), and the installer. Released and versioned; low churn.
- **`metacognition-vault`** — the **knowledge**: one Obsidian-shaped vault with a top-level `<topic>/` folder per sibling, each holding `INDEX.md` + `knowledge/<slug>.md` entries. Mutated and committed at runtime by the engine; high churn.

**Why two repos, not one:**

- **Opposite change cadence.** The vault takes a commit on every knowledge edit; the tooling changes rarely. Merged into one history, each buries the other.
- **Different audiences.** The tooling is the shareable product — others install it. The vault is personal knowledge. Splitting lets the tooling be published openly while the vault stays private (or is published on its own).
- **Mutation isolation.** The engine commits *only* to the vault's own history, so knowledge writes never touch the tooling history or any personal/dotfiles repo. This is the reason the layout exists.
- **Swappable vault.** One tooling install can point at different vaults (personal, work, a shared team vault) with no code change.

## The family model

Federated focused skills, not one broad knowledge base. Each **sibling** is one coherent, closeable agent-practice topic — `context-engineering`, `prompt-engineering`, `tool-design`, … — realized as the same proven pattern: a `<topic>/` folder in the vault, operated by the shared engine, surfaced to each agent through a thin `SKILL.md` adapter.

Small coherent units retrieve precisely: a skill auto-invokes on its one-line description, so a narrow description is a sharp trigger. This beats one giant index on both recall and scaling cost, and isolates knowledge by topic. `FAMILY.md` is the registry — the "should I add a sibling?" decision record and map; it is not itself a skill.

## Components (this repo)

```
metacognition/
├── engine/kb-engine     shared operations engine — capture / refresh / remove / locate
├── config/<stem>        thin per-sibling config — stem, ENV prefix, INDEX heading, tier
├── wiring/<stem>        discovery source — the SKILL.md description (+ an AGENTS.md block for everyday tiers)
├── templates/           single-sourced pattern templates — adapter body, INDEX skeleton, config schema
├── install              the installer — renders adapters from templates + config + wiring, deploys to both agents
└── FAMILY.md            the family registry
```

A sibling's entire surface is `{ template + config + description }` — never a hand-encoded copy. The structural pattern lives once, in `templates/`; the only per-sibling difference is the small `config/` and the `wiring/` description. This is what lets a new sibling be instantiated — by hand or by a generator — without re-encoding the pattern, and what keeps the two providers' adapters from ever drifting apart.

## How it works

**Install — wiring the framework into your agents.** For each sibling, the installer reads its `config` + the `wiring` description + the one shared adapter-body template, renders a single `SKILL.md`, and writes that byte-identical adapter into both `~/.claude/skills/<name>/` and `~/.codex/skills/<name>/`. For everyday-tier siblings it also upserts a named trigger block into the shared `AGENTS.md`. Finally it ensures the vault is a git repo root and records the vault's location where the engine will look for it. No plugin and no privileged agent — both agents consume the same Agent-Skills `SKILL.md`.

**Operate — changing knowledge.** Every add / update / remove goes through the engine: it validates the entry's frontmatter, writes it into the vault, keeps the topic's `INDEX.md` slug-sorted, and records the change as exactly one commit in the vault repo's own history. Retrieval is the reverse and needs no engine — read the topic `INDEX.md`, then load only the entries that match the query.

## Load-bearing rules

- **The engine is the only writer, and it commits to the vault.** The validate → write → commit path lives entirely inside the engine, so nothing bypasses validation and every change is one recoverable commit in the vault's own history — never in personal config.
- **The vault must be a git repo root.** Before any write, the engine refuses a vault that is missing, not a git repo, or nested inside another repo. The nesting check is the safeguard: an un-rooted vault sitting under a tracked `$HOME` would otherwise let a change commit into that enclosing/dotfiles repo — the exact leak this layout exists to prevent.
- **The two providers never diverge.** Both adapters are emitted from one body template in one installer pass, so Claude Code and Codex always receive the identical skill.
- **Discovery is tiered by universality.** Every sibling's description is wired into both adapters. Beyond that, only an *everyday* concern — relevant on roughly every turn — earns an always-loaded trigger block in the shared `AGENTS.md`; *common* and *situational* siblings rely on their description alone, which costs nothing in a turn until the work matches.
- **Nothing runs on its own.** There is no scheduler and no automatic capture or refresh. Knowledge changes only when the engine is invoked explicitly.

## Vault location

The engine resolves where the vault lives, in precedence order:

1. an explicit `--vault` argument;
2. a per-sibling `<PREFIX>_KB_VAULT` environment variable;
3. the family-level `KB_VAULT` environment variable;
4. the file the installer writes at `${XDG_CONFIG_HOME:-~/.config}/metacognition/vault`;
5. a standard default — `~/.local/share/metacognition-vault`.

The per-sibling environment hook is the escape valve for a sibling that ever needs its own separate vault.

## Optional satellites

Neither is required; the framework is complete without them.

- **chezmoi** — on a personal machine, an optional one-time bootstrap can clone both repos and run the installer. chezmoi is a *consumer* of the installer, not the home of the family; it never hosts the knowledge or the tooling content.
- **Obsidian** — the vault is already Obsidian-shaped (frontmatter + `[[wikilinks]]`), so Obsidian opens it with zero migration as a read-only human lens onto the knowledge. It must never write the vault: the engine is the sole writer, and a second uncontrolled writer would bypass validation.
