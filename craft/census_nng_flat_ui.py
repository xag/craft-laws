"""A census: Kate Moran, Flat UI Elements Attract Less Attention and Cause Uncertainty (Nielsen Norman Group, 2017-09-03), whole.

It roots a-control-looks-clickable, and a source is adopted entire or not at all (the
source-the-rule protocol). The article reports an eyetracking experiment; the census unit is each
sentence that draws a rule from it, read on 2026-11-20 at
https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/. The method and the
results report the study and ask nothing.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"Designs with weak clickability signifiers waste users' time" against a button drawn as amber text.

    python -m craft.census_nng_flat_ui
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Users need to be able to look at a page, and understand their options immediately.': (
        'covered', 'a-control-looks-clickable', "the law's aim"),
    "Designs with weak clickability signifiers waste users' time": (
        'covered', 'a-control-looks-clickable', 'quoted by the law'),
    'As long as in-line text links are presented in a contrasting color, users will recognize their purpose, even without an underline.': (
        'covered', 'a-control-looks-clickable', 'quoted by the law: what suffices for a link in text'),
    'Ideally, to avoid click uncertainty, all three of those criteria should be met, not just one or two.': (
        'owed', '', 'low density, a traditional layout, salient targets: partly decidable from the page'),
    'A site with a substantial amount of potentially overwhelming content, or radically new page layouts or patterns, should proceed with caution when adopting an ultraflat design.': (
        'set aside', '', 'a caution; a reading'),
    "Strong signifiers are helpful in situations where users care about finding something specific. They're absolutely crucial in situations where you care that users discover a feature that they didn't know existed.": (
        'covered', 'a-control-looks-clickable', "the law's strongest case"),
    "it's a good idea to use a practice task to ensure that participants understand the instructions. (It's also best to conduct pilot testing before even starting the real study to iron out any methodology issues.)": (
        'owed', '', "a study's practice task and pilot, decidable from its protocol"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 7


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_flat_ui",
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
    print(f"Moran, Flat UI Elements Attract Less Attention and Cause Uncertainty: {len(CENSUS)} classified\n")
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
