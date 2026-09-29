"""The runner of every check: seen red, seen green, answered in list order, and CI's only step."""

import sys
from pathlib import Path

from craft import gate

ROOT = Path(__file__).resolve().parents[1]


def test_a_red_check_makes_the_gate_red_and_the_list_order_holds(capsys):
    checks = (gate.Check("fails", ("craft.gate", "--jobs", "not-a-number")),
              gate.Check("holds", ("craft.gate", "--help")))
    assert gate.run(checks, jobs=2) == 1
    out = capsys.readouterr().out.splitlines()
    marks = [l.split()[0] + " " + l.split()[-1] for l in out if l[:3] in ("ok ", "RED")]
    assert marks == ["RED fails", "ok holds"]


def test_every_check_green_is_a_green_gate(capsys):
    assert gate.run((gate.Check("holds", ("craft.gate", "--help")),), jobs=1) == 0


def test_ci_runs_the_gate_and_nothing_beside_it():
    """The list has one home: a step added to the workflow instead of CHECKS would run on CI
    and never on the machine where the work is done."""
    workflow = (ROOT / ".github" / "workflows" / "check.yml").read_text(encoding="utf-8")
    runs = [l.strip() for l in workflow.splitlines() if l.strip().startswith("run:")]
    assert runs == ["run: uv run python -m craft.gate"]


def test_another_project_runs_its_own_commands_from_its_own_root(tmp_path, capsys):
    """A project hands its list to the runner: whole command lines, run from its root."""
    here = (sys.executable, "-c", f"import os, sys; sys.exit(0 if os.path.samefile(os.getcwd(), {str(tmp_path)!r}) else 1)")
    assert gate.run((gate.Check("runs from the project's root", command=here),), jobs=1, cwd=tmp_path) == 0
    red = (sys.executable, "-c", "import sys; print('the project says no'); sys.exit(3)")
    assert gate.run((gate.Check("a red command", command=red),), jobs=1, cwd=tmp_path) == 1
    assert "the project says no" in capsys.readouterr().out
