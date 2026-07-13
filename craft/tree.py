"""The craft tree: craft@0.1.0's semantics, with the laws hanging under them."""

from __future__ import annotations

import os
from pathlib import Path

import bom.grounding  # noqa: F401 -- the natives; the packages themselves arrive by pin
from bom import Bom
from bom.library import consume

from .laws import GATE, LAWS

_ROOT = Path(__file__).resolve().parents[1]


def build() -> Bom:
    # The channel exists now (xag/bom#19) and these lines became the promised pin:
    # craft@0.1.0 is published to the registry like anything else, and this repo consumes
    # its own product by digest -- bom.lock, .bom/library, proof re-run at sync. `craft`
    # was always a Package; now it has somewhere to go. Refining the laws is a republish
    # under a new version and a repin, which is not friction: for a package of LAWS,
    # every change deliberate is the point.
    lib, refs = consume(_ROOT, os.environ.get("BOM_REGISTRY", _ROOT.parent / "bom-registry"))

    bom = Bom(packages=[r for r in refs if r.name in ("craft", "ledger")])
    bom = lib.effective(bom)
    bom.root.children = [*LAWS, GATE]
    return bom
