# -*- coding: utf-8 -*-
"""The tray icon for the reply reviews: what is checking your answers, and which ones.

A FACE on `craft.review`, never a second authority. It owns no state — it reads what
`review.state()` reads (the per-review switch files and the master one) and flips through
the same functions a human at a prompt or an agent over MCP would call. It POLLS, because
what it shows can be changed by hands that are not this icon's.

The menu carries one checkbox per review, which is the thing the old icon could not do:
`craft.account` had a single on/off over a lane that had quietly become three reviews with
different costs. Switching the argument review off (its one small-model call per turn) while
keeping the claim deciders (a millisecond of data) is a real thing to want, and until now
the only way to ask for it was to hand-edit settings.json.

  GREEN  every review is on
  AMBER  some on, some off — the deliberate middle, and the icon says which in its tooltip
  GREY   nothing is reviewing replies

Run headless with `pythonw -m craft.review_tray`; a second launch bows out rather than
stacking icons. `pystray` and `Pillow` arrive via the `tray` extra — the reviews themselves
stay stdlib.
"""

from __future__ import annotations

import ctypes
import sys
import threading

import pystray
from PIL import Image, ImageChops, ImageDraw, ImageFont

from craft import review

POLL_SECONDS = 4.0
_stop = threading.Event()

INK = "#3b3b3b"      # the standard dark tray-glyph grey beside OneDrive and friends
WARN = "#c47a10"     # amber ink: some reviews on, some off


def already_running() -> bool:
    """One icon per machine: two icons showing different states is the ambiguity this
    kind of switch exists to remove."""
    try:
        ctypes.windll.kernel32.CreateMutexW(None, False, "craft-review-tray")
        return ctypes.windll.kernel32.GetLastError() == 183   # ERROR_ALREADY_EXISTS
    except AttributeError:                                    # not Windows
        return False


def image(state: str = "green") -> Image.Image:
    """A bare section sign in the dark grey of the neighbouring tray glyphs — the mark
    the account tray wore, kept, because this icon replaces it and a user should not
    have to learn a new shape for the same job. Amber when the set is mixed, struck
    through when nothing is reviewing. Drawn at 256px, downscaled once with Lanczos."""
    S = 256
    colour = WARN if state == "amber" else INK
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = None
    for path in ("C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/times.ttf",
                 "C:/Windows/Fonts/segoeui.ttf"):
        try:
            font = ImageFont.truetype(path, 250)
            break
        except OSError:
            continue
    if font is not None:
        bb = d.textbbox((0, 0), "§", font=font)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((S - w) / 2 - bb[0], (S - h) / 2 - bb[1]), "§", font=font, fill=colour)
    else:                       # no font: a plain square keeps the state visible
        d.rounded_rectangle((48, 48, 208, 208), radius=40, fill=colour)
    if state == "grey":
        halo = Image.new("L", (S, S), 0)
        ImageDraw.Draw(halo).line((30, 226, 226, 30), fill=255, width=34)
        img.putalpha(ImageChops.subtract(img.getchannel("A"), halo))
        d = ImageDraw.Draw(img)
        d.line((38, 218, 218, 38), fill=colour, width=16)
        for cx, cy in ((38, 218), (218, 38)):
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=colour)
    # hand Windows its own small-icon metric instead of a 64px image it will soften
    try:
        metric = ctypes.windll.user32.GetSystemMetrics(49) or 16
    except AttributeError:
        metric = 16
    side = max(32, min(64, metric * 2))
    return img.resize((side, side), Image.LANCZOS)


def title(s: dict) -> str:
    if not s["on"]:
        return "craft reviews - OFF, no reply is being checked"
    line = "craft reviews - on: " + ", ".join(s["on"])
    if s["off"]:
        line += " | off: " + ", ".join(s["off"])
    return line[:127]            # the shell truncates a tooltip past this, silently


def refresh(icon: pystray.Icon) -> None:
    s = review.state()
    icon.icon = image(s["colour"])
    icon.title = title(s)


def _toggle(item_id: str):
    def act(icon, _item=None):
        r = review.BY_ID[item_id]
        r.set(not r.on)
        if icon is not None:
            refresh(icon)
    return act


def _checked(item_id: str):
    return lambda _item: review.BY_ID[item_id].on


def _all(on: bool):
    def act(icon, _item=None):
        for r in review.REVIEWS:
            r.set(on)
        if icon is not None:
            refresh(icon)
    return act


def _flip_all(icon, _item=None) -> None:
    """The blunt one: everything off if anything is on, else everything back on."""
    _all(not review.enabled())(icon, _item)


def menu() -> pystray.Menu:
    """A default action first, then one checkbox per review.

    THE DEFAULT ITEM IS NOT DECORATION. On Windows a left-click invokes a menu's default
    item and nothing else — with no default, the icon simply does not answer a click, which
    is what a user calls a broken tray icon. The predecessor had one and this replacement
    shipped without it. Left-click flips everything; the per-review choice is one right-click
    away, where a choice belongs.

    Built once: pystray re-reads the text and checked callbacks on every open, so both the
    label and the marks follow switches flipped by other hands."""
    items = [pystray.MenuItem(f"{r.id}: {r.what}", _toggle(r.id),
                              checked=_checked(r.id))
             for r in review.REVIEWS]
    return pystray.Menu(
        pystray.MenuItem(lambda _i: ("Turn every review off" if review.enabled()
                                     else "Turn every review on"),
                         _flip_all, default=True),
        pystray.Menu.SEPARATOR,
        *items,
        pystray.Menu.SEPARATOR,
        # a balloon, not print(): under pythonw stdout is DEVNULL and the item did nothing
        pystray.MenuItem("Status", lambda ic, _i=None: ic.notify(
            review.render(review.state()), "craft reviews")),
        pystray.MenuItem("Quit", lambda ic, _i: (_stop.set(), ic.stop())),
    )


def _poll(icon: pystray.Icon) -> None:
    icon.visible = True
    while not _stop.wait(POLL_SECONDS):
        try:
            refresh(icon)
        except Exception:
            pass                     # a tray icon must never take the session with it


def main() -> int:
    if already_running():
        print("a craft review tray icon is already running")
        return 0
    s = review.state()
    icon = pystray.Icon("craft-review", image(s["colour"]), title(s), menu=menu())
    icon.run(setup=_poll)
    return 0


if __name__ == "__main__":
    sys.exit(main())
