# 0001-self-initiated-skill-activation — DESIGN RATIONALE

## Decision-1: eval-gated-mechanism-slot

**Forces.** The activation mechanism is genuinely unknown, and the REQUIREMENT makes "Solving by plausibility" a Non-goal — a change that can't show measured lift doesn't count. This project exists *because* an ungrounded mechanism (a "lead-with-the-trigger / capability-first licenses inline" theory) was shipped earlier and had to be reverted: it sounded right, matched no authority, and was contradicted by the canonical capability-first example. Eval-driven-development names the failure mode directly — "vibes-based development collapses the moment a non-deterministic system is modified."

**Alternative considered — pick a mechanism and ship it.** Choose the most plausible lever (the consultation checkpoint, or description tuning) on reasoning and roll it out. Rejected: this is exactly the move that just failed. Plausibility is not evidence, and skill activation is non-deterministic, so eyeballing a few good outcomes proves nothing.

**Chosen path.** Make the mechanism a pluggable config the harness runs and scores. The design commits to the *selection process*, not a mechanism. The candidate matrix (C1 checkpoint, C2 reflection pass, C3 description variants, C4 keyword-control ceiling) is a set of test inputs, refinable as error analysis surfaces better candidates; the winner is whichever clears the gate.

**Invalidation triggers.** (1) If no candidate clears the gate across iterations, the honest output is the instrument + a negative result — and the question escalates: is no-cue self-activation reachable at the instruction layer at all, or does it require a harness-level (Claude Code) change beyond this framework's reach? (2) If the corpus can't discriminate candidates (all score alike), the corpus is too easy or the metric too coarse — fix the measurement before trusting any verdict.

## Decision-2: out-of-band-transcript-scorer

**Forces.** The scorer needs a cheap, trustworthy "did skill X fire" signal, and O-2 needs the *negative* too (a should-have-fired-but-didn't). The framework's existing measurement tools (`health-check`, `no-net-loss`) are all out-of-band, read-only, model-free readers — and the Explore pass confirmed Claude Code persists every session as JSONL with skill firing observable two independent ways (`Skill` tool-use `input.skill`, and the top-level `attributionSkill` field).

**Alternatives considered.**
- *Live `PreToolUse` hook on the `Skill` tool.* Rejected: the framework establishes no such facility, all its measurement is out-of-band, and — decisively — a hook sees *firings* but not the should-have-fired *misses*. O-2's negative is only recoverable by comparing the scenario's `should_fire` label against the transcript, which is a scoring step, not a hook event.
- *LLM judge over the trajectory.* Rejected: unnecessary and harmful. "Did skill X fire" is a deterministic fact in the transcript; agent-trajectory-evaluation is explicit that a deterministic final-state check beats a judge when ground truth exists (τ-bench compares to goal state with no judge). A judge would only add position/verbosity/self-enhancement bias and cost.

**Chosen path.** Deterministic transcript read, dual-keyed on `Skill` tool-use *and* `attributionSkill` for robustness against either being absent, walking the `subagents/` subdir for sub-agent runs.

**Invalidation trigger.** The reader is pinned to Claude Code's observed transcript schema. If `attributionSkill` is dropped or the `Skill` block shape changes, the reader must fail loudly (not silently miss), since a silent schema drift would read as "skill never fired" and corrupt every rate.

## Decision-3: labeled-no-cue-corpus

**Forces.** The dataset caps everything downstream — building-eval-datasets: "its quality caps every judge and metric." We need real *and* synthetic cases, and labeled *negatives* (non-matching scenarios) so false-fire is measurable, not just recall.

**Chosen recipe.** Dimensions (scoped-skill × framing × should_fire) → ~20 hand-written seeds that set the distribution → synthetic scale-up in two stages (tuples, then natural-language inputs) → filter through cheap assertions. The real compact-focus failure ("continue or compact?") is seed #1. Crucially, error analysis comes first: review real session transcripts (≈100, or until ~20 turn up no new failure category) to source genuine misses and build the label taxonomy — error-analysis-look-at-your-data calls this the highest-ROI, most-skipped eval activity.

**Alternatives rejected.**
- *Off-the-shelf "helpfulness / quality" metrics.* The documented trap — they score abstract qualities that may not track our actual failure (a skill not firing), creating unjustified confidence.
- *"Generate 100 scenarios" from an LLM.* Repetitive, low-coverage phrasing; the dimensions+seeds recipe exists precisely to avoid it.
- *YAML data config.* Rejected for repo-idiom consistency: the framework tolerates YAML only inside entry frontmatter and has no YAML-data precedent; declarative JSON (transcripts are already JSONL) is the conservative, stdlib-parseable choice.

**Invalidation cues.** If ~20 fresh real traces stop surfacing new failure categories, the taxonomy is saturated — stop expanding. If the corpus passes ~100% at baseline `C0`, it's too easy to discriminate anything — make it harder; a meaningful set leaves real headroom (pass-rate is a product decision, not a vanity 100%).

## Decision-4: replayed-headless-driver

**Forces.** A controlled candidate A/B needs fresh runs under each config; and self-activation is noisy, so a single run per scenario misleads.

**Chosen path.** A headless driver runs each scenario `N` independent trials per config and aggregates pass^k-style. Agent-trajectory-evaluation is explicit that "a single pass is noise" and pass^k "exposes inconsistency a single run hides" — SOTA function-callers were brittle (pass^8 < 25% in retail), so k > 1 is mandatory, not optional. This realizes the "sustains across runs rather than spiking once" clause of SPEC#INV-1-self-use-rate-beats-baseline.

**Alternative considered — score only pre-existing real transcripts.** Rejected as the *sole* source: you cannot run a controlled comparison of a candidate mechanism on transcripts recorded before that candidate existed. Real traces still feed the *corpus* (Decision-3), but the baseline-vs-candidate measurement needs freshly driven runs.

**Invalidation / risk.** Headless reproduction of *stateful* triggers — compact-focus fires on "context is heavy," which an explicit one-shot prompt doesn't recreate — is the hard part. The mitigation is in Decision-4's contract: a scenario whose triggering condition can't be reproduced deterministically is dropped and logged, never faked. If the dropped set is large, the corpus under-covers the stateful triggers, and that coverage gap must be stated as a known limitation, not hidden behind a green number.
