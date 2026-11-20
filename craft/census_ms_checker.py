"""A census: Microsoft Support, Improve accessibility with the Accessibility Checker, whole.

A how-to page: it tells a document's author how to run the checker and work through its
findings. A source is adopted entire or not at all (the source-the-rule protocol), so every
instruction and every statement of how the checker shows its findings is classified here, read
on 2026-11-20 at
https://support.microsoft.com/en-us/office/improve-accessibility-with-the-accessibility-checker-a16f6de0-2f39-4a2b-8bd8-5ad801426c7f
(served from https://support.microsoft.com/en-us/accessibility/office-accessibility/improve-accessibility-with-the-accessibility-checker).
The page's Windows, macOS and web sections say the same things in other words; each is
counted once. Most of the page describes the product, and a description asks nothing of a
design: it adds no law. Its rules for classifying issues are on its companion page, censused in
craft/census_ms_checker_rules.py.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its issues grouped by severity, each opening to its instances, each instance going to its place.

    python -m craft.census_ms_checker
"""

from __future__ import annotations

# instruction -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Before you send an Outlook email message or share a Word document, Excel spreadsheet, PowerPoint presentation, or OneNote notebook, run the Accessibility Checker': (
        'owed', '', 'a check run before sharing: decidable from a record of runs and shares'),
    'issues are organized into Warnings, Errors, and Tips under Inspection Results.': (
        'set aside', '', "describes the product; the rule behind it is the companion page's, carried by a-problem-is-ranked-by-its-severity"),
    "In the Accessibility pane, you'll see a list of errors and warnings, with how-to-fix recommendations for each.": (
        'set aside', '', 'describes the product'),
    'select an issue under Warnings or Errors. The list will expand and show the items and objects affected by the issue.': (
        'set aside', '', 'describes the product'),
    'Select the item or object to view the exact location of the affected item or object.': (
        'set aside', '', 'describes the product: a finding takes its reader to its place; no rule is stated'),
    'Select an item or object in the list to highlight the corresponding element, and then fix the issue.': (
        'set aside', '', 'describes the product'),
    'To address the issue, select the down arrow button next to it and open the Recommended Actions list.': (
        'set aside', '', 'describes the product'),
    'Select an item or object to see why you should fix the issue and the steps to take to correct it.': (
        'set aside', '', 'describes the product'),
    'Go through and resolve each issue under Warnings and Errors. [...] Address all issues in the errors and warnings categories.': (
        'owed', '', "every error and warning resolved before sharing: decidable from the checker's last run"),
    "When you're done, select Recheck to make sure you didn't miss anything.": (
        'covered', 'make-it-fail-before-you-fix-it', 'the check that showed the failure is run again and turns green'),
    'Select the Review tab. [...] Select Check Accessibility to open the Accessibility pane': (
        'set aside', '', 'operating the product, on each platform'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 11


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_ms_checker",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} instructions")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Microsoft Support, Improve accessibility with the Accessibility Checker: {len(CENSUS)} classified\n")
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
    print("\n  Every covered instruction names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
