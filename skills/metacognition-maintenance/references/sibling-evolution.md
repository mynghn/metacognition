# T2 — evolve a sibling

Re-derive a **whole sibling's entry-set** and emit the change as a ratifiable diff. Where T1 heals one
entry *in place*, T2 fixes the sibling's **decomposition** — entries that overlap, an entry that sprawls
two concepts, a topic that has split, a gap, a stale boundary. T2 is **always a proposal** (never auto):
a decomposition change is structural, and structural changes are ratified, not silently applied.

T2 invents no new engine verb. Its ops are compositions of `refresh`/`capture`/`remove` (below), run as
one multi-commit proposal through the spine's **restartable composite applier**. The mechanism already
exists and is pinned; the new work is the **re-derivation and its review**. It is **provider-neutral**:
only the installer-resolved `@`-tokens, `git`, and independent sub-agents.

Read **`references/propose-on-branch.md`** (the composite applier, branch/ratify mechanics, the `Heal-*`
schema) and **`references/verification.md`** (the envelope) before any write. Each *refresh* op T2 emits
is a T1 heal — reuse **`references/heal-t1.md`** for it (including its quarantine handling, below). A
*capture* op is a brand-new entry, so it has no T1 decay loop: it runs on the spine + envelope with
researched, cited content.

## The cardinal rule — no single-entry insert (the holistic check)

**Every** add / split / merge / retire / re-scope is the *output* of a whole-sibling re-derivation that
passes an orthogonality check — there is **no** path that touches one entry in isolation. Even "just add
one entry" triggers the full re-derivation: a new concept can overlap an existing entry, belong inside
one, or split one — and you cannot see that without looking at the whole set. A blind single-entry insert
is the failure mode T2 exists to prevent. (A genuine *single-entry content* decay, with the
decomposition still sound, is a **T1** heal, not T2.)

## When T2 (vs T1 / T3)

- **T1** — one entry's *content* decayed; the sibling's decomposition is still right. Heal in place.
- **T2** — the sibling's *decomposition* is wrong: entries overlap or have a gap, one entry covers two
  concepts (split), two cover one (merge), an entry is obsolete (retire), or a boundary drifted
  (re-scope). This is also where a T1 heal lands when it discovers the decay is structural.
- **T3** — the disruption crosses sibling boundaries (a whole sibling should be added / merged / retired,
  or a boundary between *siblings* moves). That carries a `FAMILY.md` edit → family evolution.

## The procedure

1. **Scope the sibling.** Read its **whole** entry-set — `<sibling>/INDEX.md` and every
   `<sibling>/knowledge/*.md`. Read freely; the engine remains the sole writer.
2. **Re-derive the decomposition** (the holistic step). Ask: given current SOTA, what set of
   **orthogonal** entries *should* this sibling hold? The orthogonality check — each entry one concept,
   no two overlapping, no gap between them, granularity neither too fine nor too coarse. The output is the
   *target* set, derived from the subject matter, not patched from the current set.
3. **Diff current → target** as a list of ops, each one entry (or entry pair):

   | Op | Meaning | Verb composition |
   |---|---|---|
   | **keep** | entry is correct as-is | none |
   | **refresh** | content update, boundary unchanged (a T1 heal) | `refresh <slug>` |
   | **split** | one entry → two concepts | `refresh <surviving>` + `capture <new>` (a slug free within the sibling) |
   | **merge** | two entries → one | `refresh <target>` + `remove <absorbed>` |
   | **retire** | entry is obsolete | `remove <slug>` |
   | **re-scope** | boundary moves / tightens | `refresh` (one entry, or both for a boundary move between two) |

4. **Research, reconcile, and verify** — every `refresh`/`capture` carries researched, cited,
   reconciled content. The envelope (`verification.md`) splits across two scopes here: its **mechanical
   floor** (the `@NO_NET_LOSS@` diff + citation resolve) runs **per op**, on each entry's candidate; its
   **independent-reviewer judgment** runs **once over the whole-sibling diff** — the reviewers' review
   unit is the entire proposal (every entry's candidate *and* each `remove`), which is what gives them
   the cross-entry visibility the per-entry floor lacks. Two structural facts shape how T2 uses it:

   - **The no-net-loss floor is single-entry.** `@NO_NET_LOSS@ <prior> <candidate>` diffs one slug's prior
     against that *same* slug's candidate (both files must exist). It therefore **cannot run on a `remove`**
     (no candidate) and is **blind to content moving between entries** (it never cross-compares two slugs).
     So for every op that *removes* or *relocates* content, the cross-entry "moved/obsoleted, not lost"
     judgment is the **reviewers' and the human ratifier's**, with no mechanical floor underneath — adjudicate
     each by hand:
     - **split** — the surviving `refresh`'s floor flags the content you moved out as *dropped* (it can't
       see it land in the new entry). Adjudicate against **both halves**: confirm each flagged drop reappears
       in the `capture <new>` entry. The capture itself has no prior, so no-net-loss is N/A for it.
     - **merge** — the target `refresh` passes the floor clean (it only *gained* content); the `remove`
       can't be diffed. Confirm by hand that the absorbed entry's prior content is fully carried into the
       target candidate before the `remove`.
     - **retire** — no candidate to diff; the floor cannot run. The reviewers + ratification confirm the
       knowledge is genuinely obsolete, not silently dropped (nothing leaves the vault except by a ratified,
       adjudicated `remove`).
     - **re-scope** — a boundary move both changes a `description` (the envelope's scope-drift flag — here
       an *intentional*, re-derivation-justified move, not the silent drift T1 rejects) **and** relocates
       content (the losing side's `refresh` trips the link/number/source-drop flags). Adjudicate the drops
       like a merge: confirm the moved content lands in the entry on the other side of the boundary.
   - **Quarantine rides along.** If a content-bearing op's reconciliation can't meet the source bar, do
     **not** let the verb die on the engine's refusal — carry a `degraded: <reason>` marker on that op
     (T1's quarantine, `heal-t1.md` → "Quarantine routes to the proposal path"). The engine admits it via
     its quarantine exemption, and the envelope's Degrade-justification check quorum-verifies the negative.
     T2 is already on the proposal/ratify path, so the degrade needs no separate routing — it rides the
     same merge=ratify gate.

5. **Emit the whole diff as ONE proposal.** Branch `proposal/t2-<sibling>-<n>` off `main`; apply the op
   sequence on the worktree via the **restartable composite applier** (each verb one commit, skip-by-log
   on restart — see propose-on-branch.md). The reviewable artifact is the whole-sibling
   `git diff main..proposal/t2-<sibling>-<n>`; **merge = ratify**, worktree-remove + branch-delete =
   reject (main untouched). Every commit carries `Heal-*` provenance (`Heal-mode:ratified`,
   `Heal-verdict:split|merge|retire|re-scope|stale|current`, one shared `Heal-run` grouping the sibling's
   ops); each op stays individually revertible.

## When the re-derivation finds nothing structural

If the holistic check confirms the decomposition is already orthogonal, the diff is all `keep` /
`refresh` — emit only the refreshes (each a T1 heal on its own route), or, if nothing changed at all,
write nothing and report the sibling sound. A no-op re-derivation is a valid T2 outcome; never
manufacture a split/merge to justify the pass.

## What stays true

T2 invents no new engine or selftest mechanism — its op sequences are all built from already-pinned
verbs. `maintenance-selftest` pins the split composite (`t2-split-1`: `refresh+capture`) and the merge
composite (`t2-merge-1`: `refresh+remove`) by name — multi-commit proposal, ratify-merge,
individually-revertible, restartable skip-by-log. **retire** reuses the `remove` verb whose restartable
skip is pinned *inside* the merge composite, and **re-scope** reuses `refresh` (one or two), key-identical
under the applier's `<verb> <slug>` skip to the split's refresh — so neither introduces a new mechanical
seam. What T2 *adds* is this documented re-derivation procedure and the holistic-check + cross-entry
adjudication discipline — enforced by coherence with the spine + envelope, by independent review, and by
the human ratification every T2 proposal requires (the engine stays vocabulary-free, so "did you re-derive
the whole sibling?" is the agent's and the reviewer's check, not a mechanical gate). Every op is one
revertible engine commit; knowledge leaves only by a ratified, adjudicated `remove`.
