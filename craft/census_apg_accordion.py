"""A census: W3C WAI, ARIA Authoring Practices Guide, Accordion Pattern, whole.

It roots an-accordion-header-is-a-button-alone-inside-a-heading, and a source is adopted entire
or not at all (the source-the-rule protocol). The census unit is each bullet of the pattern's
Keyboard Interaction and WAI-ARIA Roles, States, and Properties, read on 2026-11-20 at
https://www.w3.org/WAI/ARIA/apg/patterns/accordion/. "About This Pattern" defines its terms and
asks nothing.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
its header, a button alone inside a heading, against rows that put a heading inside a button.

    python -m craft.census_apg_accordion
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Enter or Space: When focus is on the accordion header for a collapsed panel, expands the associated panel. If the implementation allows only one panel to be expanded, and if another panel is expanded, collapses that panel.': (
        'owed', '', "decidable by keys sent to the header and the panels' states after"),
    'Enter or Space: When focus is on the accordion header for an expanded panel, collapses the panel if the implementation supports collapsing.': (
        'owed', '', 'decidable the same way'),
    'Tab: Moves focus to the next focusable element; all focusable elements in the accordion are included in the page Tab sequence.': (
        'owed', '', 'decidable by a focus walk'),
    'Shift + Tab: Moves focus to the previous focusable element; all focusable elements in the accordion are included in the page Tab sequence.': (
        'owed', '', 'decidable by a focus walk'),
    'The title of each accordion header is contained in an element with role button.': (
        'covered', 'an-accordion-header-is-a-button-alone-inside-a-heading', 'the button'),
    'Each accordion header button is wrapped in an element with role heading that has a value set for aria-level that is appropriate for the information architecture of the page.': (
        'covered', 'an-accordion-header-is-a-button-alone-inside-a-heading', 'quoted by the law'),
    'If the native host language has an element with an implicit heading and aria-level, such as an HTML heading tag, a native host language element may be used.': (
        'set aside', '', 'a permission'),
    'The button element is the only element inside the heading element.': (
        'covered', 'an-accordion-header-is-a-button-alone-inside-a-heading', 'quoted by the law'),
    'If the accordion panel associated with an accordion header is visible, the header button element has aria-expanded set to true. If the panel is not visible, aria-expanded is set to false.': (
        'covered', 'an-accordion-header-is-a-button-alone-inside-a-heading', 'quoted by the law'),
    'The accordion header button element has aria-controls set to the ID of the element containing the accordion panel content.': (
        'covered', 'an-accordion-header-is-a-button-alone-inside-a-heading', 'the panel named'),
    'If the accordion panel associated with an accordion header is visible, and if the accordion does not permit the panel to be collapsed, the header button element has aria-disabled set to true.': (
        'owed', '', 'decidable from the DOM'),
    'Optionally, each element that serves as a container for panel content has role region and aria-labelledby with a value that refers to the button that controls display of the panel.': (
        'set aside', '', 'optional'),
    'Avoid using the region role in circumstances that create landmark region proliferation, e.g., in an accordion that contains more than approximately 6 panels that can be expanded at the same time.': (
        'owed', '', 'decidable by counting region panels'),
    'Role region is especially helpful to the perception of structure by screen reader users when panels contain heading elements or a nested accordion.': (
        'set aside', '', 'explains the option'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 14


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apg_accordion",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the pattern's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"W3C WAI APG, Accordion Pattern: {len(CENSUS)} classified\n")
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
