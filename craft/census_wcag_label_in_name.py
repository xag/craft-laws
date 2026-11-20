"""A census: W3C, Understanding WCAG 2.2, Success Criterion 2.5.3 Label in Name, whole.

It roots the-accessible-name-contains-the-visible-label, and a source is adopted entire or not at
all (the source-the-rule protocol). craft/census_wcag.py routes the criterion itself; this is its
Understanding document. The census unit is each statement of what an author does or must do: the
In Brief advice, the criterion and its note, the intent's requirements, and the sufficient and
advisory techniques and failures, read on 2026-11-20 at
https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html. The benefits, examples and key
terms ask nothing of their own.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"A best practice is to have the text of the label at the start of the name" for buttons named by their words, then their flaw.

    python -m craft.census_wcag_label_in_name
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Where practical, make the control's text label and name match.": (
        'covered', 'the-accessible-name-contains-the-visible-label', 'the In Brief advice'),
    'For user interface components with labels that include text or images of text, the name contains the text that is presented visually.': (
        'covered', 'the-accessible-name-contains-the-visible-label', 'quoted by the law'),
    'A best practice is to have the text of the label at the start of the name.': (
        'covered', 'the-accessible-name-contains-the-visible-label', 'quoted by the law'),
    'it is best to conservatively interpret the label as being only the text in close proximity.': (
        'owed', '', "which text is the label: decidable from the layout's adjacency"),
    'text should not be considered a visible label if it is used in a symbolic manner [...] the accessible name should be the function the button serves': (
        'owed', '', 'a symbol is a reading; a name that repeats the symbol is decidable'),
    "it's still a good idea for authors to match the case/capitalization of the visible label and the accessible name in these cases.": (
        'owed', '', 'decidable from the two strings'),
    'The label should not be overwritten in the accessible name, and substitutions of words where a formula is used should be avoided [...] The proper operator symbol (in this case the &times; symbol) should be used.': (
        'owed', '', 'decidable from the two strings'),
    'when a visible label already exists, aria-label should be avoided or used carefully, and aria-labelledby should be used as a supplement with care.': (
        'owed', '', 'decidable from the DOM'),
    'the context of headings, instructions, and group labels can be provided through the accessible description': (
        'owed', '', 'decidable from the DOM: context in the description, not the name'),
    'where parenthetical information provides important context, such as indication of a required field or limitations on what is allowed for input, this information must be provided programmatically in some other way': (
        'owed', '', 'decidable from the DOM (required, aria-describedby)'),
    'G208: Including the text of the visible label as part of the accessible name': (
        'covered', 'the-accessible-name-contains-the-visible-label', 'the law'),
    'G211: Matching the accessible name to the visible label': (
        'covered', 'the-accessible-name-contains-the-visible-label', 'the law'),
    'G162: Positioning labels to maximize predictability of relationships': (
        'owed', '', 'a-checkbox-sits-left-of-its-label holds it for checkboxes'),
    'If an icon has no accompanying text, consider using its hover text as its accessible name (Potential future technique)': (
        'owed', '', 'decidable from the DOM'),
    'F96: Failure due to the accessible name not containing the visible label text': (
        'covered', 'the-accessible-name-contains-the-visible-label', "the law's falsifier"),
    'F111: Failure of Success Criteria 1.3.1, 2.5.3, and 4.1.2 due to a control with visible label text but no accessible name': (
        'covered', 'the-accessible-name-contains-the-visible-label', "the law's falsifier"),
    'Accessible name contains the visible label text, but the words of the visible label are not in the same order as they are in the visible label text (Potential future technique)': (
        'covered', 'the-accessible-name-contains-the-visible-label', "the law's falsifier"),
    'Accessible name contains the visible label text, but one or more other words are interspersed in the label (Potential future technique)': (
        'covered', 'the-accessible-name-contains-the-visible-label', "the law's falsifier"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 18


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_wcag_label_in_name",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Understanding WCAG 2.2, SC 2.5.3 Label in Name: {len(CENSUS)} classified\n")
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
    print("\n  Every covered statement names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
