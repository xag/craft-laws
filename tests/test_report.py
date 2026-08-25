"""The commit-message register gate: filed measurements travel whole."""

import json
import subprocess
from pathlib import Path

from craft.report import _alarm, added_measurements, check_commit


def _repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for k, v in (("user.email", "t@example.invalid"), ("user.name", "t")):
        subprocess.run(["git", "-C", str(tmp_path), "config", k, v], check=True)
    return tmp_path


def _commit(root: Path, message: str, claims: list[dict]):
    with (root / "claims.jsonl").open("a", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c) + "\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", message],
                   check=True)


def test_a_one_cell_message_convicts_and_names_the_missing_cell(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "The gate works: 12 caught",
            [{"kind": "measurement", "text": "t", "caught": 12, "false_alarms": 3}])
    found = check_commit(root)
    assert [f.check for f in found] == ["half-the-cross-tab"]
    assert "false_alarms=3" in found[0].why


def test_a_whole_cross_tab_message_passes(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "First run: 12 caught, 3 false alarms",
            [{"kind": "measurement", "text": "t", "caught": 12, "false_alarms": 3}])
    assert check_commit(root) == []


def test_a_commit_filing_no_measurement_owes_nothing(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "anything at all", [{"kind": "done", "text": "t"}])
    assert check_commit(root) == []


def test_only_added_lines_are_read_from_the_diff(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "old: 5 caught, 2 false alarms",
            [{"kind": "measurement", "text": "old", "caught": 5,
              "false_alarms": 2}])
    _commit(root, "a later commit filing only a done-claim",
            [{"kind": "done", "text": "t"}])
    assert added_measurements(root, "HEAD") == []
    assert check_commit(root) == []


def test_the_alarm_is_live(capsys):
    assert _alarm() == 0
