"""A census: the GOV.UK Design System's Details component, whole.

It is cited by content-most-people-need-is-not-folded-away, and a source is adopted entire or not
at all (the source-the-rule protocol). The census unit is each guideline sentence of the page's
guidance, read on 2026-11-20 at https://design-system.service.gov.uk/components/details/, from
"When to use this component" to "Write clear link text". The research section reports findings
and the change log states no guideline.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"information that only some users will need" for closing what holds behind one heading.

    python -m craft.census_govuk_details
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Use the details component to make a page easier to scan when it contains information that only some users will need.': (
        'covered', 'rare-actions-go-to-a-second-layer', 'what few need goes to a second layer'),
    'Do not use the details component to hide information that the majority of your users will need.': (
        'covered', 'content-most-people-need-is-not-folded-away', 'quoted by the law'),
    'Use the details component instead of tabs or an accordion if you only have 1 section of content.': (
        'owed', '', 'decidable by counting the sections'),
    'The details component is less visually prominent than tabs and accordions, so tends to work better for content which is not as important to users.': (
        'set aside', '', "a 'tends to'; a reading of importance"),
    'Make the link text short and descriptive so users can quickly work out if they need to click on it.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', 'the summary says what it holds'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 5


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_govuk_details",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} guidelines")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"GOV.UK Design System, Details: {len(CENSUS)} classified\n")
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
    print("\n  Every covered guideline names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
