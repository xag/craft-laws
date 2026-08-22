"""The Stop hook is OFF for written answers, and that is a finding rather than a retreat.

Every law whose trigger fires for an answer to a person — done-is-observed,
a-qualifier-is-licensed, a-remainder-names-its-debt, and the rest of the practice family —
is about what a CLAIM may assert. Not one of them is countable. The countable laws in this
package belong to other surfaces: interface copy, or documentation read long after it was
written, and their triggers say so.

An earlier version ran the countable ones on answers anyway, chosen by whether the law was
"about words". It reported every sentence over twenty-five words — a GOV.UK guideline for
public service copy, whose own trigger is "the app's voice does work of its own (dry, terse,
no explaining text)" — and answers came back chopped into fragments to satisfy a counter
never addressed to them.

Judging the laws that do apply costs one to three minutes per answer, which cannot sit in
front of a person waiting. So nothing runs inline, and `python -m craft.answer` runs the
reader on demand.

This module stays as the entry point for the day a fast path exists — a local model, an API
call, a law whose falsifier turns out countable. It records nothing and says nothing today.
"""

from __future__ import annotations

import sys


def main() -> int:
    """Silent by design: see the module docstring. Exit 0, always."""
    return 0


if __name__ == "__main__":
    sys.exit(main())
