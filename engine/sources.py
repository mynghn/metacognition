"""sources — the family's source-authority policy logic.

The single home for parsing SOURCES.md (the human-ratifiable "what counts as
authoritative" policy) and applying it. Imported by BOTH consumers the policy
serves: kb-engine's write-gate (reject a write whose sole support is below the
allowlist) and the health-check source-lint (flag sub-allowlist citations and an
uncorroborated load-bearing number). One parser, so the bar a write must clear is
byte-identical to the bar detection flags against — they can never drift apart.

Authority (allowlist) and corroboration (>=2 distinct sources) are ORTHOGONAL: an
entry can be well-corroborated yet all-sub-tier (gated on authority), or single-
sourced yet authoritative (corroboration-flagged only if it also makes a load-
bearing numeric claim). The two checks are kept separate for that reason.
"""
import os
import re

# SOURCES.md lives at the engine REPO root (one dir up from engine/), alongside
# FAMILY.md — it is framework policy, not vault content, and applies family-wide.
DEFAULT_SOURCES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SOURCES.md")

# Citation hosts are read from BOTH schemed URLs and bare domain tokens. A `sources:` line is
# free-text (`- <citation or url>`), and an LLM-rendered citation routinely drops the scheme
# ("Author, sitename.com, 2026"). Reading only `https?://…` left a scheme-less sub-tier host
# invisible to the gate — it was admitted clean, the exact defeat of the authority bar this code
# exists to enforce. _SCHEMED_RE captures a URL's authority (userinfo/port stripped downstream);
# _BARE_HOST_RE catches a bare domain, its lookbehind skipping an email local-part's `@domain`.
_SCHEMED_RE = re.compile(r"(?i)\b[a-z][a-z0-9+.\-]*://([^/\s)\"'>\]]+)")
_BARE_HOST_RE = re.compile(r"(?i)(?<![\w@.])((?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+[a-z]{2,})\b")


def resolve_sources(explicit=None):
    """Resolve the policy path: explicit `--sources` > $KB_SOURCES > engine-repo default."""
    for cand in (explicit, os.environ.get("KB_SOURCES"), DEFAULT_SOURCES):
        if cand and cand.strip():
            return os.path.abspath(os.path.expanduser(cand.strip()))
    return DEFAULT_SOURCES


def load_allowlist(path):
    """Parse the fenced ```hosts block of SOURCES.md into lowercased host patterns.
    Returns (patterns, found): found is False when the file, the fenced block, OR its host list
    is absent/empty — an empty allowlist is reported as not-found so the caller fails LOUD
    rather than silently treating a blanked/comment-only policy as a reject-all (or admit-all)
    bar. Either silent reading of absence corrupts the authority bar."""
    if not os.path.isfile(path):
        return [], False
    text = open(path, encoding="utf-8").read()
    m = re.search(r"(?m)^```hosts[ \t]*\n(.*?)^```", text, re.S)
    if not m:
        return [], False
    pats = []
    for raw in m.group(1).splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            pats.append(line.lower())
    return pats, bool(pats)


def host_allowed(host, patterns):
    """True if host matches any allowlist pattern. `*.example.com` matches the apex
    (`example.com`) AND any subdomain (`docs.example.com`) — the intuitive domain-and-
    subdomains semantics; a bare `example.com` pattern is an exact match only."""
    host = (host or "").strip().lower().rstrip(".")
    if not host:
        return False
    for pat in patterns:
        if pat.startswith("*."):
            base = pat[2:]
            if host == base or host.endswith("." + base):
                return True
        elif host == pat:
            return True
    return False


def split_frontmatter(body):
    """Return (frontmatter, rest): frontmatter is the leading `---\\n…\\n---` block, or ''."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", body, re.S)
    return (m.group(1), m.group(2)) if m else ("", body)


def _authority_host(authority):
    """The real host of a URL authority: drop userinfo (keep the part after the LAST '@') and
    the :port, so `arxiv.org@evil.com` resolves to `evil.com` — a spoofed allowlisted userinfo
    can't smuggle a sub-tier real host past the gate."""
    return authority.rsplit("@", 1)[-1].split(":", 1)[0].lower().rstrip(".")


def source_hosts(body):
    """Ordered, de-duplicated citation hosts from the entry's `sources:` frontmatter block.
    Reads only the sources block (not the prose body), so an inline link in the text is never
    mistaken for a citation that clears the authority bar. Schemed and bare-domain citations are
    both recognized; a citation line with no host token at all contributes nothing (a citation
    without a verifiable host can't clear the bar, and an entry with zero hosts is left to the
    existing presence check)."""
    fm, _ = split_frontmatter(body)
    msrc = re.search(r"(?ms)^sources:[ \t]*\n(.*?)(?=^\S|\Z)", fm + "\n")
    block = msrc.group(1) if msrc else ""
    seen, out = set(), []

    def add(h):
        h = h.lower().rstrip(".")
        if h and h not in seen:
            seen.add(h)
            out.append(h)

    for m in _SCHEMED_RE.finditer(block):
        add(_authority_host(m.group(1)))
    # Bare domains in what's left after removing schemed URLs, so a URL's userinfo/path can't
    # re-surface a host that _authority_host already resolved away.
    for m in _BARE_HOST_RE.finditer(_SCHEMED_RE.sub(" ", block)):
        add(m.group(1))
    return out


def authority_violation(body, patterns):
    """Authority gate: a write's sole support must not be below the bar. Returns an error
    string when NO citation host clears the allowlist (sole support below the bar → reject,
    never write dirty), or None when at least one does. An entry with zero citations is left
    to the existing presence check — this judges only the hosts that are there."""
    hosts = source_hosts(body)
    if not hosts:
        return None
    if any(host_allowed(h, patterns) for h in hosts):
        return None
    return ("no citation clears the source allowlist (sole support below the authority bar): %s"
            % ", ".join(hosts))


# A load-bearing number is a quantitative CLAIM in the prose — a percentage, a decimal, a
# currency figure, a magnitude-suffixed count, or a 4+-digit integer — but NOT a bare year
# (1900-2099) or a number inside a URL/citation. Deterministic by construction: detection
# performs no content research, only pattern-matching over the text.
_YEAR_RE = re.compile(r"^(?:19|20)\d{2}$")
# Strip WHOLE URLs (schemed and bare `host/path`) before scanning, so a digit in a URL PATH
# (e.g. `/abs/2401.12345`) is never misread as a numeric claim.
_URL_STRIP_RE = re.compile(
    r"(?i)(?:\b[a-z][a-z0-9+.\-]*://[^\s)\"'>\]]+"
    r"|\b(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+[a-z]{2,}/[^\s)\"'>\]]*)")
# ONE alternation, scanned non-overlapping (finditer) with the suffixed forms FIRST, so a
# decimal percentage/currency is captured whole (`90.2%`) and the bare-decimal branch never
# re-matches its digits (`90.2`) — one claim, one token.
_NUM_RE = re.compile(r"""
      \$\d[\d,]*(?:\.\d+)?            # $47,000
    | \d+(?:\.\d+)?%                  # 18%  90.2%
    | \d+(?:\.\d+)?\s*[kKmMbB]\b      # 10k  1.5M
    | \d+(?:\.\d+)?x\b                # 3x
    | \d{1,3}(?:,\d{3})+              # 194,480
    | \d+\.\d+                        # 2.5
    | \d{4,}                         # 10000
""", re.X)


def load_bearing_numbers(body):
    """The load-bearing numeric claims in an entry's prose body (frontmatter + whole URLs
    stripped, bare years excluded). Ordered, de-duplicated. KNOWN LIMITATION: a 4-digit quantity
    that falls in 1900-2099 (e.g. `2048 tokens`) is treated as a year and not surfaced — the
    deterministic layer can't tell a year from a same-range magnitude, so the heal-time
    verification envelope, not this advisory, is the backstop for an in-range numeric claim."""
    _, prose = split_frontmatter(body)
    prose = _URL_STRIP_RE.sub(" ", prose)
    seen, out = set(), []
    for m in _NUM_RE.finditer(prose):
        t = m.group(0).strip()
        if _YEAR_RE.match(t) or t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


def corroboration_flag(body):
    """Flag an entry that makes a load-bearing numeric claim on fewer than two distinct
    sources — a load-bearing number must carry a corroborating source. Returns the list
    of uncorroborated numbers (a non-empty list is the flag), or [] when corroborated or
    number-free. Advisory by design — corroboration is a judgment the deterministic layer can
    surface but not adjudicate; the hard call lives in the skill's verification envelope."""
    nums = load_bearing_numbers(body)
    if nums and len(source_hosts(body)) < 2:
        return nums
    return []
