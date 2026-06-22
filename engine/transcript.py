"""transcript — deterministic "did a scoped skill fire in this run" reader over Claude Code session JSONL.

The single home for turning a persisted session transcript into the fact the activation eval is built
on: which scoped skills fired. Model-free, read-only, deterministic — a transcript fact, never a judge: a
deterministic final-state read beats an LLM judge when the ground truth is already in the trace. The
scorer imports this so its firing signal cannot drift from the corpus's notion of scope.

Firing is DUAL-KEYED for robustness against either signal being absent in a given record:
  1. an assistant content block {"type":"tool_use","name":"Skill","input":{"skill":"<scoped>"}} — the
     invocation site (input.skill is the bare skill name);
  2. a top-level record field attributionSkill == "<scoped>" — Claude Code's own attribution of the
     record to the skill that produced it.
Either alone counts as a firing. Both signals are observed in live Claude Code transcripts on this machine.

A run is the MAIN transcript UNION every sub-agent transcript: sub-agent (Task / workflow) runs are
persisted under <session-uuid>/subagents/.../*.jsonl, NOT inlined into the parent, so a firing inside a
sub-agent is only visible by walking that subdir.

FAIL LOUD on an unrecognized transcript shape (UnknownTranscriptSchema), never silently report "no
fire": a silent schema drift would read as "skill never fired" and corrupt every self-use / false-fire
rate. The pinned, universally-present envelope is "each record is a
JSON object carrying a `type` key" — verified true across 52k real records spanning 14 record types, so
detection gates on `type`'s PRESENCE, never its value (new record types appear over time). KNOWN BOUND:
this catches a broken record envelope; a silent RENAME of the firing keys themselves (attributionSkill /
the Skill block) cannot be detected from a single transcript and remains the reader's pinned-schema risk.
"""
import json
import os

# The scoped skills the activation contract is bound to — the guarantee holds within, and only within,
# this designated set. Single-sourced here so the scorer, the driver, and the corpus's scope all read
# it from one place and cannot drift.
SCOPED_SKILLS = ("compact-focus", "handoff")


class UnknownTranscriptSchema(Exception):
    """A transcript does not match Claude Code's observed record envelope. Raised instead of returning
    "no fire" so a schema drift surfaces as a hard failure rather than silently zeroing the rates."""


def iter_records(path):
    """Yield each JSONL record (a dict) from a transcript file, in order. Blank lines are skipped; an
    empty file yields nothing (a valid empty transcript, not a schema error). Raises
    UnknownTranscriptSchema on a line that is not a JSON object carrying a `type` key — the envelope
    every Claude Code record shares — so a malformed transcript fails loud at the read."""
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise UnknownTranscriptSchema(
                    "%s:%d is not valid JSON (%s)" % (path, lineno, exc)) from exc
            if not isinstance(rec, dict) or "type" not in rec:
                raise UnknownTranscriptSchema(
                    "%s:%d record lacks the expected {\"type\": ...} envelope" % (path, lineno))
            yield rec


def _firings_in_record(rec):
    """The scoped skills one record shows firing, dual-keyed (attributionSkill OR a Skill tool_use)."""
    fired = set()
    att = rec.get("attributionSkill")
    if att in SCOPED_SKILLS:
        fired.add(att)
    msg = rec.get("message")
    content = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(content, list):
        for block in content:
            if (isinstance(block, dict) and block.get("type") == "tool_use"
                    and block.get("name") == "Skill"):
                skill = (block.get("input") or {}).get("skill")
                if skill in SCOPED_SKILLS:
                    fired.add(skill)
    return fired


def fired_in_transcript(path):
    """The set of scoped skills that fired anywhere in ONE transcript file."""
    fired = set()
    for rec in iter_records(path):
        fired |= _firings_in_record(rec)
    return fired


def subagent_transcripts(session_path):
    """Every sub-agent transcript (*.jsonl) under a session's <uuid>/subagents/ tree, sorted. Walked
    recursively because workflow runs nest deeper than the flat agent-<id>.jsonl layout; the sibling
    *.meta.json files are not transcripts and are skipped by the .jsonl filter."""
    base = os.path.splitext(session_path)[0]
    subdir = os.path.join(base, "subagents")
    out = []
    if os.path.isdir(subdir):
        for root, _dirs, files in os.walk(subdir):
            for fn in files:
                if fn.endswith(".jsonl"):
                    out.append(os.path.join(root, fn))
    return sorted(out)


def fired_in_session(session_path):
    """The set of scoped skills that fired in a run: the main transcript UNION every sub-agent
    transcript. This is the deterministic "did a scoped skill fire in this run" read the scorer
    aggregates into rates."""
    fired = fired_in_transcript(session_path)
    for sub in subagent_transcripts(session_path):
        fired |= fired_in_transcript(sub)
    return fired
