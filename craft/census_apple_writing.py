"""A census: Apple's Human Interface Guidelines, Writing, whole.

It roots a-label-names-the-thing-not-a-speaker, and a source is adopted entire or not at all
(the source-the-rule protocol): every guideline the page states is classified here, not only
the ones that convicted the label. The census unit is each guideline's lead sentence, read
from the page on 2026-09-27 (developer.apple.com/design/human-interface-guidelines/writing):
four under "Getting started", twelve under "Best practices"; "Platform considerations" adds
none.

One guideline disagrees with a law already standing: Apple shows hints as placeholder text in
text fields, where no-placeholder-labels (GOV.UK) keeps them out of the placeholder. The law
stands on its own source's reason - a placeholder vanishes as the user types - and the
disagreement is recorded here rather than resolved by choosing the convenient one.

    python -m craft.census_apple_writing
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- Getting started ----------------------------------------------------------------
    "Determine your app's voice.": (
        "covered", "a-label-names-the-thing-not-a-speaker",
        "its list of common terms is one-act-one-name's; the voice is the product's, not a "
        "speaker's, which is this law"),
    "Match your tone to the context.": (
        "set aside", "",
        "a tone per situation is a writer's judgment with no observable a law can hold"),
    "Be clear.": (
        "covered", "a-label-names-the-thing-not-a-speaker",
        "'Check each word to be sure it needs to be there' is quoted by the law"),
    "Write for everyone.": (
        "covered", "no-system-vocabulary",
        "plain language, no jargon; the localisation half is the translation laws'"),
    # --- Best practices -----------------------------------------------------------------
    "Consider each screen's purpose.": (
        "covered", "one-surface-one-job",
        "one idea per screen, the most important first (front-load-first-words)"),
    "Be action oriented.": (
        "covered", "says-what-happens",
        "a verb on a button; 'too cute or clever' is quoted by "
        "a-label-names-the-thing-not-a-speaker, 'Click here' by links-say-where-they-lead"),
    "Build language patterns.": (
        "covered", "one-act-one-name",
        "the same words for the same act, every time"),
    "Adopt capitalization rules that align with your app's style, then apply them "
    "consistently.": (
        "covered", "sentence-labels-take-sentence-case",
        "one case per kind of element; the law holds the sentence-case half both its "
        "sources agree on"),
    "Give clear guidance and use consistent language throughout processes with multiple "
    "steps.": (
        "covered", "one-act-one-name",
        "the same word for the same step of a flow, and 'Done' where it ends"),
    "Use possessive pronouns sparingly.": (
        "covered", "a-label-names-the-thing-not-a-speaker",
        "quoted by the law, with Microsoft's allowance for 'my' in toggles in its note"),
    "Write for how people use each device.": (
        "owed", "",
        "'tap' not 'click' on a touch device is decidable from the platform and the words; "
        "no law holds it yet"),
    "Provide clear next steps on any blank screens.": (
        "covered", "empty-state-never-contradicts",
        "an empty state that guides to an action; the law holds that it never contradicts "
        "the controls around it"),
    "Write clear error messages.": (
        "covered", "error-says-the-fix",
        "the fix, beside the problem (error-lands-at-the-field), without blame or 'oops' "
        "(error-neither-begs-nor-blames)"),
    "Choose the right delivery method.": (
        "set aside", "",
        "which channel a message goes by is a design choice per message, not a property of "
        "words on a screen"),
    "Keep settings labels clear and simple.": (
        "covered", "a-label-names-the-thing-not-a-speaker",
        "quoted by the law; 'describe what it does when turned on' is NN/g's toggle label "
        "rule, the same law's"),
    "Show hints in text fields.": (
        "covered", "no-placeholder-labels",
        "label every field and put the error next to it; Apple's placeholder hint is the one "
        "point the law, on GOV.UK's ground, does not follow (see above)"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 16


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apple_writing",
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
    print(f"Apple HIG, Writing: {len(CENSUS)} classified\n")
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
