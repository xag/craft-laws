"""A census: WebAIM, WAVE Help, whole.

A source is adopted entire or not at all (the source-the-rule protocol). The page is a tool's
help: the census unit is each section of it, read on 2026-11-20 (wave.webaim.org/help), with
the statements of the section on its icons taken one by one, since the design review cited it.
Most of it describes the tool and is set aside. It states one rule craft-laws lacks, about what
an automated check may claim - that it never says a page passed what only a person can judge -
which is owed; and it states no rule for the design under review.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20, which cited WAVE's icons embedded in the page as
the shape of one alternative.

    python -m craft.census_wave_help
"""

from __future__ import annotations

_DESC = "describes the tool; states no rule"

# section or statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "WAVE cannot tell you if your web content is accessible. Only a human can determine true accessibility. But, WAVE can help you, as a human, evaluate the accessibility of your web content.": (
        "owed", "",
        "an automated check never certifies what only a person can judge; "
        "a-check-reports-what-it-could-not-judge asks for the count, not this"),
    "Our philosophy is to focus on issues that we know impact end users, facilitate human evaluation, and to educate about web accessibility.": (
        "set aside", "", "the tool's aims"),
    "WAVE will present your page with embedded icons and indicators. Each icon, box, and piece of information added by WAVE presents some information about the accessibility of your page.": (
        "set aside", "", _DESC),
    "The WAVE sidebar indicates if WAVE has detected any errors or not. The absence of errors DOES NOT mean your page is accessible or compliant.": (
        "owed", "", "the same rule: no errors found is not a pass"),
    "RED icons indicate accessibility errors that need to be fixed. GREEN icons indicate accessibility features ... yellow alert icons, highlight other elements that you should look at.": (
        "set aside", "", _DESC),
    "The goal should not be to get rid of all icons, except for the errors which may represent an end user issue, but must be manually assessed.": (
        "set aside", "", "how to use the tool"),
    "While WAVE can identify errors ... it cannot tell you if your page is accessible. For this reason, we never indicate that your page is accessible or if it has 'passed' WAVE. ... we do not provide any approval or certification indicators or badges.": (
        "owed", "", "the same rule, stated as the tool's practice"),
    "WAVE cannot check all of the issues in these guidelines - no automated tool can.": (
        "covered", "a-check-reports-what-it-could-not-judge", "a check states what it cannot judge"),
    "WAVE cannot tell you if your alternative text is equivalent and appropriate, so it instead reveals the alternative text so it can be evaluated by the WAVE user.": (
        "owed", "", "what a check cannot judge it shows to the person who can"),
    "Styles and Code: disabling page CSS styles shows the underlying reading and navigation order; the Code tab shows the markup.": (
        "set aside", "", _DESC),
    "How are the WAVE extensions different?: the extensions evaluate content as it is rendered within your web browser.": (
        "set aside", "", _DESC),
    "Because WAVE injects icons into your web page, it often breaks the page layout or results in page elements overlapping.": (
        "set aside", "", _DESC),
    "WAVE reports an error, but I don't see a red icon: the icon is most likely within an area hidden using CSS.": (
        "set aside", "", _DESC),
    "How does WAVE handle \"hidden\" elements?: WAVE detects accessibility issues in all page elements, even those that are hidden ... if we err on this point, we err on the side of users with disabilities.": (
        "set aside", "", "the tool's choice"),
    "Javascript and CSS: WAVE evaluates your content after JavaScript and CSS has been applied to it.": (
        "set aside", "", _DESC),
    "Is WAVE accessible?: designed to be very accessible to users with disabilities, including screen reader users.": (
        "set aside", "", _DESC),
    "Why are results different between the online version vs WAVE extension vs WAVE API?": (
        "set aside", "", _DESC),
    "Add a WAVE link to your web page; use the browser bookmarklet; problems or feedback; more than one page at a time.": (
        "set aside", "", _DESC),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 18


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_wave_help",
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
    print(f"WebAIM, WAVE Help: {len(CENSUS)} classified\n")
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
