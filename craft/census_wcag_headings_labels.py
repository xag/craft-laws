"""A census: W3C, Understanding WCAG 2.2, Success Criterion 2.4.6 Headings and Labels, whole.

It roots headings-and-labels-describe-topic-or-purpose, and a source is adopted entire or not at
all (the source-the-rule protocol). craft/census_wcag.py routes the criterion itself; this is
its Understanding document, a different text. The census unit is each statement of what an
author does or must do: the criterion, the intent's requirements, and the sufficient and
advisory techniques, read on 2026-11-20 at
https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html. The In Brief box restates
the criterion; the benefits, examples and key terms explain and ask nothing of their own.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
"Descriptive labels help users identify specific components" against six buttons under one name.

    python -m craft.census_wcag_headings_labels
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Headings and labels describe topic or purpose.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'quoted by the law'),
    'Labels and headings do not need to be lengthy. A word, or even a single character, may suffice if it provides an appropriate cue to finding and navigating content.': (
        'set aside', '', 'a permission; it asks nothing'),
    'In these cases, authors should ensure that the image and its use as a label (in context) are widely understood.': (
        'owed', '', 'an icon used as a label: its text alternative is decidable, its being widely understood is a reading'),
    'This success criterion requires that if headings or labels are provided, they be descriptive.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', "the law's scope: those present"),
    'This success criterion does not require the use of labels; however, it does require that if labels are present, they must be accurate and sufficiently clear or descriptive.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'the same, for labels'),
    'G130: Providing descriptive headings': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'the heading half'),
    'G131: Providing descriptive labels': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'the label half'),
    'Headings and labels must be programmatically determined, per Success Criterion 1.3.1.': (
        'owed', '', 'WCAG 1.3.1, routed in census_wcag; decidable from the markup'),
    'G201: Giving users advanced warning when opening a new window': (
        'owed', '', 'a link opening a new window with no warning is decidable from the DOM'),
    'SCR24: Using progressive enhancement to open new windows on user request': (
        'owed', '', 'decidable from the DOM and its script'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 10


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_wcag_headings_labels",
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
    print(f"Understanding WCAG 2.2, SC 2.4.6 Headings and Labels: {len(CENSUS)} classified\n")
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
