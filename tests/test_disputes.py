"""The dispute channel: a convicted turn's false-positive report is data on disk,
and the conviction text routes rebuttal there instead of into the user's reply."""

import json
from pathlib import Path

import craft.account_hook as account_hook
import craft.claims_hook as claims_hook
import craft.disputes as disputes
from craft.claims import ClaimFinding


def test_a_dispute_is_one_appended_json_line(tmp_path, monkeypatch):
    monkeypatch.setattr(disputes, "DISPUTES", tmp_path / "disputes.jsonl")
    disputes.file_dispute("absence-of-evidence-concludes-nothing",
                          "critic-live-3.json r2",
                          "the premise is a definition, not a search",
                          session="s-1")
    disputes.file_dispute("an-account-is-an-aif-graph", "critic-live-1.json r2",
                          "the critic split one argument across files", session="s-2")
    recs = [json.loads(x) for x in
            (tmp_path / "disputes.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [r["law"] for r in recs] == ["absence-of-evidence-concludes-nothing",
                                        "an-account-is-an-aif-graph"]
    assert recs[0]["session"] == "s-1" and recs[0]["ts"]


def test_the_cli_files_and_confirms(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(disputes, "DISPUTES", tmp_path / "disputes.jsonl")
    rc = disputes.main(["--law", "x-law", "--where", "claims.jsonl#3",
                        "--why", "the figure was measured", "--session", "s"])
    assert rc == 0
    assert "x-law" in capsys.readouterr().out
    assert (tmp_path / "disputes.jsonl").exists()


def test_every_conviction_text_routes_rebuttal_to_the_ledger_not_the_user():
    """The three promises of the contract: the dispute command is in the text, the
    text forbids responding to the conviction in the conversation, and the visible
    move it licenses is self-correction of what was said."""
    claims_text = claims_hook.report(
        [ClaimFinding(law="l", where="claims.jsonl#1", quote="q", why="w")],
        session="sess-1")
    account_text = account_hook._conviction_contract("sess-1")
    for text in (claims_text, account_text):
        assert "craft.disputes" in text and "--law" in text
        assert "sess-1" in text
        assert "Never RESPOND" in text and "noise" in text
        assert "correct" in text and "caught" in text