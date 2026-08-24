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
        _uncited(),
        falsifier="A catalogue stated as 'the N families/laws/items of <source>' where the "
                  "source, read in full, lists an item the catalogue neither carries nor "
                  "names as owed — an enumeration filtered by what was feasible to build.",
        triggers=["a catalogue or census is authored from a cited source",
                  "a count of families, laws or items is stated"],
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
             "the source's, and what was left out is a number too.",
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
