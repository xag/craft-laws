"""The report register gate, on commit messages: a measured figure travels whole.

Root: quality-harness's debt the-reports-register-is-unchecked, whose sightings are
the owner's two register corrections of 2026-08-25 - a report evocative where it
should state mechanisms, and a measured flaw framed as a design property. The
meaning half of register stays a reading, by the standing word-list decision: no
code here judges tone, and none reads the prose for numbers. What became code is the
computable core: THE FAVOURABLE CELL DOES NOT TRAVEL ALONE.

A commit message is this estate's durable per-turn report - the artifact a later
reader actually opens. The check is a data join, in one direction only: for each
measurement claim a commit ADDS to a claims record (read from the diff, which is
data), the commit's message must contain that measurement's `caught` and
`false_alarms` values. A message free to say anything remains free to say anything -
except to present new measured work without the cell that argues against it.

The same join runs on prose files through their drawings (craft/drawing.py's
half-the-cross-tab conviction); this module is the commit-message surface.

    python -m craft.report            # HEAD, in the current repo
    python -m craft.report <rev>      # any single commit
    python -m craft.report --alarm    # a synthetic repo that must convict and pass
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReportFinding:
    check: str
    where: str
    why: str


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, timeout=120)
    if done.returncode != 0:
        raise RuntimeError(done.stderr.decode("utf-8", "replace").strip())
    return done.stdout.decode("utf-8", "replace")


def added_measurements(root: Path, rev: str) -> list[dict]:
    """The measurement claims a commit adds to any claims record - read from the
    diff's added lines, which are data, not from any prose."""
    diff = _git(root, "show", "--format=", "--unified=0", rev, "--", "claims.jsonl",
                "*/claims.jsonl")
    out: list[dict] = []
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        try:
            rec = json.loads(line[1:].strip())
        except ValueError:
            continue
        if isinstance(rec, dict) and rec.get("kind") == "measurement":
            out.append(rec)
    return out


def check_commit(root: Path, rev: str = "HEAD") -> list[ReportFinding]:
    message = _git(root, "log", "-1", "--format=%B", rev)
    short = _git(root, "rev-parse", "--short", rev).strip()
    findings: list[ReportFinding] = []
    for rec in added_measurements(root, rev):
        for cell in ("caught", "false_alarms"):
            value = rec.get(cell)
            if isinstance(value, (int, float)) and str(value) not in message:
                findings.append(ReportFinding(
                    "half-the-cross-tab", f"commit {short}",
                    f"the message reports work that filed a measurement "
                    f"({rec.get('text', '')[:60]!r}) and omits {cell}={value}; "
                    "a figure travels with its unfavourable cell or not at all"))
    return findings


def _alarm() -> int:
    """A synthetic repo: a commit filing a measurement with a one-cell message must
    convict; amending both cells in must pass."""
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _git(root.parent, "init", "-q", str(root))
        _git(root, "config", "user.email", "alarm@example.invalid")
        _git(root, "config", "user.name", "alarm")
        (root / "claims.jsonl").write_text(json.dumps(
            {"kind": "measurement", "text": "the checker's first run",
             "caught": 9, "false_alarms": 4}) + "\n", encoding="utf-8")
        _git(root, "add", "claims.jsonl")
        _git(root, "commit", "-q", "-m", "The checker works: 9 caught")
        found = check_commit(root)
        if [f.check for f in found] != ["half-the-cross-tab"]:
            bad += 1
            print(f"ALARM one-cell message not convicted: {found}")
        _git(root, "commit", "-q", "--amend", "-m",
             "The checker's first run: 9 caught, 4 false alarms")
        if check_commit(root):
            bad += 1
            print("ALARM whole-cross-tab message convicted")
    if not bad:
        print("alarm: the one-cell message convicts, the whole one passes.")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args == ["--alarm"]:
        return _alarm()
    rev = args[0] if args else "HEAD"
    findings = check_commit(Path.cwd(), rev)
    for f in findings:
        print(f"{f.check:18} {f.where}")
        print(f"                   {f.why}")
    if not findings:
        print(f"{rev}: every measurement the commit files travels whole in its "
              "message.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
