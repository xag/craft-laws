"""A census: Hoa Loranger, Accordions Are Not Always the Answer for Complex Content on Desktops (Nielsen Norman Group, 2014-05-18), whole.

It roots content-most-people-need-is-not-folded-away, and a source is adopted entire or not at
all (the source-the-rule protocol). The census unit is each guideline sentence of the article,
read on 2026-11-20 at https://www.nngroup.com/articles/accordions-complex-content/ (the research
named it "Accordions on Desktop: When and How to Use"): the usability issues, the myths and the
criteria. The advantages it lists first describe accordions and ask nothing.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
it to weigh showing every flaw at once against rows that open, and to fold what holds behind a count.

    python -m craft.census_nng_accordions
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "If people need to open the majority of subtopics to have their questions answered or to get the full story then an accordion is not the way to go. In this situation, it's better to expose all the content at once.": (
        'covered', 'content-most-people-need-is-not-folded-away', 'quoted by the law'),
    'Headings and titles must be descriptive and enticing enough to motivate people to “spend” clicks on them.': (
        'covered', 'headings-and-labels-describe-topic-or-purpose', "the descriptive half; 'enticing' is a reading"),
    'Pages and widgets must be coded with accessibility in mind': (
        'owed', '', "an accordion's markup (button, aria-expanded, region) is decidable from the DOM"),
    'Make sure to optimize your pages for printing.': (
        'owed', '', 'decidable by printing the page with its sections closed'),
    "While you should still be mindful of people's limited attention span on websites and prioritize content wisely, you shouldn't fear long formats.": (
        'set aside', '', 'a reading of what to put first'),
    'Websites should not be information light. The same information needs to be written, structured, and presented differently.': (
        'set aside', '', 'a reading of how much to say'),
    'The best place to start when deciding to use an accordion is to evaluate common and critical use cases for your audience.': (
        'owed', '', "needs a new fact: the view's use cases, recorded"),
    'Accordions should be avoided when your audience needs most or all of the content on the page to answer their questions.': (
        'covered', 'content-most-people-need-is-not-folded-away', 'quoted by the law'),
    'If your pages are extremely long, perhaps the accordion is not the appropriate widget. [...] However, avoid the temptation to go extreme by cutting up content into short tiny pages.': (
        'set aside', '', "a 'perhaps'; how long is too long is a reading"),
    'If you do use accordions, make sure to give people the capability to open multiple sections at a time': (
        'owed', '', 'decidable by opening two sections'),
    'Items that are opened or closed should remain in that state until the user changes it.': (
        'owed', '', "decidable by reading each section's state across a re-render"),
    'Accordions are more suitable when people need only a few key pieces of content on a single page.': (
        'covered', 'rare-actions-go-to-a-second-layer', 'nothing rarely needed on the first layer (NN/g heuristic #8)'),
    'Another situation in which accordions are helpful is when the information is restricted to very small spaces, such as on mobile devices.': (
        'owed', '', "decidable at a phone's width once the use is recorded"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 13


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_accordions",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the article's {SOURCE_COUNT} guidelines")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Loranger, Accordions Are Not Always the Answer for Complex Content on Desktops: {len(CENSUS)} classified\n")
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
