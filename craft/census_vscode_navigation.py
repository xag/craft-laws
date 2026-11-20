"""A census: Visual Studio Code documentation, Code Navigation (docs/editor/editingevolved), whole.

A source is adopted entire or not at all (the source-the-rule protocol), and this one states no
rule craft-laws lacks: it is one product's manual, saying what the product does, and a product
doing a thing is a precedent, not a rule. The census unit is each section of the page, and each
item of the section on errors and warnings, which the design review cited, read on 2026-11-20
(code.visualstudio.com/docs/editor/editingevolved, dated 11/18/2026 on the page). Every row is
set aside as a description of the product; where a section agrees with a law the note says so.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20, which cited the errors and warnings section as the
editors' practice: a mark in the text and in the overview ruler, and a count that opens a list.

    python -m craft.census_vscode_navigation
"""

from __future__ import annotations

_DESC = "describes the product; states no rule"

# section or statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Quick file navigation: Ctrl+P opens any file by name; Ctrl+Tab lists the open files of a group; Alt+Left and Alt+Right move between files and edit locations.": (
        "set aside", "", _DESC),
    "Breadcrumbs: a navigation bar above the contents shows the current location and allows you to quickly navigate between folders, files, and symbols.": (
        "set aside", "", _DESC),
    "Breadcrumb customization: breadcrumbs.filePath, breadcrumbs.symbolPath, breadcrumbs.icons.": (
        "set aside", "", _DESC),
    "Symbol order in Breadcrumbs: position, name or type.": (
        "set aside", "", _DESC),
    "Breadcrumb path copying: Copy Breadcrumbs Path; breadcrumbs.symbolPathSeparator.": (
        "set aside", "", _DESC),
    "Breadcrumb keyboard navigation: Focus Breadcrumbs, Left and Right, typing to filter, Space to reveal.": (
        "set aside", "", _DESC),
    "Go to Definition: F12; Ctrl and hover previews the declaration.": (
        "set aside", "", _DESC),
    "Go to Type Definition: from the context menu or the Command Palette.": (
        "set aside", "", _DESC),
    "Go to Implementation: Ctrl+F12.": (
        "set aside", "", _DESC),
    "Go to Symbol: Ctrl+Shift+O; typing : groups the symbols by category.": (
        "set aside", "", _DESC),
    "Open symbol by name: Ctrl+T.": (
        "set aside", "", _DESC),
    "Peek: Go to References and Peek Definition embed the result inline; Escape closes the peek window.": (
        "set aside", "", _DESC + "; Escape closing it agrees with escape-closes-the-overlay"),
    "Bracket matching: matching brackets are highlighted as soon as the cursor is near one of them.": (
        "set aside", "", _DESC),
    "Bracket Pair Colorization: editor.bracketPairColorization.enabled; up to six themeable colours.": (
        "set aside", "", _DESC),
    "Reference information: some languages show inline reference counts, updated live; editor.codeLens.": (
        "set aside", "", _DESC),
    "Rename symbol: F2 renames every usage across files.": (
        "set aside", "", _DESC),
    "Warnings or Errors can be generated either via configured tasks, by rich language services, or by linters, that constantly analyze your code in the background.": (
        "set aside", "", _DESC),
    "In the Status Bar, there is a summary of all errors and warnings counts.": (
        "set aside", "", _DESC),
    "You can click on the summary or press Ctrl+Shift+M to display the PROBLEMS panel with a list of all current errors.": (
        "set aside", "",
        _DESC + "; a summary that opens the list agrees with error-lands-at-the-field's summary"),
    "If you open a file that has errors or warnings, they will be rendered inline with the text and in the overview ruler.": (
        "set aside", "",
        _DESC + "; the same two places a-correction-is-marked-in-the-line-and-in-the-margin "
        "names, as one product's practice"),
    "To loop through errors or warnings in the current file, you can press Alt+F8 or Shift+Alt+F8 which will show an inline zone detailing the problem and possible Code Actions": (
        "set aside", "", _DESC),
    "Code Action: Warnings and Errors can provide Code Actions (also known as Quick Fixes) ... displayed in the editor in the left margin as a lightbulb.": (
        "set aside", "", _DESC),
    "Inlay Hints: additional information about source code rendered inline; editor.inlayHints.enabled.": (
        "set aside", "", _DESC),
    "Outgoing link protection: VS Code displays a prompt before opening an outgoing website link from the editor; trusted domains.": (
        "set aside", "", _DESC),
    "Common questions: selecting the second entry in Quick Open; Ctrl+Tab across all groups; recently used editors without a picker.": (
        "set aside", "", _DESC),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 25


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_vscode_navigation",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"VS Code docs, Code Navigation: {len(CENSUS)} classified\n")
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
