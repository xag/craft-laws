"""The ids a law was published under before it was renamed, and the id it answers to now.

A law's id is data other people hold: an adopter's rulings file, a filed dispute, a
decider registered in another package, a claim in claims.jsonl, a critic verdict. A
rename must not strand any of it, so every place an id arrives from outside reads it
through current_id, and a record filed under a former name keeps resolving
(a-published-name-keeps-working, applied to the catalogue's own names). Former ids are
never reused for another law.
"""

from __future__ import annotations

FORMER_IDS: dict[str, str] = {
    "a-label-names-the-thing-not-a-speaker": "keep-labels-clear-and-simple",
    "no-calque": "a-metaphor-is-rechosen-in-each-language",
    "untranslatable-tone": "a-tone-only-line-may-be-dropped-in-translation",
    "glossary-first": "settle-the-glossary-before-translating",
    "composed-prose": "never-build-a-sentence-from-fragments",
    "text-expansion": "layout-survives-longer-translations",
    "rare-action-folds-away": "rare-actions-go-to-a-second-layer",
    "a-way-back": "every-mistake-has-a-way-back",
    "empty-state-never-contradicts": "an-empty-state-never-contradicts-the-controls",
    "words-keep-their-space": "a-control-in-a-line-adds-no-space",
    "space-comes-in-measured-intervals": "space-comes-in-multiples-of-one-unit",
    "what-stays-stays-put": "what-stays-on-screen-keeps-its-place",
    "space-is-held-for-what-arrives": "space-is-reserved-for-what-will-appear",
    "error-names-the-culprit": "an-error-names-the-field",
    "known-date-three-boxes": "a-known-date-is-three-fields",
    "works-both-ways-up": "works-in-portrait-and-landscape",
    "text-survives-doubling": "text-works-at-twice-its-size",
    "speaks-to-you": "address-the-reader-as-you",
    "locale-machinery-formats": "dates-and-numbers-use-locale-formatting",
    "yesterdays-names-keep-answering": "a-published-name-keeps-working",
    "the-answers-span-the-question": "the-answers-offered-cover-every-possible-answer",
    "a-verb-travels-as-a-verb": "write-an-action-as-a-verb",
    "the-users-attention-is-not-a-test-harness": "never-ask-the-user-to-run-a-check-you-can-run",
    "deliberate-names-its-decision": "calling-a-state-deliberate-names-the-decision",
    "a-remainder-names-its-debt": "what-is-left-undone-is-named-as-a-debt",
    "a-view-moves-on-observation-not-on-company": "a-view-changes-on-new-observation-not-to-agree",
    "a-qualifier-is-licensed-by-the-evidence": "a-hedge-needs-a-named-unknown",
}


def current_id(law_id: str) -> str:
    """The id a law answers to now, for an id filed under any of its names."""
    return FORMER_IDS.get(law_id, law_id)
