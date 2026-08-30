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


def test_the_live_critic_skips_short_replies_without_spawning(tmp_path):
    t = _transcript(tmp_path, [("q", "Clear - nothing to do.")])
    called = []
    out = tmp_path / "acc"
    lines = critic.criticize_turn(t, "s", out, runner=lambda p: called.append(p) or "[]")
    assert lines == [] and called == []


def test_the_live_critic_feeds_back_a_conviction(tmp_path):
    long_reply = "The check passed and therefore everything works. " * 10
    t = _transcript(tmp_path, [("does it work?", long_reply)])

    def runner(prompt):
        assert "TURN 0" in prompt
        return json.dumps([{"turn": 0, "nodes": [
            {"id": "g1", "type": "I", "ground": "given",
             "quote": "words the user never typed"},
            {"id": "c1", "type": "I", "role": "conclusion", "text": "x"},
            {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["g1"],
             "conclusion": "c1"}]}])

    out = tmp_path / "acc"
    lines = critic.criticize_turn(t, "s", out, runner=runner)
    assert lines and "a-ground-is-a-quotation-from-the-record" in lines[0]
    assert (out / "critic-live-0.json").exists()


def test_a_clean_live_turn_returns_nothing(tmp_path):
    long_reply = "The check passed; the record shows the run and its count. " * 8
    t = _transcript(tmp_path, [("does it work?", long_reply)])

    def runner(prompt):
        return json.dumps([{"turn": 0, "nodes": [
            {"id": "g1", "type": "I", "ground": "given", "quote": "does it work?"},
            {"id": "c1", "type": "I", "role": "conclusion", "text": "it works"},
            {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["g1"],
             "conclusion": "c1"}]}])

    assert critic.criticize_turn(t, "s", tmp_path / "acc", runner=runner) == []


def test_tool_results_reach_the_digest_and_the_prompt(tmp_path):
    """The tool excerpt exists so a true nothing-was-found conclusion can ground
    its search: without it the anti-fabrication rule and the absence law made
    such convictions deterministic (seen live 2026-08-30)."""
    lines = [
        json.dumps({"type": "user", "message": {"content": "is there any pnl code?"}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {}}]}}),
        json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1",
             "content": "grep -rn pnl: no matches in 41 files"}]}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "No P&L code exists; the grep over all 41 "
             "files found no matches, so the notebook cannot compute returns. " * 4}]}}),
    ]
    t = tmp_path / "t.jsonl"
    t.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pairs = critic.digest(t)
    assert len(pairs) == 1
    assert "no matches in 41 files" in pairs[0]["tools"]
    assert "TOOLS (excerpt" in critic.critic_prompt(pairs)


def test_a_turns_reply_is_all_its_assistant_text_merged(tmp_path):
    lines = [
        json.dumps({"type": "user", "message": {"content": "q"}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "status note"}]}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "the actual answer"}]}}),
    ]
    t = tmp_path / "t.jsonl"
    t.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pairs = critic.digest(t)
    assert len(pairs) == 1
    assert "status note" in pairs[0]["reply"] and "the actual answer" in pairs[0]["reply"]
