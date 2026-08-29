"""The adjudicator pass over cleared accounts.

The mechanical deciders check what an account CLAIMS hard: quotes exist verbatim in
the record, claimed deductions entail, the graph is well-formed. What they never
judge is the semantic link the account merely declares: whether a premise's reading
follows from its quote, and whether a defeasible inference's premises support its
conclusion. Until 2026-08-29 that link was checked by nobody, and the estate's own
law says routing it to the owner's attention is a defect
(the-users-attention-is-not-a-test-harness). This module is the recorded remedy
(quality-harness: the-remainder-can-be-adjudicated-without-a-person): a judge model
reads each link WITH the material in hand and rules on it; a person sees only what
the judge could not support.

What it does, mechanically:

  - `units(account)` extracts the judgeable links: one READING unit per grounded
    premise (quote -> text), one INFERENCE unit per non-deduction RA node (premise
    texts -> conclusion text). Deductions are excluded on purpose - Z3 already
    decides those, and a second judge over a proof is noise.
  - `adjudicate(paths, judge)` runs the judge over every unit not already ruled on,
    and appends each verdict to `adjudications.jsonl` beside the accounts: the
    append-only labeled set from which the lane's error rates become measurable.
  - The verdict vocabulary is closed: `supported`, `unsupported`, `cannot-tell`.
    Any other word from the judge is recorded as `cannot-tell` with the judge's
    words kept - a judge inventing vocabulary is a fact worth keeping, never a
    crash.
  - Per the rulings doctrine (only-the-owner-exempts): the adjudicator's verdicts
    PROPOSE. An `unsupported` is a finding for a person to act on; nothing here
    edits an account, and nothing here exempts one.

The judge is a callable `judge(units) -> list[dict]` so tests inject a fake; the
default is `api_judge`, which calls the Anthropic API (lazily imported, key from
ANTHROPIC_API_KEY) with every unit of one account in one request. The API judge is
deliberate: the party being graded authors the accounts, so the client that wrote
them cannot also be the judge - that is the self-report failure this estate
convicts elsewhere.

    python -m craft.adjudicate <dir-or-account.json ...>      # judge fresh units
    python -m craft.adjudicate --list <dir ...>               # show units, no judge
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

VERDICTS = ("supported", "unsupported", "cannot-tell")

DEFAULT_MODEL = "claude-sonnet-5"

ADJUDICATIONS = "adjudications.jsonl"


@dataclass
class Unit:
    """One judgeable link of one account."""
    account: str          # file name
    node: str             # node id (reading) or RA id (inference)
    kind: str             # "reading" | "inference"
    question: str         # what the judge is asked, with the material inline


@dataclass
class Verdict:
    account: str
    node: str
    kind: str
    verdict: str          # a member of VERDICTS
    why: str
    judge: str            # model id, or the fake's name in tests
    at: str               # ISO-8601 UTC


def _node_text(nodes: dict, nid) -> str:
    n = nodes.get(nid) if isinstance(nid, str) else None
    return str((n or {}).get("text") or (n or {}).get("quote") or nid)


def units(path: Path) -> list[Unit]:
    """The judgeable links of one account file. An unreadable or empty account
    yields no units - the caller reports the zero (a-check-exhibits-what-it-read)."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    nodes = {n["id"]: n for n in raw.get("nodes", []) if isinstance(n, dict) and "id" in n}
    out: list[Unit] = []
    for n in nodes.values():
        if n.get("type") == "I" and n.get("ground") and n.get("quote") and n.get("text"):
            out.append(Unit(
                account=path.name, node=n["id"], kind="reading",
                question=("Does the READING assert only what the QUOTE shows? The "
                          "quote is a verbatim record excerpt; the reading is what "
                          "its author says it shows. Answer supported only when a "
                          "careful reader of the quote alone would accept the "
                          "reading.\n"
                          f"QUOTE: {n['quote']}\n"
                          f"READING: {n['text']}")))
    for n in nodes.values():
        if n.get("type") != "RA" or n.get("scheme") == "deduction":
            continue
        cid = n.get("conclusion")
        cid = cid if isinstance(cid, str) else (list(cid or [None])[0])
        prem = "\n".join(f"- {_node_text(nodes, p)}" for p in n.get("premises", []))
        out.append(Unit(
            account=path.name, node=n["id"], kind="inference",
            question=(f"Do the PREMISES give real (defeasible, scheme "
                      f"'{n.get('scheme', '?')}') support to the CONCLUSION - not "
                      "proof, but would the conclusion be reasonable to hold on "
                      "these premises alone? Answer unsupported when the premises "
                      "are consistent with the conclusion being false and add no "
                      "real weight, or bear on a different claim.\n"
                      f"PREMISES:\n{prem}\n"
                      f"CONCLUSION: {_node_text(nodes, cid)}")))
    return out


def _already(dirpath: Path) -> set[tuple[str, str]]:
    seen = set()
    f = dirpath / ADJUDICATIONS
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                seen.add((r["account"], r["node"]))
            except (ValueError, KeyError):
                continue
    return seen


def api_judge(batch: list[Unit], model: str = DEFAULT_MODEL):
    """One API request per account batch. Lazily imported so the module costs
    nothing to import; raises with a plain sentence when the key is absent."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY is not set - the adjudicator needs "
                           "the metered judge; the graded author cannot judge "
                           "its own accounts")
    import anthropic

    prompt = (
        "You adjudicate links in a formal argument account. For each numbered unit "
        "answer with a JSON array of objects {\"i\": <number>, \"verdict\": "
        "\"supported\"|\"unsupported\"|\"cannot-tell\", \"why\": <one sentence>}. "
        "Only the JSON array, nothing else.\n\n"
        + "\n\n".join(f"UNIT {i}:\n{u.question}" for i, u in enumerate(batch)))
    client = anthropic.Anthropic()
    msg = client.messages.create(model=model, max_tokens=2000,
                                 messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    start, end = text.find("["), text.rfind("]")
    rows = json.loads(text[start:end + 1]) if start >= 0 <= end else []
    out = []
    for i, u in enumerate(batch):
        row = next((r for r in rows if r.get("i") == i), None)
        v = str((row or {}).get("verdict", "cannot-tell"))
        why = str((row or {}).get("why", "the judge returned nothing for this unit"))
        if v not in VERDICTS:
            why = f"judge said {v!r}: {why}"
            v = "cannot-tell"
        out.append({"verdict": v, "why": why})
    return out


def adjudicate(paths: list[Path], judge=None, judge_name: str = DEFAULT_MODEL
               ) -> tuple[list[Verdict], int]:
    """Judge every fresh unit of the given account files; append verdicts beside
    them. Returns (fresh verdicts, units skipped as already adjudicated)."""
    judge = judge or api_judge
    fresh: list[Verdict] = []
    skipped = 0
    by_dir: dict[Path, list[Path]] = {}
    for p in paths:
        by_dir.setdefault(p.parent, []).append(p)
    for d, files in by_dir.items():
        seen = _already(d)
        dir_fresh: list[Verdict] = []
        for f in sorted(files):
            us = units(f)
            todo = [u for u in us if (u.account, u.node) not in seen]
            skipped += len(us) - len(todo)
            if not todo:
                continue
            answers = judge(todo)
            now = datetime.now(timezone.utc).isoformat()
            for u, a in zip(todo, answers):
                dir_fresh.append(Verdict(account=u.account, node=u.node, kind=u.kind,
                                         verdict=a["verdict"], why=a["why"],
                                         judge=judge_name, at=now))
        if dir_fresh:
            with open(d / ADJUDICATIONS, "a", encoding="utf-8") as fh:
                for v in dir_fresh:
                    fh.write(json.dumps(asdict(v)) + "\n")
        fresh.extend(dir_fresh)
    return fresh, skipped


def _account_files(args: list[str]) -> list[Path]:
    out = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out.extend(f for f in sorted(p.glob("*.json"))
                       if f.name not in ("residual.json",))
        elif p.suffix == ".json":
            out.append(p)
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.adjudicate",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help="account files or session directories")
    ap.add_argument("--list", action="store_true",
                    help="print the judgeable units and stop; no judge is called")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ns = ap.parse_args(argv)

    files = _account_files(ns.paths)
    all_units = [u for f in files for u in units(f)]
    if ns.list:
        for u in all_units:
            print(f"{u.account} {u.node} [{u.kind}]")
        print(f"{len(files)} account(s), {len(all_units)} judgeable unit(s).")
        return 0
    if not all_units:
        # a-check-exhibits-what-it-read: zero units is said, never passed over
        print(f"{len(files)} account(s), 0 judgeable unit(s): nothing judged.")
        return 0
    try:
        fresh, skipped = adjudicate(files, judge_name=ns.model,
                                    judge=lambda b: api_judge(b, ns.model))
    except RuntimeError as e:
        print(str(e))
        return 1
    bad = [v for v in fresh if v.verdict == "unsupported"]
    unsure = [v for v in fresh if v.verdict == "cannot-tell"]
    for v in bad + unsure:
        print(f"{v.verdict.upper()}  {v.account} {v.node} [{v.kind}]: {v.why}")
    print(f"{len(files)} account(s), {len(fresh)} unit(s) adjudicated "
          f"({skipped} already ruled), {len(bad)} unsupported, "
          f"{len(unsure)} cannot-tell.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
