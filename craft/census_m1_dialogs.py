"""A census: Google, Material Design (first edition), Components, Dialogs, whole.

It roots a-dialog-opens-no-dialog-unless-it-fills-the-screen, and a source is adopted entire or
not at all (the source-the-rule protocol). The census unit is each sentence of the page that
says what a dialog is, does, should or should not do, read on 2026-11-20
(m1.material.io/components/dialogs.html): Behavior, Alerts, Simple menus, Simple dialogs,
Confirmation dialogs, Full-screen dialogs and Specs. A sentence the page repeats (the
full-screen title that wraps then truncates) is one row. Material's own measures (dp values,
keylines) are set aside as one row each block.

Two sentences contradict a law: "The confirmation action is disabled until all mandatory
fields in the dialog are met" and "Affirmative actions are more likely to be disabled until a
choice is made", against no-disabled-submit (GOV.UK, Button). They are set aside here and left
to the owner. Two rows disagree with Primer (craft/census_primer_dialog.py): Primer accepts two
nested dialogs, and requires a title where this page says most alerts need none.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_m1_dialogs
"""

from __future__ import annotations

_MEASURE = "Material's own measure"

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- Behavior ---------------------------------------------------------------------------
    "Use dialogs sparingly because they are interruptive. ... Not every choice, setting, or detail warrants interruption. Alternatives to dialogs include menus or inline expansion, both of which maintain the current context.": (
        "owed", "", "needs a fact: which choices warrant an interruption"),
    "Dialogs should never be obscured by other elements or appear partially on screen.": (
        "covered", "no-element-covers-another", "the obscured half; the off-screen half is owed with it"),
    "Dialogs always retain focus until dismissed or a required action has been taken, such as choosing a setting.": (
        "owed", "", "decidable: Tab never leaves an open dialog"),
    "Dialogs should avoid: Opening dialogs from within a dialog": (
        "covered", "a-dialog-opens-no-dialog-unless-it-fills-the-screen", "quoted by the law"),
    "Dialogs should avoid: Containing scrolling content": (
        "owed", "", "decidable from the rendered dialog"),
    "Full-screen dialogs may open additional dialogs, such as pickers, because their design accommodates additional layers of material": (
        "covered", "a-dialog-opens-no-dialog-unless-it-fills-the-screen", "quoted by the law"),
    "For scrollable lists of options, the dialog title remains pinned to the top. ... Otherwise, the title scrolls off with the content. Actions always remain in place when content scrolls.": (
        "owed", "", "decidable by scrolling the dialog"),
    "Dialogs are separate from the underlying parent material and do not scroll with it.": (
        "owed", "", "decidable by scrolling the page under the dialog"),
    "To disclose additional content in a dialog, do so using inline expansion within the content area. Or consider alternative components that are optimized for large amounts of content.": (
        "owed", "", "decidable: what a dialog's 'more' opens"),
    "Dialogs may be dismissed either by tapping outside of the dialog, or tapping the system back button (on Android).": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "Back on Android"),
    # --- Alerts -----------------------------------------------------------------------------
    "Alerts are urgent interruptions, requiring acknowledgement, that inform the user about a situation.": (
        "set aside", "", "a definition"),
    "Snackbars present optional information after an action, such as confirming the discarding of a draft. They often allow a user to undo an action just taken.": (
        "set aside", "", "a definition, to tell the two apart"),
    "Most alerts don't need titles.": (
        "owed", "", "decidable from the DOM; Primer requires a title on every dialog"),
    "They summarize a decision in a sentence or two by either: Asking a question ... Making a statement related to the action buttons": (
        "owed", "", "decidable: an alert's text is one or two sentences"),
    "The affirmative action text “Discard” clearly indicates the outcome of the decision. ... A better action pair would be an explicit “Cancel” and “Delete.”": (
        "covered", "says-what-happens", "the button says the outcome, not 'No'"),
    "Use title bar alerts only for high-risk situations, such as the potential loss of connectivity.": (
        "owed", "", "needs a fact: which situations are high-risk"),
    "Users should be able to understand the choices based on the title and button text alone.": (
        "owed", "", "a reading of the title and buttons together"),
    "Use a clear question or statement with an explanation in the content area, such as \"Erase USB storage?\"": (
        "owed", "", "the title's form; a reading"),
    "Avoid apologies, ambiguity, or questions, such as “Warning!” or “Are you sure?”": (
        "owed", "",
        "the apology half is error-neither-begs-nor-blames for an error; no law covers an "
        "alert's title"),
    # --- Simple menus and simple dialogs ------------------------------------------------------
    "Simple menus display options for list items, and they immediately commit choices upon selection.": (
        "set aside", "", "a definition"),
    "Simple dialogs can display the same content as simple menus. However, simple menus are preferred because they are less disruptive to the user’s current context.": (
        "owed", "", "decidable: a dialog whose only content is a list of options"),
    "Choosing an option immediately commits the option and closes the menu. Touching outside of the dialog, or pressing Back, cancels the action and closes the dialog": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "Back closes it"),
    "Simple dialogs are more interruptive than simple menus and should be used sparingly.": (
        "owed", "", "the same rule as the menus' preference"),
    "On mobile, a dialog’s width is based on a multiple of a unit.": (
        "set aside", "", _MEASURE),
    "Simple dialogs do not have explicit buttons that accept or cancel an operation.": (
        "owed", "", "decidable from the DOM"),
    "Row heights can vary in simple dialogs; centered; at least 40dp left and right, 24dp top and bottom; content 24dp from the edge.": (
        "set aside", "", _MEASURE),
    "If any text in a simple menu wraps to another line, use a simple dialog instead.": (
        "owed", "", "decidable from the rendered menu"),
    # --- Confirmation dialogs -----------------------------------------------------------------
    "Confirmation dialogs require users to explicitly confirm their choice before an option is committed.": (
        "set aside", "", "a definition"),
    "Tapping “Cancel” in a confirmation dialog, or pressing “Back,” cancels the action, discards any changes, and closes the dialog.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "Back closes it"),
    "Confirmation dialogs should avoid launching additional simple dialogs or simple menus, as they add complexity and appear to increase an app’s elevation. If they are needed to complete a task, consider using a full-screen dialog instead.": (
        "covered", "a-dialog-opens-no-dialog-unless-it-fills-the-screen", "quoted by the law"),
    "Confirmation dialogs can use layouts other than lists, such as a date picker, but remain focused on specifying a single value": (
        "owed", "", "decidable: the controls in a confirmation dialog set one value"),
    "Confirmation dialogs provide both an explicit confirmation button and explicit cancel button. ... A single dialog button makes the system Back action ambiguous": (
        "owed", "", "decidable from the DOM"),
    # --- Full-screen dialogs -------------------------------------------------------------------
    "Mobile only: Due to limited space, full-screen dialogs may be more appropriate for mobile devices than dialogs used on devices with larger screens.": (
        "set aside", "", "a reading"),
    "Full-screen dialogs group a series of tasks (such as creating a calendar entry) before they may be committed or discarded. No selections are saved until “Save” is touched. Touching the “X” discards all changes and exits the dialog.": (
        "set aside", "", "a definition"),
    "Full-screen dialogs may be used for content or tasks that meet any of these criteria: an input method editor; changes not saved in real time; no draft capability; batch operations": (
        "owed", "", "needs facts the criteria name"),
    "Place confirmation and dismissive actions for full-screen dialogs at the top of the screen.": (
        "owed", "", "decidable from the rendered dialog"),
    "The confirmation action in the top right of the screen uses descriptive verbs, such as: save, send, share, update or create. Don’t use vague actions for confirming action, such as: done, ok or close.": (
        "covered", "says-what-happens", "the verb of the act, not 'done'"),
    "The confirmation action is disabled until all mandatory fields in the dialog are met.": (
        "set aside", "", "contradicts no-disabled-submit; left to the owner"),
    "Both the discard action (the “X” at the top left of the screen) and the Back button close the full-screen dialog and discard changes. If no changes have been made, ... no discard confirmation is required. If the user has made any changes, they are prompted to confirm the discard action": (
        "covered", "the-users-work-is-never-harmed-by-an-act-or-by-inaction",
        "changes are discarded only after the person confirms"),
    "The “X” used in a full-screen dialog differs from an up arrow, which indicates the view’s state is constantly being saved.": (
        "owed", "", "decidable: the close glyph against whether changes are kept"),
    "Full-screen dialog titles don’t use dynamic type.": (
        "set aside", "", _MEASURE),
    "Titles should be succinct. They can wrap to a second line if necessary, and should then be truncated.": (
        "owed", "", "decidable from the rendered title"),
    "If the full-screen dialog uses titles of variable length or anticipates long titles (for example, because certain words are longer in different languages), place title text in the content area of the dialog instead of the app bar.": (
        "owed", "", "one remedy for what layout-survives-longer-translations asks; no law names it"),
    # --- Specs ----------------------------------------------------------------------------------
    "The title briefly describes the type of choice being made. Titles should always be displayed in their entirety and only used when necessary.": (
        "owed", "", "decidable from the rendered title"),
    "Dialog content ... is focused on a specific task, such as confirming item deletion or choosing a setting.": (
        "covered", "one-surface-one-job", "one task per dialog"),
    "Dialogs present a focused and limited set of actions, which are generally affirmative or dismissive.": (
        "owed", "", "decidable from the DOM, with the next row's count"),
    "Affirmative actions are placed on the right side and continue the process. ... Dismissive actions are placed directly to the left of affirmative actions": (
        "owed", "", "decidable from the rendered actions"),
    "Dismissive and affirmative action text can be “Cancel”/“OK” or specific active verbs or verb phrases that indicate the outcome of the decision.": (
        "set aside", "", "a permission; says-what-happens is narrower and stands"),
    "Dialog actions should present a clear choice directly related to the dialog’s title and content.": (
        "owed", "", "a reading of actions against title"),
    "In situations where users are required to acknowledge the dialog’s content to proceed, an alert may contain only one action. Use this type of alert sparingly as it is interruptive. Consider other methods of communicating the information to users, such as in-line with a view’s content.": (
        "owed", "", "needs a fact: whether acknowledgement is required"),
    "Dialogs should not include more than two actions. A third action, such as “Learn more,” navigates away from the dialog, potentially leaving the task unfinished.": (
        "owed", "", "decidable from the DOM"),
    "Avoid using a “Learn more” action to access help documentation; in-line expansion within the dialog should be used instead. If more extensive information is needed, provide it prior to entering the dialog.": (
        "owed", "", "decidable: an action that leaves the dialog for help"),
    "Dialog actions use system colors by default, but they should reflect your product's color palette. Use a contrasting color, such as the palette’s accent color, to distinguish dialog actions from dialog content.": (
        "owed", "", "decidable from rendered colours"),
    "For languages without capitalization (such as Chinese, Japanese or Korean), it is important to maintain consistent placement, spacing, and colors for actions to distinguish them from regular text.": (
        "covered", "one-act-one-look-one-place", "the same look and place for actions"),
    "Affirmative actions are more likely to be disabled until a choice is made. Dismissive actions are never disabled.": (
        "set aside", "", "the first half contradicts no-disabled-submit; left to the owner"),
    "Content guidelines and button width and padding: 24dp, 20dp, 8dp, 36dp, 52dp, 64dp minimum width": (
        "set aside", "", _MEASURE),
    "Side-by-side buttons are recommended when the text of each label does not exceed the maximum button width ... (Dialog width - 8dp - 8dp - 8dp)/2": (
        "owed", "", "decidable from rendered label widths"),
    "When text labels exceed the maximum button width, use stacked buttons to accommodate the text. Affirmative actions are stacked above dismissive actions.": (
        "owed", "", "decidable from the rendered actions"),
    "Touchable target height for each button: 48dp": (
        "set aside", "", "Material's measure; targets-are-thumb-sized holds the floor it agrees with"),
    "Simple dialog keylines: vertical keyline at 24dp; content with an icon or avatar at 80dp.": (
        "set aside", "", _MEASURE),
    "It is recommended that simple dialogs have titles, but titles can be omitted based on your product’s needs.": (
        "owed", "", "decidable from the DOM"),
    "Full-screen dialog title measures: app bar 56dp or 80dp, keyline 72dp, 20sp, padding 20dp, 16dp, 14sp.": (
        "set aside", "", _MEASURE),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 62


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_m1_dialogs",
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
    print(f"Material Design (first edition), Dialogs: {len(CENSUS)} classified\n")
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
