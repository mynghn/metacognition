# scenarios/

The labeled **no-cue scenario corpus** — the measurement substrate the skill-activation eval is bound to.
Each scenario is a realistic situation in which a *scoped* skill either should or should not self-activate
when the user names no skill and types no trigger command. A baseline self-use rate and false-fire rate are
recorded against this set before any activation mechanism is changed; every later measurement is relative to
it. The guarantees the eval makes hold within, and only within, this set — widening the scoped-skill set
re-binds the contract.

**Scoped skills:** `compact-focus`, `handoff` — the single-sourced scope in `engine/transcript.py`
(`SCOPED_SKILLS`); the corpus, the firing reader, and the scorer all read scope from that one place so they
cannot drift.

## What "no-cue" means here

Every scenario is **no-cue**: the user's turn names no skill and types no slash-command / invocation. A
handful of `should_fire: true` scenarios still contain the plain English word *compact* or *handoff* as a
homonym — most notably the anchor scenario `cf-01`, the canonical real failure where the user asked
"continue or compact?" and the skill did not self-activate (it fired only once the user later named it).
That weak-signal case is deliberately in scope: the point is that self-activation failed even with the word
present. It is the mirror image of the negatives `cf-13` / `ho-16`, where the word appears but the
triggering condition is genuinely absent and firing would be wrong.

## Schema

One JSON object per line (JSONL — the transcripts the scorer reads are already JSONL). Exactly these keys:

| key | type | meaning |
| --- | --- | --- |
| `id` | string | stable unique id (`cf-NN` compact-focus, `ho-NN` handoff) |
| `skill` | `"compact-focus"` \| `"handoff"` | the scoped skill the scenario is about |
| `setup` | string | analyst-facing description of the triggering condition + framing, generic (no proprietary content) |
| `prompt` | string | the **verbatim first-person no-cue user turn the driver injects** — what the agent actually receives (a description fed as a prompt makes the agent reason *about* the scenario, not *be in* it) |
| `framing` | `deliberation` \| `imperative` \| `tangential` \| `unrelated` | how the user's turn carries the moment |
| `should_fire` | bool | whether the scoped skill should self-activate on this moment |
| `reproducible` | bool | whether a single headless turn can establish the condition; the driver drops `false` (logged) |

`framing`: **deliberation** = the user openly weighs the decision; **imperative** = a forward command that
creates the boundary; **tangential** = the condition is incidental to what the user asked; **unrelated** =
superficially similar but the condition does not actually call for the skill (a negative).

## Dimensions and the grid

Dimensions are `skill × framing × should_fire`. Both matching (`should_fire: true`) **and** non-matching
(`should_fire: false`) scenarios exist for each scoped skill — negatives are required, because without them
the false-fire rate is not measurable and only recall (not precision) could be scored. Current distribution
(30 scenarios; compact-focus 14, handoff 16; true 21, false 9):

```
compact-focus  deliberation  true 4  false 1
compact-focus  imperative    true 4  false 1
compact-focus  tangential    true 2
compact-focus  unrelated             false 2
handoff        deliberation  true 3
handoff        imperative    true 8  false 3
handoff        tangential           false 2
```

## Replayability — what the headless driver can measure

A scenario is only useful to the live driver if a single headless turn can establish its condition. The
driver injects the `prompt` and drops every `reproducible:false` scenario (logged, not faked). The split is
**fundamental, not incidental**:

- **compact-focus's trigger is the live window actually being heavy/long** — a state a fresh `claude -p`
  process cannot embody, and describing it in a prompt does not make the window heavy. So **all 10
  compact-focus positives are `reproducible:false`**, and **compact-focus self-use is not measurable headlessly
  at all** — only its false-fire (on genuinely-light fresh sessions) is.
- **handoff's trigger is a boundary departing to a new goal**, which a single turn *can* self-contain (finished
  prior work stated compactly + the new goal). All 16 handoff scenarios are `reproducible:true`.

| skill | self-use (reproducible positives) | false-fire (reproducible negatives) |
| --- | --- | --- |
| compact-focus | **0 — not headlessly measurable** | 4 |
| handoff | 11 | 5 |

A live pilot confirmed both the mechanism and the failure: handed the injected first-person `prompt` for a
plan→implement boundary, the agent said *"I'm at the handoff from planning to implementation"* and produced a
manual checkpoint — but never invoked the handoff skill. The miss is behavioral, not a replay artifact.

## Recorded baseline (C0)

`baseline-C0.json` — the first real measurement, current state with no activation mechanism applied (the
state that already ships the trigger-first skill descriptions). Every candidate is scored relative to it.

| | self-use | false-fire | n_trials | model |
| --- | --- | --- | --- | --- |
| **C0** | **0.09** (handoff only) | **0.00** | 3 | Opus 4.8 |

What it says: **scoped skills do not self-activate on cueless moments.** Across 11 reproducible handoff
positives × 3 trials, only one (`ho-01`, the most explicitly trigger-shaped wording) fired, and it fired on
every trial; the other ten missed on every trial. The gap the project exists to measure is real and large,
not a rounding artifact — and it is *not* a too-easy corpus (a near-100% baseline would be the invalidation
cue). Self-activation is also non-deterministic across the boundary: a single pilot trial of `ho-08` fired,
yet all three baseline trials of `ho-08` missed — which is why a verdict aggregates N trials and never reads
one run.

Read with the scope and the caveats above:

- **Self-use is handoff-only.** All 10 compact-focus positives are dropped as non-reproducible (see
  *Replayability*), so this number says nothing about compact-focus self-activation.
- **Trust the 0.00 false-fire weakly.** It rests on 9 negatives, mostly synthetic/cued (see *Known
  limitations*); it is consistent with no false firing, not proof of it.
- **Gate parameters** recorded with the baseline: `margin 0.10` (a candidate must lift self-use by ≥10 points
  to be worth its added machinery) and `false_fire_bar 0.10` (≤1-in-10 negatives may fire before "crying
  wolf" outweighs the recall gain). Both are provisional product decisions, refinable before the candidate
  matrix is run.

Reproduce: `run-scenarios --corpus scenarios/corpus.jsonl --config C0 -n 3 --out <manifest> --cwd <fresh-dir>
--model claude-opus-4-8`, then `skill-activation-check --corpus scenarios/corpus.jsonl --runs <manifest>
--record-baseline scenarios/baseline-C0.json --margin 0.10 --bar 0.10`.

## How it was built

Error-analysis-first, the highest-ROI and most-skipped eval activity: real session transcripts were reviewed
to source genuine misses and build the failure taxonomy *before* any scenario was written, rather than asking
a model to invent scenarios cold. 31 real transcripts (every observed compact-focus / handoff firing plus
discovered no-cue miss candidates across ~2.2k sessions) yielded 55 trigger moments and a 10-category failure
taxonomy; seeds were then hand-written and hand-reviewed to set the distribution from those real moments.
Review stopped at saturation — the last ~dozen traces surfaced no new failure category, every one
re-instantiating one of two dominant patterns: compact-focus missing on a heavy / near-exhaustion window, and
handoff missing on a "finished Y, now do X" new-goal pivot.

`cf-01` is **seed #1**: the real compact-focus failure that motivated the project.

The next stage of the recipe — synthetic scale-up from these seeds, then filtering — is intentionally not yet
applied; the seed set is the hand-reviewed distribution it would scale from.

## Provenance

Most scenarios are grounded in real trace moments. Five are **synthetic-extrapolation** and are marked here
because that distinction matters when reading the rates: `cf-11`, `cf-12`, `cf-13`, `ho-15`, `ho-16`. Source
session paths are local and private and are deliberately not committed; provenance is recorded at this
grounded-vs-synthetic granularity.

## Known limitations (read before trusting any rate)

These are stated, not hidden behind a green number — a corpus that cannot discriminate must be fixed before
its verdict is trusted.

- **The negative space is thin and skewed.** Genuine `should_fire: false` cases are scarce in real traces.
  Only two negatives are solidly grounded (`ho-12`, `ho-13`), both handoff, both with a trigger word present —
  so they exercise *cued* false-fire, not the *no-cue* false-fire the eval ultimately cares about. There is no
  grounded compact-focus negative and no grounded cue-absent negative for either skill. Before the false-fire
  rate is treated as trustworthy, more grounded no-cue negatives — for both skills — should be authored and
  human-validated; the synthetic five above are a placeholder, not that evidence.
- **Framing is skewed** toward imperative and deliberation; tangential/unrelated negatives are almost entirely
  synthetic, and no real tangential/unrelated handoff true-fire was observed.
- **Cue confound.** Nearly every real positive is either a cued-fire or a no-cue miss where a cue arrived a
  turn later, so the corpus measures the self-activation *gap* well but offers few clean, isolated no-cue
  moments with no nearby cue at all.
- **compact-focus self-use is not headlessly measurable.** Its trigger is the live window's actual state, which
  a single headless turn cannot reproduce, so all 10 compact-focus positives are dropped (see *Replayability*).
  The headless baseline therefore covers handoff self-use + both skills' false-fire, but says nothing about
  compact-focus self-activation — which likely needs a multi-turn / stateful replay or a harness-level signal,
  an escalation this instrument surfaces rather than hides.
