"""a-check-exhibits-what-it-read: the alarm pairs for its three firing points.

Every decider faces a guilty case it must convict and a clean one it must not. The
guilty cases here are reconstructions of the two founding sightings (2026-08-29): an
account parsing to zero nodes read as all-pass, and the hook finding zero accounts
and exiting silently.
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


def test_the_hook_says_zero_accounts_once_per_session(tmp_path, monkeypatch, capsys):
    # the transcript: one user line, no tool calls, so no roots are derived and no
    # accounts exist anywhere for this invented session
    transcript = tmp_path / "t.jsonl"
    transcript.write_text(json.dumps(
        {"type": "user", "message": {"content": "hello"}}) + "\n", encoding="utf-8")
    monkeypatch.setattr(account_hook, "_SEEN", tmp_path / "seen.json")
    monkeypatch.chdir(tmp_path)  # cwd holds no .craft/accounts/<session>
    payload = {"session_id": "no-such-session-xyz", "transcript_path": str(transcript)}
    assert account_hook.stop(payload) == 2
    err = capsys.readouterr().err
    assert "0 account(s) found" in err
    # the second turn with the same zero is silent: said once, not nagged
    assert account_hook.stop(payload) == 0


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
