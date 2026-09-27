"""A renamed law keeps answering to every name it was filed under: the rename table points
only at laws that exist, never reuses a live id, and each place an id arrives from
outside - a dispute, a rulings file, a decider's registration - reads it through it."""

import json

import craft.disputes as disputes
from craft import account_laws, compile as compile_, rulings
from craft.former_ids import FORMER_IDS, current_id
from craft.laws import LAWS
from craft.practice import PRACTICE


def _live() -> set[str]:
    return ({x.id for x in LAWS} | {x.id for x in PRACTICE}
            | {x.id for x in account_laws.ACCOUNT})


def test_every_former_id_points_at_a_law_that_exists_and_none_is_live():
    live = _live()
    assert all(new in live for new in FORMER_IDS.values())
    assert not (set(FORMER_IDS) & live)


def test_a_current_id_answers_to_itself():
    assert current_id("targets-are-thumb-sized") == "targets-are-thumb-sized"


def test_a_dispute_filed_under_a_former_id_lands_under_the_current_one(tmp_path, monkeypatch):
    monkeypatch.setattr(disputes, "DISPUTES", tmp_path / "disputes.jsonl")
    old, new = next(iter(FORMER_IDS.items()))
    assert disputes.file_dispute(old, "w", "why")["law"] == new


def test_a_rulings_file_keyed_under_a_former_id_keeps_its_verdicts(tmp_path):
    old, new = next(iter(FORMER_IDS.items()))
    path = tmp_path / "rulings.json"
    path.write_text(json.dumps({f"ruling:{old}--tab:today": {"verdict": "stand"}}), encoding="utf-8")
    recorded = rulings.read_rulings(path)
    assert rulings.verdict_for(new, "tab:today", {}, recorded) == {"verdict": "stand"}
    assert rulings.verdict_for(old, "tab:today", {}, recorded) == {"verdict": "stand"}


def test_a_decider_registered_under_a_former_id_registers_under_the_current_one():
    ui = {x.id for x in LAWS}
    old, new = next((o, n) for o, n in FORMER_IDS.items() if n in ui)
    assert compile_._law(old) == new


def test_a_claim_that_consulted_a_law_by_a_former_id_still_resolves():
    from craft import consulted
    old, new = next(iter(FORMER_IDS.items()))
    kind = next(iter(consulted.WORK_KINDS))
    claim = {"kind": kind, "consulted": [old]}
    assert consulted.check_claims([claim], {new: "law"}, 0) == []
