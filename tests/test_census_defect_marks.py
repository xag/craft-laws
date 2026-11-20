"""The fifteen censuses of the sources a design review of marks on improvable places gathered
stay whole and honestly routed: every rule of each source present, every route from the agreed
set, and every covered rule naming a law that exists."""

import pytest

from craft import (census_gdocs_comments, census_govuk_warning_text, census_inal,
                   census_m1_dialogs, census_material_badge, census_mdn_closewatcher,
                   census_ms_spelling, census_nng_icons, census_nng_indicators,
                   census_nng_modal, census_primer_dialog, census_proofreading_marks,
                   census_vscode_navigation, census_wave_help, census_wicg_close_watcher)
from craft.laws import LAWS
from craft.practice import PRACTICE

COUNTS = [(census_nng_indicators, 24), (census_nng_icons, 18), (census_nng_modal, 20),
          (census_primer_dialog, 26), (census_m1_dialogs, 62), (census_mdn_closewatcher, 11),
          (census_wicg_close_watcher, 27), (census_material_badge, 13),
          (census_govuk_warning_text, 5), (census_proofreading_marks, 48), (census_inal, 10),
          (census_vscode_navigation, 25), (census_ms_spelling, 17),
          (census_gdocs_comments, 32), (census_wave_help, 18)]


@pytest.mark.parametrize("census,count", COUNTS)
def test_the_census_is_whole(census, count):
    assert len(census.CENSUS) == census.SOURCE_COUNT == count


@pytest.mark.parametrize("census", [c for c, _ in COUNTS])
def test_routes_come_from_the_agreed_set_and_name_real_laws(census):
    ids = {l.id for l in LAWS} | {l.id for l in PRACTICE}
    for rule, (route, law, _) in census.CENSUS.items():
        assert route in census.ROUTES, rule
        assert (law in ids) if route == "covered" else law == "", rule
