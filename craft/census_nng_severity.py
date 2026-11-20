"""A census: Jakob Nielsen, Severity Ratings for Usability Problems (Nielsen Norman Group, 1994-11-01), whole.

It roots a-problem-is-ranked-by-its-severity, and a source is adopted entire or not at all (the
source-the-rule protocol). The census unit is each guideline sentence of the article, read on
2026-11-20 at https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/:
the summary, the three factors, the scale, and "Severity Ratings in Heuristic Evaluation". The
sentences that explain a guideline state none of their own.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its three factors to say a flaw's level must come from its consequence.

    python -m craft.census_nng_severity
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'If the severity ratings indicate that several disastrous usability problems remain in an interface, it will probably be unadvisable to release it.': (
        'owed', '', 'decidable once each problem carries a recorded level: a release over level-4 problems'),
    'The severity of a usability problem is a combination of three factors: The frequency with which the problem occurs [...] The impact of the problem if it occurs [...] The persistence of the problem': (
        'covered', 'a-problem-is-ranked-by-its-severity', 'quoted by the law'),
    'Finally, of course, one needs to assess the market impact of the problem': (
        'set aside', '', "a business reading of the product's market"),
    'it is common to combine all aspects of severity in a single severity rating as an overall assessment of each usability problem in order to facilitate prioritizing and decision-making.': (
        'covered', 'a-problem-is-ranked-by-its-severity', 'one level per problem, ordered by it'),
    "The following 0 to 4 rating scale can be used to rate the severity of usability problems: 0 = I don't agree that this is a usability problem at all [...] 4 = Usability catastrophe: imperative to fix this before product can be released": (
        'owed', '', "a scale for the law's level; what each step obliges (4 before release, 1 only with time to spare) is decidable once levels are recorded"),
    'severity ratings can be collected by sending a questionnaire to the evaluators after the actual evaluation sessions, listing the complete set of usability problems that have been discovered, and asking them to rate the severity of each problem.': (
        'owed', '', "rating after finding, over the whole list: decidable from the review's record"),
    'the problems need to be described in reasonable depth, possibly using screendumps as illustrations.': (
        'owed', '', 'a rater who did not find the problem gets its description and picture; partly a reading'),
    'It is important to note that each evaluator should provide individual severity ratings independently of the other evaluators.': (
        'owed', '', 'independence of raters, decidable from who saw which ratings before rating'),
    'It is possible that the evaluators can gain additional insights by revisiting parts of the running interface rather than relying on their memory and the written problem descriptions.': (
        'set aside', '', 'a trade-off the article leaves open, against speed'),
    'severity ratings from a single evaluator are too unreliable to be trusted. [...] using the mean of a set of ratings from three evaluators is satisfactory for many practical purposes.': (
        'owed', '', 'decidable from the record: how many raters a level rests on'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 10


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_severity",
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
    print(f"Nielsen, Severity Ratings for Usability Problems: {len(CENSUS)} classified\n")
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
