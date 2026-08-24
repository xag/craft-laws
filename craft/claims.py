"""The claim deciders: the practice laws' checks, run on assertions instead of screens.

A LAW is general and timeless: it says what must hold whenever its trigger fires, for
anyone, and it can be argued with in a diff. A CLAIM is one utterance at one moment —
"it is done", "this fixes it", "the cause is the cache" — true or unsupported about one
state of the world, and gone from the record the moment the conversation scrolls. The
practice laws (craft/practice.py) fire on CLAIMS: their triggers are not properties of
an app but properties of an assertion, which is why the interface compiler cannot touch
them. This module is the missing half — the same move prose.py made for the doc laws:
give the subject a data shape, then convict with certainty or stay silent.

The shape is one JSON object per claim, appended to a session's `claims.jsonl` at the
moment of claiming (the discipline flight-recorder already imposes at the storage and
HTTP boundaries, imposed here at the boundary that failed on 2026-08-17: the boundary
between what was done and what was said about it):

    {"kind": "done", "text": "the sheet renders on the phone",
     "evidence": [{"where": "user-surface", "what": "beacon self-fetched at 21:48:55,
                    four report_card_state calls after it"}]}

    {"kind": "fixed", "text": "the empty card", "reproduced_first": true,
     "changes": ["self-fetch on missing payload"],
     "evidence": [{"where": "stand-in", "what": "harness NO_PAYLOAD mode green",
                   "gap": "the phone itself not observed"}]}

    {"kind": "diagnosis", "text": "the host never pushes tool results",
     "prior_theories": 4, "new_observation": "beacon: after-initialized, no-payload"}

    {"kind": "confirmation", "text": "the user is right that the suite gates itself",
     "checked": "ran npm test with credentials stripped: 87 tests, 6.4s, 2 skipped"}

    {"kind": "measurement", "text": "the turn checker's accuracy",
     "corpus": "every transcript in ~/.claude/projects, exhaustive",
     "size_declared_before": true, "prespecified": true,
     "reference_standard": "a person's reading of each candidate",
     "author_knew_answers": false, "judge_saw_verdict": true,
     "caught": 1, "false_alarms": 17, "misses": "unmeasured: no sampling of the cleared"}

A MEASUREMENT is an accuracy, coverage or calibration figure filed as a claim, and its
fields are STARD 2015's items as data — the protocol a diagnostic-accuracy report must
state, imposed on a check's report the day the laws arrived, so the laws are checked by
code and not by a reader. Absent fields convict; an honest "unmeasured: why" in
`misses` passes the code check and stays visible, because reporting the missing row as
missing is the minimum item 23 demands and hiding it is the breach.

A CONFIRMATION is an agreement filed as a claim: "you are right", "yes, that is the
cause", "the premise holds". It is the easiest claim to make and the least likely to
rest on anything — agreeing reads as deference, which is what makes an unchecked one
insidious — so it carries `checked`: what was actually verified before agreeing. The
root is the IPCC note's paragraph 2 verbatim: judgments are explained "by providing a
traceable account ... which together form the basis for a given key finding", and an
agreement is a finding like any other. What it deliberately does NOT get is a decider
for REVERSALS: a flipped position with no new observation is a real defect (both edges
fired on 2026-08-24), but Agans rule 3 covers explanations of failures, not positions,
and no root has been found that reaches the conversational case — that gap is recorded
at `a-ruling-has-no-stated-lifetime`, and minting without the root is how the practice
family got into debt.

`evidence.where` takes three words. **user-surface**: the thing the user touches was
observed (a beacon from their device, their screenshot, their report). **stand-in**: a
faithful reconstruction was observed (their real payload in a real browser) — honest
ONLY with a `gap` naming what it cannot show. **producer**: tests, deploys, logs, files
on the machine — necessary, and never sufficient for a done-claim on its own.

    python -m craft.claims claims.jsonl
    python -m craft.claims --alarm

What stays with a reader, on purpose: whether the evidence is truthful. A decider
reads what the record says was observed, not the world; a session that lies in its
claims ledger has left the game these checks are part of.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from craft.practice import PRACTICE

_LAW_IDS = {law.id for law in PRACTICE}


@dataclass
class ClaimFinding:
    law: str
    where: str       # file and line ordinal, so the claim can be found again
    quote: str
    why: str


def _law(law_id: str) -> str:
    if law_id not in _LAW_IDS:
        raise ValueError(f"no practice law '{law_id}' in craft@")
    return law_id


_WHERES = ("user-surface", "stand-in", "producer")


def check_done_is_observed(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A done/fixed claim carries user-surface evidence, or a stand-in that names its
    gap. Producer evidence alone — however much of it — does not close a done-claim."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") not in ("done", "fixed"):
            continue
        ev = c.get("evidence") or []
        if any(e.get("where") == "user-surface" for e in ev):
            continue
        stand_ins = [e for e in ev if e.get("where") == "stand-in"]
        if stand_ins and all(str(e.get("gap") or "").strip() for e in stand_ins):
            continue
        why = ("every item of evidence is producer-side — the claim observes the "
               "shipping, not the thing the user touches"
               if ev and all(e.get("where") == "producer" for e in ev) else
               "a stand-in without a named gap claims to be the user's surface"
               if stand_ins else
               "the claim carries no evidence at all")
        out.append(ClaimFinding(_law("done-is-observed-where-the-user-stands"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120], why))
    return out


def check_fixed_reproduced_first(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A fixed-claim names the reproduction that failed before the change. A fix
    reasoned from a description of the failure is a theory wearing a verb."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "fixed":
            continue
        if c.get("reproduced_first") is True:
            continue
        out.append(ClaimFinding(_law("make-it-fail-before-you-fix-it"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                "no reproduction preceded the fix — the failure was "
                                "only ever seen where it was reported"))
    return out


def check_one_candidate_per_fix(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A fixed-claim lists the changes it shipped; two or more independent candidates
    for one symptom mean the outcome names no cause."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "fixed":
            continue
        changes = c.get("changes") or []
        if len(changes) > 1:
            out.append(ClaimFinding(_law("one-candidate-fix-per-deploy"),
                                    f"{name}#{i + 1}", "; ".join(map(str, changes))[:120],
                                    f"{len(changes)} candidate fixes ride one claim — "
                                    "whatever happens next confirms none of them"))
    return out


def check_theories_carry_observations(name: str, claims: list[dict]
                                      ) -> list[ClaimFinding]:
    """A diagnosis that follows earlier theories names the NEW observation that
    separates it from them. Two explanations, zero new signals, is guessing."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "diagnosis":
            continue
        if int(c.get("prior_theories") or 0) < 1:
            continue
        if str(c.get("new_observation") or "").strip():
            continue
        out.append(ClaimFinding(_law("instrument-before-the-second-theory"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                "a follow-up theory with no new observation between "
                                "it and the last one — the next act is an instrument"))
    return out


def check_detours_say_so(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A claim that resolves a report by a different route says `detour: true` and
    names what stays broken. Routing around is fine; calling it fixed is not."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "detour":
            continue
        if str(c.get("still_broken") or "").strip():
            continue
        out.append(ClaimFinding(_law("a-detour-is-announced-as-a-detour"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                "a detour that does not name what stays broken is "
                                "a fix-claim in costume"))
    return out


# THREE DECIDERS WERE REMOVED HERE, 2026-08-22, and this note is why they should not come
# back in this shape. deliberate-names-its-decision, a-remainder-names-its-debt and
# a-census-is-read-from-its-source were checked by matching WORDS in a claim's prose --
# /deliberate|by design|on purpose/, /later|next|not yet|deferred|owed|blocked|remains/,
# a count-noun pattern -- and requiring a structured field once a word hit. The match only
# TRIGGERED and the verdict was structural, which is a real distinction and not enough of
# one: a word list over prose is a reading, and this repo has already measured what a
# reading costs when it fires as a check. Seven convictions in eight were not defects, and
# two of them convicted the law being OBEYED. These three fired at Stop, with exit 2, on
# laws that cite nobody, which the-deciders-run-by-hand rejects: 'a reading law reported as
# a block is the noise that ends the practice'.
#
# The three laws STAY. They carry falsifiers and real sightings, and they are red because
# they cite nobody, which is this repo's honest state for a law with no root. What they no
# longer have is a mechanism, and that is the accurate position: unmechanized, not faked.
# The decision is recorded at `a-word-list-is-a-reading-not-a-mechanization` in the ledger.


def check_confirmations_carry_their_account(name: str, claims: list[dict]
                                            ) -> list[ClaimFinding]:
    """A confirmation names what was checked before agreeing. An agreement is the
    highest confidence term there is, and one with no traceable account behind it is
    exactly the unlicensed qualifier — in the direction that wears deference."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "confirmation":
            continue
        if str(c.get("checked") or "").strip():
            continue
        out.append(ClaimFinding(_law("a-qualifier-is-licensed-by-the-evidence"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                "an agreement with nothing checked behind it — the "
                                "finding has no traceable account, and assent the "
                                "evidence does not license is worth nothing when "
                                "it agrees"))
    return out


# A measurement claim's protocol, field by field, each field one law. Table-driven
# because the deciders are field-presence checks and a table keeps the law-to-field
# mapping readable in one place; the VERDICT stays structural (the field is there or it
# is not), which is what keeps this a check in code rather than a reading.
_MEASUREMENT_PROTOCOL = (
    ("corpus", "a-corpus-names-its-assembly",
     "the corpus is unstated — findings over a corpus name how it was assembled, "
     "and whether the series was exhaustive, random, or convenient"),
    ("size_declared_before", "calibration-size-is-declared-before-the-run",
     "nothing says the calibration size was settled before the run — a figure whose "
     "corpus was sized after the results is tuned, not measured"),
    ("prespecified", "prespecified-is-distinguished-from-exploratory",
     "nothing says whether the thresholds were set before or after the results were "
     "seen"),
    ("reference_standard", "the-reference-standard-is-named-with-its-rationale",
     "no reference standard is named — accuracy against nothing is a number about "
     "nothing"),
    ("author_knew_answers", "blindness-is-disclosed",
     "blinding is undisclosed: did the check's author know the answers while writing "
     "it?"),
    ("judge_saw_verdict", "blindness-is-disclosed",
     "blinding is undisclosed: did the judge see the check's verdict before "
     "deciding?"),
    ("misses", "a-check-reports-its-misses",
     "only what was caught is reported — the cross tabulation has no row for misses; "
     "'unmeasured: <why>' is an honest value and absence is not"),
)


def check_measurements_state_their_protocol(name: str, claims: list[dict]
                                            ) -> list[ClaimFinding]:
    """An accuracy, coverage or calibration figure states its protocol: STARD's items
    as fields, each convicting by absence. The one field with graded honesty is
    `misses` — an explicit "unmeasured: why" passes, silence does not."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "measurement":
            continue
        for field, law, why in _MEASUREMENT_PROTOCOL:
            if field in c and (c[field] is not None and str(c[field]).strip() != ""):
                continue
            out.append(ClaimFinding(_law(law), f"{name}#{i + 1}",
                                    str(c.get("text", ""))[:120], why))
    return out


CHECKS = (check_done_is_observed, check_fixed_reproduced_first,
          check_one_candidate_per_fix, check_theories_carry_observations,
          check_detours_say_so, check_confirmations_carry_their_account,
          check_measurements_state_their_protocol)


def check_file(path: Path) -> list[ClaimFinding]:
    claims = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            claims.append(json.loads(line))
    out: list[ClaimFinding] = []
    for check in CHECKS:
        out.extend(check(path.name, claims))
    return out


def _alarm() -> int:
    """Every decider against a convicting record and a clean one. A checker that has
    never been seen red is relocated guessing — the lesson this repo's own screenshot
    harness re-taught on its first CI run."""
    guilty = [
        {"kind": "done", "text": "deployed and verified",
         "evidence": [{"where": "producer", "what": "suite green, machine has file"}]},
        {"kind": "fixed", "text": "the empty card",
         "changes": ["hashed uri", "renamed tool", "reshaped meta"]},
        {"kind": "diagnosis", "text": "it is the html cache", "prior_theories": 3},
        {"kind": "detour", "text": "use /deck instead"},
        {"kind": "done", "text": "it renders",
         "evidence": [{"where": "stand-in", "what": "jsdom run"}]},
        {"kind": "confirmation", "text": "you are right, the tests are irrelevant"},
        {"kind": "measurement", "text": "the checker is accurate",
         "corpus": "twenty transcripts", "caught": 18},
    ]
    clean = [
        {"kind": "done", "text": "the sheet renders on the phone",
         "evidence": [{"where": "user-surface",
                       "what": "beacon self-fetched; four card reports after"}]},
        {"kind": "fixed", "text": "the empty card", "reproduced_first": True,
         "changes": ["self-fetch on missing payload"],
         "evidence": [{"where": "stand-in", "what": "NO_PAYLOAD harness green",
                       "gap": "the phone itself not observed"}]},
        {"kind": "diagnosis", "text": "the host never pushes", "prior_theories": 4,
         "new_observation": "beacon: after-initialized then no-payload"},
        {"kind": "detour", "text": "use /deck meanwhile",
         "still_broken": "the MCP card until the host refreshes"},
        {"kind": "confirmation", "text": "the suite already gates itself correctly",
         "checked": "ran npm test with credentials stripped: 87 tests, 6.4s, 2 skipped"},
        {"kind": "measurement", "text": "the three word lists over the estate's docs",
         "corpus": "87 markdown files across the estate, exhaustive glob",
         "size_declared_before": True, "prespecified": True,
         "reference_standard": "a person reading every hit in its paragraph",
         "author_knew_answers": True, "judge_saw_verdict": True,
         "caught": 3, "false_alarms": 2,
         "misses": "unmeasured: no sampling of the files with no hits"},
    ]
    dead = []
    for check in CHECKS:
        if not check("guilty", guilty):
            dead.append(f"{check.__name__} missed the guilty record")
        if check("clean", clean):
            dead.append(f"{check.__name__} convicted the clean record")
    for d in dead:
        print(f"DEAD ALARM  {d}")
    print("all alarms live" if not dead else f"{len(dead)} dead alarm(s)")
    return 1 if dead else 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.claims",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--alarm", action="store_true")
    ns = ap.parse_args(argv)
    if ns.alarm:
        return _alarm()
    total = 0
    for f in ns.files:
        for x in check_file(f):
            total += 1
            print(f"{x.law}  {x.where}\n  «{x.quote}»\n  {x.why}")
    if not total:
        print(f"{len(ns.files)} file(s): no claim decider convicts.")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
