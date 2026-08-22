"""An answer, held to the laws about how work is reported."""

import json

import craft.answer as answer
import craft.answer_hook as hook
from craft.answer import Finding, laws, turns
from craft.practice import PRACTICE


def test_the_law_set_is_a_family_not_a_selection():
    # the failure this replaces: laws picked by hand, or by asking "is this about words?".
    # Both are guesses, and one of them pulled in a law whose own statement says "interface
    # prose" — answers came back chopped to satisfy a counter never addressed to them.
    # The practice family was already drawn, by this package, for exactly this subject.
    assert {lid for lid, _, _ in laws()} == {n.id for n in PRACTICE}


def test_a_law_travels_with_its_falsifier():
    # a reader asked to judge without the falsifier is being asked for an opinion
    for lid, says, falsifier in laws():
        assert says and falsifier, lid


def test_no_reader_is_not_a_clean_answer(monkeypatch):
    # an absent reader and an empty law set are both NOT CHECKED. Recording either as clean
    # is the difference between a check and a decoration.
    monkeypatch.setattr(answer, "_ask", lambda p, **k: None)
    assert answer.judge("some answer", "evidence") is None
    assert answer.judge("some answer", "evidence", law_set=[]) is None


def test_a_finding_names_a_law_that_exists(monkeypatch):
    # a reader that invents a law id, or stretches one, is answering a different question
    monkeypatch.setattr(answer, "_ask", lambda p, **k: {"findings": [
        {"law": "done-is-observed-where-the-user-stands", "sentence": "s", "because": "w"},
        {"law": "a-law-nobody-wrote", "sentence": "s", "because": "w"}]})
    got = answer.judge("an answer", "evidence")
    assert [f.law for f in got] == ["done-is-observed-where-the-user-stands"]


def test_a_turn_ends_when_the_person_speaks(tmp_path):
    t = tmp_path / "t.jsonl"
    t.write_text("\n".join(json.dumps(r) for r in [
        {"type": "user", "message": {"role": "user", "content": "do it"}},
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "1", "name": "Bash", "input": {}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "content": "1072 passed"}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "done"}]}},
        {"type": "user", "message": {"role": "user", "content": "next"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "second"}]}},
    ]), encoding="utf-8")
    got = turns(t)
    assert len(got) == 2
    assert got[0].said.strip() == "done" and "1072 passed" in got[0].results
    assert got[0].tools == 1 and got[1].said.strip() == "second"


def test_the_same_answer_is_handed_back_once(tmp_path, monkeypatch):
    # without this a revised answer still carrying a breach comes straight back, and again,
    # and the loop never settles — a check that will not let go gets switched off
    monkeypatch.setattr(hook, "_SEEN", tmp_path / "seen.json")
    assert hook._already_reported("an answer") is False
    assert hook._already_reported("an answer") is True
    assert hook._already_reported("a different answer") is False


def test_the_finding_goes_to_the_author_and_refuses_nothing():
    said = hook.report([Finding(law="done-is-observed-where-the-user-stands",
                                sentence="the suite is green so it works",
                                because="no observation of a surface a person touches")])
    assert "done-is-observed-where-the-user-stands" in said
    assert "no observation of a surface a person touches" in said
    # it reports; it does not overrule. The author decides what the sentence should be.
    assert "nothing is refused" in said and "say so and carry on" in said
