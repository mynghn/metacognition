# templates/

The family's structural pattern as **single-sourced, config-parameterized templates** — the one canonical source of structural truth, consumed by both the engine (mutation) and any sibling-creation flow (a future generator):

- the **adapter body** — one shared `SKILL.md` body emitted identically to both Claude and Codex (replaces chezmoi `.chezmoitemplates`);
- the empty **`INDEX` skeleton**;
- the per-sibling **config schema**;
- the **entry** and **README** shapes.

A sibling is `{ template + config + description }`, never a hand-encoded copy — this is what lets the generator instantiate a sibling without re-encoding the pattern, and what stops the two providers' adapters from ever diverging.

Single-sourced pattern templates are what keep the install provider-neutral and let a sibling be a `{ template + config + description }` instance. The directory holds the per-sibling config schema (`sibling-config.schema.md`), the single adapter-body template (`skill-body.md`), and the empty `INDEX` skeleton (`index-skeleton.md`, rendered by the generator into a new topic's `INDEX.md`); the entry/README shapes follow. Consumed by the installer, the engine, and the generator.

`index-skeleton.md` tokens: `@TITLE@` (title-cased stem + " Knowledge Base"), `@TOPIC@` (stem), `@NOUN_PLURAL@` (lowercased `index_heading`), `@NOUN@` (singular, `noun_of(index_heading)`), `@INDEX_HEADING@` (the `## ` section the engine upserts under), `@SEEDS_LIST@` (the generated `## Seeds` bullet list). The `## Seeds` section sits BEFORE `## @INDEX_HEADING@` so the engine's INDEX upsert (which reshapes only the lines after the heading) preserves it; it is transient scaffolding the content build consumes and clears.
