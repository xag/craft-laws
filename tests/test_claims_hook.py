"""The Stop hook: the claim deciders, run before the turn is handed back."""

import json
import time
from pathlib import Path

import craft.claims_hook as hook
from craft.claims import ClaimFinding, check_file


def _transcript(tmp_path: Path, *written: Path) -> Path:
    t = tmp_path / "t.jsonl"
    rows = [{"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": str(i), "name": "Write",
         "input": {"file_path": str(p)}}]}} for i, p in enumerate(written)]
    t.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return t


def test_it_finds_the_claims_of_every_repo_the_turn_wrote_to(tmp_path):
    # a turn edits several checkouts, and the claim belongs in the one the work was in.
    # Reading only the current directory would miss exactly what a cross-repo turn claims.
    for name in ("alpha", "beta"):
        repo = tmp_path / name
        (repo / ".git").mkdir(parents=True)
        (repo / "claims.jsonl").write_text("", encoding="utf-8")
        (repo / "src").mkdir()
    t = _transcript(tmp_path, tmp_path / "alpha" / "src" / "a.py",
                    tmp_path / "beta" / "src" / "b.py")
    assert hook.touched(t) == sorted([tmp_path / "alpha" / "claims.jsonl",
                                      tmp_path / "beta" / "claims.jsonl"])


def test_a_repo_with_no_claims_file_is_not_invented(tmp_path):
    repo = tmp_path / "gamma"
    (repo / ".git").mkdir(parents=True)
    (repo / "src").mkdir()
    assert hook.touched(_transcript(tmp_path, repo / "src" / "c.py")) == []


def test_the_deciders_convict_in_code_and_in_milliseconds(tmp_path):
    # the point of the whole rewrite: this is code over data, not a model reading prose
    claims = tmp_path / "claims.jsonl"
    claims.write_text(json.dumps({
        "kind": "done", "text": "the card renders on the phone",
        "evidence": [{"where": "producer", "what": "the suite is green"}]}) + "\n",
        encoding="utf-8")
    t0 = time.time()
    found = check_file(claims)
    assert time.time() - t0 < 0.5
    assert [f.law for f in found] == ["done-is-observed-where-the-user-stands"]


def test_the_same_findings_are_handed_back_once(tmp_path, monkeypatch):
    # a turn already told, which chose, is not told again — a check that will not let go
    # is one that gets switched off. The store is the courier's since 2026-09-01; what
    # counts as the same thing said twice stays this producer's judgment.
    monkeypatch.setenv("COURIER_DIR", str(tmp_path / "courier"))
    from courier import mail
    f = [ClaimFinding(law="l", where="claims.jsonl#1", quote="q", why="w")]
    other = [ClaimFinding(law="l", where="claims.jsonl#2", quote="q", why="w")]
    assert hook._identity(f) != hook._identity(other)
    assert mail.post_once("s", "craft.claims", "a", key=hook._identity(f))["status"] == "sent"
    assert mail.post_once("s", "craft.claims", "a", key=hook._identity(f))["status"] == "duplicate"
    assert mail.post_once("s", "craft.claims", "b", key=hook._identity(other))["status"] == "sent"


def test_the_finding_goes_to_the_author_and_refuses_nothing():
    said = hook.report([ClaimFinding(law="done-is-observed-where-the-user-stands",
                                     where="claims.jsonl#3", quote="the suite is green",
                                     why="every item of evidence is producer-side")])
    assert "done-is-observed-where-the-user-stands" in said
    assert "every item of evidence is producer-side" in said
    assert "Nothing is refused" in said


def _transcript_with(tmp_path: Path, rows: list) -> Path:
    t = tmp_path / "t2.jsonl"
    t.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return t


def _tool(input_):
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "x", "name": "T", "input": input_}]}}


def test_a_written_repo_with_an_untouched_record_is_named(tmp_path):
    repo = tmp_path / "delta"
    (repo / ".git").mkdir(parents=True)
    (repo / "claims.jsonl").write_text("", encoding="utf-8")
    t = _transcript_with(tmp_path, [_tool({"file_path": str(repo / "src.py")})])
    assert hook.silent_repos(t) == [repo]


def test_filing_by_file_path_clears_the_repo(tmp_path):
    repo = tmp_path / "delta"
    (repo / ".git").mkdir(parents=True)
    (repo / "claims.jsonl").write_text("", encoding="utf-8")
    t = _transcript_with(tmp_path, [
        _tool({"file_path": str(repo / "src.py")}),
        _tool({"file_path": str(repo / "claims.jsonl")})])
    assert hook.silent_repos(t) == []


def test_filing_by_shell_command_clears_the_named_repo(tmp_path):
    repo = tmp_path / "delta"
    (repo / ".git").mkdir(parents=True)
    (repo / "claims.jsonl").write_text("", encoding="utf-8")
    t = _transcript_with(tmp_path, [
        _tool({"file_path": str(repo / "src.py")}),
        _tool({"command": f"cd {repo} && python -c \"open('claims.jsonl','a')\""})])
    assert hook.silent_repos(t) == []


def test_an_unattributable_filing_clears_everything(tmp_path):
    # under-reporting beats a false alarm: a bare mention of the record clears all,
    # because a noisy informant is one that gets switched off
    repo = tmp_path / "delta"
    (repo / ".git").mkdir(parents=True)
    (repo / "claims.jsonl").write_text("", encoding="utf-8")
    t = _transcript_with(tmp_path, [
        _tool({"file_path": str(repo / "src.py")}),
        _tool({"command": "python - <<PY\nopen('claims.jsonl','a')\nPY"})])
    assert hook.silent_repos(t) == []


def test_a_repo_without_a_record_is_not_nagged_about_one(tmp_path):
    repo = tmp_path / "epsilon"
    (repo / ".git").mkdir(parents=True)
    t = _transcript_with(tmp_path, [_tool({"file_path": str(repo / "src.py")})])
    assert hook.silent_repos(t) == []


def test_the_consult_gate_reaches_the_author_at_the_stop(tmp_path, monkeypatch, capsys):
    """The gate ran only in CI, and CI red on anything else meant it never ran at
    all. Now an unconsulted work claim comes back through the same Stop handback as
    every other finding - while the claim can still be edited."""
    repo = tmp_path / "adopted"
    (repo / ".git").mkdir(parents=True)
    (repo / ".craft").mkdir()
    (repo / ".craft" / "ledger.json").write_text(
        json.dumps({"module": "tests.fake_ledger", "since": 0}), encoding="utf-8")
    (repo / "claims.jsonl").write_text(json.dumps(
        {"kind": "done", "text": "walked in",
         "evidence": [{"where": "user-surface", "what": "seen at the door"}]}) + "\n",
        encoding="utf-8")
    (repo / "src").mkdir()
    t = _transcript(tmp_path, repo / "src" / "a.py")
    monkeypatch.setenv("COURIER_DIR", str(tmp_path / "courier"))
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1]))
    rc = hook.run({"transcript_path": str(t), "session_id": "s"})
    # nothing blocks any more: the courier carries the finding to the next seam
    assert rc == 0
    from courier import mail
    posted = mail.take("s")
    # the findings and the intake-silence note travel as separate messages now, so each
    # is thrown away or repeated on its own terms rather than as one blob
    assert {m["producer"] for m in posted} == {"craft.claims"}
    assert any("unconsulted" in m["body"] for m in posted)
