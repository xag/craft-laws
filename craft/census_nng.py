"""The census of Nielsen's ten heuristics, none skipped.

NN/g roots FIVE interface laws — no-system-vocabulary (#2), a-way-back (#3),
one-act-one-name (#4), status-is-visible (#1), rare-action-folds-away and
one-surface-one-job (#8) — and the set was never censused. Five heuristics used,
five unread: the picked-item defect `a-census-is-read-from-its-source` names, in
the source this family quotes most often.

What prompted it, 2026-09-14: a page built in a language-learning app for choosing what
to practise from opened on sixty words of policy prose above its search box, gave
every result two buttons where one would do, kept a rarely-used upload form
permanently expanded, and ran to eight phone screens. The founder: "atrocious.
typical Claude. lunatic." Every one of those was already a breach of a law in this
file — rare-action-folds-away's own sighting reads "its largest element was a
fully-expanded create-a-new-team form" — and nothing looked. THE LAW WAS NOT
MISSING; THE CHECK WAS. That is the finding this census exists to record, and it
is why the routes below are honest about how few of these a machine can decide.

The census unit is the source's own list: the ten numbered heuristics at
nngroup.com/articles/ten-usability-heuristics/ (Jakob Nielsen, first published
1994-04-24, last reviewed 2024-01-30), rooted in Molich & Nielsen 1990, "Improving
a human-computer dialogue", and Nielsen 1994, "Enhancing the explanatory power of
usability heuristics". The heuristic NAMES and the quoted sentences are the
source's words.

    python -m craft.census_nng

Routes, as census_wcag and census_rgaa use them:
  covered  a law in craft/laws.py carries it and a decider can reach it
  vocab    a law could carry it once some fact about the work is recorded
  judge    it stays a reading; no decider is honest for it
"""

from __future__ import annotations

# heuristic -> (route, the laws that carry it, one line on the mapping)
CENSUS: dict[str, tuple[str, tuple[str, ...], str]] = {
    "1. Visibility of System Status": (
        "covered", ("status-is-visible",),
        "the heuristic rooted this law directly; a state change that is only "
        "visual, or only in a place the reader is not looking, is its falsifier"),
    "2. Match Between the System and the Real World": (
        "covered", ("no-system-vocabulary",),
        "the heuristic rooted this law directly: a word on screen that only the "
        "people who built it use"),
    "3. User Control and Freedom": (
        "covered", ("a-way-back", "escape-closes-the-overlay"),
        "the marked exit, and the one exit a keyboard always expects"),
    "4. Consistency and Standards": (
        "covered", ("one-act-one-name", "one-act-one-look-one-place", "navigation-keeps-its-order"),
        "one act under one name, with one look in one place, and the order a person "
        "learned once kept everywhere it is repeated"),
    "5. Error Prevention": (
        "covered", ("check-before-commit", "validate-at-field-exit",
                    "destructive-is-set-apart", "no-disabled-submit",
                    "known-date-three-boxes", "no-autocorrect-on-identifiers"),
        "the heuristic's own emphasis — the best design prevents the problem — "
        "carried by six laws over the commit, the field and the keyboard"),
    "6. Recognition Rather than Recall": (
        "vocab", ("no-placeholder-labels",),
        "one mechanical edge is covered: a label that vanishes when you type is a "
        "label you must remember. The heuristic's body — that options are VISIBLE "
        "rather than remembered across a flow — needs a fact nothing records: "
        "which of a flow's steps depend on something shown in an earlier one"),
    "7. Flexibility and Efficiency of Use": (
        "judge", (),
        "no law, and none is honest: whether a shortcut speeds an expert without "
        "confusing a novice is a reading about two populations, and nothing here "
        "records which of them is at the screen"),
    "8. Aesthetic and Minimalist Design": (
        "covered", ("rare-action-folds-away", "one-surface-one-job", "say-it-once",
                    "paragraphs-stay-under-five-sentences",
                    "a-screen-carries-no-words-nobody-acts-on"),
        "the frequency half and the one-job half are each a law, and both were "
        "breached by the page that prompted this census. WHAT NO LAW HERE DECIDES "
        "is the heuristic's own second sentence — that every extra unit competes "
        "with the relevant ones — as a property of a screen taken whole. That is "
        "not a threshold anybody can root; it is a quantity that should not grow "
        "unnoticed, so a language-learning app records it per screen inductively "
        "(tools/prose.py), the way tools/answers.py records the words of a tool's "
        "answer: no budget, no reading, the ceiling is what stands today"),
    "9. Help Users Recognize, Diagnose, and Recover from Errors": (
        "covered", ("error-names-the-culprit", "error-says-the-fix",
                    "error-neither-begs-nor-blames", "error-lands-at-the-field"),
        "the heuristic's three clauses — plain language, precisely indicate the "
        "problem, constructively suggest a solution — are three of these four; "
        "the fourth puts the message where the problem is"),
    "10. Help and Documentation": (
        "vocab", ("terms-defined-before-use", "a-readme-answers-what-why-how"),
        "the doc lane carries what documentation must do once it exists. The "
        "heuristic's actual claim — that it is best if the system needs none — "
        "needs a fact nothing records: which tasks a person completed without "
        "reaching for help"),
}

ROUTES = ("covered", "zero", "vocab", "judge")
SOURCE_COUNT = 10
SOURCE = ("Jakob Nielsen, 10 Usability Heuristics for User Interface Design, "
          "Nielsen Norman Group, published 1994-04-24, last reviewed 2024-01-30")
SOURCE_URL = "https://www.nngroup.com/articles/ten-usability-heuristics/"


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    assert len(CENSUS) == SOURCE_COUNT, "the source states ten; none may be skipped"
    from craft.laws import LAWS
    ids = {law.id for law in LAWS}
    missing = [(h, name) for h, (_, laws, _) in CENSUS.items()
               for name in laws if name not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"{SOURCE}: {len(CENSUS)} heuristics classified, none skipped\n")
    for heuristic, (route, laws, note) in CENSUS.items():
        print(f"  {route:<8} {heuristic}")
        print(f"           -> {', '.join(laws) if laws else '(no law, and none honest)'}")
    print()
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    if missing:
        for heuristic, name in missing:
            print(f"\n  BROKEN  {heuristic} names law {name!r} and no such law exists")
        return 1
    print("\n  Every heuristic names laws that exist in laws.py — checked against the "
          "laws, not asserted.")
    print("  Five of the ten already rooted a law and the set was never read whole; "
          "reading it whole found no heuristic this family had misread, and two it "
          "cannot honestly decide at all.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
