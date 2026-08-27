"""Walton's argumentation schemes as data, read from the committed capture.

THE ONE-FORMALISM DECISION (the owner's, 2026-08-27): schemes enter as DATA in one
uniform structure -- premises, exceptions (critical questions that defeat the
inference until answered), assumptions (critical questions whose burden sits with
the proponent), conclusion -- and every critical question flows through the SAME
defense mechanics the account already runs, instead of forty-one hand-written
deciders. Strict inference stays Z3; acceptability stays Dung; this module only
serves the catalogue.

The capture is docs/sources/walton-reed-macagno-2008-carneades.yml -- the Carneades
encoding of Walton, Reed & Macagno 2008 -- and this parser reads THAT file, so the
catalogue is the committed artifact and never a copy in code. census_walton.py pins
the expected counts; a drifted capture is a visible diff in two places.

A deliberately small parser for one fixed file. It is not a YAML implementation, and
it self-checks: parsing that loses a scheme or a slot fails the census's pinned
counts, which run in the test suite and in CI.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

CAPTURE = Path(__file__).resolve().parents[1] / "docs" / "sources" / \
    "walton-reed-macagno-2008-carneades.yml"

_SECTION = re.compile(r"^    (premises|exceptions|assumptions|conclusions|"
                      r"variables|meta):")
_ITEM = re.compile(r"^      - (.+?)\s*$")
_ID = re.compile(r"^  - id: (\S+)")
_LANG = re.compile(r"^  ([a-z_0-9]+)/(\d+): (.+)$")
_PRED = re.compile(r"^([a-z_0-9]+)")


def _predicate(expr: str) -> str:
    """The predicate name of a scheme slot: `expert(W,D)` -> `expert`."""
    m = _PRED.match(expr.strip())
    return m.group(1) if m else expr.strip()


@lru_cache(maxsize=1)
def catalogue() -> dict:
    """id -> {"premises": [...], "exceptions": [...], "assumptions": [...]},
    slot expressions verbatim from the capture."""
    schemes: dict[str, dict] = {}
    cur, sec = None, None
    for ln in CAPTURE.read_text(encoding="utf-8").splitlines():
        m = _ID.match(ln)
        if m:
            cur = m.group(1)
            schemes[cur] = {"premises": [], "exceptions": [], "assumptions": [],
                            "conclusions": []}
            sec = None
            continue
        if cur is None:
            continue
        m = _SECTION.match(ln)
        if m:
            sec = m.group(1)
            continue
        m = _ITEM.match(ln)
        if m and sec in ("premises", "exceptions", "assumptions", "conclusions"):
            schemes[cur][sec].append(m.group(1))
    return schemes


@lru_cache(maxsize=1)
def language() -> dict:
    """predicate -> the capture's own rendering of what the slot says."""
    out = {}
    in_lang = False
    for ln in CAPTURE.read_text(encoding="utf-8").splitlines():
        if ln.startswith("language:"):
            in_lang = True
            continue
        if in_lang and ln and not ln.startswith("  "):
            break
        m = _LANG.match(ln)
        if in_lang and m:
            out[m.group(1)] = m.group(3).strip().strip('"')
    return out


def slots(scheme_id: str) -> dict:
    """The scheme's slot predicates by kind, or None for an unknown scheme."""
    s = catalogue().get(scheme_id)
    if s is None:
        return None
    return {kind: [_predicate(x) for x in s[kind]]
            for kind in ("premises", "exceptions", "assumptions")}
