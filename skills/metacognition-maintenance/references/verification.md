# Verification envelope: the guard before any write

The envelope is the load-bearing guard against the **healer's own failure modes** — a fabricated
citation, a silently dropped claim/source, a plausible-but-wrong reconciliation. It runs on the
*reconciled candidate*, before any `kb-engine` write, **identically on both write paths** (auto and
proposal).

**Cardinal rule — independence.** You cannot guard an LLM's failure mode with the *same* LLM's
unaided judgment. So the envelope splits the work in two, by who may do it:

- the **reconciling agent** (the one that produced the candidate) may run ONLY the *mechanical*
  steps — the deterministic `@NO_NET_LOSS@` tool and the citation *fetch* (does the URL resolve).
  It never adjudicates its own work.
- **every judgment verdict** — does a citation actually SUPPORT its claim, is a flagged drop a
  sanctioned supersession or a silent loss, has the entry drifted out of scope, is any claim
  refuted — is made by **independent reviewers** that did NOT produce the reconciliation.

It is provider-neutral: a shell HTTP client (`curl`/`wget`), the `@NO_NET_LOSS@` CLI, and
independent sub-agents (each provider spawns them with its own mechanism). No agent-specific tool.

## Step A — deterministic pre-pass (the reconciler may run this)

1. **No-net-loss floor** — run the tool on the candidate against the current entry:

   ```sh
   @NO_NET_LOSS@ <prior-entry.md> <candidate.md>     # exit nonzero iff something was dropped
   ```

   It lists every dropped `[[link]]`, dropped load-bearing number, and dropped citation source
   (by host), and flags a `description` change. A nonzero exit means **stop** — each drop must be
   adjudicated in Step B. The tool is the floor, not the ceiling: it cannot see a prose claim with
   no number/link/source, a bare 1-3 digit count ("3 reviewers", "350 ms"), or a same-host source
   swap — those go to Step B. A reported `dropped-link` may be a *rename* whose replacement appears
   as a body addition; Step B pairs them rather than treating it as a retired cross-link.
2. **Citation resolve** — for every new or changed citation, fetch the URL (`curl -sSL`/`wget`).
   A non-resolving reference cannot back a claim. (Resolve is mechanical; whether the source
   *supports* the claim is judgment → Step B.)

## Step B — independent adversarial review (NOT the reconciler)

Spawn **N independent reviewers** (default **3**; keep **N odd**), none of which produced the
reconciliation. **Each reviewer independently evaluates the WHOLE candidate against ALL of the
checks below** — do NOT split the checks across reviewers: a flaw only one reviewer is assigned to
look for would be outvoted by the rest under the majority rule. Decorrelate by *independence*
instead — each reasons on its own, none sees another's verdict, and vary the framing/emphasis per
reviewer so they do not share one blind spot. Each is told to **assume the candidate is wrong and
try to refute it**, and to **default to REJECT when uncertain** (the bar is "is this demonstrably
correct?", not "is it plausible?"). Every reviewer checks:

- **Support** — for each claim's citation, read the *fetched* source and confirm a quoted span
  actually supports *that* claim. A resolved-but-unsupported citation is the fabricated-citation
  failure mode.
- **No-net-loss adjudication** — for each drop the tool flagged (link / number / source) and each
  prose claim or cross-link gone from the candidate, decide: sanctioned supersession (e.g. a number
  updated against a re-fetched source, a link retired deliberately) or silent loss?
- **Scope drift** — does the entry still sit within its declared `description` boundary, or has it
  quietly become a different entry? (A `description-changed` flag is the prompt to check this.)

A reviewer votes **REJECT** if it finds any silent loss, scope drift, or unsupported citation, or
cannot demonstrate the candidate correct on at least one load-bearing claim.

**Aggregate (default-REJECT): a majority-REJECT FAILS the candidate; only a majority accept clears
it** (odd N + binary votes → there is never a tie). On failure:

- a candidate routed to the **auto** path is **downgraded to the proposal path** (committed to a
  `proposal/...` branch for human ratification — see `propose-on-branch.md`), never auto-written;
- a candidate already on the **proposal** path is **fixed and re-run**, not surfaced refuted.

## Recording the outcome

Carry the result into the `Heal-*` provenance: the review's `Heal-confidence`, and — when a refute
downgraded an auto change — the fact it became a ratified proposal (`Heal-mode:ratified`, not
`auto`). `git log` then shows both that the change was verified and how it was gated.

## What enforces this (and what does not)

Only the Step-A no-net-loss tool is mechanically enforced once invoked. **Everything else is
agent-enforced** — that the envelope runs at all on the auto path, the gate's mechanical-vs-claim
classification, and the reviewers' verdicts. The engine is deliberately **vocabulary-free**: it
records the `Heal-*` provenance trailers but never reads them, so it *cannot* refuse an auto write
that skipped the envelope (giving it that power would make the shared writer learn one feature's
words — the very coupling the engine is designed to avoid). This is the inherent boundary of an
LLM-in-the-loop maintainer. The backstop is the proposal path's human reviewer, which is why any
refuted **or uncertain** change is routed there rather than auto-applied.
