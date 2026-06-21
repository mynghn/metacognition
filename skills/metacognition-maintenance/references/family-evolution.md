# T3 — evolve the family

Re-derive the **whole family of siblings** and emit the change as a ratifiable proposal. Where T1
heals one entry and T2 re-derives one sibling's *entry-set*, T3 fixes the **family's decomposition**
— which siblings exist and where the boundaries between them lie. Its ops are **add a sibling**,
**merge two siblings**, **retire a sibling**, and **move a boundary between two siblings**. T3 is
**always a proposal** (never auto): a family-structure change is the most structural change the vault
admits, so it is ratified, not silently applied.

T3 invents no new engine verb. The sibling-entry side of every op is the same `refresh`/`capture`/
`remove` composition T2 uses, run through the spine's restartable applier. What is **new** in T3 is
that a family change also edits the **family registry** (`@FAMILY@`) and the per-sibling `config/`,
and those are **engine-repo files, not vault entries** — so a T3 proposal spans **two repos**. It is
**provider-neutral**: only the installer-resolved `@`-tokens, `git`, and independent sub-agents.

Read **`references/propose-on-branch.md`** (the spine: branch/ratify mechanics, the restartable
applier, the `Heal-*` schema), **`references/verification.md`** (the envelope, incl. the
**Family-orthogonality** reviewer check T3 leans on), and **`references/sibling-evolution.md`**
(every sibling-side change in a T3 op *is* a T2 re-derivation of that sibling — reuse it, including
its cross-entry adjudication and quarantine handling) before any write.

## The two sides of a family change (the cross-repo fact)

A T3 op touches two repos with independent histories:

- **Vault side** (`@VAULT@`) — the sibling **entries**: a sibling is a `<stem>/` folder (INDEX +
  `knowledge/*.md`). Adding / merging / retiring a sibling, or moving entries across a boundary, is
  `capture`/`refresh`/`remove` through the **engine** (the sole writer of vault entries), on a
  proposal branch — the spine, unchanged. A T3 vault composite may **span two stems** (e.g. a
  boundary move `remove`s from sibling A's config and `capture`s into sibling B's), so each op runs
  under its own `--config @CONFIG_DIR@/<stem>`; the applier's skip-by-log keys on the full
  engine-shaped subject `<stem>: <verb> <slug>`, which stays correct across stems.
- **Registry side** (`@FAMILY_REPO@`, the engine repo) — the **family-level files**: the `@FAMILY@`
  registry row(s) and the per-sibling `config/<stem>`. These are **not vault content**; the engine
  has no verb that writes them, and the skill's first law (sole writer) **explicitly exempts** them.
  So the registry edit is a **plain `git` hand-edit + commit** on a proposal branch in the engine
  repo — *not* a `kb-engine` write. This is the "own ratify path" the first law promised for
  `@FAMILY@` (the registry + `config/`). (`@SOURCES@` authority-policy edits share the same plain-git
  propose→ratify *shape* but are out of T3's scope — T3 reads `@SOURCES@` as the write-gate input,
  never writes it — and no tier in this feature owns them.)

**The proposal is one logical change split across two branches** — same branch name
`proposal/t3-<change>-<n>` in each repo. **Ratify = merge BOTH; reject = delete BOTH.** There is no
atomic cross-repo merge, so the coupling is a discipline the skill and the human ratifier enforce: a
half-ratify (registry merged, vault not, or the reverse) leaves the family **inconsistent** — a row
claiming a sibling whose entries don't exist, or vice versa. Surface both diffs as one artifact and
ratify them in one sitting; the post-merge **consistency check** (below) is mandatory.

## The cardinal rule — no single-sibling insert (the family holistic check)

**Every** add / merge / retire / boundary-move is the *output* of a whole-**family** re-derivation
that passes a family-level orthogonality check — no structural change is admitted except as the
output of a whole-family (or whole-sibling) re-derivation, so there is **no** path that bolts on one
sibling in isolation. "Just add a sibling"
triggers the full re-derivation: a new topic can overlap an existing sibling, belong inside one, or
pull a concept out of one — and you cannot see that without looking at the whole family. Adding a
sibling therefore routinely **edits a neighbour too** (reconcile the overlap *out* of the shipped
sibling, not only *into* the newcomer) — that is the bilateral reconciliation, below.

**T3 does not discover work.** It runs on a human-triggered cross-sibling disruption — there is no
net-new topic discovery, and nothing runs without a human or change trigger. The holistic
re-derivation places that triggered change correctly within the family — it does **not** scan the
field for missing siblings on its own. A no-op re-derivation (the family is already orthogonal) is a
valid T3 outcome.

## When T3 (vs T2 / T1)

- **T1** — one entry's *content* decayed; heal it in place.
- **T2** — one sibling's *decomposition* is wrong (entries overlap / gap / split / merge / re-scope
  *within* the sibling). One sibling, vault-only.
- **T3** — the disruption **crosses sibling boundaries**: a whole sibling should be added, two should
  merge, one should be retired, or a concept should move from one sibling to another. This is the
  only tier that edits `@FAMILY@`.

## The procedure

1. **Scope the family.** Read `@FAMILY@` (the registry: the family table, boundary rulings, admission
   test) and the **INDEX** of every sibling the disruption could touch — at minimum both sides of any
   boundary in question. Read freely; the engine stays the sole writer of entries and you hand-edit
   only the registry files.
2. **Re-derive the family decomposition** (the holistic step). Given current SOTA and the triggered
   disruption, ask: what set of **orthogonal** siblings *should* this family hold — each one coherent
   and closeable, none overlapping, no gap between them? The output is the *target* family, derived
   from the subject matter, not patched from the current table.
3. **Run the admission test** on the target — the registry's own bar: **coherent + closeable +
   backed by primary sources + non-overlapping** with the rest of the family. Every op states its
   verdict against it:
   - **add** — the newcomer passes admission (and the rule of three still holds for any extracted
     shared pattern);
   - **merge** — the union of the two siblings is still *one* coherent, closeable sibling (not a
     grab-bag);
   - **retire** — the sibling fails to justify a standing slot (obsolete, or it folds into another —
     record it under the registry's *Excluded* with the why, never just delete the row);
   - **boundary-move** — both siblings remain coherent and non-overlapping *after* the move (no new
     gap, no new overlap).
4. **Draft the bilateral reconciliation.** Whenever an op touches the seam between two siblings
   (every merge and boundary-move, and any add that reclaims a concept from a neighbour), reconcile
   **both** sides together — both registry rows' Scope/Boundary text **and** both entry-sets — so the
   family stays orthogonal. Editing one side and leaving the other dangling is the failure mode this
   step exists to prevent.
5. **Diff current → target family** as a list of ops, each two-sided:

   | Op | Vault side (engine, on `proposal/t3-…` in `@VAULT@`) | Registry side (plain `git`, on `proposal/t3-…` in `@FAMILY_REPO@`) |
   |---|---|---|
   | **add sibling** | *first* scaffold the new sibling skeleton (see "Bootstrapping a new sibling" below), *then* `capture` its entries (a multi-`capture` composite); `refresh` any neighbour an entry was reclaimed from | new `@FAMILY@` row (or promote a *planned* row to *built*); `generate`-produced `config/<stem>` + `wiring/<stem>`; edit a neighbour's Boundary text if reclaimed |
   | **merge siblings** | `refresh` the survivor's entries that have a same-slug counterpart (absorbing) + `capture survivor/<slug>` each of the absorbed sibling's **unique** entries (no counterpart — `refresh` would die "entry not found", so it is a `capture` into the survivor) + `remove` **all** the absorbed sibling's entries (cross-stem) — leaves the absorbed `<stem>/` an empty skeleton (see residue note) | remove the absorbed `config/<stem>`; in `@FAMILY@` drop the absorbed row and widen the survivor's Scope/Boundary |
   | **retire sibling** | `remove` all its entries — leaves an empty `<stem>/` skeleton (see residue note) | remove its `config/<stem>`; in `@FAMILY@` move its row to *Excluded* (with the why) |
   | **boundary-move** | move each reclassified concept: `remove <A>/<slug>` + `capture <B>/<slug>` (a folder is fixed, so a move is remove-then-capture across stems); `refresh` the re-scoped survivors on both sides | edit **both** siblings' Scope/Boundary text in `@FAMILY@` (bilateral; no `config` change — both siblings persist) |

   **Bootstrapping a new sibling (add only).** The engine **cannot** create a sibling — `capture`
   requires an existing `<stem>/INDEX.md` and dies "INDEX.md not found" otherwise, and the first law
   forbids the skill hand-writing that INDEX. The sanctioned scaffolder is **`generate <stem>`** (repo
   root): it reads the new `@FAMILY@` row and renders `config/<stem>` + `wiring/<stem>` (engine repo)
   **and** the skeletal `<stem>/INDEX.md` (vault, from `templates/index-skeleton.md`) — the empty
   skeleton INDEX is a **generator artifact, like `config/`** (not a skill hand-edit, not an engine
   write, so the first law and the no-new-engine-primitive rule both hold). So an **add-sibling**
   sequences: write the `@FAMILY@` row → `generate <stem> --no-install` onto the two proposal branches
   (`--no-install` so no adapter deploys before ratification — deployment is the installer's later
   pass) → *then* the engine multi-`capture` of its entries onto the now-scaffolded INDEX.
   **Re-adding a previously-retired stem:** if the stem still has its empty-skeleton residue (below)
   from a prior retire/merge, its `<stem>/INDEX.md` already exists, so `generate` **refuses** (it
   declines "to overwrite an already-scaffolded sibling"). **Skip generate's INDEX render and `capture` straight into the residue INDEX** (it
   already carries the `## <index_heading>` section, so capture works; still no hand-edit, first law
   holds); only regenerate the `config/<stem>` + `wiring/<stem>` the retire removed (`generate --force`
   re-renders those, but mind that `--force` also re-renders the INDEX from the empty skeleton). Use
   `generate` for a truly new `<stem>/`; capture-into-residue for a re-add.

   **Empty-skeleton residue (merge / retire).** `remove` deletes a `knowledge/<slug>.md` and its
   INDEX line only — it never deletes the `<stem>/` folder or its `INDEX.md`, and **no engine verb
   does** (verbs are `capture`/`refresh`/`remove`). So removing a sibling's *last* entry leaves an
   empty `<stem>/` folder + an entry-less `INDEX.md` in the vault. This is **benign, expected
   residue** — an entry-less INDEX surfaces nothing in retrieval (INDEX→JIT), and the registry row is
   gone, so the installer renders no adapter for it. Do **not** hand-delete it (first law); the
   consistency check (step 8) treats an emptied skeleton as the correct end state of a retire/merge,
   not a half-merge.

6. **Research, reconcile, and verify.** Every `refresh`/`capture` carries researched, cited,
   reconciled content (a `capture` has no prior, so no-net-loss is N/A for it; a `refresh` is a T1
   heal — reuse `heal-t1.md`, including its quarantine handling). Run the envelope
   (`verification.md`) over the **whole cross-repo diff** — every entry candidate, each `remove`,
   *and* the `@FAMILY@` edit:
   - the **mechanical floor** (`@NO_NET_LOSS@` + citation resolve) runs **per op**, on each entry's
     candidate, exactly as in T2 — it is single-entry, cannot run on a `remove`, and is blind to
     content moving between entries (here, across siblings). So every cross-sibling **move** and
     every `remove`'s "relocated / obsoleted, not lost" call is the reviewers' and the human
     ratifier's, adjudicated against the whole diff (T2's cross-entry adjudication, now spanning two
     stems);
   - the **independent-reviewer judgment** runs **once over the whole diff**, and for T3 it adds the
     **Family-orthogonality (admission)** check: the reviewers independently re-run the admission
     test on the proposed family and confirm **registry ⇔ vault consistency** — every added/removed
     `@FAMILY@` row matches a vault topic-folder change in the *same* proposal, and the touched
     siblings are non-overlapping with no gap. A family that isn't orthogonal, or a registry that
     disagrees with the vault, is a REJECT (see `verification.md`).
   - **Quarantine rides along** — if a content-bearing op can't meet the source bar, carry a
     `degraded:` marker on that op (T1's quarantine); T3 is already on the proposal/ratify path, so
     it rides the same merge=ratify gate. The envelope's Degrade-justification check quorum-verifies
     the negative.
7. **Emit the whole change as ONE coupled proposal** — the two branches:
   - **Vault side:** `git -C @VAULT@ worktree add -b proposal/t3-<change>-<n> <wt> main`; apply the
     op sequence on the worktree via the **restartable composite applier** (each verb one commit,
     skip-by-log on the full `<stem>: <verb> <slug>` subject — correct across the two stems). Every
     commit carries `Heal-*` provenance (`Heal-mode:ratified`, the family verdict
     `Heal-verdict:add-sibling|merge-sibling|retire-sibling|boundary-move`, one shared `Heal-run`).
   - **Registry side:** use the **same worktree discipline** as the vault side — a plain-`git`
     in-place branch can't honour the byte-for-byte-unchanged reject (you can't delete the branch
     you're on, and `generate`'s scaffold writes uncommitted files that would pollute the live engine
     repo). So `git -C @FAMILY_REPO@ worktree add -b proposal/t3-<change>-<n> <ewt> main`, then make
     **all** registry edits land on `<ewt>`: hand-edit `<ewt>/FAMILY.md`; for an **add**, run
     `generate <stem> --no-install --family <ewt>/FAMILY.md --config-dir <ewt>/config --wiring-dir
     <ewt>/wiring --vault <vault-wt>` (custom dirs require `--no-install`, which T3 uses anyway — it
     writes `config/<stem>`+`wiring/<stem>` into `<ewt>` and the skeletal INDEX into the vault
     worktree); for a **retire/merge**, `git -C <ewt> rm config/<stem>` (+ `wiring/<stem>`). Then
     `git -C <ewt> add -A && git -C <ewt> commit` with **plain `git`**, carrying the **same `Heal-run`
     id** (and `Heal-mode`/`Heal-verdict`) in the message's trailer block — git trailers are plain
     message lines, no engine needed — so `git log` across **both** repos reconnects the two sides of
     one family change. Reject = `worktree remove --force <ewt>` + `branch -D` (engine repo truly
     byte-for-byte unchanged, like the vault side).
   - **Pre-surface coupling check** (the vault side is restartable by skip-by-log; the registry side
     is plain `git` and re-runnable, but the *two-branch* pairing is not mechanically enforced). Before
     surfacing, assert **both** `proposal/t3-<change>-<n>` branches exist — one in `@VAULT@`, one in
     `@FAMILY_REPO@` — and carry the **same `Heal-run`**. If only one exists, the run was interrupted:
     rebuild the missing side (re-run the registry edit, or re-apply the vault op sequence) before
     going on. **Never surface a single-sided proposal** for ratification — half the change reviewed as
     if whole is exactly the half-ratify failure in disguise.
   - **Surface both diffs** as the single ratifiable artifact:
     `git -C @VAULT@ diff main..proposal/t3-<change>-<n>` **and**
     `git -C @FAMILY_REPO@ diff main..proposal/t3-<change>-<n>`, plus the admission-test verdict and
     the drafted bilateral reconciliation. **Merge both = ratify; remove both worktrees + delete both
     branches = reject** (both repos left byte-for-byte unchanged).
8. **Consistency check after ratify** (the cross-repo invariant the half-merge risk demands). **First,
   op-agnostically, confirm BOTH sides actually merged** — each repo's `main` now contains its
   `proposal/t3-<change>-<n>` (e.g. `git -C <repo> branch --contains <tip>` shows `main`, or the
   surfaced `main..` diff is now empty) for **both** `@VAULT@` and `@FAMILY_REPO@`. This is the
   backstop that catches *every* half-merge regardless of op — including a **boundary-move**, whose
   registry side is pure Scope/Boundary prose with no row-status or `config/` change for the per-op
   checks below to anchor on; merging the vault entries but forgetting the registry prose would
   otherwise pass silently. **Then** the content consistency, scoped to **this proposal's delta and the
   registry's Status**, not a whole-registry bijection (the registry deliberately carries non-built
   rows — *planned*, *Excluded*, *Watch* — that by design have **no** vault folder or `config/`; exempt
   them):
   - a row this proposal **added or promoted to *built*** ⇒ a non-empty `<stem>/` folder (≥1
     `knowledge/` entry) **and** a `config/<stem>` now exist;
   - a sibling this proposal **retired / merged away** ⇒ its `config/<stem>` is gone and its row is
     *Excluded*/dropped; its `<stem>/` folder is the **empty skeleton** the engine leaves (zero
     `knowledge/` entries) — that residue is the expected end state, **not** a half-merge;
   - **untouched *built* rows** ⇒ unchanged (still a non-empty folder + config);
   - a **boundary-move** changes no row's built/retired status — verify only that both siblings' rows
     and folders still exist and the moved entries landed on the receiving side.
   A mismatch *within this delta* (a newly-built row with no folder, a retired sibling whose config or
   row survived, a moved entry that didn't land) means only one side merged — finish or revert the
   other; never leave the registry and the vault disagreeing. (This assumes the registry's Status
   column is current; reconcile stale Status before relying on the check — a live dogfood target.)

The new sibling's **skill adapter** (its rendered Claude/Codex `SKILL.md`) is **not** T3's to write:
adapters are rendered from `@FAMILY@` + `config/` by the installer on its next pass (that wiring is
the maintenance-skill installer pass). T3 makes the sibling *real* in the source of truth (registry +
config + vault entries); deployment to providers is the installer's job — keeping T3 provider-neutral.

## When the re-derivation finds nothing structural

If the holistic check confirms the family is already orthogonal, there is no family op — the
disruption was really a T2 (one sibling) or T1 (one entry); hand it down, or, if nothing changed at
all, write nothing and report the family sound. Never manufacture an add/merge/retire to justify the
pass.

## What stays true (and what enforces it)

T3 invents no new engine or selftest *mechanism* for the sibling-entry side — its vault ops are the
`refresh`/`capture`/`remove` composites W1 already pins, now possibly **cross-stem**;
`maintenance-selftest` pins that a two-stem composite is skip-by-log restartable and that ratify-merge
lands both stems. The **registry side is plain `git`** — file edits reviewed as a diff and merged —
so there is nothing engine-specific to pin there; its correctness (the registry edit, the registry ⇔
vault consistency, the bilateral reconciliation, the admission verdict) is **agent- and
reviewer-enforced and human-ratified**, exactly the boundary `verification.md` describes for an
LLM-in-the-loop maintainer. The engine stays vocabulary-free: "did you re-derive the whole family?
does the registry match the vault?" is the agent's and the reviewer's check, not a mechanical gate.
Every vault op is one revertible engine commit; every registry op is one revertible git commit; the
two are linked by a shared `Heal-run`; knowledge and siblings leave the family only by a ratified,
adjudicated change across both repos.
