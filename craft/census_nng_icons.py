"""A census: Aurora Harley, Icon Usability (Nielsen Norman Group, 2014-07-27), whole.

It roots an-icon-carries-a-visible-text-label, and a source is adopted entire or not at all
(the source-the-rule protocol). The census unit is each sentence of the article that says what
an icon does, should or should not be, read on 2026-11-20 (nngroup.com/articles/icon-usability/):
the summary, the list of benefits (one row), and the four sections. The examples (Buy Me a Pie,
Combadi, Fab, a clock icon, Usability.gov, Upworthy) illustrate the sentences listed.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_nng_icons
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Due to the absence of a standard usage for most icons, text labels are necessary to communicate the meaning and reduce ambiguity.": (
        "covered", "an-icon-carries-a-visible-text-label", "the summary of the law"),
    "icons must first and foremost communicate meaning in a graphical user interface.": (
        "covered", "an-icon-carries-a-visible-text-label", "the end the label serves"),
    "The benefits of icons in a graphical user interface (GUI) include: good targets, saving space, fast recognition, no translation, aesthetic appeal, a product family.": (
        "set aside", "", "claims of benefit, not rules"),
    "There are a few icons that enjoy mostly universal recognition from users. ... Outside of these examples, most icons continue to be ambiguous to users": (
        "set aside", "", "the finding the label rule rests on"),
    "Even a slight difference in meaning and functionality hinders the ability for a user to understand and rely on an icon when it is encountered in future experiences.": (
        "owed", "", "an icon keeps the meaning it has elsewhere; needs that meaning recorded"),
    "To help overcome the ambiguity that almost all icons face, a text label must be present alongside an icon to clarify its meaning in that particular context.": (
        "covered", "an-icon-carries-a-visible-text-label", "quoted by the law"),
    "And even if you’re using a standard icon, it’s often safer to include a label, especially if you slightly altered the icon to match your aesthetic preferences or constraints.": (
        "covered", "an-icon-carries-a-visible-text-label", "no exception for standard icons"),
    "Icon labels should be visible at all times, without any interaction from the user.": (
        "covered", "an-icon-carries-a-visible-text-label", "quoted by the law"),
    "For navigation icons, labels are particularly critical. Don’t rely on hover to reveal text labels": (
        "covered", "an-icon-carries-a-visible-text-label", "never revealed only on hover"),
    "if you find you need to ponder to come up with an icon for navigation, chances are it’s not going to be easily recognizable or intuitive for users.": (
        "set aside", "", "a designer's heuristic; nothing to observe on the screen"),
    "Also consider the relative size of an icon compared to other visual elements presented on the screen.": (
        "owed", "", "decidable from rendered sizes once a floor is stated; no law states one"),
    "This issue can be avoided on larger screens (where there is usually plenty of space) by simply making the navigation visible rather than collapsing it under an icon.": (
        "owed", "", "decidable at a wide viewport: is the navigation behind an icon"),
    "If you decide to include icons in your interface, do your research first! Familiarize yourself with icons used by your competitors and with icons commonly used on the platforms that you target": (
        "owed", "", "needs a fact: the platform's and the field's icons for the same meaning"),
    "Keep the design simple and schematic.": (
        "set aside", "", "a reading of the glyph"),
    "Use the 5-second rule: if it takes you more than 5 seconds to think of an appropriate icon for something, it is unlikely that an icon can effectively communicate that meaning.": (
        "set aside", "", "a designer's heuristic"),
    "Test the icons for recognizability: ask people what they expect the icons to stand for.": (
        "owed", "", "needs a fact: a test's record"),
    "Test the icons for memorability: ask a repeat set of users if they can remember the icon’s meaning after being told what it represented a couple weeks earlier.": (
        "owed", "", "needs a fact: a test's record"),
    "And always include a visible text label.": (
        "covered", "an-icon-carries-a-visible-text-label", "the article's last word"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 18


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_icons",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the article's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"NN/g, Icon Usability: {len(CENSUS)} classified\n")
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
