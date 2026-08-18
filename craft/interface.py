"""interface@0.4.0 — an interface's denotation as data: what each screen shows, held
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
        "never changes; `intent` names the one job this element serves a person "
        "arriving to do (rename, create, configure — two intents co-visible is what "
        "one-surface-one-job convicts); `frequency: 'rare'` marks an act performed "
        "orders of magnitude less often than its surface is visited (create a "
        "household vs switch one — rare-action-folds-away expects such an element's "
        "`when` to pass through a disclosure state variable, so seeing it costs a "
        "deliberate act); `reveals` says this element appears on hover or focus "
        "rather than living on the surface — a dict {on: 'hover'|'focus', "
        "dismissable, hoverable, persistent}, the three booleans WCAG 1.4.13 and "
        "RGAA 10.13 read: it can be dismissed without moving the pointer, the "
        "pointer can travel onto it, and it stays until dismissed; `motion` says "
        "the act this element commits also listens to device motion — a dict "
        "{input: 'device-motion'|'tilt'|'shake', alternative: element-id, "
        "disableable} naming the conventional control that performs the same act "
        "and whether the listening can be turned off (WCAG 2.5.4, RGAA 13.12). "
        "These are the facts the compilable laws read — stated on "
        "the element because they are properties of the drawing, not observations of "
        "a screen, and each is a judgment a person makes ONCE at authoring time that "
        "the prover then enforces over every reachable state.",
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
        kind="term",
        description="One settled word of the app's own language: a domain concept "
        "with its canonical word per shipped language, the words the app must NOT "
        "use for it (`strays`: ad-hoc synonyms against the settled glossary — "
        "glossary-first's mechanical half), and the literal translations that read "
        "as translationese (`calques` — no-calque's mechanical half). Payload: "
        "`concept`, `words` ({lang: word}), `strays` ({lang: [words]}), `calques` "
        "({lang: [words]}). This is the language substrate's first kind — the "
        "drawing's move repeated for words: the glossary the law demands as an "
        "artifact becomes data a check can run over, and the judgment of WHICH "
        "words are settled is made once, at authoring time, by someone who speaks "
        "the language. The reading residue — a stray nobody pre-listed — stays "
        "with the judge and must shrink as terms accrete, or the convergence "
        "hypothesis's falsifier fires.",
    ),
    KindDef(
        kind="voice",
        description="The app's tone as data — the last of the language substrate's "
        "three kinds (term settled the nouns, the element's verb fact the acts; "
        "this settles the REGISTER). Payload: `never` ({lang: [words or short "
        "phrases]}) — vocabulary outside the app's declared voice, per language: "
        "exclamation-mark habits, slang, the third-person 'the user', mascot-speak. "
        "What it mechanizes is untranslatable-tone's and speaks-to-you's wordlist "
        "halves: a declared-off word found in a catalogue convicts. What it "
        "cannot hold — whether a metaphor LANDS — stays the reading residue, and "
        "the convergence hypothesis is falsified or defended by whether that "
        "residue keeps shrinking as voices accrete. Declared per app by whoever "
        "owns its voice, once.",
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
    KindDef(
        kind="media",
        description="A piece of media standing in an element — the content family "
        "the cost-blind censuses named unsayable (RGAA 4.x whole, WCAG 1.2.x "
        "whole) because the estate's own apps carry none of it. Payload: `temporal` "
        "(a timeline: video, audio, animation — False for a chart or an image map "
        "standing as non-temporal media), `live` (produced as it is consumed), "
        "`autoplay` (it starts by nobody's act — the fact WCAG 1.4.2 and RGAA 4.10 "
        "convict over when no reachable control stops it), `controllable` (play, "
        "pause, stop, volume reachable — the operability laws' subject), and "
        "`alternatives` (a list from: transcript, captions, audiodescription, "
        "sign-language, media-alternative — each naming an element id that carries "
        "it, so 'the transcript exists' is a reference the tree resolves, never a "
        "recollection). What stays with a reader is pertinence — whether the "
        "captions are any good — exactly as the censuses' judge rows say. Carried "
        "honestly: no compiler consumes this kind yet; what it settles today is "
        "expressibility, which is the census's whole question.",
    ),
    KindDef(
        kind="table",
        description="A data table's semantics as data — the seat RGAA 5.x had no "
        "vocabulary for. Payload: `complex` (a header structure a scope attribute "
        "cannot carry — the authoring-time judgment RGAA 5.1 demands a summary "
        "for), `layout` (a table used for arrangement, owed the OPPOSITE care: no "
        "data-table markup, linearizable source order). Its caption and summary "
        "are bindings or content among its children, so a table accounts for its "
        "words the way every element does. Header-cell association is the DOM "
        "instrument's half — markup, read where it renders; this kind carries the "
        "judgments only an author can make. Carried honestly: no compiler consumes "
        "it yet; it settles expressibility, the census's question.",
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
    # The voice, in the same demo domain: the checkout app's register, declared.
    Node(
        id="the-checkout-voice", kind="voice", name="the checkout app's register",
        payload={"never": {"en": ["oops", "awesome", "the user"],
                           "fr": ["oups", "génial"]}},
    ),
    # The glossary's canonical example, in the same demo domain: the settled word,
    # the ad-hoc synonym the app must not drift to, the literal translation that
    # reads as translationese.
    Node(
        id="the-basket-term", kind="term", name="the basket",
        payload={"concept": "basket",
                 "words": {"en": "basket", "fr": "panier"},
                 "strays": {"en": ["cart"], "fr": ["chariot"]},
                 "calques": {"fr": ["corbeille d'achat"]}},
    ),
    # The media and table kinds, in the same demo domain: the product's demo video
    # with its declared alternatives, and the sizing chart as a data table.
    Node(
        id="the-product-video", kind="media", name="the product demo video",
        payload={"temporal": True, "live": False, "autoplay": False,
                 "controllable": True,
                 "alternatives": [{"kind": "transcript",
                                   "element": "ex-video-transcript"},
                                  {"kind": "captions",
                                   "element": "ex-video-captions"}]},
    ),
    Node(
        id="the-sizing-chart", kind="table", name="the sizing chart",
        payload={"complex": False, "layout": False},
        children=[
            Node(id="ex-table-caption", kind="binding",
                 payload={"key": "sizes.caption", "role": "text"}),
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
    version="0.4.0",
    description="An interface's denotation as data: surfaces, elements, bindings, "
                "content, denials, witnesses, media, tables and (one day) "
                "constraints — the "
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
