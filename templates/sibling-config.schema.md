# Per-sibling config — schema

The thin config the family is parameterized by (DESIGN Decision-3). One file per sibling under [`config/`](../config), consumed by the shared [`engine/`](../engine) and the installer. A sibling's whole surface is `{ template + config + description }` (Decision-8) — this is the `config` half.

Flat `key = value`, one per line; `#` starts a comment. Deliberately not a templating language — the observed variation across siblings is exactly this fixed field set, nothing more.

| Field | Required by | Meaning | Example |
|---|---|---|---|
| `stem` | engine | the topic's vault folder name (`<vault>/<stem>/`) and the sibling's identity | `context-engineering` |
| `index_heading` | engine | the `## <heading>` section in the topic's `INDEX.md` that entries are upserted under | `Concepts` |
| `env_prefix` | E2 (location override) | prefix for the env var that overrides the vault location (e.g. `<PREFIX>_KB_VAULT`) | `CE` |
| `tier` | D2 (discovery wiring) | `everyday` \| `common` \| `situational` — gates the tier-gated `AGENTS.md` block (Decision-5) | `everyday` |

The engine (task E1) reads `stem` + `index_heading`; `env_prefix` and `tier` are reserved for E2 and D2 and ignored by the engine today.

## Example

```
# config/context-engineering
stem = context-engineering
index_heading = Concepts
env_prefix = CE
tier = everyday
```

The three shipped siblings' instances are authored in task M2; new siblings are instantiated from this schema by the generator (feature 0005).
