"""A census: Page Laubheimer and Raluca Budiu, Accordion Icons: Which Signifiers Work Best? (Nielsen Norman Group, 2020-08-23), whole.

It roots content-that-opens-in-place-is-marked-with-a-caret, and a source is adopted entire or not
at all (the source-the-rule protocol). The census unit is each recommendation the article makes:
its Design Recommendations, its Summary, and the key findings it words as advice, read on
2026-11-20 at https://www.nngroup.com/articles/accordion-icons/. The method and the results
report the study and ask nothing.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"the caret appears to be the safest icon choice" against a right-pointing chevron on rows that open in place.

    python -m craft.census_nng_accordion_icons
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'If using accordions in your mobile menus, the caret appears to be the safest icon choice.': (
        'covered', 'content-that-opens-in-place-is-marked-with-a-caret', 'quoted by the law'),
    "Do not have icons and text labels link to different actions (i.e. label directly to page, icon opening an accordion). [...] it's not safe to use split buttons for accordions": (
        'owed', '', 'decidable: a header whose icon and label have different targets'),
    'Decide if your menu items will either open a submenu accordion or go directly to a category-overview page. If you choose to have your menu items link directly to a landing page, do not use a right-aligned icon.': (
        'owed', '', 'decidable: a link to a page carrying a right-aligned icon'),
    'Use a caret icon to designate an accordion, whether on desktop or mobile': (
        'covered', 'content-that-opens-in-place-is-marked-with-a-caret', 'quoted by the law'),
    "Making up new icons for accordion signifiers or using no signifiers at all is not a good idea as they violate users' expectations (which are that they will be taken to a new page).": (
        'covered', 'content-that-opens-in-place-is-marked-with-a-caret', "the law's falsifier"),
    'The arrow is not statistically different than the foil or no-icon conditions, suggesting that this icon should not be used for accordions.': (
        'covered', 'content-that-opens-in-place-is-marked-with-a-caret', 'quoted by the law'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 6


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_accordion_icons",
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
    print(f"Laubheimer & Budiu, Accordion Icons: Which Signifiers Work Best?: {len(CENSUS)} classified\n")
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
