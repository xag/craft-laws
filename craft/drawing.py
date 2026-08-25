"""Prose is checked through its drawing: derived structure as data, validated by code.

The division of labour, decided 2026-08-23 for the estate's prose program and applied
here to the claim lane: a MODEL OF THE PROSE is built as data by whoever authors or
audits the prose (an agent, at derivation time), and every check runs in code over
that data. The derivation can be wrong; the checks cannot. What makes the derivation
trustworthy is not the deriver but the artifact: it is committed next to its source,
pinned to the source text by hash (line endings normalized, nothing else), and every node in it must quote its
sentence verbatim - so a wrong derivation is refutable by reading, and a stale or
fabricated one is refuted by code.

The drawing for a prose file F is F + ".drawing.json":

    {"source": "README.md",
     "sha256": "<source_hash of the text at derivation time>",
     "nodes": [
       {"kind": "measurement", "quote": "<verbatim sentence from the source>",
        "claim": 12},                          # 1-based line in the repo's claims.jsonl
       {"kind": "done", "quote": "...", "unfiled": "<why no claim is filed>"}]}

Every check below is deterministic over this data and the files it names:

  stale       - the source no longer hashes to sha256: the prose was edited
                without re-deriving, so nothing the drawing says is current.
  unanchored  - a node's quote is not a substring of the source (whitespace runs
                collapsed on both sides first, which is a defined canonical form,
                not a similarity measure): the drawing asserts a sentence the
                prose does not contain.
  unknown kind - a node's kind is not one of the claim kinds the deciders know.
  unresolved  - a node's claim reference names no line, or a line that does not
                parse, in the repo's claims.jsonl.
  kind mismatch - the referenced claim's kind differs from the node's.
  unfiled     - the drawing says a sentence asserts a claim and no claim is filed:
                the remedy is to file the claim, reword the prose, or correct the
                drawing - each a recorded, refutable act.

There is no word list and no pattern matching anywhere in this module: the sentences
a drawing covers were chosen by its deriver, and the checks only hold the drawing to
the source, the record, and itself. A derivation that under-reports is measured the
way any reporting bias is measured here - by a later audit against the same source -
not guessed at by code.

    python -m craft.drawing <prose-file> [<prose-file>...]
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from .claims import CLAIM_KINDS


@dataclass
class DrawingFinding:
    check: str
    where: str
    why: str


def _canon(text: str) -> str:
    return " ".join(text.split())


def source_hash(text: str) -> str:
    """sha256 of the source with line endings normalized to \\n.

    The hash pins content, and the same committed content materializes with
    different line endings across platforms (observed 2026-08-25: a git checkout
    on Windows restored a file to different bytes than the drawing was derived
    from). Normalizing the one representational difference keeps the check exact
    while making it about the text, not the platform."""
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def check_drawing(prose: Path, drawing: Path | None = None) -> list[DrawingFinding]:
    """Every conviction the drawing for `prose` earns. Deterministic throughout."""
    drawing = drawing or prose.with_name(prose.name + ".drawing.json")
    if not drawing.exists():
        return [DrawingFinding("missing", str(drawing),
                               "the prose has no drawing; derive one or exempt the "
                               "file from the drawing gate")]
    try:
        data = json.loads(drawing.read_text(encoding="utf-8"))
    except ValueError as e:
        return [DrawingFinding("unreadable", str(drawing), f"not JSON: {e}")]

    findings: list[DrawingFinding] = []
    source_text = prose.read_bytes().decode("utf-8", "replace")
    stated = str(data.get("sha256") or "")
    actual = source_hash(source_text)
    if stated != actual:
        findings.append(DrawingFinding(
            "stale", str(drawing),
            f"the source hashes to {actual[:12]}..., the drawing was derived from "
            f"{stated[:12] or '(none)'}...; the prose changed without re-derivation"))

    text = _canon(source_text)
    claims_file = prose.parent / "claims.jsonl"
    claim_lines = (claims_file.read_text(encoding="utf-8").splitlines()
                   if claims_file.exists() else [])

    for i, node in enumerate(data.get("nodes") or []):
        where = f"{drawing.name}#nodes[{i}]"
        kind = node.get("kind")
        quote = str(node.get("quote") or "")
        if kind not in CLAIM_KINDS:
            findings.append(DrawingFinding(
                "unknown-kind", where, f"kind {kind!r} is not a claim kind"))
        if not quote or _canon(quote) not in text:
            findings.append(DrawingFinding(
                "unanchored", where,
                f"the quote is not in the source verbatim: {quote[:80]!r}"))
        ref = node.get("claim")
        if ref is not None:
            line = (claim_lines[ref - 1]
                    if isinstance(ref, int) and 1 <= ref <= len(claim_lines) else None)
            try:
                filed = json.loads(line) if line else None
            except ValueError:
                filed = None
            if filed is None:
                findings.append(DrawingFinding(
                    "unresolved", where,
                    f"claim reference {ref!r} names no parseable line in "
                    f"{claims_file.name}"))
            elif filed.get("kind") != kind:
                findings.append(DrawingFinding(
                    "kind-mismatch", where,
                    f"the drawing says {kind}, line {ref} of {claims_file.name} "
                    f"says {filed.get('kind')}"))
            elif kind == "measurement":
                # the register's computable core (quality-harness:
                # the-reports-register-is-unchecked): a sentence presenting a
                # measured figure presents the whole cross-tab, not the
                # favourable cell - checked as a data join against the record,
                # never by reading the prose for numbers
                for cell in ("caught", "false_alarms"):
                    value = filed.get(cell)
                    if isinstance(value, (int, float)) and str(value) not in quote:
                        findings.append(DrawingFinding(
                            "half-the-cross-tab", where,
                            f"the quoted sentence omits {cell}={value} from the "
                            f"measurement it presents (line {ref}); a figure "
                            "travels with its unfavourable cell or not at all"))
        elif "unfiled" in node:
            findings.append(DrawingFinding(
                "unfiled", where,
                f"the drawing marks a {kind}-assertion with no filed claim "
                f"({node['unfiled']}): file it, reword the prose, or correct the "
                "drawing - quote: " + quote[:80]))
        else:
            findings.append(DrawingFinding(
                "unjoined", where,
                "the node neither references a filed claim nor says why none is "
                "filed; a drawing states the join explicitly either way"))
    return findings


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print(__doc__.splitlines()[0])
        print("usage: python -m craft.drawing <prose-file> [<prose-file>...]")
        return 2
    bad = 0
    for name in args:
        for f in check_drawing(Path(name)):
            bad += 1
            print(f"{f.check:12} {f.where}")
            print(f"             {f.why}")
    if not bad:
        print(f"{len(args)} drawing(s): every check passes.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
