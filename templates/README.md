# templates/

The family's structural pattern as **single-sourced, config-parameterized templates** — the one canonical source of structural truth, consumed by both the engine (mutation) and any sibling-creation flow (the generator, feature `0005`):

- the **adapter body** — one shared `SKILL.md` body emitted identically to both Claude and Codex (replaces chezmoi `.chezmoitemplates`);
- the empty **`INDEX` skeleton**;
- the per-sibling **config schema**;
- the **entry** and **README** shapes.

A sibling is `{ template + config + description }`, never a hand-encoded copy — this is what lets the generator instantiate a sibling without re-encoding the pattern, and what stops the two providers' adapters from ever diverging.

DESIGN Decision-8 (single-sourced-pattern-templates), Decision-2 (provider-neutral-install-via-shared-skill). Populated by feature `0004`: the per-sibling config schema (`sibling-config.schema.md`) in E1; the adapter-body / INDEX skeleton / entry+README shapes in D1. Consumed by the engine + the generator (`0005`).
