"""A census: Therese Fessenden, Modal & Nonmodal Dialogs: When (& When Not) to Use Them (Nielsen Norman Group, 2017-04-23), whole.

It roots a-modal-dialog-holds-what-its-decision-needs and a-modal-dialog-serves-the-task-at-hand,
and a source is adopted entire or not at all (the source-the-rule protocol). The census unit
is each disadvantage the article lists, each of its seven numbered guidelines with the rules
stated under it, and the rules of "Consider Nonmodal Dialogs Instead" and the conclusion, read
on 2026-11-20 (nngroup.com/articles/modal-nonmodal-dialog/). The definitions of dialog, mode,
modal and nonmodal, and the examples (PowerPoint, Gmail, Etsy, Zillow, GoodHousekeeping,
Wayfair, Walmart, Frontier, Meowbox), state no rule of their own.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_nng_modal
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- Disadvantages of Modal Dialogs ---------------------------------------------------
    "They require immediate attention.": (
        "set aside", "", "a disadvantage: the reason for the guidelines"),
    "They interrupt the user’s workflow.": (
        "set aside", "", "a disadvantage: the reason for the guidelines"),
    "They cause users to forget what they were doing.": (
        "set aside", "", "a disadvantage: the reason for the guidelines"),
    "They cause the users to create and address an extra goal — to dismiss the dialog.": (
        "set aside", "", "a disadvantage: the reason for the guidelines"),
    "They block the content in the background. When a dialog appears on top of the current window, it can cover important content and remove context.": (
        "covered", "a-modal-dialog-holds-what-its-decision-needs", "quoted by the law"),
    # --- Guidelines for Using Modal Dialogs ----------------------------------------------
    "1. Use modal dialogs for important warnings, as a way to prevent or correct critical errors.": (
        "owed", "", "needs a fact: which errors are critical or irreversible"),
    "an error in a form should be reported on the page, next to where it occurred, so that users can refer to the error message while they fix the problem.": (
        "covered", "error-lands-at-the-field", "the error beside its field, not in a modal"),
    "2. Use modal dialogs to request the user to enter information critical to continuing the current process.": (
        "owed", "", "needs a fact: what the process cannot continue without"),
    "3. Modal dialogs can be used to fragment a complex workflow into simpler steps.": (
        "owed", "", "a permission; no law states it"),
    "So if you must do multiple-step modals, give users a sense of their progress, so they don’t abandon immediately.": (
        "owed", "", "decidable: a multi-step modal shows the step and the count"),
    "That said, if it requires multiple steps to begin with, it probably justifies dedicating a full page to it.": (
        "owed", "", "decidable: a modal with several steps"),
    "4. Use modal dialogs to ask for information that, when provided, could significantly lessen users’ work or effort.": (
        "owed", "", "needs a fact: what the answer saves"),
    "5. Do not use modal dialogs for nonessential information that is not related to the current user flow.": (
        "covered", "a-modal-dialog-serves-the-task-at-hand", "quoted by the law"),
    "6. Avoid modal dialogs that interrupt high-stake processes such as checkout flows.": (
        "owed", "", "needs a fact: which processes are high-stake"),
    "7. Avoid modal dialogs for complex decision making that requires additional sources of information unavailable in the modal.": (
        "covered", "a-modal-dialog-holds-what-its-decision-needs", "quoted by the law"),
    "Modal dialogs should be used for short, direct dialogs with the user.": (
        "covered", "a-modal-dialog-holds-what-its-decision-needs", "quoted by the law"),
    # --- Consider Nonmodal Dialogs Instead -------------------------------------------------
    "In situations where the task is not critical, a nonmodal dialog might be appropriate.": (
        "owed", "", "needs the same fact as guideline 1"),
    "However, they can still be disruptive, especially if they obscure important information on the screen or if they require too complex interactions.": (
        "covered", "no-element-covers-another", "a nonmodal dialog covering what must be read"),
    "Nonmodal windows are useful when users need to quickly switch between modes in order to access certain information.": (
        "set aside", "", "when they help; a reading"),
    # --- Conclusion -----------------------------------------------------------------------
    "Avoid unnecessarily interrupting users and disrupting their workflows.": (
        "set aside", "", "the conclusion restating the guidelines"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 20


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_modal",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the article's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"NN/g, Modal & Nonmodal Dialogs: {len(CENSUS)} classified\n")
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
