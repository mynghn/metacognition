# SOURCES — authority policy

What counts as an authoritative source for a vault entry. This file is **policy, not
mechanism**: the prose below is the human-ratifiable bar; the fenced `hosts` block is the
machine-parseable allowlist the [`engine/`](engine) write-gate and the
[`health-check`](health-check) source-lint both read (one parser, so the bar a write must
clear is exactly the bar detection flags against). SOURCES.md is itself a living artifact —
evolve it through the same propose→ratify path as any vault change, never a silent edit.

## Tier-1 — authoritative (at or above the bar)

A citation clears the bar when it is one of:

- **Peer-reviewed or foundational research** — arXiv, ACL Anthology, OpenReview, NeurIPS/ICML
  proceedings, ACM DL, and the canonical first-party report behind a named result.
- **Official standards & specifications** — the standards body or spec home itself (OWASP,
  IETF, W3C, the Model Context Protocol spec).
- **First-party vendor engineering docs** — the vendor's own documentation/research for the
  system under discussion (Anthropic, OpenAI, the model/framework's own docs site). Vendor
  *marketing* pages do not clear the bar; vendor *engineering/research* pages do.
- **Named practitioners with standing** — a recognised individual writing in their area of
  expertise (e.g. Martin Fowler on architecture, Hamel Husain on evals). The authority is the
  person, not the platform — so a named practitioner's own site is listed by host, while a
  generic blogging platform (dev.to, Medium, Substack) is **not** allowlisted: anyone can post
  there, so a post's authority cannot be read from the host.

Everything else is **sub-tier**: usable as colour or a secondary pointer, but it may not be an
entry's *sole* support, and it never satisfies the corroboration rule for a load-bearing number.

## Allowlist

Host patterns. `*.example.com` matches the apex and any subdomain; a bare `example.com` is an
exact match. Lowercase; `#` starts a comment. Keep this list curated to Tier-1 — adding a host
lowers the bar for every future write.

```hosts
# Research / peer-reviewed / foundational
arxiv.org
*.arxiv.org
aclanthology.org
openreview.net
*.neurips.cc
proceedings.mlr.press
dl.acm.org
distill.pub

# Official standards & specifications
*.owasp.org
*.ietf.org
*.w3.org
modelcontextprotocol.io

# First-party model / framework / vendor engineering docs
*.anthropic.com
*.claude.com
*.openai.com
*.langchain.com
*.temporal.io
*.trychroma.com
*.ragas.io
*.inngest.com
ai.google.dev
*.deepmind.com
learn.microsoft.com
docs.aws.amazon.com

# Recognised research orgs / institutes
metr.org
*.aisi.org.uk
*.lmsys.org
*.evidentlyai.com

# Named practitioners with standing (the person, not the platform)
martinfowler.com
hamel.dev
```

## Corroboration

A **load-bearing number** — a percentage, a benchmark figure, a cost, a dataset size, any
quantitative claim the entry leans on — must carry at least one corroborating source: ideally a
Tier-1 primary, and a second independent source when the figure is surprising or contested. A
single-sourced load-bearing number is *flagged*, not auto-rejected — the deterministic layer can
surface the gap but not judge whether the figure is truly load-bearing; that call belongs to the
heal-time verification envelope. Authority and corroboration are independent: clearing the
allowlist does not waive corroboration, and being well-corroborated does not waive the allowlist.
