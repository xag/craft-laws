# -*- coding: utf-8 -*-
"""Every check this repo keeps, in one list, run at once, answered when the last one ends.

    python -m craft.gate            # every check, in parallel; exit 1 when any is red
    python -m craft.gate --jobs 1   # one at a time, in list order

The checks lived as steps of `.github/workflows/check.yml`, so the only way to learn whether
a commit held was to push it and wait for a runner to come round and read the log. They are
independent processes that read the tree and write nothing to it, so they run side by side
here: each is started as soon as a worker is free, its result is printed in list order the
moment it and every check above it are done, and the command returns when the slowest one
does - never on a fixed wait. CI runs this same command, so the list has one home.

Two checks were inline shell in the workflow and are functions here: the red set is exactly
the declared red set, and LAWS.md is the data rendered.
"""

from __future__ import annotations

import argparse
import difflib
import glob
import io
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The laws that stay red, by name, never by count (counts-are-computed). The two laws carry
# their reasons in their own authority notes: ITIL 4's glossary text is not in hand
# (a-detour), and no source has been found that STATES the whole-view norm (a-view); the
# two publish gates refuse them. A law that loses or gains a citation changes this set, and
# the change is made here, deliberately, in the same commit.
DECLARED_RED = frozenset({
    "a-view-arrives-whole",
    "a-detour-is-announced-as-a-detour",
    "publish", "publish-practice",
})

STAMP = "GENERATED from craft@"


@dataclass(frozen=True)
class Check:
    name: str
    args: tuple

    def argv(self) -> list[str]:
        out = []
        for a in self.args:
            out.extend(sorted(glob.glob(str(ROOT / a))) if "*" in a else [a])
        return [sys.executable, "-m", *out]


CHECKS = (
    Check("The red is exactly the declared red", ("craft.gate", "--red")),
    # The law registry gate: every id a decider convicts under must resolve to a
    # registered, cited law, and every source must be adopted whole. A rule added by hand
    # fails here -- the owner's standing order of 2026-08-27.
    Check("No rule enters by hand", ("pytest", "tests", "-q", "-p", "no:cacheprovider")),
    Check("The account deciders' alarms are live", ("craft.account", "--alarm")),
    Check("The claim deciders' alarms are live", ("craft.claims", "--alarm")),
    Check("The card deciders' alarms are live", ("craft.cards", "--alarm")),
    Check("The ruling pipeline's alarms are live", ("craft.rulings", "--alarm")),
    # An alarm nobody runs is a checker never seen red: prose shipped two defects in one
    # week while its alarm was left out of the list.
    Check("The prose deciders' alarms are live", ("craft.prose", "--alarm")),
    Check("The rendered-world probes' alarms are live", ("craft.instruments", "--alarm")),
    # «a rule about a card is not generic and should not go to craft laws»: a law states
    # itself in the world's vocabulary or the gate fails - craft/genericity.py has the bar.
    Check("The genericity alarm is live", ("craft.genericity", "--alarm")),
    Check("Every law is a proposition, not an app spec", ("craft.genericity",)),
    # A library knows nothing of its consumers. The names live in CRAFT_CLIENT_NAMES
    # (a repository variable on CI), never in the repository.
    Check("No word of the library names a client project", ("craft.genericity", "--clients")),
    Check("This repo's own claims hold", ("craft.claims", "claims.jsonl")),
    Check("Work claims name the decisions consulted, and the names resolve",
          ("craft.consulted", "claims.jsonl")),
    Check("The consult gate convicts what it must", ("craft.consulted", "--alarm")),
    Check("The neutrality audit flags a verdict-shaped feature and clears an innocent one",
          ("craft.neutrality", "--alarm")),
    Check("No account feature is a verdict in disguise",
          ("craft.neutrality", ".craft/accounts/*")),
    Check("Every kind in every committed record resolves to a pinned KindDef",
          ("craft.formats", ".")),
    Check("The format gate convicts what it must", ("craft.formats", "--alarm")),
    Check("A filed measurement travels whole in the commit message", ("craft.report", "HEAD")),
    Check("The report gate convicts what it must", ("craft.report", "--alarm")),
    Check("The README passes its own laws", ("craft.prose", "README.md")),
    Check("The README's drawing is fresh, anchored, and joined to the record",
          ("craft.drawing", "README.md")),
    Check("LAWS.md is the data, rendered", ("craft.gate", "--rendered")),
)


def red_is_declared() -> int:
    from quern import run_rules

    from craft.tree import build
    red = {r.node for r in run_rules(build()) if not r.ok}
    if red != DECLARED_RED:
        print(f"the red set changed: {sorted(red)} != {sorted(DECLARED_RED)} - a law lost or "
              "gained a citation without the record moving. Update laws.py AND "
              "craft/gate.py DECLARED_RED in the same commit, deliberately.")
        return 1
    print(f"red is exactly the declared red: {sorted(red)}")
    return 0


def laws_md_is_rendered() -> int:
    """LAWS.md is a view of the data; a view that can drift from it is a second source of
    truth. Re-rendered and compared, the rev stamp aside."""
    done = subprocess.run([sys.executable, "-m", "craft.render"], cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8")
    if done.returncode:
        print(done.stdout + done.stderr)
        return 1
    fresh = [l for l in done.stdout.splitlines() if STAMP not in l]
    held = [l for l in (ROOT / "LAWS.md").read_text(encoding="utf-8").splitlines()
            if STAMP not in l]
    if fresh == held:
        print("LAWS.md is the data, rendered")
        return 0
    sys.stdout.writelines(l + "\n" for l in list(difflib.unified_diff(
        held, fresh, "LAWS.md", "rendered", lineterm=""))[:40])
    print("LAWS.md disagrees with the data - re-render: python -m craft.render > LAWS.md")
    return 1


@dataclass
class Result:
    check: Check
    code: int
    out: str
    seconds: float


def client_names() -> str:
    """CRAFT_CLIENT_NAMES from the environment, or from the repository variable CI reads it
    from, through `gh`; empty when neither answers, and the check says so."""
    names = os.environ.get("CRAFT_CLIENT_NAMES", "")
    if names:
        return names
    try:
        done = subprocess.run(["gh", "variable", "get", "CRAFT_CLIENT_NAMES"], cwd=ROOT,
                              capture_output=True, text=True, encoding="utf-8", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def run_one(check: Check, env: dict) -> Result:
    start = time.monotonic()
    try:
        done = subprocess.run(check.argv(), cwd=ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env)
        code, out = done.returncode, (done.stdout or "") + (done.stderr or "")
    except OSError as e:
        code, out = 1, f"could not start: {e}"
    return Result(check, code, out, time.monotonic() - start)


def run(checks=CHECKS, jobs: int | None = None) -> int:
    jobs = jobs or min(len(checks), os.cpu_count() or 4)
    start = time.monotonic()
    env = dict(os.environ, PYTHONIOENCODING="utf-8", CRAFT_CLIENT_NAMES=client_names())
    red = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(run_one, c, env) for c in checks]
        for f in futures:            # list order; each prints as soon as it and those above are done
            r = f.result()
            mark = "ok " if r.code == 0 else "RED"
            print(f"{mark} {r.seconds:5.1f}s  {r.check.name}", flush=True)
            if r.code:
                red.append(r.check.name)
                tail = r.out.strip().splitlines()[-30:]
                print("".join(f"      {l}\n" for l in tail), end="", flush=True)
    wall = time.monotonic() - start
    print(f"\n{len(checks) - len(red)}/{len(checks)} green in {wall:.1f}s "
          f"({jobs} at a time)" + (f"; red: {', '.join(red)}" if red else ""))
    return 1 if red else 0


def main(argv=None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                                  line_buffering=True)
    ap = argparse.ArgumentParser(prog="python -m craft.gate", description=__doc__.splitlines()[0])
    ap.add_argument("--jobs", type=int, default=None,
                    help="how many checks run at once (default: one per CPU)")
    ap.add_argument("--red", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--rendered", action="store_true", help=argparse.SUPPRESS)
    ns = ap.parse_args(argv)
    if ns.red:
        return red_is_declared()
    if ns.rendered:
        return laws_md_is_rendered()
    return run(jobs=ns.jobs)


if __name__ == "__main__":
    raise SystemExit(main())
