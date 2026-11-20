"""The thirteen censuses of the sources a review of a written design for listing a design's
flaws relied on stay whole and honestly routed: every rule of each source present, every route
from the agreed set, and every covered rule naming a law that exists. The four laws they root
cite what the censuses route to them."""

import pytest

from craft import (census_cati_interference, census_claude_prompting,
                   census_debugbear_lighthouse, census_github_autofix, census_govuk_radios,
                   census_grammarly_bulk_accept, census_grammarly_grouped, census_ms_checker,
                   census_ms_checker_rules, census_nng_accordions, census_nng_severity,
                   census_vscode_eslint, census_wcag_headings_labels)
from craft.laws import LAWS
from craft.practice import PRACTICE

COUNTS = [(census_cati_interference, 15), (census_claude_prompting, 71),
          (census_debugbear_lighthouse, 10), (census_github_autofix, 22),
          (census_govuk_radios, 21), (census_grammarly_bulk_accept, 11),
          (census_grammarly_grouped, 7), (census_ms_checker, 11),
          (census_ms_checker_rules, 19), (census_nng_accordions, 13),
          (census_nng_severity, 10), (census_vscode_eslint, 12),
          (census_wcag_headings_labels, 10)]


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
    ("a-problem-is-ranked-by-its-severity", census_nng_severity),
    ("headings-and-labels-describe-topic-or-purpose", census_wcag_headings_labels),
    ("content-most-people-need-is-not-folded-away", census_nng_accordions),
    ("radios-for-one-answer-checkboxes-for-several", census_govuk_radios),
])
def test_each_new_law_is_rooted_in_its_census(law_id, census):
    assert any(law == law_id for _, law, _ in census.CENSUS.values())
    law = next(l for l in LAWS if l.id == law_id)
    assert law.params["authority"].provenance == "cited"
