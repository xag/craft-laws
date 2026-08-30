"""The Stop hook: run the claim deciders before the turn is handed back.

`craft.claims` is the check, and it has been all along: five code deciders over the claims
a session records, each reading a field and never a word of prose. Its own docstring says the move — "give
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

Each working turn records one flight tape under this checkout's .craft/flight: the payload
is the call, everything read and written crosses as effects of the craft.flight boundary.
CRAFT_FLIGHT=0 opts out; a recorder failure is as silent as every other failure here.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from . import flight

_ROOT = Path(__file__).resolve().parents[1]
_SEEN = _ROOT / ".craft" / "seen.json"


def touched(transcript: Path) -> list[Path]:
    """The claims files of every repository this turn wrote to.

    A turn edits several checkouts, and the claim it should have recorded belongs in the one
    the work was in. Reading only the current directory's file would miss exactly the claims
    a cross-repo turn makes."""
    roots: set[Path] = set()
    for line in flight.transcript_text(transcript).splitlines()[-4000:]:
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
            root = flight.git_root(Path(str(path)).parent)
            if root:
                roots.add(Path(root))
    return sorted(r / "claims.jsonl" for r in roots
                  if flight.exists(r / "claims.jsonl"))


def silent_repos(transcript: Path) -> list[Path]:
    """The repositories this turn WROTE TO whose claims file the turn never touched.

    The intake debt's diff half, mechanized: the deciders convict filed claims, and
    until this function nothing saw the turn whose work never reached the record at
    all — self-report catches the part already noticed. The diff IS data: the same
    transcript parse that finds the claims files also shows which repositories got
    writes, and whether any tool call touched their claims.jsonl (a file_path ending
    in it, or a shell command naming it — claims are filed both ways). A command
    that names claims.jsonl without naming a repository clears EVERY written repo:
    under-reporting beats a false alarm, because a noisy informant is one that gets
    switched off. A repo written-to with its record untouched is not a conviction —
    a turn may be mid-work — it is the record's reporting bias, measured per turn
    and said to the author while the sentence can still be fixed."""
    wrote: set[Path] = set()
    filed: set[Path] = set()
    cleared_all = False
    for line in flight.transcript_text(transcript).splitlines()[-4000:]:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") != "assistant":
            continue
        for block in (rec.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            inp = block.get("input") or {}
            path = inp.get("file_path")
            if path:
                root = flight.git_root(Path(str(path)).parent)
                if root:
                    wrote.add(Path(root))
                    if str(path).replace("\\", "/").endswith("claims.jsonl"):
                        filed.add(Path(root))
            cmd = str(inp.get("command") or "")
            if "claims.jsonl" in cmd:
                named = False
                norm = cmd.replace("\\", "/")
                for repo in list(wrote):
                    if str(repo).replace("\\", "/") in norm or repo.name in cmd:
                        filed.add(repo)
                        named = True
                if not named:
                    cleared_all = True
    if cleared_all:
        return []
    return sorted(r for r in wrote - filed if flight.exists(r / "claims.jsonl"))


def _already_reported(findings) -> bool:
    key = hashlib.sha256(
        "|".join(f"{f.law}{f.where}{f.quote}" for f in findings).encode("utf-8", "replace")
    ).hexdigest()
    try:
        seen = set(json.loads(flight.file_text(_SEEN)))
    except Exception:
        seen = set()
    if key in seen:
        return True
    seen.add(key)
    try:
        _SEEN.parent.mkdir(parents=True, exist_ok=True)
        flight.write_text(_SEEN, json.dumps(sorted(seen)[-400:]))
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


def _silence_note(repos: list[Path]) -> str:
    names = ", ".join(r.name for r in repos)
    return ("\n".join([
        f"This turn wrote files in {names} and touched no claims record there.",
        "If the turn's sentence reports work finished, fixed, diagnosed or a "
        "workaround, the record is silent exactly where the work happened — "
        "a-corpus-of-reports-carries-its-reporting-bias, and the conviction "
        "statistics are drawn only from what gets filed. File the claim, or say "
        "the work is mid-flight. This is information, not a conviction; nothing "
        "is refused."]))


def run(payload: dict) -> int:
    """One turn's check, whole. Public and called through the module so the recorder
    wraps it: the payload is the recorded call, and everything the deciders read
    arrives as effects (craft.flight is the boundary)."""
    path = payload.get("transcript_path")
    if not path or payload.get("stop_hook_active"):
        return 0
    from .claims import ClaimFinding, check_file
    findings = [f for claims in touched(Path(path)) for f in check_file(claims)]
    silent = silent_repos(Path(path))
    # the silence rides the same once-per-content throttle as the findings: a
    # repo the author was told about, and chose to leave silent, is not nagged —
    # a noisy informant is one that gets switched off
    notes = []
    if silent:
        marker = [ClaimFinding(law="intake-silence", quote="",
                               where="|".join(sorted(r.name for r in silent)),
                               why="")]
        if not _already_reported(marker):
            notes.append(_silence_note(silent))
    if findings and not _already_reported(findings):
        notes.insert(0, report(findings))
    if not notes:
        return 0
    print("\n\n".join(notes), file=sys.stderr)
    return 2


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        # a re-fire (stop_hook_active) and a payload with no transcript both do no
        # work; a tape of nothing is noise in the pile the tapes exist to be read as
        if payload.get("transcript_path") and not payload.get("stop_hook_active"):
            flight.record(sys.modules[__name__], "claims")
        return run(payload)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
