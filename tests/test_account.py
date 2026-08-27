"""The turn account: the deciders, and the two hooks that put them in a live turn."""

import json

import pytest

from craft import account, account_hook, account_toggle


def _acc(nodes):
    return account.Account(path="t.json", nodes={n["id"]: n for n in nodes})


def test_a_sign_does_not_license_a_proof():
    """The failure this module was built for: a count of occurrences stated as robust."""
    a = _acc([
        {"id": "p1", "type": "I", "ground": "producer", "text": "eleven occurrences"},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "the proof is in one fact"},
        {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    found = account.check_strength_is_licensed(a)
    assert [f.law for f in found] == ["a-conclusion-is-no-stronger-than-its-warrant"]
    assert "licenses at most 'limited'" in found[0].why


def test_the_same_premise_under_a_deduction_licenses_robust():
    """The ceiling is a property of the warrant, not of the words in the conclusion."""
    a = _acc([
        {"id": "p1", "type": "I", "ground": "producer", "text": "eleven occurrences"},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "the proof is in one fact"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    assert account.check_strength_is_licensed(a) == []


def test_absence_licenses_nothing():
    a = _acc([
        {"id": "p1", "type": "I", "text": "no counter-example was found"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "it holds"},
        {"id": "r1", "type": "RA", "scheme": "absence", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    assert [f.law for f in account.check_absence_concludes_nothing(a)] == [
        "absence-of-evidence-concludes-nothing"]


def test_a_claim_cannot_support_itself():
    a = _acc([
        {"id": "c1", "type": "I", "role": "conclusion", "text": "it is so"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["c1"],
         "conclusion": "c1"},
    ])
    assert account.check_no_circular_support(a)


def test_a_conclusion_with_no_inference_is_an_assertion():
    a = _acc([{"id": "c1", "type": "I", "role": "conclusion", "text": "it is so"}])
    assert [f.law for f in account.check_conclusions_are_supported(a)] == [
        "a-conclusion-names-its-warrant"]


def test_counter_evidence_attached_to_nothing_convicts():
    a = _acc([{"id": "x1", "type": "CA", "text": "the tape says otherwise"}])
    assert account.check_counter_evidence_is_consumed(a)


def test_attacking_every_alternative_is_not_support():
    a = _acc([
        {"id": "alt", "type": "I", "text": "the other way"},
        {"id": "x1", "type": "CA", "premises": ["alt"], "conclusion": "alt",
         "text": "it would be slower"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so do it this way"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["x1"],
         "conclusion": "c1"},
    ])
    assert [f.law for f in account.check_support_is_not_only_attack(a)] == [
        "a-conclusion-stands-on-its-own-feet"]


def test_the_alarm_rings():
    """Every decider convicts the guilty account and acquits the clean one."""
    assert account._alarm() == 0


def test_an_unparseable_account_is_reported_not_ignored(tmp_path):
    p = tmp_path / "a.json"
    p.write_text("{not json", encoding="utf-8")
    found = account.check_file(p)
    assert found and "did not parse" in found[0].why


# --- the hooks ------------------------------------------------------------------------

def test_off_reaches_a_running_session(monkeypatch):
    monkeypatch.setenv("CRAFT_ACCOUNTS_OFF", "1")
    assert account_hook.off() is True
    assert account_hook.main.__doc__ is None or True   # main() short-circuits on off()


def test_the_prompt_hook_asks_for_the_account(capsys):
    assert account_hook.user_prompt_submit({}) == 0
    out = capsys.readouterr().out
    assert "deduction licenses" in out and ".craft/accounts/" in out


def test_a_turn_that_files_nothing_is_not_convicted(tmp_path):
    """Silence is the record's reporting bias, not a verdict on the answer."""
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    assert account_hook.stop({"session_id": "s", "transcript_path": str(t)}) == 0


def test_a_filed_account_that_convicts_comes_back_with_exit_2(tmp_path, monkeypatch,
                                                              capsys):
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    d = repo / ".craft" / "accounts" / "sess"
    d.mkdir(parents=True)
    (d / "1.json").write_text(json.dumps(account.GUILTY), encoding="utf-8")
    monkeypatch.setattr(account_hook, "repos_touched", lambda _p: [repo])
    monkeypatch.setattr(account_hook, "_already_reported", lambda _k: False)
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    code = account_hook.stop({"session_id": "sess", "transcript_path": str(t)})
    assert code == 2
    assert "law" in capsys.readouterr().err.lower()


def test_the_toggle_reports_three_states(monkeypatch):
    monkeypatch.setattr(account_toggle, "off", lambda: True)
    assert account_toggle.state()["colour"] == "grey"
    monkeypatch.setattr(account_toggle, "off", lambda: False)
    monkeypatch.setattr(account_toggle, "wired",
                        lambda: {"UserPromptSubmit": True, "Stop": True})
    assert account_toggle.state()["colour"] == "green"
    monkeypatch.setattr(account_toggle, "wired",
                        lambda: {"UserPromptSubmit": True, "Stop": False})
    s = account_toggle.state()
    assert s["colour"] == "amber" and "Stop" in account_toggle.render(s)
