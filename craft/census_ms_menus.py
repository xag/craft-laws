"""A census: Microsoft, Windows 7 user experience guidelines, Menus (Design basics), whole.

It roots a-stable-menu-disables-what-does-not-apply, a-contextual-menu-lists-only-what-applies and
a-shortcut-or-context-menu-is-never-the-only-way-to-a-command, and a source is adopted entire or
not at all (the source-the-rule protocol). The source is
https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus, read on 2026-11-20. Microsoft
labels it "created for Windows 7 and has not been updated for newer versions of Windows. Much of
the guidance still applies in principle, but the presentation and examples do not reflect our
current design guidance."

The census unit is each line of the page's Guidelines, from General to Documentation, that states
a rule, in the page's own words. The page's descriptive text before the Guidelines, each
"In this example" caption, the lists of example labels and keys, and the bullets under a "consider"
or "make" line (read with the line above them, which carries their rule) are not units. Where a
line gathers two sentences, the unit is the whole line. A rule that applies to the Windows menu bar
or its keys alone is routed owed all the same: it is decidable from data a program can record,
though this repo holds no law on it yet.

What prompted it: a complaint, 2026-11-20, that an interface showed a command that does nothing in
the present state (a control to spread the parts of a multi-part object, offered in a 3D view of
a single part). The page states when such a command is shown unavailable and when it is removed.

    python -m craft.census_ms_menus
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'All menu patterns except menu bars need a drop-down arrow to indicate the presence of a pull-down menu. The presence of menus goes without saying in a menu bar, but not in the other patterns.': (
        'owed', '', 'decidable from the pattern: a drop-down arrow on every menu pattern but the menu bar'),
    "Don't change menu item names dynamically. Doing so is confusing and unexpected. For example, don't change a Portrait mode option to Landscape mode upon selection. For modes, use bullets and checkmarks instead.": (
        'set aside', '', "contradicts Apple's changeable label (Show Map to Hide Map); left to the owner"),
    'Exception: You can change menu item names that are based on object names dynamically. For example, lists of recently used files or window names can be dynamic.': (
        'set aside', '', 'the exception to the rule above it'),
    'Consider eliminating menu bars with three or fewer menu categories. If there are only a few commands, prefer lighter alternatives such as toolbar menus, or more direct alternatives such as command buttons and links.': (
        'set aside', '', 'a consideration; a reading'),
    "Don't have more than 10 menu categories. Too many menu categories is overwhelming and makes the menu bar difficult to use.": (
        'owed', '', 'decidable by counting the categories'),
    'Consider hiding the menu bar if the toolbar or direct commands provide almost all of the commands needed by most users. Allow users to show or hide with a Menu bar check mark option in a toolbar menu.': (
        'set aside', '', 'a consideration; a reading'),
    'Hide the menu bar by default if your toolbar design makes having a menu bar redundant.': (
        'set aside', '', 'a reading of whether the toolbar makes the menu bar redundant'),
    'Hide the menu bar instead of removing it completely, because menu bars are more accessible for keyboard users.': (
        'owed', '', 'decidable: a menu bar hidden and still reachable by keyboard'),
    'To restore the menu bar, provide a Menu bar checkmark option in the View (for primary toolbars) or Tools (for secondary toolbars) menu category. For more information, see Standard menu and split buttons.': (
        'owed', '', 'decidable: a menu bar checkmark option in View or Tools'),
    'Choose single word names for menu categories. Using multiple words makes the separation between categories confusing.': (
        'owed', '', 'decidable: a category name is one word'),
    'For programs that create or view documents, use the standard menu categories such as File, Edit, View, Tools, and Help. Doing so makes common menu items predictable and easier to find.': (
        'owed', '', 'decidable for a document program: the standard categories present'),
    "For other types of programs, consider organizing your commands and options into more useful, natural categories based on your program's purpose and the way users think about their tasks and goals. Don't feel obligated to use the standard menu organization if it isn't suitable for your program.": (
        'set aside', '', 'a consideration; a reading'),
    'If you choose to use non-standard menu categories, you must choose good category names. For more information, see the Labels section.': (
        'set aside', '', 'a reading of the names'),
    'Prefer task-oriented menu categories over generic categories. Task-oriented categories make menu items easier to find.': (
        'set aside', '', 'a reading of the categories'),
    'Avoid menu categories with only one or two menu items. If sensible, consolidate with other menu categories, perhaps using a submenu.': (
        'owed', '', 'decidable by counting the items in a category'),
    'Consider putting the same menu item in multiple categories only if:': (
        'set aside', '', 'a consideration with three conditions; a reading'),
    "Don't put different menu items that use the same name in multiple categories. For example, don't have different Options menu items in multiple categories.": (
        'owed', '', 'decidable: two different items under one name in several categories'),
    'Exception: The tab menu pattern may have different Options and Help menu items in each tab menu.': (
        'owed', '', 'the exception to the rule above it'),
    'Organize the menu items into groups of seven or fewer strongly related items. For this, submenus count as a single menu item in the parent menu.': (
        'owed', '', 'decidable by counting the items in a group'),
    "Don't put more than 25 items within a single level of a menu (not counting submenus).": (
        'owed', '', 'decidable by counting the items in a level'),
    'Put separators between the groups within a menu. A separator is a single line that spans the width of the menu.': (
        'owed', '', 'decidable: a separator between groups; the page states the same line again for context menus'),
    'Within a menu, put the groups in their logical order. If there is no logical order, place the most commonly used groups first.': (
        'set aside', '', 'a reading of logical order'),
    'Within a group, put the items in their logical order. If there is no logical order, place the most commonly used items first. Put numeric items (such as zoom percentages) in numeric order.': (
        'set aside', '', 'a reading of logical order'),
    'Avoid using submenus unnecessarily. Submenus require more physical effort to use and generally make the menu items more difficult to locate.': (
        'set aside', '', 'a reading of necessity'),
    "Don't put frequently used menu items in a submenu. Doing so would make using these commands inefficient. However, you can put frequently used commands in a submenu if they are normally accessed more directly, such as with a toolbar.": (
        'owed', '', 'decidable once item use is recorded'),
    'Consider using a submenu if:': (
        'set aside', '', 'a consideration with conditions; a reading'),
    'Use at most three levels of menus. That is, you can have a primary menu and at most two levels of submenus. Two levels of submenus should be rare.': (
        'owed', '', 'decidable by counting the levels'),
    "Disable menu items that don't apply to the current context, instead of removing them. Doing so makes menu bar contents stable and easier to find. Exceptions:": (
        'covered', 'a-stable-menu-disables-what-does-not-apply', 'the law: a stable menu disables what does not apply; its exception for contextual categories is the next law'),
    "For contextual menu categories, remove rather than disable context menu items that don't apply to the current context. A menu category is contextual when it is displayed only for specific modes, such as when a certain object type is selected. For details, see the remove vs. disable guidelines for context menus.": (
        'covered', 'a-contextual-menu-lists-only-what-applies', 'the law'),
    'If determining when a menu item should be disabled causes noticeable performance problems, leave the menu item active and if necessary have its selection result in an error message.': (
        'covered', 'a-stable-menu-disables-what-does-not-apply', 'the performance exception, carried by the law'),
    "Each tab menu may have context specific Options and Help menu items. This is in contrast to all other menu patterns. Each tab is used for a dedicated set of tasks, so any redundancy across tab menus isn't confusing.": (
        'set aside', '', 'states what a tab menu may hold; a permission'),
    'Use context menus only for contextual commands and options. The menu items should apply only to the selected (or clicked upon) object or window region, not the entire program.': (
        'set aside', '', 'a reading of whether an item is contextual'),
    "Don't make commands only available through context menus. Like shortcut keys, context menus are alternative means of performing commands and choosing options. For example, a Properties command is also available through the menu bar or the Alt+Enter access key.": (
        'covered', 'a-shortcut-or-context-menu-is-never-the-only-way-to-a-command', 'the law, the context menu half'),
    'Provide context menus for all objects and window regions that benefit from a small set of contextual commands and options. Many users right-click regularly and expect to find context menus anywhere.': (
        'set aside', '', 'a reading of what benefits from a context menu'),
    'Consider using a menu drop-down arrow button for context menus targeted at all users. Normally context menus are suitable for commands and options targeted at advanced users. However, you can use a menu drop-down button in cases where context menus are the best menu choice and you need to target all users.': (
        'set aside', '', 'a consideration; a reading'),
    'Organize the menu items into groups of seven or fewer strongly related items.': (
        'owed', '', 'decidable by counting the items in a group'),
    'Avoid using submenus to keep context menus simple, direct, and efficient.': (
        'owed', '', 'decidable: a submenu in a context menu'),
    "Don't put more than 15 items within a context menu.": (
        'owed', '', 'decidable by counting the items'),
    'Present menu items using the following order:': (
        'set aside', '', 'a reading of which commands are primary, secondary, transfer or object commands'),
    'Display the default command using bold. When practical, also make it the first menu item. The default command is invoked when users double-click or select an object and press Enter.': (
        'owed', '', 'decidable: the default command in bold and first'),
    "Remove rather than disable context menu items that don't apply to the current context. Doing so makes context menus contextual and efficient.": (
        'covered', 'a-contextual-menu-lists-only-what-applies', 'the law'),
    "Exception: Disable menu items that don't apply if there is a reasonable expectation for them to be available:": (
        'covered', 'a-contextual-menu-lists-only-what-applies', 'the exception, carried by the law'),
    'Always have the relevant standard context menu commands, such as Cut, Copy, Paste, Delete, and Rename.': (
        'covered', 'a-contextual-menu-lists-only-what-applies', 'the first case of the exception'),
    "Always have the commands that complete related sets. For example, if there is a Back, there should also be a Forward. If there's a Cut, always have a Copy and Paste.": (
        'covered', 'a-contextual-menu-lists-only-what-applies', 'the second case of the exception'),
    'Menu items that are options may use bullets and checkmarks. Commands may not.': (
        'owed', '', 'decidable: bullets and checkmarks only on options'),
    'Use a bullet to choose one option from a small set of mutually exclusive choices. There should always be at least two bullets in a group. For more information, see Radio buttons.': (
        'owed', '', 'decidable: at least two bullets in a group'),
    "Use a checkmark to toggle an independent setting on or off. If the selected and cleared states aren't clear and unambiguous opposites, use a set of bullets instead. For more information, see Check boxes.": (
        'owed', '', 'decidable: a checkmark on an independent setting'),
    'For a mixed checkmark state, display a menu item without a checkmark. The mixed state is used for multiple selection to indicate that the option is set for some, but not all, objects, so each individual object has either the selected or cleared state. The mixed state is not used as a third state for an individual item.': (
        'owed', '', 'decidable: the mixed state shown without a checkmark'),
    'Put separators between the related sets of checkmarks or bullets. A separator is a single line that spans the width of the menu.': (
        'owed', '', 'decidable: separators between related sets'),
    'Consider providing menu item icons for:': (
        'set aside', '', 'a consideration; a reading'),
    "If you use icons, don't feel obligated to provide them for all menu items. Cryptic icons aren't helpful, create visual clutter, and prevent users from focusing on the important menu items.": (
        'set aside', '', 'a reading of which icons are cryptic'),
    'Make sure menu icons conform to the Aero-style icon guidelines.': (
        'set aside', '', 'a reference to another guide'),
    'Assign access keys to all menu items. No exceptions.': (
        'owed', '', 'decidable: every menu item has an access key'),
    "Whenever possible, assign access keys for commonly used commands according to the Standard Access Key Assignments. While consistent access key assignments aren't always possible, they are certainly preferred - especially for frequently used commands.": (
        'owed', '', 'decidable against the standard access key assignments'),
    'For dynamic menu items (such as recently used files), assign access keys numerically.': (
        'owed', '', 'decidable: dynamic items take numeric access keys'),
    'Assign unique access keys within a menu level. You can reuse access keys across different menu levels.': (
        'owed', '', 'decidable: access keys unique within a menu level'),
    'Make access keys easy to find:': (
        'set aside', '', 'the heading of the next five guidelines'),
    'For the most frequently used menu items, choose characters at the beginning of the first or second word of the label, preferably the first character.': (
        'set aside', '', 'a reading of the label'),
    'For less frequently used menu items, choose letters that are a distinctive consonant or a vowel in the label.': (
        'set aside', '', 'a reading of the label'),
    'Prefer characters with wide widths, such as w, m, and capital letters.': (
        'set aside', '', 'a preference; a reading'),
    'Prefer a distinctive consonant or a vowel, such as "x" in "Exit."': (
        'set aside', '', 'a preference; a reading'),
    'Avoid using characters that make the underline difficult to see, such as (from most problematic to least problematic):': (
        'set aside', '', 'a reading of which glyphs hide an underline'),
    "Assign shortcut keys to the most frequently used menu items. Infrequently used menu items don't need shortcut keys because users can use access keys instead.": (
        'owed', '', 'decidable once item use is recorded'),
    "Don't make a shortcut key the only way to perform a task. Users should also be able to use the mouse or the keyboard with Tab, arrow, and access keys.": (
        'covered', 'a-shortcut-or-context-menu-is-never-the-only-way-to-a-command', 'the law, the shortcut key half'),
    'For well-known shortcut keys, use the standard assignments.': (
        'owed', '', 'decidable against the standard assignments'),
    "Don't assign different meanings to well-known shortcut keys. Because they are memorized, inconsistent meanings for well-known shortcuts are frustrating and error prone. See Windows Keyboard Shortcut Keys for the well-know shortcut keys used by Windows programs.": (
        'owed', '', 'decidable against the standard assignments'),
    "Don't try to assign system-wide program shortcut keys. Your program's shortcut keys will have effect only when your program has input focus.": (
        'owed', '', 'decidable: no system-wide shortcut registered'),
    'Document all shortcut keys. Doing so helps users learn the shortcut key assignments.': (
        'owed', '', 'decidable: every shortcut key documented'),
    "Exception: Don't display shortcut key assignments within context menus. Context menus don't display the shortcut key assignments because they are optimized for efficiency.": (
        'owed', '', 'decidable: no shortcut shown in a context menu'),
    "Choose shortcut keys that don't have standard assignments. Never reassign standard shortcut keys.": (
        'owed', '', 'decidable against the standard assignments'),
    "Use non-standard key assignments consistently throughout your program. Don't assign different meanings in different windows.": (
        'owed', '', 'decidable: one meaning per key across windows'),
    'If possible, choose mnemonic key assignments, especially for frequently used commands.': (
        'set aside', '', 'a preference; a reading'),
    'Use function keys for commands that have a small-scale effect, such as commands that apply to the selected object. For example, F2 renames the selected item.': (
        'set aside', '', 'a reading of the scale of a command'),
    'Use Ctrl key combinations for commands that have a large-scale effect, such as commands that apply to an entire document. For example, Ctrl+S saves the current document.': (
        'set aside', '', 'a reading of the scale of a command'),
    'Use Shift key combinations for commands that extend or complement the actions of the standard shortcut key. For example, the Alt+Tab shortcut key cycles through open primary windows, whereas Alt+Shift+Tab cycles in the reverse order. Similarly, F1 displays Help, whereas Shift+F1 display context-sensitive Help.': (
        'set aside', '', 'a reading of what extends a standard key'),
    "Don't use the following characters for shortcut keys: @ $ {} [] \\ ~ | ^ ' < >. These characters require different key combinations across languages or are locale specific.": (
        'owed', '', 'decidable: none of the listed characters used as a shortcut key'),
    "Don't use Ctrl+Alt combinations, because Windows interprets this combination in some language versions as an AltGR key, which generates alphanumeric characters.": (
        'owed', '', 'decidable: no Ctrl+Alt combination'),
    "If your program assigns many shortcut keys, provide the ability to customize the assignments. Doing so allows users to reassign conflicting shortcut keys and migrate from other products. Most programs don't assign enough shortcut keys to need this feature.": (
        'owed', '', 'decidable: shortcuts customizable when many are assigned'),
    'Use the standard menu organization for programs that create or view documents. The standard menu organization makes common menu items predictable and easier to find.': (
        'owed', '', 'decidable for a document program: the standard organization present'),
    "For other types of programs, use the standard menu organization only when it makes sense to. Consider organizing your commands and options into more useful, natural categories based on your program's purpose and the way users think about their tasks and goals.": (
        'set aside', '', 'a reading of whether the standard organization suits'),
    'The standard menu bar structure is as follows. This list shows the menu category and item labels, their order with separators, their access and shortcut keys, and their ellipses.': (
        'set aside', '', 'the standard menu bar listed: a reference list'),
    'The standard toolbar menu buttons are as follows. This list shows the menu category and item labels, their order with separators, their shortcut keys, and their ellipses.': (
        'set aside', '', 'the standard toolbar menu buttons listed: a reference list'),
    "The standard context menu contents are as follows. This list shows the menu item labels, their order with separators, their access keys, and their ellipses. Context menus don't show shortcut keys.": (
        'set aside', '', 'the standard context menu listed: a reference list'),
    'While menu commands are used for immediate actions, more information might be needed to perform the action. Indicate a command that needs additional information (including a confirmation) by adding an ellipsis at the end of the label.': (
        'covered', 'ellipsis-promises-more-input', 'the law: an ellipsis exactly when more information is needed'),
    'Proper use of ellipses is important to indicate that users can make further choices before performing the action, or even cancel the action entirely. The visual cue offered by an ellipsis allows users to explore your software without fear.': (
        'covered', 'ellipsis-promises-more-input', 'the law'),
    "This doesn't mean you should use an ellipsis whenever an action displays another window only when additional information is required to perform the action. For example, the commands About, Advanced, Help, Options, Properties, and Settings must display another window when clicked, but don't require additional information from the user. Therefore they don't need ellipses.": (
        'covered', 'ellipsis-promises-more-input', 'the law: no ellipsis where a window opens with nothing to ask'),
    "In case of ambiguity (for example, the command label lacks a verb), decide based on the most likely user action. If simply viewing the window is a common action, don't use an ellipsis.": (
        'set aside', '', 'a reading of the most likely user action'),
    "When determining if a menu command needs an ellipsis, don't use the need to elevate privileges as a factor.": (
        'owed', '', 'decidable: the need to elevate is not a factor, the shield marks it'),
    'Use sentence-style capitalization.': (
        'covered', 'sentence-labels-take-sentence-case', 'the law'),
    'Exception: For legacy applications, you may use title-style capitalization if necessary to avoid mixing capitalization styles.': (
        'owed', '', 'the exception to the rule above it'),
    'Use menu category names that are single word verbs or nouns. A multiple-word label might be confused for two one-word labels.': (
        'owed', '', 'decidable: a category name is one word, a verb or a noun'),
    "Prefer verb-based menu names. However, omit the verb if it is Create, Show, View, or Manage. For example, the following menu categories don't have verbs:": (
        'owed', '', 'decidable: the verb omitted only for Create, Show, View, Manage'),
    "For non-standard category names, use a single, specific word that clearly and accurately describes the menu contents. While the names don't have to be so general that they describe everything in the menu, they should be predictable enough so that users aren't surprised by what they find in the menu.": (
        'set aside', '', 'a reading of the name'),
    'Use menu item names that start with a verb, noun, or noun phrase.': (
        'owed', '', 'decidable: a name starts with a verb, a noun or a noun phrase'),
    'Prefer verb-based menu names. However, omit the verb if:': (
        'owed', '', 'decidable: the verb omitted only for Create, Show, View, Manage, or when it repeats the category'),
    'The verb is the same as the menu category name to avoid repetition. For example, in the Insert menu category, use Text, Table, and Picture instead of Insert text, Insert table, and Insert picture.': (
        'owed', '', 'the second case of the omission'),
    'Use specific verbs. Avoid generic, unhelpful verbs, such as Change and Manage.': (
        'owed', '', 'decidable against a list of generic verbs'),
    'Use singular nouns for commands that apply to a single object, otherwise use plural nouns.': (
        'owed', '', 'decidable: singular for one object, plural otherwise'),
    'Use modifiers as necessary to distinguish between similar commands. Examples: Insert row above, Insert row below.': (
        'set aside', '', 'a reading of similarity'),
    'For pairs of complementary commands, choose clearly complementary names. Examples: Add, Remove; Show, Hide; Insert, Delete.': (
        'set aside', '', 'a reading of complementary names'),
    'Choose menu item names based on user goals and tasks, not on technology.': (
        'set aside', '', 'a reading of goals against technology'),
    'Use the following menu item names for the stated purpose:': (
        'owed', '', 'decidable: the stated names used for the stated purposes'),
    'Menu items that display submenus never have an ellipsis on their label. The submenu arrow indicates that another selection is required.': (
        'owed', '', 'decidable: no ellipsis on an item that opens a submenu'),
    "In commands that show or hide menus, refer to menu bars. Don't refer to them as classic menus.": (
        'owed', '', 'decidable over documentation: menu bars, not classic menus'),
    "Refer to menus by their labels. Use the exact label text, including its capitalization, but don't include the access key underscore or ellipsis.": (
        'owed', '', 'decidable over documentation: the exact label text'),
    'To refer to menu categories, use "On the <category name> menu." If the location of a menu item is clear from the context, you don\'t need to mention the menu category.': (
        'owed', '', 'decidable over documentation: the form On the <category> menu'),
    "To describe user interaction of menu items, use click, without the word menu or command. Don't use choose, select, or pick. Don't refer to a menu item as a menu item except in technical documentation.": (
        'owed', '', 'decidable over documentation: click, not choose, select or pick'),
    "To describe removing a check mark from a menu option, use click to remove the check mark. Don't use clear.": (
        'owed', '', 'decidable over documentation: click to remove the check mark'),
    'Refer to context menus as context menus, not shortcut menus.': (
        'owed', '', 'decidable over documentation: context menu, not shortcut menu'),
    "Don't use cascading, pull-down, drop-down, or pop-up to describe menus, except in programming documentation.": (
        'owed', '', 'decidable over documentation: none of the four terms'),
    'Refer to unavailable menu items as unavailable, not as dimmed, disabled, or grayed. Use disabled in programming documentation.': (
        'owed', '', 'decidable over documentation: unavailable, not dimmed, disabled or grayed'),
    'When possible, format the labels using bold text. Otherwise, put the labels in quotation marks only if required to prevent confusion.': (
        'owed', '', 'decidable over documentation: labels in bold'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 112


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_ms_menus",
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
    print(f"Microsoft, Windows 7 user experience guidelines, Menus: {len(CENSUS)} classified\n")
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
