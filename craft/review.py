# -*- coding: utf-8 -*-
"""Every review that judges a turn, in one registry, each switchable on its own.

Three reviews of the agent's own work grew separately, and by 2026-09-01 each had its own
hook entry, its own on/off, and no way to ask "what is checking my replies right now?"
without reading two modules and a settings file. They differ by WHAT THEY READ, and the
names say so — they used to be `claims`, `argument` and `intake`, and the owner asked what
the difference was, which is the only review a name gets:

  record     the turn's claims record, judged whole — both what it says and where it
             says nothing. The claim deciders convict a done-claim resting on the
             author's own test output or a fixed-claim with no reproduction; and
             a-corpus-of-reports-carries-its-reporting-bias (PRISMA 2020 items 14 and
             21) names the repos this turn EDITED and then filed nothing about, because
             a conviction rate drawn from self-filed records is a rate over what somebody
             chose to file. Data, no model, about a millisecond.
  reasoning  what the reply SAID TO THE USER: the critic reconstructs its argument and
             the deciders judge it — a conclusion with nothing supporting it, a "nothing
             was found" with no search behind it, a name coined and never defined. Costs
             one small-model call, detached, never blocking.

So: what the turn recorded, and what the turn said. Two, because they read different
things and cost differently; the record's silences are NOT a third — that was `intake`,
and it was a review of its own only because it had its own code path. It is one law over
the same corpus at the same cost, and nobody wants "check what the record says" without
"say where it is silent": they are two halves of judging one record. The rule about
sourcing rules held (that law is cited and its source censused whole); the extra SWITCH
was the unearned part, and it is gone.

What survives per review is its JUDGMENT; the plumbing (delivery, dedupe, the seam)
belongs to the courier.

    python -m craft.review              # what runs, and what is off
    python -m craft.review on reasoning  # per-review switches, reaching running sessions
    python -m craft.review off

A review is OFF the moment its file exists — the switch is read at every turn, so it
reaches a session already running rather than the next one, which is the property that
makes it a switch and not a setting.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

from . import flight

_ROOT = Path(__file__).resolve().parents[1]


def _home() -> Path:
    return Path.home() / ".craft"


@dataclass(frozen=True)
class Review:
    """One review of a reply: an id, what it looks at, what it costs to run, and the
    producer label its findings travel under in the courier — the one fact that lets a
    watcher count what a review found without reading the finding."""

    id: str
    what: str
    cost: str
    producer: str

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
    Review("record", "the turn's claims — what it wrote down, and where it wrote nothing",
           "data only, about a millisecond", "craft.claims"),
    Review("reasoning", "what the reply told the user, and whether it holds up",
           "one small-model call, detached — never blocks", "craft.critic"),
)

BY_ID = {r.id: r for r in REVIEWS}


def enabled() -> tuple:
    return tuple(r for r in REVIEWS if r.on)


def findings(since: float) -> dict:
    """How many findings each review posted after `since`, counted off the courier's
    outboxes without taking anything: the findings are addressed to sessions, and the
    session is the reader; a watcher only counts. Across every session on this machine,
    because the boxes are keyed by a one-way hash and cannot be told apart — so the
    honest question is "since when", never "in which session". Empty without a courier."""
    try:
        from courier import mail
    except ImportError:
        return {r.id: 0 for r in REVIEWS}
    by_producer = {r.producer: r.id for r in REVIEWS}
    out = {r.id: 0 for r in REVIEWS}
    for m in mail.survey(since):
        rid = by_producer.get(m.get("producer"))
        if rid is not None:
            out[rid] += 1
    return out


def state(since: float | None = None) -> dict:
    """What is checking replies right now — the question that needed two modules and a
    settings file to answer. With `since`, also what they found after that moment:
    a count per review under `findings`, and their sum under `landed`."""
    on = enabled()
    s = {"on": [r.id for r in on], "off": [r.id for r in REVIEWS if not r.on],
         "colour": "green" if len(on) == len(REVIEWS)
                   else "grey" if not on else "amber"}
    if since is not None:
        s["since"] = since
        s["findings"] = findings(since)
        s["landed"] = sum(s["findings"].values())
    return s


def render(s: dict) -> str:
    if not s["on"]:
        line = "reviews OFF — no reply is being checked"
    else:
        line = "reviews on: " + ", ".join(s["on"])
        line += f"   (off: {', '.join(s['off'])})" if s["off"] else ""
    if s.get("landed"):
        clock = time.strftime("%H:%M", time.localtime(s["since"]))
        per = ", ".join(f"{k} {v}" for k, v in s["findings"].items() if v)
        line += f"\n{s['landed']} finding(s) since {clock}: {per}"
    elif "landed" in s:
        clock = time.strftime("%H:%M", time.localtime(s["since"]))
        line += f"\nnothing found since {clock}"
    return line


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

    if "record" in on:
        from . import claims_hook
        claims_hook.run(payload)

    if "reasoning" in on:
        from .account_hook import spawn_critic
        spawn_critic(session, transcript, payload.get("cwd"))
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
