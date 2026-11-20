"""The eight censuses of the sources the second review of a written design for listing a
design's flaws relied on stay whole and honestly routed, and the six laws they root cite what
the censuses route to them."""

import pytest

from craft import (census_apg_accordion, census_apple_pull_down_buttons, census_govuk_button,
                   census_govuk_details, census_nng_accordion_icons, census_nng_flat_ui,
                   census_wcag_label_in_name, census_whatwg_button)
from craft.laws import LAWS
from craft.practice import PRACTICE

COUNTS = [(census_apg_accordion, 14), (census_apple_pull_down_buttons, 9),
          (census_govuk_button, 19), (census_govuk_details, 5),
          (census_nng_accordion_icons, 6), (census_nng_flat_ui, 7),
          (census_wcag_label_in_name, 18), (census_whatwg_button, 7)]


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
    ("one-main-call-to-action-per-page", census_govuk_button),
    ("a-control-looks-clickable", census_nng_flat_ui),
    ("a-button-holds-only-phrasing-content", census_whatwg_button),
    ("an-accordion-header-is-a-button-alone-inside-a-heading", census_apg_accordion),
    ("content-that-opens-in-place-is-marked-with-a-caret", census_nng_accordion_icons),
    ("the-accessible-name-contains-the-visible-label", census_wcag_label_in_name),
    ("content-most-people-need-is-not-folded-away", census_govuk_details),
])
def test_each_law_is_rooted_in_its_census(law_id, census):
    assert any(law == law_id for _, law, _ in census.CENSUS.values())
    law = next(l for l in LAWS if l.id == law_id)
    assert law.params["authority"].provenance == "cited"
