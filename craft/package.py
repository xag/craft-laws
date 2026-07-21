"""craft@0.1.0 — the laws of interface and copy, as data a rule can go red on.

Why this is a package and not a checklist
-----------------------------------------
A checklist is prose, and prose does not fire. The laws below were first written as bullets in
a markdown file, and that file contained this sentence:

    "A law with no source is a hypothesis, and is labelled so. Three of the ten are. Source them
     or delete them; do not let them harden into laws by sitting here."

That sentence is true, and it will go on being true, silently, for as long as anybody leaves it
there — which is the exact failure the ledger package exists to prevent, reproduced inside the
artifact that teaches it. So the laws are data now, and "a law names its source" is a rule that
goes red rather than a bullet nobody runs.

Why it requires `ledger`
------------------------
Because an unsourced law *is* a ledger hypothesis, exactly and not by analogy: a belief held
provisionally, carrying the observation that would kill it. There is no reason to re-invent that
vocabulary, and every reason not to — `invest` re-authored the ledger's kinds and Home Hub rolled
its own, and the whole point of a package is that the third project does not make the same
mistake a third time.

So a law's `authority` is a `grounding` Quantity: grounded when somebody reputable has actually
said this, ungrounded when it is my opinion wearing a lab coat. Then `nothing-unsound-passes-a-
gate` — the load-bearing rule the ledger already ships — asks the publication gate whether any
uncited law is about to travel through it. It does not need to be told what a law is. It only
asks whether the thing resting on it was ever checked.

SITING. This package does not live in quern's source, and that is deliberate. `ledger@0.1.0` does,
and its own docstring calls that wrong: a package inside the substrate means refining a
vocabulary requires a *quern release*, which is the pathology quern exists to dissolve (xag/quern#19).
Putting a set of UX laws in there would reproduce that error knowingly, and would mean a better
citation for a button label waits on a substrate release. So `craft` roots itself in its own
Library, in its own repo, on its own clock — which is what #19 will make ordinary, and which is
possible today only because quern already lets local vocabulary win over a package's.

`craft` is therefore the SECOND independent consumer wanting that channel. One is a special
case. Two is evidence.
"""

from __future__ import annotations

from quern import KindDef, Node, Rule
from quern.library import CounterExample, Package
from quern.provenance import Quantity
from quern.tree import PackageRef

VOCABULARY = [
    KindDef(
        kind="law",
        description="A claim about interface or copy that holds across apps, domains and "
        "languages — not a preference. It carries an `authority` param, which is grounded when "
        "a reputable source has actually said this and ungrounded when it is somebody's taste. "
        "An ungrounded law is not deleted: it is carried, visibly, as the ledger carries a debt, "
        "and the gate below will not let it pass as though it were settled.",
        links={"supersedes": "the law this one replaces, if any"},
    ),
    KindDef(
        kind="citation",
        description="Where the law actually comes from: a publisher, a title, a URL, and — the "
        "part that matters — the QUOTE. A citation without the words is a citation nobody can "
        "check, and an unfalsifiable appeal to authority is worse than an honest opinion.",
    ),
    KindDef(
        kind="falsifier",
        description="The observation that constitutes a violation. Stated so that a verdict can "
        "be `fail` and not merely 'I do not like it'. A law whose violation cannot be observed "
        "is a taste, and tastes do not belong in a package.",
    ),
    KindDef(
        kind="trigger",
        description="A property of an app's INTENT or scenarios that switches this law on. This "
        "is what makes the laws free to the author: they write what the app is for, and the "
        "relevant laws arrive. A law with no trigger is a checklist item, and checklists are "
        "ignored — which is why the rule below insists on one.",
    ),
    KindDef(
        kind="sighting",
        description="A real defect this law actually caught, in a real app, on a real screen. "
        "Evidence, not decoration: a law that has never caught anything is a law nobody should "
        "trust, and one that has caught the same thing twice has earned its place.",
    ),
]

RULES = [
    Rule(
        name="a-law-can-be-violated-observably",
        kind="law",
        description="A law whose breach cannot be observed cannot produce a verdict, and a "
        "verdict is the only thing a law is for. Without this, a package of laws is a package "
        "of opinions with a version number.",
        expr="len(nodes('falsifier', self)) >= 1",
    ),
    Rule(
        name="a-law-is-switched-on-by-something",
        kind="law",
        description="Laws arrive because the app's intent called for them. A law that applies "
        "to everything applies to nothing: it becomes a checklist item, and a checklist item is "
        "read once and never again.",
        expr="len(nodes('trigger', self)) >= 1",
    ),
    Rule(
        name="a-law-cites-a-source",
        kind="law",
        description="The rule this package exists for. These laws were first written from "
        "memory, by the agent that had just been burnt by the defects they describe — which is "
        "the same act as inventing a translation glossary and handing it to a translator as "
        "binding, and it is the very thing GLOSSARY-FIRST forbids. A law that cannot name who "
        "said it is a hypothesis. It may be carried, and it will be red, and that is the "
        "honest state of it.",
        expr="len(nodes('citation', self)) >= 1",
    ),
]

# --- examples, and the counter-examples that prove the guards guard -----------------
#
# quern will not publish a package whose rules have no examples, and it stages each counter-example
# ALONE so the named rule has to fail on that node and not on some other defect. Which is the
# same demand this whole file was written under: not "does the method explain the defects you
# already found", but "does it reject something it should".

EXAMPLES = [
    Node(
        id="a-well-formed-law",
        kind="law",
        name="A control's label describes the action it performs",
        params={"authority": Quantity(value=1, unit="law", provenance="cited", grounded=True,
                                      source="GOV.UK Design System, Button")},
        children=[
            Node(id="ex-falsifier", kind="falsifier",
                 payload={"claim": "A button labelled with a noun, or with the name of the "
                                   "section it sits in."}),
            Node(id="ex-trigger", kind="trigger",
                 payload={"when": "any interface with a control that commits something"}),
            Node(id="ex-citation", kind="citation", name="GOV.UK Design System — Button",
                 payload={"url": "https://design-system.service.gov.uk/components/button/",
                          "quote": "Write button text in sentence case, describing the action "
                                   "it performs."}),
            Node(id="ex-sighting", kind="sighting", name="chores, the member sheet",
                 payload={"what": "A section headed 'Absence' whose submit button was also "
                                  "labelled 'Absence'."}),
        ],
    ),
]

COUNTER_EXAMPLES = [
    CounterExample(
        rule="a-law-cites-a-source",
        because="a law that names no authority — which is an opinion with a version number, and "
                "is exactly how this package's own laws were first written",
        node=Node(
            id="feels-wrong-to-me", kind="law",
            name="Buttons should be blue",
            params={"authority": Quantity(value=1, unit="law", provenance="asserted",
                                          grounded=False, source="I think so")},
            children=[
                Node(id="cx1-f", kind="falsifier", payload={"claim": "a button that is not blue"}),
                Node(id="cx1-t", kind="trigger", payload={"when": "any interface"}),
            ],
        ),
    ),
    CounterExample(
        rule="a-law-can-be-violated-observably",
        because="a law whose breach cannot be observed can never produce a verdict, so it is a "
                "taste and not a law",
        node=Node(
            id="be-elegant", kind="law",
            name="The interface should feel elegant",
            params={"authority": Quantity(value=1, unit="law", provenance="cited", grounded=True,
                                          source="a design book")},
            children=[
                Node(id="cx2-t", kind="trigger", payload={"when": "any interface"}),
                Node(id="cx2-c", kind="citation", name="A design book",
                     payload={"url": "https://example.invalid", "quote": "Be elegant."}),
            ],
        ),
    ),
    CounterExample(
        rule="a-law-is-switched-on-by-something",
        because="a law that nothing switches on is a checklist item, and a checklist item is "
                "read once and never again",
        node=Node(
            id="always-applies", kind="law",
            name="Contrast must meet WCAG AA",
            params={"authority": Quantity(value=1, unit="law", provenance="cited", grounded=True,
                                          source="WCAG 2.2")},
            children=[
                Node(id="cx3-f", kind="falsifier",
                     payload={"claim": "a contrast ratio below 4.5:1 on body text"}),
                Node(id="cx3-c", kind="citation", name="WCAG 2.2",
                     payload={"url": "https://www.w3.org/TR/WCAG22/",
                              "quote": "Contrast (Minimum): 4.5:1."}),
            ],
        ),
    ),
]


CRAFT_PACKAGE = Package(
    name="craft",
    version="0.1.1",
    description="The laws of interface and copy, as checkable data: each carrying the "
                "observation that would convict it, the property of an app's intent that "
                "switches it on, the source that authorises it, and the real defects it has "
                "actually caught. An uncited law is an ungrounded param, so the ledger's own "
                "gate can refuse to let it travel as though it were settled. The point is not "
                "to write the best practice down — a style guide already does that, and a style "
                "guide cannot fire.",
    publisher="poietic.studio",
    requires=[
        # Versions pinned exactly, by doctrine. Since xag/quern#19, ledger@ and
        # grounding@ are their own authoring repos; craft names the versions it
        # builds on rather than importing their Python to read a constant.
        # 0.1.1 moves both to the current pair — ledger@0.5.0 carrying grounding@1.1.0,
        # whose provenance contracts each describe themselves instead of sharing one
        # line. No kind, rule or example changed; a closure that mixes ledger versions
        # is a diamond, so a consumer wanting the legible contracts needs craft to name
        # the same ones.
        PackageRef(name="ledger", version="0.5.0"),
        PackageRef(name="grounding", version="1.1.0"),
    ],
    vocabulary=VOCABULARY,
    rules=RULES,
    examples=EXAMPLES,
    counter_examples=COUNTER_EXAMPLES,
)
