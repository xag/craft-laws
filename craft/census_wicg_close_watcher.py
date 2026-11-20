"""A census: WICG, Close Watchers explainer (archived; merged into the HTML Standard), whole.

It roots an-overlay-closes-on-the-devices-close-request, with MDN's reference
(craft/census_mdn_closewatcher.py), and a source is adopted entire or not at all (the
source-the-rule protocol). The explainer proposes a browser interface: the census unit is each
statement of the problem, each goal, each statement of what developers do today, and each
section of the proposal, the alternatives and the security and privacy considerations, read on
2026-11-20 (github.com/WICG/close-watcher/blob/main/README.md, fetched raw). Most of it is about
designing the interface and states no rule for what a person sees; the rows that do are routed.

What prompted it: the review of a written design for marks on the places an assembly
instructions viewer can improve, 2026-11-20.

    python -m craft.census_wicg_close_watcher
"""

from __future__ import annotations

_API = "the interface's design, not a rule for what a person sees"

# statement -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- The problem -------------------------------------------------------------------------
    "An important common feature of these components is that they are designed to be easy to close, with a uniform interaction mechanism for doing so. Typically, this is the Esc key on desktop platforms, and the back button on some mobile platforms (notably Android).": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "quoted by the law"),
    "We define a close request as a platform-mediated interaction that's intended to close an in-page component. This is distinct from page-mediated interactions, such as clicking on an \"x\" or \"Done\" button, or clicking on the backdrop outside of the modal.": (
        "set aside", "", "a definition"),
    "The user might click the back button hoping to close the date picker, like they would in a native app. But instead, the back button navigates the web page's history tree, likely closing the whole form and losing the filled information.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "the defect the law prevents"),
    # --- Goals ---------------------------------------------------------------------------------
    "Allow web developers to intercept close requests (e.g. Esc on desktop, back button on Android, \"z\" gesture on iOS using VoiceOver) to close custom components that they create.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "the goal the law states for the person"),
    "Discourage platform-specific code for handling modal close requests, by providing an API that abstracts away the differences.": (
        "set aside", "", _API),
    "Allow future platforms to introduce new close requests (e.g., the introduction of the swipe-from-the-sides dismiss gesture in Android 10), such that code written against the API proposed here automatically works on such platforms.": (
        "set aside", "", _API),
    "Prevent abuse that traps the user on a given history state by disabling the back button's ability to actually navigate backward in history.": (
        "owed", "", "a page never takes Back from the person; decidable by pressing Back"),
    "Be usable by component authors, in particular by avoiding any global state modifications that might interfere with the app or with other components.": (
        "set aside", "", _API),
    "Specify uniform-per-platform behavior across existing platform-provided components, e.g. <dialog>, <input> pickers, and fullscreen.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "every overlay alike"),
    "Allow the developer to confirm a close request with the user, to avoid potential data loss.": (
        "covered", "the-users-work-is-never-harmed-by-an-act-or-by-inaction",
        "a close that would lose input asks first"),
    "Explain <dialog>'s existing close and cancel events in terms of this model.": (
        "set aside", "", _API),
    "Avoid an awkward transition period ... right now users generally know the Android back button fails to close modals in web apps and avoid it when modals are open": (
        "set aside", "", "an observation of users and a goal the authors gave up"),
    # --- What developers are doing today ------------------------------------------------------
    "On desktop platforms, this problem is currently solved by listening for the keydown event, and closing the component when the Esc key is pressed. ... this can be easy to get wrong, e.g. by accidentally listening for keyup or keypress.": (
        "set aside", "", "how it is built today"),
    "This UI state is non-navigational, i.e., the URL doesn't and shouldn't change when opening a component. When the page is reloaded or shared, web developers generally don't want to automatically re-open the same component.": (
        "owed", "", "decidable: the address before and after opening an overlay"),
    "It's very hard to determine when the component's state is popped out of history ... The history.state API ... is rather fragile ... History navigation is not cancelable. ... A shared component that attempts to use the history API to implement these techniques can easily corrupt a web application's router.": (
        "set aside", "", "why the history interface is a poor fit; facts about it"),
    # --- Proposal --------------------------------------------------------------------------------
    "If more than one CloseWatcher is active at a given time, then only the most-recently-constructed one gets events delivered to it.": (
        "covered", "stacked-dialogs-close-from-the-top-two-deep-at-most",
        "the close request reaches the top overlay only"),
    "Requesting close yourself: watcher.requestClose() acts as if a close request had been sent by the user, to centralize close-handling code.": (
        "set aside", "", _API),
    "Asking for confirmation: ... This is useful in cases where, e.g., the modal contains a form with unsaved data.": (
        "covered", "the-users-work-is-never-harmed-by-an-act-or-by-inaction",
        "the confirmation's use"),
    "User activation grouping; using AbortSignals to destroy CloseWatchers.": (
        "set aside", "", _API),
    "Abuse analysis: a maximally-abusive page could make it take N + 2 back button presses to escape.": (
        "set aside", "", "the interface's security trade-off"),
    "Note that it never really makes sense to use the cancel event for a sidebar. ... picker UIs do not usually require confirmation on closing": (
        "set aside", "", "usage advice for the interface"),
    # --- Platform close requests -------------------------------------------------------------------
    "It allows the Android back button to close dialogs, subject to anti-abuse restrictions.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "quoted by the law"),
    "Existing Fullscreen implementations implement this using the Esc key on desktop, the back button on Android, and a floating software \"x\" button on iPadOS.": (
        "covered", "an-overlay-closes-on-the-devices-close-request", "fullscreen alike"),
    "Integration with popover=\"\" and <input>.": (
        "set aside", "", _API),
    # --- Alternatives considered ------------------------------------------------------------------
    "Integration with the history API: ... In our taxonomy, this new-URL lightbox is a navigation, and it would not be suitable to use the CloseWatcher API for it, because closing it needs to update the URL back to what it was originally": (
        "set aside", "", "an overlay with its own address is a page; the owed URL row holds the rule"),
    "Automatically translating all close requests to Esc; a single event; browser-mediated confirmation dialogs; no confirmation dialogs; no free close watcher; bundling with high-level APIs.": (
        "set aside", "", "alternatives to the interface, rejected"),
    # --- Security and privacy -----------------------------------------------------------------------
    "Security considerations: preventing abusive pages from hijacking the fallback behavior ... Privacy considerations: the only information it gives ... is that a close request has occurred.": (
        "set aside", "", "the interface's security and privacy"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 27


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_wicg_close_watcher",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the explainer's {SOURCE_COUNT} rules")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"WICG, Close Watchers explainer: {len(CENSUS)} classified\n")
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
