# -*- coding: utf-8 -*-
"""The one Stop entry point for every review of a reply.

Two hook entries became one on 2026-09-01: `craft.account_hook` and `craft.claims_hook`
were separate wirings for what a user experiences as one thing — the checks on their
agent's answers. Which of them run is `craft.review`'s question, answered per review and
switchable from the tray. This module is the doorway and nothing else.
"""

from __future__ import annotations

import sys

from craft.review import hook_main

if __name__ == "__main__":
    raise SystemExit(hook_main())
