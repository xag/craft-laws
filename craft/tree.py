"""The craft tree: craft@0.1.0's semantics, with the laws hanging under them."""

from __future__ import annotations

import tempfile
from pathlib import Path

from bom import Bom, Library
from bom.grounding import GROUNDING_PACKAGE
from bom.ledger import LEDGER_PACKAGE

from .laws import GATE, LAWS
from .package import CRAFT_PACKAGE


def build() -> Bom:
    # No package channel exists yet (xag/bom#19), so a package reaches a consumer by exactly two
    # routes: code inside bom's source, or copy-paste. `craft` takes neither — it publishes
    # itself into its own Library at load, which is the third route #19 will make ordinary and
    # which works today only because bom lets a project's own vocabulary stand alongside a
    # package's.
    #
    # When #19 lands, these three lines become a pin against a registry and nothing else here
    # changes: `craft` was always a Package, merely one with nowhere to go.
    lib = Library(Path(tempfile.mkdtemp(prefix="craft-lib-")))
    lib.publish(GROUNDING_PACKAGE, {})
    lib.publish(LEDGER_PACKAGE, {})
    lib.publish(CRAFT_PACKAGE, {})

    bom = Bom(packages=[
        {"name": "craft", "version": CRAFT_PACKAGE.version},
        {"name": "ledger", "version": LEDGER_PACKAGE.version},
    ])
    bom = lib.effective(bom)
    bom.root.children = [*LAWS, GATE]
    return bom
