"""The two hooks that put craft.account in the loop of a live turn.

  UserPromptSubmit  ask for the account BEFORE the answer is written, the way
                    transponder asks for a claim before the edit. Reaches the model
                    while it can still change what it is about to say.
  Stop              check what was filed, and hand back what convicts, on stderr with
                    exit 2 -- the moment the sentence can still be fixed.

WHERE ACCOUNTS GO: `.craft/accounts/<session>/<n>.json` under the repo the turn is
working in. One file per turn, numbered, never overwritten.

THE SILENCE IS REPORTED, NOT CONVICTED. A turn that files nothing is told so once, in
the same words the claims hook uses for an untouched record: it is information about the
record's own reporting bias, not a verdict on the answer. A hook that refused a turn for
not arguing would make every "yes" and "done" into paperwork, and would be switched off
within the day.

EVERY FAILURE PATH EXITS 0 IN SILENCE. Instrumentation that breaks the thing it
instruments gets removed, and then nothing is checked at all.

OFF MEANS OFF, and it must reach a session already running: `~/.craft/ACCOUNTS_OFF`
(or CRAFT_ACCOUNTS_OFF=1) is checked on every call, so the tray icon and the CLI both
reach a live session instantly. Removing the hooks from settings.json only affects
sessions that start afterwards.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SEEN = _ROOT / ".craft" / "accounts-seen.json"


def off_path() -> Path:
    return Path(os.path.expanduser("~")) / ".craft" / "ACCOUNTS_OFF"


def off() -> bool:
    """The panic switch, checked on every call so it reaches a running session."""
    v = os.getenv("CRAFT_ACCOUNTS_OFF")
    if v is not None:
        return v.strip().lower() not in ("", "0", "false", "no", "off")
    try:
        return off_path().exists()
    except OSError:
        return False


INSTRUCTION = """\
craft.account is ON. If this turn ARGUES for a conclusion, file the argument as data:

  .craft/accounts/<session-id>/<n>.json   in the repo you are working in

  {"nodes": [
    {"id": "p1", "type": "I", "ground": "producer",
     "quote": "<verbatim words from a tool result THIS turn>",
     "text": "<your reading of what that shows>"},
    {"id": "g1", "type": "I", "ground": "given",
     "quote": "<verbatim words the USER typed>"},
    {"id": "c1", "type": "I", "role": "conclusion", "strength": "limited|medium|robust",
     "text": "<the conclusion you are about to state>"},
    {"id": "r1", "type": "RA", "scheme": "deduction|verified-source|sign|example|authority|absence",
     "premises": ["p1", "g1"], "conclusion": "c1"}]}

EVERY GROUNDED PREMISE MUST QUOTE THE RECORD, and the Stop hook checks the quote
against the transcript: producer/stand-in quote tool results, given/user-surface quote
the user's messages. A quote the record does not hold convicts. Strength follows the
IPCC scale, computed: one grounded premise is limited, two or more is medium, and
robust needs a verified entailment from given premises alone. An absence warrant
convicts unless a grounded premise documents the search. A turn that argues nothing
files nothing, and that is the honest state, not a gap."""


def accounts_for(session: str, roots: list[Path]) -> list[Path]:
    out = []
    for r in roots:
        d = r / ".craft" / "accounts" / session
        if d.is_dir():
            out += sorted(d.glob("*.json"))
    return out


def repos_touched(transcript: Path) -> list[Path]:
    """Every git repo this turn wrote a file in -- where an account would have been
    filed. Same parse as claims_hook, and the same limitation: a tool call carrying a
    file_path is counted, whatever the tool was."""
    roots: set[Path] = set()
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    for line in lines[-4000:]:
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
    return sorted(roots)


def _already_reported(key: str) -> bool:
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


def user_prompt_submit(payload: dict) -> int:
    print(INSTRUCTION)
    return 0


def stop(payload: dict) -> int:
    from .account import check_file

    session = str(payload.get("session_id") or "")
    tpath = payload.get("transcript_path")
    if not session or not tpath:
        return 0
    roots = repos_touched(Path(tpath)) or [Path.cwd()]
    files = accounts_for(session, roots)
    if not files:
        return 0            # nothing filed: silence is information, not a conviction
    from .record import read
    corpus = read(Path(tpath))          # the record the grounds must quote
    findings = [f for p in files for f in check_file(p, corpus)]
    if not findings:
        return 0
    key = hashlib.sha256("|".join(f"{f.law}{f.where}{f.quote}" for f in findings)
                         .encode("utf-8", "replace")).hexdigest()
    if _already_reported(key):
        return 0
    lines = [f"{len(findings)} finding(s) in this turn's argument. Each names a law "
             "with a published root; fix the argument or the account and finish. "
             "Nothing is refused."]
    for f in findings:
        lines.append(f"  {f.law}  ({f.where})")
        if f.quote:
            lines.append(f"    {f.quote}")
        lines.append(f"    why: {f.why}")
    print("\n".join(lines), file=sys.stderr)
    return 2


HANDLERS = {"UserPromptSubmit": user_prompt_submit, "Stop": stop}


def main() -> int:
    try:
        if off():
            return 0
        payload = json.load(sys.stdin)
        if payload.get("stop_hook_active"):
            return 0
        handler = HANDLERS.get(payload.get("hook_event_name") or "")
        return handler(payload) if handler else 0
    except SystemExit:
        raise
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
