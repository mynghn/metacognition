# Practice skills

Authored, in-action skills the framework ships into every agent runtime (`handoff`, `compact-focus`, …) — distinct from the generated knowledge-base siblings (`config/` + `templates/`) and the family-level `metacognition-maintenance` skill. Each lives in `skills/practice/<name>/` and is deployed by the practice-skill lane in `install` (`deploy_practice_skill` → `practice_sources`).

## The vendor-divergence test

A skill should be the **same** prose for every runtime. Divergence is debt — two SKILL.md files to keep in sync — so a skill earns a per-vendor split only by passing this test, in order:

1. **Shared by default.** Author one `<name>/SKILL.md`; it deploys byte-identical to both providers. This is the right answer for almost every skill, because most of what a skill says is runtime-independent discipline.
2. **Split only on a runtime-forced primitive.** Diverge **only** where a body names a mechanism one runtime has and the other lacks — and would otherwise hand that runtime an instruction that does not work. The concrete forcing functions today:
   - Claude Code's `/compact <focus>` takes a focus argument; Codex's `/compact` does not (the Codex pattern is a pre-compaction *message*, then plain `/compact`).
   - `$ARGUMENTS` is a Claude-Code substitution; Codex has no equivalent.
   - Frontmatter conventions differ: Claude reads `argument-hint`; Codex reads `compatibility` + `metadata.short-description`.
   - The `@`-mention file affordance is a Claude-Code convention; on Codex `@` triggers an input-picker, so a brief is referenced by **plain path**.
   A *preference* ("this reads better on Codex") is not a forcing primitive. If the same words work on both, they must be shared.
3. **Minimize the split.** Even in a per-vendor skill, only the forced lines differ. Keep every shared bullet, rule, and example byte-identical across the two bodies; let the divergence be exactly the runtime-specific delivery and nothing more.
4. **A large delta is a smell.** If two bodies diverge well beyond their forcing primitives, that is the signal to reconcile — pull the shared majority back together — not to accept the drift. If a *set* of skills starts carrying the same conditional split, that is the signal to graduate to templating/composition; until then, authored duplication is the cheaper trade for a small curated set.

## Layout

```
skills/practice/<name>/
  SKILL.md              # SHARED skill: one body, byte-identical to both providers   (the default)
  — or —
  claude/SKILL.md       # PER-VENDOR skill: one body per runtime                      (the exception)
  codex/SKILL.md
  agents.md             # the single, provider-neutral <tag>…</tag> activation block  (always shared)
  vendor-divergence     # per-vendor skills only: the golden divergence snapshot (gate; see below)
```

A shared `SKILL.md` **and** a per-vendor `<provider>/` dir together is an authoring ambiguity, not a merge — `install` rejects it. The activation block is always one shared, provider-neutral span (the file both runtimes read is shared, so it names no single-runtime-only invocation as the only path).

`@VAULT@` is the only token a body carries; `install` bakes it to the adopter's vault and fails fast on any other unbaked `@TOKEN@`.

## The divergence gate

`install-selftest` enforces the *minimize* and *large-delta-is-a-smell* steps mechanically, so they cannot quietly erode:

- **Golden snapshot.** Each per-vendor skill ships `vendor-divergence` — a *content-not-position* record (the sorted set of non-blank lines unique to each provider's SKILL.md, frontmatter + body; reordering a shared line is invisible, but any added or removed provider-unique line registers). The gate asserts the live divergence equals the snapshot, so drift in **either** direction fails: gratuitous new divergence, and a reconcile-toward-shared, both stop the build until the change is acknowledged. Regenerate intentionally after a real divergence change with `./install-selftest --update-divergence`.
- **Semantic check.** No Claude-only primitive (`$ARGUMENTS`, a `/compact <focus>` argument form) may appear in a Codex body — a direct guard on the C-3 "deployed skill matches its runtime" constraint.

The snapshot is the review surface: read it to see, at a glance, exactly how two SKILL.md files differ and judge whether every line of that difference is genuinely runtime-forced.
