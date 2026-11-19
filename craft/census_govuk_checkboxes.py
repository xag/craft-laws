"""A census: the GOV.UK Design System's Checkboxes component, whole.

It roots a-checkbox-sits-left-of-its-label and a-checkbox-group-has-a-legend, and a source is
adopted entire or not at all (the source-the-rule protocol): every guideline the page states
is classified here, not only the two that convicted a mockup. The census unit is each
guideline sentence of the page's guidance, read on 2026-11-19
(design-system.service.gov.uk/components/checkboxes/), from "When to use this component" to
"Error messages"; the research notes after it state no guideline.

What prompted it is the same mockup as craft/census_nng_checkboxes.py: checkboxes at the right
end of each row, tied together by one heading drawn above them.

    python -m craft.census_govuk_checkboxes
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Use the checkboxes component when you need to help users: select multiple options from "
    "a list, toggle a single option on or off.": (
        "owed", "", "Nielsen's when-to-use, owed there too"),
    "Do not use the checkboxes component if users can only choose one option from a "
    "selection. In this case, use the Radios component.": (
        "owed", "", "the same choice"),
    "Always position checkboxes to the left of their labels.": (
        "covered", "a-checkbox-sits-left-of-its-label", "quoted by the law"),
    "Do not assume that users will know how many options they can select based on the visual "
    "difference between radios and checkboxes alone.": (
        "owed", "", "a hint such as 'Select all that apply' where needed; a reading"),
    "Do not pre-select checkbox options": (
        "owed", "", "a question's checkbox checked on arrival is decidable from the DOM"),
    "Order checkbox options alphabetically by default.": (
        "owed", "", "decidable from the labels' order, with the page's stated exception"),
    "Group checkboxes together in a <fieldset> with a <legend> that describes them": (
        "covered", "a-checkbox-group-has-a-legend", "quoted by the law"),
    "If you're asking just one question per page as recommended, you can set the contents of "
    "the <legend> as the page heading.": (
        "owed", "", "legend as heading on a one-question page: decidable from the DOM"),
    "Keep each hint to a single short sentence, without any full stops.": (
        "owed", "", "a hint's length and stops are decidable from its text"),
    "Do not use links in hint text.": (
        "owed", "", "a link inside a hint is decidable from the DOM"),
    "When 'none' would be a valid answer, give users the option to check a box to say none of "
    "the other options apply to them": (
        "set aside", "", "whether 'none' is a valid answer is a reading of the question"),
    "Show the 'none' option last. Separate it from the other options using a divider.": (
        "owed", "", "decidable once the 'none' option is marked"),
    "Write a label that repeats the key part of the question.": (
        "owed", "", "the 'none' label echoing the question; a reading"),
    "You should only conditionally reveal questions - do not show or hide anything that is "
    "not a question.": (
        "owed", "", "what a checkbox reveals is decidable from the DOM"),
    "Use standard-sized checkboxes in most cases.": (
        "owed", "", "the box's size is decidable from the rendered page"),
    "Make sure errors follow the guidance in the Error message component and have specific "
    "error messages for specific error states.": (
        "covered", "error-says-the-fix", "the fix beside the problem, specific to it"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 16


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_govuk_checkboxes",
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
    print(f"GOV.UK Design System, Checkboxes: {len(CENSUS)} classified\n")
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
