"""A census: Grammarly, Our New Grouped Suggestions Help You Improve Your Writing Even Faster (Grammarly blog, updated 2020-11-17), whole.

A product announcement, read on 2026-11-20 at
https://www.grammarly.com/blog/product/grouped-writing-suggestions/. A source is adopted entire or
not at all (the source-the-rule protocol), so every statement it makes about how suggestions are
shown is classified here. It states no rule for interface or practice work: each statement
describes the product, and a description asks nothing of a design. Its ten category names
describe kinds of writing suggestion and are one statement.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its suggestions grouped by type and taken one at a time.

    python -m craft.census_grammarly_grouped
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "These suggestions are now grouped together to help you edit your text in a way that's approachable and high-impact.": (
        'set aside', '', 'describes the product'),
    'filter through all your suggestions, which are now grouped together based on what type of improvements you want to make': (
        'set aside', '', 'describes the product'),
    'if you click on one spelling mistake, you can accept that suggestion, and then move on to see what other spelling and grammar errors appear in your text.': (
        'set aside', '', 'describes the product'),
    'You can reject any suggestion by clicking on the trash can icon.': (
        'set aside', '', 'describes the product'),
    'If you want to know why you are getting a certain suggestion, you can click on Learn more, and a complete explanation of the suggestion will appear.': (
        'set aside', '', 'describes the product'),
    'Each category is designed to help you focus on one type of improvement at a time.': (
        'set aside', '', 'describes the product'),
    'Fix spelling and grammar; Rewrite for clarity; Improve readability; Enhance your fluency; Reduce wordiness; Check your tone; Follow your company style guide; Improve inclusivity; Enhance your word choice; Keep your style consistent': (
        'set aside', '', "the product's categories"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 7


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_grammarly_grouped",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the post's {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Grammarly, Our New Grouped Suggestions: {len(CENSUS)} classified\n")
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
