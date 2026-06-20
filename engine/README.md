# engine/

The **shared operations engine** — one implementation backing every sibling's `capture` / `refresh` / `remove` / `locate`, parameterized by the thin per-sibling [`config/`](../config). Replaces today's per-sibling near-duplicate `*-kb` scripts (which differ only in four tokens).

Operation semantics are preserved exactly: frontmatter validation (`name` == slug, non-empty `description`, `last_refreshed`, `sources`), `INDEX` upsert sorted by slug, `capture` refuses an existing slug / `refresh` refuses an absent one. The engine validates + mutates a vault folder and records each change as **exactly one commit to the vault repo's own history** (never the dotfiles repo), resolving the vault location from `$<PREFIX>_KB_VAULT` / `$KB_VAULT` / installer config / a default. A non-git or nested-inside-another-repo vault is refused, and a failed commit rolls the working tree back — mutation is one atomic, single-channel step.

DESIGN Decision-3 (shared-operations-engine), Decision-4 (mutation-commits-to-vault-repo). Built by feature `0004`, tasks E1 → E2.
