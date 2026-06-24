# VERDICT — no-cue skill-activation candidate matrix

**The gap is closable at the instruction layer.** A standing skill-consultation checkpoint (**C1**) lifts
no-cue handoff self-activation from the 0.09 baseline to ~0.48 across two independent runs, with no added
false-firing — it clears the promotion gate and is **promoted**. Reordering a skill's description
trigger-first (**C3**) *hurt* (0.09 → 0.00), so it is **held** — and that is direct, measured evidence
against the plausibility theory behind the shipped trigger-first wiring.

Scored against `scenarios/baseline-C0.json` (gate: self-use ≥ baseline + 0.10 margin = **0.19**, AND
false-fire ≤ **0.10** bar). Handoff self-use only — compact-focus self-use is not headlessly measurable
(`scenarios/README.md`). N=3 trials/scenario, Opus 4.8, 20 reproducible scenarios.

## Scores

| config | mechanism | self-use | false-fire | verdict |
| --- | --- | --- | --- | --- |
| C0 | baseline — current state, capability-first descriptions | 0.09 | 0.00 | — |
| **C1** | standing skill-consultation checkpoint (system-prompt) | **0.39 / 0.58** (two runs) | 0.00 / 0.00 | **PROMOTE** |
| C3 | trigger-first scoped-skill descriptions | 0.00 | 0.00 | HOLD |
| C2, C4 | reflection pass; keyword-control ceiling | not run | — | deferred |

Per-scenario, handoff positives (fires / 3 trials):

| id | framing | C0 | C1 | C1-confirm | C3 |
| --- | --- | --- | --- | --- | --- |
| ho-01 | deliberation | 3/3 | 3/3 | 3/3 | 0/3 |
| ho-02 | imperative | 0/3 | 2/3 | 3/3 | 0/3 |
| ho-03 | imperative | 0/3 | 3/3 | 2/3 | 0/3 |
| ho-04 | imperative | 0/3 | 0/3 | 0/3 | 0/3 |
| ho-05 | deliberation | 0/3 | 3/3 | 3/3 | 0/3 |
| ho-06 | imperative | 0/3 | 0/3 | 3/3 | 0/3 |
| ho-07 | imperative | 0/3 | 2/3 | 3/3 | 0/3 |
| ho-08 | imperative | 0/3 | 0/3 | 0/3 | 0/3 |
| ho-09 | deliberation | 0/3 | 0/3 | 2/3 | 0/3 |
| ho-10 | imperative | 0/3 | 0/3 | 0/3 | 0/3 |
| ho-11 | imperative | 0/3 | 0/3 | 0/3 | 0/3 |

## C1 — promoted, lift confirmed

A standing checkpoint in the system layer — *"each turn, check whether the moment calls for one of your
skills; if one fits, use it; if not, proceed — don't force"* — raised self-use 4–6× over baseline. The
lift **sustains** rather than spiking once: two independent runs (0.39, 0.58) both clear the gate
decisively, both at 0.00 false-fire. Five positives fire in **both** runs (ho-01/02/03/05/07), two are
intermittent (ho-06/09), and four resist the checkpoint entirely (ho-04/08/10/11 — all plain imperative
"finished Y, now do X" pivots, where the next action is stated so directly the agent simply does it). The
deliberately non-forcing wording is why recall rose with zero false-fire — subject to the negative-space
caveat below.

## C3 — held; trigger-first ordering hurts

Reordering the handoff / compact-focus descriptions trigger-first ("Use when…" leading) — the *only*
change, bodies byte-identical to the installed skills — drove self-use to **0.00**: every positive missed
on every trial, including ho-01, which fires reliably under both capability-first C0 and under C1. This is
clean evidence that the plausibility rationale behind `29c45d0` ("a skill's description is its activation
signal, so leading with the trigger sharpens auto-invocation") is **false for these scoped skills** — it
is actively counterproductive. Caveat: the eval measures the scoped skills, not the KB-wiring skills that
`29c45d0` actually reordered, so this informs that commit's keep/revert question by strong analogy, not by
measuring those skills directly.

## Caveats (read before acting on the numbers)

- **Handoff-only.** compact-focus self-use is not headlessly measurable (its trigger is a heavy live
  window). C1's lift is shown for handoff; whether it carries to compact-focus is unmeasured.
- **False-fire 0.00 is weak evidence.** It rests on 9 negatives, mostly synthetic/cued. C1 added no
  false-firing on them, but a trustworthy precision claim needs more grounded no-cue negatives.
- **C1 is partial, not a cure.** ~0.48 still misses about half the moments; four imperative pivots resist
  it. C1 closes much of the gap, not all of it.

## Recommendation / follow-on decisions (for the operator)

- **Adopt C1** — wire the consultation checkpoint into the shared operating frame. This is a change to
  global config, left for the operator to apply; the eval's job was to select the evidenced mechanism, and
  C1 is it.
- **Revisit `29c45d0`.** Trigger-first hurt the scoped skills; consider reverting it, or at least not
  extending it to the scoped skills' descriptions — now with data rather than plausibility.
- **Optional further measurement:** author grounded no-cue negatives to firm up the false-fire side; run
  C2 (reflection pass) and C4 (keyword ceiling) for a fuller matrix; tackle compact-focus self-use via a
  stateful / multi-turn replay or a harness-level signal (the escalation the instrument surfaces).

## Reproduce

```
run-scenarios --corpus scenarios/corpus.jsonl --config C1 -n 3 --out <manifest> --cwd <fresh-dir> --model claude-opus-4-8
skill-activation-check --corpus scenarios/corpus.jsonl --runs <manifest> --baseline scenarios/baseline-C0.json
```

C3 additionally swaps `configs/C3-skills/<skill>/SKILL.md` over the installed `~/.claude/skills/<skill>/SKILL.md`
for the duration of its run, then restores them (`configs/README.md` → "Why C3 swaps the global skill files").
