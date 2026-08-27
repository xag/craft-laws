"""The anchor corpus: grounds quote artifacts the account's author does not write."""

import json

from craft import account
from craft.record import Corpus, read


def _transcript(tmp_path, lines):
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in lines), encoding="utf-8")
    return p


def test_tool_results_and_user_text_land_in_separate_pools(tmp_path):
    t = _transcript(tmp_path, [
        {"type": "user", "message": {"content": [
            {"type": "text", "text": "build something that works"}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "content": [
                {"type": "text", "text": "43 passed in 1.52s"}]}]}},
        {"type": "assistant", "message": {"content": [
            {"type": "text", "text": "assistant prose anchors nothing"}]}},
    ])
    c = read(t)
    assert c.anchors("producer", "43 passed in 1.52s")
    assert c.anchors("given", "build something that works")
    assert not c.anchors("producer", "build something that works")   # wrong pool
    assert not c.anchors("given", "43 passed in 1.52s")              # wrong pool
    assert not c.anchors("producer", "assistant prose anchors nothing")
    assert not c.anchors("given", "assistant prose anchors nothing")


def test_whitespace_is_the_only_forgiveness(tmp_path):
    t = _transcript(tmp_path, [
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "content": [
                {"type": "text", "text": "every  alarm\n rings"}]}]}},
    ])
    c = read(t)
    assert c.anchors("stand-in", "every alarm rings")
    assert not c.anchors("stand-in", "every alarm sings")


def test_a_fabricated_quote_convicts_and_a_missing_record_is_not_a_pass():
    corpus = Corpus(tool_text="43 passed", user_text="do it")
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "producer", "quote": "999 passed"},
        {"id": "p2", "type": "I", "ground": "given", "quote": "do it"},
        {"id": "p3", "type": "I", "ground": "producer"},
    ]})
    got = {f.where: f for f in account.check_grounds_are_anchored(a, corpus)}
    assert set(got) == {"p1", "p3"}
    assert "does not hold" in got["p1"].why and "no quote" in got["p3"].why
    import pytest
    with pytest.raises(LookupError, match="unverifiable is not judged"):
        account.check_grounds_are_anchored(a, None)


def test_relabelling_a_counted_premise_as_given_no_longer_launders():
    """The closing defect of the removed lane: producer -> given flipped the verdict.
    Now `given` demands words the user actually typed."""
    corpus = Corpus(tool_text="text appears eleven times", user_text="fix the mess")
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "given",
         "quote": "text appears eleven times"},
    ]})
    found = account.check_grounds_are_anchored(a, corpus)
    assert found and "the user's messages" in found[0].why


# --- the residual: the reply's unchecked share, extracted ------------------------------

def test_the_residual_names_what_no_node_claims(tmp_path):
    import json as _json
    from craft.account_hook import residual
    acc = tmp_path / "1.json"
    acc.write_text(_json.dumps({"nodes": [
        {"id": "c1", "type": "I", "role": "conclusion",
         "says": "The gate holds both sources.",
         "text": "the gate holds"},
        {"id": "p9", "type": "I", "says": "a sentence the reply never contains"},
    ]}), encoding="utf-8")
    reply = ("The gate holds both sources. The tray is green. "
             "Nothing was pushed.")
    res = residual(reply, [acc])
    assert res["sentences"] == 3 and res["covered"] == 1
    assert "The tray is green." in res["residual"]
    assert res["unmatched_says"] and res["unmatched_says"][0]["node"] == "p9"
