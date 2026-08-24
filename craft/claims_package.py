"""claims@ — a session's assertions as data: the record the practice laws fire on.

Minted beside craft@ the way interface@ was: craft@ holds the LAWS about the work, and
this holds the DENOTATION of what a session asserts — the claim kinds, the evidence
grading, the measurement protocol, the agreed calibration scales. The wire format stays
one JSON object per claim in a repo's claims.jsonl; this package is that format's
meaning, published and pinned so a consumer can name the version it writes and a reader
can know what a record meant on the day it was filed.

The split is grounding@'s: MEANING IS DATA, CHECKING IS CODE. The deciders
(craft/claims.py) convict in code at the Stop hook, and no rule here duplicates a
payload-reading decider — the rules below are the structural minimum a tree-shaped
claim must satisfy, and the deciders are the real gate. A test in this repository holds
the two together: the package's kinds and the deciders' kinds must be the same set, so
the meaning and the check cannot drift apart silently.

The vocabulary this package carries GREW OFF-LEDGER first: the kinds and fields
accumulated in craft/claims.py as code while the published-kind convergence series
counted zero, and the owner asked the right question — how did the vocabulary have to
grow — before this publish made the growth visible. That history is the package's own
first lesson: vocabulary that lives only in code is vocabulary the estate's instruments
cannot see.
"""

from __future__ import annotations

from quern.library import CounterExample, Package
from quern.tree import KindDef, Node, Rule

VOCABULARY = [
    KindDef(
        kind="done",
        description="Work reported finished. Carries `text` (the claim, one utterance "
        "about one state of the world) and evidence children. The law it answers to: "
        "done is observed where the user stands, so evidence that is all producer-side "
        "does not close it, and a stand-in closes it only with a named gap. Optional "
        "grade facts on any claim kind: `evidence_strength` (limited | medium | "
        "robust) and `agreement` (low | medium | high) — the calibration vocabulary "
        "agreed 2026-08-24 and recorded at the-calibration-vocabulary in this "
        "repository's ledger; both dimensions or neither, and the low end carries "
        "`why_low`. The scales are closed: widening one is an edit to that decision, "
        "never a synonym in a record.",
    ),
    KindDef(
        kind="fixed",
        description="A defect reported repaired. Carries `text`, `reproduced_first` "
        "(the run that showed the failure before the change — without it the fix is a "
        "theory wearing a verb), `changes` (ONE candidate; two candidates on one claim "
        "mean the outcome names no cause), and evidence like a done-claim.",
    ),
    KindDef(
        kind="diagnosis",
        description="A cause reported identified. Carries `text`, `prior_theories` "
        "(how many explanations preceded this one) and `new_observation` (the signal "
        "separating this theory from the last — required whenever prior_theories is "
        "nonzero, because two explanations with no new observation between them is "
        "guessing). A diagnosis MAY say `resembles` — the known failure shape the "
        "symptom matched, an honest disclosure that the reasoning ran on "
        "similarity — and saying it obliges `base_rate`: how often that cause "
        "family actually occurs here, computable from the filed diagnoses "
        "themselves, with 'unknown: why' the honest value where the record is "
        "thin. The striking match is weighed against the common cause, per "
        "a-cause-is-weighed-by-how-often-not-only-how-alike. A diagnosis of a "
        "law going red also carries the `red` record: check, culprit, "
        "tool_named, session.",
    ),
    KindDef(
        kind="detour",
        description="A report resolved by a different route. Carries `text` and "
        "`still_broken` — what remains wrong. A detour that does not name what stays "
        "broken is a fix-claim in costume.",
    ),
    KindDef(
        kind="confirmation",
        description="An agreement filed as a claim: you are right, the premise holds, "
        "that is the cause. Carries `text` and `checked` — what was actually run or "
        "read before agreeing. The root is the IPCC note's paragraph 2: a finding is "
        "explained by a traceable account, and an agreement is a finding at the "
        "highest confidence there is. An unchecked confirmation reads as deference, "
        "which is what makes it insidious; assent that rests on nothing is worth "
        "nothing when it agrees.",
    ),
    KindDef(
        kind="measurement",
        description="An accuracy, coverage, hit-rate or calibration figure filed as a "
        "claim, carrying STARD 2015's items as fields: `corpus` (how assembled — "
        "exhaustive, random, or convenience), `size_declared_before`, `prespecified`, "
        "`reference_standard`, `author_knew_answers` and `judge_saw_verdict` "
        "(disclosure, not virtue — false passes, silence convicts), `caught`, "
        "`false_alarms`, and `misses` (the cross-tabulation's other row; 'unmeasured: "
        "why' is an honest value and absence is the breach). Corroborated blind by "
        "CONSORT 2025, STROBE and ARRIVE, and by Model Cards and Datasheets for "
        "Datasets. The per-factor gap those flagged is closed as of 0.3.0: "
        "optional `factors` rows — [{factor, caught, false_alarms, ...}] — and a "
        "measurement whose protocol declares factors reports them or convicts "
        "under a-figure-is-broken-down-by-its-declared-factors. An average over "
        "declared variation is a number about a mixture.",
    ),
    KindDef(
        kind="protocol",
        description="The before-artifact: what a run WILL measure, declared before it "
        "runs. Carries `name` (what measurements reference it by), `corpus` (what the "
        "run will read), `expectations` (the thresholds or hypotheses, set before the "
        "results exist to tune them), and `stopping` (the rule for ending early — "
        "'none' is an honest value and absence is not). A measurement claiming "
        "`prespecified: true` names its protocol: an earlier protocol record in the "
        "same append-only file, or 'external: <where the dated artifact lives>' for a "
        "protocol that predates the record, a census's source checklist being the "
        "standing example. The root is a-protocol-is-an-artifact-before-the-run "
        "(SPIRIT item 5, TOP's Study Protocol practice, ARRIVE item 19): saying "
        "thresholds were set in advance is a memory, and the artifact is checkable "
        "against the file's order and git's dates. Optional `factors`: the "
        "dimensions the corpus varies over (language, repository, surface), "
        "declared here so the breakdown a measurement owes is data, not "
        "judgment.",
    ),
    KindDef(
        kind="evidence",
        description="One observation offered for a claim. Carries `where` — "
        "user-surface (the thing the user touches was observed), stand-in (a faithful "
        "reconstruction, honest only with a `gap` naming what it cannot show), or "
        "producer (tests, deploys, logs — necessary, never sufficient for a done-claim "
        "alone) — and `what`, the observation in enough detail to be checked again. "
        "In the JSONL wire format evidence rides as a list under the claim; as a tree "
        "it is the claim's children, which is what the rules below read.",
    ),
]

RULES = [
    Rule(
        name="a-done-claim-carries-evidence",
        kind="done",
        description="A done-claim with no evidence at all is an assertion nobody could "
        "stand behind. WHICH evidence suffices is the deciders' question, answered in "
        "code where payload can be read; that a claim carries some is the structural "
        "floor, and it is all a tree rule can honestly check.",
        expr="len(nodes('evidence', self)) >= 1",
    ),
    Rule(
        name="a-fixed-claim-carries-evidence",
        kind="fixed",
        description="The same floor for a fix: something was observed, or nothing "
        "supports the verb.",
        expr="len(nodes('evidence', self)) >= 1",
    ),
]

EXAMPLES = [
    Node(id="an-example-done", kind="done",
         name="An example: work reported finished, with the observation that closes it",
         payload={"text": "the sheet renders on the phone"},
         children=[
             Node(id="an-example-done-evidence", kind="evidence",
                  payload={"where": "user-surface",
                           "what": "beacon self-fetched; four card reports after"}),
         ]),
    Node(id="an-example-fixed", kind="fixed",
         name="An example: a fix, reproduced first, one candidate, gap named",
         payload={"text": "the empty card", "reproduced_first": True,
                  "changes": ["self-fetch on missing payload"]},
         children=[
             Node(id="an-example-fixed-evidence", kind="evidence",
                  payload={"where": "stand-in", "what": "NO_PAYLOAD harness green",
                           "gap": "the phone itself not observed"}),
         ]),
    Node(id="an-example-diagnosis", kind="diagnosis",
         name="An example: a cause, with the observation that separates it",
         payload={"text": "the host never pushes tool results", "prior_theories": 4,
                  "new_observation": "beacon: after-initialized then no-payload"}),
    Node(id="an-example-detour", kind="detour",
         name="An example: a workaround that says what stays broken",
         payload={"text": "judge on /deck meanwhile",
                  "still_broken": "the MCP card until the host refreshes"}),
    Node(id="an-example-confirmation", kind="confirmation",
         name="An example: an agreement with its traceable account",
         payload={"text": "the suite already gates itself correctly",
                  "checked": "ran the tests with credentials stripped: 87 tests, "
                             "6.4s, 2 skipped"}),
    Node(id="an-example-protocol", kind="protocol",
         name="An example: the before-artifact a measurement references",
         payload={"name": "wordlist-sweep",
                  "text": "the word-list sweep, declared before running it",
                  "corpus": "every markdown file under the estate, exhaustive glob",
                  "expectations": "hits read in context by a person",
                  "stopping": "none — the glob is finite and read to its end"}),
    Node(id="an-example-measurement", kind="measurement",
         name="An example: a figure with its whole protocol",
         payload={"text": "the three word lists over the estate's docs",
                  "corpus": "87 markdown files, exhaustive glob",
                  "size_declared_before": True, "prespecified": True,
                  "reference_standard": "a person reading every hit in its paragraph",
                  "author_knew_answers": True, "judge_saw_verdict": True,
                  "caught": 3, "false_alarms": 2,
                  "misses": "unmeasured: files with no hits were not sampled"}),
]

COUNTER_EXAMPLES = [
    CounterExample(
        rule="a-done-claim-carries-evidence",
        because="done with nothing observed at all — the fifteen-times failure in its "
                "purest form, an assertion with no observation anywhere under it",
        node=Node(id="just-done", kind="done",
                  name="Deployed and verified", payload={"text": "it works now"}),
    ),
    CounterExample(
        rule="a-fixed-claim-carries-evidence",
        because="a fix nobody watched fail or pass — the change is real, the claim "
                "about it rests on nothing",
        node=Node(id="just-fixed", kind="fixed",
                  name="Fixed the empty card", payload={"text": "the empty card"}),
    ),
]

CLAIMS_PACKAGE = Package(
    name="claims",
    version="0.4.0",
    description="A session's assertions as data: seven claim kinds, graded evidence, "
                "the measurement protocol and the agreed calibration scales — the "
                "record the practice laws fire on, published so the vocabulary is "
                "versioned and visible instead of accumulating silently in code. "
                "The deciders stay code in the repository that owns the laws; this "
                "is the meaning they implement.",
    publisher="xag",
    requires=[],
    vocabulary=VOCABULARY,
    rules=RULES,
    examples=EXAMPLES,
    counter_examples=COUNTER_EXAMPLES,
)


def build() -> Package:
    return CLAIMS_PACKAGE
