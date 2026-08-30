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
        name="Every defect a person finds — feedback, an issue, a ruling on a proposed "
             "conviction — passes through one question before it is fixed: what valid generic "
             "rule did it break? The answer lands here, as a law or a refinement, so the fix "
             "ships with a regression test for every app that adopts the package, not only the "
             "app where it was found",
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
                "Every law before this entered after a defect shipped: it taught its law, and "
                "the law joined. Honest, but biased — a package grown only from one estate's "
                "own defects covers that estate's habits. Four mining passes (accessibility, "
                "government/forms/copy, localization, empirical/content) worked a catalogue "
                "built to be category-exhaustive, with the gaps recorded as gaps and an overlap "
                "map so each law cites its strongest root: WCAG for the rule, GOV.UK for the "
                "operational wording, Baymard for the tested statistic, CLDR under everything "
                "plural. Every citation quote was fetched and verified verbatim — one pass "
                "caught the fetch tool FABRICATING a spec sentence and re-verified against raw "
                "source, which is the whole argument for quotes over paraphrases. Where "
                "clusters collided (error messaging arrived from three roots), the collision is "
                "merged and recorded in the law's note.",
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
            Node(id="the-rejected-alternative-was-rebuilt", kind="grounds",
                 name="2026-08-25: the rejected alternative was rebuilt, and no "
                      "check fired",
                 payload={"what":
                          "A pattern set over the turn's final text shipped under "
                          "alt-keep-them's own defence, reworded. 70 false alarms "
                          "in 176 hits; removed the same day by the owner reading "
                          "the summary - every gate passed, since each reads "
                          "records, laws or the thing itself, and none compares "
                          "new work against this file's decisions.",
                          "where": "user-surface",
                          "gap": "one rebuild observed; the estate-wide rebuild "
                                 "rate is unmeasured"}),
        ],
    ),
    Node(
        id="the-critic-not-the-author-files-the-account",
        kind="decision",
        links={"rests_on": ["the-account-is-anchored-to-the-turns-record"]},
        name="The responding agent sees no account instruction: a session-end critic "
             "reconstructs the session's arguments and judges them, speaking only on "
             "conviction",
        payload={
            "rationale":
                "The inline design was measured against a full live session on "
                "2026-08-30: the instruction was injected 31 times (~15k tokens of "
                "identical text), 36 of 234 tool calls authored or repaired account "
                "files before counting their commits, the injected register "
                "contaminated the replies badly enough to need a standing style rule, "
                "every live conviction was an error OF the inline formalization, and "
                "the independent judge ruled 59 of 106 inline readings unsupported. "
                "The one benefit the injection was built for - same-turn repair - "
                "repaired paperwork, not answers. The critic design keeps everything "
                "that worked (anchoring against the transcript, the deciders, the "
                "adjudicator) and moves authorship to a fresh context at session end: "
                "craft/critic.py digests the dialogue, reconstructs accounts marked "
                "as reconstruction whose conclusions quote the reply's own sentences, "
                "and writes critique.md only when a decider convicts.",
            "consequence":
                "user_prompt_submit prints nothing and the settings entry is removed; "
                "SessionEnd spawns the critic with the account hook off; a turn with "
                "no accounts is the norm, so the zero-accounts line retired. "
                "Author-filed accounts remain first-class where an author chooses to "
                "file - the Stop check still judges them.",
        },
        children=[
            Node(id="the-measured-session", kind="grounds",
                 name="One full session measured under the inline design",
                 payload={"what": "31 injections, 36/234 tool calls on account "
                                  "upkeep, a style rule forced into the owner's "
                                  "global instructions, 13 live convictions all of "
                                  "them formalization errors, 59/106 readings "
                                  "unsupported by the independent judge.",
                          "where": "producer",
                          "gap": "One session, the same one that built the lane - "
                                 "the overheads of a session NOT building the lane "
                                 "it runs under are unmeasured and likely lower."}),
            Node(id="alt-instruct-the-author-inline", kind="alternative",
                 name="Keep injecting the instruction and filing during the turn",
                 payload={"why": "The measured costs above, against a same-turn "
                                 "repair benefit that fixed paperwork and never "
                                 "answers."}),
            Node(id="alt-no-account-lane", kind="alternative",
                 name="Drop the lane entirely",
                 payload={"why": "The anchoring checks caught seven real fidelity "
                                 "failures in one session - the lane pays where it "
                                 "is externally anchored, and the critic keeps "
                                 "exactly that half at zero cost to the session."}),
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
            "Fifteen done-claims cited green suites, deploy ids and log lines — producer-side "
            "every one, and none an observation of the surface a person touches. The estate "
            "already had the doctrine that would have caught it (instrument the boundary; "
            "replay the tape rather than re-derive what must have happened) and applied it to "
            "storage and HTTP while leaving the one boundary that mattered — the widget's — "
            "dark. A doctrine held in prose binds only where somebody remembers it. The remedy "
            "is the same one this repo already made for interfaces: state it as data with a "
            "falsifier, so the claim can be checked instead of trusted. Agans wrote four of the "
            "six in 2002; they are cited, because doing a known-catastrophic thing is worse "
            "than inventing a new one.",
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


DECISIONS.append(Node(
    id="the-calibration-vocabulary",
    kind="decision",
    name="The words that grade a finding are two closed scales, adopted from the IPCC "
         "note's own summary terms - evidence: limited, medium, robust; agreement: "
         "low, medium, high - and there is deliberately no confidence scale",
    payload={
        "rationale":
            "calibration-is-agreed-before-the-case demands the grading vocabulary be "
            "agreed in advance, and on 2026-08-24 the owner said: agree it. The scales "
            "are paragraph 8's own summary terms, not an invention, with each term "
            "bound to an observable so a grade is a fact about the record and not a "
            "mood. EVIDENCE: limited - one source or one run; medium - repeated runs "
            "or one independent replication; robust - the note's own bar, multiple "
            "consistent independent lines of high-quality evidence. AGREEMENT: low - "
            "a named dissent stands; medium - one judge and no dissent; high - "
            "independent judges concur. Confidence stays what this estate already "
            "enforces: a finding is stated as fact when the evidence settles it, or "
            "hedged by a NAMED unknown - the qualifier law's two positions - and "
            "never graded on a five-term scale.",
        "consequence":
            "Three of the tranche's graded laws become code the day this is agreed: "
            "a term outside these scales convicts under "
            "calibration-is-agreed-before-the-case, one dimension without the other "
            "convicts under validity-is-evidence-and-agreement, and a low grade "
            "without its reason convicts under "
            "low-confidence-is-reserved-and-explained. The scales are a closed set, "
            "so widening them is an edit to this decision, made deliberately, never "
            "a synonym slipped into a claim.",
    },
    params={
        "evidence_strength": Quantity(
            value=3, unit="term", provenance="cited", grounded=True,
            source="IPCC AR5 uncertainty guidance, paragraph 8: summary terms "
                   "'limited,' 'medium,' or 'robust'"),
        "agreement": Quantity(
            value=3, unit="term", provenance="cited", grounded=True,
            source="IPCC AR5 uncertainty guidance, paragraph 8: summary terms "
                   "'low,' 'medium,' or 'high'"),
    },
    children=[
        Node(id="alt-the-ipcc-confidence-scale", kind="alternative",
             name="Adopt the note's five-term confidence scale as well",
             payload={"why": "The census already ruled on it: set aside, because 'the "
                             "estate's finding is observed or not; a five-term scale "
                             "would invite invented middles.' That ruling stands - a "
                             "ruling outlives its turn - and the qualifier law "
                             "already gives confidence its two honest positions: "
                             "stated as fact, or hedged by a named unknown."}),
        Node(id="alt-counted-agreement", kind="alternative",
             name="Record agreement as counts of judges and dissents instead of terms",
             payload={"why": "More precise on paper and ceremony in practice: the "
                             "judges of a finding are rarely enumerable (a suite, a "
                             "person, a replay), and a count field nobody can fill "
                             "honestly is worse than a term bound to an observable. "
                             "The observables are in the definitions instead: a named "
                             "dissent, one judge, independent concurrence."}),
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
        name="PARTLY DISCHARGED 2026-08-25 - fifteen sources censused, and nine of the "
             "thirteen red laws were rooted 2026-08-25 in sources captured verbatim; "
             "three stay red, each with its reason in its own authority note",
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
                "What remains is capture, not survey: a-detour-is-announced-as-a-detour "
                "waits on the official ITIL 4 glossary text (paywalled, not in hand - "
                "secondary glossaries agree on the wording and are not the authority), "
                "type-stays-legible waits on the Apple HIG sentence its note describes, "
                "and a-view-arrives-whole has had no authority found that STATES the "
                "norm - its own note rules adjacent citations decoration. Deleting any "
                "of the three would lose a law that caught real defects to tidy a "
                "gate.",
        },
        params={
            "laws_without_authority": Quantity(
                value=3, unit="law", provenance="verified", grounded=True,
                source="run_rules over the tree, 2026-08-25: 3 laws RED on "
                       "a-law-cites-a-source - a-detour-is-announced-as-a-detour "
                       "(practice; ITIL 4 text not in hand), type-stays-legible "
                       "(Apple HIG text not in hand), a-view-arrives-whole (no "
                       "authority found stating the norm)"),
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
        links={"rests_on": ["a-human-found-defect-enters-as-a-law"],
               "blocked_by": ["the-practice-family-cites-nothing"]},
        name="Defects a person found in one session, none of which any law forbids: a claim "
             "hedged past its own evidence, reasoning from one context written into "
             "another's record, two ways of spending a person's attention badly, and "
             "reading an existing state as a chosen one, and building a thing away from "
             "its subject. THREE ARE NOW LAWS, each cited; the rest are still only written "
             "here",
        payload={
            "what_it_costs":
                "a-human-found-defect-enters-as-a-law says every defect a person finds passes "
                "through one question before it is fixed: what valid generic rule did it break. "
                "These two were found, the question was asked, and the answer has nowhere to "
                "go. Both are recurring rather than incidental. HEDGING PAST VERIFICATION: a "
                "fact established by running something, then reported with a qualifier the "
                "evidence does not license - understating confidence is as much an error as "
                "overstating it, and it is the harder one to notice because it looks like "
                "caution. CONTEXT LEAKING INTO A RECORD: reasoning that belongs to the "
                "conversation written into a ledger entry, a code comment or a CI config, where "
                "it is inert for that reader at best and doctrine at worst. It has the same "
                "shape as the estate's standing rule that a library never names a client: the "
                "dependency points one way. A DECISION THE EVIDENCE SETTLED, ASKED ANYWAY: a "
                "question put to the person whose answer the same turn had just argued for. It "
                "is the exact sibling of [[the-users-attention-is-not-a-test-harness]] - that "
                "law refuses to delegate a CHECK the author can run, and this refuses to "
                "delegate a DECISION the author's own evidence makes; asking reads as "
                "deference, which is what makes it insidious. The same law's other edge: a "
                "question that IS the person's, put with no recommendation. One over-delegates "
                "the decision, the other under-prepares it. What reaches a person should be the "
                "smallest decision left, already reasoned to a proposal they can veto in one "
                "word - and once vetoed or agreed, acted on without asking again.",
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
        links={"rests_on": ["only-the-owner-exempts"],
               "blocked_by": ["epure:no-kind-records-an-adjudication"]},
        name="DISCHARGED 2026-08-25 - settle routes by the decision: a delegated fix or "
             "stand settles with what it rested on, a delegated exempt is refused and "
             "dealt on as data, and the orphan check keeps a delegated ruling honest",
        payload={
            "what_it_costs":
                "The decision is recorded and nothing routes by it, so the queue still fills "
                "with the cards that need no person and the exempts still wait behind them. "
                "Every day it stays unbuilt is a day the reviewer's attention is spent on "
                "readings a tool settles - which is how a review track stops being used, and "
                "the reason the decision was made.",
            "why_it_is_not_paid":
                "PAID in the pipeline, with the queue half's boundary stated rather than "
                "crossed. A ruling carries `by` and, when delegated, `rested_on`; settle "
                "takes the owner's name (opt-in - the first alarm run of the change "
                "escalated the owner's own hand against a real consumer's rulings, and "
                "the owner declaration is exactly the thing only the app knows) and "
                "routes: delegated fix and stand settle with what they rested on, a "
                "delegated ruling resting on nothing is refused, and a delegated exempt "
                "returns to the deck carrying `escalate` with the reason in words. The "
                "escalation is DATA on the deck; which queue it reaches - the docket, an "
                "app's own deck - is each consumer's wiring, which is where the queue "
                "half always belonged: this module knows no app.",
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
        name="DISCHARGED 2026-08-25 - the hook sees the turn whose work reached no "
             "record, the intake rate is measured, and prose is checked through its "
             "derived drawing: structure as data, every validation in code",
        payload={
            "what_it_costs":
                "craft.claims is real and it works, and it can only convict what was chosen "
                "for it: a claim recorded, in a file, by the same agent whose work is being "
                "judged. Every defect in [[corrections-outrun-the-laws]] was found by a "
                "person reading prose, and both had already reached a durable record - a "
                "ledger entry, a CI comment, a commit message - by the time they were named. "
                "Self-report catches the part already noticed, which is the part that needed "
                "no check. "
                "WHAT IS PAID, 2026-08-25, and what the first measurement said. The diff "
                "half is code: claims_hook.silent_repos names, at Stop, every repository "
                "the turn wrote to whose record it never touched - information, not a "
                "conviction, throttled so it says each silence once. And craft.intake "
                "measures the bias over git: across twelve repos, the share of working "
                "commits filing a claim in the same commit runs from zero to about a "
                "quarter, with most repos near three percent - a floor, since same-turn "
                "separate-commit filings count as silence, and the first number the "
                "reporting-bias law ever had. THE RESPONSE HALF: prose is checked "
                "through its DRAWING (craft/drawing.py). The author derives, as data, "
                "which sentences assert a claim and of which kind; code then validates "
                "with zero false positives - the drawing is pinned to the source text "
                "by hash so an edit without re-derivation is stale, every node quotes "
                "its sentence verbatim so an invented reading is unanchored, and every "
                "node either references the filed claim (kind checked against the "
                "record) or is convicted as unfiled. Three earlier attempts stand "
                "recorded as what NOT to build: a word list that judged (wrong seven "
                "in eight), a per-turn model (33-47 seconds, non-deterministic), a "
                "word list that proposed (70 false alarms in 176, removed the day it "
                "was built - the owner's standard: no word lists over prose, no "
                "mechanisms with false positives). The owner's direction of "
                "2026-08-25 set the design: the ambition to check prose stands; "
                "constraints specify the solution, they do not cancel the goal.",
            "why_it_is_not_paid":
                "PAID, with the fallible layer named rather than hidden: the "
                "derivation is authored, not computed, so it can under-report - the "
                "same direction as the diff-side informant, and measured the same "
                "way, by a later audit of the same source against its drawing. What "
                "the checks themselves assert is exact: staleness, anchoring, and "
                "the join to the record are decided from data, and a wrong drawing "
                "is a committed, quotable artifact anyone can refute and correct on "
                "the record.",
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
    Node(
        id="the-prose-lane-contradicts-the-word-list-decision",
        kind="debt",
        links={"rests_on": ["a-word-list-is-a-reading-not-a-mechanization"]},
        name="PAID IN FULL 2026-08-27 - this repository decided that a law checked by "
             "matching words never holds a handback, the documentation lane gated the "
             "build on three such laws for a week, they were demoted to reporting on "
             "2026-08-24, and the checks were deleted outright on 2026-08-27",
        payload={
            "what_it_costs":
                "The decision this rests on says it in one line, with its own measurement "
                "behind it: a law checked by matching words in prose is unmechanized, does not "
                "get a decider, and never holds a handback.\n\ncraft/prose.py held seven "
                "checks. Four are structural and not in scope. THREE WERE THE SHAPE THE "
                "DECISION NAMES: time anchors (six words), positional references (four "
                "patterns), trailing conditions (two). Each chose which sentences its law "
                "covered by reading them, and CI ran the lane, so all three held a "
                "handback.\n\nThe size is in the grounds below; the contradiction is what this "
                "entry is for.",
            "why_it_is_not_paid":
                "PAID IN FULL 2026-08-27. The 2026-08-24 route kept them reporting "
                "because deleting them leaves three documentation laws with no check; "
                "the owner ruled that an inert check is worth removing and that a law "
                "without a mechanism is the accurate position, not a gap. Mechanizing "
                "them still wants [[the-prose-lane-has-no-drawing]].",
        },
        children=[
            Node(id="three-of-seven-read-meaning-from-words", kind="grounds",
                 name="Three of the lane's seven checks decide subjecthood by reading "
                      "prose, and the build gates on all three",
                 payload={"what": "The three checks and their patterns are named in "
                                  "the entry above; CI ran the lane, so a hit failed "
                                  "the build.",
                          "where": "producer",
                          "gap": "A reading of the module as it stood. It establishes "
                                 "the contradiction and measures nothing."}),
            Node(id="the-three-fire-three-times-in-eighty-seven-files", kind="grounds",
                 name="Measured over the estate before demoting: three hits in 87 files, "
                      "and two of the three are the laws quoting the words they forbid",
                 payload={"what": "time-anchors 2, positional 1, trailing 0. Two hits are "
                                  "LAWS.md: 'never now, no new, no currently' and 'never "
                                  "above, below, or as mentioned earlier'. On the 31 "
                                  "READMEs the build gates, one hit, arguably true.",
                          "where": "producer",
                          "gap": "The measurement gives the size, not whether a word "
                                 "list can ever be a mechanization."}),
            Node(id="discharge-remove-them-outright", kind="discharge",
                 name="PAID FURTHER 2026-08-27: the three word lists are deleted, not "
                      "demoted, at the owner's direction",
                 payload={"route":
                          "The owner ruled deletion: inert is a reason to remove, not "
                          "to keep. The three checks are gone with their word tables, "
                          "the READINGS split and holds_the_build(). unruled() and LANGS "
                          "went too - they existed because a word list goes SILENT in an "
                          "unruled language, and every remaining decider fails the other "
                          "way, convicting more rather than less. Four structural "
                          "deciders remain; the three LAWS stay, unmechanized. The lane's "
                          "one true positive in 87 files was a clause reading 'thin as "
                          "it currently is'; reworded for the word list it became "
                          "'thin as it is', which means nothing, and was deleted."}),
            Node(id="discharge-measure-then-demote-or-mechanize", kind="discharge",
                 name="PAID: measured, then demoted to a radar - they report and the "
                      "exit status ignores them",
                 payload={"route":
                          "DONE 2026-08-24. The number came first, as the decision's "
                          "own did, and said nearly inert rather than dangerous, so the "
                          "route was the radar and not deletion. "
                          "craft/prose.py now splits its checks into those "
                          "that may hold a handback and those that may only report; "
                          "the three word lists are in the second set, print under a "
                          "reading heading that says they hold nothing, and no longer "
                          "reach the exit status. What is NOT paid is the deeper half: "
                          "they are still word lists, and mechanizing them properly "
                          "still wants [[the-prose-lane-has-no-drawing]]."}),
        ],
    ),
    Node(
        id="a-ruling-has-no-stated-lifetime",
        kind="debt",
        links={"rests_on": ["corrections-outrun-the-laws"]},
        name="Nothing says how long a person's ruling binds, so an agent reopened one on a "
             "two-word instruction and abandoned another on a single question, in "
             "consecutive turns",
        payload={
            "what_it_costs":
                "[[corrections-outrun-the-laws]] holds how a decision should REACH a "
                "person: the smallest one left, reasoned to a proposal they can veto in a "
                "word, neither over-delegated nor under-prepared. It says nothing about "
                "what happens after they answer, and both failures live there.\n\n"
                "REOPENED BY A GENERAL INSTRUCTION. A law's scope had been ruled on "
                "explicitly, twice. A later proposal flagged that re-scoping would reverse "
                "that ruling and said it was the owner's call. The owner answered a "
                "two-word go, and it was read as authorising the one thing already "
                "refused. An instruction that names nothing specific reopens nothing "
                "specific, and the agent that had just identified the conflict is the one "
                "that should know it.\n\n"
                "ABANDONED BY A QUESTION. In the next turn, a position that had been "
                "reasoned and built was withdrawn entirely on one clarifying question, "
                "before any counter-argument arrived. The owner named the cost precisely: "
                "you cannot tell a conviction from an accommodation, so arguing with the "
                "agent stops being worth the time. A position that folds on being asked "
                "about carries no information when it holds.\n\n"
                "The two look like opposite vices and are one gap. A ruling with no stated "
                "lifetime can be treated as expired whenever it is convenient and as "
                "overturned whenever it is questioned, and both readings are available to "
                "an agent that wants to move.",
            "why_it_is_not_paid":
                "No root found. The nearest law this package holds is `never-ask-twice`, "
                "whose practice form roots the corrections above, and it does not reach "
                "either edge: one is not asking when the answer was already given, and the "
                "other is not defending an answer already reached. Configuration "
                "management and change control state something adjacent - a baseline holds "
                "until a change is authorised - and whether that transfers to a ruling "
                "made in conversation is a reading nobody has done. Minting without the "
                "root is how this family got into debt.",
        },
        children=[
            Node(id="both-edges-in-consecutive-turns", kind="grounds",
                 name="Both failures in consecutive turns of one session, 2026-08-24",
                 payload={"what": "A law's triggers were widened past an explicit ruling "
                                  "on a two-word instruction, and reverted. In the next "
                                  "turn a built and tested proposal was withdrawn on one "
                                  "question, and had to be restored after the owner said "
                                  "the folding was itself the failure.",
                          "where": "user-surface",
                          "gap": "One session, one agent. It shows the two edges are "
                                 "available at once; it does not show which is commoner "
                                 "or whether a stated lifetime would prevent either."}),
            Node(id="discharge-root-the-lifetime-or-drop-it", kind="discharge",
                 name="Find the root that states how long a decision binds, or record that "
                      "none exists and stop looking",
                 payload={"route":
                          "The candidate lane is change control: a baseline holds until a "
                          "change request is authorised, and the authorisation names what "
                          "it changes. If a standard states that in a form whose breach is "
                          "observable, the law follows and both edges are its falsifier. "
                          "If the reading finds nothing transferable, that is a result "
                          "too, and this entry says so rather than carrying a law nobody "
                          "sourced."}),
        ],
    ),
    Node(
        id="a-laws-denominator-is-uncounted",
        kind="debt",
        name="A law's record counts its catches and not its trials - how many candidate "
             "laws were tried and dropped, and how many convictions a ruling later stood "
             "down, are counted nowhere, so a surviving law's sightings cannot be "
             "discounted for selection",
        payload={
            "what_it_costs":
                "The catalogue trusts a law by its sightings - a law that has never caught "
                "anything is a law nobody should trust - which is the numerator of a rate "
                "whose denominator nobody keeps. Laws are mined from corrections and "
                "censuses, candidates are tried and dropped, and the drops leave no count; "
                "rulings stand findings down and no projection folds those back onto the "
                "law that convicted. The estate has paid for the missing number once "
                "already, at small n: a turn checker calibrated at zero false positives "
                "over 33 turns was later found wrong about seven times in eight, and the "
                "selection story stayed invisible until a person read the cleared cases. "
                "Every multiple-testing correction the finance literature offers (deflated "
                "statistics, reality checks) needs exactly the number this catalogue does "
                "not keep: how many were tried.",
            "why_it_is_not_paid":
                "The records that would carry the counts exist in pieces - dropped "
                "candidates sit in the tree's git history and in the corrections debt's "
                "prose, rulings are data, sightings ride on the laws - but no projection "
                "reads them together, and back-counting drops from git history is a "
                "reading, not a computation. The cheap version, a hand-typed trials field "
                "per law, is the self-report this repository refuses elsewhere: a count "
                "whose deciding input the counted party chooses reports those choices.",
        },
        children=[
            Node(id="discharge-the-denominator-is-a-projection", kind="discharge",
                 name="Trials and overturns are computed from records that already exist, "
                      "never typed",
                 payload={"route":
                          "Candidate laws enter as recorded candidates from the day this "
                          "discharges - the corrections debt already holds them as data - "
                          "so tried-and-dropped becomes countable from the tree itself; a "
                          "ruling that stands a finding down is joined back to the "
                          "convicting law by id. Both counts are computed beside sightings "
                          "wherever sightings are shown. No field an author fills; "
                          "grounding is the join existing and being read."}),
        ],
    ),
]

DECISIONS.append(Node(
    id="the-turn-account-lane-is-removed",
    kind="decision",
    name="The turn-account lane is removed: every verdict it produced tracked words "
         "the graded author chose, and its live hooks never convicted a real turn",
    payload={
        "rationale":
            "Built 2026-08-27 at the owner's direction to check the argument a turn "
            "makes: AIF nodes filed per turn, a controlled proposition language parsed "
            "by Lark, entailment decided by Z3, a prompt hook asking for the filing and "
            "a Stop hook judging it. The owner refuted five versions in one day, each "
            "the same defect one field deeper: scheme was a label; mood and figure were "
            "two labels; the proposition was a record of typed parts; the parser and "
            "rules were hand-rolled; and with all of that replaced, `ground` and "
            "`strength` still were words the author picked. The closing observation: "
            "the only filing ever convicted was authored by the checked party with the "
            "incriminating strength typed in by that party; relabelling one word "
            "(producer to given), propositions unchanged, passed the same argument; and "
            "across the whole day the live Stop hook convicted nothing. Lark and Z3 "
            "computed real consequences, but only of choices - translation, scheme, "
            "ground, strength - the graded author made alone. A grader fed only by the "
            "graded party's labels reports those labels.",
        "note":
            "The ambition stands; it is quality-harness's argument hypothesis, whose "
            "kill-criteria concern an honestly extracted graph and are untouched by "
            "this. What this paid for is the constraint one step earlier, the same "
            "boundary Yuan et al. 2016 reported: the lanes that keep working here "
            "(claims, prose, drawing) each hold a filing to something its author "
            "cannot retro-fit - a field's shape, a source hash, a verbatim quote - "
            "and the account had no such anchor anywhere.",
    },
    children=[
        Node(id="alt-verify-the-grounds-too", kind="alternative",
             name="Add a sixth layer that checks `ground` against the claims record",
             payload={"why": "Each of the five fixes moved the author-chosen word one "
                             "field deeper and bought no independence; the translation "
                             "into the controlled language would still be the author's, "
                             "so the regress does not terminate inside self-report."}),
        Node(id="alt-keep-lark-and-z3", kind="alternative",
             name="Keep the grammar and the entailment module as an unconsumed library",
             payload={"why": "Nothing consumes them, and a second mechanism standing "
                             "near a subject drifts from the first - the reason the "
                             "scope-rulings pin was withdrawn although it worked. git "
                             "keeps the code; a future design with an independent "
                             "grader can recover it by commit."}),
    ],
))

DECISIONS.append(Node(
    id="the-account-is-anchored-to-the-turns-record",
    kind="decision",
    links={"rests_on": ["the-turn-account-lane-is-removed"]},
    name="The account lane returns anchored: every grounded premise quotes, verbatim, "
         "an artifact its author does not write - tool results for producer and "
         "stand-in, the user's own messages for given and user-surface",
    payload={
        "rationale":
            "The removal entry states the constraint: a checker fed only by the "
            "checked party's labels reports those labels. The rebuild supplies the "
            "anchor the first lane lacked, the same one the working lanes already "
            "use: craft/record.py reads the session transcript - written by the "
            "harness, not by the author - into two pools, and "
            "a-ground-is-a-quotation-from-the-record convicts any grounded premise "
            "whose quote the right pool does not hold, any grounded premise with no "
            "quote, and any grounded premise checked with no record supplied. The "
            "closing defect of the removed lane is closed by construction: "
            "relabelling a counted observation as `given` now demands words the "
            "user actually typed. Run against this session's real transcript (538 "
            "tool results, 73 user texts): an honest filing passes, a fabricated "
            "quote convicts, the laundered founding case convicts on the anchor, "
            "and the honest founding case convicts on strength.",
        "residue":
            "Three things stay with a reader, stated so the pass report cannot "
            "overclaim: selection (quoting the one line that helps), translation "
            "into the controlled language, and a staged record - a command run to "
            "print a wanted sentence anchors, but sits in the record beside its "
            "output where an audit can see it. Silence stays information, never a "
            "conviction.",
    },
    children=[
        Node(id="alt-an-independent-model-grader", kind="alternative",
             name="Have a second model derive the account and grade the turn",
             payload={"why": "The removed prose grader measured 33-47 seconds a turn "
                             "and non-deterministic verdicts. An independent AUDITOR "
                             "of selection bias, run off the hot path over committed "
                             "accounts, remains the natural next instrument - as an "
                             "audit, not a gate."}),
        Node(id="alt-trust-the-labels", kind="alternative",
             name="Keep grounds and strengths as authored fields, checked for shape only",
             payload={"why": "The removed lane, whole: five refutations in one day "
                             "showed each shape-check of an authored label relocates "
                             "the defect one field deeper."}),
    ],
))

DECISIONS.append(Node(
    id="the-account-laws-are-sourced-whole-or-absent",
    kind="decision",
    links={"rests_on": ["the-account-is-anchored-to-the-turns-record"]},
    name="Every law the account deciders convict under is registered with a fetched "
         "citation and maps into a source adopted whole; the invented warrant and "
         "ground tables are deleted, and a rule added by hand is a red build",
    payload={
        "rationale":
            "Ordered by the owner on 2026-08-27: remove ours, replace with sourced laws, and "
            "never adopt a rule in isolation - when you source, you fetch them all, and CI goes "
            "red otherwise. The Greenwell taxonomy paper was fetched whole and captured "
            "(docs/sources/), and fetching it corrected a law: Arguing from Ignorance ships its "
            "own exemption for a documented search, which the decider had omitted - adopting "
            "the conviction without the exemption is authoring a stricter rule under the "
            "source's name. The warrant table (sign/example/authority ceilings) and the ground "
            "table are gone; two grading rules died here in one day, both refuted by the owner: "
            "a count-based cap (premise nodes are not evidence lines), then a demanded basis "
            "field, killed by the criterion the audit then applied to every decider - a rule "
            "ensures no reasoning flaw remains, never that everything said is justified. The "
            "machine now polices no grade beyond scale membership; what it convicts are flaws: "
            "fabricated grounds, circularity, failed or unexhibited deductions, unanswered "
            "attacks on live support, undocumented absence warrants, support that is only "
            "attack. craft/account_laws.py is the registry; tests/test_law_registry.py, run by "
            "CI, refuses an unregistered decider id, an uncited law, a cherry-picked census "
            "row, a decider on a judge-routed row, a dead registry entry and a missing capture. "
            "Its first run caught its own scanner miscounting law constructors as convictions, "
            "which is what an alarm is for.",
        "note":
            "The protocol is the source-a-law skill (.claude/skills/); the gate is "
            "its checkable half. What no gate checks, stated: whether a census "
            "route honestly reads the source, and whether a quote's context "
            "supports the law drawn from it - the captures are committed so a "
            "reader can refute both from the file.",
    },
    children=[
        Node(id="alt-keep-ours-as-honest-reds", kind="alternative",
             name="Keep the invented tables, carried red under a-law-cites-a-source",
             payload={"why": "The carried-red state exists for laws awaiting a "
                             "capture, not for numbers nobody published; the owner "
                             "ruled the new family starts clean or not at all."}),
        Node(id="alt-paraphrase-when-fetch-fails", kind="alternative",
             name="Cite with a paraphrase when the paper resists fetching",
             payload={"why": "A paraphrase dressed as a quotation is the fabrication "
                             "the citation discipline exists against; the one capture "
                             "that is a reading (AIF) says so in its own source "
                             "string instead."}),
    ],
))

DECISIONS.append(Node(
    id="the-second-source-is-the-founding-catalogue",
    kind="decision",
    links={"rests_on": ["the-account-laws-are-sourced-whole-or-absent"]},
    name="Sophistical Refutations is adopted whole - thirteen fallacies, the "
         "author's own complete enumeration - and the Greenwell adoption is "
         "finished: every row either census routes as decidable now has a decider",
    payload={
        "rationale":
            "Ordered by the owner on 2026-08-27: source known patterns of reasoning "
            "flaw and detect them. Two moves, both under the whole-source rule. "
            "Greenwell's last decidable row, Pseudo-Precision, is mechanized over "
            "declared quantities: a conclusion whose tolerance is tighter than "
            "every input's claims precision from nowhere. And the founding "
            "catalogue is censused whole (craft/census_sophistici.py, 13 rows): "
            "three rows were already covered - Consequent and Ignoratio elenchi by "
            "the entailment law, Begging the question by circularity - and the one "
            "newly decidable row, non-cause, is mechanized by re-asking Z3 with "
            "each premise removed: a premise the verified entailment holds without "
            "was inserted as though the conclusion depended upon it, which is "
            "Aristotle's own definition. Declared deductions also stop needing a "
            "form field: any count of parseable premises goes to Z3 directly, and "
            "the syllogism name is only a label when the shape has one.",
        "note":
            "The honest count across both adoptions: Greenwell 6 of 33 decidable, "
            "all six now live; Sophistici 4 of 13, all four live (three covered, "
            "one new). Eight of the thirteen SR rows are linguistic or "
            "meaning-bound and stay with a reader; the census says which and why.",
    },
    children=[
        Node(id="alt-adopt-a-modern-compendium-instead", kind="alternative",
             name="Adopt Walton's scheme catalogue or the IEP fallacy files next",
             payload={"why": "Both are real and both are large - sixty schemes, two "
                             "hundred entries - and a census that big authored in "
                             "one sitting would be a reading nobody checked. The "
                             "quality-harness kill-criterion on Walton's critical "
                             "questions is the standing reason to do it properly "
                             "later, at thirty questions tried against a real "
                             "graph."}),
        Node(id="alt-detect-without-censusing", kind="alternative",
             name="Add the two deciders without adopting their sources whole",
             payload={"why": "The sourcing rule exists because a source mined for "
                             "one convenient rule is a word list one level up; "
                             "thirteen rows is an afternoon, and the census is what "
                             "makes the 4-of-13 an honest number instead of a "
                             "highlight reel."}),
    ],
))

DECISIONS.append(Node(
    id="one-formalism-carries-the-schemes",
    kind="decision",
    links={"rests_on": ["the-account-laws-are-sourced-whole-or-absent"]},
    name="Defeasible inference enters as data in one structure - premises, "
         "exceptions, assumptions - and every critical question flows through the "
         "existing defense decider; the decider count for the whole catalogue is one",
    payload={
        "rationale":
            "Ordered by the owner on 2026-08-27 after the audits: one formalism "
            "that covers all, never per-law ad-hoc interpretations. The Carneades "
            "encoding of Walton, Reed & Macagno 2008 proves the uniformity - 24 "
            "schemes, 41 critical questions, one shape - so craft/schemes.py reads "
            "the committed capture as the catalogue (never a copy in code, and the "
            "gate holds parser, census and capture equal), and the account gains "
            "two small things: an RA may claim scheme walton:<id> with premises "
            "filling the scheme's slots, and a critical question is a CA on the "
            "inference carrying the exception's slot. Undercuts were the one "
            "extension the defense decider needed - an attack on a live inference "
            "counts like an attack on live support - so raising and answering "
            "critical questions is judged by machinery that already existed. One "
            "new law only: a scheme invoked without exhibiting its premises is its "
            "warrant asserted, not shown - the unexhibited-deduction flaw one "
            "level up. The registry gate convicted this law before it was "
            "registered, which is the gate doing its job on its own author.",
        "note":
            "Burden of proof is not modeled: Carneades distinguishes exceptions "
            "(defeat when raised) from assumptions (proponent discharges when "
            "questioned), and here both defeat when raised and unanswered. Stated "
            "rather than approximated silently; the distinction becomes meaningful "
            "only with an evaluation semantics over unknowns, which nothing here "
            "computes yet.",
    },
    children=[
        Node(id="alt-forty-one-deciders", kind="alternative",
             name="Mechanize each critical question as its own decider",
             payload={"why": "Forty-one hand-written interpretations of one "
                             "uniform structure, each a place to drift; the "
                             "structure was the source's own answer."}),
        Node(id="alt-full-aspic-semantics", kind="alternative",
             name="Implement ASPIC+ preferences and burden-aware evaluation now",
             payload={"why": "Nothing files preference or burden data yet; "
                             "machinery for data that does not exist is the "
                             "withdrawn-pin shape. The grounded-defense fragment "
                             "in use is the part with inputs."}),
    ],
))

DECISIONS.append(Node(
    id="the-account-has-a-grammar-and-the-reply-has-a-residual",
    kind="decision",
    links={"rests_on": ["one-formalism-carries-the-schemes"]},
    name="The account's syntax is a JSON Schema validated before any soundness "
         "decider runs, and the reply's unchecked share is extracted at Stop as a "
         "named residual instead of an invisible one",
    payload={
        "rationale":
            "The owner's checklist of 2026-08-27, closed item by item. Syntax "
            "before soundness: account.schema.json is the grammar - node types, "
            "field enums, additionalProperties refusing what the format does not "
            "admit (mood and figure among it) - validated per node in check_shape, "
            "so hand-written ifs stopped being the format's definition. The "
            "residual: a node may claim a reply sentence with `says`, verbatim "
            "under the anchor's own canonical form aimed the other way, and the "
            "Stop hook writes residual.json beside the accounts - sentence count, "
            "covered count, the unclaimed sentences, and any says-quote the reply "
            "does not contain. Information, never a conviction: formalizing part "
            "of a reply is the honest common case, and the point is that the "
            "unchecked part is named. The docs follow the data: the account "
            "family renders into LAWS.md from the registry, and the README "
            "carries the lane.",
        "note":
            "Coverage is claimed by the author and measured by matching, so "
            "under-claiming inflates the residual and never deflates it - the "
            "safe direction. Sentence-splitting reuses craft.prose; a says-quote "
            "matching is case-sensitive by the same canonical form as the record "
            "anchor.",
    },
    children=[
        Node(id="alt-schema-as-refusal", kind="alternative",
             name="Reject the whole file on the first schema violation",
             payload={"why": "A syntax error in one node would silence every "
                             "soundness decider on the rest - the alarm's guilty "
                             "fixture depends on junk and judgment coexisting, and "
                             "so does an honest partial filing."}),
        Node(id="alt-residual-as-conviction", kind="alternative",
             name="Convict a reply whose residual is non-empty",
             payload={"why": "Paperwork by the owner's own criterion: an "
                             "unformalized sentence is not a demonstrated flaw, "
                             "and a hook that nags every turn is a hook that gets "
                             "switched off."}),
    ],
))
