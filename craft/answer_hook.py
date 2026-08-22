"""Hold a written answer to the laws — and put the findings where they can be acted on.

Two entry points, and the difference between them is the whole point.

`stop` runs when an answer is finished. It RECORDS the findings and says nothing to anybody.
It cannot usefully say anything: the answer has already gone, and the only reader still
present is the person who was waiting for it. Handing them a list of the author's breaches
spends their attention on a check the author could run — which
`the-users-attention-is-not-a-test-harness` forbids by name, and which is exactly what an
earlier version of this file did.

`prompt` runs when the person speaks again, before the next answer is written. It reads back
what the last answer broke and hands it to the AUTHOR as context. That is the only moment
the finding is worth anything: early enough to change the sentence, addressed to whoever can
change it.

Only the COUNTABLE laws run in either, and that is latency rather than principle. The laws
whose own falsifiers say "Countable" or "A wordlist scan" cost 0.01s for thirty-nine answers.
The ones needing a reader cost 150s or more and run on demand (`python -m craft.answer`).

It never blocks; the exit status is always 0. A failure anywhere is silent, because
instrumentation that breaks the thing it instruments gets removed, and then nothing is
checked at all.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CAP = 8


def _findings(transcript: str):
    from .answer import mechanical, turns
    said = [t for t in turns(Path(transcript)) if t.said.strip()]
    return mechanical(said[-1].said) if said else []


def context(findings) -> str:
    """What the author is told, before writing the next answer."""
    by_law: dict[str, list] = {}
    for f in findings:
        by_law.setdefault(f.law, []).append(f)
    lines = [f"Your last answer broke {len(findings)} craft law(s). Not a block — a reading, "
             "from laws with falsifiers and roots outside this estate. Fix the habit in this "
             "answer rather than apologising for the last one."]
    for law, group in by_law.items():
        lines.append(f"  {law} — {len(group)}x")
        for f in group[:3]:
            lines.append(f"    ({f.because}) {f.sentence[:110]}")
        if len(group) > 3:
            lines.append(f"    ... and {len(group) - 3} more")
    return "\n".join(lines[:CAP + 6])


def main(mode: str) -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path:
            return 0
        found = _findings(path)
        if not found:
            return 0
        if mode == "stop":
            # record and stay silent: the answer has gone, and the only person here is the
            # one who was waiting for it
            from .answer import record
            record(found)
        else:
            # stdout from a UserPromptSubmit hook becomes context for the author
            print(context(found))
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main("prompt" if "--prompt" in sys.argv else "stop"))
