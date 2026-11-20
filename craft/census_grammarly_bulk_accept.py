"""A census: Denys Kulyk, How We Built It: Accepting Multiple Suggestions at Once for Grammarly Premium Users (Grammarly engineering blog, updated 2021-03-31), whole.

A product team's account of building one feature, read on 2026-11-20 at
https://www.grammarly.com/blog/engineering/accepting-multiple-suggestions (served with a
trailing slash). A source is adopted entire or not at all (the source-the-rule protocol), so
every decision and practice the post states is classified here. Its decisions are the team's,
for its product, and a decision taken for one product is not a rule stated for others: those are
set aside. The practices it states as its own way of working are routed like any rule.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its bulk accept kept for the suggestions people nearly always accept.

    python -m craft.census_grammarly_bulk_accept
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'there are certain suggestions that people tend to always accept, and others that are more likely to require further consideration': (
        'set aside', '', "a finding about the product's users"),
    'Instead, we framed the problem as “accept multiple suggestions that we are pretty confident you were going to accept anyway.”': (
        'set aside', '', "the team's decision for its product: a bulk act limited to what is nearly always accepted"),
    "after we define the problem (and before doing anything else) we establish the key metrics we'll be tracking. Otherwise, we won't have a way of knowing what success looks like.": (
        'covered', 'a-protocol-is-an-artifact-before-the-run', 'what will be measured, fixed before the work'),
    'When testing any new model for a feature, we always analyze precision and recall.': (
        'covered', 'a-check-reports-its-misses', 'what it caught, missed and wrongly flagged'),
    "But it's also important to find ways to get a measure of precision and recall on live data.": (
        'owed', '', 'needs a new fact: a live outcome per suggestion (here, a revert)'),
    "How many suggestions needed to meet our model's threshold in order for us to provide the user with the option of accepting them all at once? Was two enough? We decided on three.": (
        'set aside', '', "the team's decision"),
    'When our feature triggered, an Accept button would appear at the top of the suggestions feed.': (
        'set aside', '', 'describes the first design'),
    'We also needed a way for people to change their mind after clicking on the button. [...] So we added an undo button and designed a way to revert individual corrections': (
        'covered', 'every-mistake-has-a-way-back', 'an exit from the bulk act, whole or in part'),
    'Our new UX was less minimal, clearly showing which suggestions would be accepted using a preview panel.': (
        'owed', '', 'a bulk act shows what it will change before it is taken; the post reports activation over 10 percent better'),
    "If people had to search through their text to get the key context for Grammarly's suggestions, we would be defeating the time-saving purpose of our feature.": (
        'set aside', '', "the reason for the team's context API"),
    'we still decided to release the initial version of our MVP to 5 percent and then 10 percent of our Grammarly Premium users. This way, we could collect baseline metrics against which to judge our subsequent efforts.': (
        'set aside', '', "the team's release process"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 11


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_grammarly_bulk_accept",
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
    print(f"Grammarly, How We Built It: Accepting Multiple Suggestions at Once: {len(CENSUS)} classified\n")
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
