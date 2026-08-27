"""Syllogistic validity computed from the form, not declared by the author."""

import pytest

from craft import account, syllogism


def test_the_procedure_yields_the_traditions_own_forms():
    """15 unconditional, 24 under existential import, out of 256 mood/figure pairs."""
    assert len(syllogism.valid_forms(False)) == 15
    assert len(syllogism.valid_forms(True)) == 24
    assert set(syllogism.valid_forms(True)) == set(syllogism.NAMES)


def test_barbara_holds_and_names_itself():
    assert syllogism.judge("AAA", 1).valid
    assert syllogism.NAMES["AAA-1"] == "Barbara"


@pytest.mark.parametrize("mood,figure,rule", [
    ("AAA", 2, "undistributed-middle"),
    ("AAA", 3, "illicit-minor"),
    ("EEE", 1, "two-negative-premises"),
    ("AAE", 1, "negative-conclusion-from-affirmative-premises"),
    ("EAA", 1, "affirmative-conclusion-from-a-negative-premise"),
])
def test_each_invalidity_names_the_rule_it_breaks(mood, figure, rule):
    v = syllogism.judge(mood, figure)
    assert not v.valid and rule in v.broke


def test_existential_import_is_a_choice_not_a_constant():
    """Darapti is valid for the tradition and invalid in modern predicate logic;
    the reading is a parameter because the disagreement is real."""
    assert not syllogism.judge("AAI", 3, existential_import=False).valid
    assert syllogism.judge("AAI", 3, existential_import=True).valid


def test_a_declared_deduction_is_verified_not_believed():
    """The defect this closed: scheme='deduction' used to pass on the word alone.
    Now the propositions decide, and these compose to AAA-2."""
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "text": "every P is M",
         "prop": {"quantity": "all", "quality": "affirmative",
                  "subject": "P", "predicate": "M"}},
        {"id": "p2", "type": "I", "text": "every S is M",
         "prop": {"quantity": "all", "quality": "affirmative",
                  "subject": "S", "predicate": "M"}},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "every S is P",
         "prop": {"quantity": "all", "quality": "affirmative",
                  "subject": "S", "predicate": "P"}},
        {"id": "r1", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "premises": ["p1", "p2"], "conclusion": "c1"},
    ]})
    found = account.check_declared_deductions_are_valid(a)
    assert [f.law for f in found] == ["a-syllogism-holds-or-it-does-not"]
    assert "AAA-2" in found[0].why and "undistributed-middle" in found[0].why


def test_a_deduction_with_no_form_shows_nothing_and_says_so():
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "text": "a premise"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "a conclusion"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["p1"],
         "conclusion": "c1"},
    ]})
    assert [f.law for f in account.check_deduction_shows_its_form(a)] == [
        "a-declared-deduction-shows-its-form"]


def test_the_syllogism_alarm_rings():
    assert syllogism._alarm() == 0


# --- the form is derived, not declared ------------------------------------------------

def test_the_form_is_computed_from_the_propositions():
    from craft.syllogism import derive
    barbara = ([{"quantity": "all", "quality": "affirmative",
                 "subject": "B", "predicate": "A"},
                {"quantity": "all", "quality": "affirmative",
                 "subject": "C", "predicate": "B"}],
               {"quantity": "all", "quality": "affirmative",
                "subject": "C", "predicate": "A"})
    assert derive(*barbara) == ("AAA", 1)


def test_the_same_propositions_cannot_be_relabelled_into_a_different_figure():
    """The defect the owner found: 'figure': 2 -> 1, propositions unchanged, verdict
    flipped. The figure is now a consequence of where the middle term sits."""
    from craft.syllogism import derive
    props = ([{"quantity": "all", "quality": "affirmative",
               "subject": "P", "predicate": "M"},
              {"quantity": "all", "quality": "affirmative",
               "subject": "S", "predicate": "M"}],
             {"quantity": "all", "quality": "affirmative",
              "subject": "S", "predicate": "P"})
    assert derive(*props) == ("AAA", 2)          # and no field can say otherwise


def test_a_stated_mood_or_figure_is_refused():
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "prop": {"quantity": "all", "quality": "affirmative",
                                           "subject": "P", "predicate": "M"}},
        {"id": "p2", "type": "I", "prop": {"quantity": "all", "quality": "affirmative",
                                           "subject": "S", "predicate": "M"}},
        {"id": "c1", "type": "I", "role": "conclusion",
         "prop": {"quantity": "all", "quality": "affirmative",
                  "subject": "S", "predicate": "P"}},
        {"id": "r1", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "mood": "AAA", "figure": 1, "premises": ["p1", "p2"], "conclusion": "c1"},
    ]})
    assert [f.law for f in account.check_declared_deductions_are_valid(a)] == [
        "a-form-is-derived-not-declared"]


def test_premises_that_never_meet_are_reported_as_not_a_syllogism():
    from craft.syllogism import FormError, derive
    with pytest.raises(FormError, match="never meet"):
        derive([{"quantity": "all", "quality": "affirmative",
                 "subject": "A", "predicate": "B"},
                {"quantity": "all", "quality": "affirmative",
                 "subject": "C", "predicate": "D"}],
               {"quantity": "all", "quality": "affirmative",
                "subject": "C", "predicate": "B"})
