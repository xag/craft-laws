"""The fifth practice census: Agans's nine debugging rules, none skipped.

Agans rooted four practice laws on the day the family was founded and was never
censused — nine rules, four used, five unread, which is the picked-item defect
`a-census-is-read-from-its-source` names, standing since 2026-08-17 in the source
that started the family. The census unit is the book's own list: chapter 2, "The
Rules — Suitable for Framing", downloaded from the author's site
(debuggingrules.com/Debugging_CH2.PDF) and quoted from that text. The rule NAMES are
the source's words; where a law transfers a rule from debugging hardware to judging
work, the transfer is the law's own note and never presented as the book's.

    python -m craft.census_agans
"""

from __future__ import annotations

# rule -> (route, the law that carries it, one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "UNDERSTAND THE SYSTEM": (
        "covered", "the-systems-own-record-is-read-first",
        "minted 2026-08-24 from this census: a chase begins by reading what the "
        "system says about itself — the manual, the ledger, the trigger on the law"),
    "MAKE IT FAIL": (
        "covered", "make-it-fail-before-you-fix-it",
        "founding law of the family, 2026-08-17"),
    "QUIT THINKING AND LOOK": (
        "covered", "instrument-before-the-second-theory",
        "founding law of the family, 2026-08-17"),
    "DIVIDE AND CONQUER": (
        "covered", "a-hunt-narrows-the-space",
        "minted 2026-08-24 from this census, with its falsifier honestly weak — "
        "whether a step narrowed the space is often a reading; the law says so"),
    "CHANGE ONE THING AT A TIME": (
        "covered", "one-candidate-fix-per-deploy",
        "founding law of the family, 2026-08-17"),
    "KEEP AN AUDIT TRAIL": (
        "covered", "the-trail-is-written-as-it-happens",
        "minted 2026-08-24 from this census: the claims record and the flight tapes "
        "are this rule practised; the law is what makes skipping them a breach"),
    "CHECK THE PLUG": (
        "covered", "the-baseline-assumption-is-verified",
        "minted 2026-08-24 from this census"),
    "GET A FRESH VIEW": (
        "covered", "a-resisting-failure-gets-fresh-eyes",
        "minted 2026-08-24 from this census"),
    "IF YOU DIDN'T FIX IT, IT AIN'T FIXED": (
        "covered", "done-is-observed-where-the-user-stands",
        "founding law of the family, 2026-08-17"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 9


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_agans",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the book's {SOURCE_COUNT} rules")
        return 1

    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE}
    missing = [(rule, law) for rule, (_, law, _) in CENSUS.items() if law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Agans, the nine debugging rules (chapter 2, the author's own PDF): "
          f"{len(CENSUS)} classified\n")
    for rule, (route, law, note) in CENSUS.items():
        print(f"  {route:<9} {rule}")
        print(f"            -> {law}")
    print()
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    if missing:
        for rule, law in missing:
            print(f"\n  BROKEN  {rule} names law {law!r} and no such law exists")
        return 1
    print("\n  Every rule names a law that exists in practice.py — checked against "
          "the laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
