---
name: metacognition-freshness
description: Check and (after confirmation) update the freshness and validity of the Metacognition framework — the tooling repo and the private vault repo (vs their remotes), plus whether installed Claude+Codex adapters cover every configured sibling. Use after a Metacognition main-branch update, when siblings/entries may be stale, or to confirm the framework is current. Metacognition is install-bootstrapped, NOT a chezmoi external — update via git pull + re-run install, not chezmoi. For the chezmoi-managed dotfiles surface use chezmoi-freshness instead.
argument-hint: "[check | update]"
---

The **Metacognition surface** of this machine's agent toolchain: the `metacognition` tooling repo +
the private `metacognition-vault` repo, and the installed Claude+Codex KB adapters. Mechanism is
imperative: `git pull` + re-run `install`. It is **not** a chezmoi external, so `chezmoi update`
will never touch it. The chezmoi-managed dotfiles surface is owned by `chezmoi-freshness`.

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

## Gotchas

- **mynghn credential.** Both repos are mynghn-owned and the vault is private; the active gh account
  may not be able to reach it. The check fetches with a mynghn credential automatically when
  available. To pull/push manually:
  ```sh
  export MYNGHN_TOKEN=$(gh auth token --user mynghn)
  git -C <repo> -c credential.helper= \
    -c credential.helper='!f(){ echo username=mynghn; echo "password=$MYNGHN_TOKEN"; };f' pull --ff-only
  unset MYNGHN_TOKEN
  ```
- **Not a chezmoi external.** `chezmoi update` will not update it; use `git pull` + re-run `install`
  so both providers' adapters are re-rendered from `templates + config + wiring`.
- **Re-run `install` after pulling.** New/renamed siblings only become live adapters when `install`
  runs; the adapter-parity check catches a skipped install.
- **Vault writes go through the engine and commit as `mynghn`.** Never hand-edit the vault; never
  commit it under another identity.
- Sibling skill: **chezmoi-freshness** owns the dotfiles + chezmoi-external surface.
