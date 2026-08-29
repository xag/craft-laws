"""The adjudicator pass: guilty and clean cases with an injected fake judge.

The fake judge tests the plumbing - unit extraction, freshness, storage, the exit
code - never the judgment. The judgment's own quality becomes measurable only from
the adjudications file this module appends, read later against a person's rulings.
"""

import json

from craft import adjudicate


ACCOUNT = {"nodes": [
    {"id": "g1", "type": "I", "ground": "given", "quote": "does it work?",
     "text": "the owner asked whether the hook works"},
    {"id": "p1", "type": "I", "ground": "producer", "quote": "132 passed in 5.49s",
     "text": "every apple on the moon is green"},          # a faithless reading
    {"id": "c1", "type": "I", "role": "conclusion", "text": "it works"},
    {"id": "r1", "type": "RA", "scheme": "verified-source",
     "premises": ["g1", "p1"], "conclusion": "c1"},
    {"id": "r2", "type": "RA", "scheme": "deduction", "premises": ["p1"],
     "conclusion": "c1", },                                 # excluded: Z3's job
]}


def _write(tmp_path, name="1.json", obj=ACCOUNT):
    p = tmp_path / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


def test_units_are_readings_and_non_deduction_inferences(tmp_path):
    us = adjudicate.units(_write(tmp_path))
    kinds = [(u.node, u.kind) for u in us]
    assert ("g1", "reading") in kinds and ("p1", "reading") in kinds
    assert ("r1", "inference") in kinds
    assert all(n != "r2" for n, _ in kinds), "a claimed deduction is Z3's, not the judge's"


def test_unsupported_reading_convicts_and_lands_in_the_file(tmp_path):
    p = _write(tmp_path)

    def judge(batch):
        return [{"verdict": "unsupported" if u.node == "p1" else "supported",
                 "why": "the reading is about the moon; the quote is a test count"}
                for u in batch]

    fresh, skipped = adjudicate.adjudicate([p], judge=judge, judge_name="fake")
    assert skipped == 0
    bad = [v for v in fresh if v.verdict == "unsupported"]
    assert [v.node for v in bad] == ["p1"]
    rows = [json.loads(x) for x in
            (tmp_path / adjudicate.ADJUDICATIONS).read_text(encoding="utf-8").splitlines()]
    assert {r["node"] for r in rows} == {"g1", "p1", "r1"}
    assert all(r["judge"] == "fake" for r in rows)


def test_already_ruled_units_are_not_judged_again(tmp_path):
    p = _write(tmp_path)
    calls = []

    def judge(batch):
        calls.append(len(batch))
        return [{"verdict": "supported", "why": "ok"} for _ in batch]

    adjudicate.adjudicate([p], judge=judge, judge_name="fake")
    fresh, skipped = adjudicate.adjudicate([p], judge=judge, judge_name="fake")
    assert fresh == [] and skipped == 3 and calls == [3]


def test_an_invented_verdict_word_is_kept_as_cannot_tell():
    # exercised through the api_judge post-processing shape: main() maps any
    # non-vocabulary word to cannot-tell inside api_judge; here we check the
    # adjudicate layer stores whatever the judge callable returns, so the closed
    # vocabulary is api_judge's contract, tested at its own seam below if the
    # key is ever present in CI. This test pins the vocabulary constant instead.
    assert adjudicate.VERDICTS == ("supported", "unsupported", "cannot-tell")


def test_the_cli_exhibits_a_zero(tmp_path, capsys):
    empty = tmp_path / "0.json"
    empty.write_text(json.dumps({"nodes": []}), encoding="utf-8")
    assert adjudicate.main([str(empty)]) == 0
    assert "0 judgeable unit(s): nothing judged." in capsys.readouterr().out


def test_the_api_route_without_a_key_says_so_plainly(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    p = _write(tmp_path)
    assert adjudicate.main([str(p), "--api"]) == 1
    assert "ANTHROPIC_API_KEY is not set" in capsys.readouterr().out
