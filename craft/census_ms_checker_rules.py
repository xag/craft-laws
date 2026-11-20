"""A census: Microsoft Support, Rules for the Accessibility Checker, whole.

It roots a-problem-is-ranked-by-its-severity (beside NN/g) and is cited by
headings-and-labels-describe-topic-or-purpose, and a source is adopted entire or not at all (the
source-the-rule protocol). The census unit is each rule the page states: its instructions to the
reader, its classification of issues, and every row of its tables of errors, warnings, tips and
Intelligent Services, read on 2026-11-20 at
https://support.microsoft.com/en-us/office/rules-for-the-accessibility-checker-651e08f2-0fc3-4e10-aaca-74b4a67101c1
(served from https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker).
A table row's "verifies" and "why fix" columns belong to its rule. The limitations section
states what the checker cannot detect and asks nothing.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its errors, warnings and tips, ranked by consequence, to say a flaw's level must come from what it does.

    python -m craft.census_ms_checker_rules
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "That's why it's important to always review your work visually to find the issues hiding from the Accessibility Checker.": (
        'covered', 'done-is-observed-where-the-user-stands', "a checker's pass is the producer's side; the rendered work is looked at"),
    'Depending on how severe the issue is, the Accessibility Checker classifies each issue as an error, warning, or tip.': (
        'covered', 'a-problem-is-ranked-by-its-severity', "quoted by the law, with the error's definition"),
    'Intelligent Services. Content that is automatically made accessible by AI, and that you should review for accuracy and context': (
        'owed', '', 'generated alt text reviewed before it stands; decidable from a record of review'),
    'you should only use tables when they are necessary to present your data. Avoid tables that only have a layout purpose.': (
        'owed', '', 'a layout table is decidable from the DOM'),
    'All non-text content has alternative text (alt text).': (
        'owed', '', 'WCAG 1.1.1, routed in census_wcag; no law holds it'),
    'Tables specify column header information.': (
        'owed', '', 'WCAG 1.3.1, decidable from the markup'),
    'All sections have meaningful names.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'quoted by the law'),
    'All slides have titles.': (
        'owed', '', "the-title-names-the-place holds it for a window's title, not a slide's"),
    "Cells in an Excel worksheet don't use red-only formatting for negative numbers.": (
        'covered', 'colour-is-never-the-only-signal', 'red alone carrying the sign'),
    'Document access is not restricted.': (
        'owed', '', "decidable from the file's permission settings"),
    'All content control fields have titles.': (
        'covered', 'every-input-labeled', 'a field with no title'),
    'Table has a simple structure.': (
        'owed', '', 'merged, split or nested cells are decidable from the markup'),
    'Sheet tabs have meaningful names.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', "'Sheet1' is the law's default name"),
    'Sufficient contrast between text and background.': (
        'covered', 'text-holds-its-contrast', 'the same measurement'),
    'Closed captions are included for inserted audio and video.': (
        'owed', '', 'WCAG 1.2.2, routed in census_wcag; no law holds it'),
    'The reading order of the objects on a slide presentation is logical.': (
        'owed', '', 'WCAG 1.3.2, routed in census_wcag'),
    'The section names in a deck are unique.': (
        'owed', '', 'decidable from the names'),
    'Slide titles in a deck are unique.': (
        'owed', '', 'decidable from the titles; the-title-names-the-place holds it for windows'),
    'Documents use heading styles.': (
        'owed', '', 'WCAG 1.3.1: headings marked up as headings'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 19


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_ms_checker_rules",
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
    print(f"Microsoft Support, Rules for the Accessibility Checker: {len(CENSUS)} classified\n")
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
