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
            ("chores ruling cards, 2026-08-18",
             "The judgment surface itself: ungrouped conviction cards served law ids, "
             "element ids, click paths and solver margins as the sentence to judge — "
             "«targets-are-thumb-sized: '-8.6px margin at 15px' — 'header-all' renders "
             "26.8x15.4px…» — on the one screen whose whole job is a person deciding. "
             "The founder: 'humans don't read code to decide'. The drawing had named "
             "every element in the owner's words all along (the All toggle beside the "
             "date); the cards had never consulted it. A tool built to enforce laws is "
             "not excused from them, and is where their breach costs most."),
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
             "translation, and nobody had ever read the screen."),
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
        
            ("spec-studio ruling cards, 2026-08-18",
             "a ruling card is itself a surface with one job — one decision — and one "
             "card gathered the chore form's rhythm line with the Today tab's swap "
             "line, because its grouping matched a law with an empty surface prefix. "
             "The founder: 'the two items are not related'. The law that was almost "
             "minted for this ('one-card-one-screen') was this law, applied to a "
             "card."),
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

    _law(
        "the-title-names-the-place",
        "The window or tab title says where the person is, not only what the app is "
        "called",
        _cited("W3C, WCAG 2.2, SC 2.4.2 Page Titled, Level A"),
        falsifier="Two different places in the app whose window titles read the same — "
                  "or a title that is blank, or only ever the product's name — while "
                  "the screens beneath them differ. Observable per walked surface by "
                  "reading document.title beside the tape's surface name.",
        triggers=["the app runs in a browser tab or names its screens in a window "
                  "title"],
        citations=[("W3C — WCAG 2.2, SC 2.4.2 Page Titled",
                    "https://www.w3.org/TR/WCAG22/#page-titled",
                    "Web pages have titles that describe topic or purpose."),
                   ("RGAA 4 — Critère 8.5 / 8.6",
                    "https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/",
                    "Chaque page web a-t-elle un titre de page ? … Pour chaque page "
                    "web ayant un titre de page, ce titre est-il pertinent ?")],
        note="The RGAA citation is deliberate beyond redundancy: the package's "
             "non-anglophone root, phrased as a numbered test procedure rather "
             "than a rule — the falsifiability this catalogue selects for.",
    ),

    # --- laws the formalism was NOT designed around ------------------------------
    # The three above the fold entered when their defects did, and the interface
    # vocabulary grew up beside them — so a skeptic should ask whether the machinery
    # only fits the laws it was shaped by. These three arrived later, from standing
    # authorities, chosen for what they demand of the model rather than for any
    # defect already caught: one reads the ACTION graph against the drawing, one
    # reads the drawing against itself across surfaces, one reads measured geometry.
    # No sightings yet, and that is the honest state of a law on arrival.

    _law(
        "counts-are-computed",
        "Documentation never carries a number a tool can compute — prose states the "
        "command, the tool states the count",
        _uncited(),
        falsifier="A number in documentation or docstrings describing an enumerable "
                  "the repo can compute (how many laws, surfaces, rules, entries) — "
                  "observable by comparing the prose against the computing command's "
                  "output.",
        triggers=["any interface at all"],
        sightings=[
            ("craft-laws itself, 2026-08-16 — three times in one day",
             "The README said 'twelve laws' while the file held 57; the census "
             "document's hand tally said 24 while the computed status said 25; "
             "chores' probe docstring described a two-surface drawing at eleven "
             "surfaces. Each was written true and went silently false — the exact "
             "failure mode this package's founding argument names, reproduced in "
             "its own prose. The fixes all had one shape: the prose keeps the "
             "command, the tool keeps the number."),
        ],
        note="Uncited and red, in this repo's own tradition: observed in practice, "
             "no authority found stating it for documentation. It is the "
             "documentation instance of a wider truth this estate keeps re-learning "
             "— a claim that cannot fire goes stale the moment it is written.",
    ),

    _law(
        "docs-do-not-date-themselves",
        "Documentation describes what the product is, never how it just changed — no "
        "'now', no 'new', no 'currently'",
        _cited("Google developer documentation style guide, Timeless documentation"),
        falsifier="A time-anchoring word — currently, now, new, soon, latest, 'at the "
                  "time of writing' — in documentation describing a capability. Each "
                  "is a sentence pre-written to go stale; observable by a wordlist "
                  "over the docs, no interpretation needed.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("Google developer documentation style guide — Timeless "
                    "documentation",
                    "https://developers.google.com/style/timeless-documentation",
                    "Timeless documentation is documentation that avoids words and "
                    "phrases that anchor the documentation to a point in time or "
                    "assume knowledge of prior or future products and features… "
                    "Words like now, new, and currently can render such "
                    "documentation inaccurate, outdated, or unmeaningful.")],
        note="counts-are-computed's cited sibling: the same staleness mechanism, "
             "caught at the word level where a wordlist can decide it, instead of "
             "the number level where only a computation can. Release notes and "
             "blog posts are exempt by the source's own carve-out — they are "
             "time-stamped content, and 'new' is true there in a way it cannot "
             "stay true in a reference.",
    ),

    _law(
        "terms-defined-before-use",
        "A term of art is defined at or before its first use — a reader never meets "
        "a word whose definition is still ahead of them",
        _cited("Google developer documentation style guide, Jargon"),
        falsifier="A document's own coinage — a 'twin', a 'walk', a 'lane' — used "
                  "before the sentence that says what it is. Observable from "
                  "reading order alone, by a reader: no document here declares its "
                  "own coinages, so nothing can compute which words are terms.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("Google developer documentation style guide — Jargon",
                    "https://developers.google.com/style/jargon",
                    "Are you using the term throughout your document? If so, "
                    "briefly describe the term in parentheses on first reference, "
                    "or link to a trusted definition.")],
        sightings=[
            ("craft-laws itself, 2026-08-17 — its own README",
             "The front page used 'drawing', 'twin', 'critic' and 'witness' "
             "before any sentence defined them — the framework's own coinages, "
             "handed to a stranger undefined. Caught by the framework's owner "
             "reading as that stranger; minted through the loop the same day."),
        ],
    ),

    _law(
        "a-readme-answers-what-why-how",
        "A repository front page answers, in this order and before anything else: "
        "what the project does, why it is useful, how to get started",
        _cited("GitHub Docs, About READMEs"),
        falsifier="A README a stranger can read to the bottom of without learning "
                  "what the project is, why they would want it, or what command "
                  "starts it — or one that opens on house doctrine, internal "
                  "history, or its own cleverness before those three.",
        triggers=["the project has a repository front page (a README)"],
        citations=[("GitHub Docs — About READMEs",
                    "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes",
                    "A README is often the first item a visitor will see when "
                    "visiting your repository. README files typically include "
                    "information on: What the project does. Why the project is "
                    "useful. How users can get started with the project.")],
        sightings=[
            ("craft-laws itself, 2026-08-17 — its own README",
             "The front page of the whole framework opened on its cleverest "
             "in-joke ('this repo does not pass its own check — on purpose'), "
             "put the definition third, and kept the founding story — the "
             "reason a reader would care — in the last section. Called an "
             "insult to readers by the person the page exists to serve."),
        ],
    ),

    _law(
        "paragraphs-stay-under-five-sentences",
        "No paragraph of documentation or interface prose runs past five sentences",
        _cited("GOV.UK writing guidelines, Use clear language"),
        falsifier="A paragraph of six or more sentences. Countable — checkable by "
                  "machine exactly as sentences-stay-under-twenty-five-words is.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("GOV.UK — Writing guidelines, Use clear language",
                    "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/",
                    "Keep chunks of text short. Paragraphs should have no more "
                    "than 5 sentences each.")],
        sightings=[
            ("craft-laws itself, 2026-08-17 — its own README",
             "The old opening carried the definition of a law, the red-gate "
             "argument, the prose-cannot-fire thesis and the counts doctrine in "
             "one seven-sentence paragraph — four ideas a reader had to "
             "disentangle unaided."),
        ],
        note="The sibling of the 25-word sentence ceiling, one level up, from the "
             "same authority and page.",
    ),

    _law(
        "say-it-once",
        "A document states each fact once — an edit integrates into what is "
        "already written, it never restates it",
        _cited("GOV.UK writing guidelines, Create a clear structure"),
        falsifier="Two sentences in one document saying the same thing in nearly "
                  "the same words. Observable by comparison, and the signature of "
                  "a machine edit that appended instead of integrating — the "
                  "reader meets the same fact twice and wonders which copy is "
                  "current.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("GOV.UK — Writing guidelines, Clear structure",
                    "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/",
                    "Do not repeat yourself. You’ll have to write a summary to go "
                    "at the top of the page. Do not repeat the summary in the "
                    "first paragraph.")],
        note="Also the readability face of a deeper defect: two copies of one "
             "fact drift independently, and then the document disagrees with "
             "itself — the doc-lane twin of no-cross-context-string-reuse.",
    ),

    _law(
        "references-name-their-target-not-its-position",
        "A document refers to its own parts by name — never 'above', 'below', or "
        "'as mentioned earlier', which break silently when an edit moves things",
        _cited("Google developer documentation style guide, word list: above"),
        falsifier="'See above', 'the section below', 'as mentioned earlier' — a "
                  "wordlist over the document. Each is a reference that goes "
                  "quietly wrong the day a paragraph moves, which is every day a "
                  "machine edits.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("Google developer documentation style guide — word list, "
                    "'above'",
                    "https://developers.google.com/style/word-list",
                    "Don't use to refer to a position in a document. Instead, use "
                    "earlier or preceding.")],
        note="instructions-point-by-name-not-by-place, one lane over: that law "
             "holds app copy that directs a person to a control; this one holds "
             "a document that directs a reader to itself.",
    ),

    _law(
        "acronyms-spell-out-on-first-reference",
        "An abbreviation is spelled out the first time it appears; only then may "
        "the short form travel alone",
        _cited("Google developer documentation style guide, Abbreviations"),
        falsifier="An acronym used bare before (or without) the sentence that "
                  "spells it out — observable from reading order alone, exactly "
                  "as terms-defined-before-use is, and mechanical without even a "
                  "glossary: the short form and its parenthetical expansion have "
                  "a fixed shape.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("Google developer documentation style guide — Abbreviations",
                    "https://developers.google.com/style/abbreviations",
                    "Spell out abbreviations on first reference.")],
        note="The source's own carve-out stands: standard acronyms the audience "
             "reads faster than their expansions (API, URL, JSON) are exempt — "
             "the decider carries that list, visibly.",
    ),

    _law(
        "conditions-come-before-instructions",
        "The circumstance, condition, or goal comes before the instruction it "
        "qualifies — the reader learns whether a sentence applies before paying "
        "for it",
        _cited("Google developer documentation style guide, Sentence structure"),
        falsifier="An instruction with its condition trailing — 'Click Delete if "
                  "you want to delete the document', 'See X for more "
                  "information' — the source's own not-recommended shapes, "
                  "matchable by pattern.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        citations=[("Google developer documentation style guide — Sentence "
                    "structure",
                    "https://developers.google.com/style/sentence-structure",
                    "If you want to tell the reader to do something, try to "
                    "mention the circumstance, conditions, or goal before you "
                    "provide the instruction. Mentioning the circumstance first "
                    "lets the reader skip the instruction if it doesn't apply.")],
    ),

    _law(
        "internal-references-resolve",
        "Every reference a document makes to its own parts — an anchor, a section "
        "name, a relative link — points at something that exists",
        _uncited(),
        falsifier="A markdown anchor with no matching heading, a relative link to "
                  "a file that is not there, a named section nobody can find. "
                  "Fully mechanical, and the documentation counterpart of drift: a "
                  "green document over a moved target is a proof over a fiction.",
        triggers=["the project ships documentation meant to be read long after it "
                  "is written (a README, a guide, a reference)"],
        note="Uncited and red, in this repo's own tradition: universally enforced "
             "by link checkers everywhere, yet no style authority has been found "
             "STATING it as a writing rule. Source it or drop it — and meanwhile "
             "it is the one defect class every long-lived document accumulates "
             "under machine editing.",
    ),

    _law(
        "status-is-visible",
        "Every act a person commits shows them something changed",
        _cited(NNG + ", #1 Visibility of System Status"),
        falsifier="An action that commits — a tap that succeeds — after which nothing a person "
                  "can see is different. 'It worked and nothing happened': no error, no "
                  "refusal, and the person left tapping again.",
        triggers=["any interface with a control that commits something"],
        citations=[(NNG + " — #1 Visibility of System Status", NNG_URL,
                    "The design should always keep users informed about what is going on, "
                    "through appropriate feedback within a reasonable amount of time.")],
    ),

    _law(
        "one-act-one-name",
        "The same action wears the same words everywhere it is offered",
        _cited(NNG + ", #4 Consistency and Standards"),
        falsifier="Two controls committing the same action under different labels — or a "
                  "SPECIFIC label (one that names an act: 'Add it', 'Send') committing "
                  "different actions on different screens. Platform-conventional generic "
                  "confirms (OK, Done, Cancel) are exempt from the second half: they claim "
                  "no act beyond 'commit this context', which is the convention the law's "
                  "own citation tells interfaces to follow.",
        triggers=["any interface with a control that commits something"],
        citations=[(NNG + " — #4 Consistency and Standards", NNG_URL,
                    "Users should not have to wonder whether different words, situations, or "
                    "actions mean the same thing. Follow platform and industry conventions.")],
        sightings=[
            ("chores 2026-08-16, the three add sheets",
             "'Add it' committed add-a-chore, add-a-category and add-a-tag on three "
             "different sheets — proved co-offered by the compiled law the day the sheets "
             "were drawn, each conviction carrying its two-tap path. Ruled a defect: the "
             "act was already named by the menu that led there, so the commits became a "
             "generic confirm — and the ruling refined this law with the generic-confirm "
             "exemption, so every adopter inherits the sharper check."),
        
            ("spec-studio ruling cards, 2026-08-18",
             "the ellipsis card carried twelve findings: six menu entries × two "
             "languages, the identical sentence beneath each. A bilingual app finds "
             "every string defect once per language BY CONSTRUCTION, so evidence "
             "doubles unless something merges it — the founder: 'there is "
             "duplication'. One line now quotes all twelve places."),
        ],
        note="Which labels count as generic is an authoring-time declaration (the compiler's "
             "generic_keys), not a hardcoded wordlist: 'OK' is generic everywhere, but an "
             "app's voice may make 'Done' specific, and only its authors know.",
    ),

    _law(
        "targets-are-thumb-sized",
        "A control a finger must hit is at least 24 by 24 CSS pixels",
        _cited("W3C, WCAG 2.2, Success Criterion 2.5.8 Target Size (Minimum), Level AA"),
        falsifier="A pointer target measuring under 24 CSS pixels in either dimension, with no "
                  "equivalent larger control on the same view and no 24px undersized-target "
                  "spacing exception applying.",
        triggers=["the app is used on a phone",
                  "any interface with a control that commits something"],
        citations=[("W3C — WCAG 2.2, SC 2.5.8 Target Size (Minimum)",
                    "https://www.w3.org/TR/WCAG22/#target-size-minimum",
                    "The size of the target for pointer inputs is at least 24 by 24 CSS "
                    "pixels, except where: Spacing: Undersized targets ... Equivalent: The "
                    "function can be achieved through a different control on the same page "
                    "that meets this criterion.")],
        note="WCAG's floor, not the platforms' comfort: Apple's HIG asks 44pt and Material "
             "48dp. The law takes the citable minimum; an app may hold itself to more.",
    ),

    # =========================================================================
    # THE MINED LAWS — 2026-08-16, from the source catalogue (docs/sources.md).
    # Four mining passes (accessibility, government/forms/copy, localization,
    # empirical/content), every citation quote fetched and verified verbatim
    # against the cited page; where clusters collided (errors, colour), the
    # overlap map decided the root and the collision is recorded in the note.
    # =========================================================================

    # --- errors ------------------------------------------------------------------

    _law(
        "error-names-the-culprit",
        "A rejected input is identified by name and its error described in words",
        _cited("W3C, WCAG 2.2, SC 3.3.1 Error Identification, Level A"),
        falsifier="A failed submit showing only a generic verdict ('Something went wrong'), "
                  "a colour change alone, or one message for two distinguishable causes the "
                  "backend can tell apart (too short vs wrong prefix vs missing).",
        triggers=["any interface with a control that commits something"],
        citations=[("W3C — WCAG 2.2, SC 3.3.1 Error Identification",
                    "https://www.w3.org/TR/WCAG22/#error-identification",
                    "If an input error is automatically detected, the item that is in error "
                    "is identified and the error is described to the user in text."),
                   ("Baymard Institute — Improve Validation Errors with Adaptive Messages",
                    "https://baymard.com/blog/adaptive-validation-error-messages",
                    "98% of sites in our benchmark don't use error messages targeted "
                    "specifically at the exact problem that triggered the error — despite "
                    "the back-end logic knowing the issue")],
        note="WCAG is the formal root; Baymard's testing sharpens it to the EXACT cause "
             "('we observed participants take up to five minutes to resolve simple errors "
             "... solely due to vague error message wording').",
    ),

    _law(
        "error-says-the-fix",
        "An error states what happened and the specific instruction that fixes it",
        _cited("W3C, WCAG 2.2, SC 3.3.3 Error Suggestion; GOV.UK Design System"),
        falsifier="A message naming a problem whose correction is known without stating what "
                  "a valid entry looks like — 'invalid date' where the format was knowable; "
                  "an error code with no instruction.",
        triggers=["any interface with a control that commits something"],
        citations=[("W3C — WCAG 2.2, SC 3.3.3 Error Suggestion",
                    "https://www.w3.org/TR/WCAG22/#error-suggestion",
                    "If an input error is automatically detected and suggestions for "
                    "correction are known, then the suggestions are provided to the user, "
                    "unless it would jeopardize the security or purpose of the content."),
                   ("GOV.UK Design System — Error message",
                    "https://design-system.service.gov.uk/components/error-message/",
                    "Describe what has happened and tell them how to fix it. The message "
                    "must be in plain English, use positive language and get to the point.")],
        note="GOV.UK's operational split is itself checkable per message: 'Use an "
             "instruction for empty fields like ‘Enter your name’, but a description like "
             "‘Name must be 35 characters or less’ for entries that are too long.' "
             "Research-backed: users 'understood what went wrong, knew how to fix the "
             "problem, were able to recover from the error.'",
    ),

    _law(
        "error-neither-begs-nor-blames",
        "Error copy neither pleads, apologises, nor accuses — no please, no sorry, no "
        "blame words",
        _cited("GOV.UK Design System, Error message"),
        falsifier="An error message containing 'please', 'sorry', or blame vocabulary such "
                  "as 'forbidden', 'illegal', 'you forgot', 'prohibited'. A wordlist scan.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Error message",
                    "https://design-system.service.gov.uk/components/error-message/",
                    "Do not use: 'please' because it implies a choice ... 'sorry' because "
                    "it does not help fix the problem ... words like 'forbidden', "
                    "'illegal', 'you forgot' and 'prohibited'")],
        note="Adjacent to no-system-vocabulary (which bans the machine's words); this bans "
             "the beggar's and the judge's. Decider material: a pure wordlist.",
    ),

    _law(
        "error-lands-at-the-field",
        "A validation error renders beside the field it names, and the page-level summary "
        "links to it in identical words",
        _cited("GOV.UK Design System, Error summary"),
        falsifier="A failed submit whose message is not adjacent to the offending field; a "
                  "multi-error page with no summary; or a summary entry worded differently "
                  "from the inline message beside the field.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Error summary",
                    "https://design-system.service.gov.uk/components/error-summary/",
                    "Always show an error summary when there is a validation error, even "
                    "if there's only one. ... make sure the error messages in the error "
                    "summary are worded the same as those which appear next to the inputs "
                    "with errors"),
                   ("USWDS — Form",
                    "https://designsystem.digital.gov/components/form/",
                    "Align validation messages with the input fields so people using "
                    "screen magnifiers can read them quickly.")],
    ),

    _law(
        "validate-at-field-exit",
        "Validity is checked when the user leaves a field — not on every keystroke, not "
        "only at submit",
        _cited("Baymard Institute, inline form validation testing"),
        falsifier="Errors first appearing only after full-form submission; errors firing "
                  "mid-typing on an incomplete value.",
        triggers=["any interface with a control that commits something"],
        citations=[("Baymard Institute — Usability Testing of Inline Form Validation",
                    "https://baymard.com/blog/inline-form-validation",
                    "the validity of each field input should be checked when the user "
                    "leaves the field"),
                   ("Shopify — app design, Alerts",
                    "https://shopify.dev/docs/apps/design/user-experience/alerts",
                    "Avoid showing an error while merchants are typing, because it can "
                    "cause confusion.")],
        note="Empirical root: without inline validation Baymard's 'participants were "
             "forced to come to a complete stop.'",
    ),

    # --- forms -------------------------------------------------------------------

    _law(
        "no-placeholder-labels",
        "Placeholder text never carries a label, hint, or example — what the user needs "
        "survives them starting to type",
        _cited("GOV.UK Design System, Text input"),
        falsifier="An input whose label, hint, or format example exists only as placeholder "
                  "text that vanishes on focus or typing.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Text input",
                    "https://design-system.service.gov.uk/components/text-input/",
                    "Do not use placeholder text in place of a label, or for hints or "
                    "examples, as: it vanishes when the user starts typing, which can "
                    "cause problems for users with memory conditions or when reviewing "
                    "answers")],
        note="GOV.UK gives three independent failure modes (vanishing, screen readers "
             "skipping it, default contrast failing), so the breach is observable without "
             "user testing. 'All text inputs must have labels, and in most cases the "
             "label should be visible.'",
    ),

    _law(
        "every-input-labeled",
        "Every control that collects input carries a visible label or instruction that "
        "survives interaction",
        _cited("W3C, WCAG 2.2, SC 3.3.2 Labels or Instructions, Level A"),
        falsifier="A field whose only identification vanishes on focus, or an unlabeled "
                  "input whose purpose must be guessed from position.",
        triggers=["any interface with a control that commits something"],
        citations=[("W3C — WCAG 2.2, SC 3.3.2 Labels or Instructions",
                    "https://www.w3.org/TR/WCAG22/#labels-or-instructions",
                    "Labels or instructions are provided when content requires user "
                    "input.")],
        note="The formal root under no-placeholder-labels: GOV.UK operationalizes what "
             "3.3.2 requires.",
    ),

    _law(
        "never-ask-twice",
        "Information the user already gave in a process is auto-populated or selectable, "
        "never retyped",
        _cited("W3C, WCAG 2.2, SC 3.3.7 Redundant Entry, Level A"),
        falsifier="Within one flow, a field asking again for a value entered at an earlier "
                  "step, offering neither pre-fill nor selection of the previous entry.",
        triggers=["any interface with a control that commits something"],
        citations=[("W3C — WCAG 2.2, SC 3.3.7 Redundant Entry",
                    "https://www.w3.org/TR/WCAG22/#redundant-entry",
                    "Information previously entered by or provided to the user that is "
                    "required to be entered again in the same process is either: "
                    "auto-populated, or available for the user to select.")],
        note="The spec's own exceptions travel with it: essential re-entry, security, "
             "expired validity.",
    ),

    _law(
        "mark-optional-and-required-alike",
        "Both required and optional fields are explicitly marked — never just one class",
        _cited("Baymard Institute, checkout usability testing"),
        falsifier="A form where required fields carry a mark and optional fields carry "
                  "nothing, or vice versa.",
        triggers=["any interface with a control that commits something"],
        citations=[("Baymard Institute — Mark Both Required and Optional Fields",
                    "https://baymard.com/blog/required-optional-form-fields",
                    "both required and optional fields should be explicitly marked")],
        note="Tested: '32% of users during testing had a validation error because they "
             "did not complete a required field' when only optional fields were marked. "
             "Only 14% of benchmarked checkouts do this.",
    ),

    _law(
        "field-width-matches-the-answer",
        "A field's rendered width matches the length of the expected input",
        _cited("Baymard Institute, form field usability testing"),
        falsifier="A fixed-length input (CVC, ZIP, year) rendered at full form width; "
                  "uniform widths across fields with known different input lengths.",
        triggers=["any interface with a control that commits something"],
        citations=[("Baymard Institute — Form Field Usability: Matching User Expectations",
                    "https://baymard.com/blog/form-field-usability-matching-user-expectations",
                    "If a field was too long or too short, the test subjects started to "
                    "wonder if they had misunderstood the label")],
        note="Users read width as a format hint; the geometry is measurable, so this can "
             "one day join the constraint solver.",
    ),

    _law(
        "one-entity-one-field",
        "A single input entity — phone, date typed as one, name, card number — is one "
        "field, never split across several",
        _cited("Baymard Institute, mobile form usability testing"),
        falsifier="A phone number split into three boxes; separate MM and YY expiry "
                  "fields; auto-tab hopping between fragments.",
        triggers=["the app is used on a phone"],
        citations=[("Baymard Institute — Avoid Splitting Single Input Entities",
                    "https://baymard.com/blog/mobile-form-usability-single-input-fields",
                    "you should avoid splitting single input entities across multiple "
                    "fields")],
        note="Lives beside known-date-three-boxes without contradiction: GOV.UK's date "
             "rule is the researched exception for memorable dates, where the three "
             "parts are how people actually hold the value.",
    ),

    _law(
        "known-date-three-boxes",
        "A date the user knows is three labelled text fields — day, month, year — never "
        "a calendar picker or dropdowns, never auto-tabbed",
        _cited("GOV.UK Design System, Date input; USWDS, Date of birth"),
        falsifier="A memorable date (birth, document) offered only as a calendar control "
                  "or selects; auto-advance between the boxes.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Date input",
                    "https://design-system.service.gov.uk/components/date-input/",
                    "Never automatically tab users between the fields of the date input "
                    "because this can be confusing and may clash with normal keyboard "
                    "controls."),
                   ("USWDS — Date of birth pattern",
                    "https://designsystem.digital.gov/patterns/create-a-user-profile/date-of-birth/",
                    "Do not use a date picker.")],
        note="Research-backed twice: GOV.UK's teacher-training service saw errors 'drop "
             "dramatically' after the change. Scope: KNOWN dates; USWDS keeps pickers "
             "for scheduling ('If users are trying to schedule something, the date "
             "picker might make more sense').",
    ),

    _law(
        "no-disabled-submit",
        "A control that commits is never shown disabled — the button stays live and a "
        "failed press explains what is missing",
        _cited("GOV.UK Design System, Button"),
        falsifier="A greyed-out submit or action button, absent documented research "
                  "justifying it.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Button",
                    "https://design-system.service.gov.uk/components/button/",
                    "Disabled buttons have poor contrast and can confuse some users, so "
                    "avoid them if possible. ... Only use disabled buttons if research "
                    "shows it makes the user interface easier to understand.")],
        note="The escape hatch is itself falsifiable: a disabled button with no research "
             "on file is the breach.",
    ),

    _law(
        "keyboard-matches-the-field",
        "Each input summons the touch keyboard matching its content type, consistently "
        "across the whole flow",
        _cited("Baymard Institute, mobile touch keyboard benchmark"),
        falsifier="A card-number or phone field summoning the alphabetic keyboard; a flow "
                  "right on one screen and wrong on the next.",
        triggers=["the app is used on a phone"],
        citations=[("Baymard Institute — Touch Keyboard Implementations",
                    "https://baymard.com/blog/mobile-touch-keyboards",
                    "54% of mobile sites fail to invoke optimized touch keyboards")],
    ),

    _law(
        "no-autocorrect-on-identifiers",
        "Autocorrect and autocapitalize are off for identifiers the dictionary does not "
        "know: emails, names, addresses, usernames, codes",
        _cited("Baymard Institute, mobile touch keyboard benchmark"),
        falsifier="An email field capitalizing its first letter; an address line whose "
                  "street name gets dictionary-corrected.",
        triggers=["the app is used on a phone"],
        citations=[("Baymard Institute — Touch Keyboard Implementations",
                    "https://baymard.com/blog/mobile-touch-keyboards",
                    "auto-correction on this type of information led to numerous "
                    "interruptions")],
        note="Observed: with autocapitalize on, 'the subjects frequently went back and "
             "actively deleted the first capital letters as they feared e-mail delivery "
             "issues.'",
    ),

    # --- flows -------------------------------------------------------------------

    _law(
        "one-question-per-page",
        "A transactional flow starts at one question per page; questions share a page "
        "only when evidence shows the grouping helps",
        _cited("GOV.UK Design System, Question pages"),
        falsifier="A step in a form flow piling unrelated questions onto one page with "
                  "no research behind the grouping.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Question pages",
                    "https://design-system.service.gov.uk/patterns/question-pages/",
                    "Asking just one question per question page helps users understand "
                    "what you're asking them to do, and focus on the specific question "
                    "and its answer.")],
        note="The flow-shaped sibling of one-surface-one-job (which governs a surface's "
             "purpose); the default-until-evidence direction is the law.",
    ),

    _law(
        "check-before-commit",
        "Before an irreversible submit the user sees everything they entered, and "
        "changing an answer never re-walks the rest of the flow",
        _cited("GOV.UK Design System, Check answers"),
        falsifier="A multi-step transaction committing without a review page; a Change "
                  "link that forces the user back through subsequent steps.",
        triggers=["any interface with a control that commits something"],
        citations=[("GOV.UK Design System — Check answers",
                    "https://design-system.service.gov.uk/patterns/check-answers/",
                    "When they've finished, the 'Continue' button should return them to "
                    "the check answers page. They should not need to go through the rest "
                    "of the transaction again.")],
        note="Distinct from a-way-back: that is escape, this is verification before "
             "commitment. The round-trip clause is the sharp edge — many apps have the "
             "review page and fail the return path.",
    ),

    _law(
        "destructive-is-set-apart",
        "A destructive action is visually separated from safe actions, marked in the "
        "critical tone, and paired with a cancel in its confirmation",
        _cited("Shopify Polaris, Button group"),
        falsifier="A Delete adjacent to and styled identically to Save; a destructive act "
                  "executing with no confirmation; a confirm whose destructive button "
                  "has no paired cancel.",
        triggers=["an action is destructive, irreversible, or binding on somebody else "
                  "(a task assigned to another person; a schedule change for the "
                  "whole group)"],
        citations=[("Shopify Polaris — Button group",
                    "https://shopify.dev/docs/api/app-home/web-components/actions/button-group",
                    "Pair a cancel button with a critical action for destructive "
                    "confirmation flows. ... Separate destructive actions: Position "
                    "destructive actions appropriately and use critical tone to prevent "
                    "accidental activation.")],
        note="The weakest citation of the mined set — component-level guidance rather "
             "than a stated principle; the claim stays inside the quoted text and wants "
             "a stronger root when one is found.",
    ),

    # --- keyboard and pointer ----------------------------------------------------

    _law(
        "escape-closes-the-overlay",
        "Escape dismisses a modal overlay, and closing it returns focus to what opened it",
        _cited("W3C, ARIA Authoring Practices Guide, Modal Dialog pattern (non-normative)"),
        falsifier="A dialog that survives Escape; a closed dialog dropping focus on the "
                  "page body instead of the invoking element.",
        triggers=["any interface at all"],
        citations=[("W3C — ARIA Authoring Practices, Modal Dialog",
                    "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/",
                    "Escape: Closes the dialog.")],
        note="The keyboard instance of a-way-back. APG is the true root — WCAG never "
             "requires Escape — and APG is non-normative, said here because a citation "
             "that overstates its authority is worse than none. Also from the pattern: "
             "'When a dialog closes, focus returns to the element that invoked the "
             "dialog'.",
    ),

    _law(
        "one-tab-stop-per-widget",
        "Tab moves between widgets; arrows move within one — a composite widget is a "
        "single tab stop",
        _cited("W3C, ARIA Authoring Practices Guide, Developing a Keyboard Interface "
               "(non-normative)"),
        falsifier="Tabbing steps through every option of one radio group or cell of one "
                  "grid; focus inside a composite where arrow keys move nothing.",
        triggers=["any interface at all"],
        citations=[("W3C — ARIA APG, Developing a Keyboard Interface",
                    "https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/",
                    "the tab sequence should include only one focusable element of a "
                    "composite UI component. Once a composite contains focus, keys other "
                    "than Tab and Shift + Tab enable the user to move focus among its "
                    "focusable elements.")],
    ),

    _law(
        "no-keyboard-trap",
        "Anywhere focus can enter, focus can leave by keyboard alone",
        _cited("W3C, WCAG 2.2, SC 2.1.2 No Keyboard Trap, Level A"),
        falsifier="Tab into a component; Tab, Shift+Tab and arrows cannot move focus "
                  "out, and no exit method is announced.",
        triggers=["any interface at all"],
        citations=[("W3C — WCAG 2.2, SC 2.1.2 No Keyboard Trap",
                    "https://www.w3.org/TR/WCAG22/#no-keyboard-trap",
                    "If keyboard focus can be moved to a component of the page using a "
                    "keyboard interface, then focus can be moved away from that "
                    "component using only a keyboard interface")],
        note="a-way-back's keyboard-focus instance, as escape-closes-the-overlay is its "
             "overlay instance: three laws, one doctrine, three falsifiers.",
    ),

    _law(
        "touch-commits-on-release",
        "A pointer action commits on release, never on press — sliding off is a cancel",
        _cited("W3C, WCAG 2.2, SC 2.5.2 Pointer Cancellation, Level A"),
        falsifier="A control firing on touch-down; press, drag off, release — and the "
                  "action fires anyway.",
        triggers=["the app is used on a phone"],
        citations=[("W3C — WCAG 2.2, SC 2.5.2 Pointer Cancellation",
                    "https://www.w3.org/TR/WCAG22/#pointer-cancellation",
                    "No Down-Event: The down-event of the pointer is not used to execute "
                    "any part of the function"),
                   ("BBC — Mobile Accessibility Guidelines, Appropriate triggers",
                    "https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/appropriate-triggers/",
                    "This allows users to change their mind and adjust focus, without "
                    "being forced to commit to an action until the clicked mouse, or "
                    "touch is removed.")],
        note="WCAG codifies a platform convention older than it — native controls "
             "behave this way by default, so the breach is almost always a hand-rolled "
             "control.",
    ),

    _law(
        "gesture-has-a-plain-alternative",
        "Anything operable by swipe, pinch, or multi-finger gesture is also operable by "
        "a single tap on a visible control",
        _cited("W3C, WCAG 2.2, SC 2.5.1 Pointer Gestures, Level A"),
        falsifier="A function (carousel advance, dismiss, zoom) reachable only through a "
                  "path-based or multipoint gesture, with no visible single-pointer "
                  "control doing the same.",
        triggers=["the app is used on a phone"],
        citations=[("W3C — WCAG 2.2, SC 2.5.1 Pointer Gestures",
                    "https://www.w3.org/TR/WCAG22/#pointer-gestures",
                    "All functionality that uses multipoint or path-based gestures for "
                    "operation can be operated with a single pointer without a "
                    "path-based gesture, unless a multipoint or path-based gesture is "
                    "essential."),
                   ("BBC — Mobile Accessibility Guidelines, Alternative input methods",
                    "https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/alternative-input-methods/",
                    "a carousel must not support only touch interaction, it must also "
                    "support alternative inputs via visible focusable elements.")],
    ),

    _law(
        "works-both-ways-up",
        "The app works in portrait and landscape alike",
        _cited("W3C, WCAG 2.2, SC 1.3.4 Orientation, Level AA"),
        falsifier="Rotate the device: content refuses to rotate, or view or operation "
                  "breaks in one orientation.",
        triggers=["the app is used on a phone"],
        citations=[("W3C — WCAG 2.2, SC 1.3.4 Orientation",
                    "https://www.w3.org/TR/WCAG22/#orientation",
                    "Content does not restrict its view and operation to a single "
                    "display orientation, such as portrait or landscape, unless a "
                    "specific display orientation is essential.")],
    ),

    # --- signals and structure ---------------------------------------------------

    _law(
        "colour-is-never-the-only-signal",
        "No distinction, state, or prompt is carried by colour and nothing else",
        _cited("W3C, WCAG 2.2, SC 1.4.1 Use of Color, Level A"),
        falsifier="Desaturate a screenshot to grayscale: some information disappears — "
                  "the errored field, the selected tab, the actionable-vs-static "
                  "distinction. A measurement, not a judgement.",
        triggers=["any interface at all"],
        citations=[("W3C — WCAG 2.2, SC 1.4.1 Use of Color",
                    "https://www.w3.org/TR/WCAG22/#use-of-color",
                    "Color is not used as the only visual means of conveying "
                    "information, indicating an action, prompting a response, or "
                    "distinguishing a visual element."),
                   ("USWDS — Color tokens",
                    "https://designsystem.digital.gov/design-tokens/color/overview/",
                    "Color should only be used as progressive enhancement — if color is "
                    "the only signal, that signal won't get through as intended to "
                    "everyone.")],
        note="BBC generalizes past colour ('Visual formatting alone must not be used to "
             "convey meaning') — carried here as a note until formatting-alone earns "
             "its own falsifier.",
    ),

    _law(
        "navigation-keeps-its-order",
        "A navigation mechanism repeated across screens keeps the same relative order "
        "everywhere",
        _cited("W3C, WCAG 2.2, SC 3.2.3 Consistent Navigation, Level AA"),
        falsifier="Two screens sharing a nav bar or menu where the same items appear in "
                  "a different relative order, unrequested.",
        triggers=["any interface at all"],
        citations=[("W3C — WCAG 2.2, SC 3.2.3 Consistent Navigation",
                    "https://www.w3.org/TR/WCAG22/#consistent-navigation",
                    "Navigational mechanisms that are repeated on multiple Web pages "
                    "within a set of Web pages occur in the same relative order each "
                    "time they are repeated, unless a change is initiated by the "
                    "user.")],
        note="The structural sibling of one-act-one-name (WCAG 3.2.4, which that law "
             "already covers): same words there, same order here.",
    ),

    _law(
        "truncation-is-signposted",
        "When a set of items is cut off, the cut is visible — a count, an arrow, a "
        "partial item — never a clean edge that looks complete",
        _cited("Baymard Institute, product-gallery usability testing"),
        falsifier="A truncated list or gallery whose visible items form a tidy, "
                  "complete-looking set with no cue that more exist.",
        triggers=["any interface at all"],
        citations=[("Baymard Institute — Always Signpost Hidden Thumbnails",
                    "https://baymard.com/blog/truncating-product-gallery-thumbnails",
                    "participants did not always realize additional images were "
                    "available")],
        note="The empirical cousin of the drawing's totality doctrine: a silent cut "
             "reads as the whole.",
    ),

    _law(
        "text-survives-doubling",
        "Everything the screen says is still there, still readable, and still "
        "operable with the text at twice its size",
        _cited("W3C, WCAG 2.2, SC 1.4.4 Resize Text, Level AA"),
        falsifier="At 200% text size, a string clipped, a control pushed off-screen "
                  "or under another, a function no longer reachable. Measurable: the "
                  "same layout premises the fits constraints solve over, with the "
                  "font widths doubled.",
        triggers=["any interface at all"],
        citations=[("W3C — WCAG 2.2, SC 1.4.4 Resize Text",
                    "https://www.w3.org/TR/WCAG22/#resize-text",
                    "Except for captions and images of text, text can be resized "
                    "without assistive technology up to 200 percent without loss of "
                    "content or functionality."),
                   ("RGAA 4 — Critère 10.4",
                    "https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/",
                    "Dans chaque page web, le texte reste-t-il lisible lorsque la "
                    "taille des caractères est augmentée jusqu’à 200 %, au moins "
                    "(hors cas particuliers) ?")],
        note="text-expansion's monolingual twin: that law doubles the words "
             "(another language), this one doubles the glyphs (the reader's eyes). "
             "Both land on the same solver over the same measured premises.",
    ),

    _law(
        "ellipsis-promises-more-input",
        "A control label ends in an ellipsis exactly when the action needs further "
        "input before it can run",
        _cited("GNOME Human Interface Guidelines, Writing Style"),
        falsifier="A 'Delete…' that deletes immediately; a 'Save As' with no ellipsis "
                  "that opens a dialog. Both directions breach.",
        triggers=["any interface with a control that commits something"],
        citations=[("GNOME HIG — Writing Style",
                    "https://developer.gnome.org/hig/guidelines/writing-style.html",
                    "Use an ellipsis (…) at the end of a label if further input or "
                    "confirmation is required from the user before the action can be "
                    "carried out.")],
        note="GNOME states it as a biconditional, which is what makes it a law rather "
             "than a style tip: the ellipsis is a load-bearing signal, so a decorative "
             "one is a lie.",
    ),

    _law(
        "sentence-labels-take-sentence-case",
        "Labels that form or run into sentences — field labels, checkbox captions, "
        "column headings — take sentence case, never title case",
        _cited("GNOME HIG, Writing Style; GitLab Pajamas, UI text"),
        falsifier="A field label or checkbox caption in Title Case on a surface whose "
                  "siblings are sentence case.",
        triggers=["any interface with a control that commits something"],
        citations=[("GNOME HIG — Writing Style",
                    "https://developer.gnome.org/hig/guidelines/writing-style.html",
                    "Sentence capitalization should be used for labels that form "
                    "sentences or that run on to other text, including labels for check "
                    "boxes, radio buttons, sliders, text entry boxes, field labels and "
                    "combobox labels."),
                   ("GitLab Pajamas — How to write UI text",
                    "https://design.gitlab.com/content/ui-text",
                    "Use sentence case for field labels and column headings. Avoid "
                    "title case.")],
        note="The sources disagree on buttons (GNOME header-caps them, GitLab does "
             "not), so the law claims only what both assert: sentence-shaped labels "
             "never get title case.",
    ),

    # --- copy --------------------------------------------------------------------

    _law(
        "sentences-stay-under-twenty-five-words",
        "No sentence of interface prose runs past 25 words unsplit",
        _cited("GOV.UK writing guidelines, Use clear language"),
        falsifier="A sentence in UI copy exceeding 25 words. Countable.",
        triggers=["the app's voice does work of its own (dry, terse, no explaining text)"],
        citations=[("GOV.UK — Writing guidelines, Use clear language",
                    "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/",
                    "Try to split up sentences that are over 25 words long.")],
        note="The source says 'try': the law reads a standing unsplit 26-word sentence "
             "as the breach and leaves deliberate exceptions to the judge. The one "
             "mined law with a number in its falsifier — decider material.",
    ),

    _law(
        "front-load-first-words",
        "Headings, titles, and messages put the differentiating information in the "
        "first words, never behind boilerplate",
        _cited("GOV.UK writing guidelines, Create a clear structure"),
        falsifier="A heading like 'Introduction'; a notification opening with preamble "
                  "before the fact that matters.",
        triggers=["the app's voice does work of its own (dry, terse, no explaining text)"],
        citations=[("GOV.UK — Writing guidelines, Clear structure",
                    "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/",
                    "descriptive – avoid generic headings like 'Introduction'")],
        sightings=[
            ("craft-laws itself, 2026-08-17 — its own README",
             "The front page's first words were 'This repo does not pass its own "
             "check today — on purpose' — the house paradox front-loaded ahead of "
             "the one fact a visitor came for, what the repo is."),
        ],
        note="Grounded on the same page: users 'only read 20 to 28% of text on a "
             "webpage' and read in an F-pattern — the first words are the only ones "
             "guaranteed to be read.",
    ),

    _law(
        "speaks-to-you",
        "Copy addresses the user as 'you' in the active voice — never 'the user' in "
        "the third person, never a passive that hides who must act",
        _cited("GOV.UK style guide; digital.gov plain language guide"),
        falsifier="Interface copy referring to its own reader in the third person; an "
                  "instruction phrased passively so the actor is absent ('The form "
                  "must be completed').",
        triggers=["the app's voice does work of its own (dry, terse, no explaining text)"],
        citations=[("GOV.UK — A to Z style guide",
                    "https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/",
                    "Address the user as 'you' where possible"),
                   ("digital.gov — Plain language guide (formerly plainlanguage.gov)",
                    "https://digital.gov/guides/plain-language/writing",
                    "Active voice makes it clear who should do what. It eliminates "
                    "ambiguity about responsibilities.")],
    ),

    _law(
        "links-say-where-they-lead",
        "A link's own words say what it opens — 'here' and 'this page' say nothing "
        "without the sentence around them",
        _cited("W3C, WCAG 2.2, SC 2.4.4 Link Purpose (In Context), Level A"),
        falsifier="A link or navigation control whose text is 'here', 'click here', "
                  "'this document', 'this page', 'more', 'read more', or a bare URL — "
                  "a wordlist over link labels, no interpretation needed.",
        triggers=["the app or its documentation links a reader somewhere else"],
        citations=[("W3C — WCAG 2.2, SC 2.4.4 Link Purpose (In Context)",
                    "https://www.w3.org/TR/WCAG22/#link-purpose-in-context",
                    "The purpose of each link can be determined from the link text "
                    "alone or from the link text together with its programmatically "
                    "determined link context, except where the purpose of the link "
                    "would be ambiguous to users in general."),
                   ("Google developer documentation style guide — Link text",
                    "https://developers.google.com/style/link-text",
                    "Write link text that makes sense without the surrounding text. "
                    "Don't use phrases such as this document, this article, or "
                    "click here."),
                   ("RGAA 4 — Critère 6.1, test 6.1.1",
                    "https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/",
                    "Chaque lien est-il explicite (hors cas particuliers) ? … "
                    "L’intitulé de lien seul permet d’en comprendre la fonction")],
        note="The standard is the root; Google's page is the operational wordlist "
             "half (decider material), and RGAA the test-procedure phrasing. "
             "Kin to says-what-happens — that law holds a control's label to its "
             "act, this one holds a link's label to its destination.",
    ),

    _law(
        "instructions-point-by-name-not-by-place",
        "Copy that directs a person to a control names it — never 'the button on the "
        "right', 'the green icon', 'below'",
        _cited("W3C, WCAG 2.2, SC 1.3.3 Sensory Characteristics, Level A"),
        falsifier="An instruction identifying its target only by shape, colour, size, "
                  "or position — a wordlist over the catalogue ('on the right', "
                  "'above', 'below', 'the green/red …'), each hit checkable against "
                  "whether the sentence also names the control.",
        triggers=["the app's copy or documentation directs a person to a control"],
        citations=[("W3C — WCAG 2.2, SC 1.3.3 Sensory Characteristics",
                    "https://www.w3.org/TR/WCAG22/#sensory-characteristics",
                    "Instructions provided for understanding and operating content "
                    "do not rely solely on sensory characteristics of components "
                    "such as shape, color, size, visual location, orientation, or "
                    "sound."),
                   ("RGAA 4 — Critère 10.9",
                    "https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/",
                    "Dans chaque page web, l’information ne doit pas être donnée "
                    "uniquement par la forme, taille ou position.")],
        note="Also the layout truth beneath it: a position-worded instruction is a "
             "sentence that goes false when the layout reflows — the same staleness "
             "mechanism docs-do-not-date-themselves names for time.",
    ),

    # --- localization ------------------------------------------------------------

    _law(
        "no-cross-context-string-reuse",
        "A string resource serves exactly one UI context; the same phrase in two "
        "places is two entries",
        _cited("Mozilla, Localization best practices for developers"),
        falsifier="One catalogue entry referenced from two distinct UI surfaces (a "
                  "button label and a dialog title sharing an ID) — visible in the "
                  "resource file's reference graph, and as a translation fix in one "
                  "place visibly changing the other.",
        triggers=["the app is translated into any second language"],
        citations=[("Mozilla — Localization best practices for developers",
                    "https://mozilla-l10n.github.io/documentation/localization/dev_best_practices.html",
                    "some locales use nouns for titles, and verbs for actions (for "
                    "example button labels)")],
        note="Distinct from composed-prose: this is one string in two PLACES, not two "
             "strings glued into one sentence.",
    ),

    _law(
        "string-id-tracks-meaning",
        "When a string's meaning changes, its ID changes — so stale translations fall "
        "out instead of shipping silently",
        _cited("Mozilla, Localization best practices for developers"),
        falsifier="A commit altering a source string's meaning while keeping its ID, "
                  "with an old translation of the previous meaning still rendering in "
                  "a shipped locale.",
        triggers=["the app is translated into any second language"],
        citations=[("Mozilla — Localization best practices for developers",
                    "https://mozilla-l10n.github.io/documentation/localization/dev_best_practices.html",
                    "If you are changing a string such that its meaning has changed, "
                    "you must update the string ID.")],
    ),

    _law(
        "locale-machinery-formats",
        "Dates, times, numbers, and currency reach the screen through locale "
        "formatting machinery, never hand-assembled or hardcoded",
        _cited("Unicode CLDR"),
        falsifier="A date, number, or amount built by concatenation or a literal "
                  "pattern — observable as the value rendering identically under two "
                  "locales that format it differently.",
        triggers=["any count, duration, date, currency or name is interpolated into a "
                  "sentence"],
        citations=[("Unicode CLDR Project",
                    "https://cldr.unicode.org/",
                    "Formatting dates, numbers, currencies, and units of measurement "
                    "is far more complicated across different languages and regions "
                    "than most people recognize.")],
    ),

    _law(
        "list-patterns-not-commas",
        "Variable-length lists rendered into prose go through locale list patterns, "
        "not a hardcoded join",
        _cited("Unicode CLDR, list patterns"),
        falsifier="Code joining item arrays with literal separators and a conjunction "
                  "— an English-shaped list ('X, Y, and Z') verbatim inside another "
                  "locale's UI.",
        triggers=["the app is translated into any second language"],
        citations=[("Unicode CLDR — Lists",
                    "https://cldr.unicode.org/translation/miscellaneous-displaying-lists",
                    "List patterns can be used to format variable-length lists of "
                    "things in a locale-sensitive manner")],
        note="CLDR's own example: 'Monday, Tuesday, Friday, and Saturday' in English "
             "against 'lundi, mardi, vendredi et samedi' in French.",
    ),

    _law(
        "sort-by-collation",
        "User-visible lists sort through locale collation, never by code point",
        _cited("Unicode CLDR"),
        falsifier="A sorted user-facing list in a locale with accented or non-Latin "
                  "letters ordering by byte value — 'é' after 'z' in a French list.",
        triggers=["the app is translated into any second language"],
        citations=[("Unicode CLDR Project",
                    "https://cldr.unicode.org/",
                    "the alphabetical order of the files. All of these will vary "
                    "depending on your language — and all of these are usually "
                    "supplied by CLDR.")],
    ),

    _law(
        "language-declared",
        "The document declares its language, and every passage in another language "
        "is marked where it occurs",
        _cited("W3C, Internationalization — Declaring language in HTML"),
        falsifier="A served page whose html tag carries no lang attribute; a "
                  "foreign-language passage inside an element chain with no lang of "
                  "its own. Inspectable in the DOM.",
        triggers=["any interface at all"],
        citations=[("W3C i18n — Declaring language in HTML",
                    "https://www.w3.org/International/questions/qa-html-language-declarations",
                    "Always use a language attribute on the html tag to declare the "
                    "default language of the text in the page.")],
    ),

    _law(
        "base-direction-in-markup",
        "Base text direction is set in the markup, never through CSS alone",
        _cited("W3C, Internationalization — Structural markup and right-to-left text"),
        falsifier="An RTL locale served with direction applied only via CSS — no dir "
                  "attribute in the DOM, and scrambled ordering when styles fail.",
        triggers=["the app is translated into any second language"],
        citations=[("W3C i18n — Structural markup and right-to-left text in HTML",
                    "https://www.w3.org/International/questions/qa-html-dir",
                    "Do not use CSS to apply base direction in HTML pages.")],
        note="The spec's reason travels: 'you want the directional information to be "
             "available even when the CSS is not.'",
    ),

    _law(
        "rtl-mirrors-except-meaning",
        "In RTL locales the layout and directional icons mirror — except icons whose "
        "meaning does not mirror: media transport, physical objects, logos",
        _cited("Microsoft, Globalization documentation — Mirroring"),
        falsifier="In an RTL build, a forward arrow still pointing the LTR way; or a "
                  "play/fast-forward icon flipped. Either shows in one screenshot.",
        triggers=["the app is translated into any second language"],
        citations=[("Microsoft — Globalization, Mirroring",
                    "https://learn.microsoft.com/en-us/globalization/fonts-layout/mirroring",
                    "Note that not all images and icons should be mirrored. For "
                    "example, common icons such as the fast-forward and rewind icons "
                    "in media players, use the same orientation in both LTR and RTL "
                    "layouts.")],
        note="Material's bidirectionality page is the popular statement but is "
             "unfetchable (JS shell) — Microsoft carries the citation; Android's "
             "judgment clause corroborates ('if reflecting your drawable changes its "
             "interpretation, you can perform the mirroring yourself').",
    ),

    _law(
        "pseudolocale-before-translation",
        "The app builds and is exercised under a pseudolocale before strings go out "
        "for translation",
        _cited("Android Developers, Test your app with pseudolocales"),
        falsifier="No pseudolocale configuration in the build; or a pseudolocale run "
                  "showing unaccented (hardcoded) text or clipped expansion, shipped "
                  "anyway.",
        triggers=["the app is translated into any second language"],
        citations=[("Android Developers — Test your app with pseudolocales",
                    "https://developer.android.com/guide/topics/resources/pseudolocales",
                    "Hardcoded strings, which can't be sent to translation, display "
                    "as unaccented text in the pseudolocale to make them "
                    "noticeable.")],
        note="A practice law — it polices the build, not a screen — kept because its "
             "falsifier is observable in the repo and its breaches (hardcoded "
             "strings, clipped expansion) are the very defects text-expansion and "
             "the coach's #97 record.",
    ),

    _law(
        "no-text-baked-into-images",
        "Words never ship rasterized inside image assets",
        _cited("Android Developers, Localize your app; W3C WCAG 2.2 SC 1.4.5"),
        falsifier="A shipped image containing rendered words that stay identical when "
                  "the locale changes — a screenshot diff across locales, or a grep "
                  "of assets against the catalogue.",
        triggers=["the app is translated into any second language"],
        citations=[("Android Developers — Localize your app",
                    "https://developer.android.com/guide/topics/resources/localization",
                    "If you generate images with text, put those strings in "
                    "strings.xml as well, and regenerate the images after "
                    "translation."),
                   ("W3C — WCAG 2.2, SC 1.4.5 Images of Text",
                    "https://www.w3.org/WAI/WCAG21/Understanding/images-of-text.html",
                    "If the technologies being used can achieve the visual "
                    "presentation, text is used to convey information rather than "
                    "images of text")],
    ),

    # --- what accompanies a claim, 2026-08-18 --------------------------------------
    # Minted once, after a correction: five card-specific laws were written here first,
    # and the founder ruled the failure was at GENERALIZATION — «a rule about a card is
    # not generic». Three were instances of laws this file already had (say-it-once,
    # one-surface-one-job, no-system-vocabulary; their sightings moved there), one was
    # an app's own product spec and went back to its app, and the two about evidence
    # were one proposition wearing two costumes. This is that proposition, stated at
    # its real generality.

    _law(
        "what-accompanies-a-claim-supports-it",
        "Whatever is presented WITH a claim — a picture, a quotation, a figure — is "
        "relevant to it and consistent with it",
        _cited("H. P. Grice, Logic and Conversation — the maxims of Relation and "
               "Quality"),
        falsifier="Hold the claim against its own accompaniment: the picture does not "
                  "contain what the claim is about, or the words assert what the "
                  "accompaniment disproves — «the app says nothing» beside a "
                  "quotation of what it says.",
        triggers=["a claim is presented together with supporting material"],
        citations=[("Grice — Logic and Conversation, the maxim of Relation",
                    "https://plato.stanford.edu/entries/implicature/",
                    "Be relevant."),
                   ("Grice — Logic and Conversation, the maxim of Quality",
                    "https://plato.stanford.edu/entries/implicature/",
                    "Do not say what you believe to be false.")],
        sightings=[("spec-studio ruling cards, 2026-08-18",
                    "twice in one day. A conviction carried a photograph that did not "
                    "contain the convicted control — the capture walked to a screen "
                    "and photographed whatever was there, and once photographed the "
                    "right controls in the WRONG state, a healthy sheet as evidence "
                    "of a defect. Then a card claimed a button «greys out and says "
                    "nothing» directly above its own photograph of the app saying "
                    "«That name is already taken» in red. The founder found both.")],
        note="The decidable half is cheap because claim and accompaniment are both in "
             "the record. The checks live in craft/cards.py; they enforce THIS law in "
             "the card context and existing laws (say-it-once, one-surface-one-job, "
             "no-system-vocabulary) in the same pass. And a correction stands behind "
             "this entry: five card-specific laws stood here first, and the bar is "
             "now a proposition somebody outside that surface would recognize — "
             "otherwise it is the app's own spec and belongs in the app.",
    ),

    # --- the deck, 2026-08-17 ----------------------------------------------------
    # Two laws earned in one afternoon by spec-studio's one-card redesign: each is a
    # defect the owner caught on their own screen within minutes of the deploy.

    _law(
        "type-stays-legible",
        "No text ships below the platform's legibility floor",
        Quantity(value=1, unit="law", provenance="asserted; authority known, text not "
                 "yet captured", grounded=False,
                 source="Apple's Human Interface Guidelines (Typography) state a "
                        "minimum around 11 points for phone text; the HIG renders "
                        "through script and the verbatim sentence has not been "
                        "captured. Capture it and promote, or find a quotable floor."),
        falsifier="Measure the smallest computed font size on a phone screen: a "
                  "rendered string below about 11px/11pt. A measurement, not a "
                  "judgement — the chip that fails is found by a style audit, not by "
                  "squinting.",
        triggers=["the app is used on a phone",
                  "a status chip, badge, overline, or caption is styled"],
        sightings=[("spec-studio sheet v2, 2026-08-17",
                    "the status chip shipped at 9px and the group overline at 10px. "
                    "The previous design's label 'took too much space'; the correction "
                    "overshot straight through the floor — 'the tiny fonts are "
                    "ridiculous'. Fixing one extreme by shipping the other is the "
                    "shape of the defect; the floor is what stops the pendulum.")],
        note="The ceiling complaint (a label eating the screen) and the floor "
             "complaint (a chip nobody can read) are the same missing constraint "
             "stated from opposite ends.",
    ),

    _law(
        "controls-sit-where-the-gesture-goes",
        "A gesture's on-screen alternative sits on the side the gesture ends",
        _cited("Nielsen Norman Group, Natural Mappings and Stimulus-Response "
               "Compatibility in User Interface Design"),
        falsifier="Perform the gesture and read the buttons: the swipe that commits an "
                  "action travels toward one side while the button naming that action "
                  "sits on the other — swiping right keeps, but keep is the left-hand "
                  "button.",
        triggers=["a gesture and a visible control operate the same function"],
        citations=[("NN/g — Natural Mappings and Stimulus-Response Compatibility",
                    "https://www.nngroup.com/articles/natural-mappings/",
                    "a design in which the system's controls represent or correspond "
                    "to the desired outcome"),
                   ("NN/g — Natural Mappings and Stimulus-Response Compatibility",
                    "https://www.nngroup.com/articles/natural-mappings/",
                    "When controls map to the actions that will result, systems are "
                    "faster to learn and easier to remember.")],
        sightings=[("spec-studio sheet v2, 2026-08-17",
                    "swipe right = keep and swipe left = drop, while the buttons "
                    "rendered keep on the left and drop on the right. Each half "
                    "followed its own convention (swipe from card decks, buttons from "
                    "affirmative-first ordering) and together they pointed a user's "
                    "muscle memory at the destructive verb.")],
    ),

    # A third law stood in that section — a-ui-change-is-not-done-until-someone-has-
    # looked — and was folded into done-is-observed-where-the-user-stands
    # (practice.py) when the laws were audited against the generalization bar: it was
    # that law specialized to UI changes, misfiled among the laws about screens, and
    # carried as uncited red while its twin held the Agans citation. Its sighting
    # travelled with it.

    _law(
        "a-view-arrives-whole",
        "What a host fetches to show is the whole view, not a stub that fetches the rest",
        Quantity(value=1, unit="law", provenance="asserted; the norm is practised "
                 "widely, no authority stating it has been captured", grounded=False,
                 source="The proposition is recognizable wherever views are delivered "
                        "into a host someone else controls — mail clients strip "
                        "scripts, AMP forbids author JavaScript outright — but no "
                        "captured text STATES the norm. CSP3 was cited here once; it "
                        "documents the mechanism that punishes the stub, not the rule, "
                        "and a citation that says something adjacent is decoration "
                        "(what-accompanies-a-claim-supports-it, applied to this file). "
                        "Find a source that says it, or this stays honest red."),
        falsifier="Load the view in its real sandbox: styles and markup appear, "
                  "behaviour does not — an empty frame in the shape of the real one. "
                  "The tell is a runtime-created <script> that never executes and "
                  "raises nothing the page can catch.",
        triggers=["a view is delivered into a sandbox somebody else controls",
                  "a page builds part of itself after loading"],
        sightings=[("spec-studio sheet, 2026-08-17",
                    "the card's resource was a bootstrap that called a tool for the "
                    "real widget and injected it. It fetched, it ran, it called the "
                    "tool twice — and the founder got a card-shaped empty box. The "
                    "served document's inline script was permitted; the script node "
                    "the stub created was not, so markup and styles landed and the "
                    "behaviour was dropped in silence. The stub existed to defeat a "
                    "cache that a content-hashed URI defeats natively.")],
        note="A stub is a second round-trip and a second trust decision, bought to "
             "solve a caching problem that a content-addressed name solves without "
             "either. The environment evidence, kept as evidence and not as authority: "
             "CSP3 §6.1 script-src ('The script-src directive restricts the locations "
             "from which scripts may be executed', w3.org/TR/CSP3) is why the stub's "
             "injected script died silently — the mechanism, not the norm.",
    ),

    _law(
        "yesterdays-names-keep-answering",
        "A name once served keeps answering, whatever today's name is",
        _cited("Hyrum Wright, Hyrum's Law"),
        falsifier="Rename or remove a served name — a tool, a route, a resource URI — "
                  "and drive a client that holds the old catalogue: 'Unknown tool', a "
                  "404, or a dead widget where the same request answered yesterday.",
        triggers=["a served name changes", "any client caches the catalogue of names"],
        citations=[("Hyrum's Law", "https://www.hyrumslaw.com/",
                    "With a sufficient number of users of an API, it does not matter "
                    "what you promise in the contract: all observable behaviors of "
                    "your system will be depended on by somebody.")],
        sightings=[("spec-studio, 2026-08-17",
                    "project_card was renamed project_deck to bust a platform cache "
                    "and the old name was pruned in the same deploy — the founder's "
                    "phone, holding the cached registry, got 'Unknown tool' where the "
                    "sheet had answered an hour earlier. The repo already carried this "
                    "rule for resource URIs, in a comment beside SHEET_URIS_PRIOR: "
                    "'never prune a name a client may still hold'. It was broken the "
                    "same afternoon for tool names — a rule stated for one kind of "
                    "name is not yet a rule.")],
        note="A rename busts a cache only where the client re-lists; everywhere else "
             "it is an outage. Serve both names until no client can hold the old one, "
             "which for an unexpirable cache means indefinitely.",
    ),

    _law(
        "no-element-covers-another",
        "No element a person must read or press is covered by another — two rendered "
        "rectangles intersect only where one is declared the other's ground",
        _uncited(),
        falsifier="A close control rendered on top of a title: the title unreadable, "
                  "part of what lies under both unreachable. Measurable: two "
                  "elements' rects intersect and neither declares the other its "
                  "ground (a sheet over a dimmed page, a menu over what opened it "
                  "are declared coverings, not breaches).",
        triggers=["any interface at all"],
        sightings=[("spec-studio, 2026-08-17 (xag/spec-studio#13)",
                    "The expanded view rendered its close button on top of its "
                    "title — the title unreadable and part of what sat under both "
                    "unreachable — while every layout check passed, because each "
                    "checks one element against one box and overlap is a relation "
                    "between two.")],
        note="Nearest stated kin: WCAG 2.2 SC 2.4.11 (a focused component not "
             "entirely hidden by author content) and SC 1.4.10 (no loss under "
             "reflow) — each asserts a corner of this, neither the law itself, so "
             "it stands uncited rather than wearing a citation that says something "
             "adjacent. The mechanical route is the layout solver's own class: a "
             "pairwise intersection test over measured rects, endpoint-exact "
             "across the viewport interval, refusing on anything unmeasured — plus "
             "one new fact, the declared ground.",
    ),

    _law(
        "the-answers-span-the-question",
        "The answers a surface offers span the answers its question admits",
        _cited("Krosnick & Presser, Question and Questionnaire Design "
               "(Handbook of Survey Research, 2010)"),
        falsifier="A question posed beside a fixed answer set that cannot express "
                  "an answer the question itself invites — the person is made to "
                  "pick a word that answers something else, and the record shows a "
                  "choice nobody made.",
        triggers=["any interface that asks the user a question with a fixed "
                  "answer set",
                  "one verdict vocabulary is reused across rows that ask "
                  "different questions"],
        citations=[("Krosnick & Presser — Question and Questionnaire Design, "
                    "Handbook of Survey Research (2010), ch. 9",
                    "https://web.stanford.edu/dept/communication/faculty/krosnick/"
                    "docs/2010/2010%20Handbook%20of%20Survey%20Research.pdf",
                    "Make response options exhaustive and mutually exclusive")],
        sightings=[("spec-studio, 2026-08-18 (xag/spec-studio#14)",
                    "A judgment row carried a genuine open question in its text "
                    "and declared no answer set, so it fell back to the sheet's "
                    "default keep/drop — neither word answers it. Sibling rows on "
                    "the same sheet carried their own three-word vocabulary, proof "
                    "the row-specific set exists and this row simply never "
                    "declared one.")],
        note="Survey methodology is the discipline that studies closed questions, "
             "and it is this law's root — a new lane in docs/sources.md. The "
             "route is hybrid: the declared answer set is structural (the offered "
             "options are data), whether it spans the question's own text is one "
             "reading per question — the radar pattern.",
    ),

    _law(
        "commit-is-a-bare-verb",
        "A control that commits, creates or destroys is labelled with its verb — a "
        "real object may follow, an object pronoun may not",
        _cited("UK Parliament Design System, Button — the verb half; the "
               "no-object-pronoun refinement is this package's, from the sighting"),
        falsifier="A commit control whose label is a verb plus a pronoun standing "
                  "for the thing on the sheet («Make it», «Save it», «Take it "
                  "off») where the bare verb — Save, Create, Remove — is what a "
                  "person would say.",
        triggers=["any interface with a control that commits something"],
        citations=[("UK Parliament Design System — Button",
                    "https://designsystem.parliament.uk/components/button/",
                    "Start button text with a verb (an action), for example, "
                    "‘Save and continue’.")],
        sightings=[("chores, 2026-08-18 (xag/craft-laws#11)",
                    "The create-a-household form commits with «Make it» and the "
                    "edit sheet's remove control reads «Take it off». Both reached "
                    "the judgment surface only as by-products of other findings — "
                    "the wording itself was never the complaint, and would have "
                    "survived a fix to either.")],
        note="A verb with a real object — «Add a person», «Take a turn» — passes: "
             "the defect is the pronoun, which names nothing its reader can "
             "check. French wants the same bare form (Enregistrer, Créer, "
             "Supprimer — never «Fais-le»), and its object clitics attach by "
             "hyphen, which is what a decider should key on there. Decidable "
             "from the label and the control's role alone — the lexicon family, "
             "beside ellipsis-promises-more-input.",
    ),

]

# What the laws are allowed to travel through. Ungrounded authority — an uncited law — will not
# pass, because `nothing-unsound-passes-a-gate` (shipped by `ledger`) counts it.
GATE = Node(
    id="publish",
    kind="gate",
    name="What may be relied on as a law",
    payload={
        "note": "Red, and correctly so: the check names every law that cites nobody, and "
                "counts them itself (this note once said 'three' and went stale the day a "
                "fourth arrived — counts-are-computed was minted on exactly that defect). "
                "They are carried on purpose and they are visible — which is the whole "
                "difference between this and the markdown file it replaced, where the same "
                "laws sat in a sentence that was true and could not fire. Discharge by "
                "finding the source, or by deleting the law. Never by editing this file.",
    },
    links={"admits": [law.id for law in LAWS]},
)
