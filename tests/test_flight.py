"""One tape per hook turn, and the tape replays: craft.flight declares the whole of
what a hook run cannot predict, so a verdict from another session can be read back
instead of re-argued from guesses about what that session's transcript held."""

import json
from pathlib import Path

import craft.account_hook as account_hook
import craft.claims_hook as claims_hook
import craft.flight as flight


def _repo(tmp_path: Path, name: str, claims: str = "") -> Path:
    repo = tmp_path / name
    (repo / ".git").mkdir(parents=True)
    (repo / "claims.jsonl").write_text(claims, encoding="utf-8")
    (repo / "src").mkdir()
    return repo


def _transcript(tmp_path: Path, *written: Path) -> Path:
    t = tmp_path / "t.jsonl"
    rows = [{"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": str(i), "name": "Write",
         "input": {"file_path": str(p)}}]}} for i, p in enumerate(written)]
    t.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return t


def _tape_lines(tape: Path) -> tuple[dict, list[dict]]:
    lines = [json.loads(x) for x in tape.read_text(encoding="utf-8").splitlines()]
    return lines[0], [x for x in lines if x.get("ev") == "call"]


def _record_claims_turn(tmp_path, monkeypatch) -> tuple[int, Path, Path]:
    """One convicting claims-hook turn, recorded; returns (exit, tape, transcript)."""
    from flight_recorder import install, session_path, uninstall

    repo = _repo(tmp_path, "alpha", json.dumps(
        {"kind": "done", "text": "shipped",
         "evidence": [{"where": "producer", "what": "suite green"}]}) + "\n")
    t = _transcript(tmp_path, repo / "src" / "a.py")
    monkeypatch.setattr(claims_hook, "_SEEN", tmp_path / "seen.json")
    flight.reset()
    install(flight.boundary("claims"), claims_hook,
            directory=str(tmp_path / "flight"))
    try:
        rc = claims_hook.run({"transcript_path": str(t), "session_id": "s"})
        tape = session_path()
    finally:
        uninstall()
    return rc, Path(tape), t


def test_a_claims_turn_records_one_tape_holding_the_whole_verdict(tmp_path,
                                                                  monkeypatch,
                                                                  capsys):
    rc, tape, t = _record_claims_turn(tmp_path, monkeypatch)
    assert rc == 2                    # the producer-only done-claim convicts
    header, calls = _tape_lines(tape)
    assert header["hook"] == "claims"
    assert [c["fn"] for c in calls] == ["run"]
    assert calls[0]["kwargs"]["payload"]["transcript_path"] == str(t)
    fns = [e.get("fn") for e in calls[0]["events"]]
    # the verdict's inputs all crossed as effects: the transcript once (memoized),
    # the claims file, the seen-state read, and the seen-state write
    assert fns.count("craft.flight.read_transcript") == 1
    assert "craft.flight.file_text" in fns
    assert "craft.flight.write_text" in fns


def test_the_tape_replays_the_turn_without_touching_the_world(tmp_path, monkeypatch,
                                                              capsys):
    from flight_recorder import ReplayAdapter, replay_call

    _, tape, _ = _record_claims_turn(tmp_path, monkeypatch)
    seen_after_record = (tmp_path / "seen.json").read_text(encoding="utf-8")

    class Adapter(ReplayAdapter):
        boundary = flight.boundary("claims")

        def resolve(self, fn_name, feed):
            return getattr(claims_hook, fn_name)

    flight.reset()   # a fresh hook process starts with no memo; so must a replay
    report = replay_call(tape, 0, Adapter())
    assert report.ok, report
    # the recorded write was served, not executed: replay advanced no live state
    assert (tmp_path / "seen.json").read_text(encoding="utf-8") == seen_after_record


def test_an_account_turn_records_its_tape_too(tmp_path, monkeypatch, capsys):
    from flight_recorder import install, session_path, uninstall

    repo = _repo(tmp_path, "beta")
    t = _transcript(tmp_path, repo / "src" / "b.py")
    monkeypatch.setattr(account_hook, "_SEEN", tmp_path / "aseen.json")
    flight.reset()
    install(flight.boundary("account"), account_hook,
            directory=str(tmp_path / "flight"))
    try:
        # no accounts filed and a transcript with no user turns: the critic has
        # nothing to digest, so the turn is clean and quiet -- and still on tape
        rc = account_hook.stop({"transcript_path": str(t), "session_id": "sess-x"})
        tape = session_path()
    finally:
        uninstall()
    assert rc == 0
    header, calls = _tape_lines(Path(tape))
    assert header["hook"] == "account"
    assert [c["fn"] for c in calls] == ["stop"]
    fns = [e.get("fn") for e in calls[0]["events"]]
    assert "craft.flight.read_transcript" in fns
    assert "craft.flight.working_dir" in fns
