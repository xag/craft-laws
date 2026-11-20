"""A census: John Van Engen, SOLIDWORKS Assembly Validation Tools - Part 2 - Interference Detection (CATI blog, 2014-07-18), whole.

A reseller's walk through one CAD command, read on 2026-11-20 at https://cati.com/?p=120210
(served from https://www.cati.com/blog/solidworks-assembly-validation-tools-part-2-interference-detection/).
SOLIDWORKS' own help pages are drawn by script and returned no text to a fetch. A source is
adopted entire or not at all (the source-the-rule protocol), so every capability the post lists,
every action it gives on a result and its one tip are classified here. It states no rule for
interface or practice work: it describes the command, and a description asks nothing of a
design. The steps that set a part's fastener property operate the product and are left out.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its selected interference highlighted in the model to show the standard for showing where a problem is.

    python -m craft.census_cati_interference
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Determine the interference between components.': (
        'set aside', '', 'describes the command'),
    'Display the true volume of interference as a shaded volume.': (
        'set aside', '', 'describes the command'),
    'Change the display settings of the interfering and non-interfering components to see the interference better.': (
        'set aside', '', 'describes the command'),
    'Select to ignore interferences that you want to exclude, such as press fits, interferences of threaded fasteners, and so on.': (
        'set aside', '', 'describes the command'),
    'Choose to include interferences between bodies within a multibody part.': (
        'set aside', '', 'describes the command'),
    "Choose to treat a subassembly as a single component, so that interferences between the subassembly's components are not reported.": (
        'set aside', '', 'describes the command'),
    'Distinguish between coincidence interferences and standard interferences.': (
        'set aside', '', 'describes the command'),
    'The detected interferences are listed under Results. The volume of each interference appears to the right of each listing.': (
        'set aside', '', 'describes the command'),
    'Select an interference to highlight it in red in the graphics area.': (
        'set aside', '', 'describes the command: a result takes its reader to its place; no rule is stated'),
    'Expand interferences to display the names of the interfering components.': (
        'set aside', '', 'describes the command'),
    'Right-click an interference and select Zoom to selection, to zoom to the interfering components in the graphics area.': (
        'set aside', '', 'describes the command'),
    'Right-click an interference and select Ignore.': (
        'set aside', '', 'describes the command'),
    'Right-click an ignored interference and select Un-Ignore': (
        'set aside', '', 'describes the command'),
    'Options: Treat coincidence as interference; Show ignored interferences; Treat subassemblies as components; Include multibody part interferences; Make interfering parts transparent; Create fasteners folder; Create matching cosmetic threads folder; Ignore hidden bodies/components': (
        'set aside', '', "the command's settings"),
    'When you run Interference Detection, the interferences between the threads of fasteners are reported. Generally, you want to ignore these interferences.': (
        'set aside', '', 'a modelling tip for one command'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 15


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_cati_interference",
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
    print(f"CATI, SOLIDWORKS Assembly Validation Tools - Part 2 - Interference Detection: {len(CENSUS)} classified\n")
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
