"""The reporting-rate instrument: how much of the work reaches the claims record.

a-corpus-of-reports-carries-its-reporting-bias says every conviction statistic from the
claims deciders is drawn from claims somebody chose to file, and the selection is named
beside the number or the number misleads. This measures the selection: over a repo's
git history, the share of working commits that file a claim in the same commit. It is
the intake debt's measuring half — the informant at the Stop hook is the per-turn half,
and this is the per-history one.

WHAT THE NUMBER MISSES, stated because the instrument is subject to its own law: a
claim filed in a different commit than its work (same turn, separate commits — the
common shape when a claim is appended right before committing) counts as a claims-only
commit and a silent working commit, so the per-commit join UNDERSTATES the true rate.
The direction of the bias is known and fixed; the size is not. A turn-level join needs
the transcript, which git does not hold.

    python -m craft.intake <repo> [<repo>...]
    python -m craft.intake --estate <dir>      # every repo under it with a claims file
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def _sh(*args: str, cwd: Path) -> str:
    try:
        done = subprocess.run(args, capture_output=True, cwd=cwd, timeout=300)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.decode("utf-8", "replace")


def rate(repo: Path) -> dict:
    """Per-commit classification over the whole history: working commits (any change
    beyond claims.jsonl), filing commits (claims.jsonl changed), and the join."""
    log = _sh("git", "log", "--format=%H", "--name-only", cwd=repo)
    if not log.strip():
        return {"repo": repo.name, "unread": "git log said nothing"}
    working = filing = joined = 0
    files: list[str] = []

    def close():
        nonlocal working, filing, joined
        if not files:
            return
        works = any(not f.endswith("claims.jsonl") for f in files)
        claims = any(f.endswith("claims.jsonl") for f in files)
        working += works
        filing += claims
        joined += works and claims

    for line in log.splitlines():
        line = line.strip()
        if len(line) == 40 and all(c in "0123456789abcdef" for c in line):
            close()
            files = []
        elif line:
            files.append(line.replace("\\", "/"))
    close()
    return {"repo": repo.name, "working": working, "filing": filing,
            "joined": joined,
            "rate": round(joined / working, 3) if working else None}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.intake",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("repos", nargs="*", type=Path)
    ap.add_argument("--estate", type=Path,
                    help="measure every repo under this directory with a claims file")
    args = ap.parse_args(argv)

    repos = list(args.repos)
    if args.estate:
        repos += sorted(p.parent for p in args.estate.glob("*/claims.jsonl")
                        if (p.parent / ".git").exists())
    if not repos:
        ap.error("give repos, or --estate")

    print("repo                 working  filing  joined   rate")
    unread = []
    for r in repos:
        row = rate(r)
        if "unread" in row:
            unread.append(f"{row['repo']}: {row['unread']}")
            continue
        print(f"{row['repo']:20} {row['working']:7} {row['filing']:7} "
              f"{row['joined']:7}   {row['rate']}")
    print("\n  rate = working commits that file a claim IN THE SAME COMMIT. A claim "
          "filed in a\n  separate commit counts as silence here, so the true rate is "
          "HIGHER than this\n  number — the bias's direction is known, its size is "
          "not, and a turn-level join\n  needs the transcript.")
    for u in unread:
        print(f"  UNREAD  {u}")
    return 1 if unread else 0


if __name__ == "__main__":
    raise SystemExit(main())
