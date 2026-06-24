# configs/

The **activation-mechanism candidates** — the pluggable slot the driver applies before running the
corpus. Each is a *test input*, not a chosen mechanism: a candidate is adopted only if it clears the
promotion gate against the recorded baseline (`scenarios/baseline-C0.json`). Baseline `C0` is current
state and lives in no file here (it applies nothing).

How the driver (`run-scenarios`) applies a candidate, by mechanism family:

| family | how it is applied | candidate(s) |
| --- | --- | --- |
| **system-prompt addition** | `<config>.append-system-prompt` → `run-scenarios --config <name>` passes its text as `--append-system-prompt` | `C1` |
| **skill-description variant** | `C3-skills/<skill>/SKILL.md` is swapped over the installed `~/.claude/skills/<skill>/SKILL.md` around the run, then restored | `C3` |

## Candidates

- **C1 — standing skill-consultation checkpoint** (`C1.append-system-prompt`). A standing instruction
  added to the system layer telling the agent to check, each turn, whether the moment calls for one of
  its skills — naming the no-cue pass-over failure and the session-management category, but *not*
  re-describing each skill (that is C3's lever). Worded as a calm "if one fits, use it; if not, proceed"
  rather than a forceful directive, so it lifts recall without inducing over-firing (which would breach
  the false-fire bar).

- **C3 — trigger-first scoped-skill descriptions** (`C3-skills/`). The scoped skills `handoff` /
  `compact-focus` ship **capability-first** (description leads with the capability, then "Use when …").
  C3 reorders each description **trigger-first** ("Use when …" leads), changing *only* the description —
  the skill body is byte-identical to the installed skill. This is the clean A/B that adjudicates the
  trigger-first ordering theory for the scoped skills (and by extension the shipped KB-wiring reordering).

### Why C3 swaps the global skill files

Claude Code (v2.1.185) exposes **no per-invocation override** of an existing skill's description:
project-local `.claude/skills/` is not loaded by headless `claude -p`; `--plugin-dir` adds a separately
namespaced `plugin:<skill>` rather than replacing the original; and no setting targets a single skill's
description. So the only faithful way to present `handoff` / `compact-focus` with a different description
is to temporarily replace the installed `SKILL.md`. The C3 run does this under a guaranteed restore
(backup → swap → run → restore + byte-identical verify); the descriptions are functionally equivalent
(same content, reordered), so the brief window of mutation cannot change behaviour for anything else.

Because the swap is global state every headless run reads, **C3 cannot run concurrently with any other
config** — its batch is serialized, and the global is capability-first for every non-C3 run.

## Deferred

`C2` (reflection/self-check pass) and `C4` (keyword-control ceiling) are part of the initial matrix but
are run only if the first pass (C1, C3) leaves the question open — to keep the live-run spend matched to
what the results justify.
