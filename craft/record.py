"""The turn's record, read as an anchor corpus: what the harness wrote and what the
user typed, against which an account's grounds are checked.

WHY THIS MODULE EXISTS. The first account lane was removed (the-turn-account-lane-is-
removed) because every word its verdict depended on was chosen by the checked party.
The rebuild anchors those words here: a grounded premise must QUOTE, verbatim, a
stretch of an artifact its author does not write. Two such artifacts exist in every
turn, and they divide exactly along the ground vocabulary:

  tool results   written by the harness: what commands actually printed, what files
                 actually contained. Anchors `producer` and `stand-in`.
  user messages  written by the person. Anchors `given` and `user-surface`.

The assistant's own prose is deliberately NOT corpus: quoting yourself is the
self-report this lane was removed for.

WHAT ANCHORING PROVES, and what it does not -- stated here because overclaiming is the
founding defect of this lane. A quote that anchors proves those words appeared in the
record, selected by the author from output the author did not write. It does not prove
the record was not staged: a command can be run whose output prints the desired
sentence, and its quote will anchor. What anchoring buys over self-report is that
staging is VISIBLE -- the command sits in the record beside its output, auditable by a
reader -- where a self-chosen label left nothing to audit at all. Under-selection
(quoting the one line that helps) likewise remains the author's, measured only by a
later audit of the same record; that is the same declared residue as drawing.py's
authored derivation.

Quotes are matched with whitespace runs collapsed on both sides -- drawing.py's
canonical form, a defined normalization and not a similarity measure.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

_WS = re.compile(r"\s+")


def _canon(s: str) -> str:
    return _WS.sub(" ", s).strip()


@dataclass
class Corpus:
    """The two anchor pools, whitespace-normalized once at construction."""
    tool_text: str = ""
    user_text: str = ""
    counts: dict = field(default_factory=dict)

    def anchors(self, ground: str, quote: str) -> bool:
        pool = (self.tool_text if ground in ("producer", "stand-in")
                else self.user_text if ground in ("given", "user-surface")
                else "")
        q = _canon(quote)
        return bool(q) and q in pool


def _texts(content) -> list[str]:
    """Every text payload in a message content value, whatever its nesting."""
    out = []
    if isinstance(content, str):
        out.append(content)
    elif isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                out.append(str(block.get("text", "")))
            elif block.get("type") == "tool_result":
                out.extend(_texts(block.get("content")))
    return out


def read(transcript: Path) -> Corpus:
    """The corpus from a session transcript (JSONL, one message per line).

    Tool results live inside user-role messages as tool_result blocks; the person's
    own words are the user-role text blocks that are not tool results. Assistant
    messages are skipped whole -- the author's prose anchors nothing."""
    tool_parts: list[str] = []
    user_parts: list[str] = []
    n_tool = n_user = 0
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") != "user":
            continue
        content = (rec.get("message") or {}).get("content")
        if isinstance(content, str):
            user_parts.append(content)
            n_user += 1
            continue
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_result":
                tool_parts.extend(_texts(block.get("content")))
                n_tool += 1
            elif block.get("type") == "text":
                user_parts.append(str(block.get("text", "")))
                n_user += 1
    return Corpus(tool_text=_canon("\n".join(tool_parts)),
                  user_text=_canon("\n".join(user_parts)),
                  counts={"tool_results": n_tool, "user_texts": n_user})
