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

EACH JUDGED TURN RECORDS ONE FLIGHT TAPE under this checkout's .craft/flight: the
payload is the call; the transcript, the filed accounts, the seen-state and the
critic's model call all cross as effects of the craft.flight boundary. CRAFT_FLIGHT=0
opts out; a recorder failure is as silent as every other failure here.

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

from . import flight

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
    for r in list(roots) + [_ROOT, Path(flight.working_dir())]:
        d = Path(r) / ".craft" / "accounts" / session
        if flight.is_dir(d):
            for f in (Path(x) for x in flight.listing(d, "*.json")):
                # the critic's own products live beside author-filed accounts and
                # are judged at their own firing point - re-reading them here made
                # yesterday's reconstructions convict as today's filed argument
                if (f.name == "residual.json" or f.name == "adjudications.jsonl"
                        or f.name.startswith("critic-")):
                    continue
                seen[f.resolve()] = f
    return [seen[k] for k in sorted(seen)]


def repos_touched(transcript: Path) -> list[Path]:
    """Every git repo this turn wrote a file in -- where an account would have been
    filed. Same parse as claims_hook, and the same limitation: a tool call carrying a
    file_path is counted, whatever the tool was."""
    roots: set[Path] = set()
    try:
        lines = flight.transcript_text(transcript).splitlines()
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
            root = flight.git_root(Path(str(path)).parent)
            if root:
                roots.add(Path(root))
    return sorted(roots)


def _already_reported(key: str) -> bool:
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


_RESIDUAL_SEEN = _ROOT / ".craft" / "residual-seen.json"


def _residual_seen() -> set:
    try:
        return set(json.loads(flight.file_text(_RESIDUAL_SEEN)))
    except Exception:
        return set()


def _mark_residual_seen(paths) -> None:
    seen = _residual_seen() | {str(Path(p).resolve()) for p in paths}
    try:
        _RESIDUAL_SEEN.parent.mkdir(parents=True, exist_ok=True)
        flight.write_text(_RESIDUAL_SEEN, json.dumps(sorted(seen)[-400:]))
    except OSError:
        pass


def reply_text(transcript: Path) -> str:
    """The turn's final assistant prose -- the response the accounts formalize."""
    last = ""
    try:
        lines = flight.transcript_text(transcript).splitlines()
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
            raw = json.loads(flight.file_text(path))
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
    """Silent. No instruction is injected (the 2026-08-30 measurement: inline
    formalization taxed every answer and repaired none), and no critique is
    drained here either -- the critic couriers its findings as transponder
    direct mail, which the transponder's own hook delivers at every seam. One
    substrate for pushed content, owned where it lives."""
    return 0


def _conviction_contract(session: str) -> str:
    """The tail of every conviction handed back: correct yourself or dispute, and
    either way the USER HEARS NOTHING ABOUT THE CONVICTION. It is between the
    author and the record. The turns that argued back in the reply proved the
    failure mode this closes: the person reads a rebuttal of a message they never
    saw, which is pure noise -- and the rebuttal itself evaporates with the
    transcript, measuring nothing. The dispute file is the channel that persists:
    false positives filed there are what the checker's own defect rate is computed
    from (a critique reconstructs from a bounded excerpt, and may itself be at
    fault). And the visible move, when a finding is right, is SELF-correction --
    the sentence fixed as if the author had caught it, because to the user that is
    exactly what happened."""
    return ("If a finding is right, correct what you told the user - restate the "
            "sentence as it should have been said, the way you would fix any "
            "error you caught yourself. If it is a false positive, file that as "
            "data and move on:\n"
            f"  uv run --no-sync --directory {_ROOT.as_posix()} python -m "
            f"craft.disputes --law <law> --where \"<where>\" "
            f"--why \"<one line>\" --session {session or '<session-id>'}\n"
            "Do NOT re-run searches or re-verify work the record already shows. "
            "Never RESPOND to the conviction in the conversation: no mention of "
            "it, no defense, no acknowledgment that a check ran. The user never "
            "saw the conviction; to them every word about it is noise, and a "
            "correction that cites its trigger is a response, not a correction.")


def _live_critic(session: str, tpath) -> int:
    """Spawn, and only spawn. The critic judges the turn that just ended,
    detached (measured 2026-09-01: 135-202s a critique, nothing synchronous
    survives), and DELIVERS ITS OWN FINDINGS as transponder direct mail -- the
    estate's one pushed channel, drained by its hook at every tool call, so a
    finding reaches the session mid-turn, at the next action after it exists.
    This hook owns no delivery: one substrate, the courier's (the owner's
    2026-09-01 correction -- the wheel existed, use it)."""
    out = Path(flight.working_dir()) / ".craft" / "accounts" / session
    _spawn_critic(session, tpath, out)
    return 0


def spawn_critic(session: str, tpath) -> None:
    """The argument review, started detached. Public because craft.review owns the
    question of WHICH reviews run; this module owns what this one is."""
    out = Path(flight.working_dir()) / ".craft" / "accounts" / session
    _spawn_critic(session, tpath, out)


def _spawn_critic(session: str, tpath, out: Path) -> None:
    """This turn's critic, started and left. The flags are NOT this repo's business:
    courier.spawn owns the windowless rule, having been given it by transponder's
    relaunch.py, which had it from being bitten. This module's own attempt paired
    CREATE_NO_WINDOW with DETACHED_PROCESS -- mutually exclusive, silently ignored --
    and flashed a console every turn until 2026-09-01."""
    try:
        from courier import spawn
    except ImportError:
        return
    spawn.detach(["-m", "craft.critic", str(tpath), session,
                  "--out", str(out), "--live"],
                 cwd=str(_ROOT),
                 env=dict(os.environ, CRAFT_ACCOUNTS_OFF="1"))


def stop(payload: dict) -> int:
    from .account import check_file

    session = str(payload.get("session_id") or "")
    tpath = payload.get("transcript_path")
    if not session or not tpath:
        return 0
    roots = repos_touched(Path(tpath)) or [Path(flight.working_dir())]
    files = accounts_for(session, roots)
    if not files:
        # Nothing filed is the NORM since 2026-08-30: the author is no longer
        # instructed to file, so a zero here is not a dead instrument. The live
        # critic below judges the turn instead.
        return _live_critic(session, tpath)
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
            flight.write_text(out_path, json.dumps(res, indent=1))
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
        # A clean pass is SILENT since the silent-critic redesign - and it must
        # fall through to the critic, never return early: on 2026-08-30 the
        # ever-changing residual summary made this pass line "fresh" every turn,
        # its exit 2 short-circuited the critic, and a planted test error sailed
        # past a critic that never ran.
        return _live_critic(session, tpath)
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
        return _live_critic(session, tpath)
    lines = [f"{len(fresh)} finding(s) in this turn's argument. Each names a law "
             "with a published root. Nothing is refused."]
    for acc, f in fresh:
        lines.append(f"  {f.law}  ({acc} {f.where})")
        if f.quote:
            lines.append(f"    {f.quote}")
        lines.append(f"    why: {f.why}")
    if carried:
        # standing convictions are counted, never re-listed: still true, already said
        lines.append(f"  ({carried} earlier finding(s) still standing, reported once "
                     "when they appeared)")
    print("\n".join(lines) + summary + "\n" + _conviction_contract(session),
          file=sys.stderr)
    return 2


def main() -> int:
    """Dispatches by NAME through the module, never through a dict built at import:
    the recorder patches module attributes, and a dict holding the original function
    objects would route every live turn around the wrapper it just installed."""
    try:
        if off():
            return 0
        payload = json.load(sys.stdin)
        if payload.get("stop_hook_active"):
            return 0
        event = payload.get("hook_event_name") or ""
        if event == "Stop":
            # one tape per judged turn; the prompt-submit lane is silent and records
            # nothing worth a file
            flight.record(sys.modules[__name__], "account")
            return stop(payload)
        if event == "UserPromptSubmit":
            return user_prompt_submit(payload)
        return 0
    except SystemExit:
        raise
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
