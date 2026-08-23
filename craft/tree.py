"""The craft tree: craft@0.1.0's semantics, with the laws hanging under them."""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401 -- the natives; the packages themselves arrive by pin
from quern import Quern
from quern.library import consume

from quern import Node
from quern.provenance import Quantity

from .laws import GATE, LAWS
from .practice import PRACTICE, PRACTICE_GATE

_ROOT = Path(__file__).resolve().parents[1]

# The per-sighting exposure call the public flip required (xag/craft-laws#2), taken once
# for the whole file because every sighting has the same shape: UI copy and screen
# placement from one named app, no person, no household, no data.
DECISIONS = [
    Node(
        id="sightings-name-the-app",
        kind="decision",
        name="The sightings keep the app's name and date; nothing else of the app is "
             "exposed, and nothing personal ever was",
        payload={
            "rationale":
                "A sighting is evidence, and evidence anonymized loses exactly the "
                "property that makes a law trustworthy: that somebody can ask 'did this "
                "really happen'. Every sighting in laws.py was re-read for this "
                "decision; each exposes the app's name (chores), a date, a screen, and "
                "the defective copy itself — no user, no household, no stored data, no "
                "identifier. The app's name is already the estate's public case study "
                "(the 486-green localisation story is the launch narrative), so the "
                "name reveals nothing the story does not.",
            "consequence":
                "A future sighting drawn from real usage must clear the same bar before "
                "it enters: the defect is the content, the person is never. One that "
                "cannot be told without exposing a user is genericized or kept out.",
        },
        children=[
            Node(id="every-sighting-was-re-read", kind="grounds",
                 name="Every sighting in laws.py was re-read for this decision",
                 payload={"what": "Each exposes the app's name, a date, a screen and the defective copy — no user, no household, no stored data, no identifier. The app's name is already the estate's public case study.",
                           "where": "producer",
                           "gap": "A review of what the sightings contain today. It does not bound what a future sighting might expose."}),
            Node(id="alt-genericize-the-app", kind="alternative",
                 name="Scrub the app name from every sighting ('a household app')",
                 payload={"why":
                          "Costs the credibility that is the whole value of a sighting "
                          "— an anonymous anecdote is decoration — and protects "
                          "nothing, since the app's name is already public in the "
                          "estate's own telling of the story."}),
        ],
    ),
    Node(
        id="the-laws-side-has-a-formalism-side",
        kind="decision",
        name="interface@ is minted beside craft@: the denotation of an interface as "
             "data — surfaces, elements, bindings, content, denials, witnesses, "
             "constraints — with the decidable laws compiling against it "
             "(craft/compile.py) instead of being read against screens",
        payload={
            "rationale":
                "A law's trigger names properties of an app, and those properties had "
                "no formalism: 'any count is shown to a person' was prose matched by "
                "judgment. With the drawing as a tree, the property IS a node shape — "
                "an element declaring count_var — and both halves of the mechanical "
                "filter (which laws apply; whether they hold) become functions. The "
                "compilable laws (empty-state-never-contradicts, composed-prose, "
                "plurals-and-agreement) emit épure invariants, one per conviction, so "
                "an exhaustive prover checks them over every reachable UI state with "
                "a minimal click-path per violation. The laws and the formalism "
                "version together here because they drift apart anywhere else.",
            "consequence":
                "Only the decidable half compiles, and the split is enforced out "
                "loud: asking compile.py for a reading law raises, never silently "
                "skips. The constraint kind is minted as a seat (layout as solved "
                "interval queries, not three sampled viewports) and carried "
                "honestly with no consumer yet. First consumer of the whole package "
                "is chores' interface drawing, whose render-layer bindings are "
                "generated from the tree — drift impossible by construction for "
                "what is generated.",
        },
        children=[
            Node(id="the-trigger-was-prose-matched-by-judgment", kind="grounds",
                 name="A law's trigger named app properties that had no formalism",
                 payload={"what": "'Any count is shown to a person' was prose matched by judgment. With the drawing as a tree the property IS a node shape — an element declaring count_var — and both halves of the filter become functions.",
                           "where": "producer",
                           "gap": "Shown for the compilable laws. Whether every trigger reduces to a node shape is the open question the mechanization census exists to answer."}),
            Node(id="alt-interface-in-its-own-repo", kind="alternative",
                 name="Mint interface@ in a repo of its own",
                 payload={"why":
                          "The vocabulary is only load-bearing where laws bind to it: "
                          "a trigger that names an element shape must version with "
                          "the shape it names, or a law silently fires on a stale "
                          "formalism. Two repos would make that drift a resolver "
                          "accident; one repo makes it a diff in one review."}),
            Node(id="alt-compilers-in-the-package", kind="alternative",
                 name="Ship the compilers inside the published package",
                 payload={"why":
                          "Compilers are host code, like vigil's natives: Python "
                          "that runs, not data that means. The package carries what "
                          "a rule can go red on; the compilers travel with the repo "
                          "and are pinned by rev like any other code."}),
        ],
    ),
    Node(
        id="a-human-found-defect-enters-as-a-law",
        kind="decision",
        name="Every defect a person finds — feedback, an issue, a ruling on a "
             "proposed conviction — passes through one question before it is fixed: "
             "what valid generic rule did it break? The answer lands here, as a law "
             "or a refinement, so the fix ships with a regression test for every "
             "app that adopts the package, not just the one that bled",
        payload={
            "rationale":
                "A fix without a law repairs one screen once; a law repairs a class "
                "forever, everywhere the package is pinned. The first exercise of "
                "the protocol is one-act-one-name's first sighting: 'Add it' "
                "committing three different acts was proved co-offered by the "
                "compiler, ruled a defect by a person, and the RULING itself was "
                "generic — the act was already named by the menu that led there, so "
                "a commit may wear a conventional confirm. That became the law's "
                "generic-confirm exemption (falsifier text and compiler both), and "
                "chores' fix and the law's sharpening shipped as one motion. The "
                "sighting records it, because a law that has caught something is a "
                "law somebody may trust.",
            "consequence":
                "The question is also allowed to answer 'no generic rule — this is "
                "app taste', and then no law is minted: a package that absorbs "
                "every preference becomes a checklist, and checklists are ignored. "
                "The bar is the same as for any law: a falsifier somebody could "
                "observe, a trigger that switches it on, an authority or the "
                "honest uncited red.",
        },
        children=[
            Node(id="the-first-exercise-of-the-protocol", kind="grounds",
                 name="one-act-one-name's first sighting ran the protocol end to end",
                 payload={"what": "'Add it' committing three different acts was proved co-offered by the compiler, ruled a defect by a person, and the ruling itself was generic — so it became the law's generic-confirm exemption, in the falsifier text and the compiler both.",
                           "where": "user-surface",
                           "gap": "One exercise. It shows the protocol can run; it does not show the ruling is generic often enough to be worth the ceremony."}),
            Node(id="alt-fix-and-move-on", kind="alternative",
                 name="Fix the app and record nothing",
                 payload={"why": "The defect class survives the fix and re-enters "
                                 "through the next sheet somebody adds — the exact "
                                 "history of every law already in this file, each "
                                 "of which shipped as a one-off fix somewhere "
                                 "before it was written down as a law."}),
        ],
    ),
    Node(
        id="the-laws-grew-by-mining-not-by-bleeding",
        kind="decision",
        name="The package grew from 15 laws to 57 by mining the source catalogue "
             "(docs/sources.md) — sources chosen by authority and falsifiability, "
             "never fame — so coverage stops being an artifact of which defects "
             "happened to hurt us first",
        payload={
            "rationale":
                "Every law before this entered through a wound: a defect shipped, "
                "taught its law, and the law joined. Honest, but biased — a package "
                "grown only from one estate's scars covers that estate's habits. "
                "Four mining passes (accessibility, government/forms/copy, "
                "localization, empirical/content) worked a catalogue built to be "
                "category-exhaustive, with the gaps recorded as gaps and an overlap "
                "map so each law cites its strongest root: WCAG for the rule, "
                "GOV.UK for the operational wording, Baymard for the tested "
                "statistic, CLDR under everything plural. Every citation quote was "
                "fetched and verified verbatim — one pass caught the fetch tool "
                "FABRICATING a spec sentence and re-verified against raw source, "
                "which is the whole argument for quotes over paraphrases. Where "
                "clusters collided (error messaging arrived from three roots), the "
                "collision is merged and recorded in the law's note.",
            "consequence":
                "42 new laws, all cited, all with observable falsifiers; the "
                "standing red stays exactly the three uncited originals. The known "
                "costs, carried openly: none of the 42 has a sighting yet, and the "
                "critic's own doctrine says a law that never catches anything is a "
                "law nobody should trust — the `laws` command reports the "
                "caught-nothing list, which is now long and is the pruning "
                "pressure. Weakest entries are flagged in their notes "
                "(destructive-is-set-apart wants a stronger root). Apps inherit "
                "the growth on repin, and their critics will correctly re-open "
                "queues because the law set changed.",
        },
        children=[
            Node(id="four-mining-passes-over-a-catalogue", kind="grounds",
                 name="Four mining passes worked a catalogue built to be category-exhaustive",
                 payload={"what": "Accessibility, government/forms/copy, localization and empirical/content, with the gaps recorded as gaps and an overlap map so each law cites its strongest root: WCAG for the rule, GOV.UK for the wording, Baymard for the statistic.",
                           "where": "producer",
                           "gap": "The catalogue was assembled by the same people who mined it. The cost-blind censuses exist because this pass could not test its own sampling."}),
            Node(id="alt-wait-for-wounds", kind="alternative",
                 name="Keep growing one defect at a time",
                 payload={"why": "Focused but blind: the estate would never have "
                                 "written the keyboard laws or the RTL laws from "
                                 "its own scars, because its apps have not bled "
                                 "there yet — which is precisely when a law is "
                                 "cheapest to adopt."}),
            Node(id="alt-import-a-standard-wholesale", kind="alternative",
                 name="Adopt WCAG (or any one source) wholesale as the law set",
                 payload={"why": "One source is one bias with a certificate. The "
                                 "catalogue's overlap map exists because the "
                                 "strongest root differs per law — and half the "
                                 "craft (copy voice, forms research, l10n "
                                 "practice) lives outside any single standard."}),
        ],
    ),
    Node(
        id="the-vocabulary-converges",
        kind="hypothesis",
        meta={"amended":
              "2026-08-17 — the series' evidence was impeached, correctly: the "
              "miner picked laws it could see the compile route for, so a run of "
              "+0s measured the sampling, not the vocabulary (the owner's words: "
              "'I suspect you select laws that would compile at constant "
              "vocabulary'). The remedy is the COST-BLIND CENSUS "
              "(craft/census_rgaa.py): one authoritative source's entire numbered "
              "set, every criterion classified, the distribution published "
              "whatever it says. First run over RGAA 4.1: run the census, it "
              "counts — and its vocab rows named real missing kinds (media, "
              "tables-as-semantics, hover reveals, challenges, document "
              "artifacts), clustered on content the estate's own apps do not "
              "have, which is exactly why the biased series never met them. The "
              "claim stands as written — 'vocabulary not built yet' predicted "
              "precisely such clusters — but the evidence standard changes: the "
              "mining series is anecdote now; the census, re-run as kinds land, "
              "is the instrument."},
        name="Any law compiles against a sufficient semantic twin, and the vocabulary "
             "the twin needs CONVERGES: the new facts a newly mechanized law demands "
             "tend to zero. There is no judge-forever category — only laws whose "
             "model-side vocabulary has not been built yet",
        payload={
            "held_because":
                "The mechanization series so far is asymptote-shaped. The first law "
                "bought the base drawing (surfaces, elements, bindings, witnesses, "
                "denials — call it six ideas); every law since paid less: "
                "composed-prose +0, plurals +2 facts (count_var, fixed_plural), "
                "one-surface-one-job +1 (intent), rare-action +1 (frequency, plus "
                "the disclosure set), status-is-visible +0, one-act-one-name +0 "
                "(later +1 declaration, generic_keys), targets +0 facts (one "
                "measuring instrument). Marginal cost: 6, 0, 2, 1, 1, 0, 0, 0. And "
                "the model's own fidelity is not taken on faith — the drawing is "
                "licensed by walks (drift) exactly as épure's models are licensed "
                "by tapes (refine), so the judgment that moves INTO the model at "
                "authoring time is verified against reality, not trusted. The cost "
                "of an app declaring its twin is accepted on precisely that "
                "condition.",
            "consequence_if_wrong":
                "If a law class resists — successive laws of one kind each "
                "demanding substantial new vocabulary, with no reuse — then the "
                "twin is the wrong representation for that class, and the finding "
                "is about the MODEL, not about the law. The reading seat would "
                "return for that class as a diagnosed limitation with a named "
                "boundary, never as a default category. docs/mechanization.md "
                "carries the per-law routes and the running series, so the "
                "falsification below is checkable from the record rather than "
                "from memory.",
        },
        children=[
            Node(
                id="the-marginal-vocabulary-stops-shrinking",
                kind="falsification",
                payload={
                    "claim":
                        "Three consecutive newly mechanized laws each demand two or "
                        "more new facts or kinds with no reuse between them — or "
                        "one law receives two vocabulary extensions purpose-built "
                        "for it and still cannot compile.",
                    "cadence": "at every law mechanization, recorded beside it in "
                               "docs/mechanization.md",
                    "discharge_route":
                        "Name the resisting class and its boundary in this entry "
                        "(supersede, never delete), return that class to the "
                        "reading queue as a diagnosed limitation, and keep the "
                        "asymptote claim for the classes where the series holds.",
                },
            ),
            Node(
                id="the-census-vocab-bucket-does-not-shrink",
                kind="falsification",
                payload={
                    "claim":
                        "After the facts a cost-blind census names are built, a "
                        "re-run of the same census does not shrink its vocab "
                        "bucket — criteria enter it as fast as new kinds retire "
                        "them. Convergence sampled blind, not convergence mined "
                        "by a biased hand.",
                    "cadence": "re-run python -m craft.census_rgaa at every "
                               "vocabulary extension; add a second source's "
                               "census before claiming the asymptote publicly",
                    "discharge_route":
                        "Same as the sibling: name the resisting class, bound "
                        "it, return it to the reading queue as diagnosed — and "
                        "say in mechanization.md that the asymptote holds only "
                        "outside it.",
                },
            ),
        ],
    ),
    Node(
        id="a-word-list-is-a-reading-not-a-mechanization",
        kind="decision",
        name="A law checked by matching words in prose is unmechanized, and says so - it "
             "does not get a decider, and it never holds a handback",
        payload={
            "rationale":
                "Three claim deciders were built by matching words: /deliberate|by design|"
                "on purpose/, /later|next|not yet|deferred|owed|blocked|remains/, and a "
                "count-noun pattern. The defence was that the match only TRIGGERED and the "
                "verdict was structural - a word hit, then a missing field convicts - and "
                "that distinction is real. It is not enough of one. Choosing WHICH claims "
                "are subject to a law by reading their prose is the reading, whatever "
                "decides afterwards, and this repo has the measurement: a word list over a "
                "turn's prose was wrong about seven times in eight, and twice convicted the "
                "law being OBEYED, because the difference between a hedge that is a defect "
                "and a hedge that names its own unknown is meaning. The same is true of "
                "'later': a done-claim whose gap says a part comes later may be the law "
                "broken or the law obeyed, and no pattern separates them.",
            "consequence":
                "The three are removed from craft.claims, and the LAWS stay. They carry "
                "falsifiers and real sightings and they are red on a-law-cites-a-source, "
                "which is this repo's honest state for a law with no root. What they no "
                "longer have is a mechanism, which is the accurate position rather than a "
                "gap: unmechanized, not faked. Five deciders remain, and every one of them "
                "reads a field - the shape of the evidence, a boolean, the length of a "
                "list - and never a word. The aggravation these three carried is that they "
                "fired at Stop with exit 2, so an uncited, reading-shaped rule was holding "
                "a handback, which [[the-deciders-run-by-hand]] rejects.",
        },
        children=[
            Node(id="three-deciders-built-by-matching", kind="grounds",
                 name="Three claim deciders were built by matching words, and the defence did not hold",
                 payload={"what": "The patterns were /deliberate|by design|on purpose/, /later|next|not yet|deferred|owed|blocked|remains/, and a count-noun pattern. The defence was that the match only TRIGGERED and the verdict was structural. The distinction is real and is not enough of one.",
                           "where": "producer",
                           "gap": "Three deciders in one package. It says a wordlist trigger is a reading; it does not measure how often such a trigger picks the wrong claims."}),
            Node(id="alt-keep-them-the-match-only-triggers", kind="alternative",
                 name="Keep them: the regex selects, the missing field convicts, so a "
                      "false trigger costs one extra field and never a wrong verdict",
                 payload={"why":
                          "It is the strongest argument for them and it was mine. It fails "
                          "on where the cost lands: the extra field is demanded at Stop, "
                          "with exit 2, from an author who is mid-sentence and cannot "
                          "argue with it - and a check that asks for a field on a sentence "
                          "it misread is exactly the noise that gets a check switched off. "
                          "A trigger nobody can argue with is a verdict."}),
            Node(id="alt-delete-the-three-laws-as-well", kind="alternative",
                 name="Delete the laws too, since nothing can check them",
                 payload={"why":
                          "A law is not the check. Each of these three has a falsifier a "
                          "person can observe and a sighting where it caught something "
                          "real, which is the whole argument for a law. Deleting them "
                          "would lose the finding to keep the tooling tidy, and would "
                          "leave the habit they name unnamed."}),
        ],
    ),
]


def build() -> Quern:
    # The channel exists now (xag/quern#19) and these lines became the promised pin:
    # craft@0.1.0 is published to the registry like anything else, and this repo consumes
    # its own product by digest -- quern.lock, .quern/library, proof re-run at sync. `craft`
    # was always a Package; now it has somewhere to go. Refining the laws is a republish
    # under a new version and a repin, which is not friction: for a package of LAWS,
    # every change deliberate is the point.
    lib, refs = consume(_ROOT, os.environ.get("QUERN_REGISTRY", _ROOT.parent / "quern-registry"))

    quern = Quern(packages=[r for r in refs if r.name in ("craft", "ledger")])
    quern = lib.effective(quern)
    quern.root.children = [*LAWS, *PRACTICE, *DECISIONS, *DEBTS, GATE, PRACTICE_GATE]
    return quern


DECISIONS.append(Node(
    id="the-process-is-ruled-too",
    kind="decision",
    name="The WORK is governed by laws in this package, beside the laws about "
         "interfaces — same shape (falsifier, trigger, citation, sighting), separate "
         "family (craft/practice.py), because a claim like 'it is done' is exactly as "
         "checkable as a claim about a screen, and exactly as prone to drift",
    payload={
        "rationale":
            "Fifteen done-claims cited green suites, deploy ids and log lines "
            "— producer-side every one, and none an observation of the surface "
            "a person touches. The estate already had the doctrine that "
            "would have caught it (instrument the boundary; replay the tape rather "
            "than re-derive what must have happened) and applied it to storage and "
            "HTTP while leaving the one boundary that mattered — the widget's — dark. "
            "A doctrine held in prose is a doctrine that binds where somebody "
            "remembers it. The remedy is the same one this repo already made for "
            "interfaces: state it as data with a falsifier, so the claim can be "
            "checked instead of trusted. Agans wrote four of the six in 2002; they "
            "are cited, because doing a known-catastrophic thing is worse than "
            "inventing a new one.",
        "consequence":
            "Two families in one package and one rendered file. The practice gate is "
            "red on the same terms as the interface gate — two of the six cite nobody "
            "and say so. Their triggers are different in kind: an interface law fires "
            "on a screen, a practice law fires on a CLAIM, which means the check that "
            "would enforce them mechanically is a check on what a session asserts, and "
            "that check does not exist yet. Until it does, these are read by the agent "
            "at the moment of claiming and by the founder when a claim smells wrong — "
            "which is exactly how the interface laws lived before the compiler, and "
            "the compiler is where that history says this goes.",
    },
    children=[
        Node(id="fifteen-done-claims-against-an-empty-rectangle", kind="grounds",
             name="A card rendered as an empty rectangle and the job was declared finished fifteen times",
             payload={"what": "2026-08-17. Not one of the fifteen claims was dishonest and not one was evidence of the thing claimed: green suites, deploy ids, log lines and files on a machine — all producer-side, none an observation of the surface a person touches, while the founder answered 'still nothing'.",
                       "where": "user-surface",
                       "gap": "One session, one card. It establishes that producer-side evidence can accompany fifteen false done-claims, not the base rate at which it does."}),
        Node(id="alt-put-the-process-in-a-skill", kind="alternative",
             name="Write the lessons into the deploy/session skills as procedure",
             payload={"why":
                      "A procedure cannot go red. Skills say do this then that, and "
                      "they are the right home for the HOW (both harnesses ran, "
                      "pictures opened) — the widget procedure lives there and should. "
                      "But 'the job is done' is a claim about the world, and a claim "
                      "needs a falsifier, which is a law's shape and not a skill's."}),
        Node(id="alt-write-them-as-memories", kind="alternative",
             name="Store them as agent memories",
             payload={"why":
                      "Memory is for facts about the person and their preferences, and "
                      "it travels with one agent's context. A law about the work has to "
                      "bind every session in the estate, including the ones that never "
                      "load that memory — and has to be arguable in a diff."}),
        Node(id="alt-one-family-with-the-interface-laws", kind="alternative",
             name="Mix them into laws.py as more laws",
             payload={"why":
                      "Their triggers name different things: 'the app is used on a "
                      "phone' versus 'anything is reported as done'. A filter that "
                      "asks which laws apply to a screen would have to skip half the "
                      "file, and the compiler's whole premise is that a trigger is a "
                      "property of the artifact under test."}),
    ],
))


DECISIONS.append(Node(
    id="coverage-is-the-metric-laws-are-the-probe",
    kind="decision",
    name="An app's verification is scored by its twin's COVERAGE of the app — "
         "surfaces drawn over surfaces walked, strings bound over strings shipped, "
         "toward 100% — never by which tools it has or how many laws it passes. "
         "The law set serves the other master: each law probes whether the "
         "vocabulary suffices",
    links={"rests_on": ["the-vocabulary-converges"]},
    payload={
        "rationale":
            "The first adoption survey scored a ladder of artifacts, and that "
            "scale is contingent on today's rules: it read chores as complete "
            "(11/11 rungs) while chores' twin covered 45% of its walked surfaces "
            "and ~7% of its shipped strings — every undrawn surface a place no "
            "law can reach, invisible in the score. Coverage is the invariant: at "
            "100%, every law, current and future, applies wholesale and for free, "
            "which is what makes the vocabulary-plus-process the product and the "
            "law count a byproduct. The 57 laws were mined to FALSIFY the "
            "vocabulary (the convergence hypothesis), not to grade apps; a law "
            "that demands new vocabulary is doing its job either way.",
        "consequence":
            "surface_tape.adopt now headlines the coverage and names the undrawn "
            "surfaces; the rungs remain, demoted to process. The development "
            "process this implies: walk first (the walker defines the coverage "
            "denominator), draw toward it, bind toward the catalogue, and let "
            "laws-passed be something nobody optimizes directly.",
    },
    children=[
        Node(id="alt-score-by-tooling", kind="alternative",
             name="Keep the artifact ladder as the adoption score",
             payload={"why": "Contingent on the current rule set and saturates at "
                             "eleven while the twin describes a fraction of the "
                             "app - the wariness that triggered this decision."}),
        Node(id="alt-score-by-laws-passed", kind="alternative",
             name="Score apps by how many laws they pass",
             payload={"why": "The denominator grows with every mined law, so the "
                             "score punishes exactly the mining the vocabulary "
                             "needs - and a pass over an undrawn surface is a "
                             "silence, not a pass."}),
    ],
))


DECISIONS.append(Node(
    id="the-ruling-pipeline-is-the-packages-the-questions-are-the-apps",
    kind="decision",
    name="The ruling-card pipeline — carding, readability, grouping, settling, "
         "orphan reporting — lives here as craft/rulings.py, consumer-blind; an "
         "app keeps only what only it can know: its authored question texts, its "
         "grouping of findings into decisions, and its lanes",
    payload={
        "rationale":
            "2026-08-19, the architecture ruling on the first adopter's copy: the "
            "logic is load-bearing, the intent is not. Every function in the "
            "adopter's rulings module below its question texts — settle's binding "
            "of verdicts to the deck, the jargon-to-reading passes (plainer, "
            "readable, speak), the merges that never synthesize a sentence "
            "(dedupe, collapse), the sentence-safe cut, the drawing readers that "
            "name and sketch, the orphan report — was written against generic "
            "inputs (a drawing, findings, a rulings file) and carried lessons "
            "every adopter will need: an owner cannot rule on a walker's "
            "notation, a merged head must never invert a finding, an id drift "
            "must be said out loud. Held in one app, the second adopter forks "
            "the lessons and the third forks the fork. Dependencies point app → "
            "harness libs, never the reverse: the module reads a drawing plus "
            "findings plus a rulings file, and knows no app.",
        "consequence":
            "craft/rulings.py, with its own --alarm in the house style: every "
            "transformer faces a guilty case it must change and a clean case it "
            "must not (the element-names alarm caught its author's own wrong "
            "expectation on first run). The app-side residue is data handed in: "
            "GROUPS ((law, where-prefix) -> (group id, question)), QUESTIONS "
            "(authored per-law texts), plainer extras for the app's own note "
            "jargon, and the app's instruments feeding add_finding. The first "
            "adopter re-adopts by deleting everything else.",
    },
    children=[
        Node(id="the-first-adopters-rulings-module-read-line-by-line", kind="grounds",
             name="Every function in the first adopter's rulings module was read and classified",
             payload={"what": "2026-08-19: settle's binding of verdicts to the deck, the jargon-to-reading passes, the merges that never synthesize a sentence, the sentence-safe cut, the drawing readers, the orphan report — the logic is load-bearing and generic, the question texts are the app's.",
                       "where": "producer",
                       "gap": "One adopter. The split held for its module; a second adopter could put app-specific logic where this one put none."}),
        Node(id="alt-leave-it-in-the-adopter", kind="alternative",
             name="Leave the pipeline in the app that grew it; let the next "
                  "adopter copy the file",
             payload={"why":
                      "A copy forks the lessons: the next founder meets the raw "
                      "walker notation again, because the fix that made cards "
                      "readable lives in a repo their app does not read. The "
                      "estate exists to make a defect fixed once fixed for every "
                      "adopter."}),
        Node(id="alt-put-it-in-the-judgment-surface", kind="alternative",
             name="Put the pipeline in the deck app that renders the cards",
             payload={"why":
                      "The deck is one client family among several, a peer of "
                      "the apps it serves, and the pipeline must run in the "
                      "app's own CI with no door in sight. A pipeline living in "
                      "the renderer couples conviction to display — the exact "
                      "coupling the settle consultation was built to end."}),
        Node(id="alt-put-it-in-surface-tape", kind="alternative",
             name="Ship it with the walk artifact in surface-tape",
             payload={"why":
                      "The cards are the LAWS' loop: what they card are this "
                      "package's convictions, and stand/exempt/fix is doctrine "
                      "about how a law's red may be answered. surface-tape "
                      "carries evidence, not doctrine; the rulings consult the "
                      "drawing and the laws, both of which live here."}),
    ],
))


DECISIONS.append(Node(
    id="only-the-owner-exempts",
    kind="decision",
    name="An adjudicator may rule `fix` and `stand`; `exempt` is the escalation - the split "
         "is not confidence, it is whether the verdict removes evidence",
    payload={
        "rationale":
            "'The checks convict; only the owner rules' was written when the owner was the "
            "only reader who could rule at all. That is no longer true, and the rule as "
            "written spends the one scarce reviewer on the wrong cards. The verdicts are not "
            "equally dangerous to delegate, and the axis is not how sure the adjudicator "
            "sounds. `fix` leaves the red standing until the code moves - the verdict is an "
            "instruction, the red is its own check, and a wrong one is corrected by the next "
            "run. `stand` leaves the red standing, acknowledged - it hides nothing either. "
            "`exempt` is the one verdict that makes an instance STOP COUNTING: it removes "
            "evidence, permanently, and a wrong exempt is invisible afterwards because the "
            "thing that would have shown it is the thing that was silenced. So the narrowed "
            "contract is: the checks convict, an adjudicator rules, and only the owner "
            "exempts.",
        "consequence":
            "Cards ruled `fix` or `stand` are settled by the adjudicator and recorded with "
            "what they rested on - the finding, the drawing, the law - as any ruling is. A "
            "card whose answer is `exempt` is not ruled: it is escalated, and the person's "
            "queue holds only decisions that make something invisible, which is a small "
            "fraction of cards and the fraction worth their attention. Two conditions carry "
            "over unchanged, and they are what keep a delegated ruling checkable: a ruling "
            "names what it rested on, and a ruling whose finding no longer exists is "
            "reported rather than left standing - the pipeline's orphan check already does "
            "this, and it is now load-bearing rather than tidy.",
    },
    children=[
        Node(id="the-rule-was-written-when-the-owner-was-the-only-reader", kind="grounds",
             name="'The checks convict; only the owner rules' outlived the condition that made it true",
             payload={"what": "It was written when the owner was the only reader who could rule at all. The verdicts are not equally dangerous to delegate: `fix` leaves the red standing until the code moves, so the verdict is an instruction and the red is its own check.",
                       "where": "producer",
                       "gap": "An argument from how the verdicts differ, not an observation of a delegated ruling going wrong. No exempt has yet been wrongly granted, because none has been delegated."}),
        Node(id="alt-the-owner-rules-everything", kind="alternative",
             name="Keep the contract as written: every card, whatever its verdict, waits for "
                  "the owner",
             payload={"why":
                      "The queue fills with `fix` and `stand` - technical readings of a law "
                      "against a drawing, which an adjudicator settles as well or better - "
                      "and the exempts, the only cards that need a person, wait behind them. "
                      "A review queue that costs more than it decides stops being read, and "
                      "then nothing is ruled at all."}),
        Node(id="alt-the-adjudicator-rules-everything", kind="alternative",
             name="Delegate all three verdicts, exempt included, and escalate nothing",
             payload={"why":
                      "An exempt silences the check that would have caught the exempt. It is "
                      "the one verdict whose error cannot be found by running the tools "
                      "again, and in the record a wrong one is indistinguishable from a sound "
                      "one. Delegating it trades a bounded cost - a person reading a few "
                      "cards - for an unbounded and undetectable one."}),
        Node(id="alt-escalate-on-low-confidence", kind="alternative",
             name="Let the adjudicator rule whatever it is sure of and escalate the rest",
             payload={"why":
                      "Confidence is the wrong axis, and picking it would put the queue in "
                      "the adjudicator's gift. The dangerous card is a CONFIDENT exempt, "
                      "which such a filter would keep; the harmless card is an unsure `fix`, "
                      "which it would escalate. What the verdict does to the evidence is a "
                      "property of the verdict, knowable in advance, and it does not move "
                      "with how the reasoning happens to feel."}),
    ],
))


DEBTS = [
    Node(
        id="triggers-are-prose-so-applicability-cannot-be-computed",
        kind="debt",
        name="A law says when it applies in a sentence a person reads, so nothing can "
             "compute which laws bind a README, an error message or an answer in a terminal",
        payload={
            "what_it_costs":
                "Every law carries a `trigger` in prose - 'any interface with a control that "
                "commits something', 'the project ships documentation meant to be read long "
                "after it is written'. That is right for a person deciding whether a law "
                "bears on their screen, and it makes selection unreproducible: each caller "
                "re-decides, and the only way to check an answer is to re-read ninety-one "
                "triggers. The prose drifts unseen for the same reason. 'The app coins "
                "domain concepts of its own' exists twice, once with an example and once "
                "without; 'the app's voice does work of its own' exists as both '(dry, "
                "terse, no explaining text)' and '(dry, warm, terse)'. One condition written "
                "four ways, and no check can see it, because free text cannot be compared.",
            "why_it_is_not_paid":
                "It is a vocabulary change across every law and a publish. The cheap "
                "alternatives are worse than waiting: selecting by keyword picks laws whose "
                "own statements name a different surface, and mapping trigger prose to "
                "condition ids by table is the same matching under a better name - "
                "hand-authored once per string, drifting from the triggers the moment either "
                "side is edited.",
        },
        params={
            "distinct_trigger_strings": Quantity(
                value=55, unit="string", provenance="verified", grounded=True,
                source="counted over the 91 laws, 2026-08-22: 55 distinct trigger strings, "
                       "of which the six commonest cover 66 laws. The long tail is where the "
                       "duplicates hide - a closed set would have about twenty entries, and "
                       "near-duplicates would collide on one id instead of coexisting"),
        },
        children=[
            Node(id="discharge-a-trigger-is-an-expr", kind="discharge",
                 name="A trigger becomes an expression over a declared context, and the "
                      "substrate solves it",
                 payload={"route":
                          "This substrate already evaluates exprs over declared data - that "
                          "is what a ledger rule IS, and craft has been carrying prose where "
                          "it could carry an expression. Declare the conditions an artifact "
                          "can have (has_committing_control, ships_documentation, "
                          "reports_work_as_done, is_translated, runs_on_a_phone), let each "
                          "law state the expression it fires under, and applicability "
                          "becomes solve(trigger, context): computed, reproducible, arguable "
                          "against the artifact's own declaration. Two checks come free that "
                          "are impossible today - a law whose trigger names no known "
                          "condition can never be selected and goes red, and two conditions "
                          "meaning the same thing collide on one id."}),
        ],
    ),
    Node(
        id="the-practice-family-cites-nothing",
        kind="debt",
        links={"rests_on": ["the-process-is-ruled-too"]},
        name="PARTLY DISCHARGED 2026-08-22 - the catalogue exists (docs/practice-sources.md) "
             "and its first source is censused whole; thirteen laws still cite nothing",
        payload={
            "what_it_costs":
                "the-laws-grew-by-mining-not-by-bleeding is true of the interface family and "
                "false of this one. Those laws came from docs/sources.md - a survey chosen by "
                "authority and falsifiability, category-exhaustive on purpose so coverage is "
                "chosen rather than accidental. The practice laws came from defects: each one "
                "is real, and each one is a house rule until something outside this repo says "
                "it too. `a-law-cites-a-source` says exactly that on five of them, and the "
                "publish-practice gate carries the red. The cost is not tidiness. A house "
                "rule cannot be argued with from outside, cannot be checked against a source "
                "that moved, and gives an adjudicator nothing to reason from when a card asks "
                "whether the law was really broken.",
            "why_it_is_not_paid":
                "The survey is done and the mining is not. docs/practice-sources.md ranks "
                "nine sources by authority and falsifiability, records the three gaps found "
                "(delegating a decision; context leaking between records; the longevity "
                "companion paper, paywalled and unread), and censuses TWO sources - the IPCC "
                "guidance note whole (21 items: 3 covered, 8 owed, 10 set aside) and the "
                "existence-bias paper from its abstract, which enumerates its own studies (6 "
                "items: 4 covered). Two laws are cited from them, and what the sources do "
                "not cover is a number rather than a silence. Seven sources are unread and "
                "the five laws that were red are still red: none is about uncertainty or the "
                "status quo.",
        },
        params={
            "laws_without_authority": Quantity(
                value=13, unit="law", provenance="verified", grounded=True,
                source="quern brief, 2026-08-22: 13 laws RED on a-law-cites-a-source - 5 in "
                       "the practice family (the-users-attention-is-not-a-test-harness, "
                       "a-detour-is-announced-as-a-detour, deliberate-names-its-decision, "
                       "a-remainder-names-its-debt, a-census-is-read-from-its-source) and 8 "
                       "in the interface family, whose catalogue exists and simply has not "
                       "been read down to them"),
        },
        children=[
            Node(id="discharge-survey-the-practice-field", kind="discharge",
                 name="A practice source catalogue, surveyed the way docs/sources.md was",
                 payload={"route":
                          "Same two ranking criteria, stated as the bias-guards: authority "
                          "(standard, statute, or published empirical research - never fame) "
                          "and falsifiability (can a breach be observed). Category-exhaustive, "
                          "with the gaps recorded at the bottom, so a thin category is a "
                          "boundary chosen rather than one fallen into. Then every practice "
                          "law cited or marked owed, and the five reds go green or stay red "
                          "for a stated reason. Agans is next: it already roots four of "
                          "these laws in the prose and none of them in a citation."}),
        ],
    ),
    Node(
        id="corrections-outrun-the-laws",
        kind="debt",
        links={"rests_on": ["a-human-found-defect-enters-as-a-law"]},
        name="Defects a person found in one session, none of which any law forbids: a claim "
             "hedged past its own evidence, reasoning from one context written into "
             "another's record, two ways of spending a person's attention badly, and "
             "reading an existing state as a chosen one, and building a thing away from "
             "its subject. THREE ARE NOW LAWS, each cited; the rest are still only written "
             "here",
        payload={
            "what_it_costs":
                "a-human-found-defect-enters-as-a-law says every defect a person finds passes "
                "through one question before it is fixed: what valid generic rule did it "
                "break. These two were found, the question was asked, and the answer has "
                "nowhere to go. Both are recurring rather than incidental. HEDGING PAST "
                "VERIFICATION: a fact established by running something, then reported with a "
                "qualifier the evidence does not license - understating confidence is as much "
                "an error as overstating it, and it is the harder one to notice because it "
                "wears modesty. CONTEXT LEAKING INTO A RECORD: reasoning that belongs to the "
                "conversation written into a ledger entry, a code comment or a CI config, "
                "where it is inert for that reader at best and doctrine at worst. It has the "
                "same shape as the estate's standing rule that a library never names a "
                "client: the dependency points one way. A DECISION THE EVIDENCE SETTLED, "
                "ASKED ANYWAY: a question put to the person whose answer the same turn had "
                "just argued for. It is the exact sibling of "
                "[[the-users-attention-is-not-a-test-harness]] - that law refuses to delegate "
                "a CHECK the author can run, and this refuses to delegate a DECISION the "
                "author's own evidence makes; asking reads as deference, which is what makes "
                "it insidious. The same law's other edge: a question that IS the "
                "person's, put with no recommendation. One over-delegates the decision, "
                "the other under-prepares it. What reaches a person should be the "
                "smallest decision left, already reasoned to a proposal they can veto "
                "in one word - and once vetoed or agreed, acted on without asking "
                "again.",
            "why_it_is_not_paid":
                "All three want [[the-practice-family-cites-nothing]] paid first, or they "
                "enter as more house rules - and the third has a root already in this "
                "package's own reach, since `never-ask-twice` states the interface form of "
                "not asking for what you already hold. They mechanize very differently, and "
                "pretending otherwise would sink the one that works: "
                "hedging-past-verification has a tight predicate - a qualifier attached to "
                "something the same turn verified - while the other two have none yet and "
                "enter `owed`. The third's honest discriminator is whether the act was "
                "reversible, which no predicate knows: confirming before something hard to "
                "undo is right, and confirming before something the author could simply do "
                "and report is the defect. A check that fires wrongly is one everybody learns "
                "to skip, which costs more than the law was worth.",
        },
        params={
            "corrections_without_a_law": Quantity(
                value=7, unit="correction", provenance="verified", grounded=True,
                source="one session, 2026-08-22: hedging past verification (a parallel test "
                       "run called weaker evidence after its isolation had been checked), "
                       "context leaking into a record (that same caution written into an "
                       "app's ledger and CI), and a decision delegated after the evidence "
                       "settled it (asking whether to sweep, one paragraph after arguing "
                       "that building the vocabulary first would be guessing), and a "
                       "decision that WAS the person's put as a blank question (a name "
                       "and a shape, with no proposal attached), and a fifth of the "
                       "same after both were written down - asking permission to run a "
                       "command whose running was already agreed; and a sixth, defending "
                       "two existing names against a proposed one because they had 'earned' "
                       "their obscurity - one of them has no naming decision at all, so half "
                       "that justification was read off the fact that the name exists. SIX "
                       "in one session, and a seventh - a law-checker built inside "
                       "the project for pointers and hypotheses, now the law "
                       "a-thing-is-built-where-its-subject-lives. SEVEN in one session, "
                       "each recorded as it happened, and the record prevented none of "
                       "the ones after it. That is the number, and what it measures is "
                       "not the "
                       "author's carelessness but the gap between a law written and a "
                       "law enforced. It is the case for "
                       "[[the-deciders-run-by-hand]] stated in evidence rather than in "
                       "argument"),
        },
        children=[
            Node(id="discharge-cite-and-mechanize", kind="discharge",
                 name="Each law cited from the catalogue, the first mechanized and the rest "
                      "entered owed",
                 payload={"route":
                          "Calibrated-language guidance is the root for the first - it exists "
                          "to stop an author picking a confidence term the evidence does not "
                          "license, in either direction. Plain-language guidance (statutory, "
                          "public domain, already in the interface catalogue) is the root for "
                          "the second. The third's root is the service-design rule against "
                          "asking for what you already hold, which this package already "
                          "carries in its interface form as `never-ask-twice` - the practice "
                          "form is the same rule with the author on the other side of the "
                          "question. Falsifiers and triggers as any law, and the census says "
                          "covered or owed rather than the count of laws built."}),
        ],
    ),
    Node(
        id="the-ruling-track-is-decided-and-unbuilt",
        kind="debt",
        links={"rests_on": ["only-the-owner-exempts"]},
        name="only-the-owner-exempts says an adjudicator rules `fix` and `stand` and only "
             "`exempt` escalates - and craft/rulings.py still deals every card to the owner",
        payload={
            "what_it_costs":
                "The decision is recorded and nothing routes by it, so the queue still fills "
                "with the cards that need no person and the exempts still wait behind them. "
                "Every day it stays unbuilt is a day the reviewer's attention is spent on "
                "readings a tool settles - which is the way a review track dies, and the "
                "reason the decision was made.",
            "why_it_is_not_paid":
                "It needs a second surface as well as this one: the adjudicator's verdict has "
                "to be recorded with what it rested on (the finding, the drawing, the law), "
                "and an escalation has to reach the docket rather than a printed line. The "
                "pipeline half is here; the queue half is not.",
        },
        children=[
            Node(id="discharge-route-the-cards", kind="discharge",
                 name="Adjudicated verdicts recorded like any ruling; exempts escalated",
                 payload={"route":
                          "craft/rulings.py gains the verdict's author beside its words, so a "
                          "ruling says who settled it and on what; `exempt` from anyone but "
                          "the owner is refused and dealt on. The orphan check, which reports "
                          "a ruling whose finding no longer exists, stops being tidy and "
                          "becomes the thing that keeps a delegated ruling honest."}),
        ],
    ),
    Node(
        id="the-deciders-run-by-hand",
        kind="debt",
        links={"rests_on": ["the-process-is-ruled-too"]},
        name="The practice deciders convict a claims file somebody remembered to write and "
             "run - nothing reads what a turn actually produced, so a defect reaches a record "
             "before any law is consulted",
        payload={
            "what_it_costs":
                "craft.claims is real and it works, and it can only convict what was chosen "
                "for it: a claim recorded, in a file, by the same agent whose work is being "
                "judged. Every defect in [[corrections-outrun-the-laws]] was found by a "
                "person reading prose, and both had already reached a durable record - a "
                "ledger entry, a CI comment, a commit message - by the time they were named. "
                "Self-report catches the part already noticed, which is the part that needed "
                "no check.",
            "why_it_is_not_paid":
                "The cheap version is the wrong one. A check over the turn's own writing has "
                "to read what was actually produced - the diff AND the response, since the "
                "reasoning appears in the response first and sets in the record afterwards, "
                "and fail-fast puts the check at the earlier one. Only a mechanized law can "
                "hold a handback; a reading law can only be reported, and a reading law "
                "reported as a block is the noise that ends the practice.",
        },
        children=[
            Node(id="discharge-check-the-turn", kind="discharge",
                 name="A check over the turn's diff and its response, blocking on the "
                      "mechanized laws only",
                 payload={"route":
                          "The deciders read what the turn wrote rather than what it said "
                          "about itself. A correction from a person is the trigger to consult "
                          "the laws first and name the generic rule before anything is fixed, "
                          "which is a-human-found-defect-enters-as-a-law made unconditional "
                          "instead of remembered. Wants "
                          "[[the-practice-family-cites-nothing]] and "
                          "[[corrections-outrun-the-laws]] paid first: a harness that enforces "
                          "house rules enforces them faster, not better."}),
        ],
    ),
    Node(
        id="a-laws-scope-is-baked-into-its-statement",
        kind="debt",
        name="A law says WHERE it applies inside the rule itself, so a rule that is true of "
             "more than one surface can only ever be checked on one of them",
        payload={
            "what_it_costs":
                "sentences-stay-under-twenty-five-words is the worked example. Its statement "
                "says 'interface prose', its falsifier says 'a sentence in UI copy', and its "
                "citation is GOV.UK's Writing guidelines - content design rules for "
                "everything they publish, not for chrome. The law is NARROWER THAN ITS OWN "
                "SOURCE, and the narrowing lives in the two fields a check reads. So the doc "
                "lane, which wanted exactly this rule, could not legitimately run it and the "
                "only remedy available was deletion: the rule is gone from documentation "
                "even though its authority covers documentation. A law with a scope in its "
                "falsifier cannot be re-aimed, only rewritten.\n\n"
                ""
                "This is NOT [[triggers-are-prose-so-applicability-cannot-be-computed]], "
                "though the two compound. That debt says nothing can COMPUTE which laws bind "
                "a subject. This one says that even computed perfectly, a falsifier reading "
                "'UI copy' still cannot convict a README - the trigger would fire and the "
                "law would have nothing to say.",
            "why_it_is_not_paid":
                "It is a per-law reading and not a sweep. Scope in a falsifier is CORRECT "
                "wherever the law is genuinely about a screen (empty-state-never-contradicts) "
                "or genuinely physical (targets-are-thumb-sized); the defect is only where "
                "the law is narrower than the source it cites, and that question is one "
                "reading per law against nine sources. Re-scoping also changes what "
                "convicts, so each one is a publish and a re-run of every adopter's "
                "findings - which is why it wants doing deliberately, a law at a time, and "
                "never as a regex over the catalogue.",
        },
        params={
            "laws_scoped_in_statement_or_falsifier": Quantity(
                value=38, unit="law", provenance="verified", grounded=True,
                source="counted over the 91 laws, 2026-08-23: 38 carry a scope word "
                       "(interface, UI, screen, app, control, documentation, README) in "
                       "their statement or falsifier, 31 of them in the falsifier. How many "
                       "are narrower than their own citation is unread - that is the "
                       "reading this debt owes, and 38 is its upper bound, not its size"),
        },
        children=[
            Node(id="discharge-scope-lives-in-the-trigger", kind="discharge",
                 name="The rule is stated scope-free and the trigger carries the surface",
                 payload={"route":
                          "A law states what is true; its triggers state where. Twenty-three "
                          "laws already carry more than one trigger, so the shape needs no "
                          "invention - a law then serves every surface whose trigger fires, "
                          "and the doc lane gets the 25-word rule back by pointing at it "
                          "rather than by copying it. Each law is re-read against its "
                          "citation first: the source's scope is the law's scope, and a "
                          "narrowing the source does not make is the defect."}),
        ],
    ),
    Node(
        id="the-prose-lane-has-no-drawing",
        kind="debt",
        name="Markdown is reduced to units inside every decider instead of once, so each "
             "law brings its own reader and the reduction itself is what breaks",
        payload={
            "what_it_costs":
                "Every other lane reduces its subject ONCE and lets the laws read the "
                "reduction. An app authors a drawing; a claim is a record in a known shape. "
                "Markdown has neither, so craft/prose.py re-derives its units inside each "
                "check - five of the seven deciders open with the same walk over "
                "paragraphs(text), and paragraphs, sentences and _plain are called eighteen "
                "times across the module. A law wanting a unit nobody has built yet - a "
                "heading, a term, a code fence, a table - brings its own reader, so this "
                "lane's cost is linear in laws where the drawing's is flat.\n\n"
                ""
                "The reduction is also where it actually breaks, twice this week, and "
                "neither defect could produce a finding: a paragraph opening in bold was "
                "classified as a list item and never judged at all, and a run-in heading "
                "was counted as one of the paragraph's five sentences. A skipped paragraph "
                "leaves no finding for a decider to be wrong about, so the lane reported "
                "green over text it had never read. That is worse than checking nothing, "
                "and it is invisible to every check the lane runs on itself.",
            "why_it_is_not_paid":
                "The honest fix is a document's own drawing - its units declared as data, "
                "the way interface@ declares surfaces, elements and bindings - and that is a "
                "vocabulary addition and a publish, plus an authoring cost per document that "
                "no README pays today. The cheap version is worse than waiting: handing "
                "every decider one shared parse is the same per-decider reading with one "
                "fewer call, and it leaves the reduction exactly as unchecked as it was.",
        },
        children=[
            Node(id="discharge-a-document-declares-its-units", kind="discharge",
                 name="A document declares its units; deciders become predicates over them",
                 payload={"route":
                          "The reduction is authored and checkable rather than re-derived "
                          "per law, so a defect in it is something somebody can convict "
                          "instead of a silence. Deciders stop parsing and start deciding, "
                          "and a new law costs a predicate rather than a reader. The pins "
                          "standing in craft/prose.py's alarm - a bold-led paragraph is "
                          "read, a list item is not prose, a run-in heading is not a "
                          "sentence - are the reduction's first tests and say what the "
                          "declared units have to get right."}),
        ],
    ),
]
