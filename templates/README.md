# templates/

The family's structural pattern as **single-sourced, config-parameterized templates** — the one canonical source of structural truth, consumed by both the engine (mutation) and any sibling-creation flow (a future generator):

- the **adapter body** — one shared `SKILL.md` body emitted identically to both Claude and Codex (replaces chezmoi `.chezmoitemplates`);
- the empty **`INDEX` skeleton**;
- the per-sibling **config schema**;
- the **entry** and **README** shapes.

A sibling is `{ template + config + description }`, never a hand-encoded copy — this is what lets the generator instantiate a sibling without re-encoding the pattern, and what stops the two providers' adapters from ever diverging.

Single-sourced pattern templates are what keep the install provider-neutral and let a sibling be a `{ template + config + description }` instance. The directory holds the per-sibling config schema (`sibling-config.schema.md`) and the single adapter-body template (`skill-body.md`); the INDEX skeleton + entry/README shapes follow. Consumed by the installer, the engine, and a future generator.
