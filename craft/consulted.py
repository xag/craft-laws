"""The consult gate: work names the recorded decisions it rests on, and code checks it.

Root: quality-harness's debt a-recorded-decision-binds-no-new-work, from the two
sightings of 2026-08-25 - a decision's rejected alternative rebuilt reworded, a
standing ambition closed against - both with every gate green, because every gate read
records, laws, or the built thing, and none read the relation between new work and the
decisions that had already judged it.

The payment follows the estate's one pattern: the fallible part is authored as data,
the checks are code and exact. A session cannot be made to UNDERSTAND a decision by any
check; it can be made to say which entries it consulted, in a place where the saying is
demanded, resolvable, and auditable afterwards - the same trust model as
reproduced_first on a fixed-claim and the quote on a drawing annotation.

A repo opts in with `.craft/ledger.json` beside its claims file:

    {"module": "craft.tree", "since": 49}

`module` names the module whose build() returns the ledger this repo's decisions live
in. `since` is the number of claims already filed when the gate was adopted - those are
exempt by ordinal, as data, because a demand nobody could have known about convicts
nothing but the calendar.

The checks, each deterministic:

  unconsulted  - a done- or fixed-claim past `since` carries no `consulted`. The value
                 owed is a list of ledger entry ids, or the string "none: <why>" - an
                 honest statement that no recorded decision bears on the work, which is
                 auditable precisely because it is on the record.
  unresolved   - a consulted id that is not an entry in the ledger. A consultation
                 that names nothing checkable is a memory.
  rejected     - a consulted id that resolves to an `alternative` node: a road the
                 ledger already rejected. The argument projection reads an alternative
                 as a proposition under attack from its own parent; a defeated entry is
                 not a foundation, and the thing to consult is the decision that
                 rejected it - which is exactly the reading that would have stopped the
                 word-list rebuild, had the rebuild been made to declare itself.

WHAT THIS DOES NOT CLAIM: that the right decisions were consulted, or that the reading
was competent. That stays authored and auditable, never computed - computing it would
mean reading meaning, and the estate's word-list decision stands.

    python -m craft.consulted <claims.jsonl> [...]
    python -m craft.consulted --alarm
"""

from __future__ import annotations

import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

WORK_KINDS = ("done", "fixed")


@dataclass
class ConsultFinding:
    check: str
    where: str
    why: str


def ledger_index(module_name: str) -> dict[str, str]:
    """Every entry id in the ledger, mapped to its kind - children included, because
    the rejected alternatives this gate exists to refuse are children."""
    module = importlib.import_module(module_name)
    index: dict[str, str] = {}

    def walk(n):
        if getattr(n, "id", None):
            index[n.id] = getattr(n, "kind", "") or ""
        for k in getattr(n, "children", []) or []:
            walk(k)

    for n in module.build().root.children:
        walk(n)
    return index


def check_claims(claims: list[dict], index: dict[str, str], since: int,
                 name: str = "claims.jsonl") -> list[ConsultFinding]:
    findings: list[ConsultFinding] = []
    for i, claim in enumerate(claims, 1):
        if i <= since or claim.get("kind") not in WORK_KINDS:
            continue
        where = f"{name}#{i}"
        consulted = claim.get("consulted")
        if consulted is None:
            findings.append(ConsultFinding(
                "unconsulted", where,
                "a work claim past the gate's adoption names no consulted entries; "
                "list the ledger entries the design rests on, or say "
                "'none: <why>' on the record"))
            continue
        if isinstance(consulted, str):
            if consulted.startswith("none:") and consulted[5:].strip():
                continue
            findings.append(ConsultFinding(
                "unconsulted", where,
                f"'{consulted}' is neither a list of entry ids nor 'none: <why>'"))
            continue
        for cid in consulted:
            kind = index.get(str(cid))
            if kind is None:
                findings.append(ConsultFinding(
                    "unresolved", where,
                    f"consulted entry {cid!r} is not in the ledger"))
            elif kind == "alternative":
                findings.append(ConsultFinding(
                    "rejected", where,
                    f"{cid!r} is a rejected alternative - a defeated entry is not a "
                    "foundation; consult the decision that rejected it"))
    return findings


def check_file(path: Path) -> list[ConsultFinding] | None:
    """None when the repo has not adopted the gate - opt-in is data, not a guess."""
    decl_path = path.parent / ".craft" / "ledger.json"
    if not decl_path.exists():
        return None
    decl = json.loads(decl_path.read_text(encoding="utf-8"))
    claims = [json.loads(line) for line in
              path.read_text(encoding="utf-8").splitlines() if line.strip()]
    index = ledger_index(decl["module"])
    return check_claims(claims, index, int(decl.get("since", 0)), path.name)


def _alarm() -> int:
    """The gate against records that must convict and records that must pass, over
    this repo's real ledger - a checker never seen red is relocated guessing."""
    index = ledger_index("craft.tree")
    guilty = [
        {"kind": "done", "text": "work with no consultation"},
        {"kind": "fixed", "text": "consulting a ghost",
         "consulted": ["an-entry-nobody-wrote"]},
        {"kind": "done", "text": "resting on a rejected road",
         "consulted": ["alt-keep-them-the-match-only-triggers"]},
        {"kind": "done", "text": "an empty why", "consulted": "none:"},
    ]
    clean = [
        {"kind": "done", "text": "consulting the decision itself",
         "consulted": ["a-word-list-is-a-reading-not-a-mechanization"]},
        {"kind": "done", "text": "an honest none",
         "consulted": "none: greenfield module, no decision touches it"},
        {"kind": "measurement", "text": "not a work claim", "caught": 1},
    ]
    bad = 0
    for i, claim in enumerate(guilty):
        if not check_claims([claim], index, 0):
            bad += 1
            print(f"ALARM guilty record {i} was not convicted: {claim['text']}")
    convicted = [f for c in clean for f in check_claims([c], index, 0)]
    for f in convicted:
        bad += 1
        print(f"ALARM clean record convicted: {f.check} - {f.why}")
    if not bad:
        print(f"alarm: {len(guilty)} guilty convicted, {len(clean)} clean pass.")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args == ["--alarm"]:
        return _alarm()
    if not args:
        print(__doc__.splitlines()[0])
        print("usage: python -m craft.consulted <claims.jsonl> [...] | --alarm")
        return 2
    bad = 0
    for name in args:
        found = check_file(Path(name))
        if found is None:
            print(f"{name}: no .craft/ledger.json beside it - the gate is opt-in.")
            continue
        for f in found:
            bad += 1
            print(f"{f.check:12} {f.where}")
            print(f"             {f.why}")
    if not bad:
        print(f"{len(args)} file(s): every consultation resolves.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
