# The write spine — route the decision to the unchanged engine

Read this before any write. The gate **never writes the vault itself** — it only decides whether and
how to invoke `@ENGINE_BIN@`. The engine stays the sole writer: it re-runs its own form-gate
(frontmatter validity, create-vs-update slug rule) and its host-allowlist gate, then writes the
entry, upserts the INDEX, and records exactly one commit.

## One decision → one engine operation

The maintainer's decision routes to exactly one outcome:

| Maintainer decision        | Engine operation                          | Vault effect                    |
|----------------------------|-------------------------------------------|---------------------------------|
| register a **new** entry   | `@ENGINE_BIN@ … capture <slug>`           | new entry + INDEX line          |
| **refresh** a named entry  | `@ENGINE_BIN@ … refresh <slug>`           | named entry superseded in place |
| **reject**                 | *(none)*                                  | unchanged                       |
| **accept-with-concerns**   | `capture`/`refresh` **+ `degraded:` marker** | admitted, down-ranked `⚠`    |

`capture` refuses a slug that already exists and `refresh` refuses one that does not — so the
orthogonality classification (new vs refresh-of-named-entry) and the engine verb must agree. Reject
issues no engine call at all; the vault is left exactly as it was.

## The verdict trailer

Every admitted entry carries the gate's verdict as a git trailer, so the maintainer-reviewed
admission decision lands in the vault commit alongside the entry — the same provenance mechanism
maintenance uses for its `Heal-*` trailers (the engine writes trailers verbatim and never reads
them, so this vocabulary is the gate's, not the engine's):

```
--trailer Capture-verdict:new       # accepted as a new entry
--trailer Capture-verdict:refresh   # accepted as a refresh of the named existing entry
```

`git log` parses it back out (`--format='%(trailers:key=Capture-verdict,valueonly)'`), so every
admitted entry is auditable as having passed the gate. A rejected candidate produces no commit and
therefore no trailer.

## The engine call

Compose the topic's config from the resolved `<stem>` and pipe the full entry markdown on stdin
(the engine reads the entry from stdin only — there is no file argument):

```sh
@ENGINE_BIN@ --config @CONFIG_DIR@/<stem> --vault @VAULT@ capture <slug> \
    --sources @SOURCES@ --trailer Capture-verdict:new <<'EOF'
---
name: <slug>
description: "<one-line retrieval trigger — load when…>"
last_refreshed: <YYYY-MM-DD>
sources:
  - "<citation or url>"
---

<distilled, self-contained body — usable without any other entry>

Related: [[<other-slug>]]
EOF
```

Swap `capture` → `refresh` and the trailer → `Capture-verdict:refresh` for a refresh of a named
entry; everything else is identical.

**Quote `description` and every `sources` value in double quotes.** Triggers and citation titles
routinely contain a colon-space (`SoK: …`, `load when: …`); left unquoted, YAML misreads the value
and the engine bounces the write. Quoting up front avoids the round-trip.

## Accept-with-concerns → the `degraded:` marker

When the maintainer accepts despite an unresolved authority or merit concern (e.g. the per-claim
authority flag from `assessment.md`), do not pass it off as a clean full-merit entry and do not
silently drop the concern — write it through the engine's existing `degraded:` frontmatter marker.
Add one line to the frontmatter:

```
degraded: "<the concern — e.g. headline is synthesized; sole citation backs a sub-claim>"
```

The engine then admits the entry even when its sole host is below the authority bar (the marker is
the one deliberate way past the host-gate) and down-ranks it `⚠` in the INDEX — a visible trace for
review, the opposite of a silent dirty write. This is a maintainer **option**, never forced: law 2
keeps the maintainer the sole decider, and the verdict trailer still records the admission.

## What the gate must never do

- Never hand-edit an entry or INDEX, and never write the vault by any path other than the engine.
- Never reimplement or bypass the engine's form-gate or host-allowlist gate — the per-claim
  authority judgment in `assessment.md` layers *above* that gate, it does not replace it.
- Never auto-reject or hard-block a candidate — the maintainer's decision is the sole admission gate.
