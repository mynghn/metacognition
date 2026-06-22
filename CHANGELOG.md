# Changelog

Notable changes to the **Metacognition tooling** (this repo). The companion knowledge
corpus lives in [`metacognition-vault`](https://github.com/mynghn/metacognition-vault).

## [0.1.0] — 2026-06-22

### Added — `0010-vault-self-evolution`: on-demand, ratified self-maintenance for the vault

**What it is.** A way for the knowledge vault to **heal and evolve its own knowledge, safely**.
An in-session, provider-neutral **maintenance skill** (the only LLM in the loop) reconciles decayed
knowledge against current sources and routes every change through a gate: mechanical, claim-preserving
fixes auto-apply; any claim-affecting or structural change becomes a **ratifiable proposal a human
merges**. Every write flows through the existing `kb-engine` (the sole writer), and nothing runs on a
schedule — detection and healing only ever start on explicit demand. A deterministic `health-check`
surfaces decay (dead links, over-age entries, below-bar sources) without invoking a model.

Three tiers, all **compositions of the existing engine verbs** (`capture` / `refresh` / `remove`) —
no new engine primitive:

- **T1 — heal** one entry in place.
- **T2 — sibling evolution**: re-derive a whole sibling's entry-set (keep / refresh / split / merge /
  retire / re-scope) and emit it as one proposal — never a blind single-entry insert.
- **T3 — family evolution**: add / merge / retire a sibling or move a boundary, *with* the `FAMILY.md`
  registry edit — a **cross-repo coupled proposal** (vault entries via the engine + the engine-repo
  registry via plain git; ratify both or reject both).

A **verification envelope** guards every write against the LLM healer's own failure modes: a
deterministic no-net-loss diff + citation re-fetch (run by the reconciler), then **independent
adversarial reviewers** (default-REJECT quorum) judging citation support, silent loss, scope drift,
and corroboration — the reconciler never adjudicates its own work. Auto-apply is *gated* by this
envelope, not unguarded.

**What we did.**

- **Engine + policy + detection:** structured provenance commit-trailers (`Heal-*`); a `SOURCES.md`
  authority policy + write-gate; a `degraded:` quarantine marker (preserve, don't delete, when a
  source falls below the bar); and the deterministic `health-check` (reachability · age×volatility ·
  source-lint), read-only and model-free.
- **The maintenance skill** (`skills/metacognition-maintenance`): the propose→ratify spine
  (worktree+branch, merge=ratify, restartable composite applier), the verification envelope, and the
  T1/T2/T3 procedures — provider-neutral, shipped **byte-identical to `~/.claude` and `~/.codex`** by
  the installer.
- **Fixes surfaced by dogfooding:** `health-check` now classifies a bot-refused `403/429` as
  `[unverifiable]` (a refused bot is not proof a page is gone) instead of a false `[dead-link]`;
  `generate-selftest` restored to green against pre-existing config/source drift.
- **Acceptance on the real corpus:** `health-check` validated end-to-end; two genuinely under-sourced
  entries re-sourced to authoritative references — and the envelope did its job, **rejecting a heal
  for a fabricated citation and a silent loss, then accepting the corrected version**.
- Every step adversarially verified before commit; all self-tests green (engine 105, maintenance 66,
  install 46, generate 62, health-check 19, no-net-loss 22).

### Changed

- **Registry (`FAMILY.md`):** marked the four delivered siblings — `agent-architectures`,
  `agent-runtime`, `evaluation-observability`, `skill-design` — **built** (with entry counts) and
  synced the `context-engineering` count, correcting stale `planned` labels. Ratified through the new
  **T3 family-evolution path** — i.e. dogfooded the feature on its own registry.

Design docs (the LeanPlan requirement → spec → design → plan → understanding chain) live in the
feature workspace, outside this repo.
