"""The switch for craft.account. `python -m craft.account_toggle on | off | status`.

Two dimensions, reported separately, because they fail differently:

  ARMED   `~/.craft/ACCOUNTS_OFF` exists -> both hooks no-op. Reaches a session that is
          ALREADY RUNNING, on the next hook call. Instant.
  WIRED   the hooks are in ~/.claude/settings.json -> new sessions run them at all.

`on` disarms AND wires, because a checker that reports itself on while its hooks are
missing is the worst of the states: it checks nothing and says it is checking.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from craft.account_hook import off, off_path

SETTINGS = Path.home() / ".claude" / "settings.json"
COMMAND = ("uv run --no-sync --directory C:/Users/trans/Projects/craft-laws "
           "python -m craft.account_hook")


def _settings() -> dict:
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def wired() -> dict:
    """Which events run the account hook, as settings.json has it now."""
    hooks = (_settings().get("hooks") or {})
    out = {}
    for event in ("UserPromptSubmit", "Stop"):
        out[event] = any(h.get("command") == COMMAND
                         for group in (hooks.get(event) or [])
                         for h in (group.get("hooks") or []))
    return out


def state() -> dict:
    w = wired()
    armed = off()
    if armed:
        colour = "grey"
    elif all(w.values()):
        colour = "green"
    else:
        colour = "amber"        # claiming to check while a hook is missing
    return {"armed": armed, "wired": w, "colour": colour}


def render(s: dict) -> str:
    if s["armed"]:
        return "OFF - the switch is armed; both hooks no-op in every running session."
    missing = [e for e, v in s["wired"].items() if not v]
    if missing:
        return ("AMBER - not armed, but these hooks are missing from settings.json: "
                + ", ".join(missing) + ". Nothing is being checked. Run `on` to wire.")
    return "ON - disarmed and wired; every turn is asked for an account and checked."


def enable() -> None:
    try:
        off_path().unlink()
    except OSError:
        pass
    data = _settings()
    hooks = data.setdefault("hooks", {})
    for event in ("UserPromptSubmit", "Stop"):
        groups = hooks.setdefault(event, [])
        if any(h.get("command") == COMMAND
               for g in groups for h in (g.get("hooks") or [])):
            continue
        groups.append({"hooks": [{"type": "command", "command": COMMAND,
                                  "timeout": 20}]})
    SETTINGS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def disable() -> None:
    p = off_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("armed\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m craft.account_toggle",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=("on", "off", "status"))
    args = ap.parse_args(argv)
    if args.action == "on":
        enable()
    elif args.action == "off":
        disable()
    print(render(state()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
