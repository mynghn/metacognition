# 0001-self-initiated-skill-activation — SPEC

## Outcome

### O-1: skill-fires-on-cueless-match
When a turn presents a situation that matches a scoped skill's purpose, and the operator names no skill and uses no trigger word, the agent invokes that skill instead of improvising past it. One-shot verifiable: replay a labeled no-cue scenario for a scoped skill and observe whether the skill is invoked.

### O-2: passed-over-moment-observable
When a turn that should have invoked a scoped skill completes without it firing, the non-invocation is captured as a reviewable event that carries the moment and the skill that should have fired. The miss is observable after the fact rather than silent. This observability is what makes O-1's rate countable at all (REQUIREMENT "Misses become visible").

## Invariants

### INV-1: self-use-rate-beats-baseline
Across the designated no-cue evaluation set (INV-3), the rate at which scoped skills self-invoke on the moments that call for them holds at or above the pre-recorded baseline by an agreed margin, and sustains across repeated runs rather than spiking once. Verified by re-running the set and comparing against the recorded baseline. The margin is a setup parameter fixed before baseline capture — its value is not an observable this SPEC pins; the testable predicate is "rate ≥ baseline + margin, sustained". Realizes the REQUIREMENT success signal as its observable form.

### INV-2: false-fire-rate-bounded
Across the same evaluation set, the rate at which a scoped skill is surfaced or invoked on a moment that does not call for it stays at or below an agreed bar (a setup parameter, fixed with the baseline). Realizes the REQUIREMENT "No crying wolf" system policy as its observable form: precision is constrained, not only recall.

### INV-3: scope-and-measurement-binding
The guarantees above hold within, and only within, a designated environment. The scoped skills are the compaction and handoff skills first. The measurement substrate is a designated set of realistic no-cue situations — both matching and non-matching, each labeled with whether a scoped skill should fire — against which a baseline self-use rate and false-fire rate are recorded before any change is made. Behavior outside this scope is not constrained by this SPEC; widening the scoped-skill set re-binds the contract.

## Non-goals
- **The explicit-cue path.** Moments where the operator names the skill or uses its trigger word are not contracted here; that path is separately and mechanically addressable (REQUIREMENT Non-goals). O-1 covers only the no-cue case.
