"""An answer, held to the laws that need no reader."""

from craft.answer import WRITTEN_ANSWER, laws, mechanical, missing


def test_every_named_law_still_exists():
    # a rename would otherwise stop an answer being held to a law, with nothing said
    assert missing() == []
    assert len(laws()) == len(WRITTEN_ANSWER)


def test_a_law_travels_with_its_falsifier():
    # a reader asked to judge without the falsifier is being asked for an opinion
    for lid, says, falsifier in laws():
        assert says and falsifier, lid


def test_a_long_sentence_is_counted_not_guessed():
    long = " ".join(["word"] * 30) + "."
    found = mechanical(long)
    assert [f.law for f in found] == ["sentences-stay-under-twenty-five-words"]
    assert "30 words" in found[0].because and found[0].adjudicator == "counted"
    assert mechanical(" ".join(["word"] * 20) + ".") == []


def test_code_is_not_prose():
    # a fenced block is not a sentence a person reads, and counting it as one would fire on
    # every answer that shows a command
    assert mechanical("```\n" + " ".join(["x"] * 40) + "\n```") == []
    assert mechanical("`" + " ".join(["x"] * 40) + "`") == []


def test_a_positional_reference_is_a_wordlist():
    # "above" breaks silently the day a paragraph moves, which is every day a machine edits
    found = mechanical("The rule is stated above, and it holds.")
    assert any(f.law == "references-name-their-target-not-its-position" for f in found)


def test_a_paragraph_of_six_sentences_is_counted():
    six = " ".join("One two three." for _ in range(6))
    assert any(f.law == "paragraphs-stay-under-five-sentences" for f in mechanical(six))
    five = " ".join("One two three." for _ in range(5))
    assert not any(f.law == "paragraphs-stay-under-five-sentences" for f in mechanical(five))


def test_the_findings_come_back_while_the_answer_can_still_change():
    # two earlier shapes missed the window: a systemMessage at Stop reaches the person
    # waiting rather than the writer, and injecting at the next prompt reaches the right
    # party a turn late, when all that is left is an apology.
    from craft.answer import Finding
    from craft.answer_hook import report
    said = report([Finding(law="sentences-stay-under-twenty-five-words",
                           sentence="a very long sentence", because="52 words unsplit",
                           adjudicator="counted")])
    assert "This answer breaks" in said
    assert "sentences-stay-under-twenty-five-words" in said and "52 words unsplit" in said
    # it reports; it does not overrule. The author decides what the sentence should be.
    assert "nothing is refused" in said and "say so and carry on" in said


def test_the_same_answer_is_handed_back_once_and_not_argued_over(tmp_path, monkeypatch):
    # without this guard a revised answer still carrying a long sentence comes straight
    # back, and again, and the loop never settles - a check that will not let go is one
    # that gets switched off
    import craft.answer_hook as H
    monkeypatch.setattr(H, "_SEEN", tmp_path / "seen.json")
    assert H._already_reported("an answer") is False
    assert H._already_reported("an answer") is True
    assert H._already_reported("a different answer") is False
