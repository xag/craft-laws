"""A written answer, held to the laws it is subject to.

`craft.claims` convicts a claims file somebody chose to write, so it sees only what its
author already noticed. This reads the answer itself — the text that went to the person at
the end of a turn — and holds it to the laws in this package that a written answer can break.

Forty-odd laws here are about WORDS, and most were written for an interface's copy. An answer
to a person is copy: the same claims, the same falsifiers, the same roots. `WRITTEN_ANSWER`
below is the subset whose falsifier a reader can decide from the answer and the evidence
behind it, and nothing else. Laws about controls, fields, focus order and images are left out
because nothing here can see what they are about — not because they matter less.

There is no pattern matching. An earlier attempt put a hedge lexicon in front of the reader
to "narrow" the prose; measured over twenty transcripts it was wrong about seven times in
eight, and worse, it could only recognise about twenty hedge words — so every law that is not
about hedging was invisible however badly broken. A filter that cannot see a law's subject
cannot filter for it. The whole answer goes to the reader, with the laws.

It INFORMS. It never blocks. Every finding is recorded with what it rested on, because a
verdict that leaves no trace is an opinion and this is how a wrong one gets argued with.

    python -m craft.answer                    # the newest transcript for a project
    python -m craft.answer --transcript PATH --all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from .laws import LAWS
from .practice import PRACTICE

_ROOT = Path(__file__).resolve().parents[1]

# The laws whose TRIGGER fires for a written answer to a person, read one by one out of the
# nodes rather than picked by whether the law is "about words".
#
# That distinction is the whole of it, and getting it wrong produced visible nonsense. An
# earlier set was chosen by keyword and included sentences-stay-under-twenty-five-words,
# whose own statement reads "No sentence of INTERFACE PROSE", whose falsifier reads "A
# sentence in UI COPY", and whose trigger is "the app's voice does work of its own (dry,
# terse, no explaining text)". An explanation is explaining text; the trigger never fires.
# The check duly reported every long sentence in an answer and the answers came back chopped
# into fragments to satisfy a counter that was never addressed to them.
#
# Six more triggered on "the project ships documentation meant to be read long after it is
# written (a README, a guide, a reference)". A chat answer is read once, now. Three needed a
# control that commits something.
#
# What survives is the practice family and its neighbours: laws about what a claim may
# assert, which fire on "anything is reported as done", "a result is reported to somebody
# who will act on it", "a gap is being explained". NONE of them is countable — every one
# needs a reader, and that is a fact about this surface rather than a gap in the tooling.
WRITTEN_ANSWER = [
    "done-is-observed-where-the-user-stands",
    "the-users-attention-is-not-a-test-harness",
    "a-detour-is-announced-as-a-detour",
    "deliberate-names-its-decision",
    "a-remainder-names-its-debt",
    "a-census-is-read-from-its-source",
    "a-qualifier-is-licensed-by-the-evidence",
    "what-exists-is-not-thereby-chosen",
    "a-thing-is-built-where-its-subject-lives",
    "what-accompanies-a-claim-supports-it",
]


@dataclass
class Finding:
    law: str
    sentence: str
    because: str
    adjudicator: str = "claude -p"


@dataclass
class Turn:
    said: str = ""
    results: str = ""
    tools: int = 0


def laws(ids: list[str] | None = None) -> list[tuple[str, str, str]]:
    """(id, statement, falsifier) for each named law, from this package's own nodes."""
    want = set(ids if ids is not None else WRITTEN_ANSWER)
    out = []
    for node in [*LAWS, *PRACTICE]:
        if node.id not in want:
            continue
        falsifier = next((c.payload.get("claim", "") for c in node.children
                          if c.kind == "falsifier"), "")
        out.append((node.id, node.name or "", falsifier))
    return out


def missing(ids: list[str] | None = None) -> list[str]:
    """Named laws this package no longer has — a rename would otherwise stop an answer
    being held to a law with nothing said."""
    want = set(ids if ids is not None else WRITTEN_ANSWER)
    return sorted(want - {n.id for n in [*LAWS, *PRACTICE]})


def _text(content) -> str:
    if isinstance(content, str):
        return content
    out = []
    for block in content or []:
        if isinstance(block, dict) and block.get("type") == "text":
            out.append(block.get("text") or "")
        elif isinstance(block, dict) and block.get("type") == "tool_result":
            c = block.get("content")
            out.append(c if isinstance(c, str) else _text(c))
    return "\n".join(out)


def turns(transcript: Path) -> list[Turn]:
    """Every turn in a Claude Code transcript, oldest first; a turn ends when the person
    speaks again."""
    out: list[Turn] = []
    cur = Turn()
    for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        kind, msg = rec.get("type"), rec.get("message") or {}
        if kind == "assistant":
            for block in msg.get("content") or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    cur.said += "\n" + (block.get("text") or "")
                elif block.get("type") == "tool_use":
                    cur.tools += 1
        elif kind == "user":
            content = msg.get("content")
            if isinstance(content, list) and any(
                    isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                cur.results += "\n" + _text(content)
            else:
                if cur.said.strip() or cur.tools:
                    out.append(cur)
                cur = Turn()
    if cur.said.strip() or cur.tools:
        out.append(cur)
    return out


# NO LAW HERE IS COUNTABLE, and that is the finding rather than a shortcoming. The
# countable ones — sentence length, paragraph length, wordlists — all belong to surfaces this
# is not: interface copy, or documentation read long after it was written. Every law whose
# trigger fires for an answer is about what a claim may assert, and that needs a reader.
#
# So there is no fast path. `judge` costs one to three minutes and runs on demand.

_PROMPT = """You are holding one written answer to the laws it is subject to.

The answer was written to a person at the end of a turn in which tools were run. The evidence
section is what those tools actually established while it was being written.

THE LAWS. Each has a statement and a FALSIFIER. The falsifier is what a breach looks like and
it is what you judge against. Do not invent laws and do not stretch one to fit.

{laws}

--- evidence the tools established this turn ---
{evidence}
--- end evidence ---

--- the answer ---
{answer}
--- end answer ---

Report only clear breaches: a sentence you could show a person beside the falsifier and have
them agree. Prefer saying nothing to reaching. Quote the offending sentence verbatim from the
answer and give the reason in at most 25 words.

Answer with JSON only, no prose around it:
{{"findings": [{{"law": "<law id>", "sentence": "<verbatim>", "because": "<reason>"}}]}}"""


def _ask(prompt: str, timeout: float = 180.0) -> dict | None:
    try:
        done = subprocess.run(["claude", "-p", "--output-format", "text", prompt],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout, cwd=_ROOT)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (done.stdout or "").strip()
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b <= a:
        return None
    try:
        return json.loads(text[a:b + 1])
    except ValueError:
        return None


def judge(answer: str, evidence: str, law_set=None) -> list[Finding] | None:
    """The whole answer against the whole law set.

    None means NOT CHECKED — no reader, or no laws. Neither may be recorded as a clean
    answer; that difference is what separates a check from a decoration."""
    law_set = laws() if law_set is None else law_set
    if not law_set or not answer.strip():
        return None
    got = _ask(_PROMPT.format(
        laws="\n\n".join(f"{i + 1}. {lid}\n   SAYS: {says}\n   BREACH: {fal}"
                         for i, (lid, says, fal) in enumerate(law_set)),
        evidence=(evidence or "(none)")[-2500:], answer=answer[-6000:]))
    if got is None or "findings" not in got:
        return None
    known = {lid for lid, _, _ in law_set}
    return [Finding(law=f["law"], sentence=str(f.get("sentence", ""))[:300],
                    because=str(f.get("because", ""))[:200])
            for f in got["findings"] if isinstance(f, dict) and f.get("law") in known]


def record(findings: list[Finding], path: Path | None = None) -> Path:
    path = path or (_ROOT / ".craft" / "answers.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        for x in findings:
            f.write(json.dumps(asdict(x), ensure_ascii=False) + "\n")
    return path


def newest_transcript(project: Path) -> Path | None:
    root = Path(os.path.expanduser("~")) / ".claude" / "projects"
    for candidate in sorted(root.glob("*")):
        if candidate.is_dir() and project.name in candidate.name:
            tapes = sorted(candidate.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
            if tapes:
                return tapes[-1]
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m craft.answer", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--transcript", type=Path, default=None)
    ap.add_argument("--project", type=Path, default=Path.cwd())
    ap.add_argument("--all", action="store_true")
    ns = ap.parse_args(argv)

    path = ns.transcript or newest_transcript(ns.project)
    if path is None or not path.exists():
        print("no transcript found; nothing to check")
        return 0
    if gone := missing():
        print(f"named but no longer a law here: {', '.join(gone)}")
    law_set = laws()
    read = [t for t in turns(path) if t.said.strip()]
    subject = read if ns.all else read[-1:]
    print(f"{len(subject)} answer(s), {len(law_set)} law(s)")
    total = 0
    for i, t in enumerate(subject):
        found = judge(t.said, t.results, law_set)
        if found is None:
            print(f"  answer {i}: NOT CHECKED (no reader)")
            continue
        for f in found:
            total += 1
            print(f"  {f.law}\n    {f.sentence[:160]}\n    why: {f.because}")
    print(f"{total} finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
