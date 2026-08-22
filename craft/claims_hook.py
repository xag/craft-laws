"""The Stop hook: run the claim deciders before the turn is handed back.

`craft.claims` is the check, and it has been all along: eight code deciders, one per
practice law, over the claims a session records. Its own docstring says the move — "give
the subject a data shape, then convict with certainty or stay silent." It costs a
millisecond.

This runs it when a turn ends, on the claims files of every repository the turn wrote to,
and hands anything it convicts back to the AUTHOR through stderr with exit 2 — the moment
the sentence can still be fixed. Claude Code returns a Stop hook's stderr to the model and
the model carries on with it in hand. Nothing is refused.

WHAT THIS IS NOT. An earlier version sampled a model to read the answer's PROSE against the
laws. It cost 33-47 seconds a turn, spent tokens grading the author's own writing, and was
aimed at the wrong substrate: these laws fire on claims, and a claim is data. The prose was
never what they check.

Once per set of findings, by hash: a turn that has already been told, and chose, is not told
again. Every failure path exits 0 in silence, because instrumentation that breaks the thing
it instruments gets removed, and then nothing is checked at all.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SEEN = _ROOT / ".craft" / "seen.json"


def touched(transcript: Path) -> list[Path]:
    """The claims files of every repository this turn wrote to.

    A turn edits several checkouts, and the claim it should have recorded belongs in the one
    the work was in. Reading only the current directory's file would miss exactly the claims
    a cross-repo turn makes."""
    roots: set[Path] = set()
    for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines()[-4000:]:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") != "assistant":
            continue
        for block in (rec.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            path = (block.get("input") or {}).get("file_path")
            if not path:
                continue
            here = Path(str(path)).parent
            for parent in [here, *here.parents]:
                if (parent / ".git").exists():
                    roots.add(parent)
                    break
    return sorted(r / "claims.jsonl" for r in roots if (r / "claims.jsonl").exists())


def _already_reported(findings) -> bool:
    key = hashlib.sha256(
        "|".join(f"{f.law}{f.where}{f.quote}" for f in findings).encode("utf-8", "replace")
    ).hexdigest()
    try:
        seen = set(json.loads(_SEEN.read_text(encoding="utf-8")))
    except Exception:
        seen = set()
    if key in seen:
        return True
    seen.add(key)
    try:
        _SEEN.parent.mkdir(parents=True, exist_ok=True)
        _SEEN.write_text(json.dumps(sorted(seen)[-400:]), encoding="utf-8")
    except OSError:
        pass
    return False


def report(findings) -> str:
    lines = [f"{len(findings)} claim(s) recorded this turn break a practice law. Each law "
             "carries a falsifier; fix the claim or the work and finish. Nothing is refused."]
    for f in findings:
        lines.append(f"  {f.law}  ({f.where})")
        lines.append(f"    {f.quote[:150]}")
        lines.append(f"    why: {f.why}")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path or payload.get("stop_hook_active"):
            return 0
        from .claims import check_file
        findings = [f for claims in touched(Path(path)) for f in check_file(claims)]
        if not findings or _already_reported(findings):
            return 0
        print(report(findings), file=sys.stderr)
        return 2
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
