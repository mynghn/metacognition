# 0005-kb-capture-merit-gate — Design Rationale

## D-1: dedicated-capture-front-door-skill

Forces: the handoff offered three shapes — a dedicated capture skill, inlining the merit checklist into each KB skill's Capture section, or an engine pre-capture hook — and asked not to pre-commit. The assessment is substantial (five dimensions, a per-claim authority mapping, a worked instance) and is LLM judgment, not code. The family already has a precedent for an operational, engine-driving, multi-file skill: `metacognition-maintenance`.

Alternatives considered:
- **Engine pre-capture hook** — rejected. `kb-engine`'s `write_entry()` is a single linear, deterministic, stdlib-only, provider-neutral function with no hook point; its source-authority gate (deterministic host allowlist) is the ceiling of in-engine merit. Embedding LLM judgment there makes the engine non-deterministic / provider-coupled, or shrinks the gate to a mechanical check — and violates the standing "engine stays form-only; don't reimplement it" constraint (`Spec#C-2-writes-only-through-the-engine`).
- **Inline the checklist into the shared KB body** (`templates/skill-body.md`) — rejected as the home, though the body is still lightly edited (D-3). One source, every sibling covered automatically — but the full assessment prose then loads on every sibling activation (attention-diluting bloat across all seven adapters), the gate's evolution couples to the KB body template, and there is no clean "front door" to position beside maintenance/freshness. KB siblings render from a single shared body with no per-skill `references/`, so progressive disclosure of a large procedure has no home there.
- **Dedicated `metacognition-capture` skill** — chosen. Mirrors `metacognition-maintenance` exactly: hand-authored `SKILL.md` + `references/`, its own `deploy_capture` installer lane, byte-identical to both providers, engine-driven. The substantial procedure lives in one place with progressive disclosure (references), the family gains a clean admission front door (admit-new) beside maintenance (curate-admitted) and freshness (install-currency), and it matches the maintainer's stated intent ("let the user register any entry with a provided skill"). Cost accepted: a new skill plus an installer lane to author and keep parity-checked across both providers.

Invalidation: if the KB lane later grows per-sibling `references/` support, the bloat objection to the inline option weakens — but the front-door positioning and single-home-for-the-procedure arguments stand independently.

## D-2: gate-runs-as-instructions-engine-unchanged

Forces: the gate must run *before* the engine write yet must not become a second writer or a bypassable side door, and it must ship identically to Claude and Codex. The seam between "decide to capture" and "engine writes" is a single direct CLI call (`@ENGINE@ capture|refresh <slug>` with the entry on stdin) baked into the skill body — there is no wrapper today.

Alternatives considered:
- **A thin read-only helper script** (e.g. an orthogonality differ that prints candidate-vs-INDEX overlap) — rejected as a component. Merit is judgment, not code, so a helper could only re-check form/host (duplicating the engine) or compute a weak lexical overlap that the LLM reading the INDEX does better. A helper that also shells the engine risks becoming a second front door future callers could skip, weakening the single-seam invariant; and any executable would need provider-neutral install parity like the engine. The INDEX is small and JIT-readable, so the orthogonality comparison is better done as instruction-driven judgment over the read INDEX.
- **Pure provider-neutral instructions, engine unchanged** — chosen. The assessment is prose the agent executes; accepted entries flow through the existing, unmodified engine CLI (one commit, sole writer preserved). Nothing executable is added, so there is no determinism/parity burden beyond the skill body itself, which the existing installer pipeline already renders identically to both providers.

Invalidation: if orthogonality recall proves unreliable as pure judgment at vault scale (many entries, subtle overlaps), revisit a *read-only advisory* differ that feeds — never gates — the judgment, keeping admission a maintainer decision.

## D-4: verdict-recorded-as-engine-git-trailer

Forces: `Spec#C-3-gate-records-but-never-blocks` and the success signal require every admitted entry to carry a maintainer-reviewed verdict, durably. The engine already accepts `--trailer KEY:VALUE` (repeatable) and records it on the single vault commit — the exact mechanism `metacognition-maintenance` uses for `Heal-*` provenance.

Alternatives considered:
- **In the entry body / frontmatter** — rejected. Pollutes the knowledge content with process metadata, would have to pass the engine's frontmatter validation, and drifts on later refreshes.
- **A separate gate log file** — rejected. A second write outside the engine reintroduces a non-engine writer and a file that can desync from vault history.
- **Git trailer via the engine `--trailer` flag** — chosen. The verdict lands in the same commit as the entry, queryable from vault history (`git log --grep`), with zero new storage and zero new writer — consistent with the engine-as-sole-writer invariant and symmetric with maintenance's provenance trailers.

Invalidation: if a verdict needs to be richer than a trailer line comfortably holds (e.g. full per-claim tables), revisit — but the durable *record-of-decision* belongs on the commit regardless; a verbose assessment can stay ephemeral in the review surface.
