"""The consult gate: the demand, the resolution, and the refusal of defeated entries."""

import json
from pathlib import Path

from craft.consulted import check_claims, check_file, ledger_index

INDEX = {"a-decision": "decision", "a-debt": "debt", "a-road-not-taken": "alternative"}


def test_a_work_claim_past_the_adoption_names_what_it_consulted():
    found = check_claims([{"kind": "done", "text": "built"}], INDEX, since=0)
    assert [f.check for f in found] == ["unconsulted"]


def test_claims_before_the_adoption_are_exempt_by_ordinal():
    assert check_claims([{"kind": "done", "text": "old work"}], INDEX, since=1) == []


def test_non_work_kinds_owe_nothing():
    assert check_claims([{"kind": "measurement", "text": "n", "caught": 1}],
                        INDEX, since=0) == []


def test_a_consultation_resolves_or_convicts():
    found = check_claims([{"kind": "fixed", "text": "f",
                           "consulted": ["a-decision", "a-ghost"]}], INDEX, since=0)
    assert [f.check for f in found] == ["unresolved"]


def test_a_rejected_alternative_is_not_a_foundation():
    found = check_claims([{"kind": "done", "text": "d",
                           "consulted": ["a-road-not-taken"]}], INDEX, since=0)
    assert [f.check for f in found] == ["rejected"]


def test_an_honest_none_passes_and_an_empty_none_does_not():
    assert check_claims([{"kind": "done", "text": "d",
                          "consulted": "none: greenfield"}], INDEX, since=0) == []
    found = check_claims([{"kind": "done", "text": "d", "consulted": "none:"}],
                         INDEX, since=0)
    assert [f.check for f in found] == ["unconsulted"]


def test_the_gate_is_opt_in_by_declaration(tmp_path):
    claims = tmp_path / "claims.jsonl"
    claims.write_text(json.dumps({"kind": "done", "text": "d"}) + "\n",
                      encoding="utf-8")
    assert check_file(claims) is None


def test_this_repos_own_ledger_indexes_its_alternatives():
    index = ledger_index("craft.tree")
    assert index.get("a-word-list-is-a-reading-not-a-mechanization") == "decision"
    assert index.get("alt-keep-them-the-match-only-triggers") == "alternative"
