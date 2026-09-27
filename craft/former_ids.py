"""The ids a law was published under before it was renamed, and the id it answers to now.

A law's id is data other people hold: an adopter's rulings file, a filed dispute, a
decider registered in another package, a claim in claims.jsonl, a critic verdict. A
rename must not strand any of it, so every place an id arrives from outside reads it
through current_id, and a record filed under a former name keeps resolving
(yesterdays-names-keep-answering, applied to the catalogue's own names). Former ids are
never reused for another law.
"""

from __future__ import annotations

FORMER_IDS: dict[str, str] = {
    "a-label-names-the-thing-not-a-speaker": "keep-labels-clear-and-simple",
}


def current_id(law_id: str) -> str:
    """The id a law answers to now, for an id filed under any of its names."""
    return FORMER_IDS.get(law_id, law_id)
