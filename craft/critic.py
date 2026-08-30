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

MAX_TURN_CHARS = 1500      # each side of a turn is clipped to this
MAX_DIGEST_CHARS = 40_000  # the whole digest is clipped to this
CRITIC_DIR_NOTE = "critic"  # accounts written as critic-<n>.json


def digest(transcript: Path) -> list[dict]:
    """(user, reply) pairs for the session's turns, bounded. Tool traffic is left
    out on purpose: the deciders re-anchor quotes against the full corpus later,
    so the critic needs the dialogue, not the record."""
    pairs: list[dict] = []
    user_text = None
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
                user_text = c
        elif rec.get("type") == "assistant":
            parts = [b.get("text", "") for b in (rec.get("message") or {}).get("content") or []
                     if isinstance(b, dict) and b.get("type") == "text"]
            reply = "\n".join(p for p in parts if p).strip()
            if reply:
                pairs.append({"user": (user_text or "")[:MAX_TURN_CHARS],
                              "reply": reply[:MAX_TURN_CHARS]})
                user_text = None
    total = 0
    kept = []
    for p in reversed(pairs):           # newest turns are kept when space runs out
        total += len(p["user"]) + len(p["reply"])
        if total > MAX_DIGEST_CHARS:
            break
        kept.append(p)
    return list(reversed(kept))


def critic_prompt(pairs: list[dict]) -> str:
    turns = "\n\n".join(
        f"TURN {i}:\nUSER: {p['user']}\nREPLY: {p['reply']}"
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
        "turn shown; do not invent premises the reply does not state; if the "
        "reply cites tool output you cannot see, write the premise as an I node "
        "WITHOUT a ground or quote (an unanchored premise is honest; a fabricated "
        "quote is not). Mark every account {\"reconstruction\": true}. Answer "
        "with a JSON array of these account objects and nothing else.\n\n"
        + turns)


def cli_runner(prompt: str) -> str:
    import subprocess
    env = dict(os.environ, CRAFT_ACCOUNTS_OFF="1")
    done = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                          timeout=600, encoding="utf-8", errors="replace", env=env)
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
