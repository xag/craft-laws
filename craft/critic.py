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
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
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


def critic_prompt(pairs: list[dict]) -> str:
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
        'words>"},\n'
        '  {"id": "r1", "type": "RA", "scheme": '
        '"verified-source|sign|example|authority|absence", "premises": ["g1"], '
        '"conclusion": "c1"}]}\n'
        "Rules: every `says` and every `quote` must be copied verbatim from the "
        "turn shown; do not invent premises the reply does not state. When the "
        "reply rests on tool output - a search, a listing, a test run - ground "
        "that premise {\"ground\": \"producer\"} and copy its quote verbatim "
        "from the TOOLS excerpt - and a quote must come from WITHIN one tool "
        "result, never across a '--- next tool result ---' line, because such "
        "spans exist only in the excerpt, not in the record; only when the "
        "needed output is absent from the "
        "excerpt write the premise WITHOUT a ground or quote (an unanchored "
        "premise is honest; a fabricated quote is not). Mark every account "
        "{\"reconstruction\": true}. Answer with a JSON array of these account "
        "objects and nothing else.\n\n"
        + turns)


def cli_runner(prompt: str) -> str:
    import subprocess
    env = dict(os.environ, CRAFT_ACCOUNTS_OFF="1")
    # the prompt travels on stdin: a digest-sized argv element trips Windows'
    # command-line length limit (WinError 206, seen on the first live run)
    done = subprocess.run(["claude", "-p"], input=prompt, capture_output=True,
                          text=True, timeout=600, encoding="utf-8",
                          errors="replace", env=env)
    if done.returncode != 0:
        raise RuntimeError(f"claude -p failed ({done.returncode}): "
                           f"{(done.stderr or '')[:200]}")
    return done.stdout or ""


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
        p.write_text(json.dumps(a, indent=1), encoding="utf-8")
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

    runner = runner or cli_runner
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
    text = runner(critic_prompt(window))
    start, end = text.find("["), text.rfind("]")
    try:
        accounts = json.loads(text[start:end + 1]) if 0 <= start <= end else []
    except ValueError:
        accounts = []
    written = []
    out_dir.mkdir(parents=True, exist_ok=True)
    k = len(list(out_dir.glob("critic-live-*.json")))
    last_turn = len(window) - 1
    for a in accounts:
        if not isinstance(a, dict) or not a.get("nodes"):
            continue
        if a.get("turn") != last_turn:
            continue            # context turns are shown, not re-judged
        a["reconstruction"] = True
        f = out_dir / f"critic-live-{k}.json"
        k += 1
        f.write_text(json.dumps(a, indent=1), encoding="utf-8")
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
    ns = ap.parse_args(argv)
    out = Path(ns.out) if ns.out else Path.cwd() / ".craft" / "accounts" / ns.session
    n = run(Path(ns.transcript), ns.session, out)
    print(f"critic: {n} finding(s)" if n else "critic: nothing to say")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
