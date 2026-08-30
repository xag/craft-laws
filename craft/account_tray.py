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

INK = "#3b3b3b"      # the standard dark tray-glyph grey beside OneDrive and friends
WARN = "#c47a10"     # amber ink, reserved for the liar state


def already_running() -> bool:
    """One icon per machine: two icons showing different states is the ambiguity this
    kind of switch exists to remove."""
    try:
        ctypes.windll.kernel32.CreateMutexW(None, False, "craft-account-tray")
        return ctypes.windll.kernel32.GetLastError() == 183   # ERROR_ALREADY_EXISTS
    except AttributeError:                                    # not Windows
        return False


def image(state: str = "on") -> Image.Image:
    """A bare section sign, no badge, in the dark grey of the neighbouring tray
    glyphs. Segoe UI Black with a dilation pass for weight - the bold cut read
    as a thin line at 16 pixels - and the off-state strike is narrow with a
    modest halo, so the sign stays recognizable under it (the wide first cut
    hid what the icon was). Amber ink is the one use of colour, reserved for
    the liar state. Drawn at 256px, downscaled once with Lanczos."""
    from PIL import ImageChops, ImageFilter, ImageFont
    S = 256
    colour = WARN if state == "liar" else INK
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = None
    for path in ("C:/Windows/Fonts/seguibl.ttf", "C:/Windows/Fonts/segoeuib.ttf",
                 "C:/Windows/Fonts/georgiab.ttf"):
        try:
            font = ImageFont.truetype(path, 250)
            break
        except OSError:
            continue
    if font is not None:
        bb = d.textbbox((0, 0), "§", font=font)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((S - w) / 2 - bb[0], (S - h) / 2 - bb[1]), "§", font=font,
               fill=colour)
        a = img.getchannel("A").filter(ImageFilter.MaxFilter(7))
        solid = Image.new("RGBA", (S, S), colour)
        img = Image.composite(solid, Image.new("RGBA", (S, S), (0, 0, 0, 0)), a)
    else:                       # no font: a plain square keeps the state visible
        d.rounded_rectangle((48, 48, 208, 208), radius=40, fill=colour)
    if state == "off":
        halo = Image.new("L", (S, S), 0)
        ImageDraw.Draw(halo).line((30, 226, 226, 30), fill=255, width=34)
        img.putalpha(ImageChops.subtract(img.getchannel("A"), halo))
        d = ImageDraw.Draw(img)
        d.line((38, 218, 218, 38), fill=colour, width=16)
        for cx, cy in ((38, 218), (218, 38)):
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=colour)
    return img.resize((64, 64), Image.LANCZOS)


def state_name(s: dict) -> str:
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
    icon.icon = image(state_name(s))
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
    icon = pystray.Icon("craft-account", image(state_name(s)), title(s),
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
