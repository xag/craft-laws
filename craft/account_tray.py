"""A system-tray icon for craft.account: shows whether turns are being checked, and flips it.

A FACE on `craft.account_toggle`, never a second authority. It owns no state -- it reads
what `account_toggle.state()` reads (the panic file, the wiring in settings.json) and
flips through the same two functions a human or an agent would call. It POLLS, because
the state it shows can be changed by hands that are not this icon's, and an icon that
only knew what it did itself would show ON over a machine somebody just switched off.

Three colours, because the toggle says there are three states worth telling apart:

  GREEN  disarmed and wired -- every turn is asked for an account and checked.
  GREY   armed -- both hooks no-op, by request.
  AMBER  the liar state: not armed, but a hook is missing from settings.json, so
         nothing is checked and the switch says it is on.

Left-click flips it. The icon is a filled badge with a state glyph - check for ON,
dash for OFF, exclamation for the liar state - because at 16 tray pixels a drawing
with thin strokes turns to fog; colour and glyph carry the state redundantly, so it
still reads without colour. Drawn at 256px and downscaled once with Lanczos, edge to
edge, no ornament. `pystray` and `Pillow` arrive via the `tray` extra -- the checker
itself stays stdlib. Run headless with `pythonw -m craft.account_tray`; a second
launch bows out rather than stacking icons.
"""

from __future__ import annotations

import ctypes
import sys
import threading

import pystray
from PIL import Image, ImageDraw

from craft import account_toggle

POLL_SECONDS = 4.0
_stop = threading.Event()

GREEN, GREY, AMBER = "#2f9e44", "#868e96", "#e8890c"


def already_running() -> bool:
    """One icon per machine: two icons showing different states is the ambiguity this
    kind of switch exists to remove."""
    try:
        ctypes.windll.kernel32.CreateMutexW(None, False, "craft-account-tray")
        return ctypes.windll.kernel32.GetLastError() == 183   # ERROR_ALREADY_EXISTS
    except AttributeError:                                    # not Windows
        return False


def colour(s: dict) -> str:
    return {"green": GREEN, "grey": GREY, "amber": AMBER}[s["colour"]]


def image(fill: str, glyph: str = "open") -> Image.Image:
    """A filled badge with an eye - the critic watches replies. Open when
    reviewing, closed when off, struck through in the liar state (claims to
    watch, does not). A check glyph read as a to-do app; an eye says what this
    actually does. Drawn at 256px, downscaled once with Lanczos."""
    S = 256
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((6, 6, S - 6, S - 6), radius=58, fill=fill)
    white = "#ffffff"
    if glyph == "closed":
        # the lower lid: a thick downward arc, with three short lashes
        d.arc((40, 8, 216, 168), start=25, end=155, fill=white, width=24)
        for x0, y0, x1, y1 in ((70, 138, 52, 172), (128, 152, 128, 188),
                               (186, 138, 204, 172)):
            d.line((x0, y0, x1, y1), fill=white, width=18)
    else:
        # the open eye: white almond (two overlapping arcs approximated by an
        # ellipse), pupil punched in the badge colour, white highlight dot
        d.ellipse((36, 78, 220, 178), fill=white)
        d.ellipse((98, 98, 158, 158), fill=fill)
        d.ellipse((134, 106, 152, 124), fill=white)
        if glyph == "struck":
            # the liar state: the eye crossed out, badge-coloured stroke with a
            # thin white edge so it reads over the sclera
            d.line((52, 208, 204, 48), fill=white, width=40)
            d.line((52, 208, 204, 48), fill=fill, width=22)
    return img.resize((64, 64), Image.LANCZOS)


def glyph_for(s: dict) -> str:
    return {"green": "open", "grey": "closed", "amber": "struck"}[s["colour"]]


def title(s: dict) -> str:
    if s["armed"]:
        return "craft.account - OFF, both hooks no-op"
    missing = [e for e, v in s["wired"].items() if not v]
    if missing:
        return ("craft.account - AMBER, hooks NOT wired: " + ", ".join(missing))[:127]
    return "craft.account - ON, every turn asked for an account and checked"


def refresh(icon: pystray.Icon) -> None:
    s = account_toggle.state()
    icon.icon = image(colour(s), glyph_for(s))
    icon.title = title(s)


def flip(icon: pystray.Icon, _item) -> None:
    if account_toggle.off():
        account_toggle.enable()      # disarms AND wires: on has to mean on
    else:
        account_toggle.disable()
    refresh(icon)


def _poll(icon: pystray.Icon) -> None:
    icon.visible = True
    while not _stop.wait(POLL_SECONDS):
        try:
            refresh(icon)
        except Exception:
            pass                     # a tray icon must never take the session with it


def main() -> int:
    if already_running():
        print("a craft.account tray icon is already running")
        return 0
    s = account_toggle.state()
    icon = pystray.Icon("craft-account", image(colour(s), glyph_for(s)), title(s),
                        menu=pystray.Menu(
        pystray.MenuItem("Turn checking on/off", flip, default=True),
        pystray.MenuItem("Status", lambda *_: print(account_toggle.render(
            account_toggle.state()))),
        pystray.MenuItem("Quit", lambda ic, _i: (_stop.set(), ic.stop())),
    ))
    icon.run(setup=_poll)
    return 0


if __name__ == "__main__":
    sys.exit(main())
