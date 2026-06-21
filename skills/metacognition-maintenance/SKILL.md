---
name: metacognition-maintenance
description: Heal and evolve the Metacognition knowledge vault on demand — reconcile a decayed entry against current sources (T1), re-derive a sibling's entry-set (T2), or evolve the family (T3), routing each change through gated auto-apply or a ratifiable proposal branch. Use when asked to maintain, heal, verify-and-refresh, or evolve the vault, or to act on a health-check worklist. Drives kb-engine as the sole writer (never edits vault files directly) and runs only on explicit request, never on a schedule.
---

# Metacognition vault maintenance

Heal and evolve the shared knowledge vault. This skill is **provider-neutral** — it drives only
the `kb-engine` / `health-check` CLIs and `git`, and any sub-agent step ("spawn N independent
reviewers") is phrased so Claude, Codex, or any agent realizes it with its own mechanism. The
same skill ships byte-identical to every provider.

It assumes the installer has resolved these absolute paths:

- `@ENGINE_BIN@` — the `kb-engine` writer; a target in topic `<stem>` uses `--config @CONFIG_DIR@/<stem>`
- `@CONFIG_DIR@` — per-sibling configs · `@VAULT@` — vault repo root · `@SOURCES@` — authority policy
- `@HEALTH_CHECK@` — the deterministic decay detector · `@NO_NET_LOSS@` — the no-net-loss diff (the verification floor)
- `@FAMILY@` — the `FAMILY.md` family registry · `@FAMILY_REPO@` — the engine repo root holding `@FAMILY@`/`@CONFIG_DIR@` (the registry side of a T3 family change)

## Two laws (never violated)

1. **The engine is the sole writer of vault entries.** Read vault files freely to decide *what* to
   change, but **never hand-edit a knowledge entry or its INDEX**. Every entry write — capture,
   refresh, remove — is a `kb-engine` commit, so it is validated, source-gated, and recorded as one
   recoverable commit in the vault's history. (Family-level policy/registry files — `FAMILY.md`,
   `SOURCES.md` — are engine-repo artifacts, not vault content, and fall outside this rule; they
   evolve through their own plain-`git` propose→ratify path. `FAMILY.md` + `config/` are owned by the
   family tier, T3; `SOURCES.md` policy edits ride the same shape but no tier in this feature owns
   them.)
2. **Only authoritative sources, or quarantine.** Every write is gated against `@SOURCES@`. If a
   reconciliation's sole support falls below the bar and no at-or-above replacement is found, do
   **not** write it dirty and do **not** delete the entry — `refresh` it *with* a
   `degraded: <reason>` frontmatter marker (the engine down-ranks it `⚠` in the INDEX) and leave
   it for human review. Knowledge leaves the vault only by an explicit ratified `remove`.

## When this runs

Only on explicit demand — the maintainer triggers a heal/evolution, or hands you a worklist.
**Nothing here runs on a schedule or on its own.** Detection is separate and read-only: a health
pass surfaces *candidates*, it never acts.

```sh
@HEALTH_CHECK@        # → worklist: `<stem>/<slug>: [dead-link <url>] [over-age <n>d] [sub-tier <host>]`
```

## A maintenance run

1. **Scope the targets** — from the maintainer's request, or from a health-pass worklist (a
   `[dead-link]` / `[over-age]` / `[sub-tier]` line names an entry to heal).
2. **Classify the tier**:
   - **T1 — heal** one entry: reconcile it in place against current sources, routing the result
     auto / proposal / quarantine. See **`references/heal-t1.md`**.
   - **T2 — sibling evolution**: re-derive the *whole* sibling, emitting a keep/refresh/split/
     merge/retire/re-scope diff as a proposal. Never a blind single-entry insert. See
     **`references/sibling-evolution.md`**.
   - **T3 — family evolution**: re-derive the *whole family*, emitting an add/merge/retire-sibling
     or boundary-move as a proposal that spans **two repos** — the sibling entries (vault, via the
     engine) **and** the `@FAMILY@` registry + `config/` edit (engine repo, plain `git`; the engine
     does not write registry files). Carries the admission-test verdict and a bilateral
     reconciliation. See **`references/family-evolution.md`**.

   T2/T3 always re-derive the whole sibling/family before emitting any op (the holistic check) —
   there is no single-entry (or single-sibling) insert path.
3. **Research & reconcile** — gather current state-of-the-art *with citations* (web search, or a
   research skill if your provider has one) and reconcile in place: supersede stale claims in the
   one canonical entry, never append a competing view. Restamp `last_refreshed`; refresh `sources`.
4. **Verify before writing** — run the verification envelope on the reconciled result. You (the
   reconciler) run only the *mechanical* floor — the `@NO_NET_LOSS@` diff + citation resolve;
   **every judgment verdict** (does a citation support its claim, is a flagged drop a real loss,
   has scope drifted, is any claim refuted) is made by **independent reviewers that did NOT produce
   the heal** — never self-check your own work. Default-REJECT; N odd (no tie); majority refute
   fails. It runs identically on both write paths; a refute downgrades an auto change to a
   proposal. See
   **`references/verification.md`**.
5. **Route through the gate and write** — mechanical + claim-preserving → auto-apply; claim-
   affecting / structural → a ratifiable proposal branch. See **`references/propose-on-branch.md`**
   for the gate, the worktree+branch proposal, ratify=merge / reject=delete, and the restartable
   composite-op applier. Every commit carries `Heal-*` provenance trailers (schema in that file).

## References (load on demand)

- **`references/propose-on-branch.md`** — the write spine: gate, proposal worktree+branch,
  ratify/reject, restartable composite applier, provenance schema. **Read before any write.**
- **`references/verification.md`** — the verification envelope: citation re-fetch, the
  no-net-loss diff, and the default-REJECT adversarial quorum. **Read before any write.**
- **`references/heal-t1.md`** — the **T1 heal** procedure: signal→route mapping and the
  auto / proposal / quarantine outcomes for one entry. Read when healing a single entry.
- **`references/sibling-evolution.md`** — the **T2 sibling-evolution** procedure: whole-sibling
  re-derivation → a keep/refresh/split/merge/retire/re-scope diff, emitted as one proposal. Read
  when the sibling's decomposition (not just one entry's content) is what's wrong.
- **`references/family-evolution.md`** — the **T3 family-evolution** procedure: whole-family
  re-derivation → add/merge/retire a sibling or move a boundary, emitted as one cross-repo proposal
  (vault entries + the `@FAMILY@` registry edit) with the admission verdict and bilateral
  reconciliation. Read when the disruption crosses sibling boundaries.
