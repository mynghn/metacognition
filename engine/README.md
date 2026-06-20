# engine/

The **shared operations engine** — one implementation backing every sibling's `capture` / `refresh` / `remove` / `locate`, parameterized by the thin per-sibling [`config/`](../config). Replaces today's per-sibling near-duplicate `*-kb` scripts (which differ only in four tokens).

Operation semantics are preserved exactly: frontmatter validation (`name` == slug, non-empty `description`, `last_refreshed`, `sources`), `INDEX` upsert sorted by slug, `capture` refuses an existing slug / `refresh` refuses an absent one. As of **E1** the engine validates + mutates a supplied vault folder; recording each change as one commit to the **vault repo's** own history (and resolving the vault location) lands in **E2**.

DESIGN Decision-3 (shared-operations-engine), Decision-4 (mutation-commits-to-vault-repo). Built by feature `0004`, tasks E1 → E2.
