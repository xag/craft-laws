"""A census: Apple, Human Interface Guidelines, Menus, whole.

It is the second root of a-stable-menu-disables-what-does-not-apply and of
a-menu-with-nothing-available-stays-openable, and a source is adopted entire or not at all (the
source-the-rule protocol). The page was read on 2026-11-20 at
https://developer.apple.com/design/human-interface-guidelines/menus, in the JSON the site serves
to its own page (https://developer.apple.com/tutorials/data/design/human-interface-guidelines/menus.json).
The census unit is the first sentence of each paragraph that states a guideline, in the page's
words; the sentences after it explain it and state none of their own, except the one on a menu
whose items are all unavailable, which is a unit of its own. The page's descriptions of the
layouts, its resource and developer-documentation lists, and its change log state none.

What prompted it: a complaint, 2026-11-20, that an interface showed a command that does nothing in
the present state. Apple's page says an unavailable menu item is shown, dimmed, and that the menu
stays openable. It does not say, as Microsoft's does, that a contextual menu removes the item.

    python -m craft.census_apple_menus
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'For each menu item, write a label that clearly and succinctly describes it.': (
        'owed', '', 'a reading of the label'),
    'To be consistent with platform experiences, use title-style capitalization.': (
        'set aside', '', "states title style where Microsoft's page and sentence-labels-take-sentence-case state sentence style; platforms differ; left to the owner"),
    'Remove articles like a, an, and the from menu-item labels to save space.': (
        'owed', '', 'decidable: no leading article in a label'),
    'Show people when a menu item is unavailable.': (
        'covered', 'a-stable-menu-disables-what-does-not-apply', "the law; Apple states it without Microsoft's exception for contextual menus"),
    'If all of a menu’s items are unavailable, the menu itself needs to remain available so people can open it and learn about the commands it contains.': (
        'covered', 'a-menu-with-nothing-available-stays-openable', 'the law'),
    'Append an ellipsis to a menu item’s label when the action requires more information before it can complete.': (
        'covered', 'ellipsis-promises-more-input', 'the law'),
    'Represent common actions consistently.': (
        'owed', '', "decidable against the system's list of standard icons"),
    'Use menu item icons sparingly and with purpose.': (
        'set aside', '', 'a reading'),
    'Apply a uniform visual treatment across menu items in the same group.': (
        'owed', '', 'decidable: icons on all items of a group or none'),
    'Prefer listing important or frequently used menu items first.': (
        'set aside', '', 'a reading of importance'),
    'Consider grouping logically related items.': (
        'set aside', '', 'a consideration; a reading'),
    'Prefer keeping all logically related commands in the same group, even if the commands don’t all have the same importance.': (
        'set aside', '', 'a reading of relatedness'),
    'Be mindful of menu length.': (
        'owed', '', 'decidable by counting; the source gives no number'),
    'Use submenus sparingly.': (
        'owed', '', 'decidable by counting submenus; the source gives no number'),
    'Limit the depth and length of submenus.': (
        'owed', '', 'decidable: one level, about five items'),
    'Make sure a submenu remains available even when its nested menu items are unavailable.': (
        'covered', 'a-menu-with-nothing-available-stays-openable', 'the law, stated for a submenu'),
    'Prefer using a submenu to indenting menu items.': (
        'owed', '', 'decidable: no indented items in a menu'),
    'Consider using a changeable label that describes an item’s current state.': (
        'set aside', '', "contradicts Microsoft's rule not to change menu item names dynamically; left to the owner"),
    'Include a verb if a changeable label isn’t clear enough.': (
        'set aside', '', 'a reading, and bound to the changeable label above'),
    'If necessary, display both menu items instead of one toggled item.': (
        'set aside', '', 'a reading of need'),
    'Consider using a checkmark to show that an attribute is currently in effect.': (
        'set aside', '', 'a consideration; a reading'),
    'Consider offering a menu item that makes it easy to remove multiple toggled attributes.': (
        'set aside', '', 'a consideration; a reading'),
    'Let players navigate in-game menus using the platform’s default interaction method.': (
        'set aside', '', "a reading of the platform's default"),
    'Make sure your menus remain easy to open and read on all platforms you support.': (
        'set aside', '', "a reading; the size of the targets is targets-are-thumb-sized's"),
    'Choose a small or medium menu layout when it can help streamline people’s choices.': (
        'set aside', '', 'a reading of the choices'),
    'Prefer displaying a menu near the content it controls.': (
        'owed', '', 'decidable: the distance from menu to the content it controls, in a 3D scene'),
    'Prefer the subtle breakthrough effect in most cases.': (
        'set aside', '', 'a preference for one platform; a reading'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 27


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_apple_menus",
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
    print(f"Apple, Human Interface Guidelines, Menus: {len(CENSUS)} classified\n")
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
