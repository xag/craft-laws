"""The published meaning and the running deciders, held equal by code.

claims@0.1.0 states what a claim record means; craft/claims.py convicts records. If a
kind is added to one side and not the other, the vocabulary has drifted from the check
— which is precisely how the claims vocabulary grew for a week before it was published
at all. These tests make that a red bar instead of a silent divergence.
"""

from craft.claims import CHECKS, CLAIM_KINDS, _alarm
from craft.claims_package import CLAIMS_PACKAGE


def test_package_kinds_are_the_deciders_kinds():
    published = {k.kind for k in CLAIMS_PACKAGE.vocabulary}
    assert published == set(CLAIM_KINDS) | {"evidence"}, (
        "the published vocabulary and the checking side's kind list disagree — "
        "whichever moved, move the other in the same commit, deliberately")


def test_every_kind_is_exercised_by_the_alarm(capsys):
    """A kind no alarm corpus carries is a kind whose deciders are never seen red or
    green — relocated guessing, per the house rule. The alarm's own corpora are read
    off the module rather than duplicated here."""
    import craft.claims as cl
    import inspect
    src = inspect.getsource(cl._alarm)
    for kind in CLAIM_KINDS:
        assert f'"kind": "{kind}"' in src or f"'kind': '{kind}'" in src, (
            f"the alarm corpora carry no {kind!r} record — a decider for it has "
            "never been seen to fire")


def test_the_alarm_is_live():
    assert _alarm() == 0
