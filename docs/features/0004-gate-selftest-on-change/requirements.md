# 0004-gate-selftest-on-change — Enforce selftest invariants when the framework changes

## Problem

The framework now has selftests that prove its most important maintenance invariants, including the practice-skill vendor-divergence gate, but those checks still depend on a maintainer remembering to run them by hand. That leaves a trust gap at the exact moment risk is introduced: source changes can be written, reviewed, and accepted without a fresh signal that the framework still protects the invariants it claims to protect.

Maintainers feel it because every relevant change carries a hidden manual step. Reviewers feel it because review confidence depends on a remembered command rather than an enforced result. Adopters feel it later if a broken or drifted framework is shipped as healthy.

## Outcome

Relevant framework changes automatically produce a current selftest signal before they are treated as healthy. The existing invariant checks stay the source of truth; this feature makes their execution part of the normal change path for both framework homes, so enforcement no longer depends on individual memory.

User stories:

- **Maintainers get an automatic guard** — changing framework source that can affect selftest-backed invariants produces a selftest result without relying on a remembered manual run.
- **Reviewers get a trustworthy signal** — a relevant change is reviewable with visible evidence that the selftest-backed invariants still hold.
- **Both framework homes stay protected** — the enforcement expectation applies to the development repository and the imported repository, so one home does not silently become less guarded than the other.
- **Failures point back to the invariant** — when enforcement fails, the maintainer can see that the framework invariant is blocked and can re-run the same check deliberately after fixing it.

The signal that confirms it: after this feature lands, no relevant framework change is considered healthy without a fresh selftest result, and a deliberately broken selftest-backed invariant is caught before the change is accepted.

## Guarantee

- **Change-time enforcement owns the trust gap** — the framework's invariants matter most while source is being changed, because a drift that slips through review becomes part of what adopters inherit. The enforcement policy exists to make those invariants active at change time rather than remembered after the fact.
- **Repo parity preserves framework trust** — the same framework cannot have one guarded home and one convention-only home without splitting reviewer and adopter confidence. Both homes need the same enforcement expectation even if later stages decide how to keep that expectation maintainable.

## Non-goals

- **Redefining the selftest invariants.** The divergence rule and other existing selftest checks are accepted inputs; this feature decides when they are enforced, not how they compute their verdict.
- **Folding this into 0002.** The practice-skill shipping work is complete. This feature covers repo-wide enforcement for future changes.
- **Replacing broader maintenance workflows.** Existing health and maintenance commands may compose with this feature, but this feature is not a redesign of every framework audit path.

## Upstream

- Session handoff: `/private/tmp/claude-501/-Users-admin--local-share-metacognition/14ac09be-0f48-4aa3-a0f6-c93a30d2a3af/scratchpad/handoff-gate-autotrigger-leanplan.md`
