"""A census: the GOV.UK Design System's Button component, whole.

It roots one-main-call-to-action-per-page, and its sentences were already quoted by
says-what-happens and no-disabled-submit; a source is adopted entire or not at all (the
source-the-rule protocol), and the page had not been censused. The census unit is each
guideline sentence of the page's guidance, read on 2026-11-20 at
https://design-system.service.gov.uk/components/button/, from "When to use this component" to
"Stop users from accidentally sending information more than once", and its research note. The
change log states no guideline.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"Avoid using multiple default buttons on a single page" against six filled buttons on one sheet.

    python -m craft.census_govuk_button
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Use the button component to help users carry out an action like starting an application or saving their information.': (
        'owed', '', 'an action drawn as a link is decidable from the DOM'),
    'Write button text in sentence case, describing the action it performs.': (
        'covered', 'says-what-happens', 'quoted by the law'),
    'You may need to include more or different words to better describe the action.': (
        'covered', 'says-what-happens', 'quoted by the law'),
    'Align the primary action button to the left edge of your form.': (
        'owed', '', 'decidable from the rendered form'),
    'Use a default button for the main call to action on a page.': (
        'covered', 'one-main-call-to-action-per-page', 'quoted by the law'),
    'Avoid using multiple default buttons on a single page.': (
        'covered', 'one-main-call-to-action-per-page', 'quoted by the law'),
    "Use a start button for the main call to action on your service's Start page.": (
        'set aside', '', "the service's Start page, a GOV.UK pattern"),
    'Start buttons do not usually submit form data, so use a link tag instead of a button tag.': (
        'owed', '', 'decidable from the DOM'),
    'Use secondary buttons for secondary calls to action on a page.': (
        'covered', 'one-main-call-to-action-per-page', 'quoted by the law'),
    'Before adding lots of secondary buttons, try to simplify the page or break the content down across multiple pages.': (
        'owed', '', 'a reading of the page; one-surface-one-job is its neighbour'),
    'Only use warning buttons for actions with serious destructive consequences that cannot be easily undone by a user.': (
        'covered', 'destructive-is-set-apart', 'the critical tone kept for what destroys'),
    "When letting users carry out an action like this, it's a good idea to include an additional step which asks them to confirm it. In this instance, use another style of button for the initial call to action, and a warning button for the final confirmation.": (
        'covered', 'destructive-is-set-apart', 'a destructive act confirmed'),
    'Do not only rely on the red colour of a warning button to communicate the serious nature of the action.': (
        'covered', 'colour-is-never-the-only-signal', 'red alone carrying the danger'),
    'Make sure all users can see the button - the white button and background colour must have a contrast ratio of at least 4.5:1': (
        'covered', 'text-holds-its-contrast', 'the same measurement'),
    'Disabled buttons have poor contrast and can confuse some users, so avoid them if possible. Only use disabled buttons if research shows it makes the user interface easier to understand.': (
        'covered', 'no-disabled-submit', 'quoted by the law'),
    'Use a button group when two or more buttons are placed together.': (
        'owed', '', 'decidable from the DOM'),
    'If you are working in production and research shows that users are frequently sending information twice, you can configure the button to ignore the second click. [...] you should also think about the issue server-side': (
        'owed', '', 'decidable by a double press and the requests it sends'),
    "In the case of slow connections, aim to give the user information about what's happening, for example, by showing a loading spinner or a modal, before using data-prevent-double-click.": (
        'covered', 'status-is-visible', 'feedback within a reasonable time'),
    'Testing on GOV.UK has shown that using green as the colour of start buttons improved click-through rates.': (
        'set aside', '', "a finding for GOV.UK's start buttons"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 19


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_govuk_button",
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
    print(f"GOV.UK Design System, Button: {len(CENSUS)} classified\n")
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
