"""interface@0.1.0 — an interface's denotation as data: what each screen shows, held
in a tree that rules can traverse, laws can compile against, and a render layer can be
generated from.

Why this exists
---------------
The craft laws (craft@) judge what an interface SAYS; until now the thing they judged
was a walk — prose transcribed from a running app, sampled surface by surface. The
walk answers "what did it show that day". It cannot answer "what does it show in every
state", and most of what a screen shows is a function of finite state: where you are,
what the world holds, which language. This package is that function's vocabulary — the
denotational half of an interface twin. The operational half (state variables and
navigation actions) already has a home in épure's model idiom; an interface tree's
`when` conditions are written over exactly those state variables, which is the seam
the two halves join at.

With the denotation as data, three things become mechanical that were readings:

  - the decidable laws COMPILE against it (see craft/compile.py) into invariants an
    exhaustive prover checks over every reachable state, each violation carrying the
    minimal click-path that reaches it;
  - totality becomes a solvable query — every element accounts for its text, every
    bound key resolves, in every language, in every state — which no finite walk can
    ever establish;
  - the static parts of a render layer can be GENERATED from the tree, at which point
    drift between the drawing and the app is impossible by construction for whatever
    is generated, and checking retreats to what only a browser can decide.

What stays outside, said plainly: the meaning of strings (a metaphor that lands as
jargon compiles to nothing — those laws keep their judge), and the browser's own
contribution (layout engines and font metrics enter only as sampled evidence, which
is what conformance walks are for).

Why it lives here
-----------------
Beside craft@, and not by convenience: a law's trigger names properties of an app,
and this vocabulary is those properties' formalism. "Any count is shown to a person"
stops being prose the moment an element declares `count_var` — the law's relevance
becomes a mechanical filter over the tree, which is the half of judgment that never
needed a reader. The laws and the formalism they bind to version together or they
drift apart.
"""

from __future__ import annotations

from quern import KindDef, Node, Rule
from quern.library import CounterExample, Package

VOCABULARY = [
    KindDef(
        kind="surface",
        description="A place a person can be in the app — a tab, a sheet, a fold. Its "
        "payload `when` states reachability as an expression over the twin's state "
        "variables (the operational half's vocabulary), so 'which states show this "
        "surface' is a solvable question, never a recollection. Children: the elements "
        "it shows, and the witness that ties it to sampled evidence.",
    ),
    KindDef(
        kind="element",
        description="One thing a surface shows. Payload `when` narrows visibility "
        "beyond the surface's own condition (the two AND together); `sentence` marks "
        "prose that reads as one sentence rather than a list of labels; `action` names "
        "the act this control commits; `count_var` names a numeric state variable "
        "rendered inline, and `fixed_plural` that it stands beside a noun whose number "
        "never changes. These are the facts the compilable laws read — stated on the "
        "element because they are properties of the drawing, not observations of a "
        "screen.",
    ),
    KindDef(
        kind="binding",
        description="The provenance of rendered text: a catalogue key this element's "
        "words come from. Payload `key` (the catalogue's own name for the string), "
        "`role` (text | template | options — a template's holes are filled by other "
        "bindings or controls), `slot` (which hole, when this binding fills one). A "
        "flattened walk throws provenance away; the binding is where it lives instead, "
        "and it is what a generator emits into the render layer so the key names exist "
        "in exactly one artifact.",
    ),
    KindDef(
        kind="content",
        description="User or household data standing in an element — chore titles, "
        "people's names — text no catalogue carries. Payload `source` says where it "
        "comes from. An element bound to content instead of keys still accounts for "
        "its words, which is what the totality rule below demands: prose from nowhere "
        "is the blind spot no checker can see.",
    ),
    KindDef(
        kind="denial",
        description="This element's text asserts that some action is moot — 'there is "
        "nothing to add'. Payload `action` names the act denied. A denial is a legal "
        "description (apps ship them; the founding scar was one); what convicts it is "
        "the compiled empty-state law, when any reachable state shows the denial "
        "beside a control offering the very action.",
    ),
    KindDef(
        kind="witness",
        description="How sampled evidence names this surface: payload `name` (the "
        "surface-tape record name a walk deposits) and `lanes` (the population lanes "
        "whose walks can show it). The bridge from the drawing to the world — proof "
        "runs over the tree, but the tree's licence is renderings checked against it, "
        "and a surface no tape can name is a surface no walk can testify for.",
    ),
    KindDef(
        kind="constraint",
        description="A geometry or layout claim over elements — fits, does not "
        "overlap, stays visible at every width in a range — stated as an expression "
        "over element boxes. Minted now as the seat where layout stops being sampled "
        "three viewports at a time and becomes a solved interval query; carried "
        "honestly: no solver consumes this kind yet, and a kind without a consumer is "
        "a promise, not a capability.",
    ),
]

RULES = [
    Rule(
        name="an-element-declares-what-it-shows",
        kind="element",
        description="Every element accounts for its words: at least one binding (a "
        "catalogue key) or one content node (named data). Text from nowhere is the "
        "one thing neither a prover nor a drift check can ever convict, because "
        "nothing claims it — so the vocabulary refuses it at authoring time.",
        expr="len(nodes('binding', self)) + len(nodes('content', self)) >= 1",
    ),
    Rule(
        name="a-surface-is-witnessable",
        kind="surface",
        description="Every surface names how a walk would read it. Proof over the "
        "drawing is licensed by renderings checked against the drawing; a surface "
        "with no witness has opted out of that check silently, and silent is the one "
        "thing an opt-out may never be.",
        expr="len(nodes('witness', self)) >= 1",
    ),
]

# --- examples, and the counter-examples that prove the guards guard -----------------
#
# The example app is the estate's canonical one: the checkout screen whose empty state
# contradicted its own button — vigil's demo, the founding scar retold. Described here
# in its HEALTHY form; the scar variant lives in the `denial` kind's description, and
# convicting it is the compiler's job, not the vocabulary's.

EXAMPLES = [
    Node(
        id="a-checkout-surface",
        kind="surface",
        name="the checkout screen",
        payload={"when": "surface == 'checkout'"},
        children=[
            Node(id="ex-witness", kind="witness",
                 payload={"name": "tab:checkout", "lanes": ["empty", "seeded"]}),
            Node(id="ex-empty-text", kind="element", name="the empty-basket line",
                 payload={"when": "basket_count == 0", "sentence": True},
                 children=[
                     Node(id="ex-empty-binding", kind="binding",
                          payload={"key": "basket.empty_title", "role": "text"}),
                 ]),
            Node(id="ex-add-control", kind="element", name="the add button",
                 payload={"action": "add"},
                 children=[
                     Node(id="ex-add-binding", kind="binding",
                          payload={"key": "action.add_item", "role": "text"}),
                 ]),
            Node(id="ex-basket-rows", kind="element", name="the basket rows",
                 payload={"when": "basket_count >= 1"},
                 children=[
                     Node(id="ex-rows-content", kind="content",
                          payload={"source": "the items the person put in the "
                                             "basket"}),
                 ]),
            Node(id="ex-fits", kind="constraint",
                 name="the empty-basket line never overlaps the add button",
                 payload={"claim": "at every viewport width the app supports, the "
                                   "boxes of these two elements are disjoint",
                          "over": ["ex-empty-text", "ex-add-control"]}),
        ],
    ),
    # The same screen as it actually shipped, before the fix: a LEGAL drawing of a
    # defective app. The vocabulary describes what is; the compiled empty-state law is
    # what convicts this description, in every reachable state that shows both
    # elements — which for this one is the initial state itself.
    Node(
        id="the-july-checkout",
        kind="surface",
        name="the checkout screen, as it shipped with the scar",
        payload={"when": "surface == 'checkout'"},
        children=[
            Node(id="ex-july-witness", kind="witness",
                 payload={"name": "tab:checkout", "lanes": ["empty"]}),
            Node(id="ex-july-empty", kind="element",
                 name="the empty line that denied the button beneath it",
                 payload={"when": "basket_count == 0", "sentence": True},
                 children=[
                     Node(id="ex-july-binding", kind="binding",
                          payload={"key": "basket.empty_title", "role": "text"}),
                     Node(id="ex-july-denial", kind="denial",
                          payload={"action": "add"}),
                 ]),
            Node(id="ex-july-add", kind="element", name="the add button",
                 payload={"action": "add"},
                 children=[
                     Node(id="ex-july-add-binding", kind="binding",
                          payload={"key": "action.add_item", "role": "text"}),
                 ]),
        ],
    ),
]

COUNTER_EXAMPLES = [
    CounterExample(
        rule="an-element-declares-what-it-shows",
        because="an element with prose and no provenance — no key, no named data. "
                "Nothing can check words nothing claims: the drift check has no key "
                "to resolve, the totality query has no entry to refuse, and the text "
                "ships as the one part of the screen outside every net",
        node=Node(
            id="text-from-nowhere", kind="element",
            name="a caption that just appears",
            payload={"when": "basket_count == 0", "sentence": True},
        ),
    ),
    CounterExample(
        rule="a-surface-is-witnessable",
        because="a surface that never says how a walk would read it — its proof can "
                "never be licensed by a rendering, and the opt-out is silent, which "
                "is the failure mode this whole line of work exists to abolish",
        node=Node(
            id="unwitnessable-surface", kind="surface",
            name="a settings screen no tape can name",
            payload={"when": "surface == 'settings'"},
            children=[
                Node(id="cx-el", kind="element", name="a well-formed element",
                     children=[
                         Node(id="cx-el-binding", kind="binding",
                              payload={"key": "settings.title", "role": "text"}),
                     ]),
            ],
        ),
    ),
]

INTERFACE_PACKAGE = Package(
    name="interface",
    version="0.1.0",
    description="An interface's denotation as data: surfaces, elements, bindings, "
                "content, denials, witnesses and (one day) constraints — the "
                "formalism the craft laws' triggers bind to, the tree their "
                "decidable half compiles against, and the artifact a render layer's "
                "static parts are generated from so that drift is impossible by "
                "construction for whatever is generated. The operational half of the "
                "twin (state variables, navigation actions) stays with épure's model "
                "idiom; `when` expressions here are written over its state "
                "variables, which is the seam the two halves join at.",
    publisher="poietic.studio",
    requires=[],
    vocabulary=VOCABULARY,
    rules=RULES,
    examples=EXAMPLES,
    counter_examples=COUNTER_EXAMPLES,
)
