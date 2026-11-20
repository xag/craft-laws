"""A census: the README of the VS Code ESLint extension (github.com/microsoft/vscode-eslint), whole.

Read on 2026-11-20 at https://github.com/microsoft/vscode-eslint (its raw README.md on the main
branch). A source is adopted entire or not at all (the source-the-rule protocol), so every
recommendation the README makes, and the two passages the review relied on, are classified here.
It states one rule of practice, to check the plain tool before blaming the extension; the rest
configures ESLint or describes the extension, and asks nothing of a design. The release notes'
lists of changes and each setting's description document the product and are left out.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
its fix-all command beside the per-problem quick fix. Read whole, the README's "quick fix
for the corresponding ESLint problem" approves or denies running the ESLint library (version
2.1.10's notes); it is not a fix for a lint problem. The extension offers per-problem fixes in
VS Code's own quick-fix menu, which the README names only in its settings.

    python -m craft.census_vscode_eslint
"""

from __future__ import annotations

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Local install (recommended)': (
        'set aside', '', 'configures ESLint'),
    'For ESLint v9 and later (or v8.57+ with flat config), this should be one of: eslint.config.js [...]': (
        'set aside', '', 'configures ESLint'),
    'For projects using older ESLint versions (< 8.57), use a legacy .eslintrc file': (
        'set aside', '', 'configures ESLint'),
    "If you're using the legacy version, consider reading how to migrate to flat config.": (
        'set aside', '', 'configures ESLint'),
    'To use flat config files it is recommended to use ESLint version 8.57.0 or above.': (
        'set aside', '', 'configures ESLint'),
    'The experimental settings eslint.experimental.useFlatConfig is deprecated and should only be used for ESLint versions >= 8.21 < 8.57.0.': (
        'set aside', '', 'configures the extension'),
    'Although you can also use the formatter on save using the setting editor.formatOnSave it is recommended to use the editor.codeActionsOnSave feature since it allows for better configurability.': (
        'set aside', '', 'configures the editor'),
    'if you use ESLint as your default formatter you should turn off editor.formatOnSave when you have turned on editor.codeActionsOnSave. Otherwise you file gets fixed twice which in unnecessary.': (
        'set aside', '', 'configures the editor'),
    'Fix all auto-fixable problems: applies ESLint auto-fix resolutions to all fixable problems.': (
        'set aside', '', 'describes a command'),
    'using the quick fix for the corresponding ESLint problem': (
        'set aside', '', 'describes a gesture that approves running the library, not a lint fix'),
    'Please make yourself familiar with the introduction before using the VS Code ESLint extension in a TypeScript setup. Especially make sure that you can validate TypeScript files successfully in a terminal using the eslint command. [...] Before filing an issue against the VS Code ESLint extension please ensure that you can successfully validate your files in a terminal using the eslint command.': (
        'covered', 'the-baseline-assumption-is-verified', 'the plain tool checked before the layer on top is blamed'),
    'To avoid validation from any TSLint installation disable TSLint': (
        'set aside', '', 'configures the editor'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 12


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_vscode_eslint",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the README's {SOURCE_COUNT} statements")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"microsoft/vscode-eslint, README: {len(CENSUS)} classified\n")
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
