"""No rule enters by hand: every id a decider convicts under resolves to a registered
law, every account law carries a fetched citation, and every source is adopted whole.

This is the checkable half of the source-a-law skill, and it is the gate the owner
asked for on 2026-08-27: CI goes red on an ad-hoc rule, on a registered law without a
citation, on a cherry-picked catalogue row, and on a decider claiming a row the census
says needs a reader.
"""

import ast
from pathlib import Path

from craft import account_laws, census_argument, census_sophistici, laws, practice

CRAFT = Path(__file__).resolve().parents[1] / "craft"


def _decider_law_ids() -> dict[str, set]:
    """Every string literal passed as the law argument to Finding(...) or _law(...),
    per module, read from the source so nothing can convict off the record."""
    out: dict[str, set] = {}
    for py in sorted(CRAFT.glob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        ids = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if name in ("Finding", "ClaimFinding", "DocFinding") and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    ids.add(first.value)
            if name == "_law" and len(node.args) == 1 and not node.keywords:
                # the one-argument form is the resolver a decider convicts through;
                # the many-argument form is laws.py's constructor (and the synthetic
                # fixtures in alarms), which registers rather than convicts
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    ids.add(first.value)
        if ids:
            out[py.name] = ids
    return out


def _registry() -> set:
    ids = {law.id for law in laws.LAWS}
    ids |= {law.id for law in practice.PRACTICE}
    ids |= {law.id for law in account_laws.ACCOUNT}
    return ids


def test_every_decider_convicts_under_a_registered_law():
    """An id no registry carries is a rule added by hand, and it fails CI here."""
    registry = _registry()
    strays = {f"{mod}: {law}"
              for mod, ids in _decider_law_ids().items()
              for law in ids if law not in registry}
    assert not strays, ("deciders convict under unregistered law id(s) -- a rule "
                        f"added by hand: {sorted(strays)}")


def test_every_account_law_is_cited_with_a_fetched_quote():
    """A registered account law with no citation, or a citation with an empty source,
    url or quote, is an assertion wearing a law's shape."""
    bad = []
    for law in account_laws.ACCOUNT:
        if not law.citations:
            bad.append(f"{law.id}: no citation")
            continue
        for src, url, quote in law.citations:
            if not (str(src).strip() and str(url).strip() and str(quote).strip()):
                bad.append(f"{law.id}: a citation with an empty field")
        if not str(law.source_item).strip():
            bad.append(f"{law.id}: no source_item")
    assert not bad, bad


def test_no_source_is_adopted_in_isolation():
    """The Greenwell taxonomy is adopted whole: the census must hold all 33 rows,
    every Greenwell-rooted decider must claim a real row, and no decider may claim a
    row the census routes to a reader or to missing vocabulary."""
    census = census_argument.CENSUS
    assert len(census) == 33, "the census no longer covers the whole taxonomy"
    decidable = {"zero", "covered"}
    for law_id, row in account_laws.GREENWELL_ROWS.items():
        assert row in census, f"{law_id} claims a row the census does not hold: {row}"
        route = census[row][0] if isinstance(census[row], (list, tuple)) else census[row]
        assert str(route) in decidable, (
            f"{law_id} mechanizes {row!r}, which the census routes {route!r} -- "
            "a decider on a row that needs a reader")


def test_the_second_source_is_adopted_whole_too():
    """Sophistical Refutations: the author states a complete enumeration of 13; the
    census holds them all, and every SR-rooted decider claims a decidable row."""
    census = census_sophistici.CENSUS
    assert len(census) == census_sophistici.SOURCE_COUNT == 13
    for law_id, row in account_laws.SOPHISTICI_ROWS.items():
        assert row in census, f"{law_id} claims a row the census does not hold"
        assert census[row][0] in ("zero", "covered"), (
            f"{law_id} mechanizes {row!r}, routed {census[row][0]!r}")


def test_the_practice_reuse_is_real():
    """The account deciders convict under two practice-family ids; both must exist
    there, cited -- one law, one home, and a rename there goes red here."""
    by_id = {law.id: law for law in practice.PRACTICE}
    for law_id in account_laws.PRACTICE_REUSED:
        assert law_id in by_id, f"{law_id} is not a practice law any more"
        authority = by_id[law_id].params.get("authority")
        assert authority is not None and authority.provenance == "cited", (
            f"{law_id} carries no cited authority")


def test_every_account_law_is_used_by_a_decider():
    """A registered law nothing convicts under is registry padding; it goes red so
    the registry stays the deciders' exact contract."""
    used = set().union(*_decider_law_ids().values())
    dead = {law.id for law in account_laws.ACCOUNT} - used
    assert not dead, f"registered account law(s) no decider uses: {sorted(dead)}"


def test_the_captured_source_is_in_the_repo():
    """The whole-source adoption includes keeping the source: the cited capture path
    must exist, so the quotes stay checkable offline."""
    pdf = Path(__file__).resolve().parents[1] / "docs" / "sources" / \
        "greenwell-knight-holloway-pease-2006.pdf"
    assert pdf.exists() and pdf.stat().st_size > 10_000
