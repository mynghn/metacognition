# 0002-ship-practice-skills — Spec

## Behavior

### B-1: practice-skills-deployed-on-install
When the installer runs, every practice skill the framework ships is deployed into each supported agent runtime's skill location (currently Claude Code and Codex), alongside the knowledge siblings — present where that runtime discovers skills, with no manual file placement by the adopter. The set of deployed skills is keyed on the framework's shipped practice-skill set, so a later-added practice skill deploys the same way without bespoke per-skill steps.

### B-2: activation-emitted-on-install
When the installer runs, each shipped practice skill's activation entry is emitted into the shared agent-instruction surface both runtimes read — the same surface the knowledge siblings' activation already uses — present and well-formed, registering the skill to surface at its moment. The spec asserts the activation entry is in place after install; whether and how often the skill then fires is out of scope (see Non-goals).

### B-3: deployed-skill-resolves-to-adopter-vault
When the installer runs against an adopter's configured vault location, each deployed practice skill operates against that location rather than any author-specific one. Installing with a different vault location yields skills bound to that location.

## Constraint

### C-1: install-owns-only-its-regions
Install creates and updates only the framework-owned regions — the deployed practice skills and their activation entries, alongside the siblings' — and leaves everything else in the shared instruction surface unchanged, most pointedly the adopter's own operating-frame content (everything outside the framework's regions). Re-running install replaces those regions in place without duplication and never rewrites or disturbs anything outside them; an adopter's personal content survives any number of installs byte-for-byte.

### C-2: shipped-skills-carry-no-author-personal-content
No practice skill the framework ships imposes author-personal content on an adopter. Every personal-specific value — the vault location, any personal filesystem path, personal phrasing — is resolved at install time to the adopter's configuration, so no adopter ever inherits an author-specific path or wording in a deployed skill.

### C-3: deployed-skill-matches-its-runtime
No shipped skill instructs a primitive or convention its target runtime lacks. A skill deployed to a given runtime uses only that runtime's mechanisms — e.g. the Codex copy never emits Claude Code's `/compact <focus>` argument form or its `$ARGUMENTS` substitution — and the shared activation surface, read by both runtimes, names no single-runtime-only invocation as the only path. Realizing the same skill across runtimes may require per-runtime content, not one byte-identical artifact.

## Non-goals
- **Firing behavior and measured lift.** The spec covers that each practice skill's activation is shipped and in place; it does not specify whether, when, or how often a skill actually fires at its moment, nor any lift over a baseline — that behavior is owned by the self-initiated-skill-activation feature (0001).
- **The skills' own internal contract.** What `/handoff` and `/compact-focus` each produce when invoked is their pre-existing behavior; this spec covers deploying, activating, and generalizing them, not redefining what they do.
- **The correct Codex skills-home path.** B-1 deploys to each runtime's skill location via the installer's existing path. Current Codex docs put the official user-skills home at `~/.agents/skills/` rather than the `~/.codex/skills/` the installer uses for every skill today; migrating it is framework-wide (it also fixes sibling and maintenance discovery) and is deferred to its own issue.
