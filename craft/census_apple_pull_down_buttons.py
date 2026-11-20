"""A census: Apple, Human Interface Guidelines, Pull-down buttons, whole.

Read on 2026-11-20 at https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons.md
(the page's Markdown form; the page is
https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons). A source is
adopted entire or not at all (the source-the-rule protocol). The census unit is each bold
guideline of Best practices and of the iOS and iPadOS section, with the note there. The
sentences that explain a guideline state none of their own.

What prompted it: the second review of a written design for listing a design's flaws, 2026-11-20, as changed and drawn, which relied on
"people generally understand that a More button offers additional functionality" to say an ellipsis in a circle, used as a level mark, already means More. The page states that as a fact about More buttons, not as a rule against reusing the symbol, so it adds no law.

    python -m craft.census_apple_pull_down_buttons
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Use a pull-down button to present commands or items that are directly related to the button's action.": (
        'owed', '', 'a reading of what belongs in the menu'),
    "If you need to provide a list of mutually exclusive choices that aren't commands, use a pop-up button instead.": (
        'owed', '', 'decidable once the items record whether they are commands or choices'),
    "Avoid putting all of a view's actions in one pull-down button.": (
        'owed', '', 'decidable: a view whose every action is inside one menu'),
    'Balance menu length with ease of use. [...] listing a minimum of three items can help the interaction feel worthwhile. If you need to list only one or two items, consider using alternative components': (
        'owed', '', 'decidable by counting the items'),
    'Display a succinct menu title only if it adds meaning.': (
        'owed', '', 'a reading of the title'),
    "Let people know when a pull-down button's menu item is destructive, and ask them to confirm their intent.": (
        'covered', 'destructive-is-set-apart', 'marked in the critical tone, confirmed'),
    'Include an interface icon with a menu item when it provides value.': (
        'set aside', '', 'an option'),
    "Consider using a More pull-down button to present items that don't need prominent positions in the main interface. [...] weigh the convenience of its size against its impact on discoverability": (
        'covered', 'rare-actions-go-to-a-second-layer', 'what needs no prominent place goes to a second layer'),
    'You can also let people reveal a pull-down menu by performing a specific gesture on a button.': (
        'set aside', '', 'an option; gesture-has-a-plain-alternative holds what a gesture owes'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 9


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apple_pull_down_buttons",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} guidelines")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Apple HIG, Pull-down buttons: {len(CENSUS)} classified\n")
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
