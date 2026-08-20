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


import re as _re

_INTENT = _re.compile(r"\b(deliberate(?:ly)?|by design|on purpose|intentional(?:ly)?)\b",
                      _re.I)
_REMAINDER = _re.compile(r"\b(later|next|not yet|deferred|owed|blocked|remains?)\b", _re.I)
_COUNT = (r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
          r"all|every|the whole|complete|entire(?:ty)?)\b\s+(?:of\s+)?(?:the\s+)?"
          r"(?:[a-z-]+\s+)?(?:law|famil|item|rule|propert|heuristic|approach)\w*")
# A count of a SOURCE's items: the count-noun followed by its provenance ("of the paper",
# "from RFC 9110", "in Hughes"). "88 rule(s), nothing unaccounted for" is a tool's tally
# and "all 85 laws" is a catalogue's own length — neither claims to enumerate a source,
# so neither is this decider's. Precision over recall: the census node in the ledger is
# the harness; this decider only refuses the sentence that skips it.
_COUNTED = _re.compile(
    rf"{_COUNT}\s+(?:of|from|in)\s+(?:the\s+)?(?:paper|source|spec|rfc|standard|book|"
    rf"guide|heuristics|census|catalogue|[A-Z]\w+)", _re.S)


def _words(c: dict) -> str:
    """Everything a claim says, in one string: its text, its gaps, its notes."""
    parts = [str(c.get("text", "")), str(c.get("still_broken", "")), str(c.get("note", ""))]
    for e in c.get("evidence") or []:
        parts.append(str(e.get("what", "")))
        parts.append(str(e.get("gap", "")))
    return " ".join(parts)


def check_deliberate_names_its_decision(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A claim that calls a state deliberate carries `decided_at`: the ledger node, issue
    or commit where somebody decided it. The word is not evidence of the decision."""
    out = []
    for i, c in enumerate(claims):
        m = _INTENT.search(_words(c))
        if not m or str(c.get("decided_at") or "").strip():
            continue
        out.append(ClaimFinding(_law("deliberate-names-its-decision"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                f"'{m.group(0)}' with no `decided_at` — a state nobody is "
                                "shown to have decided is an accident wearing a choice"))
    return out


def check_a_remainder_names_its_debt(name: str, claims: list[dict]) -> list[ClaimFinding]:
    """A done/fixed claim that names a remainder carries `owed`: the debt entries that
    hold what was not delivered. A remainder in prose is gone with the scrollback."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") not in ("done", "fixed"):
            continue
        gaps = " ".join(str(e.get("gap", "")) for e in c.get("evidence") or [])
        m = _REMAINDER.search(gaps)
        if not m or c.get("owed"):
            continue
        out.append(ClaimFinding(_law("a-remainder-names-its-debt"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                f"the gap says '{m.group(0)}' and no `owed` names the debt "
                                "that carries it — a half-done job reported as done"))
    return out


def check_a_census_is_read_from_its_source(name: str, claims: list[dict]
                                           ) -> list[ClaimFinding]:
    """A done-claim that states a count of laws, families, items or rules — or claims
    all of them — carries `census`: the node where the source's own list lives, each
    entry covered or owed. A count grounded on the catalogue's own length is a count
    of what was built, not of what the source says."""
    out = []
    for i, c in enumerate(claims):
        if c.get("kind") != "done":
            continue
        m = _COUNTED.search(_words(c))
        if not m or str(c.get("census") or "").strip():
            continue
        out.append(ClaimFinding(_law("a-census-is-read-from-its-source"),
                                f"{name}#{i + 1}", str(c.get("text", ""))[:120],
                                f"'{m.group(0)}' with no `census` naming the source's own "
                                "list — an enumeration that may be filtered by what was "
                                "feasible"))
    return out


CHECKS = (check_done_is_observed, check_fixed_reproduced_first,
          check_one_candidate_per_fix, check_theories_carry_observations,
          check_detours_say_so, check_deliberate_names_its_decision,
          check_a_remainder_names_its_debt, check_a_census_is_read_from_its_source)


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
        {"kind": "done", "text": "the app deliberately ships without the lib",
         "evidence": [{"where": "user-surface", "what": "seen"}]},
        {"kind": "done", "text": "the natives are built",
         "evidence": [{"where": "user-surface", "what": "seen",
                       "gap": "the abstraction function comes later"}]},
        {"kind": "done", "text": "the nine families of the paper are catalogued",
         "evidence": [{"where": "user-surface", "what": "seen"}]},
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
        {"kind": "done", "text": "the app ships without the lib on purpose",
         "decided_at": "ledger: the-runtime-image-carries-no-verifier",
         "evidence": [{"where": "user-surface", "what": "seen"}]},
        {"kind": "done", "text": "the natives are built",
         "owed": ["four-families-compare-two-stretches"], "census": "hughes-2020-census",
         "evidence": [{"where": "user-surface", "what": "seen",
                       "gap": "four families are owed, not yet witnessed by a tape"}]},
        {"kind": "done", "text": "all 31 properties of the paper are catalogued",
         "census": "hughes-2020-census",
         "evidence": [{"where": "user-surface", "what": "seen"}]},
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
