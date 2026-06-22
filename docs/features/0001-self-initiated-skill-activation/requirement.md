# 0001-self-initiated-skill-activation — Use the right skill without being told

## Problem

The agent silently does worse work because it fails to use skills it already has. When a moment calls for an installed skill but the operator gives no naming cue — and the agent has already framed the moment as ordinary chat or coding — the skill goes un-invoked. The agent proceeds on its own, without the distilled practice the skill encodes: a compaction improvised by hand instead of the tailored routine, a domain judgment made without the codified knowledge, a session boundary crossed without the handoff discipline. Nothing fires and nothing is recorded, so the miss is invisible — the operator catches it only by luck, if at all.

Two costs compound. The work is quietly worse than it should be. And the effort invested in building the skill library is wasted every time the library isn't consulted. The operator's only remedy today is to name the skill by hand on every occasion — which defeats the purpose of skills that are supposed to know their own moment. The pain is sharpest precisely when no keyword is present: a named request can be caught mechanically, but an unnamed, self-initiated moment cannot.

## Outcome

The agent brings the right codified practice to bear at the moment that calls for it, without being told to — the skill's own sense of "when" is enough. The operator stops having to name a skill for it to fire, and stops silently losing the value of the skills they have built. Scope is deliberately narrow first: prove it on the skills where the gap is observed or anticipated — the compaction and handoff skills — before extending the approach to the wider library.

User stories:

- **Fires on its own cue** — when the operator describes a situation a skill exists for, without naming the skill, the agent uses the skill instead of improvising past it.
- **Misses become visible** — when the agent proceeds without a relevant skill, that is a reviewable event the operator can see and count, not a silent gap. This visibility is what makes the problem measurable at all.

System policies:

- **No crying wolf** — surfacing or running a skill when the moment does not call for it is itself a failure. A cure that over-fires trains the operator to ignore it and gets switched off, so precision matters as much as recall. SPEC owns the observable precision bar.

The signal that confirms it: on an agreed set of realistic no-cue situations — moments where a skill should fire and the operator names nothing — the relevant skill is actually used measurably more often than today's baseline, and that lift holds rather than being a one-off. Establishing the baseline comes first, because today the miss cannot even be counted.

## Non-goals

- **The named case.** Moments where the operator does name the skill or use its trigger word are separately and mechanically addressable; they are not this project's problem. This project owns the no-cue, self-initiated moment.
- **A whole-library mechanism up front.** A universal "consider every skill, every turn" behavior across the entire library is out of initial scope; generalizing beyond the observed-defect skills is a later, evidence-gated step.
- **Solving by plausibility.** A change that cannot show measured lift over baseline does not count as a solution here, however reasonable it sounds — an unmeasured mechanism is explicitly not an acceptable outcome.
