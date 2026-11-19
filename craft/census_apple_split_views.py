"""A census: Apple's Human Interface Guidelines page on split views, whole.

It roots resizable-panes-have-limits-that-keep-the-divider-usable, and a source is adopted
entire or not at all (the source-the-rule protocol). The census unit is each guideline
sentence of the page, read on 2026-11-19 through its data file
(developer.apple.com/tutorials/data/design/human-interface-guidelines/split-views.json):
Best practices and every platform's section. The sentences that explain a guideline, and the
cross-references to developer documentation, state none of their own.

What prompted it: the review of a written design for dividers that size a navigator's side
panels.

    python -m craft.census_apple_split_views
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'To support navigation, persistently highlight the current selection in each pane that leads to the detail view.': (
        'owed', '', 'decidable from the DOM: the selected row marked in each leading pane'),
    'Consider letting people drag and drop content between panes.': (
        'owed', '', "a 'consider'; whether moving content suits the app is a reading"),
    'Prefer using a split view in a regular - not a compact - environment.': (
        'owed', '', "decidable: panes side by side at a phone's portrait width"),
    'Account for narrow, compact, and intermediate window widths.': (
        'owed', '', 'decidable by laying the split out at each width'),
    "In particular, ensure that it's possible to navigate between the various panes in a logical way.": (
        'owed', '', 'the order focus and navigation take between panes; partly a reading'),
    'A split view includes dividers between panes that can support dragging to resize them.': (
        'set aside', '', 'describes the control; it asks nothing'),
    'Set reasonable defaults for minimum and maximum pane sizes.': (
        'covered', 'resizable-panes-have-limits-that-keep-the-divider-usable', 'quoted by the law'),
    "If people can resize the panes in your app's split view, make sure to use sizes that keep the divider visible.": (
        'covered', 'resizable-panes-have-limits-that-keep-the-divider-usable', 'quoted by the law'),
    'Consider letting people hide a pane when it makes sense.': (
        'owed', '', "a 'consider'; when it makes sense is a reading"),
    'Provide multiple ways to reveal hidden panes.': (
        'owed', '', 'decidable once a pane can hide: more than one control restores it'),
    'Prefer the thin divider style.': (
        'owed', '', "decidable from the divider's drawn width"),
    'Avoid using thicker divider styles unless you have a specific need.': (
        'owed', '', "the same measurement, with the page's stated exception"),
    'Choose a split view layout that keeps the panes looking balanced.': (
        'set aside', '', 'tvOS: a living-room screen with a remote'),
    'Display a single title above a split view, helping people understand the content as a whole.': (
        'set aside', '', 'tvOS'),
    "Choose the title's alignment based on the type of content the secondary pane contains.": (
        'set aside', '', 'tvOS'),
    'To display supplementary information, prefer a split view instead of a new window.': (
        'set aside', '', 'visionOS: windows in space'),
    'If you need to request a small amount of information or present a simple task that someone must complete before returning to their main task, use a sheet.': (
        'set aside', '', 'visionOS'),
    'Automatically display the most relevant detail view.': (
        'set aside', '', 'watchOS: a split shown one view at a time'),
    'If your app displays multiple detail pages, place the detail views in a vertical tab view.': (
        'set aside', '', 'watchOS'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 19


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apple_split_views",
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
    print(f"Apple HIG, Split views: {len(CENSUS)} classified\n")
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
