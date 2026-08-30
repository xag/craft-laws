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


def image(fill: str, glyph: str = "on") -> Image.Image:
    """The section sign on a state badge. The checker's whole job is citing laws,
    and the sign a law is cited by is the mark - a letterform, because at 16 tray
    pixels a letter survives where every pictogram tried here turned into
    something else (a to-do check, an eye, a mask). State is carried twice:
    colour, and solid-versus-hollow (a drained outline is off). Georgia bold for
    a jurisprudential serif; Segoe UI bold is the fallback when Georgia is not
    installed. Drawn at 256px, downscaled once with Lanczos."""
    from PIL import ImageFont
    S = 256
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    hollow = glyph == "off"
    if hollow:
        d.rounded_rectangle((10, 10, S - 10, S - 10), radius=54, outline=fill,
                            width=18)
        glyph_col = fill
    else:
        d.rounded_rectangle((6, 6, S - 6, S - 6), radius=58, fill=fill)
        glyph_col = "#ffffff"
    font = None
    for path in (r"C:\Windows\Fonts\georgiab.ttf",
                 r"C:\Windows\Fonts\segoeuib.ttf"):
        try:
            font = ImageFont.truetype(path, 185)
            break
        except OSError:
            continue
    if font is None:                    # no known font: the badge alone carries state
        return img.resize((64, 64), Image.LANCZOS)
    bb = d.textbbox((0, 0), "§", font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((S - w) / 2 - bb[0], (S - h) / 2 - bb[1]), "§", font=font,
           fill=glyph_col)
    return img.resize((64, 64), Image.LANCZOS)


def glyph_for(s: dict) -> str:
    return {"green": "on", "grey": "off", "amber": "liar"}[s["colour"]]


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
