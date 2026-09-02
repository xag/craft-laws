"""The silent critic: the account lane with the responding agent left alone.

The first design injected the account instruction into every turn of the graded
session, and the 2026-08-30 analysis of a full live session measured what that
cost: 31 injections (~15k tokens of identical text), 36 of 234 tool calls spent
authoring and repairing account files, a style contamination bad enough to need a
standing rule, and every live conviction an error OF the inline formalization -
while the independent judge ruled 59 of the 106 inline readings unsupported. The
per-turn instruction bought near-zero answer repair and taxed every answer.

This module is the replacement the owner specified: the responding agent sees
nothing. At session end, code spawns a critic - a fresh `claude -p` process with
the account hook switched off - which reads a bounded digest of the session's
turns, RECONSTRUCTS the arguments as accounts (marked as reconstruction, its
conclusions quoting the reply's own sentences so a straw man is checkable), and
the mechanical deciders then judge the reconstruction against the full transcript
corpus. If nothing convicts, nothing is said and nothing but the accounts is
written: the session is left undisturbed. If something convicts, the findings are
written to `critique.md` beside the accounts, where the owner or the next session
reads them.

Independence note (same as the adjudicator's): the critic's context never held
the authoring conversation - it sees the digest and nothing else, whatever
weights it runs on.

    python -m craft.critic <transcript.jsonl> <session-id>    # run by hand
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from . import flight

MAX_TURN_CHARS = 1500      # each side of a turn is clipped to this (whole-session)
MAX_TOOL_CHARS = 2000      # per-turn tool-result excerpt (whole-session)
LIVE_TURN_CHARS = 6000     # the live critic sees the last turn nearly whole
LIVE_TOOL_CHARS = 8000     # and a wide excerpt of its tool results
MIN_REPLY_CHARS = 200      # below this a reply is an acknowledgement, not an argument
TOOL_SEAM = "\n--- next tool result ---\n"
MAX_DIGEST_CHARS = 40_000  # the whole digest is clipped to this
CRITIC_DIR_NOTE = "critic"  # accounts written as critic-<n>.json


def _join_tools(tools: list, budget: int) -> str:
    """Join tool results with a visible seam and truncate at result boundaries,
    never mid-result: a quote spanning a seam or a cut edge is text no record
    holds, and one convicted an innocent reconstruction on 2026-08-30."""
    kept: list = []
    room = budget
    for t in reversed(tools):
        if len(t) + len(TOOL_SEAM) > room:
            break
        kept.insert(0, t)
        room -= len(t) + len(TOOL_SEAM)
    if not kept and tools:
        return tools[-1][-budget:]
    return TOOL_SEAM.join(kept)


def digest(transcript: Path, max_turn_chars: int = MAX_TURN_CHARS,
           max_tool_chars: int = MAX_TOOL_CHARS) -> list[dict]:
    """One dict per turn: the user's words, an excerpt of the turn's tool results,
    and the reply (all assistant text until the next user message, merged).

    The tool excerpt exists because its absence manufactured convictions: the
    critic was forbidden to invent quotes for tool output it could not see, while
    the absence law demands a grounded search - so every true nothing-was-found
    conclusion convicted, deterministically (seen live 2026-08-30). The excerpt
    keeps the tail of the turn's tool text, where the searches a reply cites
    usually sit; quotes copied from it anchor against the full corpus."""
    pairs: list[dict] = []
    cur: dict | None = None

    def close():
        nonlocal cur
        if cur and cur["reply"]:
            pairs.append({
                "user": cur["user"][:max_turn_chars],
                "tools": _join_tools(cur["tools"], max_tool_chars),
                "reply": "\n".join(cur["reply"]).strip()[:max_turn_chars]})
        cur = None

    try:
        lines = flight.transcript_text(transcript).splitlines()
    except OSError:
        return []
    for line in lines:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") == "user":
            c = (rec.get("message") or {}).get("content")
            if isinstance(c, str) and c.strip():
                close()
                cur = {"user": c, "tools": [], "reply": []}
            elif isinstance(c, list) and cur is not None:
                for b in c:
                    if not (isinstance(b, dict) and b.get("type") == "tool_result"):
                        continue
                    cc = b.get("content")
                    if isinstance(cc, str):
                        cur["tools"].append(cc)
                    elif isinstance(cc, list):
                        cur["tools"].append(" ".join(
                            str(x.get("text", "")) for x in cc if isinstance(x, dict)))
        elif rec.get("type") == "assistant" and cur is not None:
            parts = [b.get("text", "") for b in (rec.get("message") or {}).get("content") or []
                     if isinstance(b, dict) and b.get("type") == "text"]
            joined = "\n".join(x for x in parts if x).strip()
            if joined:
                cur["reply"].append(joined)
    close()
    total = 0
    kept = []
    for pr in reversed(pairs):          # newest turns are kept when space runs out
        total += len(pr["user"]) + len(pr["reply"]) + len(pr["tools"])
        if total > MAX_DIGEST_CHARS:
            break
        kept.append(pr)
    return list(reversed(kept))


def critic_prompt(pairs: list[dict], judge_turn: int | None = None) -> str:
    turns = "\n\n".join(
        f"TURN {i}:\nUSER: {p['user']}\n"
        f"TOOLS (excerpt of this turn's tool results): {p.get('tools') or '(none)'}\n"
        f"REPLY: {p['reply']}"
        for i, p in enumerate(pairs))
    return (
        "You are a critic reconstructing the arguments of a finished assistant "
        "session. You did not write these replies. For each turn whose REPLY "
        "argues for a conclusion (many turns argue nothing - skip those), "
        "reconstruct the argument as one JSON account:\n"
        '{"turn": <n>, "nodes": [\n'
        '  {"id": "g1", "type": "I", "ground": "given", "quote": "<verbatim words '
        "from the USER text>\"},\n"
        '  {"id": "c1", "type": "I", "role": "conclusion", "says": "<one verbatim '
        'sentence copied from the REPLY>", "text": "<the conclusion in your '
        'words>", "names": ["<short name the sentence uses for a specific thing>"]},\n'
        '  {"id": "d1", "type": "I", "defines": "<one of those names>", "quote": '
        '"<verbatim REPLY sentence stating what that name refers to>"},\n'
        '  {"id": "r1", "type": "RA", "scheme": '
        '"verified-source|sign|example|authority|absence", "premises": ["g1"], '
        '"conclusion": "c1"}]}\n'
        "Rules: every `says` and every `quote` must be copied verbatim from the "
        "turn shown; do not invent premises the reply does not state. On each "
        "conclusion, transcribe `names`: the short names — four words or fewer, "
        "articles included, copied verbatim — the `says` sentence uses to refer "
        "to specific things (a component, a mechanism, a concept) -- names that "
        "designate: the phrase could serve as the thing's title. Not counting or "
        "pointing phrases ('the other two', 'that second one', 'tonight's build', 'my earlier "
        "suggestion'), which refer without naming. Where the "
        "REPLY itself states what one of those names refers to, add a node "
        "carrying `defines` (the name) and `quote` (that REPLY sentence, "
        "verbatim; for definition nodes only, the quote comes from the REPLY). "
        "Transcribe what is there: a sentence using no such names carries no "
        "`names` field. When the "
        "reply rests on tool output - a search, a listing, a test run - ground "
        "that premise {\"ground\": \"producer\"} and copy its quote verbatim "
        "from the TOOLS excerpt - and a quote must come from WITHIN one tool "
        "result, never across a '--- next tool result ---' line, because such "
        "spans exist only in the excerpt, not in the record; only when the "
        "needed output is absent from the "
        "excerpt write the premise WITHOUT a ground or quote (an unanchored "
        "premise is honest; a fabricated quote is not). Mark every account "
        "{\"reconstruction\": true}. Answer with a JSON array of these account "
        "objects and nothing else."
        + (f" Reconstruct ONLY turn {judge_turn}; the earlier turns are context "
           "for its premises, not subjects - write no account for them."
           if judge_turn is not None else "")
        + "\n\n"
        + turns)


LIVE_MODEL = "haiku"       # the drawing task is transcription; the small model does it
LIVE_TIMEOUT_S = 240       # generous: the critic is detached, the cap only stops runaways
                           # (measured 2026-09-01: 135-202s on the small model, floor 6s)


def deliver(session: str, lines: list) -> None:
    """Hand the findings to the courier, which puts them in front of the session at its
    next seam. This module owns no delivery and no dedupe and no window flags: a
    producer's job is the judgment, and the courier's is getting it read. A courier that
    is not installed means no delivery, silently -- it must never kill a critic that has
    already written its accounts."""
    try:
        from courier import mail
    except ImportError:
        return
    mail.post(session, "craft.critic",
              "the critic judged your previous reply (produced alongside it). Each "
              "line names a law with a published root. Nothing is refused.\n  "
              + "\n  ".join(lines) + "\n"
              "If a finding is right, correct what you told the user - restate the "
              "sentence as it should have been said, the way you would fix any error "
              "you caught yourself. If it is a false positive, file that as data and "
              "move on:\n"
              "  uv run --no-sync --directory C:/Users/trans/Projects/craft-laws "
              "python -m craft.disputes --law <law> --where \"<where>\" "
              f"--why \"<one line>\" --session {session}\n"
              "Never RESPOND to this in the conversation: no mention of it, no "
              "defense. The user never saw it; a correction that cites its trigger is "
              "a response, not a correction.")


def _report_unparsed(session: str, raw) -> None:
    try:
        from courier import mail
    except ImportError:
        return
    mail.post_once(session, "craft.critic",
                   "the critic ran on your previous reply and produced no accounts it "
                   f"could parse -- its raw reply is at {raw}. Your replies are NOT "
                   "being reviewed for reasoning until this is fixed; say so to the "
                   "user once, then carry on.", key="unparsed")


def cli_runner(prompt: str, model: str | None = None, timeout: int = 600) -> str:
    import subprocess
    env = dict(os.environ, CRAFT_ACCOUNTS_OFF="1")
    # the prompt travels on stdin: a digest-sized argv element trips Windows'
    # command-line length limit (WinError 206, seen on the first live run).
    # No settings sources: the user's SessionStart/UserPromptSubmit hooks inject
    # their own context into this one-shot session, and the small model answered
    # THAT instead of the prompt -- from 2026-09-01 10:07, when the global hooks
    # went in, to 2026-09-02, every critique came back as an acknowledgement of a
    # checkout protocol, held no "[", and was filed as a clean turn. `--bare`
    # would also do it but never reads OAuth, which is how this machine is signed in.
    cmd = (["claude", "-p", "--setting-sources", ""]
           + (["--model", model] if model else []))
    done = subprocess.run(cmd, input=prompt, capture_output=True,
                          text=True, timeout=timeout, encoding="utf-8",
                          errors="replace", env=env)
    if done.returncode != 0:
        raise RuntimeError(f"claude -p failed ({done.returncode}): "
                           f"{(done.stderr or '')[:200]}")
    return done.stdout or ""


def live_runner(prompt: str) -> str:
    """The live path's runner: the small model, on a clock. Timeout raises, and the
    caller's fallback is the detached spawn -- deferred beats blocked, lost is neither."""
    return cli_runner(prompt, model=LIVE_MODEL, timeout=LIVE_TIMEOUT_S)


def run(transcript: Path, session: str, out_dir: Path, runner=None) -> int:
    """The whole pass: digest -> critic -> accounts on disk -> deciders -> a
    critique file only when something convicts. Returns the finding count."""
    from .account import check_file
    from .record import read

    runner = runner or cli_runner
    pairs = digest(transcript)
    if not pairs:
        return 0
    text = runner(critic_prompt(pairs))
    start, end = text.find("["), text.rfind("]")
    try:
        accounts = json.loads(text[start:end + 1]) if 0 <= start <= end else []
    except ValueError:
        accounts = []
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for a in accounts:
        if not isinstance(a, dict) or not a.get("nodes"):
            continue
        a["reconstruction"] = True
        p = out_dir / f"critic-{a.get('turn', len(written))}.json"
        flight.write_text(p, json.dumps(a, indent=1))
        written.append(p)
    if not written:
        return 0
    corpus = read(transcript)
    findings = [(p.name, f) for p in written for f in check_file(p, corpus)]
    if findings:
        lines = [f"# Critique of session {session}",
                 "",
                 f"{len(written)} reconstructed account(s), "
                 f"{len(findings)} finding(s). Each names a law with a published "
                 "root; the reconstruction may also be at fault - it is marked as "
                 "reconstruction and judged by the same deciders.",
                 ""]
        for name, f in findings:
            lines.append(f"- {f.law} ({name} {f.where}): {f.why}")
        (out_dir / "critique.md").write_text("\n".join(lines) + "\n",
                                             encoding="utf-8")
    return len(findings)


def criticize_turn(transcript: Path, session: str, out_dir: Path,
                   runner=None) -> list[str]:
    """The live critic: the LAST turn only, run at Stop, silent when clean.

    This is the owner's 2026-08-30 correction of the session-end design: a
    critique nobody reads is waste, and a session-start pointer criticizes an
    agent that can no longer correct anything. The criticism lands in the turn
    it criticizes - the hook feeds the returned lines back to the model, which
    corrects itself while the owner is still reading the reply. Clean turns
    return [] and the agent never learns the critic exists.
    """
    from .account import check_file
    from .record import read

    runner = runner or live_runner
    pairs = digest(transcript, max_turn_chars=LIVE_TURN_CHARS,
                   max_tool_chars=LIVE_TOOL_CHARS)
    if not pairs:
        return []
    last = pairs[-1]
    if len(last["reply"]) < MIN_REPLY_CHARS:
        return []               # acknowledgements are not arguments
    # the judged turn arrives with up to two turns of context before it: a reply
    # citing evidence from two turns back was convicted of an undocumented
    # search when the critic could only see one turn (2026-08-30)
    window = pairs[-3:]
    text = runner(critic_prompt(window, judge_turn=len(window) - 1))
    start, end = text.find("["), text.rfind("]")
    try:
        accounts = json.loads(text[start:end + 1]) if 0 <= start <= end else None
    except ValueError:
        accounts = None
    out_dir.mkdir(parents=True, exist_ok=True)
    k = len(flight.listing(out_dir, "critic-live-*.json"))
    if accounts is None:
        # A reply with no JSON array in it is the critic FAILING, not a clean
        # turn; the two read the same from the session and for a day nobody could
        # tell them apart (a-check-reports-what-it-could-not-judge). The raw reply
        # goes on disk beside the accounts, and the session hears it once.
        flight.write_text(out_dir / f"critic-live-{k}.unparsed.txt", text)
        _report_unparsed(session, out_dir / f"critic-live-{k}.unparsed.txt")
        return []
    written = []
    last_turn = len(window) - 1
    for a in accounts:
        if not isinstance(a, dict) or not a.get("nodes"):
            continue
        if a.get("turn") != last_turn:
            continue            # context turns are shown, not re-judged
        a["reconstruction"] = True
        f = out_dir / f"critic-live-{k}.json"
        k += 1
        flight.write_text(f, json.dumps(a, indent=1))
        written.append(f)
    if not written:
        return []
    corpus = read(transcript)
    return [f"{fi.law} ({f.name} {fi.where}): {fi.why}"
            for f in written for fi in check_file(f, corpus)]


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.critic",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("transcript")
    ap.add_argument("session")
    ap.add_argument("--out", default=None,
                    help="accounts directory (default: cwd/.craft/accounts/<session>)")
    ap.add_argument("--live", action="store_true",
                    help="criticize the LAST turn only and courier the findings to the "
                         "session as transponder direct mail")
    ns = ap.parse_args(argv)
    out = Path(ns.out) if ns.out else Path.cwd() / ".craft" / "accounts" / ns.session
    if ns.live:
        # Detached (the generation runs minutes; nothing synchronous survives it,
        # measured 2026-09-01) and delivered on the estate's one push channel: a
        # transponder direct message lands at the session's next tool call, mid-turn.
        # Clean turns send nothing.
        lines = criticize_turn(Path(ns.transcript), ns.session, out)
        if lines:
            deliver(ns.session, lines)
        return 0
    n = run(Path(ns.transcript), ns.session, out)
    print(f"critic: {n} finding(s)" if n else "critic: nothing to say")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
