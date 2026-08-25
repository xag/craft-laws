"""Prose checked through its drawing: every validation is deterministic over data."""

import json
from pathlib import Path

from craft.drawing import check_drawing, source_hash


def _repo(tmp_path: Path, prose: str, nodes: list, claims: list | None = None) -> Path:
    src = tmp_path / "doc.md"
    src.write_text(prose, encoding="utf-8")
    (tmp_path / "doc.md.drawing.json").write_text(json.dumps({
        "source": "doc.md",
        "sha256": source_hash(prose),
        "nodes": nodes}), encoding="utf-8")
    if claims is not None:
        (tmp_path / "claims.jsonl").write_text(
            "\n".join(json.dumps(c) for c in claims) + "\n", encoding="utf-8")
    return src


def test_a_fresh_anchored_joined_drawing_passes(tmp_path):
    src = _repo(tmp_path, "The suite covers 9 of 12 repos today.",
                [{"kind": "measurement",
                  "quote": "The suite covers 9 of 12 repos today.", "claim": 1}],
                [{"kind": "measurement", "text": "coverage"}])
    assert check_drawing(src) == []


def test_editing_the_prose_without_rederiving_is_stale(tmp_path):
    src = _repo(tmp_path, "One sentence.", [])
    src.write_text("One sentence, edited.", encoding="utf-8")
    assert [f.check for f in check_drawing(src)] == ["stale"]


def test_a_quote_the_source_does_not_contain_is_unanchored(tmp_path):
    src = _repo(tmp_path, "What the file actually says.",
                [{"kind": "done", "quote": "A sentence never written.",
                  "unfiled": "n/a"}])
    checks = [f.check for f in check_drawing(src)]
    assert "unanchored" in checks


def test_whitespace_runs_are_a_canonical_form_not_a_similarity(tmp_path):
    src = _repo(tmp_path, "Spread over\ntwo lines,   spaced.",
                [{"kind": "done", "quote": "Spread over two lines, spaced.",
                  "claim": 1}],
                [{"kind": "done", "text": "t"}])
    assert check_drawing(src) == []


def test_a_claim_reference_must_resolve_and_match_kind(tmp_path):
    src = _repo(tmp_path, "Done and measured.",
                [{"kind": "done", "quote": "Done and measured.", "claim": 5},
                 {"kind": "done", "quote": "Done and measured.", "claim": 1}],
                [{"kind": "measurement", "text": "t"}])
    assert [f.check for f in check_drawing(src)] == ["unresolved", "kind-mismatch"]


def test_an_unfiled_mark_convicts_and_a_silent_join_convicts(tmp_path):
    src = _repo(tmp_path, "It is finished.",
                [{"kind": "done", "quote": "It is finished.",
                  "unfiled": "no claim written yet"},
                 {"kind": "done", "quote": "It is finished."}])
    assert [f.check for f in check_drawing(src)] == ["unfiled", "unjoined"]


def test_a_missing_drawing_is_named_not_guessed(tmp_path):
    src = tmp_path / "doc.md"
    src.write_text("Prose without a drawing.", encoding="utf-8")
    assert [f.check for f in check_drawing(src)] == ["missing"]


def test_a_kind_outside_the_deciders_vocabulary_is_refused(tmp_path):
    src = _repo(tmp_path, "Some sentence.",
                [{"kind": "opinion", "quote": "Some sentence.", "claim": 1}],
                [{"kind": "opinion", "text": "t"}])
    assert "unknown-kind" in [f.check for f in check_drawing(src)]


def test_line_ending_materialization_is_not_drift(tmp_path):
    # observed 2026-08-25: git checkout restored a file with different line
    # endings than the drawing was derived from; content had not changed
    src = _repo(tmp_path, "Line one.\nLine two.\n", [])
    src.write_bytes(b"Line one.\r\nLine two.\r\n")
    assert check_drawing(src) == []

def test_a_quoted_measurement_carries_both_cells_of_its_cross_tab(tmp_path):
    # the register's computable core: the favourable cell alone does not travel
    src = _repo(tmp_path, "The radar caught 106 across the corpus.",
                [{"kind": "measurement",
                  "quote": "The radar caught 106 across the corpus.", "claim": 1}],
                [{"kind": "measurement", "text": "t",
                  "caught": 106, "false_alarms": 70}])
    found = check_drawing(src)
    assert [f.check for f in found] == ["half-the-cross-tab"]
    assert "false_alarms=70" in found[0].why


def test_a_quote_with_both_cells_passes(tmp_path):
    src = _repo(tmp_path, "106 caught against 70 false alarms.",
                [{"kind": "measurement",
                  "quote": "106 caught against 70 false alarms.", "claim": 1}],
                [{"kind": "measurement", "text": "t",
                  "caught": 106, "false_alarms": 70}])
    assert check_drawing(src) == []
