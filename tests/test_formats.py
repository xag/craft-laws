"""The format gate: committed records resolve their kinds through the lock."""

import json
from pathlib import Path

from craft.formats import _alarm, check_repo, kinds_used, record_files

ROOT = Path(__file__).resolve().parents[1]


def test_the_gate_is_opt_in_by_declaration(tmp_path):
    (tmp_path / "claims.jsonl").write_text('{"kind": "done"}\n', encoding="utf-8")
    assert check_repo(tmp_path) is None


def test_this_repo_declares_pins_and_covers_every_kind_in_use():
    assert check_repo(ROOT) == []


def test_the_enumeration_finds_both_record_shapes_here():
    names = {p.name for p in record_files(ROOT)}
    assert "claims.jsonl" in names
    assert "README.md.drawing.json" in names


def test_kinds_are_read_from_claims_lines_and_drawing_nodes(tmp_path):
    c = tmp_path / "claims.jsonl"
    c.write_text('{"kind": "done"}\n{"kind": "protocol"}\nnot json\n',
                 encoding="utf-8")
    assert kinds_used(c) == {"done", "protocol"}
    d = tmp_path / "x.drawing.json"
    d.write_text(json.dumps({"nodes": [{"kind": "diagnosis"}]}), encoding="utf-8")
    assert kinds_used(d) == {"diagnosis"}


def test_the_alarm_convicts_four_ways_and_clears_the_real_repo(capsys):
    assert _alarm() == 0
