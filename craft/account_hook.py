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
the user's messages. A quote the record does not hold convicts. The deciders catch
reasoning flaws, never missing paperwork: a fabricated ground, a circular argument, a
claimed deduction that fails or exhibits nothing, an unanswered attack on support you
still rely on, an absence warrant with no documented search, support that is only
attacks on alternatives. Strength words come from the agreed scale and are otherwise
your judgment. A defeasible inference may claim a published pattern with
scheme "walton:<id>" -- its premises then fill the scheme's slots (`slot` on each
premise), and a critical question is raised as a CA on the inference carrying the
exception's slot name, judged by the same defense as any attack. A turn that argues
nothing files nothing, and that is the honest state, not a gap. A node MAY carry
`says`: a verbatim sentence of your reply it formalizes -- the Stop hook extracts the
reply's residual, the sentences no node claims, and records it beside the accounts."""


def accounts_for(session: str, roots: list[Path]) -> list[Path]:
    """Every account this session filed, wherever it filed them.

    Searching only the repos a turn WROTE TO was a real defect: a turn that argues
    without editing anything -- most answers -- filed its account in one repo and
    the hook looked in another, so the account existed and was never judged. The
    session id is the key, and the search covers the roots the turn touched plus
    the checkout this hook lives in and the working directory. Deduplicated by
    resolved path, so one account is judged once however many roots reach it."""
    seen: dict = {}
    for r in list(roots) + [_ROOT, Path.cwd()]:
        d = Path(r) / ".craft" / "accounts" / session
        if d.is_dir():
            for f in sorted(d.glob("*.json")):
                if f.name == "residual.json":
                    continue
                seen[f.resolve()] = f
    return [seen[k] for k in sorted(seen)]


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


_RESIDUAL_SEEN = _ROOT / ".craft" / "residual-seen.json"


def _residual_seen() -> set:
    try:
        return set(json.loads(_RESIDUAL_SEEN.read_text(encoding="utf-8")))
    except Exception:
        return set()


def _mark_residual_seen(paths) -> None:
    seen = _residual_seen() | {str(Path(p).resolve()) for p in paths}
    try:
        _RESIDUAL_SEEN.parent.mkdir(parents=True, exist_ok=True)
        _RESIDUAL_SEEN.write_text(json.dumps(sorted(seen)[-400:]), encoding="utf-8")
    except OSError:
        pass


def reply_text(transcript: Path) -> str:
    """The turn's final assistant prose -- the response the accounts formalize."""
    last = ""
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    for line in lines:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") != "assistant":
            continue
        parts = [b.get("text", "") for b in
                 ((rec.get("message") or {}).get("content") or [])
                 if isinstance(b, dict) and b.get("type") == "text"]
        if parts:
            last = chr(10).join(parts)
    return last


def residual(reply: str, accounts: list) -> dict:
    """The part of the response no account node claims -- hence unchecked.

    A node claims a sentence with `says`: a verbatim stretch of the reply, matched
    with the record anchor's canonical form aimed the other way -- the anchor ties
    premises to what the world said, `says` ties nodes to what the RESPONSE says.
    What is left is the residual, written beside the accounts as information, never
    a conviction: formalizing part of a reply is the honest common case, and the
    point is that the unchecked part is NAMED instead of invisible."""
    from .prose import sentences
    from .record import _canon

    claims = []
    for path in accounts:
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for n in raw.get("nodes", []):
            says = _canon(str(n.get("says") or ""))
            if says:
                claims.append((n.get("id"), says, Path(path).name,
                               str(Path(path).resolve())))
    # `says` belongs to the reply of the turn that filed it. Accounts persist in the
    # session directory, so re-checking an older account's says against a later reply
    # is a category error -- the first live run reported exactly that. Only accounts
    # not yet residual-checked contribute unmatched quotes.
    # Matching is punctuation- and case-insensitive on purpose. The first weeks ran
    # verbatim containment, and every mismatch it reported was wording drift - a
    # period falling before a parenthetical, an appended commit id - which made the
    # note indistinguishable from the one thing worth reporting: a says the reply
    # NEVER asserted. A signal that fires the same way on fraud and on a period is
    # not a signal (the owner's words, 2026-08-29). Content-word containment keeps
    # exactly the fraud case.
    def _loose(s: str) -> str:
        import re as _re
        return " ".join(_re.findall(r"[a-z0-9]+", s.lower()))

    canon_reply = _loose(_canon(reply))
    fresh = {str(Path(p).resolve()) for p in accounts} - _residual_seen()
    unmatched = [{"node": nid, "account": acc, "says": txt[:120]}
                 for nid, txt, acc, path in claims
                 if path in fresh and _loose(txt) not in canon_reply]
    sents = sentences(reply)
    covered = [x for x in sents
               if any(_canon(x) in txt or txt in _canon(x)
                      for _nid, txt, _acc, _p in claims)]
    residue = [x for x in sents if x not in covered]
    return {"sentences": len(sents), "covered": len(covered),
            "residual": residue, "unmatched_says": unmatched}


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
        # a-check-exhibits-what-it-read: finding nothing is a fact the author can
        # only use if it is said once. For a whole session on 2026-08-29 this path
        # returned 0 silently while accounts sat in a directory the displaced cwd
        # never covered, and the silence read as passes. Once per session, the
        # zero is exhibited; after that, silence means the same zero.
        key = "nothing:" + hashlib.sha256(
            f"{session}|{[str(r) for r in roots]}".encode("utf-8", "replace")
        ).hexdigest()
        if not _already_reported(key):
            print(f"account check: 0 account(s) found for this session "
                  f"(searched {len(set(map(str, list(roots) + [str(_ROOT), str(Path.cwd())])))} root(s)) "
                  "-- if this turn filed one, the search did not reach it; further "
                  "silence this session means the same zero", file=sys.stderr)
            return 2
        return 0            # nothing filed: silence is information, not a conviction
    from .record import read
    corpus = read(Path(tpath))          # the record the grounds must quote
    # each finding is carried with the account it came from: two accounts can hold
    # the same flaw at the same node id with the same message, and keying without
    # the file made the second one vanish as "already reported" -- a false negative,
    # which is worse than the noise the throttle exists to stop
    findings = [(p, f) for p in files for f in check_file(p, corpus)]
    # the residual: what the response says that no account node claims. Extracted
    # and recorded every turn; said aloud only beside convictions, because partial
    # formalization is honest and a nag gets switched off.
    summary = ""
    try:
        reply = reply_text(Path(tpath))
        if reply:
            res = residual(reply, files)
            out_path = files[0].parent / "residual.json"
            out_path.write_text(json.dumps(res, indent=1), encoding="utf-8")
            _mark_residual_seen(files)
            n_res = res["sentences"] - res["covered"]
            summary = ("\n" + f"residual: {n_res} of {res['sentences']} reply "
                       f"sentence(s) outside the formal account ({out_path.name})")
            if res["unmatched_says"]:
                summary += (f"; {len(res['unmatched_says'])} says-quote(s) the "
                            "reply does not contain")
    except Exception:
        pass
    if not findings:
        # A clean verdict is reported too, once per turn. Silence on a pass is why
        # "the harness checked this" could not be said without running the checker
        # by hand: an author cannot tell a pass from a hook that never looked.
        n_nodes = 0
        for p in files:
            try:
                n_nodes += len(json.loads(Path(p).read_text(encoding="utf-8")).get("nodes", []))
            except (OSError, ValueError):
                pass
        verdict = (f"{len(files)} account(s), {n_nodes} node(s) checked, "
                   "no decider convicts." + summary)
        if not _already_reported("pass:" + hashlib.sha256(
                verdict.encode("utf-8", "replace")).hexdigest()):
            print(verdict, file=sys.stderr)
            return 2
        return 0
    # Throttle PER FINDING, not per set. Hashing the whole set meant one new account
    # changed the hash and every standing conviction returned as news -- eleven
    # findings reported for a turn that produced four. A hook that repeats yesterday's
    # convictions is one nobody reads, which is the failure a throttle exists to stop.
    fresh, carried = [], 0
    for path, f in findings:
        key = hashlib.sha256(
            f"{Path(path).name}|{f.law}|{f.where}|{f.quote}|{f.why}"
            .encode("utf-8", "replace")).hexdigest()
        if _already_reported(key):
            carried += 1
        else:
            fresh.append((Path(path).name, f))
    if not fresh:
        return 0
    lines = [f"{len(fresh)} finding(s) in this turn's argument. Each names a law "
             "with a published root; fix the argument or the account and finish. "
             "Nothing is refused."]
    for acc, f in fresh:
        lines.append(f"  {f.law}  ({acc} {f.where})")
        if f.quote:
            lines.append(f"    {f.quote}")
        lines.append(f"    why: {f.why}")
    if carried:
        # standing convictions are counted, never re-listed: still true, already said
        lines.append(f"  ({carried} earlier finding(s) still standing, reported once "
                     "when they appeared)")
    print("\n".join(lines) + summary, file=sys.stderr)
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
