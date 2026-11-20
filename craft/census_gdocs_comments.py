"""A census: Google Docs Editors Help, Use comments, action items & emoji reactions, whole.

A source is adopted entire or not at all (the source-the-rule protocol), and this one states no
rule craft-laws lacks: it is one product's help page, saying how to use the product, and a
product doing a thing is a precedent, not a rule. The census unit is each section of each of
the page's three tabs - Computer, Android phone & tablet, iPhone & iPad - read on 2026-11-20
(support.google.com/docs/answer/65129, the phone tabs at the same address with
co=GENIE.Platform=Android and =iOS). Every row is set aside as a description.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20, which cited a comment anchored to highlighted text
and comments minimised to icons in the margin.

    python -m craft.census_gdocs_comments
"""

from __future__ import annotations

_DESC = "describes the product; states no rule"

# section -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "Add a comment: Highlight the text, images, cells, slides, or scenes you want to comment on. To add a comment, in the toolbar, click Add comment.": (
        "set aside", "", _DESC + "; the comment is anchored where it applies"),
    "Show, hide, or minimize comments: ... Minimize comments: Reduces comments to icons in Docs and Sheets, which you can hover over to preview and click to show more.": (
        "set aside", "", _DESC),
    "Find comments: In the top right, click Show all comments. To find the location of a comment, click the comment. Search all comments by keywords or usernames.": (
        "set aside", "", _DESC),
    "Find a comment's location in Google Sheets: point to the comment notification on the tab; click the cell location.": (
        "set aside", "", _DESC),
    "Filter comments: all or for you; open or resolved; by sheet.": (
        "set aside", "", _DESC),
    "Edit or delete a comment: click More, then Edit or Delete.": (
        "set aside", "", _DESC),
    "Send a comment to a specific person: enter @ and their name or email address; they receive an email notification.": (
        "set aside", "", _DESC),
    "Add more comments after comment limit: resolve inactive comments, make a copy with Copy comments and suggestions.": (
        "set aside", "", _DESC),
    "Reply to comments in documents or presentations; reply to comments in spreadsheets.": (
        "set aside", "", _DESC),
    "Close or reopen a comment: click Resolve; Re-open from Comments.": (
        "set aside", "", _DESC),
    "Assign an action item in a comment; reassign an action item; mark an action item as done.": (
        "set aside", "", _DESC),
    "See the follow-ups on a document: click the number in the top right corner; If you don’t see a number, you don’t have any follow-ups for that document. To go to the first action item or suggestion, click an option from the list.": (
        "set aside", "", _DESC + "; a count that opens a list of the open items"),
    "Add emoji reactions to highlighted content in Google Docs; add emoji reactions to comments.": (
        "set aside", "", _DESC),
    "Remove or resolve emoji reactions.": (
        "set aside", "", _DESC),
    "Use keyboard shortcuts to navigate & reply to comments: R reply, J next, K previous, E resolve, U exit.": (
        "set aside", "", _DESC),
    # --- Android phone & tablet -------------------------------------------------------------
    "Android: View all comments: At the top, tap Comment. To move through discussion threads, swipe left or right.": (
        "set aside", "", _DESC),
    "Android: Add comments: Select the text or cell. Tap More Add Comment. Add your text. Tap Send.": (
        "set aside", "", _DESC),
    "Android: Respond to comments: edit, reply, resolve, move between comments by swiping, delete, Close to return to editing.": (
        "set aside", "", _DESC),
    "Android: Send a comment to a specific person: enter @ and their name or email address.": (
        "set aside", "", _DESC),
    "Android: Accept or reject a suggested edit: tap Suggestion, then Accept or Reject; Undo.": (
        "set aside", "", _DESC),
    "Android: Add comments in Microsoft Office files: change the file to a Google Docs file.": (
        "set aside", "", _DESC),
    "Android: Assign, reassign and mark done an action item.": (
        "set aside", "", _DESC),
    "Android: See the follow-ups on a document: At the top-right, tap the number.": (
        "set aside", "", _DESC),
    "Android: Add emoji reactions; archive emoji reactions (Mark done).": (
        "set aside", "", _DESC),
    # --- iPhone & iPad ------------------------------------------------------------------------
    "iPhone & iPad: View all comments: tap Comment. To find a single comment: In a document, look for yellow highlighted text. In a cell, look for an orange corner.": (
        "set aside", "", _DESC + "; the mark is at the place the comment is about"),
    "iPhone & iPad: Add comments: Select the text or cell and tap Add Comment. Add your text. Tap Done.": (
        "set aside", "", _DESC),
    "iPhone & iPad: Respond to comments: edit, reply, resolve, swipe between comments, delete, swipe down to return to editing.": (
        "set aside", "", _DESC),
    "iPhone & iPad: Send a comment to a specific person; Note: The owner of a document will get notifications for all comments by default.": (
        "set aside", "", _DESC),
    "iPhone & iPad: Accept or reject a suggested edit: tap Hidden Suggestion, then Accept or Reject; Undo.": (
        "set aside", "", _DESC),
    "iPhone & iPad: Assign, reassign and mark done an action item.": (
        "set aside", "", _DESC),
    "iPhone & iPad: See the follow-ups on a document: tap the number in the top right corner.": (
        "set aside", "", _DESC),
    "iPhone & iPad: Add emoji reactions; archive emoji reactions (Mark done).": (
        "set aside", "", _DESC),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 32


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_gdocs_comments",
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
    print(f"Google Docs Editors Help, comments: {len(CENSUS)} classified\n")
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
