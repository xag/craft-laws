"""The laws. Content, not machinery — the kinds and rules are in package.py.

Every law here was earned by a defect that shipped. The `sighting` nodes are not colour: a law
that has never caught anything is a law nobody should trust, and the ones below are the reason
each of these is in the file at all.

The sightings are drawn from one run — `chores`, 2026-07-13, a French localisation that shipped
to production with 486 tests passing, 303/303 string keys covered in both directions, `node
--check` clean, and twelve flight-recorder tapes replaying bit-for-bit. Every check was green.
None of them reads.
"""

from __future__ import annotations

from quern import Node
from quern.provenance import Quantity


def _cited(source: str) -> Quantity:
    """A law somebody reputable has actually stated. Grounded: it may be acted on."""
    return Quantity(value=1, unit="law", provenance="cited", grounded=True, source=source)


def _uncited() -> Quantity:
    """A law nobody has been found to have stated. NOT deleted — carried, and visibly ungrounded,
    so the gate will not let it pass as settled. This is the ledger's treatment of a debt, and an
    uncited law is exactly that: something known-unsound, carried on purpose, with its cost
    stated rather than forgotten."""
    return Quantity(value=1, unit="law", provenance="asserted, uncited", grounded=False,
                    source="observed in practice; no authority found. Source it or drop it.")


def _law(law_id, name, authority, *, falsifier, triggers, citations=(), sightings=(), note=""):
    kids = []
    kids.append(Node(id=f"{law_id}--falsifier", kind="falsifier", payload={"claim": falsifier}))
    for i, t in enumerate(triggers):
        kids.append(Node(id=f"{law_id}--trigger-{i}", kind="trigger", payload={"when": t}))
    for i, (title, url, quote) in enumerate(citations):
        kids.append(Node(id=f"{law_id}--citation-{i}", kind="citation",
                         name=title, payload={"url": url, "quote": quote}))
    for i, (where, what) in enumerate(sightings):
        kids.append(Node(id=f"{law_id}--sighting-{i}", kind="sighting",
                         name=where, payload={"what": what}))
    return Node(id=law_id, kind="law", name=name,
                payload={"note": note} if note else {},
                params={"authority": authority}, children=kids)


NNG = "Nielsen Norman Group, 10 Usability Heuristics for User Interface Design"
NNG_URL = "https://www.nngroup.com/articles/ten-usability-heuristics/"

LAWS = [

    # --- language and vocabulary ------------------------------------------------
    _law(
        "no-system-vocabulary",
        "The interface names things as the user names them, never as the system is built",
        _cited("NN/g heuristic #2, Match Between the System and the Real World"),
        falsifier="A word on screen that only the people who built it use.",
        triggers=["any interface at all",
                  "the app coins domain concepts of its own (a wall, a ledger, a charter)"],
        citations=[(f"{NNG} — #2 Match Between the System and the Real World", NNG_URL,
                    "The design should speak the users' language. Use words, phrases, and "
                    "concepts familiar to the user, rather than internal jargon.")],
        sightings=[
            ("chores 2026-07-13, the charter screen",
             "A section headed « Les murs » — a literal rendering of the codebase's own "
             "metaphor, 'hard walls'. A French parent does not set a wall; they forbid "
             "something. Now « Interdictions »."),
            ("chores 2026-07-13, the add-a-chore sheet",
             "« Tout l'équilibre se compte en minutes » — *l'équilibre* is the app's name for "
             "its own fairness ledger. A person counts minutes."),
        ],
    ),

    _law(
        "says-what-happens",
        "A control's label describes the action it performs",
        _cited("GOV.UK Design System, Button"),
        falsifier="A button labelled with a noun, a category, or the name of the section it "
                  "sits in.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Button",
                    "https://design-system.service.gov.uk/components/button/",
                    "Write button text in sentence case, describing the action it performs… "
                    "You may need to include more or different words to better describe the "
                    "action.")],
        sightings=[
            ("chores 2026-07-13, the member sheet",
             "A section headed « Absence » whose submit button was also labelled « Absence ». "
             "In the English original: 'Away' over 'Away' — so the defect predated the "
             "translation by a year and nobody had ever read the screen."),
        ],
    ),

    # --- composition: the laws a string catalogue cannot hold ---------------------
    _law(
        "composed-prose",
        "A sentence is one translatable unit; never assemble one from separately-translated "
        "fragments",
        _cited("Mozilla, Localization best practices for developers"),
        falsifier="Any rendered line that is not a sentence a person would write. Judged AS "
                  "RENDERED — never as an entry in a string catalogue, where each fragment is "
                  "correct and the defect does not exist.",
        triggers=["the app is translated into any second language",
                  "any count, duration, date, currency or name is interpolated into a sentence"],
        citations=[("Mozilla — Localization best practices for developers",
                    "https://mozilla-l10n.github.io/documentation/localization/dev_best_practices.html",
                    "Splitting sentences into several keys often inadvertently presumes a "
                    "grammar, a sentence structure, and such composite strings are "
                    "unnecessarily difficult to translate… it is usually easier and quicker for "
                    "translators to handle these as fixed strings rather than composed "
                    "strings.")],
        sightings=[
            ("chores 2026-07-13, a proposal's countdown",
             "`proposal.closes` = « Encore {left} pour contester » composed with `left.min` = "
             "« encore {n} min », rendering « Encore encore 3 min pour contester. » Both "
             "strings correct in isolation. The defect existed only on the screen, and a "
             "catalogue of 304 strings cannot contain it."),
        ],
    ),

    _law(
        "plurals-and-agreement",
        "Counts resolve through the target language's own plural rules, never through n == 1",
        _cited("Unicode CLDR, Plural Rules"),
        falsifier="A hand-rolled `n === 1 ? singular : plural`; a form that is wrong at 0, 2, "
                  "11 or 21; a parenthesised gender ending shown to a reader (absent(e)).",
        triggers=["the app is translated into any second language",
                  "any count is shown to a person"],
        citations=[("Unicode CLDR — Plural Rules",
                    "https://cldr.unicode.org/index/cldr-spec/plural-rules",
                    "A common mistake is to think that 'one' is only for only the number 1. "
                    "Instead, 'one' is a category for any number that behaves like 1. — six "
                    "categories: zero, one, two, few, many, other.")],
        sightings=[
            ("chores 2026-07-13, the count on Today",
             "French treats 0 as singular (« 0 tâche »); English does not ('0 turns'). A "
             "binary check is wrong in the very first language you add. Routed through "
             "Intl.PluralRules."),
        ],
        note="In some languages the `one` category covers 1, 21 and 151 but not 11. The category "
             "is grammatical behaviour, not a number.",
    ),

    # --- localisation process ------------------------------------------------------
    _law(
        "glossary-first",
        "The domain nouns are settled BEFORE a word is translated, and settled by someone who "
        "speaks the target language — not by whoever commissioned the work, and not by the "
        "translator",
        _cited("Lionbridge; Creative Words — terminology management"),
        falsifier="A glossary authored by the person requesting the translation. A domain noun "
                  "that changes after translation has begun.",
        triggers=["the app is translated into any second language"],
        citations=[
            ("Lionbridge — How to create a translation style guide and terminology glossary",
             "https://www.lionbridge.com/blog/translation-localization/how-to-create-a-translation-style-guide-and-terminology-glossary/",
             "Build a validated, client-approved glossary before a single word is translated."),
            ("Creative Words — Terminology management in localization: why we never start with "
             "translation",
             "https://www.creative-words.com/en/terminology-management-in-localization-why-we-never-start-with-translation/",
             "Terminology errors discovered late in the localization cycle require cascading "
             "fixes across all documents, all languages, and all versions."),
        ],
        sightings=[
            ("chores 2026-07-13, every screen",
             "The commissioning agent invented « maisonnée » for *household* (literary; nobody "
             "says it) and counted chores in « tours » (« il reste 3 tours » — a board game), "
             "wrote both into the translator's brief as BINDING, and every tab, count and "
             "heading inherited them faithfully. The translation was executed perfectly. The "
             "words were wrong. A native speaker settled it in one question: équipe, and turns "
             "counted in tâches."),
        ],
        note="The failure mode is not a bad translator. It is a glossary nobody validated — and "
             "the person able to validate it is usually already in the room.",
    ),

    _law(
        "text-expansion",
        "Layout survives the target language's length — and SHORT strings are the dangerous "
        "ones",
        _cited("W3C i18n, Text size in translation, citing IBM"),
        falsifier="Clipped or wrapped text in the target language at the narrowest real "
                  "viewport.",
        triggers=["the app is translated into any second language",
                  "the app is used on a phone"],
        citations=[("W3C — Text size in translation (citing IBM's globalisation guidelines)",
                    "https://www.w3.org/International/articles/article-text-size",
                    "Up to 10 characters: 200–300% expansion. 11–20: 180–200%. Over 70: 130%. "
                    "The smaller the source message, the higher the likely translation "
                    "length.")],
        sightings=[
            ("chores 2026-07-13, the tab bar",
             "'Today' (5) → « Aujourd'hui » (11). 'Household' → « Équipe ». The tab bar and the "
             "button row are the FIRST things to check, not the last — which is the opposite of "
             "the intuition that long paragraphs are the risk."),
        ],
    ),

    _law(
        "no-calque",
        "A metaphor is re-chosen in the target language, not carried across it",
        _uncited(),
        falsifier="A vivid source-language image that lands as jargon in the target language.",
        triggers=["the app is translated into any second language",
                  "the app coins domain concepts of its own"],
        sightings=[
            ("chores 2026-07-13, the households sheet",
             "« Ses propres habitants » — a *team* has no inhabitants. The word survived a "
             "glossary change from 'house' to 'team' because the sentences AROUND the changed "
             "word were never re-read."),
        ],
        note="Probably an instance of no-system-vocabulary rather than a law in its own right: a "
             "calqued metaphor is jargon in the target language. Kept separate because it is "
             "what actually goes wrong. Fold it in if it never earns a verdict of its own.",
    ),

    _law(
        "untranslatable-tone",
        "A line whose only content is TONE may be dropped in a language with no equivalent "
        "register — not rendered",
        _uncited(),
        falsifier="A translated line that carries no information.",
        triggers=["the app is translated into any second language",
                  "the app's voice does work of its own (dry, warm, terse)"],
        sightings=[
            ("chores 2026-07-13, the empty board",
             "'Nothing today. / That is the whole message.' — a dry joke about the app's own "
             "terseness. French has no such joke. Every attempt to carry it across produced a "
             "line that said nothing, and one of them — « Il n'y a rien à ajouter. » — sat "
             "forty pixels above a button marked AJOUTER. The fix was to let French decline the "
             "second line entirely."),
        ],
        note="This is the software-copy edge of transcreation, which is established practice in "
             "marketing localisation. I have not found it stated as a rule for UI copy. Source "
             "it or drop it.",
    ),

    # --- surfaces --------------------------------------------------------------------
    _law(
        "rare-action-folds-away",
        "Frequency decides prominence; rare and advanced actions are deferred to a second layer",
        _cited("NN/g, Progressive Disclosure; heuristic #8"),
        falsifier="The rarest action on a surface occupying the most space.",
        triggers=["a rare action shares a surface with frequent ones "
                  "(create vs. switch; delete vs. edit)"],
        citations=[
            ("NN/g — Progressive Disclosure",
             "https://www.nngroup.com/articles/progressive-disclosure/",
             "Initially, show users only a few of the most important options. Offer a larger "
             "set of specialized options upon request… the very fact that something appears on "
             "the initial display tells users that it's important."),
            (f"{NNG} — #8 Aesthetic and Minimalist Design", NNG_URL,
             "Interfaces should not contain information that is irrelevant or rarely needed."),
        ],
        sightings=[
            ("chores 2026-07-13, the households sheet",
             "Opened to SWITCH team; its largest element was a fully-expanded create-a-new-team "
             "form — an action performed about once a year. Folded behind a disclosure."),
        ],
    ),

    _law(
        "one-surface-one-job",
        "A surface serves one intent; a second intent is a second surface, or a disclosure",
        _cited("NN/g heuristic #8; NN/g Progressive Disclosure"),
        falsifier="A person opening a surface for job A and being met by job B's form.",
        triggers=["a surface accumulates more than one intent "
                  "(rename + configure + create)"],
        citations=[(f"{NNG} — #8 Aesthetic and Minimalist Design", NNG_URL,
                    "Interfaces should not contain information that is irrelevant or rarely "
                    "needed. Every extra unit of information in an interface competes with the "
                    "relevant units of information.")],
        sightings=[
            ("chores 2026-07-13, the households sheet",
             "Three unrelated jobs stacked flat — rename this team, set its language, create "
             "another — plus a bare text box holding the team's name with nothing saying it was "
             "a name."),
        ],
        note="Weaker than the others as a standalone law: it derives from #8 and progressive "
             "disclosure, and so far it has never produced a verdict that rare-action-folds-away "
             "did not. Merge it if that holds.",
    ),

    _law(
        "a-way-back",
        "Every action a person can take by mistake has a marked exit",
        _cited("NN/g heuristic #3, User Control and Freedom"),
        falsifier="A destructive or contested action with no undo, no cancel, and no way to "
                  "object.",
        triggers=["an action is destructive, irreversible, or binding on somebody else"],
        citations=[(f"{NNG} — #3 User Control and Freedom", NNG_URL,
                    "Users often perform actions by mistake. They need a clearly marked "
                    "'emergency exit' to leave the unwanted action without having to go through "
                    "an extended process.")],
    ),

    _law(
        "empty-state-never-contradicts",
        "No empty state asserts something the surrounding controls deny",
        _uncited(),
        falsifier="The zero state and a visible control disagreeing with each other.",
        triggers=["any surface has a zero state (a new user; a day with nothing due)"],
        sightings=[
            ("chores 2026-07-13, the empty board — the worst defect of the run",
             "« Il n'y a rien à ajouter. » rendered forty pixels above a button marked "
             "AJOUTER. As a sentence it is perfectly good French. It is absurd only in place, "
             "and no string table contains position."),
        ],
        note="A specific case of NN/g #4 (Consistency and Standards — 'users should not have to "
             "wonder whether different words, situations, or actions mean the same thing'), but "
             "I have not found it stated for empty states. It stays, uncited and red, because it "
             "caught the worst defect of the run — which is the only argument for a law that "
             "matters.",
    ),
]

# What the laws are allowed to travel through. Ungrounded authority — an uncited law — will not
# pass, because `nothing-unsound-passes-a-gate` (shipped by `ledger`) counts it.
GATE = Node(
    id="publish",
    kind="gate",
    name="What may be relied on as a law",
    payload={
        "note": "Red, and correctly so: three of the twelve laws cite nobody. They are carried "
                "on purpose and they are visible — which is the whole difference between this "
                "and the markdown file it replaced, where the same three sat in a sentence that "
                "was true and could not fire. Discharge by finding the source, or by deleting "
                "the law. Never by editing this file.",
    },
    links={"admits": [law.id for law in LAWS]},
)
