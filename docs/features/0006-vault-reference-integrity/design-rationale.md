# 0006-vault-reference-integrity — Design Rationale

## D-2: scan-skill-sources-for-baked-refs

**Forces.** The check must (a) cover exactly the framework-deployed consumer surfaces (`Spec#C-1`), (b) stay complete as that set grows without a hand-maintained list, (c) be read-only and repo-local so it can run in CI and after any vault edit, and (d) match the actual reference format the framework produces — `@VAULT@/<topic>/knowledge/<slug>.md` pre-bake, its absolute equivalent post-bake.

**Alternatives considered.**

- *Scan deployed skills* (`~/.claude/skills`, `~/.agents/skills`) for the baked absolute path. Rejected as the primary mechanism: it validates only one machine's installed state, depends on `install` having run, and can't run from the tooling repo in CI. Because `install` renders deployed skills byte-identical to their sources (orphan-pruned, fails on any unbaked token), source integrity already implies deployed integrity — so scanning sources is the stronger, earlier check. A deployed-state wrapper could be added later; it is not needed for Core.
- *Declared consumer registry* (a manifest listing each consumer and its referenced slugs). Rejected: a hand-maintained list is exactly the silently-drifting artifact this feature exists to eliminate — a new consumer or a moved reference needs a manual registry edit, and a forgotten edit is a silent coverage gap. Filesystem discovery over `skills/` is self-maintaining, mirroring the existing dynamic-discovery model of `practice_skills()` / `siblings()` (`install:296-319`).
- *Scan the whole tooling repo* for the pattern. Rejected: it would flag references in non-deployed surfaces (docs, READMEs), exceeding `Spec#C-1`'s "framework-deployed surfaces" scope and producing findings the contract does not own.

**Chosen path.** Scan `skills/` sources for `@VAULT@/<topic>/knowledge/<slug>.md`, resolve `@VAULT@` via the shared precedence, assert each target exists. Repo-local, CI-able, complete-by-construction over the deployed-skill source trees, and matched to the real reference format.

**Scope edge (logged, not silent).** KB-sibling adapters are rendered from `wiring/`+`templates/`+`config/`, not stored under `skills/`, and today carry only generic vault references (topic `INDEX`, "load matching entries"), never a hardcoded specific entry. They are therefore outside the scan. The check's summary names the roots it scanned so the edge is visible.

**Invalidation triggers.** Extend the scan beyond `skills/` if either becomes true: (1) a KB-adapter wiring/template ever bakes a specific `knowledge/<slug>.md` reference; (2) a new framework-deployed surface carrying specific-entry references is introduced outside `skills/`. Either would otherwise turn the logged edge into a silent gap.
