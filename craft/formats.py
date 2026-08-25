"""The format gate: a kind used in a committed record resolves to a published KindDef.

Root: quality-harness's debt a-shape-ships-before-its-meaning. Twice a record format
lived only in code while the published vocabulary saw nothing - the claim kinds for a
week, the drawing shape for a day - and the convergence series, whose one job is
seeing vocabulary grow, read zero both times. Both catches were the owner asking. The
discharge route on that debt: a committed record file implies a pinned package naming
its format, checkable from the lock - a walk of the pin chain, not a sweep of source
code.

This is that walk. Everything it reads is committed data:

  the record files    - claims.jsonl, and every *.drawing.json (enumerated, with the
                        usual non-source directories pruned)
  the declaration     - .craft/formats.json maps each record shape to the package
                        that publishes its meaning: {"claims.jsonl": "claims",
                        ".drawing.json": "claims"}
  the lock            - quern.lock names the pinned version
  the package's bytes - .quern/library/packages/<name>/<version>.json, committed
                        beside the lock, carrying the vocabulary as KindDefs

The convictions, each deterministic:

  undeclared        - a record file no declaration entry covers: a format nobody
                      claimed to have published.
  unpinned          - the declared package is not in quern.lock.
  unfetchable       - the pinned version's bytes are not in the committed cache, so
                      no fresh checkout could know what the records mean.
  unpublished-kind  - a `kind` used in the record that the pinned package's
                      vocabulary does not define. This is the debt's own history made
                      red: a kind invented in code and used in records would have
                      convicted here on its first appearance, both times.

WHAT THIS DOES NOT CLAIM: that the published description is faithful to what the
checking code does - that join is per-shape and lives in tests that read the code's
source (test_claims_package binds the claim kinds and the drawing fields). This gate
is the floor under those: the meaning exists, is pinned, and covers every kind in use.

    python -m craft.formats <repo-root>
    python -m craft.formats --alarm
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

_PRUNE = {".git", ".venv", "node_modules", "__pycache__", ".quern", ".craft", "dist"}


@dataclass
class FormatFinding:
    check: str
    where: str
    why: str


def record_files(root: Path) -> list[Path]:
    out: list[Path] = []

    def walk(d: Path):
        for p in sorted(d.iterdir()):
            if p.is_dir():
                if p.name not in _PRUNE:
                    walk(p)
            elif p.name == "claims.jsonl" or p.name.endswith(".drawing.json"):
                out.append(p)

    walk(root)
    return out


def kinds_used(path: Path) -> set[str]:
    """The kind values a record file actually uses - claims per line, or a drawing's
    nodes. Unreadable content contributes nothing here; shape validity is the claim
    deciders' and the drawing checks' job, not this gate's."""
    kinds: set[str] = set()
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.name.endswith(".drawing.json"):
        try:
            for node in (json.loads(text).get("nodes") or []):
                if isinstance(node, dict) and node.get("kind"):
                    kinds.add(str(node["kind"]))
        except ValueError:
            pass
        return kinds
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if isinstance(rec, dict) and rec.get("kind"):
            kinds.add(str(rec["kind"]))
    return kinds


def _declared_package(name: str, declaration: dict) -> str | None:
    if name in declaration:
        return declaration[name]
    for suffix, package in declaration.items():
        if suffix.startswith(".") and name.endswith(suffix):
            return package
    return None


def check_repo(root: Path) -> list[FormatFinding] | None:
    """None when the repo has not adopted the gate (.craft/formats.json absent)."""
    decl_path = root / ".craft" / "formats.json"
    if not decl_path.exists():
        return None
    declaration = json.loads(decl_path.read_text(encoding="utf-8"))
    lock_path = root / "quern.lock"
    pins = {p["name"]: p["version"]
            for p in (json.loads(lock_path.read_text(encoding="utf-8"))["packages"]
                      if lock_path.exists() else [])}
    findings: list[FormatFinding] = []
    vocab_cache: dict[str, set[str] | None] = {}

    def vocabulary(package: str) -> set[str] | None:
        if package not in vocab_cache:
            version = pins.get(package)
            bytes_path = (root / ".quern" / "library" / "packages" / package
                          / f"{version}.json") if version else None
            if bytes_path and bytes_path.exists():
                data = json.loads(bytes_path.read_text(encoding="utf-8"))
                vocab_cache[package] = {v["kind"] for v in data.get("vocabulary", [])}
            else:
                vocab_cache[package] = None
        return vocab_cache[package]

    for record in record_files(root):
        where = str(record.relative_to(root))
        package = _declared_package(record.name, declaration)
        if package is None:
            findings.append(FormatFinding(
                "undeclared", where,
                "no entry in .craft/formats.json covers this record file; declare "
                "which package publishes its meaning"))
            continue
        if package not in pins:
            findings.append(FormatFinding(
                "unpinned", where,
                f"the declaration names {package!r} and quern.lock does not pin it"))
            continue
        vocab = vocabulary(package)
        if vocab is None:
            findings.append(FormatFinding(
                "unfetchable", where,
                f"{package}@{pins[package]} is pinned and its bytes are not in "
                ".quern/library; a fresh checkout cannot know what these records "
                "mean"))
            continue
        for kind in sorted(kinds_used(record) - vocab):
            findings.append(FormatFinding(
                "unpublished-kind", where,
                f"the record uses kind {kind!r} and {package}@{pins[package]} does "
                "not define it - vocabulary living outside the publish, which is "
                "the exact history this gate exists to make red"))
    return findings


def _alarm() -> int:
    """The gate against a synthetic repo that must convict four ways, and this real
    repo, which must pass."""
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".craft").mkdir()
        (root / ".craft" / "formats.json").write_text(
            json.dumps({"claims.jsonl": "claims", ".drawing.json": "claims"}), encoding="utf-8")
        (root / "claims.jsonl").write_text(
            '{"kind": "done", "text": "t"}\n{"kind": "vibe", "text": "t"}\n',
            encoding="utf-8")
        (root / "doc.md.drawing.json").write_text(
            json.dumps({"nodes": [{"kind": "hunch", "quote": "q"}]}),
            encoding="utf-8")
        (root / "quern.lock").write_text(
            json.dumps({"packages": [{"name": "claims", "version": "9.9.9",
                                      "sha256": "0" * 64}]}), encoding="utf-8")
        found = check_repo(root) or []
        checks = sorted(f.check for f in found)
        if checks != ["unfetchable", "unfetchable"]:
            bad += 1
            print(f"ALARM expected two unfetchable, got {checks}")
        lib = root / ".quern" / "library" / "packages" / "claims"
        lib.mkdir(parents=True)
        (lib / "9.9.9.json").write_text(
            json.dumps({"vocabulary": [{"kind": "done"}]}), encoding="utf-8")
        checks = sorted(f.check for f in (check_repo(root) or []))
        if checks != ["unpublished-kind", "unpublished-kind"]:
            bad += 1
            print(f"ALARM expected two unpublished-kind, got {checks}")
        (root / "quern.lock").write_text(json.dumps({"packages": []}),
                                         encoding="utf-8")
        checks = {f.check for f in (check_repo(root) or [])}
        if checks != {"unpinned"}:
            bad += 1
            print(f"ALARM expected unpinned, got {checks}")
        (root / ".craft" / "formats.json").write_text(json.dumps({}),
                                                      encoding="utf-8")
        checks = {f.check for f in (check_repo(root) or [])}
        if checks != {"undeclared"}:
            bad += 1
            print(f"ALARM expected undeclared, got {checks}")
    here = Path(__file__).resolve().parents[1]
    real = check_repo(here)
    if real is None:
        bad += 1
        print("ALARM this repo has not adopted the gate")
    elif real:
        bad += 1
        for f in real:
            print(f"ALARM this repo convicts: {f.check} {f.where} - {f.why}")
    if not bad:
        print("alarm: four synthetic convictions fired, the real repo passes.")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args == ["--alarm"]:
        return _alarm()
    if not args:
        print(__doc__.splitlines()[0])
        print("usage: python -m craft.formats <repo-root> | --alarm")
        return 2
    bad = 0
    for name in args:
        found = check_repo(Path(name))
        if found is None:
            print(f"{name}: no .craft/formats.json - the gate is opt-in.")
            continue
        for f in found:
            bad += 1
            print(f"{f.check:17} {f.where}")
            print(f"                  {f.why}")
    if not bad:
        print(f"{len(args)} repo(s): every kind in every record resolves to a "
              "pinned, published KindDef.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
