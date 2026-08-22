"""An answer, held to the laws whose triggers actually fire for it."""

import craft.answer as answer
from craft.answer import WRITTEN_ANSWER, laws, missing


def test_every_named_law_still_exists():
    # a rename would otherwise stop an answer being held to a law, with nothing said
    assert missing() == []
    assert len(laws()) == len(WRITTEN_ANSWER)


def test_a_law_travels_with_its_falsifier():
    # a reader asked to judge without the falsifier is being asked for an opinion
    for lid, says, falsifier in laws():
        assert says and falsifier, lid


def test_the_law_set_is_chosen_by_trigger_not_by_keyword():
    # sentences-stay-under-twenty-five-words says "interface prose", its falsifier says "UI
    # copy", and its trigger is "the app's voice does work of its own (dry, terse, no
    # explaining text)". An explanation is explaining text, so the trigger never fires.
    # Including it by keyword produced answers chopped into fragments to satisfy a counter
    # that was never addressed to them.
    for out_of_scope in ("sentences-stay-under-twenty-five-words", "front-load-first-words",
                         "speaks-to-you", "say-it-once", "says-what-happens",
                         "paragraphs-stay-under-five-sentences",
                         "error-neither-begs-nor-blames", "terms-defined-before-use",
                         "acronyms-spell-out-on-first-reference",
                         "references-name-their-target-not-its-position"):
        assert out_of_scope not in WRITTEN_ANSWER, out_of_scope


def test_the_laws_that_do_fire_are_about_what_a_claim_asserts():
    for must in ("done-is-observed-where-the-user-stands", "a-remainder-names-its-debt",
                 "a-qualifier-is-licensed-by-the-evidence",
                 "what-exists-is-not-thereby-chosen",
                 "a-thing-is-built-where-its-subject-lives"):
        assert must in WRITTEN_ANSWER


def test_nothing_countable_applies_here():
    # the finding, not a shortcoming: every law that fires for an answer is about what a
    # claim may assert, and that needs a reader. There is no fast path left to build, and
    # pretending otherwise is what produced the chopped answers.
    assert not hasattr(answer, "mechanical")


def test_no_reader_is_not_a_clean_answer(monkeypatch):
    # an absent reader and an empty law set are both NOT CHECKED, and neither may be
    # recorded as a clean answer — that difference separates a check from a decoration
    monkeypatch.setattr(answer, "_ask", lambda p, **k: None)
    assert answer.judge("some answer", "evidence") is None
    assert answer.judge("some answer", "evidence", law_set=[]) is None
