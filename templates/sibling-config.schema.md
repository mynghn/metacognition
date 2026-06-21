# Per-sibling config — schema

The thin config the family is parameterized by. One file per sibling under [`config/`](../config), consumed by the shared [`engine/`](../engine) and the installer. A sibling's whole surface is `{ template + config + description }` — this is the `config` half.

Flat `key = value`, one per line; `#` starts a comment. Deliberately not a templating language — the observed variation across siblings is exactly this fixed field set, nothing more.

| Field | Required by | Meaning | Example |
|---|---|---|---|
| `stem` | engine | the topic's vault folder name (`<vault>/<stem>/`) and the sibling's identity | `context-engineering` |
| `index_heading` | engine | the `## <heading>` section in the topic's `INDEX.md` that entries are upserted under | `Concepts` |
| `env_prefix` | engine (location override) | prefix for the per-sibling env var that overrides the vault location: `<PREFIX>_KB_VAULT` | `CE` |
| `tier` | installer (discovery wiring) | `everyday` \| `common` \| `situational` — gates the tier-gated `AGENTS.md` block | `everyday` |
| `volatility` | health-check (age signal) | the topic's freshness threshold in **days**: `health-check` flags an entry older than this as `[over-age]`. Per-topic, because fast-moving topics decay faster than foundational ones. Optional — a sibling that omits it uses the health-check default | `180` |

The engine reads `stem`, `index_heading`, and `env_prefix` (vault-location override, checked before the family-level `$KB_VAULT`); `tier` is consumed by the installer (it gates the `AGENTS.md` trigger block, emitted only for `everyday`) and ignored by the engine. `volatility` is read only by `health-check` (the deterministic decay detector), ignored by the engine and installer.

## Example

```
# config/context-engineering
stem = context-engineering
index_heading = Concepts
env_prefix = CE
tier = everyday
volatility = 180
```

New siblings are instantiated from this schema by a future generator.
