"""The two error-taxonomy censuses stay whole and honestly routed.

Same discipline as the other censuses: every row of the source present, every route
a word from the agreed set, and the captured source on disk beside the claim that it
was read. A census that drops rows is the cherry-picking these files exist to refuse.
"""

from pathlib import Path

from craft import census_croskerry, census_mast

DOCS = Path(__file__).resolve().parents[1] / "docs" / "sources"


def test_croskerry_census_is_whole():
    assert len(census_croskerry.CENSUS) == census_croskerry.SOURCE_ROWS == 32


def test_mast_census_is_whole():
    assert len(census_mast.CENSUS) == census_mast.SOURCE_ROWS == 14


def test_routes_come_from_the_agreed_set():
    for census in (census_croskerry, census_mast):
        for item, (route, quote, means) in census.CENSUS.items():
            assert route in census.ROUTES, f"{item}: unknown route {route!r}"
            assert quote.strip(), f"{item}: a row with no words from the source"
            assert means.strip(), f"{item}: a row with no reading for the work"


def test_the_captured_sources_exist():
    assert (DOCS / "croskerry-2003-cognitive-errors.pdf").stat().st_size > 10_000
    assert (DOCS / "cemri-2025-mast.pdf").stat().st_size > 100_000


def test_the_clis_run_clean():
    assert census_croskerry.main([]) == 0
    assert census_mast.main([]) == 0
    assert census_croskerry.main(["--owed"]) == 0
    assert census_mast.main(["--owed"]) == 0
