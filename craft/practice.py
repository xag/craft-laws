"""Laws about the WORK, not about the interface. Same shape, different subject.

`laws.py` convicts a screen; these convict a way of working. They are here rather than
in a skill because a skill is a procedure — do this, then that — and a procedure cannot
go red. A law carries a falsifier, so a claim like "it is done" becomes a thing that can
be checked against the record instead of believed.

They were all earned on 2026-08-17, in one session, by one defect: a card that rendered
as an empty rectangle on the founder's phone. Fifteen times the work was declared
finished; fifteen times the founder answered that it was not. The failure was never one
bug — a stale cached widget, a CSP-blocked injected script, a tool renamed out from
under a cached registry, an oversized payload, and underneath them a host that never
pushes tool results — and every one of them drew the SAME blank box. What made it a
nine-hour day was not the bugs. It was the method: claiming done from the producer's
side, theorizing where an instrument would have answered, shipping several candidate
fixes in one deploy, and spending the founder's attention as the test harness.

Agans' nine rules name four of these exactly, which is why they are cited rather than
asserted: this is a well-known way to fail, written down in 2002, and we did it anyway.
"""

from __future__ import annotations

from quern import Node
from quern.provenance import Quantity

from .laws import _cited, _law, _uncited

PARNAS = ("David L. Parnas, On the Criteria To Be Used in Decomposing Systems into "
          "Modules, Communications of the ACM 15(12), 1053-1058, 1972")
PARNAS_URL = ("https://www.win.tue.nl/~wstomv/edu/2ip30/references/"
              "criteria_for_modularization.pdf")

EXISTENCE_BIAS = ("Eidelman, Crandall & Pattershall, The existence bias, Journal "
                  "of Personality and Social Psychology 97(5), 765-775, 2009")
EXISTENCE_URL = "https://doi.org/10.1037/a0017058"

IPCC = ("IPCC, Guidance Note for Lead Authors of the Fifth Assessment Report "
        "on Consistent Treatment of Uncertainties (Mastrandrea et al., 2010)")
IPCC_URL = ("https://www.ipcc.ch/site/assets/uploads/2017/08/"
            "AR5_Uncertainty_Guidance_Note.pdf")

AGANS = ("David J. Agans, Debugging: The 9 Indispensable Rules for Finding Even the "
         "Most Elusive Software and Hardware Problems")
AGANS_URL = "https://debuggingrules.com/"

STARD = ("Cohen et al., STARD 2015 guidelines for reporting diagnostic accuracy "
         "studies: explanation and elaboration, BMJ Open 6:e012799, item 19")
STARD_URL = "https://doi.org/10.1136/bmjopen-2016-012799"

CONSORT = ("CONSORT 2025 statement: updated guideline for reporting randomised "
           "trials, BMJ 2025;388:e081123")
CONSORT_URL = "https://doi.org/10.1136/bmj-2024-081123"

ARRIVE = ("Percie du Sert et al., The ARRIVE guidelines 2.0: updated guidelines "
          "for reporting animal research, PLOS Biology 2020")
ARRIVE_URL = "https://doi.org/10.1371/journal.pbio.3000410"

TK1974 = ("Tversky & Kahneman, Judgment under Uncertainty: Heuristics and "
          "Biases, Science 185:1124-1131, 1974")
TK1974_URL = "https://doi.org/10.1126/science.185.4157.1124"

PRISMA = ("Page et al., The PRISMA 2020 statement: an updated guideline for "
          "reporting systematic reviews, BMJ 2021;372:n71")
PRISMA_URL = "https://doi.org/10.1136/bmj.n71"

SPIRIT = ("Chan et al., SPIRIT 2025 statement: updated guideline for protocols of "
          "randomised trials, PLOS Medicine 2025;22:e1004589")
SPIRIT_URL = "https://doi.org/10.1371/journal.pmed.1004589"


def _agans(rule: str) -> Quantity:
    return Quantity(value=1, unit="law", provenance="cited", grounded=True,
                    source=f"{AGANS}, rule '{rule}'")


PRACTICE = [

    _law(
        "done-is-observed-where-the-user-stands",
        "Work is finished when the thing the user touches has been observed to work, "
        "never when the thing you control has been observed to ship",
        _agans("If you didn't fix it, it ain't fixed"),
        falsifier="Read the claim of completion and list its evidence. Every item is "
                  "producer-side — a green suite, a deploy id, a log line, a file on "
                  "the machine — and none is an observation of the surface the user "
                  "actually meets.",
        triggers=["anything is reported as done", "a fix is deployed"],
        citations=[(f"{AGANS} — rule 9",
                    AGANS_URL,
                    "If you didn't fix it, it ain't fixed")],
        sightings=[("spec-studio, 2026-08-17",
                    "fifteen rounds of 'deployed and verified' against a founder "
                    "answering 'still nothing'. Every verification was real and every "
                    "one was on the producing side: tests green, machine carrying the "
                    "file, OAuth door answering, CI passing. The card on the phone was "
                    "never once observed until the founder said 'you really won't test "
                    "what you do'."),
                   ("spec-studio sheet, 2026-08-17 — the UI-change case",
                    "the same day, the same failure at a finer grain: every claim "
                    "about the redesigned card rested on green tests, and the widget "
                    "was never rendered once. The first actual render found, in one "
                    "look, two defects no test could state — an authored example set "
                    "in monospace, so a sentence read as code, and the swipe hint "
                    "placed below the quiet links, furthest from the card it explains. "
                    "Both had been 'verified' for hours. A law was minted for this "
                    "('a-ui-change-is-not-done-until-someone-has-looked') and folded "
                    "back here: it was this law, applied to interface changes.")],
        note="The corollary is what makes it actionable: if the user's surface cannot "
             "be observed from here, say so in the same breath as the claim, and name "
             "what WAS observed instead. 'Deployed; I cannot see the phone' is honest. "
             "'Deployed and verified' is not. For anything a person will look at, the "
             "observation is a rendered picture somebody read — a test says the wiring "
             "holds, a picture says whether anyone can read it, and the second "
             "question is the product.",
    ),

    _law(
        "make-it-fail-before-you-fix-it",
        "A fix is preceded by a reproduction of the failure that the fix then turns "
        "green",
        _agans("Make it fail"),
        falsifier="Ask which run showed the defect BEFORE the change. There is none: "
                  "the failure was only ever seen on the user's screen, and the fix "
                  "was reasoned from a description of it.",
        triggers=["a defect is reported", "a change is made in order to fix something"],
        citations=[(f"{AGANS} — rule 2", AGANS_URL, "Make it fail"),
                   (f"{AGANS} — rule 2, expanded", AGANS_URL,
                    "Stimulate the failure, don't simulate the failure")],
        sightings=[("spec-studio, 2026-08-17",
                    "five fixes shipped against an empty card that had never been "
                    "reproduced anywhere but on the founder's phone. The first "
                    "reproduction — a jsdom host with no payload — was written after "
                    "the fifth fix, and it turned the defect into two seconds of "
                    "work.")],
    ),

    _law(
        "instrument-before-the-second-theory",
        "Two consecutive explanations for one failure, with no new observation "
        "between them, means the next act is an instrument and not a third "
        "explanation",
        _agans("Quit thinking and look"),
        falsifier="Count the hypotheses offered about one failure and the "
                  "observations added between them. Two or more explanations, zero "
                  "new signals.",
        triggers=["a failure resists the first fix",
                  "two possible causes produce the same symptom"],
        citations=[(f"{AGANS} — rule 3", AGANS_URL, "Quit thinking and look"),
                   (f"{AGANS} — rule 3, expanded", AGANS_URL,
                    "Build instrumentation in")],
        sightings=[("spec-studio, 2026-08-17",
                    "four hours of cache theories — connector cache, HTML cache, tool "
                    "list, URI naming — each plausible, none checkable, because a dead "
                    "script and a missing payload draw the identical blank box. One "
                    "beacon ('the script ran'; 'no payload came') settled it in two "
                    "log lines. The estate's own flight-recorder doctrine says exactly "
                    "this and it was not applied at the one boundary that mattered."),
                   ("spec-studio, 2026-08-18",
                    "the founder reported a card whose sentence the server no longer "
                    "served, and the reply was a live re-fetch plus a theory about "
                    "whose screen was stale — while the recorder, armed on this server "
                    "since day one, held every deck fetch WITH the payload served. The "
                    "founder asked one question — 'did you use flight recorder?' — and "
                    "the tape then answered in one read what the theory had spent the "
                    "founder's patience asserting: old sentence served through 15:22, "
                    "new from 15:35. The instrument existed, was running, and was not "
                    "consulted; that is a grade below not building one.")],
        note="The tell is symptom collision: when two very different faults produce "
             "one picture, no amount of reasoning separates them and one cheap signal "
             "does.",
    ),

    _law(
        "one-candidate-fix-per-deploy",
        "A release carries one candidate fix for a given failure, so that its outcome "
        "names a cause",
        _agans("Change one thing at a time"),
        falsifier="A single deploy carrying two or more independent attempts at the "
                  "same symptom. Whatever happens next, no attempt is confirmed or "
                  "refuted by it.",
        triggers=["a failure is being chased", "more than one plausible cause is open"],
        citations=[(f"{AGANS} — rule 5", AGANS_URL, "Change one thing at a time"),
                   (f"{AGANS} — rule 5, expanded", AGANS_URL, "Isolate the key factor")],
        sightings=[("spec-studio, 2026-08-17",
                    "one deploy carried a content-hashed URI, a renamed tool and a "
                    "reshaped meta block — three theories at once. It failed, and the "
                    "failure taught nothing about any of them; worse, the rename broke "
                    "a working call for clients holding the old name, so the round "
                    "cost a regression as well as an answer.")],
    ),

    _law(
        "the-users-attention-is-not-a-test-harness",
        "A check the author can run is never delegated to the person waiting for the "
        "work",
        _uncited(),
        falsifier="An exchange whose ask is 'try it and tell me what you see' for "
                  "something the author had the means to observe — a request that "
                  "spends the user's turn to learn what a script would have said.",
        triggers=["a fix is ready and its effect is unknown",
                  "the author cannot see the user's surface"],
        sightings=[("spec-studio, 2026-08-17",
                    "'open a new conversation and tell me', repeatedly, for a whole "
                    "afternoon — while the connector's own resource and payload were "
                    "readable from the author's session all along, and a browser was "
                    "installed on the same machine. The founder: 'are you asking me to "
                    "check again?'")],
        note="When the user's surface genuinely cannot be reached, the move is to "
             "build the closest faithful stand-in (their real payload, their real "
             "artifact, a real browser) and say plainly which last mile remains "
             "unobserved.",
    ),

    _law(
        "a-detour-is-announced-as-a-detour",
        "Routing around a broken thing is never reported as fixing it",
        _uncited(),
        falsifier="The thing the user reported is still broken, and the reply offers "
                  "a different route — a second endpoint, another surface, a manual "
                  "step — as the resolution.",
        triggers=["the reported failure resists", "a workaround exists"],
        sightings=[("spec-studio, 2026-08-17",
                    "a second MCP endpoint and then a whole browser deck were built "
                    "and offered while the MCP app itself stayed broken. Both were "
                    "sound work and neither was the ask: 'you can't just create a new "
                    "app', and later 'not the widget, the MCP app'.")],
        note="A detour is often the right thing to BUILD — the browser deck earned its "
             "place and carried the founder's first rulings. The defect is calling it "
             "the answer, because that ends the hunt for the cause while the cause is "
             "still there.",
    ),

    # --- earned 2026-08-20, in one session, by one habit: a job left half done and
    # --- reported as a choice. Three faces of it. All three are UNMECHANIZED: the word
    # --- lists that used to check them were removed 2026-08-22 (see craft/claims.py).
    _law(
        "deliberate-names-its-decision",
        "A state called deliberate, by design or on purpose names where the decision "
        "was made",
        _uncited(),
        falsifier="A report or claim that calls some state deliberate, intentional, by "
                  "design or on purpose, with no pointer to the ledger entry, issue or "
                  "commit in which anyone decided it.",
        triggers=["a gap, omission or limit is being explained",
                  "the explanation uses a word of intent"],
        sightings=[("a verification substrate and its first adopter, 2026-08-20",
                    "'the app deliberately ships without the library' — quoted from a "
                    "pyproject comment dated 2026-07-17 that called the dependency private. "
                    "Every repo involved had been public for weeks; nobody had decided "
                    "anything. A whole seam (a declaration table beside the code, instead "
                    "of at the emission site) was then designed around the word.")],
        note="The word 'deliberate' ends an inquiry: a reader stops asking why. So it "
             "has to be earned by a pointer, the way a citation earns 'cited'. A state "
             "nobody decided is an accident, and an accident is allowed to be fixed.",
    ),

    _law(
        "a-remainder-names-its-debt",
        "What a done-claim leaves undone is carried by a debt it names, never by a "
        "sentence",
        _uncited(),
        falsifier="A done-claim whose evidence gap, or whose report, says that some part "
                  "is later, next, not yet, deferred, owed or blocked, with no debt entry "
                  "that carries it — so the remainder lives only in the scrollback and is "
                  "gone the moment the conversation moves.",
        triggers=["a done-claim is made", "part of the ask was not delivered"],
        sightings=[("a verification substrate, 2026-08-20",
                    "four of nine law families 'carried as a named debt' — the debt was "
                    "real and in the ledger; the abstraction function, which the census's "
                    "own source ranks as the most effective family, was left out of both "
                    "the census and the debt and called 'a complement, later' in prose. "
                    "Nothing red anywhere pointed at it.")],
        note="A debt in a ledger is red-able: a rule can ask whether it still stands, a "
             "brief lists it, a discharge condition names what ends it. A remainder in "
             "prose is none of those. Nothing checks this one: the pointer is asked "
             "for by a reader, because the only mechanism tried was a word list.",
    ),

    _law(
        "a-census-is-read-from-its-source",
        "A catalogue that claims to enumerate a source carries every item the source "
        "lists, each covered or owed, and its count is computed from that list",
        _cited("PRISMA 2020, items 5, 6 and 16b: the systematic-review "
               "community's statement of the census discipline"),
        falsifier="A catalogue stated as 'the N families/laws/items of <source>' where the "
                  "source, read in full, lists an item the catalogue neither carries nor "
                  "names as owed — an enumeration filtered by what was feasible to build.",
        triggers=["a catalogue or census is authored from a cited source",
                  "a count of families, laws or items is stated"],
        citations=[(PRISMA + ", item 6", PRISMA_URL,
                    "Specify all databases, registers, websites, organisations, "
                    "reference lists and other sources searched or consulted."),
                   (PRISMA + ", item 5", PRISMA_URL,
                    "Specify the inclusion and exclusion criteria for the review "
                    "and how studies were grouped for the syntheses."),
                   (PRISMA + ", item 16b", PRISMA_URL,
                    "Cite studies that might appear to meet the inclusion "
                    "criteria, but which were excluded, and explain why.")],
        sightings=[("a behavior-law catalogue, 2026-08-20",
                    "'nine families, a census folded from Hughes's five approaches': the "
                    "paper's model-based properties — which it says 'together form a "
                    "complete specification' and rank first for bugs found — were folded "
                    "into nothing, and every family kept was weakened from a value "
                    "comparison to a presence check. The count 9 was grounded on the "
                    "length of the catalogue, i.e. on itself.")],
        note="The harness is a census node beside the catalogue: one entry per item the "
             "source lists, linking to the law that covers it or the debt that owes it, "
             "with the counts computed over the entries — so the number on the brief is "
             "the source's, and what was left out is a number too. Uncited from its "
             "minting on 2026-08-20 until 2026-08-24, when censusing PRISMA found the "
             "systematic-review community stating the same discipline item by item — "
             "the law that drove every census was rooted BY one, which is the loop "
             "closing in the right direction.",
    ),

    # --- earned 2026-08-22, in one session, by one habit with two faces: a qualifier
    # --- attached to something already checked, and the same modesty offered as deference.
    # --- Sourced rather than asserted: the IPCC's guidance note exists to stop an author
    # --- picking a confidence term the evidence does not license, and says so in a
    # --- sentence. docs/practice-sources.md censuses that note whole - 21 items, 3
    # --- covered, 8 owed, 10 set aside - so what it does NOT cover is a number too.
    _law(
        "a-qualifier-is-licensed-by-the-evidence",
        "A finding the evidence settles is stated as fact; a hedge is licensed by a named "
        "unknown, never by modesty",
        _cited(IPCC),
        falsifier="A statement qualified - weaker evidence, may, might, arguably, in "
                  "principle - about something the same piece of work established: a "
                  "command was run, an artifact was read, a check was made, and the result "
                  "of THAT is then reported with a qualifier attached to it.",
        triggers=["a claim is made about something the same session checked",
                  "a result is reported to somebody who will act on it"],
        citations=[(IPCC + ", paragraph 5", IPCC_URL,
                    "Consider that, in some cases, it may be appropriate to describe "
                    "findings for which evidence and understanding are overwhelming as "
                    "statements of fact without using uncertainty qualifiers."),
                   (IPCC + ", paragraph 6", IPCC_URL,
                    "Consider all plausible sources of uncertainty. Experts tend to "
                    "underestimate structural uncertainty arising from incomplete "
                    "understanding of or competing conceptual frameworks for relevant "
                    "systems and processes."),
                   (IPCC + ", paragraph 10", IPCC_URL,
                    "“About as likely as not” should not be used to express a lack of "
                    "knowledge."),
                   (IPCC + ", paragraph 2", IPCC_URL,
                    "Be prepared to make expert judgments in developing key findings, and "
                    "to explain those judgments by providing a traceable account: a "
                    "description in the chapter text of your evaluation of the type, "
                    "amount, quality, and consistency of evidence and the degree of "
                    "agreement, which together form the basis for a given key finding.")],
        sightings=[("a test suite parallelised, 2026-08-22",
                    "the suite's isolation was read out of its fixtures and confirmed by a "
                    "green run, and the parallel result was then reported as 'weaker "
                    "evidence than a green serial one' - a qualifier on the one thing that "
                    "had actually been checked. It reached a commit message, an app's "
                    "ledger and its CI config before a person said 'you keep insisting "
                    "parallel is not decisive'.")],
        note="It cuts both ways, and the second citation is why: the same note that says "
             "drop the qualifier when the evidence is overwhelming says experts "
             "underestimate what they do not understand. The law is not 'sound confident'. "
             "It is that a hedge must be licensed by an unknown somebody can name - and if "
             "one can be named, the honest sentence names it instead of hedging the whole "
             "claim, which is the third citation's point about a term standing in for a "
             "lack of knowledge. Understating is not the safe direction; it is the "
             "direction that wears modesty and so goes uncorrected. The fourth citation "
             "is the AGREEMENT face, added 2026-08-24: an unqualified assent is the "
             "highest confidence term there is, and paragraph 2 demands the same "
             "traceable account for it as for any finding — the confirmation kind in "
             "the claims record is that account as data, and its decider convicts the "
             "agreement that carries none.",
    ),

    # --- earned 2026-08-22, by defending two existing names against a proposed one on
    # --- the ground that they had "earned" their obscurity. One had: epure's ledger holds
    # --- the-name-is-the-drawing with two alternatives rejected. The other had not - quern
    # --- carries 21 decisions and not one of them is about its name. The justification was
    # --- read off the fact that the names exist, and half of it was invented.
    _law(
        "what-exists-is-not-thereby-chosen",
        "An existing state is called deliberate only where the decision that made it can be "
        "produced; existence, age and prevalence are not evidence that anybody chose",
        _cited(EXISTENCE_BIAS),
        falsifier="An existing thing defended or explained by its being there - it works, it "
                  "has always been so, it earned its place, it is what we do - where no "
                  "decision naming it can be produced, and a proposed alternative is judged "
                  "against it on that footing.",
        triggers=["an existing thing is weighed against a proposal",
                  "a state is called deliberate, by design, earned or considered",
                  "a convention is explained rather than looked up"],
        citations=[(EXISTENCE_BIAS, EXISTENCE_URL,
                    "The authors demonstrate that people treat the mere existence of "
                    "something as evidence of its goodness."),
                   (EXISTENCE_BIAS + ", Study 4", EXISTENCE_URL,
                    "the more a form is described as prevalent, the more aesthetically "
                    "attractive is that form. This indicates a causal relationship between "
                    "aesthetic judgments and existence in a domain lacking choice among "
                    "alternatives."),
                   (EXISTENCE_BIAS + ", conclusion", EXISTENCE_URL,
                    "mere existence leads to assumptions of goodness; the status quo is seen "
                    "as good, right, attractive, tasty, and desirable.")],
        sightings=[("this estate's own names, 2026-08-22",
                    "a proposed project name was rejected against two incumbents on the "
                    "ground that theirs 'earn their obscurity' because the metaphors do "
                    "explanatory work. Checked afterwards: epure's ledger holds a naming "
                    "decision with two rejected alternatives, and quern's holds 21 decisions "
                    "of which none is about its name. Half the justification was read off "
                    "the fact that the name exists - which is Study 4's finding about "
                    "aesthetic judgment where no choice among alternatives was made.")],
        note="The sibling of [[deliberate-names-its-decision]], and the harder direction. "
             "That law catches CALLING a state deliberate without naming the decision; this "
             "catches INFERRING that it was, which needs no words at all and so leaves no "
             "sentence to convict. It is not an argument for change: Chesterton's fence "
             "warns against removing what you have not understood, and both cautions have "
             "the same discharge - go and find the decision. Its absence is not permission "
             "to tear the thing down; it is information, and usually the most useful thing "
             "you will learn that day.",
    ),

    # --- earned 2026-08-22, by building a law-checker inside the project whose own first
    # --- decision says it holds pointers, an ordering and hypotheses and no copy of what
    # --- another ledger says. The misplacement then forced every ugly part of it.
    _law(
        "a-thing-is-built-where-its-subject-lives",
        "Work goes where the decisions it depends on already live; a piece built away from "
        "its subject pays for the distance in couplings that should not exist",
        _cited(PARNAS),
        falsifier="A module, file or feature added to a project whose stated purpose does "
                  "not admit it - and the tell is the workaround it needs: a hand-copy of "
                  "something another repository owns, a shell-out to read what an import "
                  "would have given, a dependency that cannot be taken because the two "
                  "homes disagree.",
        triggers=["something is added to a project that already states what it is for",
                  "a new piece needs data another project owns",
                  "an interface between two parts is turning out awkward"],
        citations=[(PARNAS, PARNAS_URL,
                    "We propose instead that one begins with a list of difficult design "
                    "decisions or design decisions which are likely to change. Each module "
                    "is then designed to hide such a decision from the others."),
                   (PARNAS + ", on the wrong criterion", PARNAS_URL,
                    "it is almost always incorrect to begin the decomposition of a system "
                    "into modules on the basis of a flowchart")],
        sightings=[("quality-harness, 2026-08-22",
                    "a checker holding written answers to craft laws was built inside the "
                    "project for pointers, ordering and hypotheses - whose founding decision "
                    "reads 'no copy of anything another ledger already says'. It immediately "
                    "needed a hand-copied list of 24 law ids and a subprocess to read "
                    "craft-laws from another virtualenv, because the two pin different "
                    "revisions of a shared dependency and the import was impossible. Both "
                    "workarounds were the misplacement announcing itself.")],
        note="Parnas's criterion is about which DECISION a module hides, and it reads across "
             "to repositories without stretching: a checker's reason to change is the laws, "
             "so it belongs with the laws. The practical value is the TELL rather than the "
             "principle - nobody notices they are in the wrong place, and everybody notices "
             "a hand-copy or a shell-out. Treat those as evidence about location, not as "
             "problems to solve where they appear. Symmetric with "
             "[[what-exists-is-not-thereby-chosen]]: there the question is whether a state "
             "was chosen, here whether a project's stated purpose was READ before something "
             "was added to it. Both are answered by opening the record.",
    ),
    # --- earned 2026-08-24, by a reading that reported itself as selective and was total.
    # --- Rooted rather than asserted: reporting standards for diagnostic accuracy exist
    # --- because a proportion is only as good as the set it was taken over, and STARD's
    # --- flow-diagram item says so in a sentence.
    _law(
        "a-rate-names-the-population-it-was-computed-over",
        "A rate is stated over the set the measurement could actually reach, and names "
        "that set beside the number",
        _cited("STARD 2015, item 19 and its explanation: a flow diagram exists so a "
               "reader can find the correct denominator"),
        falsifier="A rate, share or coverage figure whose denominator includes items the "
                  "measurement could never have counted in the numerator. Countable: "
                  "compare the stated denominator against the set the measurement can "
                  "reach, and a gap between them is the breach.",
        triggers=["a rate, share, coverage or hit count is reported",
                  "a check reports how much of something it found"],
        citations=[(STARD, STARD_URL,
                    "By providing the exact number of participants at each stage of the "
                    "study, including the number of true-positive, false-positive, "
                    "true-negative and false-negative index test results, the diagram "
                    "also helps identifying the correct denominator for calculating "
                    "proportions")],
        sightings=[
            ("an argument reading over five ledgers, 2026-08-24",
             "A check for claims argued only by attacking their alternatives reported "
             "4 of 16 arguments here and 19 of 96 in another ledger. Both read as "
             "selective. Counted over the set the check can reach - entries that attack "
             "something, which is entries that HAVE an alternative - it was 4 of 4 and "
             "19 of 19. The denominator was inflated by nodes the check could never "
             "convict, and 100% of the eligible population was reported as 25% of the "
             "graph. A structural fact passed for a finding, and the fix was one line "
             "of arithmetic, not one line of reasoning."),
        ],
        note="The remedy is the source's: state the set beside the number. STARD asks "
             "for a diagram because the reader cannot otherwise tell which patients were "
             "eligible; a check that prints '4 findings' owes the same - 4 of how many "
             "it could have found. Where the two differ the check is measuring itself, "
             "and that is worth reporting rather than hiding, because a check that "
             "convicts most of what it can reach has found a missing input and not a "
             "defect.",
    ),
    # --- earned 2026-08-23/24, twice in one week, by a lane that reported clean over text
    # --- it had never read. Rooted in the same source as the rate law and its neighbouring
    # --- item: STARD asks what happened to the results a test could not call, because
    # --- ignoring them biases the estimate whenever they are not a random slice.
    _law(
        "a-check-reports-what-it-could-not-judge",
        "A check reports how much of its input it did not examine, and why, beside what "
        "it found",
        _cited("STARD 2015, item 15: how indeterminate results were handled, reported "
               "with their frequencies and their reasons"),
        falsifier="A report of findings from a check that left part of its input "
                  "unexamined without saying how much. Countable: the units its "
                  "reading of the input produced, against the units it actually "
                  "tested.",
        triggers=["a check reports findings over a corpus",
                  "a report of no findings is made"],
        citations=[(STARD, STARD_URL,
                    "authors are encouraged to always report the respective frequencies "
                    "with reasons, as well as failures to complete the testing "
                    "procedure ... Ignoring indeterminate test results can produce "
                    "biased estimates of accuracy, if these results do not occur at "
                    "random")],
        sightings=[
            ("the prose lane, 2026-08-23",
             "The non-prose test matched any line beginning with an asterisk, so every "
             "paragraph opening in bold left the lane untested - eight of "
             "twenty-nine in one README. The lane reported 'no prose decider convicts'. "
             "The skipped eight were not a random slice: they were the bold-led ones, "
             "which is to say the ones carrying the argument, which is the exact "
             "condition the source names as biasing."),
            ("an argument reader over five ledgers, 2026-08-23",
             "project() skips every node kind it does not understand, by design and for "
             "a good reason - inventing an argument for a node nobody wrote would put "
             "findings in the report that no ledger asserted. It said so in a docstring "
             "and never in a report, so a reader saw the findings and not the share of "
             "the tree they were drawn from."),
        ],
        note="Two readings of the same demand, and only the weaker one is bookkeeping. "
             "The weak reading is a coverage figure beside the findings. The strong one "
             "is the source's: what a check cannot judge is rarely a random slice of "
             "what it reads, so the share it skipped predicts the direction of its bias "
             "and not merely its size. A prose lane that drops bold-led paragraphs drops "
             "the paragraphs that open arguments; a projection that skips unknown kinds "
             "skips whatever the vocabulary has not caught up with. The frequency is the "
             "cheap half and the REASON is the half worth having.",
    ),
    # =========================================================================
    # THE OWED-ROWS TRANCHE, 2026-08-24. Four sources were censused whole and
    # their owed rows sat as a queue; this drains it: 24 rows, 17 laws, each
    # quoting the source text fetched this day. None of these carries a decider
    # yet — they enter as readings, which is the honest state of a law on
    # arrival, and the ones whose data shape already exists say so in a note.
    # =========================================================================

    # --- IPCC guidance note: the seven remaining owed rows -----------------------
    _law(
        "calibration-is-agreed-before-the-case",
        "The vocabulary that grades certainty is agreed in advance, never improvised "
        "in the middle of the case it grades",
        _cited("IPCC AR5 uncertainty guidance, paragraph 1"),
        falsifier="Two reports within one practice grading certainty in incompatible "
                  "improvised vocabularies, or a graded term that no agreed scale "
                  "defines.",
        triggers=["a result is reported with a graded qualifier"],
        citations=[(IPCC + ", paragraph 1", IPCC_URL,
                    "At an early stage, consider approaches to communicating the degree "
                    "of certainty in key findings in your chapter using the calibrated "
                    "language described below. ... Agree on a moderated and balanced "
                    "process for doing this in advance of confronting these issues in a "
                    "specific context.")],
        note="The census said it plainly: the estate has no agreed calibration "
             "vocabulary, which is why each turn improvises one.",
    ),
    _law(
        "a-view-moves-on-observation-not-on-company",
        "A stated assessment changes on a named observation — never merely to converge "
        "with a view somebody expressed, and never held to a prior version beyond what "
        "the evidence justifies",
        _cited("IPCC AR5 uncertainty guidance, paragraph 3"),
        falsifier="An assessment revised toward an interlocutor's expressed view, or "
                  "held against new evidence, with no observation named between the "
                  "two versions. Both directions are the breach: folding is convergence "
                  "and stonewalling is anchoring.",
        triggers=["an assessment is restated after another party has expressed a view",
                  "a position is revised or defended"],
        citations=[(IPCC + ", paragraph 3", IPCC_URL,
                    "Be aware of a tendency for a group to converge on an expressed "
                    "view and become overconfident in it. Views and estimates can also "
                    "become anchored on previous versions or values to a greater extent "
                    "than is justified. ... Recognize when individual views are "
                    "adjusting as a result of group interactions and allow adequate "
                    "time for such changes in viewpoint to be reviewed.")],
        sightings=[
            ("a session reviewed, 2026-08-24",
             "A built and tested proposal was withdrawn entirely on one clarifying "
             "question, before any counter-argument arrived; the owner named the cost — "
             "agreement that folds on being asked carries no information when it "
             "holds — and the position had to be restored. The same week's opposite "
             "edge: a law re-scoped toward the argument of the moment against a "
             "standing ruling."),
        ],
        note="This roots the conversational half of what a-ruling-has-no-stated-"
             "lifetime recorded as rootless: the note's own remedy — write the view "
             "down before the group discussion — is the claims record's shape, and "
             "'recognize when views are adjusting as a result of group interactions' "
             "is the reversal face stated by a standing authority. The AUTHORITY half "
             "of that debt (when a person's ruling binds) stays unrooted; this law is "
             "about evidence, not command.",
    ),
    _law(
        "structural-unknowns-are-considered",
        "An evaluation of uncertainty names the structural unknowns — incomplete "
        "understanding, competing framings — and not only the measurable ones",
        _cited("IPCC AR5 uncertainty guidance, paragraph 6"),
        falsifier="A graded finding whose named unknowns are all parameter-level while "
                  "a competing framing of the mechanism stands on the record "
                  "unaddressed.",
        triggers=["a finding is graded while an alternative framing is on record"],
        citations=[(IPCC + ", paragraph 6", IPCC_URL,
                    "Consider all plausible sources of uncertainty. Experts tend to "
                    "underestimate structural uncertainty arising from incomplete "
                    "understanding of or competing conceptual frameworks for relevant "
                    "systems and processes.")],
        note="The mirror of the fact-when-settled clause on "
             "a-qualifier-is-licensed-by-the-evidence, now carrying its own falsifier "
             "instead of riding as that law's second citation only.",
    ),
    _law(
        "validity-is-evidence-and-agreement",
        "A graded finding states both dimensions of its validity — the evidence and "
        "the degree of agreement — each with its account",
        _cited("IPCC AR5 uncertainty guidance, paragraph 8 and its summary terms"),
        falsifier="A graded finding stating one dimension only: evidence with no word "
                  "on agreement, or consensus with no word on evidence.",
        triggers=["a finding is graded on the strength of more than one source or "
                  "more than one judge"],
        citations=[(IPCC + ", paragraph 8", IPCC_URL,
                    "Use the following dimensions to evaluate the validity of a "
                    "finding: the type, amount, quality, and consistency of evidence "
                    "(summary terms: “limited,” “medium,” or "
                    "“robust”), and the degree of agreement (summary terms: "
                    "“low,” “medium,” or “high”). "
                    "... Provide a traceable account describing your evaluation of "
                    "evidence and agreement in the text of your chapter.")],
        note="Covers the census's rows 8, S3 and S4 in one law: the two summary-term "
             "scales are the dimensions' vocabulary, not separate demands. The claims "
             "record has one dimension today (where the evidence stands) and no "
             "vocabulary for agreement.",
    ),
    _law(
        "low-confidence-is-reserved-and-explained",
        "The low end of a confidence scale is presented only for areas of major "
        "concern, and the reasons for presenting it are explained",
        _cited("IPCC AR5 uncertainty guidance, paragraph 9"),
        falsifier="A low-confidence grade carrying no stated reason, or low grades "
                  "spent routinely where nothing major is at stake.",
        triggers=["a finding is presented at the low end of a graded scale"],
        citations=[(IPCC + ", paragraph 9", IPCC_URL,
                    "Presentation of findings with “low” and “very "
                    "low” confidence should be reserved for areas of major "
                    "concern, and the reasons for their presentation should be "
                    "carefully explained.")],
        note="Anti-modesty, from the same note that is anti-bravado: routine "
             "lowballing devalues the signal exactly as routine overclaiming does, "
             "and it is the direction that goes uncorrected because it wears "
             "caution.",
    ),
    _law(
        "sufficient-information-gives-the-number",
        "Where the information suffices, the value is given directly; a calibrated "
        "term never stands in for a measurement that exists, or for one that was "
        "never made",
        _cited("IPCC AR5 uncertainty guidance, paragraph 10"),
        falsifier="A mid-scale term where the direct figure was available and not "
                  "given, or a mid-scale term under which no assessment exists at "
                  "all.",
        triggers=["a quantified result is reported in calibrated words"],
        citations=[(IPCC + ", paragraph 10", IPCC_URL,
                    "When there is sufficient information, it is preferable to specify "
                    "the full probability distribution or a probability range (e.g., "
                    "90-95%) without using the terms in Table 1. “About as likely "
                    "as not” should not be used to express a lack of "
                    "knowledge.")],
    ),
    _law(
        "a-conditional-finding-grades-its-condition",
        "A finding that rests on another finding is evaluated separately, and the "
        "certainty of what it rests on is stated beside its own",
        _cited("IPCC AR5 uncertainty guidance, the conditional-findings instruction"),
        falsifier="A finding reported unconditionally that holds only under another "
                  "finding whose certainty is lower and unstated.",
        triggers=["a finding rests on another finding",
                  "a green check rests on another check"],
        citations=[(IPCC + ", conditional findings", IPCC_URL,
                    "For findings (effects) that are conditional on other findings "
                    "(causes), consider independently evaluating the degrees of "
                    "certainty in both causes and effects, with the understanding that "
                    "the degree of certainty in the causes may be low.")],
        note="The census's row S5, and the row aimed most squarely at this estate: a "
             "practice whose checks are chains of pins reports leaf-greens whose "
             "certainty is the chain's weakest link, unstated.",
    ),

    # --- STARD 2015: the twelve remaining owed rows, as eight laws ---------------
    _law(
        "prespecified-is-distinguished-from-exploratory",
        "A report says whether its expectations and thresholds were set before the "
        "results were seen or after",
        _cited("STARD 2015, items 5 and 12a"),
        falsifier="A threshold or expectation presented without saying which, or "
                  "presented as set in advance when the record shows it was tuned to "
                  "what turned up.",
        triggers=["a check's threshold or expectation is reported"],
        citations=[(STARD + ", item 5", STARD_URL,
                    "Whether data collection was planned before the index test and "
                    "reference standard were performed (prospective study) or after "
                    "(retrospective study)"),
                   (STARD + ", item 12a", STARD_URL,
                    "Definition of and rationale for test positivity cut-offs or "
                    "result categories of the index test, distinguishing pre-specified "
                    "from exploratory")],
        sightings=[
            ("the run-in heading bound, 2026-08-23",
             "A six-word ceiling separating a heading from an emphasised sentence was "
             "set after seeing what it caught, and nothing in the record says so — a "
             "reader meets it as if it had been derived.")],
    ),
    _law(
        "a-corpus-names-its-assembly",
        "Findings over a corpus name how the corpus was assembled — and whether the "
        "series was exhaustive, random, or convenient",
        _cited("STARD 2015, items 7 and 9"),
        falsifier="Findings reported over a corpus whose selection is unstated, or a "
                  "convenience sample reported as if it were the population.",
        triggers=["findings are reported over a corpus somebody assembled"],
        citations=[(STARD + ", item 7", STARD_URL,
                    "On what basis potentially eligible participants were identified "
                    "(such as symptoms, results from previous tests, inclusion in "
                    "registry)"),
                   (STARD + ", item 9", STARD_URL,
                    "Whether participants formed a consecutive, random or convenience "
                    "series")],
        sightings=[
            ("the convergence series impeached, 2026-08-17",
             "A series of near-zero vocabulary costs was reported as evidence of "
             "convergence until its own author impeached it: the miner picked laws it "
             "could see the compile route for, so the line measured the mining hand. "
             "The remedy — the cost-blind census — then lived as a habit with no "
             "falsifier until this law.")],
        note="The cost-blind-census doctrine, which this repository practises and had "
             "never stated as a rule anything could break.",
    ),
    _law(
        "a-check-is-stated-to-replication",
        "A verdict's check is stated in enough detail that another hand re-runs it "
        "and reaches the same verdict",
        _cited("STARD 2015, item 10a"),
        falsifier="A reported verdict whose check cannot be re-run from what the "
                  "record states.",
        triggers=["a verdict is reported beyond the session that produced it"],
        citations=[(STARD + ", item 10a", STARD_URL,
                    "Index test, in sufficient detail to allow replication")],
    ),
    _law(
        "the-reference-standard-is-named-with-its-rationale",
        "What a check is judged against is stated, and where alternatives exist, why "
        "that standard was chosen",
        _cited("STARD 2015, items 10b and 11"),
        falsifier="An accuracy claim that names no reference standard, or names one "
                  "without a word on why it and not the alternative.",
        triggers=["a check's accuracy is claimed against some ground truth"],
        citations=[(STARD + ", item 10b", STARD_URL,
                    "Reference standard, in sufficient detail to allow replication"),
                   (STARD + ", item 11", STARD_URL,
                    "Rationale for choosing the reference standard (if alternatives "
                    "exist)")],
    ),
    _law(
        "blindness-is-disclosed",
        "Whether the check's author knew the answers while writing it, and whether "
        "the judge saw the check's verdict before deciding, is stated",
        _cited("STARD 2015, items 13a and 13b"),
        falsifier="An accuracy claim silent on either direction of blinding.",
        triggers=["a check's accuracy is claimed against a judged standard"],
        citations=[(STARD + ", item 13a", STARD_URL,
                    "Whether clinical information and reference standard results were "
                    "available to the performers/readers of the index test"),
                   (STARD + ", item 13b", STARD_URL,
                    "Whether clinical information and index test results were "
                    "available to the assessors of the reference standard")],
        sightings=[
            ("this repository's own alarms and rulings, 2026-08-24",
             "Every alarm corpus is written by the same hand as the checks it "
             "exercises, and the adjudicator reads the finding before ruling on it, "
             "always — neither fact recorded anywhere as a limitation until this "
             "law's census row said it aloud.")],
    ),
    _law(
        "missing-input-is-reported-with-its-handling",
        "How absent or unreadable input was handled is reported beside the findings",
        _cited("STARD 2015, item 16"),
        falsifier="A report over a corpus with unreadable members that does not say "
                  "how they were counted.",
        triggers=["findings are reported over a corpus any part of which could not "
                  "be read"],
        citations=[(STARD + ", item 16", STARD_URL,
                    "How missing data on the index test and reference standard were "
                    "handled")],
        note="The sibling of a-check-reports-what-it-could-not-judge one step "
             "earlier: item 15 is output the check could not call, this is input it "
             "never received. The estate's pointer check already obeys it — an "
             "unreadable ledger reports UNKNOWN, never gone — as one module's "
             "decision, which this law makes portable.",
    ),
    _law(
        "calibration-size-is-declared-before-the-run",
        "How much corpus a check is calibrated on is decided and stated before the "
        "run, with how that size was determined",
        _cited("STARD 2015, item 18"),
        falsifier="An accuracy or false-positive figure from a calibration whose "
                  "size was settled after the results were in.",
        triggers=["a check's accuracy is calibrated or claimed"],
        citations=[(STARD + ", item 18", STARD_URL,
                    "Intended sample size and how it was determined"),
                   (SPIRIT + ", item 19 — the before side", SPIRIT_URL,
                    "How sample size was determined, including all assumptions "
                    "supporting the sample size calculation")],
        sightings=[
            ("the first turn checker, 2026-08-22",
             "Calibrated on one session with one hit and reported as zero false "
             "positives; measured properly across twenty transcripts it was wrong "
             "roughly seven times in eight.")],
    ),
    _law(
        "a-check-reports-its-misses",
        "A check's accuracy is a cross tabulation: what it caught, what it missed, "
        "and what it wrongly flagged, against the reference standard",
        _cited("STARD 2015, item 23"),
        falsifier="An accuracy claim reporting only what was caught — hits with no "
                  "row for misses or false alarms.",
        triggers=["a check's accuracy is claimed",
                  "a clean bill is reported from a check"],
        citations=[(STARD + ", item 23", STARD_URL,
                    "Cross tabulation of the index test results (or their "
                    "distribution) by the results of the reference standard")],
        sightings=[
            ("the turn checker's own report, 2026-08-22",
             "Eighteen candidates over 158 turns, all cleared — with the "
             "false-negative rate admitted unmeasured in the same breath: the "
             "cross tabulation's missing row, named and then not built.")],
    ),

    # --- Parnas 1972: the three owed rows, as one law ----------------------------
    _law(
        "a-boundary-is-judged-by-what-a-change-touches",
        "A module boundary is judged by its three observable benefits: a changed "
        "decision touches one module, modules are worked on separately, and each is "
        "understood without the others",
        _cited("Parnas 1972, the expected benefits of modular programming"),
        falsifier="A change to one hidden decision that touches many modules; a "
                  "module that cannot be understood without understanding its "
                  "neighbours; work on one module that must wait on the internals of "
                  "another.",
        triggers=["a boundary between modules is drawn or defended"],
        citations=[(PARNAS, PARNAS_URL,
                    "The benefits expected of modular programming are: (1) "
                    "managerial - development time should be shortened because "
                    "separate groups would work on each module with little need for "
                    "communication; (2) product flexibility - it should be possible "
                    "to make drastic changes to one module without a need to change "
                    "others; (3) comprehensibility - it should be possible to study "
                    "the system one module at a time.")],
        note="Covers the census's rows 4, 5 and 6 in one law, because the source "
             "states them as one list: the benefits are the test. "
             "a-thing-is-built-where-its-subject-lives says where a thing goes; this "
             "is how to tell, after the fact, that it went to the wrong place — the "
             "price is measured in what a change touches.",
    ),

    # --- Eidelman et al. 2009: the one owed row ----------------------------------
    _law(
        "an-imagined-plan-is-not-thereby-likely",
        "Imagining a course in detail raises its felt likelihood and thence its felt "
        "goodness; a plan's likelihood is graded by evidence, never by how vividly "
        "it has been sketched",
        _cited("Eidelman, Crandall & Pattershall 2009, study 3 (read from the "
               "abstract; the full text is paywalled and the census says so)"),
        falsifier="A plan preferred over its alternatives with no stated evidence "
                  "beyond its own elaboration — the sketch standing where the grounds "
                  "should be.",
        triggers=["a plan is chosen among alternatives after one was sketched in "
                  "detail"],
        citations=[(EXISTENCE_BIAS + ", study 3", EXISTENCE_URL,
                    "Imagining an event increases estimates of its likelihood, which "
                    "in turn leads to favorable evaluation (Study 3).")],
        note="The sibling of what-exists-is-not-thereby-chosen, one step earlier in "
             "time: that law guards the standing thing, this guards the thing that "
             "does not exist yet and already looks right because somebody drew it.",
    ),
    # --- the Agans census, 2026-08-24: the five rules the founding day left unread.
    # --- The rule names are quoted from the author's own chapter PDF; where a law
    # --- transfers a rule from debugging machines to judging work, the note says the
    # --- transfer is ours.
    _law(
        "the-systems-own-record-is-read-first",
        "A chase begins by reading what the system says about itself — the manual, "
        "the design record, the declared behavior — before the first theory",
        _agans("Understand the system"),
        falsifier="A chase resolved by a fact the system's own record had stated all "
                  "along, where that record was never opened — discoverable whenever "
                  "the fix quotes the record it did not read.",
        triggers=["a failure is being chased in a system that carries its own record"],
        citations=[(f"{AGANS} — rule 1", AGANS_URL, "Understand the system")],
        sightings=[
            ("craft-laws, 2026-08-23",
             "A sentence-length law was run over documentation for a week. Its own "
             "trigger, in the file, said the app's voice — dry, terse, no explaining "
             "text — and reading the law's record was the entire fix: the decider came "
             "out of the lane the same hour the trigger was finally read.")],
    ),
    _law(
        "a-hunt-narrows-the-space",
        "Each observation in a hunt for a cause is chosen to rule out a region of "
        "candidates, not to audition one candidate at a time",
        _agans("Divide and conquer"),
        falsifier="A chase whose successive observations each addressed a single "
                  "candidate while the space stayed unordered — countable in an audit "
                  "trail as steps that eliminated nothing beyond themselves.",
        triggers=["a failure has more than a handful of candidate causes"],
        citations=[(f"{AGANS} — rule 4", AGANS_URL, "Divide and conquer")],
        note="The falsifier is honestly the weakest of the family: whether a step "
             "narrowed the space is often a reading of the trail rather than a count "
             "over it. It stays a reading until trails are data — which "
             "the-trail-is-written-as-it-happens, minted beside it, is the "
             "precondition for.",
    ),
    _law(
        "the-trail-is-written-as-it-happens",
        "Each act on a failure is recorded when it happens — what was done, in what "
        "order, what was observed — never reconstructed afterwards",
        _agans("Keep an audit trail"),
        falsifier="An account of a chase written after the fact that cannot say which "
                  "change preceded which observation; a fix whose trail begins at the "
                  "commit that closed it.",
        triggers=["a failure is chased across more than one attempt"],
        citations=[(f"{AGANS} — rule 6", AGANS_URL, "Keep an audit trail")],
        note="This estate practises it as substrate — claims filed at the moment of "
             "claiming, flight tapes recorded from the first commit — and had no law "
             "making the skipped trail a breach. The claims record is this rule as "
             "data; the law is what makes not filing one visible.",
    ),
    _law(
        "the-baseline-assumption-is-verified",
        "The obvious precondition is verified before the clever cause is chased — the "
        "power, the environment, the version actually running",
        _agans("Check the plug"),
        falsifier="A chase that ends at a false baseline assumption nobody had "
                  "checked: the credential that was never loaded, the stale build, "
                  "the wrong branch — while theories were built above it.",
        triggers=["a failure is being chased", "a system stops working that worked"],
        citations=[(f"{AGANS} — rule 7", AGANS_URL, "Check the plug")],
        sightings=[
            ("health, 2026-08-24",
             "An app crash chased while the actual state was a clobbered .env.local — "
             "the Vercel CLI had overwritten the credentials file, and the declared "
             "diagnosis on the work map read: restoring creds and hardening the "
             "missing-credential path. The plug, checked late.")],
    ),
    _law(
        "a-resisting-failure-gets-fresh-eyes",
        "A failure that resists is shown to a reader who has not been staring at it, "
        "and explaining it to them counts as looking",
        _agans("Get a fresh view"),
        falsifier="Rounds of theories about one failure from one head, with no second "
                  "reader brought in — countable in the record as authors per "
                  "resisting failure.",
        triggers=["a failure survives repeated attempts by the same author"],
        citations=[(f"{AGANS} — rule 8", AGANS_URL, "Get a fresh view")],
        sightings=[
            ("this estate, 2026-08-24",
             "A session's own summary of its thirteen failures misclassified the one "
             "that mattered — verified work withdrawn as unnecessary, reported as "
             "asserted work withdrawn as wrong. The owner brought in a fresh reader "
             "for the review, and the misclassification was the first thing the "
             "fresh reading found.")],
    ),
    # --- the remaining-sources censuses, 2026-08-24: the three practice rows that
    # --- were owed across CONSORT, ARRIVE and Tversky-Kahneman, each quoting the
    # --- source text fetched this day.
    _law(
        "a-null-is-stated-not-implied",
        "A report states its empty sets in words — no exclusions, no criteria, no "
        "confounders controlled — and never leaves absence to be inferred from "
        "silence",
        _cited("ARRIVE 2.0, Essential 10 item 3"),
        falsifier="A report enumerating what was found, excluded or controlled that "
                  "is silent about a set that is empty — so a reader cannot tell an "
                  "empty set from an unexamined one.",
        triggers=["a report enumerates findings, exclusions or controls"],
        citations=[(ARRIVE + ", item 3", ARRIVE_URL,
                    "If no criteria were set, state this explicitly. ... If there "
                    "were no exclusions, state so."),
                   (ARRIVE + ", item 4", ARRIVE_URL,
                    "If confounders were not controlled, state this explicitly."),
                   (SPIRIT + ", items 28a and 29", SPIRIT_URL,
                    "Alternatively, an explanation of why a DMC is not needed ... "
                    "If there is no monitoring, give explanation")],
        sightings=[
            ("this estate's own reports, 2026-08-24",
             "The prose lane reported 'no prose decider convicts' over paragraphs it "
             "had never read, and the argument reader skipped node kinds silently "
             "for a day - both fixed this week by making the report say what went "
             "unexamined, which is this law obeyed before it was found stated.")],
    ),
    _law(
        "a-stopped-run-says-why",
        "A run that ends early — stopped, interrupted, abandoned — reports that it "
        "did and why, because a result from a stopped run is a different kind of "
        "result",
        _cited("CONSORT 2025, items 16b and 23b"),
        falsifier="A figure or verdict from a run that did not complete, reported "
                  "without saying the run was stopped or why — a peek dressed as a "
                  "measurement.",
        triggers=["a run, sweep or calibration ends before its declared corpus is "
                  "exhausted"],
        citations=[(CONSORT + ", item 16b", CONSORT_URL,
                    "Explanation of any interim analyses and stopping guidelines"),
                   (CONSORT + ", item 23b", CONSORT_URL,
                    "If relevant, why the trial ended or was stopped"),
                   (SPIRIT + ", item 28b — the before side", SPIRIT_URL,
                    "Explanation of any interim analyses and stopping guidelines, "
                    "including who will have access to these interim results and "
                    "make the final decision to terminate the trial")],
        note="Stopping on a peek is the tuning defect in disguise: the moment chosen "
             "to stop selects the result. The trial standards demand the stopping "
             "rule in advance and the reason after, and both halves transfer whole.",
    ),
    _law(
        "regression-is-the-null-after-an-extreme",
        "An improvement measured after selecting on an extreme is regression to the "
        "mean until something rules that out — the fix that follows the worst day "
        "gets credit it has not earned",
        _cited("Tversky & Kahneman 1974, misconceptions of regression"),
        falsifier="A change credited for an improvement in a metric that was "
                  "selected for intervention BECAUSE it was at an extreme, with no "
                  "control for regression — observable wherever the trigger for "
                  "acting was the bad reading itself.",
        triggers=["a change is credited for improving the metric that triggered it"],
        citations=[(TK1974, TK1974_URL,
                    "misconceptions of regression"),
                   (TK1974 + " (the mechanism)", TK1974_URL,
                    "regression toward the mean")],
        note="The citation quotes the paper's own section heads; the worked example "
             "there is flight instructors concluding that punishment works because "
             "performance improved after it - the improvement was regression. The "
             "practice form: the failing check fixed on its worst day, the flaky "
             "test stabilised right after the retry was added.",
    ),
    # --- the PRISMA census, 2026-08-24: the one owed row, and it is the intake debt's
    # --- premise stated as a law by a standing authority.
    _law(
        "a-corpus-of-reports-carries-its-reporting-bias",
        "Findings drawn from a corpus of reports state the risk that what was never "
        "reported differs from what was — the file drawer is part of the corpus",
        _cited("PRISMA 2020, items 14 and 21: risk of bias due to missing results"),
        falsifier="A conclusion from filed records presented as a conclusion about the "
                  "practice, with no word on what systematically never gets filed — "
                  "observable wherever the filing itself selects for being noticed.",
        triggers=["a conclusion is drawn from a corpus of self-filed records"],
        citations=[(PRISMA + ", item 14", PRISMA_URL,
                    "Describe any methods used to assess risk of bias due to missing "
                    "results in a synthesis."),
                   (PRISMA + ", item 21", PRISMA_URL,
                    "Present assessments of risk of bias due to missing results "
                    "(arising from reporting biases) for each synthesis assessed.")],
        sightings=[
            ("the claims record itself, standing",
             "the-deciders-run-by-hand has said it in prose since 2026-08-22: "
             "self-report catches the part already noticed, which is the part that "
             "needed no check. Every conviction statistic from the claims hook is "
             "drawn from claims somebody chose to file, and until this law nothing "
             "required that selection to be named beside the number.")],
        note="The sibling of a-check-reports-its-misses one level up: that law wants "
             "the misses of a check, this wants the misses of the RECORD the checks "
             "read. It is the intake debt's premise as a falsifiable law, which means "
             "the debt's eventual discharge has a rule to answer to.",
    ),
    # --- the SPIRIT census, 2026-08-25: the before-standard's one owed row.
    _law(
        "a-protocol-is-an-artifact-before-the-run",
        "What a run will measure, over what corpus, with what thresholds and what "
        "stopping rule, exists as an accessible artifact dated before the run — "
        "prespecification is a document, never a recollection",
        _cited("SPIRIT 2025: the protocol standard itself — the entire instrument "
               "exists so the declaration precedes the trial"),
        falsifier="A report claiming its expectations were set in advance, where no "
                  "artifact dated before the run states them — the claim of "
                  "prespecification resting on the claimant's memory.",
        triggers=["a measurement claims its thresholds or expectations were set in "
                  "advance"],
        citations=[(SPIRIT + ", item 5", SPIRIT_URL,
                    "Where the trial protocol and statistical analysis plan can be "
                    "accessed"),
                   (SPIRIT + ", item 31", SPIRIT_URL,
                    "Plans for communicating important protocol modifications to "
                    "relevant parties")],
        note="The teeth prespecified-is-distinguished-from-exploratory lacks: that "
             "law asks a report to SAY whether thresholds were set in advance, and "
             "saying is a memory. This asks for the dated artifact, which in this "
             "estate is a committed record — the declaration is checkable against "
             "the history, not against sincerity. The decider route exists the day "
             "somebody wants it: a protocol filed in the claims record before the "
             "run, referenced by the measurement after it.",
    ),
]


PRACTICE_GATE = Node(
    id="publish-practice",
    kind="gate",
    name="What may be relied on as a law about the work",
    payload={
        "note": "Red on the same terms as the interface gate: a law nobody has been "
                "found to have stated is carried visibly, never silently. Two of these "
                "are ours alone — spending the user as a harness, and dressing a "
                "detour as a fix — and if somebody has said them better, cite them and "
                "the red goes away.",
    },
    links={"admits": [law.id for law in PRACTICE]},
)
