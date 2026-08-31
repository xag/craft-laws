# -*- coding: utf-8 -*-
"""The audit that keeps the drawing from becoming the conviction.

The account lane's history states the trap (the-turn-account-lane-is-removed): a checker
fed by the checked party's labels reports those labels, and five designs died moving the
author-chosen word one field deeper. The rebuilt lane holds elements to the record with
quotes — but anchoring stops fabrication, not judgment. A new element TYPE can still smuggle
a verdict: if marking it equals convicting, the transcriber is the judge and the decider is
ceremony.

That property is checkable, corpus-wide, by counting. For every element feature an account
can carry — a node type, a ground, a scheme, a role, the presence of names or definitions —
tally the accounts that carry it against the accounts a decider convicted. A feature whose
presence coincides exactly with conviction, both ways, over enough accounts, is a verdict
wearing a node type: writing it IS convicting, and the design that added it gets refused.

    python -m craft.neutrality <accounts-dir> [...]
    python -m craft.neutrality --alarm

The audit reads structure only: convictions here are the corpus-free deciders' (the record
a session argued against is not kept with its accounts), so anchor and name convictions are
not in the tally. That narrows what the audit can see and is said here rather than papered
over: a feature can pass this audit and still be judged smuggled by a reader.

What it cannot catch either: a verdict smuggled into an element's VALUE rather than its
presence ("scheme": "bad-argument" would pass a presence audit). Values are enumerated in
the schema, so a new enum member is a schema diff a reader reviews; the audit covers the
axis the schema cannot.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# a feature must appear, and be absent, at least this often before the audit will call
# perfect coincidence a verdict rather than a small sample
MIN_SUPPORT = 3


def features(account: dict) -> set:
    """The features one account carries. Presence only, never values — see the module
    docstring for what that choice covers and what it cannot."""
    out = set()
    for node in account.get("nodes", []):
        if not isinstance(node, dict):
            continue
        if node.get("type"):
            out.add(f"type:{node['type']}")
        for field in ("ground", "scheme", "role", "strength", "form"):
            if node.get(field):
                out.add(f"{field}:{node[field]}")
        for field in ("names", "defines", "quantity", "prop", "says"):
            if node.get(field):
                out.add(f"has:{field}")
    return out


def _structural_findings(path: Path) -> int:
    """Convictions from the corpus-free deciders. LookupError cannot happen here because
    the anchor and name deciders are exactly the ones this audit does not run."""
    from .account import CHECKS, load
    try:
        account = load(path)
    except (OSError, ValueError):
        return 1
    if not account.nodes:
        return 1
    return sum(len(check(account)) for check in CHECKS)


def audit(paths: list) -> tuple:
    """(rows, verdict_shaped): per feature, the coincidence table with conviction."""
    seen = []
    for path in paths:
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        seen.append((features(raw), _structural_findings(Path(path)) > 0))
    rows = []
    all_features = sorted({f for fs, _ in seen for f in fs})
    for feature in all_features:
        with_f = [convicted for fs, convicted in seen if feature in fs]
        without = [convicted for fs, convicted in seen if feature not in fs]
        rows.append({
            "feature": feature,
            "present": len(with_f), "present_convicted": sum(with_f),
            "absent": len(without), "absent_convicted": sum(without),
        })
    shaped = [r for r in rows
              if r["present"] >= MIN_SUPPORT and r["absent"] >= MIN_SUPPORT
              and r["present_convicted"] == r["present"]
              and r["absent_convicted"] == 0]
    return rows, shaped


def _accounts_in(dirs: list) -> list:
    out = []
    for d in dirs:
        out += sorted(Path(d).glob("*.json"))
    return [p for p in out
            if p.name not in ("residual.json",) and not p.name.endswith(".jsonl")]


def _alarm() -> int:
    """The audit against a corpus where one feature IS the verdict, and one where the
    same feature is innocent. Built from real element types and real structural
    convictions — an absence scheme with no grounded search convicts, one with a
    grounded search does not — so nothing here is staged except the coincidence."""
    import tempfile

    def absence_account(convicts: bool) -> dict:
        nodes = [{"id": "c1", "type": "I", "role": "conclusion"},
                 {"id": "r1", "type": "RA", "scheme": "absence",
                  "premises": ["g1"], "conclusion": "c1"},
                 {"id": "g1", "type": "I"}]
        if not convicts:
            nodes[2] = {"id": "g1", "type": "I", "ground": "producer",
                        "quote": "0 matches found"}
        return {"nodes": nodes}

    def plain_account() -> dict:
        return {"nodes": [
            {"id": "g1", "type": "I", "ground": "given", "quote": "do it"},
            {"id": "c1", "type": "I", "role": "conclusion"},
            {"id": "r1", "type": "RA", "scheme": "verified-source",
             "premises": ["g1"], "conclusion": "c1"}]}

    dead = []
    with tempfile.TemporaryDirectory() as d:
        # corpus A: scheme:absence present exactly on the convicted accounts
        for i in range(3):
            (Path(d) / f"a{i}.json").write_text(json.dumps(absence_account(True)),
                                                encoding="utf-8")
        for i in range(3):
            (Path(d) / f"b{i}.json").write_text(json.dumps(plain_account()),
                                                encoding="utf-8")
        _, shaped = audit(_accounts_in([d]))
        if "scheme:absence" not in {r["feature"] for r in shaped}:
            dead.append("a feature coinciding exactly with conviction was not flagged")
    with tempfile.TemporaryDirectory() as d:
        # corpus B: the same feature, now innocent on half its accounts
        for i in range(3):
            (Path(d) / f"a{i}.json").write_text(json.dumps(absence_account(True)),
                                                encoding="utf-8")
        for i in range(3):
            (Path(d) / f"c{i}.json").write_text(json.dumps(absence_account(False)),
                                                encoding="utf-8")
        for i in range(3):
            (Path(d) / f"b{i}.json").write_text(json.dumps(plain_account()),
                                                encoding="utf-8")
        _, shaped = audit(_accounts_in([d]))
        if shaped:
            dead.append(f"an innocent corpus was flagged: {[r['feature'] for r in shaped]}")
    for line in dead:
        print("DEAD ALARM  " + line)
    if dead:
        return 1
    print("both alarms ring: the audit flags a verdict-shaped feature and clears an "
          "innocent one.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m craft.neutrality",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("dirs", nargs="*", help="account directories to audit")
    ap.add_argument("--alarm", action="store_true")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.dirs:
        print("give account directories, or --alarm")
        return 1
    rows, shaped = audit(_accounts_in(args.dirs))
    for r in rows:
        print(f"  {r['feature']:<24} present {r['present']:>3} "
              f"(convicted {r['present_convicted']:>3})   "
              f"absent {r['absent']:>3} (convicted {r['absent_convicted']:>3})")
    if shaped:
        print("\nVERDICT-SHAPED — presence coincides exactly with conviction:")
        for r in shaped:
            print(f"  {r['feature']}")
        return 1
    print(f"\n{len(rows)} feature(s), none verdict-shaped at support {MIN_SUPPORT}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
