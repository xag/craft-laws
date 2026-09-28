"""The runner of every check: seen red, seen green, answered in list order, and CI's only step."""

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
