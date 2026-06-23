---
name: metacognition-freshness
description: Check and (after confirmation) update the freshness and validity of the Metacognition framework — the tooling repo and vault repo (vs their remotes), plus whether installed Claude+Codex adapters cover every configured sibling. Use after a Metacognition main-branch update, when siblings/entries may be stale, or to confirm the framework is current. Metacognition is install-bootstrapped; update via git pull + re-run install.
argument-hint: "[check | update]"
---

The **Metacognition surface** of an installed agent toolchain: the `metacognition` tooling repo,
the `metacognition-vault` repo, and the installed Claude+Codex KB adapters. Mechanism is
imperative: `git pull` + re-run `install`.

This installed copy has these paths baked by the Metacognition installer:

- `@FAMILY_REPO@` — Metacognition tooling repo
- `@VAULT@` — Metacognition vault repo

**Read-first, confirmed-update.** Run the check, show the verdict, then update only if it flags `**`,
and only after the user confirms.

## 1. Check (read-only)

Resolve `<SKILL_DIR>` as the directory containing this installed `SKILL.md`, then run the bundled
sweep:

```sh
<SKILL_DIR>/scripts/check.sh
```

Reports each repo's clean/dirty + **behind/ahead vs origin** (fetch-only), and **adapter parity**:
whether every `config/<stem>` has installed Claude and Codex `*-knowledge-base` adapters.
`behind=0` and adapters `ok` means fresh + valid; `**` marks an action.

## 2. Update (only if flagged, only after confirmation)

A repo behind origin, or a missing adapter (for example, `main` added a sibling but `install` was not
re-run), means pull both repos and re-render adapters:

```sh
git -C @FAMILY_REPO@ pull --ff-only
git -C @VAULT@ pull --ff-only
@FAMILY_REPO@/install --vault @VAULT@
```

Re-run the check to confirm `behind=0` and adapters `ok`.
