# LLM-Agent Knowledge Base — Tooling

The published tooling + registry home for a **federated family of agent-practice knowledge bases**. Each sibling is a focused KB skill (context-engineering, prompt-engineering, tool-design, …) that both Claude Code and Codex discover and query. This repo holds the shared machinery; the knowledge itself lives in the companion **vault repo**.

Two independent repos, two histories:

- **`llm-agent-knowledge-base`** (this repo) — the tooling: a shared operations engine, the thin per-sibling config, single-sourced pattern templates, the discovery-wiring source, the [`FAMILY.md`](./FAMILY.md) registry, and the installer. Released + versioned (low churn).
- **`llm-agent-knowledge-vault`** — one Obsidian-shaped vault, a top-level `<topic>/` folder per sibling. Mutated + committed at runtime by the engine (high churn).

Splitting them keeps runtime knowledge writes off the tooling history and lets either be published or installed on its own. See `docs/features/0004-knowledge-base-rehome/` (DESIGN Decision-1).

## Layout

```
llm-agent-knowledge-base/
├── FAMILY.md          the "should I add a sibling?" registry (map of the family)
├── engine/            shared operations engine — capture / refresh / remove / locate
├── config/            thin per-sibling config — { stem, ENV prefix, INDEX heading, tier }
├── templates/         single-sourced pattern templates — adapter body, INDEX skeleton,
│                      config schema, entry/README shapes (consumed by the engine + generator)
├── wiring/            discovery-wiring source — per-sibling description + tier-gated AGENTS.md block
└── install            the installer — renders adapters from templates/ + config/ + wiring/ and
                       deploys them into both agents (D2 adds AGENTS.md wiring; D3 adds vault setup)
```

The skeleton above is the agreed top-level layout (feature `0004`, task F1). Each directory carries a `README.md` naming its role and the task that fills it — the engine, configs, templates, wiring, and installer are built out across `0004`'s Engine / Distribution tracks.

## Install

A plain installer (built in `0004` Distribution) deploys each sibling's `SKILL.md` adapter into `~/.claude/skills/<name>/` and `~/.codex/skills/<name>/`, emits the discovery wiring, and records where the vault lives — no plugin, no privileged agent. On personal machines, chezmoi optionally bootstraps the family by cloning both repos (a consumer of the installer, not its home — mirroring the existing `leanplan` external).

## License

MIT — see [`LICENSE`](./LICENSE).
