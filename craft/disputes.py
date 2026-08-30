"""Where a convicted turn says the conviction is wrong -- as data, never to the user.

The convictions the hooks hand back land while the reply can still be fixed, and that
is where their usefulness ends: a model that believes a conviction is a false positive
has, until now, had exactly one channel to say so -- the reply itself. Every rebuttal
paragraph written there is noise to a person who never saw the conviction, and it is
also lost: prose in a scrolled transcript measures nothing.

This module is the other channel. One JSON line per dispute, appended to
`.craft/disputes.jsonl` beside the checker's other records, carrying the finding it
disputes and the one-line ground for disputing it. The pile is what the checker's
false-positive rate is computed FROM: a law that collects disputes faster than
convictions it survives is a law with a defect, and today's four absence-scheme
convictions on definitional negatives are exactly the pattern such a pile makes
visible. quality-harness reads ledgers estate-wide; this file is written to be read.

A dispute PROPOSES, like a notebook verdict: filing one does not lift the conviction,
does not edit the seen-state, and is not a verdict on the law. The judgment stays with
whoever reads the pile.

    python -m craft.disputes --law <id> --where <account#node> --why "<one line>"
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
DISPUTES = _ROOT / ".craft" / "disputes.jsonl"


def file_dispute(law: str, where: str, why: str, session: str = "") -> dict:
    """Append one dispute. Returns the record written."""
    rec = {"law": law, "where": where, "why": why, "session": session,
           "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    DISPUTES.parent.mkdir(parents=True, exist_ok=True)
    with DISPUTES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m craft.disputes",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--law", required=True, help="the law id the finding named")
    ap.add_argument("--where", required=True,
                    help="the finding's location as it was reported "
                         "(e.g. critic-live-3.json r2, or claims.jsonl#7)")
    ap.add_argument("--why", required=True,
                    help="one line: what makes this finding a false positive")
    ap.add_argument("--session", default="", help="the convicted session's id")
    ns = ap.parse_args(argv)
    rec = file_dispute(ns.law, ns.where, ns.why, ns.session)
    print(f"dispute filed: {rec['law']} ({rec['where']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
