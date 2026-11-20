"""A census: Microsoft Support, Check spelling and grammar in Office, whole.

A source is adopted entire or not at all (the source-the-rule protocol), and this one states no
rule craft-laws lacks: it is the help page of one product family, saying what the products do,
and a product doing a thing is a precedent, not a rule. The census unit is each section of the
page under its two tabs, Windows and macOS (the macOS tab per program: Word, Outlook,
PowerPoint, Excel), read on 2026-11-20 at
support.microsoft.com/en-us/office/check-spelling-and-grammar-in-office-5cdeced7-d81d-47de-9096-efd0ee909227.
Every row is set aside as a description; where a section agrees with a law the note says so.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20, which cited the squiggly underline under a word
and Word's going through the errors one by one.

    python -m craft.census_ms_spelling
"""

from __future__ import annotations

_DESC = "describes the products; states no rule"

# section -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- Windows ------------------------------------------------------------------------------
    "All Microsoft Office programs can check spelling, and most can check grammar.": (
        "set aside", "", _DESC),
    "Run the spelling and grammar checker: To start a check of the spelling and grammar in your document, just press F7.": (
        "set aside", "", _DESC),
    "Show errors automatically while you work: ... Office marks potential spelling errors with a red squiggly line, and potential grammatical errors are marked with a blue squiggly line. ... right-click on the underlined word or phrase and choose one of the options to fix the error.": (
        "set aside", "",
        _DESC + "; a mark at the word is an-indicator-sits-beside-what-it-marks in one "
        "product, and two colours alone would break colour-is-never-the-only-signal"),
    "Turn the multicolored underlining on or off: Check spelling as you type; Mark grammar errors as you type; per document in Word.": (
        "set aside", "", _DESC),
    "Turn grammar checking off entirely: clear Mark grammar errors as you type and Check grammar with spelling.": (
        "set aside", "", _DESC),
    "Recheck spelling and grammar that you previously ignored: Proofing, Recheck Document.": (
        "set aside", "", _DESC),
    # --- macOS, Word --------------------------------------------------------------------------
    "Word: Check spelling and grammar automatically as you type: Word marks potential spelling errors with a red squiggly line, and potential grammatical errors are marked with a green squiggly line.": (
        "set aside", "", _DESC),
    "Word: Turn automatic spelling and grammar checking on or off: Preferences, Spelling & Grammar.": (
        "set aside", "", _DESC),
    "Word: Check spelling and grammar all at once: ... After you correct, ignore, or skip an error, Word moves to the next one. When Word finishes reviewing the document, you'll see a message that the spelling and grammar check is complete.": (
        "set aside", "", _DESC),
    "Word: Recheck the spelling and grammar that you previously checked and chose to ignore: Reset Ignored Words and Grammar.": (
        "set aside", "", _DESC),
    # --- macOS, Outlook -----------------------------------------------------------------------
    "Outlook: Check spelling and grammar automatically as you type: a dashed red underline for possible spelling errors and a dashed green line for possible grammatical errors.": (
        "set aside", "", _DESC),
    "Outlook: Turn automatic spelling and grammar checking on or off: Settings, Spelling and Grammar.": (
        "set aside", "", _DESC),
    "Outlook: Check spelling and grammar all at once: Edit, Spelling and Grammar; Ignore once, Ignore all, Add to dictionary; Cmd+; skips to the next error.": (
        "set aside", "", _DESC),
    # --- macOS, PowerPoint --------------------------------------------------------------------
    "PowerPoint: Check spelling automatically as you type: PowerPoint automatically checks for and marks potential spelling errors with a wavy, red underline.": (
        "set aside", "", _DESC),
    "PowerPoint: Turn automatic spell checking on or off: Preferences, Proofing.": (
        "set aside", "", _DESC),
    "PowerPoint: Check spelling all at once: ... After you correct, ignore, or skip an error, PowerPoint moves to the next one.": (
        "set aside", "", _DESC),
    # --- macOS, Excel -------------------------------------------------------------------------
    "Excel: Check spelling all at once: Review, Spelling; Change, Change All, Ignore Once, Ignore All; the dialog does not open if no errors are detected.": (
        "set aside", "", _DESC),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 17


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_ms_spelling",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Microsoft Support, Check spelling and grammar in Office: {len(CENSUS)} classified\n")
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
