"""A census: Jakob Nielsen, Checkboxes vs. Radio Buttons (Nielsen Norman Group, 2004-09-26), whole.

It roots a-checkbox-label-says-what-ticking-it-does, a-checkbox-toggles-from-its-label and
a-checkbox-sets-and-never-acts, and a source is adopted entire or not at all (the
source-the-rule protocol): every guideline the article states is classified here, not only
the three that convicted a mockup. The census unit is each list item's lead sentence, read
from the page on 2026-11-19 (nngroup.com/articles/checkboxes-vs-radio-buttons/): three under
"When to Use Which Widgets", nine under "Additional Guidelines". The sub-points under an item
belong to it.

What prompted it, 2026-11-19: a mockup put a checkbox at the end of each row of a piece's
tools, under one column heading, "Yours"; ticking added the tool to the person's list at once.
The owner: "I'm sure 'Yours' breaks many rules."

    python -m craft.census_nng_checkboxes
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- When to Use Which Widgets --------------------------------------------------------
    "Radio buttons are used when there is a list of two or more options that are mutually "
    "exclusive and the user must select exactly one choice.": (
        "owed", "",
        "which control fits is decidable once the options' exclusivity is recorded; no law "
        "holds it yet"),
    "Checkboxes are used when there are lists of options and the user may select any number "
    "of choices, including zero, one, or several.": (
        "owed", "", "the other half of the same choice"),
    "A stand-alone checkbox is used for a single option that the user can turn on or off.": (
        "owed", "", "the same choice, for one option"),
    # --- Additional Guidelines ------------------------------------------------------------
    "Use standard visual representations.": (
        "owed", "",
        "a square with a check, a circle with a dot: decidable from the rendered control"),
    "Visually present groups of choices as groups, and clearly separate them from other "
    "groups on the same page.": (
        "owed", "",
        "the visual half; a-checkbox-group-has-a-legend holds the markup half, on GOV.UK's "
        "ground"),
    "Lay out your lists vertically, with one choice per line.": (
        "owed", "", "decidable from the rendered boxes"),
    "Use positive and active wording for checkbox labels, so that it's clear what will "
    "happen if the user turns on the checkbox.": (
        "covered", "a-checkbox-label-says-what-ticking-it-does", "quoted by the law"),
    "If possible, use radio buttons rather than drop-down menus.": (
        "owed", "", "a select with few options is decidable from the DOM"),
    "Always offer a default selection for radio button lists.": (
        "owed", "", "a radio group with none checked is decidable from the DOM"),
    "Because radio buttons require exactly one choice, make sure that the options are both "
    "comprehensive and clearly distinct.": (
        "set aside", "",
        "whether options cover every case is a reading of the domain, not of the screen"),
    "Let users select an option by clicking on either the button/box itself or its label": (
        "covered", "a-checkbox-toggles-from-its-label", "quoted by the law"),
    "Use checkboxes and radio buttons only to change settings, not as action buttons that "
    "make something happen.": (
        "covered", "a-checkbox-sets-and-never-acts", "quoted by the law"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 12


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_checkboxes",
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
    print(f"Nielsen, Checkboxes vs. Radio Buttons: {len(CENSUS)} classified\n")
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
