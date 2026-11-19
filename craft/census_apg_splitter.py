"""A census: the W3C WAI ARIA Authoring Practices Guide's Window Splitter Pattern, whole.

It roots a-pane-divider-is-a-focusable-separator-with-its-value and
a-pane-divider-moves-with-the-arrow-keys, and a source is adopted entire or not at all (the
source-the-rule protocol). The census unit is each sentence of the pattern that states what a
splitter is, does or carries, read on 2026-11-19 (w3.org/WAI/ARIA/apg/patterns/windowsplitter/):
the About section, every key of Keyboard Interaction with its note, and every bullet of
Roles, States, and Properties. The page's editorial note (its review waits on an ARIA 1.1
example, issue 129) and its book-reader example state no rule.

What prompted it: the review of a written design for dividers that size a navigator's side
panels.

    python -m craft.census_apg_splitter
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'A Window Splitter can be either variable or fixed. A fixed splitter toggles between two positions whereas a variable splitter can be adjusted to any position within an allowed range.': (
        'set aside', '', 'a definition of the two kinds; nothing to observe'),
    'A window splitter has a value that represents the size of one of the panes, which, in this pattern, is called the primary pane.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'its value'),
    'When the splitter has its minimum value, the primary pane has its smallest size and the secondary pane has its largest size.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', "the value agreeing with the pane's size and range"),
    'The splitter also has an accessible name that matches the name of the primary pane.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'its name'),
    'Left Arrow: Moves a vertical splitter to the left. Right Arrow: Moves a vertical splitter to the right.': (
        'covered', 'a-pane-divider-moves-with-the-arrow-keys', 'quoted by the law'),
    'Up Arrow: Moves a horizontal splitter up. Down Arrow: Moves a horizontal splitter down.': (
        'covered', 'a-pane-divider-moves-with-the-arrow-keys', 'along its axis'),
    'Enter: If the primary pane is not collapsed, collapses the pane. If the pane is collapsed, restores the splitter to its previous position.': (
        'covered', 'a-pane-divider-moves-with-the-arrow-keys', 'quoted by the law'),
    'Home (Optional): Moves splitter to the position that gives the primary pane its smallest allowed size. This may completely collapse the primary pane.': (
        'owed', '', "optional; decidable by the key and the pane's box"),
    'End (Optional): Moves splitter to the position that gives the primary pane its largest allowed size. This may completely collapse the secondary pane.': (
        'owed', '', 'optional; decidable the same way'),
    'F6 (Optional): Cycle through window panes.': (
        'owed', '', 'optional; decidable by where focus lands after F6'),
    'A fixed size splitter omits implementation of the arrow keys.': (
        'owed', '', 'decidable once a splitter is marked fixed'),
    'The element that serves as the focusable splitter has role separator.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'quoted by the law'),
    'The separator element has the aria-valuenow property set to a decimal value representing the current position of the separator.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'its current value'),
    'The separator element has the aria-valuemin property set to a decimal value that represents the position where the primary pane has its minimum size. This is typically 0.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'its minimum'),
    'The separator element has the aria-valuemax property set to a decimal value that represents the position where the primary pane has its maximum size. This is typically 100.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'quoted by the law'),
    'If the primary pane has a visible label, it is referenced by aria-labelledby on the separator element. Otherwise, the separator element has a label provided by aria-label.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'its name'),
    'The separator element has aria-controls referring to the primary pane.': (
        'covered', 'a-pane-divider-is-a-focusable-separator-with-its-value', 'quoted by the law'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 17


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apg_splitter",
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
    print(f"WAI-ARIA APG, Window Splitter: {len(CENSUS)} classified\n")
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
