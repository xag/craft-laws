"""A practice census: GOV.UK's "Identify user needs" and Jeffries's "You're NOT gonna need it!", whole.

Both root a-change-adds-no-words-nobody-asked-for, and a source is adopted entire or not at
all (the source-the-rule protocol): every rule each states is classified here, not only the
one that convicted the change. The census unit is each page's own statements, read from the
pages on 2026-09-26 (gov.uk/guidance/content-design/user-needs; ronjeffries.com, 1998-04-04).
Most of GOV.UK's page is about researching and recording needs for a publishing
organisation - practice this estate does not run - and is set aside with the reason, not
dropped.

    python -m craft.census_user_needs
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- GOV.UK, Identify user needs ------------------------------------------------------
    "Every piece of published content should meet a valid user need.": (
        "covered", "a-change-adds-no-words-nobody-asked-for",
        "the change that adds words answers for the need; the owner's request is the need"),
    "If the user does not need to take an action as a result of what they're understanding, "
    "it's not a valid user need.": (
        "covered", "a-screen-carries-no-words-nobody-acts-on",
        "the screen law's own test: a word nobody acts on"),
    "User needs and GOV.UK content must be based on actions or tasks.": (
        "covered", "a-screen-carries-no-words-nobody-acts-on",
        "the same test, stated of the content"),
    "This is not a valid user need because it creates a 'need' to justify existing content, "
    "and suggests a specific solution that may or may not be right.": (
        "covered", "a-change-adds-no-words-nobody-asked-for",
        "text already on a screen is not its own reason to stay or to be built on"),
    "Find out what you can about who your likely users are, how they currently do it, the "
    "problems they experience and what they need from your content.": (
        "set aside", "",
        "user research for a publishing organisation; the need here is the owner's request"),
    "Do this by reviewing existing evidence such as analytics, call centre data and "
    "previous research reports.": (
        "set aside", "", "the same research, its evidence"),
    "All GOV.UK user needs follow the same template, with 3 parts (As a... I need to... "
    "So that...).": (
        "set aside", "", "the format of a planning record this estate does not keep"),
    "They're written from the user's perspective and in language that a user would "
    "recognise and use themselves.": (
        "set aside", "", "about writing the need statement, not the screen"),
    "Do not begin the user need with 'as a user.'": (
        "set aside", "", "the format of the need statement"),
    "Acceptance criteria can help define a user need by listing what must be done for the "
    "need to be met.": (
        "set aside", "", "a planning aid; no product of this estate is judged by it"),
    "You should record and store any user needs for content you create.": (
        "set aside", "",
        "the estate records what binds future work in its ledgers, not a need per string"),
    # --- Jeffries, You're NOT gonna need it! ----------------------------------------------
    "Always implement things when you actually need them, never when you just foresee that "
    "you need them.": (
        "covered", "a-change-adds-no-words-nobody-asked-for",
        "a line added because someone might want it is the foreseen need"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 12


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_user_needs",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the sources' {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"GOV.UK Identify user needs and Jeffries YAGNI: {len(CENSUS)} classified\n")
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
