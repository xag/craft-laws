"""The silent critic: digest bounds, reconstruction storage, and silence-unless-convicted.

The injected fake runner tests the plumbing, never the criticism's quality - that
is judged the same way the adjudicator's is, from the files this module writes.
"""

import json

from craft import critic


def _transcript(tmp_path, turns):
    p = tmp_path / "t.jsonl"
    lines = []
    for user, reply in turns:
        lines.append(json.dumps({"type": "user", "message": {"content": user}}))
        lines.append(json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": reply}]}}))
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def test_digest_pairs_users_with_replies_and_bounds_them(tmp_path):
    t = _transcript(tmp_path, [("q1", "a1"), ("q2", "a2 " * 2000)])
    pairs = critic.digest(t)
    assert [p["user"] for p in pairs] == ["q1", "q2"]
    assert len(pairs[1]["reply"]) <= critic.MAX_TURN_CHARS


def test_a_clean_reconstruction_writes_accounts_and_no_critique(tmp_path):
    t = _transcript(tmp_path, [("does it work?", "Yes: the check passed.")])

    def runner(prompt):
        assert "TURN 0" in prompt
        return json.dumps([{"turn": 0, "nodes": [
            {"id": "g1", "type": "I", "ground": "given", "quote": "does it work?"},
            {"id": "c1", "type": "I", "role": "conclusion",
             "says": "Yes: the check passed.", "text": "the check passed"},
            {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["g1"],
             "conclusion": "c1"}]}])

    out = tmp_path / "acc"
    n = critic.run(t, "s", out, runner=runner)
    assert n == 0
    written = json.loads((out / "critic-0.json").read_text(encoding="utf-8"))
    assert written["reconstruction"] is True
    assert not (out / "critique.md").exists(), "nothing convicts: leave it undisturbed"


def test_a_fabricated_quote_in_the_reconstruction_convicts_into_critique(tmp_path):
    t = _transcript(tmp_path, [("does it work?", "Yes: the check passed.")])

    def runner(prompt):
        return json.dumps([{"turn": 0, "nodes": [
            {"id": "g1", "type": "I", "ground": "given",
             "quote": "words the user never typed"},
            {"id": "c1", "type": "I", "role": "conclusion", "text": "x"},
            {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["g1"],
             "conclusion": "c1"}]}])

    out = tmp_path / "acc"
    n = critic.run(t, "s", out, runner=runner)
    assert n >= 1
    critique = (out / "critique.md").read_text(encoding="utf-8")
    assert "a-ground-is-a-quotation-from-the-record" in critique


def test_a_runner_answering_garbage_writes_nothing(tmp_path):
    t = _transcript(tmp_path, [("q", "a")])
    out = tmp_path / "acc"
    assert critic.run(t, "s", out, runner=lambda p: "not json at all") == 0
    assert not out.exists() or not list(out.glob("critic-*.json"))
