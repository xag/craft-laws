"""A census: GOV.UK Design System, Warning text, whole.

It roots the-warning-sign-is-for-a-warning, and a source is adopted entire or not at all (the
source-the-rule protocol). The census unit is each statement of the component page, read on
2026-11-20 (design-system.service.gov.uk/components/warning-text/): "When to use this
component", "How it works" with its example markup, and the recent changes (one row; the
earlier history is behind a link and not on the page).

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_govuk_warning_text
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Use the warning text component when you need to warn users about something important, such as legal consequences of an action, or lack of action, that they might take.": (
        "covered", "the-warning-sign-is-for-a-warning", "quoted by the law"),
    "There are 2 ways to use the warning text component. You can use HTML or, if you are using Nunjucks or the GOV.UK Prototype Kit, you can use the Nunjucks macro.": (
        "set aside", "", "how to build it"),
    "<span class=\"govuk-warning-text__icon\" aria-hidden=\"true\">!</span> <strong class=\"govuk-warning-text__text\"> <span class=\"govuk-visually-hidden\">Warning</span>": (
        "owed", "",
        "the '!' hidden from assistive technology and a hidden word naming it, in strong "
        "text after it: decidable from the DOM"),
    "You might need to rewrite the hidden text (‘Warning’ in the example) to make it appropriate for your context.": (
        "owed", "", "the hidden word fits what is warned of; a reading"),
    "Recent changes: text kept bold when user agent styles are overridden; the icon's colours follow the root text and background colours, so the icon changes if a user customises them; the assistive class replaced by govuk-visually-hidden; a default for the icon's fallback text; the icon's outline no longer clipped in forced colours.": (
        "set aside", "", "the component's change log"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 5


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_govuk_warning_text",
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
    print(f"GOV.UK Design System, Warning text: {len(CENSUS)} classified\n")
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
