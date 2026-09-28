"""A practice census: Scott Hurff's "How to fix a bad user interface" (the UI Stack), whole.

It roots a-change-to-a-screen-reaches-every-state-it-has, an-error-keeps-what-the-user-entered,
the-users-work-is-never-harmed-by-an-act-or-by-inaction and an-error-message-is-human-not-technical,
and a source is adopted entire or not at all (the source-the-rule protocol): every rule the essay states is classified here,
not only the one that convicted the change. The census unit is each rule the essay states,
read from the page on 2026-09-28 (scotthurff.com, 2015-08-17; an excerpt of Designing
Products People Love, O'Reilly, 2016). Its long examples of each state's design are
illustrations of these rules and are not counted twice.

    python -m craft.census_hurff
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Every screen you interact with in a digital product has multiple personalities. Five, "
    "to be exact.": (
        "covered", "a-change-to-a-screen-reaches-every-state-it-has",
        "a screen's states - blank, loading, partial, error, ideal - are the states a change "
        "must reach"),
    "And you should consider these states for every screen you make.": (
        "covered", "a-change-to-a-screen-reaches-every-state-it-has",
        "the rule itself: every state of the screen, not the one in front of the builder"),
    "All UI states lead to the Ideal State. So start with this first, and let all of the "
    "other states fall into place as your designs get closer to solving your customer's "
    "problem.": (
        "set aside", "",
        "an order of design work; nothing in the product shows whether it was followed"),
    "Broadly speaking, the risk with empty states is that it's easy to tack them on as an "
    "afterthought.": (
        "covered", "a-change-to-a-screen-reaches-every-state-it-has",
        "an afterthought state is a state the change did not reach"),
    "The partial state is the screen someone will see when the page is no longer empty and "
    "sparsely populated. Your job here is to prevent people from getting discouraged and "
    "giving up on your product.": (
        "set aside", "",
        "a goal for one state's design; a reading, with no fact that decides it"),
    "Error states shouldn't be dramatic, nor should they be vague.": (
        "covered", "error-says-the-fix",
        "a vague error is one that does not say the fix"),
    "Make error messages human, not technical, and suited to your audience.": (
        "covered", "an-error-message-is-human-not-technical",
        "a law judged as a reading: meaning is never checked by matching words"),
    "Error states should also be comforting in the sense that your product keeps all user "
    "input safe.": (
        "covered", "an-error-keeps-what-the-user-entered",
        "decided once a new fact is recorded: what the user entered, before the error and "
        "after it"),
    "A computer shall not harm your work or, through inaction, allow your work to come to "
    "harm.": (
        "covered", "the-users-work-is-never-harmed-by-an-act-or-by-inaction",
        "Raskin's first law, quoted: decided once the work a page holds is recorded before "
        "it is left and looked for on the way back"),
    "Make your loading states a part of your prototyping efforts. They're a part of your "
    "product's experience and shouldn't be tacked on last.": (
        "covered", "a-change-to-a-screen-reaches-every-state-it-has",
        "the loading state is one the change must reach; when it is drawn is not judged"),
    "Spend time thinking through edge cases that can trigger errors.": (
        "set aside", "",
        "a practice of the designer's time; nothing in the product shows it"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 11


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_hurff",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)
    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the source's {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Hurff, the UI Stack: {len(CENSUS)} classified\n")
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
