"""The Stop hook: hold an answer to the laws about how work is reported.

What it broke comes back to the author while the sentence can still be rewritten.

The finding is worth something only while the sentence can still be rewritten. Two earlier
shapes both missed that window, and both are worth naming because the mistake is easy. A
`systemMessage` at Stop reaches the person waiting, not the author, and arrives after the
answer has gone — spending the reader's attention on a check the writer could run, which
`the-users-attention-is-not-a-test-harness` forbids. Injecting at the next prompt reaches the
right party a turn late, when all that remains is an apology.

So it comes back through Stop, to the author, at once. Claude Code returns a Stop hook's
stderr to the model when the hook exits 2, and the model carries on with it in hand. That is
feedback, not a verdict: nothing is refused, nothing is overruled, and the author decides
what the sentence should be.

ONCE PER ANSWER, and the guard is load-bearing. Without it a revised answer still carrying a
breach comes straight back, and again, and the loop never settles — a check that will not let
go is one that gets switched off. The hash of what was already reported is remembered, so a
second Stop on the same text is silent and the author's judgement stands.

It costs a reader, measured at 33-47 seconds over the twelve laws. That is real, and it is
the price of judging meaning instead of matching words. Every failure path exits 0 in
silence: instrumentation that breaks the thing it instruments gets removed, and then nothing
is checked at all.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SEEN = _ROOT / ".craft" / "seen.json"


def _already_reported(answer: str) -> bool:
    """Has this exact text already been handed back once? The author saw it and chose;
    saying it again would argue rather than inform."""
    digest = hashlib.sha256(answer.encode("utf-8", "replace")).hexdigest()
    try:
        seen = set(json.loads(_SEEN.read_text(encoding="utf-8")))
    except Exception:
        seen = set()
    if digest in seen:
        return True
    seen.add(digest)
    try:
        _SEEN.parent.mkdir(parents=True, exist_ok=True)
        _SEEN.write_text(json.dumps(sorted(seen)[-400:]), encoding="utf-8")
    except OSError:
        pass
    return False


def report(findings) -> str:
    """What the author is handed, while the answer can still be changed."""
    lines = [f"This answer breaks {len(findings)} law(s) about how work is reported — each "
             "with a falsifier and a root outside this estate. Fix it and finish; nothing is "
             "refused, and if a reading is wrong, say so and carry on."]
    for f in findings:
        lines.append(f"  {f.law}")
        lines.append(f"    {f.sentence[:170]}")
        lines.append(f"    why: {f.because}")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path or payload.get("stop_hook_active"):
            return 0
        from .answer import judge, record, turns
        said = [t for t in turns(Path(path)) if t.said.strip()]
        if not said:
            return 0
        answer, evidence = said[-1].said, said[-1].results
        if _already_reported(answer):
            return 0
        found = judge(answer, evidence)
        if not found:
            return 0        # None is NOT CHECKED, [] is clean; neither is worth interrupting
        record(found)
        print(report(found), file=sys.stderr)
        return 2
    except Exception:
        # a broken checker costs a check; it must never cost the person their turn
        return 0


if __name__ == "__main__":
    sys.exit(main())
