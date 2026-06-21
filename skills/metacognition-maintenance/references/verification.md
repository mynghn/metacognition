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
look for would be outvoted by the rest under the majority rule. **For a multi-entry proposal** (a T2
sibling or T3 family diff) the "candidate" each reviewer evaluates is the **whole diff** — every
entry's candidate *and* any candidate-less `remove` — not one entry; that whole-diff view is what
lets a reviewer tell a cross-entry *move* from a loss (the deterministic floor, per-entry, cannot). Decorrelate by *independence*
instead — each reasons on its own, none sees another's verdict, and vary the framing/emphasis per
reviewer so they do not share one blind spot. Each is told to **assume the candidate is wrong and
try to refute it**, and to **default to REJECT when uncertain** (the bar is "is this demonstrably
correct?", not "is it plausible?"). Every reviewer checks:

- **Support** — for each claim's citation, read the *fetched* source and confirm a quoted span
  actually supports *that* claim. A resolved-but-unsupported citation is the fabricated-citation
  failure mode.
- **No-net-loss adjudication** — for each drop the tool flagged (link / number / source) and each
  prose claim or cross-link gone from the candidate, decide: sanctioned supersession (e.g. a number
  updated against a re-fetched source, a link retired deliberately) or silent loss? **For a
  multi-entry proposal** (a T2 sibling or T3 family diff), the review unit is the **whole diff**, not
  one entry, and the tool is single-entry — so a drop flagged on one entry may be content **relocated
  to another entry in the same diff** (a split moving content to a new entry, a merge absorbing one
  into another, a boundary re-scope). Adjudicate each such drop against the whole diff: confirm the
  content reappears in the receiving entry (a move), versus genuinely gone (a loss). A `remove` has no
  candidate for the tool to diff at all, so its loss-vs-obsolete call is wholly this judgment.
- **Scope drift** — does the entry still sit within its declared `description` boundary, or has it
  quietly become a different entry? (A `description-changed` flag is the prompt to check this.)
- **Corroboration** — a load-bearing number the heal introduces or changes MUST carry at least one
  corroborating source (≥2 distinct supporting sources for that number). This is *not* what Support
  checks (Support confirms one citation backs a claim; this counts the distinct sources behind a
  number). Nothing mechanical enforces it — the engine's source-gate tests authority, not
  corroboration, and the deterministic detectors do not flag it — so the reviewers are the **sole**
  enforcement: a single-sourced load-bearing number is a REJECT.
- **Degrade justification** *(only when the candidate carries a `degraded:` marker)* — the marker
  asserts a *negative*: that no at-or-above source backs the claim. That negative was found by the
  reconciler and nothing else re-checks it, so each reviewer **independently attempts the at-or-above
  search**. If any reviewer finds a qualifying live source, the degrade is wrong — REJECT it so the
  heal becomes a policy-fix (re-source) instead; the degrade stands only when the quorum also fails
  to find one.

A reviewer votes **REJECT** if it finds any silent loss, scope drift, unsupported citation, or
single-sourced load-bearing number; if (for a degraded candidate) it finds an at-or-above source the
degrade missed; or if it cannot demonstrate the candidate correct on at least one load-bearing claim.

**Aggregate (default-REJECT): a majority-REJECT FAILS the candidate; only a majority accept clears
it** (odd N + binary votes → there is never a tie). **One exception — the Degrade-justification find
is dispositive:** a *single* reviewer surfacing a qualifying live source fails the degrade (re-route
it to a policy-fix re-source), not subject to the majority — finding a source positively *disproves*
the "no source exists" negative, whereas no reviewer finding one never *confirms* it (which is why a
surviving degrade still goes to human ratification, not auto). On failure:

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
