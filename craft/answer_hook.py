"""The Stop hook: hold the answer about to be handed back to the laws that need no reader.

It INFORMS. It never blocks, and the exit status is always 0.

Only the COUNTABLE laws run here, and the reason is latency rather than principle. A reader
(`python -m craft.answer`) judges the laws that need judgement — done-is-observed,
a-qualifier-is-licensed, say-it-once — and measured on this machine it costs one to three
minutes per answer. That cannot sit in front of a person, and a check that makes someone wait
is a check that gets switched off. The laws whose own falsifiers say "Countable" or "A
wordlist scan" cost 0.01s for thirty-nine answers, so they run every turn.

Every finding is recorded in `.craft/answers.jsonl` with what it rested on. A failure
anywhere is silent: instrumentation that breaks the thing it instruments gets removed, and
then nothing is checked at all.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CAP = 6


def message(findings, total: int) -> str:
    lines = [f"{total} finding(s) against the craft laws — a reading, not a block:"]
    for f in findings[:CAP]:
        lines.append(f"  {f.law} — {f.because}")
        lines.append(f"    {f.sentence[:150]}")
    if total > CAP:
        lines.append(f"  ... and {total - CAP} more; `python -m craft.answer` for all of it")
    lines.append("Each law carries a falsifier and a root outside this estate. The reader's "
                 "laws — what a claim may assert, whether a hedge is licensed — are not run "
                 "here: they cost minutes. `python -m craft.answer` runs those.")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path:
            return 0
        from .answer import mechanical, record, turns
        said = [t for t in turns(Path(path)) if t.said.strip()]
        if not said:
            return 0
        found = mechanical(said[-1].said)
        if found:
            record(found)
            print(json.dumps({"systemMessage": message(found, len(found))}))
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
