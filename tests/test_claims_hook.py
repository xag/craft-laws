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
    # is one that gets switched off
    monkeypatch.setattr(hook, "_SEEN", tmp_path / "seen.json")
    f = [ClaimFinding(law="l", where="claims.jsonl#1", quote="q", why="w")]
    assert hook._already_reported(f) is False
    assert hook._already_reported(f) is True
    other = [ClaimFinding(law="l", where="claims.jsonl#2", quote="q", why="w")]
    assert hook._already_reported(other) is False


def test_the_finding_goes_to_the_author_and_refuses_nothing():
    said = hook.report([ClaimFinding(law="done-is-observed-where-the-user-stands",
                                     where="claims.jsonl#3", quote="the suite is green",
                                     why="every item of evidence is producer-side")])
    assert "done-is-observed-where-the-user-stands" in said
    assert "every item of evidence is producer-side" in said
    assert "Nothing is refused" in said
