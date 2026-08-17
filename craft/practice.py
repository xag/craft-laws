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

from .laws import _law, _uncited

AGANS = ("David J. Agans, Debugging: The 9 Indispensable Rules for Finding Even the "
         "Most Elusive Software and Hardware Problems")
AGANS_URL = "https://debuggingrules.com/"


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
                    "what you do'.")],
        note="The corollary is what makes it actionable: if the user's surface cannot "
             "be observed from here, say so in the same breath as the claim, and name "
             "what WAS observed instead. 'Deployed; I cannot see the phone' is honest. "
             "'Deployed and verified' is not.",
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
                    "this and it was not applied at the one boundary that mattered.")],
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
