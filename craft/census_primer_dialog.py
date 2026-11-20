"""A census: GitHub's Primer design system, Dialog, Guidelines, whole.

It roots stacked-dialogs-close-from-the-top-two-deep-at-most, and a source is adopted entire or
not at all (the source-the-rule protocol). The census unit is each sentence of the guidelines
page that says what a dialog has, does, should or should not do, read on 2026-11-20
(primer.style/product/components/dialog/guidelines): Anatomy (header, subheader, body, footer,
backdrop, spacing), Usage (keep content simple, nested dialogs, deep linking, any device) and
placement (centered, side sheets, bottom sheets, full-screen). The page's Accessibility tab is
another page and is not censused here. Primer's own measures (the 16 px safe area, 480 px) are
its product's values and set aside.

Two rows disagree with Material's first edition, censused in craft/census_m1_dialogs.py:
Primer accepts two nested dialogs where Material asks a dialog to open none unless it fills the
screen, and Primer requires a title on every dialog where Material says most alerts need none.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_primer_dialog
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- Anatomy ---------------------------------------------------------------------------
    "The title is required for all Dialogs, but may be visually hidden for custom scenarios such as a command palette.": (
        "owed", "", "decidable from the DOM: a dialog with no accessible title"),
    "The close button is required and may not be visually hidden.": (
        "owed", "", "decidable from the DOM and the rendered dialog"),
    "Secondary action IconButtons may be placed next to the close button.": (
        "set aside", "", "a permission"),
    "The subheader region is an optional space for interactive controls. Use it to display a search field, a filter menu, or a local navigation component.": (
        "set aside", "", "where an optional part goes; the component's anatomy"),
    "The body region is scrollable if the content exceeds the height of the Dialog.": (
        "set aside", "", "the component's own behaviour"),
    "Primary actions should be aligned to the right of the footer, and grouped by additional related actions. Secondary actions may be shown aligned to the left side.": (
        "owed", "", "decidable from the rendered footer"),
    "If the content area has overflow scrolling, a divider should be added between the footer and content area.": (
        "owed", "", "decidable from the rendered dialog when its body scrolls"),
    "By default, clicking on the backdrop will dismiss the Dialog. However, if the Dialog contains a form that can have unsaved changes, the backdrop won't dismiss the Dialog, regardless of the state of the form.": (
        "covered", "the-users-work-is-never-harmed-by-an-act-or-by-inaction",
        "a stray click outside never discards what the person typed"),
    "Content within the body and header should remain within the 16px safe area.": (
        "set aside", "", "Primer's own measure"),
    # --- Usage -----------------------------------------------------------------------------
    "Dialogs are meant to be interacted with in a single context. Avoid creating a whole page inside a Dialog. Prefer single-column layouts that convey a clear goal from the moment the Dialog is opened.": (
        "owed", "", "decidable from the rendered dialog: columns, its own navigation"),
    "If the answer is no, or if a side navigation is required for the feature, consider designing a new page.": (
        "owed", "", "the same rule, its consequence: no side navigation in a dialog"),
    "It is acceptable to have up to two nested Dialogs as long as the Dialog is implemented with expected focus management behavior.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most", "quoted by the law"),
    "Upon closing the second nested Dialog, focus should return to the trigger control within the first Dialog.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most", "quoted by the law"),
    "When the two stacked Dialogs are open, pressing Esc should only close the top-level Dialog.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most", "quoted by the law"),
    "When one clicks outside of the second Dialog with a mouse, only the second Dialog should close.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most", "quoted by the law"),
    "However, having more than three nested Dialogs is discouraged because it adds unnecessary complexity to the user experience and can be disorienting for some users.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most",
        "quoted by the law, which takes the two the page accepts"),
    "It's crucial to consider if the Dialog should be accessible via a link. ... In such situations, it is often more advisable to avoid using a Dialog altogether and instead display the additional information directly on the page or create a new dedicated page.": (
        "owed", "", "needs a fact: whether the content is linked to from outside"),
    "Dialogs must adjust their designs to fit in smaller viewports. Make sure the Overlay contents work with all supported sizes and input methods.": (
        "owed", "", "decidable by rendering the dialog at each supported width"),
    # --- Placement -------------------------------------------------------------------------
    "By default, Dialog appears centered in the viewport, with a visible backdrop that dims the rest of the window for focus. Centered Dialogs are surrounded by a safe area of 16px between the frame and the viewport for all sizes.": (
        "set aside", "", "the component's default and Primer's own measure"),
    "Left side sheets are reserved for global navigation drawers. Right side sheets are used for global actions, but can also be considered for quick previews in full-width pages.": (
        "owed", "", "decidable from a sheet's side and what it holds"),
    "Side sheets take the entire height of the viewport, and should be used sparingly. Don't use side sheets to present create/edit forms, or flows that may contain a lot of information. For that, use a page instead.": (
        "owed", "", "decidable: a form in a side sheet"),
    "Side sheets are still considered as Dialogs, which means that interacting with the content in the background is not possible. This needs to be indicated by a backdrop and should always cover the global navigation.": (
        "owed", "", "decidable from the rendered sheet and its backdrop"),
    "Unless it's a global action, avoid side sheets in pages where content does not stretch the full width of the page.": (
        "owed", "", "decidable from the page's content width"),
    "A bottom sheet always dims the rest of the screen for focus and takes up the full width of the viewport. Tapping on the backdrop dismisses the Dialog. Use a bottom to indicate that the user is still in the context of the main page, and that the Dialog is a secondary action.": (
        "owed", "", "decidable from the rendered sheet at a narrow width"),
    "In landscape mode, a bottom sheet has a maximum width of 480px, and is centered horizontally.": (
        "set aside", "", "Primer's own measure"),
    "Full-screen Dialogs may be used to present content that needs all the available space on narrow viewports, or to act as a new page without navigating away from the main page. Dialogs that have one or more input fields should always use the full-screen variant.": (
        "owed", "", "decidable at a narrow width: a dialog with an input that does not fill the screen"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 26


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_primer_dialog",
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
    print(f"Primer, Dialog guidelines: {len(CENSUS)} classified\n")
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
