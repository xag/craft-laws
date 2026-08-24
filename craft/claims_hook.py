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
never what they check. And a word list once judged prose against a law directly — wrong seven
times in eight, because the difference between the sentence a law forbids and the sentence it
demands is meaning, which words do not carry. The claim-shape radar below is the third shape
and neither of those: it PROPOSES and never judges. It fires only when the record is already
silent where the turn worked, it names the sentence that looks claim-shaped so the author can
file the claim or reword to what was observed, and every conviction still happens in code over
the filed record. A false positive here costs one line of information; a false positive in a
judge costs the practice.

Once per set of findings, by hash: a turn that has already been told, and chose, is not told
again. Every failure path exits 0 in silence, because instrumentation that breaks the thing
it instruments gets removed, and then nothing is checked at all.
"""

from __future__ import annotations

import hashlib
import json
import re
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
    for line in transcript.read_text(encoding="utf-8",
                                     errors="replace").splitlines()[-4000:]:
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
                here = Path(str(path)).parent
                for parent in [here, *here.parents]:
                    if (parent / ".git").exists():
                        wrote.add(parent)
                        if str(path).replace("\\", "/").endswith("claims.jsonl"):
                            filed.add(parent)
                        break
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
    return sorted(r for r in wrote - filed if (r / "claims.jsonl").exists())


# One pattern per claim kind, tuned for RECALL: each is the word-shape a claim of that
# kind tends to wear in a handback. They are word-shapes and nothing more — the earlier
# word list that JUDGED prose against a law was wrong seven times in eight, and the
# lesson is recorded at the-deciders-run-by-hand. These never judge: a hit only routes
# a sentence toward the record, where the deciders read data.
_CLAIM_SHAPES = (
    ("done", re.compile(
        r"\b(?:done|completed?|finished|shipped|deployed|is live|works now|all green"
        r"|tests? (?:are )?(?:green|pass(?:ing|ed)?)|pushed)\b", re.I)),
    ("fixed", re.compile(r"\bfix(?:ed|es)?\b", re.I)),
    ("diagnosis", re.compile(
        r"\b(?:the (?:root )?cause|the culprit|turn(?:s|ed) out|because the)\b", re.I)),
    ("detour", re.compile(
        r"\b(?:workaround|work-around|meanwhile,? use|instead,)\b", re.I)),
    ("confirmation", re.compile(
        r"\b(?:you(?:'re| are) right|exactly right|good catch|as you suspected"
        r"|correct that)\b", re.I)),
    ("measurement", re.compile(
        r"\d+(?:\.\d+)?\s*%|\b\d+ of \d+\b|\brate of \d", re.I)),
)


def handback_text(transcript: Path) -> str:
    """The turn's final assistant text — the sentence being handed back to the user."""
    last = ""
    for line in transcript.read_text(encoding="utf-8",
                                     errors="replace").splitlines()[-4000:]:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("type") != "assistant":
            continue
        texts = [str(b.get("text") or "")
                 for b in (rec.get("message") or {}).get("content") or []
                 if isinstance(b, dict) and b.get("type") == "text"]
        if any(t.strip() for t in texts):
            last = "\n".join(texts)
    return last


def claim_shapes(text: str) -> list[tuple[str, str]]:
    """The sentences of a handback that wear a claim kind's word-shape.

    The intake debt's response half: the record's silence says work reached no claim,
    and this says whether the SENTENCE nonetheless asserts one — the join between what
    was said and what was filed, made while the sentence can still be fixed. One hit
    per kind, first sentence to match, fenced code stripped first because code is not
    the handback's assertion. High recall, low precision, and that is the design: the
    result is information gated behind an already-silent record, never a conviction."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    hits: list[tuple[str, str]] = []
    got: set[str] = set()
    for raw in re.split(r"(?<=[.!?:])\s+|\n+", text):
        sentence = raw.strip(" \t-*>#|")
        if not sentence:
            continue
        for kind, pattern in _CLAIM_SHAPES:
            if kind not in got and pattern.search(sentence):
                got.add(kind)
                hits.append((kind, sentence[:120]))
    return hits


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


def _silence_note(repos: list[Path], shapes: list[tuple[str, str]] = ()) -> str:
    names = ", ".join(r.name for r in repos)
    lines = [f"This turn wrote files in {names} and touched no claims record there."]
    if shapes:
        lines.append(
            "And the handback itself reads as claim-shaped — by word-shape only, a "
            "proposal and never a judgment; deciding happens in code over the filed "
            "record:")
        for kind, sentence in shapes:
            lines.append(f"  {kind}-shaped: {sentence}")
        lines.append(
            "A sentence shaped like a claim, over a record with nothing in it, is "
            "the reporting bias at the moment it is created — "
            "a-corpus-of-reports-carries-its-reporting-bias. File the claim, or "
            "reword the sentence to what was observed. This is information, not a "
            "conviction; nothing is refused.")
    else:
        lines.append(
            "If the turn's sentence reports work finished, fixed, diagnosed or a "
            "workaround, the record is silent exactly where the work happened — "
            "a-corpus-of-reports-carries-its-reporting-bias, and the conviction "
            "statistics are drawn only from what gets filed. File the claim, or say "
            "the work is mid-flight. This is information, not a conviction; nothing "
            "is refused.")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path")
        if not path or payload.get("stop_hook_active"):
            return 0
        from .claims import ClaimFinding, check_file
        findings = [f for claims in touched(Path(path)) for f in check_file(claims)]
        silent = silent_repos(Path(path))
        # the radar reads the handback only when the record is already silent: the
        # join between the sentence and the record is the whole question, and a
        # turn that filed its claims has answered it
        shapes = claim_shapes(handback_text(Path(path))) if silent else []
        # the silence rides the same once-per-content throttle as the findings: a
        # repo the author was told about, and chose to leave silent, is not nagged —
        # a noisy informant is one that gets switched off
        notes = []
        if silent:
            marker = [ClaimFinding(law="intake-silence",
                                   quote=";".join(k for k, _ in shapes),
                                   where="|".join(sorted(r.name for r in silent)),
                                   why="")]
            if not _already_reported(marker):
                notes.append(_silence_note(silent, shapes))
        if findings and not _already_reported(findings):
            notes.insert(0, report(findings))
        if not notes:
            return 0
        print("\n\n".join(notes), file=sys.stderr)
        return 2
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
