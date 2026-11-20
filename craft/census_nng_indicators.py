"""A census: Kim Flaherty, Indicators, Validations, and Notifications (Nielsen Norman Group, 2024-01-17), whole.

It roots an-indicator-sits-beside-what-it-marks, and a source is adopted entire or not at all
(the source-the-rule protocol). The census unit is each sentence of the article that says what
an indicator, a validation message or a notification is, should be or should not be, read on
2026-11-20 (nngroup.com/articles/indicators-validations-notifications/): the opening, the three
sections, "Picking the Right Communication Option Is Important" and the conclusion. The
examples (Yelp, American Century, Cobragolf, Bestbuy, Uniqlo, Mac OS, Adobe, Visual Comfort,
Mango, iPhone, Mint, Allmodern) illustrate the sentences listed and state nothing of their own.

One sentence contradicts a law: the article calls "Please enter your street address" more
polite, and error-neither-begs-nor-blames, on GOV.UK's ground, bans "please" in an error. It
is set aside here and left to the owner.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_nng_indicators
"""

from __future__ import annotations

# rule -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    "a system, whether an application, website, or piece of hardware (anything from a smartwatch to a thermostat), should always keep users informed, by providing appropriate feedback.": (
        "covered", "status-is-visible", "the heuristic the article opens on"),
    "An indicator is a way of making a page element (be it content or part of the user interface) stand out to inform the user that there is something special about it that warrants the user’s attention.": (
        "set aside", "", "a definition"),
    "If something always looks the same, it’s not an indicator, no matter how flamboyantly it’s designed.": (
        "set aside", "", "a definition"),
    "There are at least three possible ways of implementing indicators: icons, typographical variations, enlarged size or animation.": (
        "set aside", "", "the means, not a rule"),
    "Indicators are contextual. They are associated with a UI element or with a piece of content, and should be shown in close proximity to that element.": (
        "covered", "an-indicator-sits-beside-what-it-marks", "quoted by the law"),
    "Indicators are conditional— they are not always present, but appear or change depending on certain conditions.": (
        "set aside", "", "a definition of what an indicator is"),
    "Indicators are passive. They do not require that a user take action, but are used as a communication tool to cue the user to something of note.": (
        "set aside", "", "a definition of what an indicator is"),
    "Indicators can introduce noise and clutter to your overall interface, and may distract users, so it is important to consider how many (if any) indicators to use in your design.": (
        "set aside", "", "a reading, with five questions to weigh; no observation decides it"),
    "if the user’s input is incorrect, the system should inform the user by providing an identifiable and clear message that aids in correcting the error.": (
        "covered", "error-says-the-fix", "the message aids the correction"),
    "Validation messages should follow the guidelines for error messages rather than simply identifying the problem, they should tell users how to fix it.": (
        "covered", "error-says-the-fix", "the fix, not only the problem"),
    "don’t state “Field is blank.” Please enter your street address” is more polite and directs to a solution.": (
        "set aside", "",
        "the solution half is error-says-the-fix; the 'please' half contradicts "
        "error-neither-begs-nor-blames and is left to the owner"),
    "Since validation is contextual, it can be helpful to use an icon indicator along with the validation message to help communicate which input(s) are missing or need corrected.": (
        "owed", "", "decidable from the DOM once a field is in error; no law asks for it"),
    "Action-required notifications are often urgent and should be intrusive; for instance, they could be implemented as modal popups that interrupt the user, forcing immediate attention and requiring an action to be dismissed.": (
        "owed", "", "decidable once a notification is marked as requiring action"),
    "Passive notifications are typically not urgent and should be less intrusive. A typical implementation of a passive notification may be a badge icon or a small nonmodal popover in a corner of a screen.": (
        "owed", "", "the other half of the same choice"),
    "When the information provided by the notification is key to the understanding of the system, an easy-to-ignore passive notification can be problematic.": (
        "owed", "", "needs a fact: which information is key"),
    "This requires notifications to establish more context and provide users with sufficient background information to understand what the notification is about.": (
        "owed", "", "a notification names what it is about; needs that fact recorded"),
    "If a notification is contextual and relates to a specific element in the interface, an icon indicator on the element can communicate where that notification applies and catch the user’s attention.": (
        "owed", "", "decidable from the DOM; no law asks for it"),
    "A notification sent irrespective of the current user goal would likely be ignored, and may even annoy users because it will disrupt their current task and be irrelevant to their current needs.": (
        "owed", "", "needs a fact: the person's current goal"),
    "a toast (a small nonmodal popup that disappears after a few seconds ...), while appropriate for passive notifications, would be a bad way to implement an error message, be it validation or otherwise.": (
        "owed", "", "decidable: an error shown only in an element that removes itself"),
    "Such notifications sometimes cause issues for e-commerce shoppers who do not notice the message due to its location far away from the user's area of focus at the time": (
        "set aside", "",
        "an observation of one site; status-is-visible holds the rule it breaks"),
    "This may be better communicated by showing a passive nonmodal popover in the corner of the screen that can be seen, but doesn’t require the user to take action to clear it.": (
        "set aside", "", "an example of the passive-notification sentence above"),
    "Indicators provide supplementary information about a dynamic piece of content or UI element. They are conditional —that is, they may appear or change under specific conditions.": (
        "set aside", "", "the conclusion restating the definitions"),
    "Validations are tied to a user’s action or input. Notifications are focused on system-related events.": (
        "set aside", "", "the conclusion restating the definitions"),
    "By assessing the type of information delivered, we can determine the correct mechanism to use.": (
        "set aside", "", "the method the article teaches; a reading"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 24


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_nng_indicators",
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
    print(f"NN/g, Indicators, Validations, and Notifications: {len(CENSUS)} classified\n")
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
