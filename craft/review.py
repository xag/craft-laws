# -*- coding: utf-8 -*-
"""Every review that judges a reply, in one registry, each switchable on its own.

Three reviews of the agent's own answers grew separately, and by 2026-09-01 each had its
own hook entry, its own on/off, and no way to ask "what is checking my replies right now?"
without reading two modules and a settings file:

  claims    the claim deciders over what the turn RECORDED — a done-claim resting on
            producer evidence, a fixed-claim with no reproduction. Data, no model, ~1ms.
  argument  the critic reconstructs the reply's argument and the AIF deciders judge it —
            a conclusion with no warrant, an absence with no documented search, a name
            the record never used. Costs one small-model call, detached.
  intake    the reporting-bias note: this turn wrote in a repo and left its record silent.

They are one thing from where the user sits — reviews of the reply — so they are one
registry here, one Stop entry point, and one switch each. What survives per review is its
JUDGMENT; the plumbing (delivery, dedupe, the seam) belongs to the courier.

    python -m craft.review              # what runs, and what is off
    python -m craft.review on argument  # per-review switches, reaching running sessions
    python -m craft.review off

A review is OFF the moment its file exists — the switch is read at every turn, so it
reaches a session already running rather than the next one, which is the property that
makes it a switch and not a setting.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from . import flight

_ROOT = Path(__file__).resolve().parents[1]


def _home() -> Path:
    return Path.home() / ".craft"


@dataclass(frozen=True)
class Review:
    """One review of a reply: an id, what it looks at, and what it costs to run."""

    id: str
    what: str
    cost: str

    def off_path(self) -> Path:
        return _home() / f"REVIEW_OFF_{self.id}"

    @property
    def on(self) -> bool:
        # the master switch still wins, so one file silences everything as before
        from .account_hook import off as master_off
        return not master_off() and not self.off_path().exists()

    def set(self, on: bool) -> None:
        path = self.off_path()
        if on:
            try:
                path.unlink()
            except OSError:
                pass
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        except OSError:
            pass


REVIEWS = (
    Review("claims", "the claims this turn recorded, against the practice laws",
           "data only, about a millisecond"),
    Review("argument", "the argument the reply makes, reconstructed and judged",
           "one small-model call, detached — never blocks"),
    Review("intake", "repos this turn wrote in and left silent in the record",
           "data only"),
)

BY_ID = {r.id: r for r in REVIEWS}


def enabled() -> tuple:
    return tuple(r for r in REVIEWS if r.on)


def state() -> dict:
    """What is checking replies right now — the question that needed two modules and a
    settings file to answer."""
    on = enabled()
    return {"on": [r.id for r in on], "off": [r.id for r in REVIEWS if not r.on],
            "colour": "green" if len(on) == len(REVIEWS)
                      else "grey" if not on else "amber"}


def render(s: dict) -> str:
    if not s["on"]:
        return "reviews OFF — no reply is being checked"
    line = "reviews on: " + ", ".join(s["on"])
    return line + (f"   (off: {', '.join(s['off'])})" if s["off"] else "")


def run(payload: dict) -> int:
    """Every enabled review, over one finished turn. Never blocks and never refuses:
    findings go to the courier, which puts them in front of the agent at its next seam."""
    if payload.get("stop_hook_active"):
        return 0
    session = str(payload.get("session_id") or "")
    transcript = payload.get("transcript_path")
    if not transcript:
        return 0
    on = {r.id for r in enabled()}

    if {"claims", "intake"} & on:
        from . import claims_hook
        claims_hook.run({**payload, "_reviews": sorted({"claims", "intake"} & on)})

    if "argument" in on:
        from .account_hook import spawn_critic
        spawn_critic(session, transcript)
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    action = (argv[0] if argv else "status").lower()
    names = argv[1:] or [r.id for r in REVIEWS]
    if action in ("on", "off"):
        unknown = [n for n in names if n not in BY_ID]
        if unknown:
            print(f"no such review: {', '.join(unknown)} — "
                  f"have {', '.join(BY_ID)}")
            return 1
        for n in names:
            BY_ID[n].set(action == "on")
    elif action != "status":
        print("usage: python -m craft.review [status | on <review>… | off <review>…]")
        return 1
    print(render(state()))
    for r in REVIEWS:
        print(f"  {'on ' if r.on else 'off'}  {r.id:<9} {r.what}\n"
              f"          {r.cost}")
    return 0


def stop(payload: dict) -> int:
    return run(payload)


def hook_main() -> int:
    """The one Stop entry point for all three reviews."""
    import json
    try:
        payload = json.load(sys.stdin)
        if payload.get("transcript_path") and not payload.get("stop_hook_active"):
            flight.record(sys.modules[__name__], "review")
        return run(payload)
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
