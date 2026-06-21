# Propose → ratify: the write spine every tier shares

This is the mechanism behind every change the maintenance skill makes — T1 heal, T2 sibling
evolution, T3 family evolution all flow through it. It is **provider-neutral**: only `git` and
the `kb-engine` CLI, no agent-specific tool. The engine is the **sole writer** — you may *read*
vault files freely to decide what to change, but you **never** hand-edit one; every write is a
`kb-engine` commit.

The paths below assume the installer has resolved:

- `@ENGINE_BIN@` — the `kb-engine` executable
- `@CONFIG_DIR@` — the per-sibling config dir; a target in topic `<stem>` uses `@CONFIG_DIR@/<stem>`
- `@VAULT@` — the vault repo root (its `main` is the live knowledge)
- `@SOURCES@` — the `SOURCES.md` authority policy

## The gate: which path a change takes

Classify the change, then route it (this realizes the auto-vs-propose split):

- **Mechanical and claim-preserving** — a dead-link swap to an equivalent live source, a
  `last_refreshed` restamp on re-verification, pure formatting. **Nothing a reader's takeaway
  depends on changes.** → **auto path.**
- **Claim-affecting or structural** — a number, claim, or conclusion would change; or entries
  are split / merged / retired / re-scoped, or the family registry changes. → **proposal path.**

When unsure, route to the proposal path — ratification is cheap, a wrong silent write is not.
**Either path runs the full verification envelope before any write** (citation re-fetch, a
no-net-loss diff, and an adversarial quorum — see `verification.md`);
auto-apply is *gated*, not unguarded. If the envelope's adversarial quorum refutes a change
routed to auto, it is **downgraded to the proposal path**, never written silently.

## Provenance on every commit

Every `capture`/`refresh`/`remove` carries the skill's `Heal-*` trailers. The engine is
vocabulary-free — this schema is the skill's, recorded as generic git trailers:

```
--trailer Heal-verdict:current|dead-link|policy-fix|stale|split|merge|retire
--trailer Heal-mode:auto|ratified          # auto path → auto; proposal path → ratified
--trailer Heal-confidence:<0..1>
--trailer Sources-before:<url>, ...
--trailer Sources-after:<url>, ...
--trailer Heal-run:<id>                     # one id per maintenance run, to group its commits
```

`git log` parses these back out (`--format=%(trailers:key=Heal-mode,valueonly)`), so every
change is auditable and individually revertible — the subject stays the bare
`<stem>: <verb> <slug>`.

## Auto path (mechanical, claim-preserving)

Commit straight to `main` after the envelope clears — no worktree:

```sh
@ENGINE_BIN@ --config @CONFIG_DIR@/<stem> --vault @VAULT@ refresh <slug> \
    --sources @SOURCES@ --trailer Heal-mode:auto --trailer Heal-verdict:dead-link [...] < reconciled.md
```

## Proposal path (claim-affecting / structural)

A non-auto change is committed to a throwaway **worktree + branch** off `main`; the maintainer
reviews the real `git diff` and **merges to ratify** (deletes to reject). Nothing reaches `main`
without that merge.

1. **Branch off main** into a fresh worktree (`<n>` disambiguates concurrent proposals on one slug):

   ```sh
   git -C @VAULT@ worktree add -b proposal/<tier>-<slug>-<n> <worktree> main
   ```

   `kb-engine --vault <worktree>` writes to the branch — the engine accepts the linked worktree
   as its vault root, so its validation, source-gate, and one-commit-per-change all apply there.

2. **Apply the tier's verb sequence** on the worktree (one commit each), via the restartable
   applier below.

3. **Surface the diff** for review — this is the ratifiable artifact:

   ```sh
   git -C @VAULT@ diff main..proposal/<tier>-<slug>-<n>
   ```

4. **Ratify = merge**, then clean up:

   ```sh
   git -C @VAULT@ merge --no-ff proposal/<tier>-<slug>-<n> -m "ratify: <summary>"
   git -C @VAULT@ worktree remove --force <worktree>
   git -C @VAULT@ branch -d proposal/<tier>-<slug>-<n>
   ```

   Use `--force` for the cleanup (the branch is already merged — nothing of value is lost): a plain
   `worktree remove` hard-fails on any stray untracked file in the worktree and orphans it. Pick a
   fresh `<worktree>` path and a unique `<n>` per run, and `git -C @VAULT@ worktree prune` before
   starting, so an orphaned worktree or branch from an interrupted prior run can't wedge the next
   proposal with a path- or branch-name collision.

5. **Reject = discard** — the vault is left **byte-for-byte unchanged**, no `main` trace:

   ```sh
   git -C @VAULT@ worktree remove --force <worktree>
   git -C @VAULT@ branch -D proposal/<tier>-<slug>-<n>
   ```

### Lighter path for a single claim-change

A *single* T1 claim-change need not spin up a worktree: present the proposed `git diff` (render
the reconciled entry and diff it against the current one), and **on the maintainer's yes**,
`refresh` on `main` directly with `Heal-mode:ratified`. Same gate, same provenance, one commit —
just no worktree for a one-commit change. Use the full worktree flow whenever the change is
multi-verb or structural.

## Restartable composite-op applier

A multi-slug op (split = `refresh <surviving>` + `capture <new>`; merge = `refresh <target>` +
`remove <absorbed>`; retire = `remove`) is an **ordered, restartable sequence** of engine commits
on the proposal branch — there is no multi-slug engine transaction. The **proposal branch is the
atomic review unit**; a partial sequence lives only on the branch and an abandoned branch drops
clean.

**Progress is the branch's own commit log, not a side file.** Before each verb, read what is
already committed and skip it — so an interrupted run re-runs only the missing verbs, and a
finished run re-runs to a no-op:

```sh
done=$(git -C @VAULT@ log --format=%s main..proposal/<tier>-<slug>-<n>)   # "<stem>: <verb> <slug>" per line
# for each (verb, slug) in the planned sequence:
#   if "<stem>: <verb> <slug>" is already in $done  → skip (this verb is committed)
#   else run: @ENGINE_BIN@ --config @CONFIG_DIR@/<stem> --vault <worktree> <verb> <slug> --sources @SOURCES@ --trailer ... < content
```

This skip-by-log is **required**, not an optimization: the engine deliberately errors on a blind
retry — `refresh` of unchanged content dies *"nothing changed — no commit"*, `capture` of an
existing slug and `remove` of an absent one both error. Treating "already committed on the
branch" as done is how the sequence stays idempotent across a restart without tripping those
errors. (On any single git failure mid-verb the engine rolls its own change back to HEAD, so the
branch only ever holds whole, recoverable verb-commits — exactly the units this log reads.)

The skip is keyed on `<verb> <slug>`, not on content — it assumes each verb's intended content is
deterministic across passes. A restart that re-plans an already-committed verb with *different*
content must start a fresh branch, not resume this one (resuming would skip the verb and keep the
first pass's content).

## What the spine guarantees (verified)

`maintenance-selftest` (repo root) pins these against the real engine — keep it green:

- a proposal commits only on its branch; `main` HEAD + tree are untouched until merge; reject
  leaves the vault byte-for-byte identical;
- each commit carries the `Heal-*` trailers and is one revertible unit;
- an interrupted composite resumes on only the missing verbs and a full re-run is a no-op;
- every change is one engine-shaped commit and the tree is clean after each op.
