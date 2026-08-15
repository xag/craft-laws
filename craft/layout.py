"""The constraint solver: layout claims proved over a viewport interval.

First consumer of interface@'s `constraint` kind. The claim class is deliberately
narrow and the guarantee deliberately exact: a `fits` constraint says a piece of
bound text fits its container at EVERY viewport width in a range, in EVERY language
the metrics carry — not at the three widths somebody sampled.

The honest split, and it is the whole architecture: what a browser alone can know is
MEASURED, once, and travels as provenance-carrying data (the font, the rendered text
widths per catalogue key per language, the container's width at two viewport
endpoints — see the consumer's measuring tool); what follows from those measurements
is SOLVED. A container measured at two widths and declared linear between them is a
line; bound text is a constant per language; a constant against a line on an interval
is decided at the endpoints, exhaustively. That declared linearity is an assumption
and it is stated in the verdict, because a proof that hides its premises is a
sample wearing a gown.

Refusals, never defaults: a constraint naming an unmeasured container, a key the
metrics never sampled, or a language the text table lacks is an error carrying the
name — an unmeasured fit reported as green would be exactly the silent pass this
estate exists to abolish.

Constraint payload consumed here (on a `constraint` node under a surface):

    {"kind": "fits",
     "text": ["<element id>", ...],      # elements whose text bindings must fit
     "container": "<box name>",          # measured as <name>@<w> in metrics["boxes"]
     "viewport": [320, 1280]}            # the interval the claim quantifies over

Metrics shape (the consumer's measuring tool writes it; provenance in the header):

    {"measured_at": ..., "origin": ..., "font": ...,
     "text": {"en": {"<key>": px, ...}, "fr": {...}},
     "boxes": {"<name>@320": px, "<name>@1280": px, ...}}
"""

from __future__ import annotations

from dataclasses import dataclass

from quern import Node

from craft.compile import bindings, elements


@dataclass
class LayoutVerdict:
    constraint: str
    lang: str
    verdict: str            # 'proved' | 'refuted'
    margin_px: float        # smallest slack over the interval; negative = overflow
    at_width: int           # the viewport width where the margin is worst
    note: str


def _container_line(metrics: dict, name: str, lo: int, hi: int) -> tuple[float, float]:
    boxes = metrics.get("boxes", {})
    try:
        w_lo, w_hi = boxes[f"{name}@{lo}"], boxes[f"{name}@{hi}"]
    except KeyError as e:
        raise ValueError(f"container '{name}' was never measured at width "
                         f"{str(e).strip(chr(39))} — measure before solving; an "
                         "unmeasured fit reported green is a silent pass") from e
    a = (w_hi - w_lo) / (hi - lo)
    return a, w_lo - a * lo                      # width(w) = a*w + b


def _text_width(metrics: dict, lang: str, element: Node) -> float:
    table = metrics.get("text", {}).get(lang)
    if table is None:
        raise ValueError(f"no '{lang}' text metrics — the fit is a claim about every "
                         "language the app ships, or it is not the text-expansion law")
    widths = []
    for b in bindings(element):
        key = b.payload.get("key", "")
        if b.payload.get("role") != "text":
            continue
        if key not in table:
            raise ValueError(f"'{key}' was never measured in '{lang}'")
        widths.append(table[key])
    if not widths:
        raise ValueError(f"element '{element.id}' binds no measured text — a fits "
                         "constraint over nothing proves nothing")
    return max(widths)


def solve_constraints(surfaces: list[Node], metrics: dict) -> list[LayoutVerdict]:
    """Every layout verdict the drawing's constraints produce under these metrics.
    Endpoint evaluation IS the interval proof: both sides are linear in the viewport
    width, so the minimum slack over [lo, hi] is attained at lo or hi."""
    out: list[LayoutVerdict] = []
    for s in surfaces:
        for c in s.children:
            if c.kind != "constraint" or c.payload.get("kind") != "fits":
                continue
            lo, hi = c.payload.get("viewport", [320, 1280])
            a, b = _container_line(metrics, c.payload["container"], lo, hi)
            named = set(c.payload.get("text", []))
            targets = [e for e in elements(s) if e.id in named]
            missing = named - {e.id for e in targets}
            if missing:
                raise ValueError(f"constraint '{c.id}' names elements the surface "
                                 f"does not hold: {', '.join(sorted(missing))}")
            for e in targets:
                for lang in sorted(metrics.get("text", {})):
                    text = _text_width(metrics, lang, e)
                    slack_lo, slack_hi = (a * lo + b) - text, (a * hi + b) - text
                    margin, at = min((slack_lo, lo), (slack_hi, hi))
                    out.append(LayoutVerdict(
                        constraint=c.id, lang=lang,
                        verdict="proved" if margin >= 0 else "refuted",
                        margin_px=round(margin, 1), at_width=at,
                        note=f"'{e.id}' ({lang}) vs {c.payload['container']}: "
                             f"{round(text, 1)}px against {round(a * at + b, 1)}px "
                             f"at {at}px viewport — container declared linear "
                             f"between measured endpoints"))
    return out
