"""Run the laws' own rules. `uv run python -m craft.check`

Exit 1 while any rule is red, so this is a CI gate.

It is red today, on purpose and by design: three of the twelve laws cite nobody. That is the
honest state of the file, and the only reason it is *visible* is that it is data. As prose — and
it was prose, in a markdown file, four hours ago — the same fact sat in a sentence that was
perfectly true and could not fire.
"""

from __future__ import annotations

import sys

from quern import get_node, run_rules

from .tree import build


def main() -> int:
    quern = build()
    results = run_rules(quern)
    red = [r for r in results if not r.ok]

    # ASCII only: this prints to a Windows console under cp1252, which mangles anything prettier
    # and turns a clear report into mojibake exactly when it matters.
    for r in sorted(results, key=lambda r: (r.ok, r.rule, r.node)):
        mark = "ok  " if r.ok else "RED "
        at = f" @ {r.node}" if r.node else ""
        detail = f" - {r.detail}" if r.detail else ""
        print(f"{mark}{r.rule}{at}{detail}")

    print()
    if not red:
        print(f"{len(results)} rule(s), all green.")
        return 0
    print(f"{len(red)} of {len(results)} rule(s) RED.")
    print()
    for r in red:
        node = get_node(quern, r.node) if r.node else None
        why = (node.payload.get("note") if node else None) or r.detail or ""
        print(f"  {r.node or r.rule}: {why}")
    print()
    print("A law with no citation is a hypothesis. Find the source, or delete the law.")
    print("Never by editing the ledger.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
