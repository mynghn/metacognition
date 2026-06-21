# T1 — heal one entry

The leaf tier and the MVP: reconcile a **single decayed entry** against current sources, in place.
T1 is exactly one engine verb — `refresh <slug>` — wrapped in the shared spine and envelope. It
adds no mechanism of its own; it is the *procedure* that ties detection → reconciliation →
verification → route together for one entry. It is **provider-neutral**: only the installer-resolved
`@`-tokens, `git`, and independent sub-agents — no agent-specific tool.

Read **`references/verification.md`** (the envelope) and **`references/propose-on-branch.md`** (the
spine: gate, proposal branch, the lighter single-change path, the `Heal-*` schema) before any write.
This file summarizes their verdicts only as far as it needs to map signal → route; those files remain
authoritative for the mechanics.

## From signal to heal

T1 starts from a target: a maintainer names an entry, or a `@HEALTH_CHECK@` worklist line does
(`<stem>/<slug>: [dead-link <url>] [over-age <days>d] [sub-tier <host>]`). Each tag names *one*
flagged thing and says *why* the entry surfaced — but a tag is a **lint, not a verdict**: the route
depends on what reconciliation finds, not on the tag alone.

- **`[dead-link <url>]`** — one cited reference no longer resolves. Replace it with an equivalent
  **live** source backing the *same* claim → a mechanical swap (auto). A dead link beside a surviving
  live at-or-above citation strips no support — just drop it (auto). But if that reference was the
  claim's **only** live at-or-above backing and no replacement is found, the claim is left with no live
  authoritative support → **quarantine** (see the trigger note below — the engine gate will *not* catch
  this case for you).
- **`[over-age <days>d]`** — past the topic's freshness threshold; the *content* may be unchanged.
  Re-verify against current SOTA. Unchanged → restamp `last_refreshed` only (mechanical → auto). A
  claim moved → a claim-change (proposal). The decay is **structural** (the topic has split, the entry
  must be divided) → this is **not a T1**: stop and hand it to T2; never force-fit a split into a
  refresh.
- **`[sub-tier <host>]`** — health-check flags **each** cited host below the `@SOURCES@` bar, *per
  host*, even when another citation clears it. So the tag alone does not mean the entry is under-sourced:
  the engine gate rejects a plain refresh only when **no** cited host clears the bar (one at-or-above
  source admits the whole entry). Another source already clears → the sub-tier cite is a non-blocking
  lint, drop or swap it (policy-fix → auto), **no `degraded:` marker**. The sub-tier host is the entry's
  **sole** support and no at-or-above replacement is found → **quarantine**.

**The quarantine trigger, precisely:** the claim is left with **no live at-or-above source** — its sole
support is below the bar (sub-tier), *or* its sole citation no longer resolves (dead), *or* it would be
left with no citation at all. The engine source-gate catches **only the live-sub-bar** case (it rejects
when no host clears the bar) and it **fails open** when an entry has zero source hosts — so a dead or
dropped sole citation slips past it. Never lean on the gate alone: when reconciliation leaves a claim
without live authoritative support, the skill **must** quarantine (carry the `degraded:` marker) rather
than write an under-sourced entry clean. A maintainer-named target with no tag is the same procedure —
research the entry and let the change class pick the route.

## The procedure

1. **Pick the target** `<stem>/<slug>` — from the request or one worklist line. One entry per T1 run.
2. **Reconcile in place.** Research current state-of-the-art **with citations** (web search, or a
   research skill if the provider has one). Rewrite the **single canonical entry** so it supersedes the
   stale claim — never append a competing view, never split (that is T2). Restamp `last_refreshed`;
   refresh `sources`. A load-bearing number the heal introduces or changes **must carry a corroborating
   source** (≥2 distinct sources for that number): **nothing mechanical enforces this** — the engine
   source-gate tests authority, not corroboration, and no detector flags it — so the envelope's
   reviewers are its sole enforcement (step 3). The result is one candidate `<slug>.md` (full file,
   frontmatter included).
3. **Verify** — run the envelope (`verification.md`) on the candidate. You (the reconciler) run only
   the mechanical floor (`@NO_NET_LOSS@` + citation resolve); **every judgment verdict** is made by
   **independent reviewers that did not produce the heal**. A deliberate supersession (a number/claim
   you updated against a re-fetched source) **will** trip the `@NO_NET_LOSS@` floor — the old value
   shows as dropped; that is **expected**, not a failure: the nonzero exit routes each drop to the
   reviewers, who adjudicate sanctioned-supersession vs silent loss. The envelope's reviewer checklist
   also carries the two duties T1 leans on: **Corroboration** (a single-sourced load-bearing number is a
   reject) and, for a degraded candidate, **Degrade justification** (the reviewers independently re-run
   the at-or-above search behind the degrade). A majority refute fails the candidate (a refuted auto
   change downgrades to a proposal; a refuted proposal is fixed and re-run).
4. **Classify and route** (next section) on the *reconciled candidate vs the current entry*.

## The two paths, and quarantine

The spine has two write paths; T1 adds quarantine as a **proposal sub-case**, not a third auto outcome.

| Class | When | Path | Provenance |
|---|---|---|---|
| **Mechanical, claim-preserving, bar met** | equivalent dead-link swap; `last_refreshed` restamp on re-verification; dropping/swapping a sub-tier cite while another source clears the bar. **No claim a reader relies on changes.** | `refresh` straight to `main` after the envelope clears | `Heal-mode:auto`, `Heal-verdict:dead-link\|current\|policy-fix` |
| **Claim-affecting** | a number, claim, or conclusion would change | proposal branch, or the single-change lighter path — `git diff` is the ratifiable artifact, **merge = ratify** | `Heal-mode:ratified`, `Heal-verdict:stale` |
| **Quarantine** (proposal sub-case) | the claim is left with **no live at-or-above source** (sole support below the bar, dead, or absent) and no replacement is found | proposal — the maintainer ratifies the degrade; see below | `Heal-mode:ratified`, `Heal-verdict:degraded` |

When unsure between auto and proposal, route to the proposal — ratification is cheap, a wrong silent
write is not.

### Quarantine routes to the proposal path

When reconciliation leaves a claim with no live at-or-above source, do **not** write the entry dirty
and do **not** delete it — knowledge leaves the vault only by an explicit ratified `remove`. `refresh`
the candidate **with a `degraded: <reason>` frontmatter marker** naming the deficient support; for a
live-sub-bar source the engine admits the otherwise-refused write *iff* it carries that marker (its
quarantine exemption), and it prefixes the entry's INDEX line with `⚠`.

Route the degrade to the **proposal path**, not auto. The load-bearing reason: a degrade asserts a
**negative — "no at-or-above source exists"** — found by the reconciler, and absence-of-evidence is the
one verdict no fetch can confirm. The envelope's **Degrade-justification** check makes each independent
reviewer re-run that search (so the negative is quorum-checked, not taken on the reconciler's word — a
reviewer that finds a qualifying live source turns the heal into a policy-fix, not a degrade); but even a
clean quorum cannot *prove* non-existence, so "when unsure → proposal" applies at its strongest and the
maintainer makes the call. (Applying the `⚠` down-rank is also a standing change, but that is the lesser
reason — the unverifiable negative is why.) The proposal review **is** the enqueue-for-human-review;
merging applies the `⚠` mark. A degrade is a single-entry, single-verb ratifiable change, so the spine's
lighter path fits — present the degrade (the `git diff`, the "no replacement found" finding, and the
reviewers' confirmation of it); on the maintainer's yes, `refresh` on `main` with `Heal-mode:ratified`:

```sh
@ENGINE_BIN@ --config @CONFIG_DIR@/<stem> --vault @VAULT@ refresh <slug> \
    --sources @SOURCES@ --trailer Heal-mode:ratified --trailer Heal-verdict:degraded [...] < candidate.md
# candidate.md frontmatter carries:  degraded: "sole source <host> below the authority bar; no replacement found"
# [...] = the rest of the Heal-* schema (Heal-confidence, Sources-before/after, Heal-run) — see propose-on-branch.md
```

### Healing an already-degraded entry

A quarantined entry returns as a T1 target once a maintainer acts on its review. The `⚠` down-rank is
toggled **purely by marker presence** in the candidate: a successful re-source **must omit** the
`degraded:` key (a marker-free `refresh` clears the `⚠`); a still-failed re-source **re-carries** it
with an updated reason. Copying the prior frontmatter verbatim would strand a stale down-rank on a
now-healthy entry — drop the key deliberately when the source is restored.

**Clearing a degrade routes by the re-source's own class, not as another degrade.** Unlike *applying* a
degrade (an unverifiable negative → always proposal), *clearing* one rests on a **found, verifiable
positive** — a specific live at-or-above source now backs the claim — so it rides whatever route that
re-source is: a claim-preserving re-source that only swaps in the good source and drops the marker is a
policy-fix (auto); a re-source that also moves a claim is claim-affecting (proposal).

### When no defensible heal exists

If research cannot produce a demonstrably-correct reconciliation — or a proposal candidate cannot pass
review after a fix — **leave the entry unwritten and unchanged** and report it for human attention.
No write is itself a valid T1 outcome: the floor is never write dirty, never silently drop.

## Worked outcomes (the acceptance cases)

- **Dead-link-only heal → auto.** A `[dead-link]` whose reference has an equivalent live mirror: swap
  the citation, claim unchanged, envelope clears. One `refresh` commit on `main`, `Heal-mode:auto` — no
  human step.
- **Number/claim-change heal → proposal.** A `[over-age]` entry whose re-verification moves a
  load-bearing number (now carrying its corroborating source): claim-affecting → a `proposal/t1-<slug>-<n>`
  branch or the lighter path. `main` is untouched until merge; the `git diff` is the ratifiable
  artifact the maintainer merges to apply.
- **Sole source below the bar, no replacement → quarantine.** A `[sub-tier]` entry whose only support
  stays below the bar after research (and after the reviewers' own search): `refresh` with
  `degraded: <reason>` on the ratified proposal path, `⚠`-down-ranked in INDEX, the maintainer confirming
  the degrade — never written dirty, never deleted.

## What stays true

T1 invents no new engine mechanism and no new routing *enforcement*: the routing is a documented,
agent-followed procedure (the engine is vocabulary-free — see verification.md, "what enforces this and
what does not"). The mechanical primitives it composes are each already pinned — the spine
(`maintenance-selftest`), the no-net-loss floor (`no-net-loss-selftest`), and the `degraded`-admit +
`⚠` down-rank (engine `selftest`) — and `maintenance-selftest` additionally pins the degraded write
carrying `Heal-*` provenance through the maintenance route end-to-end. Every T1 write is one engine
commit carrying `Heal-*` provenance, individually revertible, and either auto-gated through the
envelope or human-ratified — never a silent, un-provenanced edit.
