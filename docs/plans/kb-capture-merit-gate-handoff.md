# Handoff — Merit-gated KB capture (Metacognition)

**Goal**: Give the vault a **soft merit gate** for new entries, so a capture must clear orthogonality / source-authority / distillation checks *before* the engine writes it — not just the engine's form-gate. Run as a LeanPlan round on `mynghn/metacognition`. English-native.

## Carry — the failure, observed live

The entry `concise-not-compressed` joined the vault on the **form-gate alone** (valid frontmatter, non-empty `sources`, `last_refreshed`, unique slug → `kb-engine capture` → commit). On merit it should not have, un-reviewed:

- **Not orthogonal.** It overlaps `literal-vs-latent-matching` heavily — the latent-recovery mechanism *is* that node. It belonged as a refresh/extension, not a new concept.
- **Lacked authority for its headline.** It cited only NoLiMa, which backs the *sub-claim* (long-context degradation) — not the headline "cut redundancy, never drop an orthogonal axis," which was synthesized in conversation. The citation lent false authority to an unsourced claim.
- **Weak approval.** A bundled "yes" + the standing "capture durable lessons" directive; no merit check by author or engine.

The engine is form-only **by design** (it is the sole writer and validates structure, not merit). The gap is a merit checkpoint *in front of* it.

## The soft gate — what it should adjudicate

- **Orthogonality** — overlap vs existing nodes → new entry / refresh-existing / reject. (Run against the INDEX.)
- **Source authority, per claim** — each major claim maps to an authoritative source, **or is explicitly marked synthesized**. Forbid a citation that covers only a supporting point from standing in for the headline. (The sharpest lesson here.)
- **Distillation** — distilled and self-contained, not a transcript.
- **Durability** — reusable beyond the originating session, not session-local.
- **Home & slug** — right family; no near-duplicate slug.

## Constraints (load-bearing)

- **Soft, not hard.** Merit / orthogonality / authority are judgment, not deterministically checkable — the gate *guides* the check and records the verdict; it does not mechanically block. (Mirrors the `concise-not-compressed` feature's own advisory-not-enforced decision.)
- **Engine stays the sole writer.** The skill is a *pre-engine* checkpoint; accepted entries still go through `kb-engine capture/refresh` (one commit). Do not bypass or reimplement the engine.
- **Don't duplicate siblings.** `metacognition-maintenance` heals/evolves *existing* entries; `metacognition-freshness` checks staleness. This is the **capture front door** — position it among them, and consider whether the existing KB skills' "Capture" sections should route through it rather than call the engine directly.
- **Provider-neutral + dual-adapter** (Claude + Codex), per the install/generate model.
- **Self-applying** — validate the gate *would have caught* `concise-not-compressed`.

## First moves

- Read `ARCHITECTURE.md`, `FAMILY.md`, the engine's capture path, the `context-/prompt-engineering-knowledge-base` skills' **Capture** sections, and the `metacognition-maintenance` skill.
- Decide the shape (don't pre-commit): a new dedicated capture skill vs. enhancing each KB skill's Capture section vs. an engine pre-capture hook.
- Allocate the round; `/requirements` framing the Problem as **merit-gate vs form-gate**, with the live failure as the worked instance.

## Refs

- Framework = install (same clone): `~/.local/share/metacognition/` — remote `https://github.com/mynghn/metacognition.git`.
- Vault: `~/.local/share/metacognition-vault/` — remote `https://github.com/mynghn/metacognition-vault.git`.
- **The gate's first test case:** entry `concise-not-compressed` (vault commit `a0de939`, currently **local-only/unpushed**, also on local branch `kb/concise-not-compressed`) — reconcile into `literal-vs-latent-matching` or re-source; do not push as-is.
- Sibling handoff (related, parked): `docs/plans/kb-skill-activation-handoff.md` (KB-consultation *activation*; this one is KB-entry *admission*).

## Drop

- The `concise-not-compressed` LeanPlan feature content — only the capture-gate meta-lesson travels.
