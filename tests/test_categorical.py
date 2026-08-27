"""The grammar: a proposition is a sentence in a language, parsed, not a record typed."""

import pytest

from craft import categorical, syllogism
from craft.categorical import ParseError, parse


@pytest.mark.parametrize("text,type_,subject,predicate", categorical.ACCEPTS)
def test_the_language_parses_to_the_traditions_four_types(text, type_, subject,
                                                          predicate):
    p = parse(text)
    assert (p.type, p.subject, p.predicate) == (type_, subject, predicate)


@pytest.mark.parametrize("text", categorical.REFUSES)
def test_a_near_miss_is_refused_by_the_grammar(text):
    with pytest.raises(ParseError):
        parse(text)


def test_the_refusal_says_where():
    with pytest.raises(ParseError, match="position 0"):
        parse("all B is A")
    with pytest.raises(ParseError, match="position"):
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
    with pytest.raises(syllogism.FormError, match="not in the language"):
        syllogism.derive(["all B is A", "every C is B"], "every C is A")


def test_the_grammar_alarm_rings():
    assert categorical._alarm() == 0


# --- the prover, and the grammar file ------------------------------------------------

def test_the_grammar_file_is_what_lark_executes():
    """Not an EBNF docstring beside a hand-rolled parser: this file IS the parser."""
    from pathlib import Path
    import craft.categorical as c
    assert c._GRAMMAR.name == "categorical.lark" and c._GRAMMAR.exists()
    assert "universal_affirmative" in c._GRAMMAR.read_text(encoding="utf-8")


def test_z3_reproduces_the_tradition_without_any_rule_written_here():
    """The cross-check that retired the hand-written distribution rules: an
    independent decision procedure must accept exactly the same forms."""
    from craft.entailment import entails
    from craft.syllogism import valid_forms
    places = {1: (("M", "P"), ("S", "M")), 2: (("P", "M"), ("S", "M")),
              3: (("M", "P"), ("M", "S")), 4: (("P", "M"), ("M", "S"))}
    say = {"A": "every {} is {}", "E": "no {} is {}",
           "I": "some {} is {}", "O": "some {} is not {}"}
    for ei in (False, True):
        got = set()
        for fig, (mj, mn) in places.items():
            for a_ in "AEIO":
                for b in "AEIO":
                    for c_ in "AEIO":
                        prem = [parse(say[a_].format(*mj)), parse(say[b].format(*mn))]
                        con = parse(say[c_].format("S", "P"))
                        if entails(prem, con, nonempty_terms=ei).valid:
                            got.add(f"{a_}{b}{c_}-{fig}")
        assert got == set(valid_forms(ei))
        assert len(got) == (24 if ei else 15)


def test_an_invalid_argument_comes_back_with_a_counter_model():
    from craft.entailment import entails
    r = entails([parse("every P is M"), parse("every S is M")], parse("every S is P"))
    assert not r.valid and r.counter_model
