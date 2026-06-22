# 0001-self-initiated-skill-activation — RESEARCH

Evidence gathered during SPEC→DESIGN. Facts only; interpretation lives in design-rationale.md.

## claude-code-transcript-observability

Source: read-only inspection of `~/.claude/projects/` and live transcript records on this machine (2026-06-22).

- Every session is persisted as JSONL. Main session: `~/.claude/projects/<cwd-slug>/<session-uuid>.jsonl` (cwd path-encoded, e.g. `-Users-admin--local-share-metacognition-vault`). ~2000 sessions present.
- Sub-agent (Task tool) runs: `~/.claude/projects/<cwd-slug>/<session-uuid>/subagents/agent-<id>.jsonl` + a sibling `agent-<id>.meta.json`. Sub-agent activity is **not** inlined into the parent as `isSidechain` records (sampled main transcript had 0).
- "Did skill X fire" is observable two independent ways:
  1. Assistant content block `{"type":"tool_use","name":"Skill","input":{"skill":"<name>","args":"<...>"}}` — `input.skill` is the bare skill name.
  2. Top-level record field `attributionSkill` carrying the bare skill name that produced the record. Confirmed values include `handoff`, `context-engineering-knowledge-base`, `compound-engineering:ce-code-review`, `mgrep:mgrep`. Plugin-namespaced skills appear as `plugin:skill`; bare framework skills (incl. `compact-focus`, `handoff`) as just the name. Companion field `attributionPlugin`.
- Record top-level keys observed: `type` (user/assistant/attachment/system), `message` (`content[]` blocks), `sessionId`, `uuid`/`parentUuid`, `timestamp`, `cwd`, `gitBranch`, `slug`, `agentName`, `isSidechain`, `toolUseResult`, `toolUseID`, `attributionSkill`, `attributionPlugin`, `isCompactSummary`, `promptSource`, `userType`.
- Claude Code hook event vocabulary: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`, `SubagentStop`, `PreCompact`. There is **no** "SkillInvoked" event. A skill firing is catchable via a `PreToolUse` matcher on the `Skill` tool, but no framework facility does this today.

## framework-tool-and-selftest-idiom

Source: read-only inspection of `/Users/admin/.local/share/metacognition/` (2026-06-22).

- Tools are stdlib-Python3 executables at repo root, no extension, `chmod +x`, `argparse` in `main(argv=None)`, ending `if __name__ == "__main__": raise SystemExit(main())`. Verb-named: `generate`, `install`, `health-check`, `no-net-loss`. Shared library under `engine/` (`engine/kb-engine`, `engine/sources.py`), imported via `sys.path.insert`.
- `health-check` = the deterministic, read-only, model-free measurement tool: argparse flags incl. `--vault`, `--today YYYY-MM-DD`, `--offline`; emits a worklist to **stdout** (one line per flagged item, silence = pass), a human summary to **stderr**, exit `0` normal / `2` usage error; reuses `engine/sources.py` so its detection bar is byte-identical to the write-gate's (single-sourcing).
- Selftest idiom: one executable `<tool>-selftest` per tool; module-level `_checks=[]` + `check(name, ok, detail)`; fixtures built at runtime in `tempfile.mkdtemp(...)`, torn down in `finally` with `shutil.rmtree`; drives the **real** tool via `subprocess.run([sys.executable, TOOL, *args], ...)`; asserts on returncode + stdout/stderr; module docstring enumerates each pinned property; exit code is the contract. No pytest, no third-party deps, no aggregator/CI runner, no on-disk fixtures.
- No `tests/`, `fixtures/`, `evals/`, `scenarios/`, or `testdata/` directory exists anywhere in the repo (confirmed by find). No existing notion of scenario corpus, golden data, scoring, or baseline. Config files (`config/<stem>`) are flat `key = value`, hand-parsed, deliberately "not a templating language."
- Docs convention: repo-root capitalized Markdown (`ARCHITECTURE.md`, `FAMILY.md`, `SOURCES.md`, `README.md`); every component dir carries its own `README.md`; feature docs under `docs/features/<KEY>/`.

## eval-methodology-basis

The measurement design is grounded in the evaluation-observability knowledge base (not re-derived here): eval-driven-development (measurement-not-vibes; three eval levels; pass-rate as a product decision), building-eval-datasets (dimensions → seeds → synthetic recipe; off-the-shelf-metric trap; real + synthetic sources), agent-trajectory-evaluation (deterministic final-state check over an LLM judge when ground truth exists; pass^k for reliability under non-determinism), and error-analysis-look-at-your-data (review real traces to build the failure taxonomy before writing evals).

## baseline-reflects-shipped-trigger-first-wiring

Source: metacognition `git log` + working tree, 2026-06-22.

- `29c45d0 refactor(wiring): lead KB descriptions with the activation trigger` is in HEAD (`merge-base --is-ancestor 29c45d0 HEAD` → true); repo in sync with `origin/main` (behind 0, ahead 0).
- It reordered the 5 KB siblings' wiring descriptions trigger-first (`agent-architectures`, `agent-runtime`, `evaluation-observability`, `skill-design`, `tool-design`); `wiring/tool-design` now reads "Use when …".
- Installed adapters match: `~/.claude/skills/<kb>/SKILL.md` and `~/.codex/skills/<kb>/SKILL.md` descriptions are trigger-first (verified for tool-design on both providers).
- The commit message grounds the change on plausibility — "a skill's description is its activation signal, so leading with the trigger sharpens auto-invocation" — not measured evidence.
- compact-focus / handoff (chezmoi-managed, outside `29c45d0`'s scope) remain capability-first.
