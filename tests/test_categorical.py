"""The grammar: a proposition is a sentence in a language, parsed, not a record typed."""

import pytest

from craft import categorical, syllogism
from craft.categorical import ParseError, parse


@pytest.mark.parametrize("text,type_,subject,predicate", categorical.ACCEPTS)
def test_the_language_parses_to_the_traditions_four_types(text, type_, subject,
                                                          predicate):
    p = parse(text)
    assert (p.type, p.subject, p.predicate) == (type_, subject, predicate)


@pytest.mark.parametrize("text,fragment", categorical.REFUSES)
def test_a_near_miss_is_refused_with_its_reason(text, fragment):
    with pytest.raises(ParseError) as e:
        parse(text)
    assert fragment in str(e.value)


def test_the_refusal_says_where():
    with pytest.raises(ParseError, match="position 0"):
        parse("all B is A")
    with pytest.raises(ParseError, match="position 12"):
        parse("every B is A.")


def test_a_term_may_be_several_words():
    p = parse("some things that are pleasant is good")
    assert p.subject == "things that are pleasant" and p.predicate == "good"


def test_a_record_of_parts_is_refused():
    """The defect this closed: quantity/quality/subject/predicate typed by hand."""
    with pytest.raises(syllogism.FormError, match="sentence in the language"):
        syllogism.type_of({"quantity": "all", "quality": "affirmative",
                           "subject": "B", "predicate": "A"})


def test_the_form_comes_out_of_the_parse():
    assert syllogism.derive(["every B is A", "every C is B"], "every C is A") == \
        ("AAA", 1)
    assert syllogism.derive(["every P is M", "every S is M"], "every S is P") == \
        ("AAA", 2)


def test_an_ungrammatical_proposition_stops_the_derivation():
    with pytest.raises(syllogism.FormError, match="expected one of"):
        syllogism.derive(["all B is A", "every C is B"], "every C is A")


def test_the_grammar_alarm_rings():
    assert categorical._alarm() == 0
