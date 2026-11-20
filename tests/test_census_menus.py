"""The two censuses of the pages that say when a command that does not apply is shown unavailable
and when it is removed stay whole and honestly routed, and the four laws they root cite what the
censuses route to them."""

import pytest

from craft import census_apple_menus, census_ms_menus
from craft.laws import LAWS
from craft.practice import PRACTICE

COUNTS = [(census_ms_menus, 112), (census_apple_menus, 27)]


@pytest.mark.parametrize("census,count", COUNTS)
def test_the_census_is_whole(census, count):
    assert len(census.CENSUS) == census.SOURCE_COUNT == count


@pytest.mark.parametrize("census", [c for c, _ in COUNTS])
def test_routes_come_from_the_agreed_set_and_name_real_laws(census):
    ids = {l.id for l in LAWS} | {l.id for l in PRACTICE}
    for rule, (route, law, _) in census.CENSUS.items():
        assert route in census.ROUTES, rule
        assert (law in ids) if route == "covered" else law == "", rule


@pytest.mark.parametrize("law_id,census", [
    ("a-stable-menu-disables-what-does-not-apply", census_ms_menus),
    ("a-stable-menu-disables-what-does-not-apply", census_apple_menus),
    ("a-contextual-menu-lists-only-what-applies", census_ms_menus),
    ("a-menu-with-nothing-available-stays-openable", census_apple_menus),
    ("a-shortcut-or-context-menu-is-never-the-only-way-to-a-command", census_ms_menus),
])
def test_each_law_is_rooted_in_its_census(law_id, census):
    assert any(law == law_id for _, law, _ in census.CENSUS.values())
    law = next(l for l in LAWS if l.id == law_id)
    assert law.params["authority"].provenance == "cited"


def test_the_contextual_law_carries_the_two_exceptions_the_source_states():
    law = next(l for l in LAWS if l.id == "a-contextual-menu-lists-only-what-applies")
    quotes = [c.payload["quote"] for c in law.children if c.kind == "citation"]
    assert any(q.startswith("Always have the relevant standard") for q in quotes)
    assert any(q.startswith("Always have the commands that complete") for q in quotes)
