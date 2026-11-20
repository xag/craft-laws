"""A census: Barbara Every, Proofreading Marks at a Glance (BioMedical Editor, 2009), whole.

It roots a-correction-is-marked-in-the-line-and-in-the-margin, and a source is adopted entire
or not at all (the source-the-rule protocol). The sheet is one page: two sentences on how the
marks are placed, then a table giving, for each correction, its marginal mark and its textual
mark. The census unit is each of the two sentences and each instruction of the table, read on
2026-11-20 from the PDF at amstp.northwestern.edu/documents/proofreading-marks-at-a-glance.pdf
(text extracted with pdftotext; the marks themselves are glyphs the extraction does not keep,
so a row names the instruction). Each instruction is the vocabulary of correcting typeset pages
by hand; it is set aside as that vocabulary, the placement rule it follows being the law's.
BS 5261-2:2005 states the same two-mark convention; its text is sold and was not read.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_proofreading_marks
"""

from __future__ import annotations

# The table's instructions, in the sheet's order (its two columns read left then right).
_INSTRUCTIONS = (
    "insert", "delete", "insert space", "insert thin space", "insert 1-em space",
    "close up space", "delete + close up", "spell out", "substitute", "transpose",
    "new paragraph", "no paragraph", "break line", "move left", "move right", "move up",
    "move down", "center", "align vertically", "capitalize", "lowercase",
    "capitalize + lowercase", "set small caps", "set italic", "set boldface", "set lightface",
    "set roman", "set superscript", "insert subscript", "wrong font", "stet (let it stand)",
    "insert period", "insert comma", "insert colon", "insert semicolon",
    "insert question mark", "insert hyphen", "set en dash", "set em dash", "insert apostrophe",
    "insert quotation marks", "insert parentheses", "insert brackets", "set minus sign",
    "insert equals sign", "set prime sign",
)

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Proofreading marks (also called proofreaders' marks) are symbols and notations for correcting typeset pages. The proofreader places these marks in the margins and in corresponding lines of text.": (
        "covered", "a-correction-is-marked-in-the-line-and-in-the-margin", "quoted by the law"),
    "A slash separates marginal marks that appear on the same line.": (
        "owed", "", "several corrections on one line keep their margin marks apart; decidable"),
    **{f"The table: the marginal and the textual mark to {i}.": (
        "set aside", "", "the vocabulary of one correction; placed as the law says")
       for i in _INSTRUCTIONS},
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 48


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_proofreading_marks",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the sheet's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Every, Proofreading Marks at a Glance: {len(CENSUS)} classified\n")
    for rule, (route, law, note) in CENSUS.items():
        print(f"  {route:<9} {rule}")
        if law:
            print(f"            -> {law}")
    print()
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    if missing:
        for rule, law in missing:
            print(f"\n  BROKEN  {rule} names law {law!r} and no such law exists")
        return 1
    print("\n  Every covered rule names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
