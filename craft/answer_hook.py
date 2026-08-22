"""Hold a written answer to the laws, and hand what it broke back to the author at once.

The finding is worth something only while the answer can still be changed. Two earlier
shapes both missed that window and both are worth naming, because the mistake is easy.

A `systemMessage` at Stop reaches the person waiting, not the author, and arrives after the
answer has gone — spending the reader's attention on a check the writer could run, which
`the-users-attention-is-not-a-test-harness` forbids. Injecting at the next prompt reaches the
right party but a turn late: the answer is out, and all that is left is an apology.

So the finding comes back through Stop, to the author, immediately. Claude Code returns a
Stop hook's stderr to the model when the hook exits 2, and the model carries on with it in
hand. That is feedback, not a verdict: nothing is refused, nothing is overruled, and the
author decides what the sentence should be. The check reports; the writer writes.

ONCE PER ANSWER, and that guard is load-bearing. Without it a revised answer that still
carries a long sentence would be handed straight back, and again, and the loop would never
settle — a check that will not let go is one that gets switched off. The hash of the answer
already reported is remembered, so a second Stop on the same text is silent and the author's
judgement stands.

Only the COUNTABLE laws run here: their own falsifiers say "Countable" or "A wordlist scan",
and they cost 0.01s for thirty-nine answers. The laws needing a reader cost 150s or more and
run on demand (`python -m craft.answer`).

A failure anywhere is silent. Instrumentation that breaks the thing it instruments gets
removed, and then nothing is checked at all.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SEEN = _ROOT / ".craft" / "seen.json"
CAP = 6


def _last_answer(transcript: str):
    from .answer import turns
    said = [t for t in turns(Path(transcript)) if t.said.strip()]
    return said[-1].said if said else ""


def _already_reported(answer: str) -> bool:
    """Has this exact answer already been handed back once? The author saw it and chose;
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
    by_law: dict[str, list] = {}
    for f in findings:
        by_law.setdefault(f.law, []).append(f)
    lines = [f"This answer breaks {len(findings)} craft law(s) — laws with falsifiers and "
             "roots outside this estate. Fix the sentences and finish; nothing is refused, "
             "and if a reading is wrong, say so and carry on."]
    for law, group in by_law.items():
        lines.append(f"  {law} — {len(group)}x")
        for f in group[:3]:
            lines.append(f"    ({f.because}) {f.sentence[:110]}")
        if len(group) > 3:
            lines.append(f"    ... and {len(group) - 3} more")
    return "\n".join(lines[:CAP + 8])


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path or payload.get("stop_hook_active"):
            return 0
        answer = _last_answer(path)
        if not answer.strip():
            return 0
        from .answer import mechanical, record
        found = mechanical(answer)
        if not found or _already_reported(answer):
            return 0
        record(found)
        print(report(found), file=sys.stderr)
        return 2
    except Exception:
        # a broken checker costs a check; it must never cost the person their turn
        return 0


if __name__ == "__main__":
    sys.exit(main())
