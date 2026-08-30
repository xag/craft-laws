"""a-check-exhibits-what-it-read: the alarm pairs for its three firing points.

Every decider faces a guilty case it must convict and a clean one it must not. The
guilty case reconstructs the first founding sighting (2026-08-29): an account
parsing to zero nodes read as all-pass. The hook's zero-accounts firing point
retired with the silent-critic redesign (2026-08-30).
"""

import json

from craft import account, account_hook, claims


def _write(path, obj):
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


CLEAN = {"nodes": [
    {"id": "c1", "type": "I", "role": "conclusion", "text": "fine"},
    {"id": "p1", "type": "I", "text": "a premise"},
    {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
     "conclusion": "c1"},
]}


def test_a_zero_node_account_convicts_instead_of_passing(tmp_path):
    p = _write(tmp_path / "empty.json", {"nodes": []})
    findings = account.check_file(p)
    assert [f.law for f in findings] == ["a-check-exhibits-what-it-read"]


def test_a_populated_account_is_not_convicted_by_the_exhibit_law(tmp_path):
    p = _write(tmp_path / "clean.json", CLEAN)
    findings = account.check_file(p)
    assert "a-check-exhibits-what-it-read" not in [f.law for f in findings]


def test_the_hook_is_silent_on_zero_accounts_since_the_critic_design():
    """The zero-accounts line retired 2026-08-30 with the per-turn instruction:
    nothing filed is the norm now, so a zero is not a dead instrument. The
    exhibit law's hook firing point moved to the critic, whose own CLI prints
    'nothing to say' rather than nothing. The other two firing points below
    still hold."""
    # behavior asserted in test_account.test_a_turn_that_files_nothing_is_silent


def test_the_claims_cli_exhibits_its_units(tmp_path, capsys):
    empty = tmp_path / "claims.jsonl"
    empty.write_text("", encoding="utf-8")
    assert claims.main([str(empty)]) == 0
    assert "0 claim(s): nothing judged." in capsys.readouterr().out
    one = tmp_path / "one.jsonl"
    one.write_text(json.dumps({"kind": "done", "text": "x", "evidence": [
        {"where": "user-surface", "what": "seen"}]}) + "\n", encoding="utf-8")
    assert claims.main([str(one)]) == 0
    assert "1 claim(s): no claim decider convicts." in capsys.readouterr().out
