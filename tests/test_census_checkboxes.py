"""The two checkbox censuses stay whole and honestly routed: every guideline of each source
present, every route from the agreed set, and every covered guideline naming a law that
exists."""

import pytest

from craft import census_govuk_checkboxes, census_nng_checkboxes
from craft.laws import LAWS
from craft.practice import PRACTICE


@pytest.mark.parametrize("census,count", [(census_nng_checkboxes, 12),
                                          (census_govuk_checkboxes, 16)])
def test_the_census_is_whole(census, count):
    assert len(census.CENSUS) == census.SOURCE_COUNT == count


@pytest.mark.parametrize("census", [census_nng_checkboxes, census_govuk_checkboxes])
def test_routes_come_from_the_agreed_set_and_name_real_laws(census):
    ids = {l.id for l in LAWS} | {l.id for l in PRACTICE}
    for guideline, (route, law, _) in census.CENSUS.items():
        assert route in census.ROUTES, guideline
        assert (law in ids) if route == "covered" else law == "", guideline
