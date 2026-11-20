"""A census: Daniel Olaogun, Understanding Lighthouse Accessibility Audit Reports (DebugBear blog, 2023-06-20, updated 2026-04-15), whole.

A vendor's tutorial on running Lighthouse and reading its report, read on 2026-11-20 at
https://www.debugbear.com/blog/lighthouse-accessibility. A source is adopted entire or not at all
(the source-the-rule protocol), so every statement of how the report presents its audits and
every instruction to its reader is classified here. The article states one rule, that the score
does not replace manual testing; the rest describes Lighthouse and DebugBear, and a description
asks nothing of a design. The installation steps operate the product and are left out.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its passed audits grouped apart under a count to show the standard for what holds.

    python -m craft.census_debugbear_lighthouse
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Passing audits are grouped under the "Passed audits" section, with the total number of audits passed in brackets.': (
        'set aside', '', 'describes the report'),
    'The failed audits are categorized based on different accessibility categories, such as contrast, navigation, and forms.': (
        'set aside', '', 'describes the report'),
    'If you click any of the failed accessibility standards, you\'ll get a brief description of why the standard is important and a "Learn more" link with further information.': (
        'set aside', '', 'describes the report'),
    'It also provides screenshots of the elements and the associated code snippets that break the standard, allowing you to see what is wrong and fix issues': (
        'set aside', '', 'describes the report'),
    'The report also shows additional accessibility considerations under "Additional Items To Manually Check". These checks can\'t be automated by Lighthouse and don\'t impact the Lighthouse Accessibility score.': (
        'set aside', '', 'describes the report; a check doing what a-check-reports-what-it-could-not-judge asks'),
    'audits that are not applicable to the website you are testing [...] are displayed in a separate "Not Applicable" category.': (
        'set aside', '', 'describes the report'),
    'Each audit is assigned a score and the overall Accessibility score is calculated by assigning a weight to each subscore.': (
        'set aside', '', 'describes the score'),
    "the Google Lighthouse extension runs the accessibility test on Google servers. For example, that means you won't be able to test pages that are behind an authentication mechanism.": (
        'set aside', '', "describes the product's reach"),
    "While Lighthouse can help you improve the accessibility of your website, you can't rely on it to find all potential accessibility issues. This requires manual testing.": (
        'covered', 'done-is-observed-where-the-user-stands', "an automated score is the producer's side; the page is used and looked at"),
    'The audits dashboard can show you how many pages are impacted by each error, helping identify high-priority fixes that apply widely across your site.': (
        'set aside', '', "describes DebugBear's product; frequency as one part of severity is a-problem-is-ranked-by-its-severity's"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 10


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_debugbear_lighthouse",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the article's {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"DebugBear, Understanding Lighthouse Accessibility Audit Reports: {len(CENSUS)} classified\n")
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
    print("\n  Every covered statement names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
