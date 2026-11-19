"""The two censuses behind the pane-divider laws stay whole and honestly routed: every rule
of each source present, every route from the agreed set, and every covered rule naming a law
that exists."""

import pytest

from craft import census_apg_splitter, census_apple_split_views
from craft.laws import LAWS
from craft.practice import PRACTICE


@pytest.mark.parametrize("census,count", [(census_apg_splitter, 17),
                                          (census_apple_split_views, 19)])
def test_the_census_is_whole(census, count):
    assert len(census.CENSUS) == census.SOURCE_COUNT == count


@pytest.mark.parametrize("census", [census_apg_splitter, census_apple_split_views])
def test_routes_come_from_the_agreed_set_and_name_real_laws(census):
    ids = {l.id for l in LAWS} | {l.id for l in PRACTICE}
    for rule, (route, law, _) in census.CENSUS.items():
        assert route in census.ROUTES, rule
        assert (law in ids) if route == "covered" else law == "", rule
