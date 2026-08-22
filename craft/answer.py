"""A report of work, held to the laws about work.

`craft.claims` convicts a claims file somebody chose to write, so it sees only what its
author already noticed — the part that needed no check. This reads what was actually said:
the answer at the end of a turn, and the tool results that were in hand while it was written.

WHICH LAWS. The whole `practice` family, and nothing else. That is not a selection: the
family exists in this package with its own docstring — "laws about the WORK, not about the
interface... these convict a way of working" — and an answer reporting work is what it was
written for. Every one of its triggers is about reporting rather than about a screen:
"anything is reported as done", "a done-claim is made", "a result is reported to somebody
who will act on it".

The interface family is excluded entirely, and that is the honest line rather than a cautious
one. Some of those laws probably do bear on an answer, but nothing here can say WHICH — their
triggers are prose, and picking among them by hand or by keyword is a guess wearing a check
(the debt `triggers-are-prose-so-applicability-cannot-be-computed` carries that, with the
route: a trigger as an expr the substrate can solve). Until it is computed, this takes a
family that was already drawn and takes all of it.

There is no pattern matching. The whole answer goes to a reader with the laws and their
falsifiers, and the reader finds what it finds.

    python -m craft.answer                    # the newest transcript for a project
    python -m craft.answer --transcript PATH --all
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from .practice import PRACTICE

_ROOT = Path(__file__).resolve().parents[1]


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


def laws() -> list[tuple[str, str, str]]:
    """(id, statement, falsifier) for every law about the work. The falsifier travels with
    the statement always: a reader asked to judge without it is being asked for an opinion."""
    out = []
    for node in PRACTICE:
        falsifier = next((c.payload.get("claim", "") for c in node.children
                          if c.kind == "falsifier"), "")
        out.append((node.id, node.name or "", falsifier))
    return out


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


_PROMPT = """You are holding one report of work to the laws about how work is reported.

The report was written to a person at the end of a turn in which tools were run. The evidence
section is what those tools actually established while it was being written.

THE LAWS. Each has a statement and a FALSIFIER. The falsifier is what a breach looks like and
it is what you judge against. Do not invent laws and do not stretch one to fit.

{laws}

--- evidence the tools established this turn ---
{evidence}
--- end evidence ---

--- the report ---
{answer}
--- end report ---

Report only clear breaches: a sentence you could show a person beside the falsifier and have
them agree. Prefer saying nothing to reaching. Quote the offending sentence verbatim and give
the reason in at most 25 words.

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
    """The whole report against the whole family.

    None means NOT CHECKED — no reader, or no laws. Neither may be recorded as a clean
    report; that difference is what separates a check from a decoration."""
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
    """Every verdict, with what it rested on. A verdict that leaves no trace is an opinion,
    and this file is how a wrong one is found later and argued with."""
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
    law_set = laws()
    read = [t for t in turns(path) if t.said.strip()]
    subject = read if ns.all else read[-1:]
    print(f"{len(subject)} report(s), {len(law_set)} law(s) about the work")
    total = 0
    for i, t in enumerate(subject):
        found = judge(t.said, t.results, law_set)
        if found is None:
            print(f"  report {i}: NOT CHECKED (no reader)")
            continue
        for f in found:
            total += 1
            print(f"  {f.law}\n    {f.sentence[:160]}\n    why: {f.because}")
    print(f"{total} finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
