"""Apple's Writing census stays whole and honestly routed: every guideline of the page
present, every route from the agreed set, and every covered guideline naming a law that
exists."""

from craft import census_apple_writing as census
from craft.laws import LAWS
from craft.practice import PRACTICE


def test_the_census_is_whole():
    assert len(census.CENSUS) == census.SOURCE_COUNT == 16


def test_routes_come_from_the_agreed_set_and_name_real_laws():
    ids = {l.id for l in LAWS} | {l.id for l in PRACTICE}
    for guideline, (route, law, _) in census.CENSUS.items():
        assert route in census.ROUTES, guideline
        assert (law in ids) if route == "covered" else law == "", guideline
