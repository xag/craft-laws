"""A census: WHATWG, HTML Living Standard, 4.10.6 The button element, whole.

It roots a-button-holds-only-phrasing-content, and a source is adopted entire or not at all (the
source-the-rule protocol). The source is the section at
https://html.spec.whatwg.org/multipage/form-elements.html#the-button-element, read on 2026-11-20.
The census unit is each requirement it places on authors, and the element's definition; the
algorithms are requirements on user agents, and the examples and the IDL ask nothing of a page.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"Phrasing content, but there must be no interactive content descendant" against a heading inside each row's button.

    python -m craft.census_whatwg_button
"""

from __future__ import annotations

# requirement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Content model: Phrasing content, but there must be no interactive content descendant and no descendant with the tabindex attribute specified.': (
        'covered', 'a-button-holds-only-phrasing-content', 'quoted by the law'),
    'Contexts in which this element can be used: Where phrasing content is expected. As the first child of a select element.': (
        'owed', '', 'decidable from the DOM'),
    'Tag omission in text/html: Neither tag is omissible.': (
        'set aside', '', "the parser's syntax"),
    'The button element represents a button labeled by its contents.': (
        'set aside', '', 'the definition; the-accessible-name-contains-the-visible-label holds what the label owes'),
    'The type attribute controls the behavior of the button when it is activated. It is an enumerated attribute with the following keywords and states: submit, reset, button': (
        'owed', '', 'decidable from the DOM'),
    'If specified, the commandfor attribute value must be the ID of an element in the same tree as the button with the commandfor attribute.': (
        'owed', '', 'decidable from the DOM'),
    'The formaction, formenctype, formmethod, formnovalidate, and formtarget must not be specified if the element is not a submit button.': (
        'owed', '', 'decidable from the DOM'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 7


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_whatwg_button",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the section's {SOURCE_COUNT} requirements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"WHATWG HTML, The button element: {len(CENSUS)} classified\n")
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
    print("\n  Every covered requirement names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
