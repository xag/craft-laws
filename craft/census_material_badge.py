"""A census: Material Components for Android, Badges (docs/components/BadgeDrawable.md), whole.

It roots a-badge-sits-on-the-top-corner-of-an-icon-or-navigation-item, and a source is adopted
entire or not at all (the source-the-rule protocol). The page documents one component of one
library: the census unit is each statement of what a badge is for, where it goes and what it
shows, and each section of how to build one, read on 2026-11-20
(github.com/material-components/material-components-android/blob/master/docs/components/BadgeDrawable.md,
fetched raw). Material 3's badges page, which the doc links to, returned only its title to the
design review and is not this source.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_material_badge
"""

from __future__ import annotations

_BUILD = "how to build one with this library"

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Badges show notifications, counts, or status information on navigation items and icons.": (
        "covered", "a-badge-sits-on-the-top-corner-of-an-icon-or-navigation-item",
        "quoted by the law"),
    "Badges can contain dynamic information, such as a number of pending requests.": (
        "set aside", "", "what a badge may hold; a description"),
    "There are two variants of badges: small badge, large badge (container and label).": (
        "set aside", "", "the component's anatomy"),
    "Key properties: color, width, height, shape, label, label length, label text color and appearance, gravity, offset alignment, padding, large font vertical offset, fixed edge.": (
        "set aside", "", _BUILD),
    "If both app:badgeText and app:number are specified, the badge label will be app:badgeText.": (
        "set aside", "", _BUILD),
    "A BadgeDrawable represents dynamic information such as a number of pending requests in a BottomNavigationView or TabLayout.": (
        "covered", "a-badge-sits-on-the-top-corner-of-an-icon-or-navigation-item",
        "a navigation item"),
    "Adding badges: create(Context); attach with BadgeUtils.attachBadgeDrawable, as a ViewOverlay (API 18+) or the foreground of a FrameLayout ancestor (before 18).": (
        "set aside", "", _BUILD),
    "By default, (TOP_END) badge aligns with the top and end edges of the anchor (with some offsets). Alternatively, you can use TOP_START to align the badge with the top and start edges of the anchor.": (
        "covered", "a-badge-sits-on-the-top-corner-of-an-icon-or-navigation-item",
        "quoted by the law"),
    "Note that BOTTOM_START and BOTTOM_END are deprecated and not recommended for use.": (
        "covered", "a-badge-sits-on-the-top-corner-of-an-icon-or-navigation-item",
        "quoted by the law"),
    "To adjust the badge's offsets relative to the anchor's center, use setHorizontalOffset(int) or setVerticalOffset(int)": (
        "set aside", "", _BUILD),
    "Regardless of offsets, badges are automatically moved to within the bounds of its first ancestor view that does not clip its children, to ensure that the badge is not clipped if there is enough space.": (
        "owed", "", "a badge is never clipped; decidable from rendered boxes"),
    "BadgeDrawable provides a getter for its content description, which is based on the displayed number or text (if any). ... setContentDescriptionQuantityStringsResource ... setContentDescriptionExceedsMaxBadgeNumberStringResource ... setContentDescriptionNumberless": (
        "owed", "",
        "a badge says in words what it counts, through the language's plural forms "
        "(plurals-and-agreement holds the plural half); no law asks for the description"),
    "This component is still under development and may not support the full range of customization Material Android components generally support": (
        "set aside", "", "a note on the library"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 13


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_material_badge",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the doc's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Material Components for Android, Badges: {len(CENSUS)} classified\n")
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
