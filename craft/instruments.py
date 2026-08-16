"""The instrument practice pack: the rendered-world laws' probe logic, written once.

The census (docs/mechanization.md) carried ~10 laws whose mechanism was "instrument
practice, zero vocabulary" — the only rows where the mechanism was a pattern rather
than code in this repo. This module is that code: PURE FUNCTIONS over data a walker
collects. The split is the same one the whole estate runs on — the app owns the
browser (its walker knows its controls, its selectors, its way of taking a shot),
and the judgment over what came back is generic and lives here, so every adopter's
walker calls the same deciders and a sharpened probe sharpens everywhere at once.

Every function convicts with certainty or stays silent — the decider discipline: a
red here is a fact about the collected data, never a heuristic's opinion. What a
function cannot decide from its inputs is not its finding to make; the collection
contract per function says exactly what the walker must gather.

The alarm test travels with the pack: `python -m craft.instruments` runs every
check against a convicting example and a clean one, and exits 1 if any alarm is
dead — a checker that has never been seen red is relocated guessing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from craft.laws import LAWS

_LAW_IDS = {law.id for law in LAWS}


@dataclass
class ProbeFinding:
    law: str
    where: str        # the surface, control, widget or image the conviction names
    quote: str        # the collected evidence, verbatim enough to argue with
    why: str


def _law(law_id: str) -> str:
    if law_id not in _LAW_IDS:
        raise ValueError(f"no law '{law_id}' in craft@")
    return law_id


# --- orientation ---------------------------------------------------------------------

def check_orientation(readings: Mapping[str, Mapping[str, str]]
                      ) -> list[ProbeFinding]:
    """works-both-ways-up: nothing the app says in one orientation is unsayable in
    the other. Collection contract: per surface, the rendered prose in 'portrait'
    and 'landscape' (the walker reads the same state twice, rotated). Convicts on
    words present whole in one orientation and absent from the other — layout may
    reflow freely; CONTENT lost to a rotation is the certain breach."""
    law = _law("works-both-ways-up")
    out: list[ProbeFinding] = []
    for surface, sides in readings.items():
        a, b = sides.get("portrait", ""), sides.get("landscape", "")
        if not a or not b:
            continue                      # one side unread is the walker's gap to report
        wa = {w for w in a.split() if len(w) > 3}
        wb = {w for w in b.split() if len(w) > 3}
        for lost, kept, way in ((wa - wb, "landscape", "portrait"),
                                (wb - wa, "portrait", "landscape")):
            if lost:
                out.append(ProbeFinding(
                    law=law, where=surface,
                    quote=" ".join(sorted(lost)[:8]),
                    why=f"said in {way} and gone in {kept} — a rotation may "
                        "reflow the words, never take them."))
    return out


# --- colour --------------------------------------------------------------------------

def check_grayscale_signal(surface: str,
                           gray_a: Sequence[Sequence[int]],
                           gray_b: Sequence[Sequence[int]],
                           colors_differ: bool) -> list[ProbeFinding]:
    """colour-is-never-the-only-signal, the shot half: two states whose difference
    matters (errored vs healthy, selected vs not), each desaturated to a luminance
    matrix by the walker. If colour differed and the grayscales are identical, the
    distinction was carried by colour and nothing else — the falsifier is literally
    'desaturate a screenshot: some information disappears', measured."""
    law = _law("colour-is-never-the-only-signal")
    if colors_differ and [list(r) for r in gray_a] == [list(r) for r in gray_b]:
        return [ProbeFinding(
            law=law, where=surface,
            quote="grayscale(state A) == grayscale(state B), colour differs",
            why="the two states are indistinguishable without colour vision or "
                "with a monochrome screen — the signal must also be carried by "
                "words, shape, or a mark.")]
    return []


# --- touch ---------------------------------------------------------------------------

def check_touch_commit(controls: Iterable[Mapping[str, str]]) -> list[ProbeFinding]:
    """touch-commits-on-release: a control commits when the finger lifts, never when
    it lands. Collection contract: per control, `commits_on` observed by the event
    probe ('press' if the act fired on pointerdown/touchstart, 'release' if on
    up/click). A press-commit can never be slid off and cancelled."""
    law = _law("touch-commits-on-release")
    return [ProbeFinding(
        law=law, where=str(c.get("id", "?")),
        quote=f"commits_on={c.get('commits_on')}",
        why="the act fires when the finger lands, so a touch can never be "
            "slid off and cancelled — commit on release.")
        for c in controls if c.get("commits_on") == "press"]


def check_plain_alternative(acts: Iterable[Mapping[str, object]]
                            ) -> list[ProbeFinding]:
    """gesture-has-a-plain-alternative: every act reachable by swipe, long-press or
    multi-touch is also reachable by a plain tap on a visible control. Collection
    contract: per act, the gesture that reaches it and the list of plain controls
    that also do."""
    law = _law("gesture-has-a-plain-alternative")
    return [ProbeFinding(
        law=law, where=str(a.get("act", "?")),
        quote=f"gesture={a.get('gesture')}, plain_controls=[]",
        why="only a gesture reaches this act — a person who cannot make it, or "
            "cannot discover it, has no way in.")
        for a in acts if a.get("gesture") and not a.get("plain_controls")]


# --- keyboard ------------------------------------------------------------------------

def check_tab_stops(widgets: Iterable[Mapping[str, object]]) -> list[ProbeFinding]:
    """one-tab-stop-per-widget: a composite widget (radiogroup, listbox, menu,
    tablist, grid) is ONE Tab stop; arrows move inside. Collection contract: per
    widget, its ARIA role and the number of Tab stops the focus walk counted in
    it."""
    law = _law("one-tab-stop-per-widget")
    composite = {"radiogroup", "listbox", "menu", "menubar", "tablist", "grid",
                 "tree", "toolbar"}
    return [ProbeFinding(
        law=law, where=str(w.get("id", "?")),
        quote=f"role={w.get('role')}, tab_stops={w.get('tab_stops')}",
        why="a composite widget claims one Tab stop and moves inside on arrows; "
            "every extra stop is a keyboard user tabbing through the whole set.")
        for w in widgets
        if str(w.get("role", "")) in composite and int(w.get("tab_stops", 1)) > 1]


# --- direction -----------------------------------------------------------------------

def check_rtl_mirror(boxes_ltr: Mapping[str, Sequence[float]],
                     boxes_rtl: Mapping[str, Sequence[float]],
                     viewport_width: float,
                     meaning: frozenset[str] | set[str] = frozenset(),
                     tolerance: float = 8.0) -> list[ProbeFinding]:
    """rtl-mirrors-except-meaning, both directions of the biconditional. Collection
    contract: per element id, its (x, width) box under LTR and under RTL at the
    same viewport, plus the app's declared `meaning` set — the elements whose
    orientation IS meaning (a play arrow, a clock, a signature glyph) and must NOT
    mirror. Layout elements must land at the mirrored x; meaning elements must
    not."""
    law = _law("rtl-mirrors-except-meaning")
    out: list[ProbeFinding] = []
    for el, (x, w) in boxes_ltr.items():
        if el not in boxes_rtl:
            continue
        rx = boxes_rtl[el][0]
        mirrored_x = viewport_width - (x + w)
        mirrored = abs(rx - mirrored_x) <= tolerance
        stayed = abs(rx - x) <= tolerance
        if el in meaning and mirrored and not stayed:
            out.append(ProbeFinding(
                law=law, where=el,
                quote=f"ltr x={x}, rtl x={rx} (mirrored)",
                why="declared meaning-bearing, and it mirrored anyway — a glyph "
                    "whose direction is its meaning must hold still."))
        elif el not in meaning and not mirrored:
            out.append(ProbeFinding(
                law=law, where=el,
                quote=f"ltr x={x}, rtl x={rx}, expected ~{mirrored_x:.0f}",
                why="layout did not mirror under RTL — the reading order flipped "
                    "and this element stayed put."))
    return out


# --- truncation ----------------------------------------------------------------------

def check_truncation_signposts(lists_shown: Iterable[Mapping[str, object]]
                               ) -> list[ProbeFinding]:
    """truncation-is-signposted: a cut-off set never looks complete. Collection
    contract: per truncated collection, how many items are shown, how many exist,
    and whether any cue is on screen (a count, an arrow, a partial item — the
    walker records `cue` as the cue's own text, empty when there is none)."""
    law = _law("truncation-is-signposted")
    return [ProbeFinding(
        law=law, where=str(t.get("id", "?")),
        quote=f"shown {t.get('shown')} of {t.get('total')}, cue: none",
        why="the visible items form a tidy, complete-looking set and more exist "
            "— the cut must show, or the hidden rest does not exist to anyone.")
        for t in lists_shown
        if int(t.get("shown", 0)) < int(t.get("total", 0))
        and not str(t.get("cue", ""))]


# --- text in images ------------------------------------------------------------------

def check_text_in_images(images: Iterable[Mapping[str, object]]
                         ) -> list[ProbeFinding]:
    """no-text-baked-into-images: words ship as text, never as pixels. Collection
    contract: per image element, a digest of its rendered pixels per locale (the
    walker screenshots the image region under each shipped language). Pixels that
    CHANGE with the locale are localized words rendered as pixels — text somebody
    baked in, invisible to translation review, screen readers and zoom alike."""
    law = _law("no-text-baked-into-images")
    out: list[ProbeFinding] = []
    for img in images:
        digests = dict(img.get("digest_by_locale") or {})
        if len(set(digests.values())) > 1:
            out.append(ProbeFinding(
                law=law, where=str(img.get("id", "?")),
                quote=", ".join(f"{loc}:{d[:8]}" for loc, d in
                                sorted(digests.items())),
                why="the image's pixels change with the locale — it contains "
                    "rendered words, which no translator, screen reader or zoom "
                    "can reach."))
    return out


# --- the alarm test ------------------------------------------------------------------

def _alarm() -> int:
    """Every check against one convicting example and one clean one. A dead alarm
    exits 1: a checker that has never been seen red is relocated guessing."""
    rings: list[tuple[str, bool, bool]] = []

    f = check_orientation({"tab:board": {"portrait": "Cook dinner tonight",
                                         "landscape": "Cook"}})
    g = check_orientation({"tab:board": {"portrait": "Cook dinner",
                                         "landscape": "dinner Cook"}})
    rings.append(("orientation", bool(f), not g))

    f = check_grayscale_signal("form", [[9, 9]], [[9, 9]], colors_differ=True)
    g = check_grayscale_signal("form", [[9, 9]], [[2, 9]], colors_differ=True)
    rings.append(("grayscale", bool(f), not g))

    f = check_touch_commit([{"id": "save", "commits_on": "press"}])
    g = check_touch_commit([{"id": "save", "commits_on": "release"}])
    rings.append(("touch", bool(f), not g))

    f = check_plain_alternative([{"act": "postpone", "gesture": "swipe-right",
                                  "plain_controls": []}])
    g = check_plain_alternative([{"act": "postpone", "gesture": "swipe-right",
                                  "plain_controls": ["menu-postpone"]}])
    rings.append(("gesture", bool(f), not g))

    f = check_tab_stops([{"id": "days", "role": "radiogroup", "tab_stops": 7}])
    g = check_tab_stops([{"id": "days", "role": "radiogroup", "tab_stops": 1}])
    rings.append(("tab-stops", bool(f), not g))

    f = check_rtl_mirror({"back": (10, 40)}, {"back": (10, 40)}, 390)
    g = check_rtl_mirror({"back": (10, 40)}, {"back": (340, 40)}, 390)
    rings.append(("rtl", bool(f), not g))

    f = check_truncation_signposts([{"id": "gallery", "shown": 4, "total": 9,
                                     "cue": ""}])
    g = check_truncation_signposts([{"id": "gallery", "shown": 4, "total": 9,
                                     "cue": "+5"}])
    rings.append(("truncation", bool(f), not g))

    f = check_text_in_images([{"id": "hero", "digest_by_locale":
                               {"en": "aaaa1111", "fr": "bbbb2222"}}])
    g = check_text_in_images([{"id": "hero", "digest_by_locale":
                               {"en": "aaaa1111", "fr": "aaaa1111"}}])
    rings.append(("text-in-images", bool(f), not g))

    dead = [name for name, rang, clean in rings if not (rang and clean)]
    for name, rang, clean in rings:
        state = "ok " if rang and clean else "DEAD"
        print(f"  {state} {name}: convicting example "
              f"{'convicts' if rang else 'PASSES'}, clean example "
              f"{'passes' if clean else 'CONVICTS'}")
    if dead:
        print(f"\nthe alarm is DEAD for: {', '.join(dead)} — do not trust these "
              "checks' greens")
        return 1
    print(f"\nevery alarm rings: {len(rings)} probe decider(s), each seen red and "
          "each seen green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_alarm())
