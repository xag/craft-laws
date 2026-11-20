"""A census: the GOV.UK Design System's Radios component, whole.

It roots radios-for-one-answer-checkboxes-for-several, and a source is adopted entire or not at
all (the source-the-rule protocol). The census unit is each guideline sentence of the page's
guidance, read on 2026-11-20 at https://design-system.service.gov.uk/components/radios/, from
"When to use this component" to "Error messages"; the known issues, the research note and the
change log state no guideline. The three wordings for an error message are one guideline.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
"Use the radios component when users can only select one option from a list" against a free-text field for a question the product holds the answers to, and its 'None of the above' or 'I do not know'.

    python -m craft.census_govuk_radios
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Use the radios component when users can only select one option from a list.': (
        'covered', 'radios-for-one-answer-checkboxes-for-several', 'quoted by the law'),
    'Do not use the radios component if users might need to select more than one option. In this case, you should use the Checkboxes component instead.': (
        'covered', 'radios-for-one-answer-checkboxes-for-several', 'quoted by the law'),
    'Always position radios to the left of their labels.': (
        'owed', '', 'a-checkbox-sits-left-of-its-label holds it for checkboxes; decidable from the rendered page'),
    'Do not assume that users will know how many options they can select based on the visual difference between radios and checkboxes alone.': (
        'owed', '', "a hint such as 'Select one option' where needed; a reading"),
    'Do not pre-select radio options': (
        'owed', '', "decidable from the DOM; Nielsen says the opposite ('Always offer a default selection'), and no law takes a side yet"),
    'you should include ‘None of the above’ or ‘I do not know’ if they are valid options.': (
        'covered', 'the-answers-offered-cover-every-possible-answer', 'the answer the question admits and the list lacked'),
    'Order radio options alphabetically by default.': (
        'owed', '', "decidable from the labels' order, with the page's stated exception and its caution about bias"),
    'Group radios together in a <fieldset> with a <legend> that describes them': (
        'owed', '', 'a-checkbox-group-has-a-legend holds it for checkboxes; decidable from the DOM'),
    'If you are asking just one question per page in your service as recommended, you can set the contents of the <legend> as the page heading.': (
        'owed', '', 'decidable from the DOM'),
    'If you’re asking more than one question on the page, do not set the contents of the <legend> as the page heading.': (
        'owed', '', 'decidable from the DOM'),
    'Only use inline radios when: the question only has two options; both options are short': (
        'owed', '', "decidable from the options' count and length"),
    'Keep each hint to a single short sentence, without any full stops.': (
        'owed', '', "decidable from the hint's text"),
    'Do not use links in hint text.': (
        'owed', '', 'decidable from the DOM'),
    'If one or more of your radio options is different from the others, it can help users if you separate them using a text divider.': (
        'owed', '', 'decidable once the different option is marked; which one differs is a reading'),
    'Keep it simple. If the related question is complicated or has more than one part, show it on the next page in the process instead.': (
        'owed', '', 'a conditionally revealed question with more than one part is decidable; one-question-per-page is the page-level rule'),
    'Conditionally reveal questions only - do not show or hide anything that is not a question.': (
        'owed', '', 'what a radio reveals is decidable from the DOM'),
    'Use standard-sized radios in nearly all cases.': (
        'owed', '', 'decidable from the rendered page'),
    'Display an error message if the user has not: selected any radios': (
        'owed', '', 'decidable by submitting with none selected'),
    'Make sure errors follow the guidance in the Error message component and have specific error messages for specific error states.': (
        'covered', 'error-says-the-fix', 'the fix beside the problem, specific to it'),
    'If it’s a ‘yes’ or ‘no’ question: Say ‘Select yes if [whatever it is is true]’. [...] If there are more than two options: Say ‘Select [whatever it is]’.': (
        'owed', '', "the message's form is decidable from its text"),
    'Include an Error message component that is clearly related to the initial question.': (
        'covered', 'an-error-names-the-field', 'the item in error identified'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 21


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_govuk_radios",
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
    print(f"GOV.UK Design System, Radios: {len(CENSUS)} classified\n")
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
