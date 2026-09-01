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
    # the say-it-once store is the courier's since 2026-09-01; point it at tmp
    monkeypatch.setenv("COURIER_DIR", str(tmp_path / "courier"))
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
    # Nothing blocks since the courier carries delivery (2026-09-01): the producer-only
    # done-claim still convicts, and the conviction is posted rather than thrown at Stop.
    assert rc == 0
    from courier import mail
    posted = mail.take("s")
    assert any("done-is-observed-where-the-user-stands" in m["body"] for m in posted)
    header, calls = _tape_lines(tape)
    assert header["hook"] == "claims"
    assert [c["fn"] for c in calls] == ["run"]
    assert calls[0]["kwargs"]["payload"]["transcript_path"] == str(t)
    fns = [e.get("fn") for e in calls[0]["events"]]
    # The verdict's inputs crossed as effects: the transcript once (memoized) and the
    # claims file. The say-it-once state is no longer among them — it moved to the
    # courier, which has its own boundary and its own tape. This tape now holds what
    # this producer DECIDED; what happened to the message afterwards is read next door.
    assert fns.count("craft.flight.read_transcript") == 1
    assert "craft.flight.file_text" in fns


def test_the_tape_replays_the_turn_without_touching_the_world(tmp_path, monkeypatch,
                                                              capsys):
    from flight_recorder import ReplayAdapter, replay_call

    repo_claims = tmp_path / "alpha" / "claims.jsonl"
    _, tape, _ = _record_claims_turn(tmp_path, monkeypatch)
    claims_after_record = repo_claims.read_text(encoding="utf-8")

    class Adapter(ReplayAdapter):
        boundary = flight.boundary("claims")

        def resolve(self, fn_name, feed):
            return getattr(claims_hook, fn_name)

    flight.reset()   # a fresh hook process starts with no memo; so must a replay
    report = replay_call(tape, 0, Adapter())
    assert report.ok, report
    # the recorded reads were served, not executed: replay advanced no live state
    assert repo_claims.read_text(encoding="utf-8") == claims_after_record


def _tape(d: Path, name: str, size: int, mtime: float) -> Path:
    p = d / name
    p.write_bytes(b"x" * size)
    import os
    os.utime(p, (mtime, mtime))
    return p


def test_the_pile_is_rolled_oldest_first_to_its_budget(tmp_path):
    d = tmp_path / "flight"
    d.mkdir()
    mb = 1024 * 1024
    old = _tape(d, "flight-20260101-000000-1.jsonl", 2 * mb, 1_000_000)
    mid = _tape(d, "flight-20260102-000000-2.jsonl", 2 * mb, 2_000_000)
    new = _tape(d, "flight-20260103-000000-3.jsonl", 2 * mb, 3_000_000)
    side = d / "flight-20260101-000000-1.call1.inflight"
    side.write_bytes(b"y")

    flight.roll(d, budget_mb=5)       # 6MB of tapes, 5MB of budget
    assert not old.exists() and mid.exists() and new.exists()
    assert not side.exists()          # the dead tape's sidecar goes with it

    # a budget under one tape's size must not empty the directory: the newest is
    # never swept, because it is the one a concurrent hook process may be writing
    flight.roll(d, budget_mb=1)
    assert not mid.exists() and new.exists()


def test_a_pile_inside_its_budget_is_left_alone(tmp_path):
    d = tmp_path / "flight"
    d.mkdir()
    keep = _tape(d, "flight-20260101-000000-1.jsonl", 1024, 1_000_000)
    flight.roll(d, budget_mb=100)
    assert keep.exists()


def test_rolling_a_directory_that_does_not_exist_is_silent(tmp_path):
    flight.roll(tmp_path / "never-created", budget_mb=1)    # must not raise


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
