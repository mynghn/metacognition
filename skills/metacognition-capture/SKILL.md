---
name: metacognition-capture
description: Merit-gate a durable lesson before it enters the Metacognition knowledge vault — assess a capture candidate across five dimensions (orthogonality against the index, per-claim source authority, distillation, durability, home/slug fit), surface a recorded verdict, and route the maintainer's register / refresh / reject / accept-with-concerns decision to the unchanged kb-engine. Use when capturing, registering, or refreshing a distilled lesson into the vault, or when a KB sibling's Capture/Refresh section routes a lesson here. The maintainer is the sole admission decision — the gate records a verdict but never auto-blocks. Drives kb-engine as the sole writer (never edits vault files directly) and runs only on explicit request, never on a schedule.
---

# Metacognition vault capture gate

The family's **admission front door**: a soft merit gate that runs *before* any capture or
refresh write, beside `metacognition-maintenance` (curation of already-admitted entries) and
`metacognition-freshness` (install currency). Where maintenance heals what is already in, this
gate decides — by maintainer judgment — *whether and how* a new lesson gets in.

This skill is **provider-neutral**: it drives only the `kb-engine` CLI and `git`, and the merit
assessment is prose judgment, not code. It ships byte-identical to every provider, and it adds
nothing to the engine — an accepted candidate flows through the unchanged engine, which stays the
sole writer.

It assumes the installer has resolved these absolute paths:

- `@ENGINE_BIN@` — the `kb-engine` writer; a target in topic `<stem>` uses `--config @CONFIG_DIR@/<stem>`
- `@CONFIG_DIR@` — per-topic engine configs · `@VAULT@` — vault repo root · `@SOURCES@` — authority policy

## Two laws (never violated)

1. **The engine is the sole writer of vault entries.** Read the vault freely to decide *what* to
   admit, but **never hand-edit an entry or its INDEX** and never reimplement or bypass the engine.
   Every accepted candidate reaches the vault as one `kb-engine capture|refresh` commit — validated,
   source-gated, and recorded as one recoverable commit — and the engine's own form-gate and
   host-allowlist gate still run underneath this one.
2. **The maintainer is the gate.** This gate is *soft*: it **records** a merit verdict but never
   mechanically rejects or hard-blocks a candidate. The maintainer's approval is the sole admission
   decision; a candidate the maintainer accepts despite recorded concerns still proceeds (written
   through the engine's `degraded:` marker). This is the deliberate contrast with maintenance's
   adversarial auto-reject — admission is a human call, healing is not.

## When this runs

Only on explicit demand — a maintainer captures/refreshes a lesson, or a KB sibling's
Capture/Refresh section routes one here. **Nothing here runs on a schedule.** The gate sits on the
admission path: no create or update reaches the engine without a preceding assessment.

## Resolve the target topic

The gate is topic-parameterized like the engine — it cannot be topic-agnostic, because
orthogonality is checked against the target topic's index and the engine call needs that topic's
config:

- **Routed from a KB sibling** → inherit that sibling's stem.
- **Invoked standalone** → ask the maintainer to name the target topic before assessing.

The resolved `<stem>` selects the engine config `@CONFIG_DIR@/<stem>` and the orthogonality
reference `@VAULT@/<stem>/INDEX.md`.

## A capture run

1. **Resolve the target topic** (above) — you need its `<stem>` for both the orthogonality read and
   the engine call.
2. **Assess merit across all five dimensions** — orthogonality, per-claim source authority,
   distillation, durability, home/slug fit — **before any engine call**. No vault write has happened
   at this point. See **`references/assessment.md`**. The assessment yields a recommended verdict:
   an orthogonality classification (new / refresh-of-named-entry / reject) plus any authority flags
   and merit concerns.
3. **Surface the assessment and the recommended verdict to the maintainer** — the full five-dimension
   read, not just a verdict label, so the decision is informed.
4. **The maintainer decides** — register a new entry, refresh a named existing entry, reject, or
   accept-with-concerns. The gate records this verdict; it never auto-rejects and never overrules the
   maintainer.
5. **Route the decision to the engine** — accept → one `kb-engine capture|refresh` call carrying the
   verdict as a trailer (accept-with-concerns adds the `degraded:` marker); reject → no engine call,
   vault unchanged. See **`references/engine-write.md`** — **read before any write.**

## References (load on demand)

- **`references/assessment.md`** — the five-dimension merit assessment: the orthogonality
  classification, the per-claim authority mapping that layers *above* the engine's deterministic
  host-check, distillation, durability, and home/slug fit. Read before assessing a candidate.
- **`references/engine-write.md`** — the write spine: how each maintainer decision routes to exactly
  one engine operation, the verdict trailer schema, the `degraded:` accept-with-concerns path, and
  the stdin entry format. **Read before any write.**
