"""The craft tree: craft@0.1.0's semantics, with the laws hanging under them."""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401 -- the natives; the packages themselves arrive by pin
from quern import Quern
from quern.library import consume

from quern import Node

from .laws import GATE, LAWS

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
    quern.root.children = [*LAWS, *DECISIONS, GATE]
    return quern


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