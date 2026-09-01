# -*- coding: utf-8 -*-
"""The reply reviews as one registry: what runs, what is off, and what the tray shows."""

import json

import pytest

from craft import review


@pytest.fixture(autouse=True)
def _switches(tmp_path, monkeypatch):
    """Per-review switches in a temp home — a suite that flips the machine's real ones
    would leave the user's reviews off after a green run."""
    monkeypatch.setattr(review, "_home", lambda: tmp_path / "craft")
    monkeypatch.setattr("craft.account_hook.off", lambda: False)


def test_every_review_names_what_it_looks_at_and_what_it_costs():
    """The registry exists to answer 'what is checking my replies' in one place. A review
    that cannot say what it reads, or what it costs to run, cannot be chosen against."""
    assert {r.id for r in review.REVIEWS} == {"record", "reasoning"}
    for r in review.REVIEWS:
        assert r.what.strip() and r.cost.strip()


def test_a_review_is_switched_on_its_own():
    review.BY_ID["reasoning"].set(False)
    assert review.state()["on"] == ["record"]
    assert review.state()["off"] == ["reasoning"]
    assert review.state()["colour"] == "amber", "some on, some off is the middle state"
    review.BY_ID["reasoning"].set(True)
    assert review.state()["colour"] == "green"


def test_the_master_switch_still_silences_everything():
    """One file has always meant 'no checking at all'; the per-review switches are a
    refinement under it, never a way around it."""
    with pytest.MonkeyPatch.context() as m:
        m.setattr("craft.account_hook.off", lambda: True)
        assert review.state()["on"] == []
        assert review.state()["colour"] == "grey"


def test_the_switch_reaches_a_session_already_running():
    """Read at every turn, not at startup: a file, not a setting. That is what makes it
    a switch — the account lane learned it, and the reviews inherit it."""
    r = review.BY_ID["record"]
    r.set(False)
    assert not r.on and r.off_path().exists()
    r.set(True)
    assert r.on and not r.off_path().exists()


def test_a_turn_with_nothing_to_review_does_nothing(tmp_path):
    assert review.run({"session_id": "s"}) == 0
    assert review.run({"transcript_path": str(tmp_path / "t.jsonl"),
                       "stop_hook_active": True}) == 0


def test_only_the_enabled_reviews_run(tmp_path, monkeypatch):
    """The point of the registry: switching one off must actually stop it, not merely
    stop reporting it."""
    ran = []
    monkeypatch.setattr("craft.claims_hook.run",
                        lambda p: ran.append(("record", tuple(p.get("_reviews") or ()))))
    monkeypatch.setattr("craft.account_hook.spawn_critic",
                        lambda s, t: ran.append(("reasoning", ())))
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    payload = {"session_id": "s", "transcript_path": str(t)}

    review.run(payload)
    assert [k for k, _ in ran] == ["record", "reasoning"]

    ran.clear()
    review.BY_ID["reasoning"].set(False)
    review.run(payload)
    assert [k for k, _ in ran] == ["record"], "the reasoning review still ran when off"

    ran.clear()
    review.BY_ID["record"].set(False)
    review.run(payload)
    assert ran == [], "everything is off and something still ran"


def test_the_record_review_judges_both_what_was_written_and_what_was_not(tmp_path,
                                                                          monkeypatch):
    """The claim deciders and the silence note are one review: a conviction rate over
    self-filed records means nothing without the filing rate beside it (PRISMA 2020
    items 14 and 21, via a-corpus-of-reports-carries-its-reporting-bias). They were
    briefly switchable apart, which nobody wanted."""
    from craft import claims_hook
    t = tmp_path / "t.jsonl"
    t.write_text(json.dumps({"type": "assistant", "message": {"content": []}}),
                 encoding="utf-8")
    seen = {}

    def _silent(_path):
        seen["silent"] = True
        return []

    monkeypatch.setattr(claims_hook, "silent_repos", _silent)
    monkeypatch.setattr(claims_hook, "touched", lambda p: [])
    claims_hook.run({"transcript_path": str(t), "session_id": "s"})
    assert seen.get("silent"), "the record review skipped its own silence half"


class TestTheTray:
    """The icon is a face on the registry. It owns no state and shows three states."""

    def test_it_shows_a_state_for_every_shape_of_the_registry(self):
        tray = pytest.importorskip("craft.review_tray")
        for r in review.REVIEWS:
            r.set(True)
        assert review.state()["colour"] == "green"
        review.BY_ID["reasoning"].set(False)
        assert review.state()["colour"] == "amber"
        for r in review.REVIEWS:
            r.set(False)
        assert review.state()["colour"] == "grey"
        for name in ("green", "amber", "grey"):
            assert tray.image(name).mode == "RGBA"

    def test_the_menu_carries_one_checkbox_per_review(self):
        """One item per review, each labelled with its id FIRST — matched on the label's
        prefix, not by searching the sentence: an earlier version grepped for a word that
        also appears in another review's description, so it passed by coincidence."""
        tray = pytest.importorskip("craft.review_tray")
        items = list(tray.menu())
        by_id = {r.id: [i for i in items if str(i.text).startswith(r.id + ":")]
                 for r in review.REVIEWS}
        assert all(len(v) == 1 for v in by_id.values()), by_id
        for r in review.REVIEWS:
            r.set(True)
        assert all(v[0].checked for v in by_id.values())
        review.BY_ID["record"].set(False)
        assert not by_id["record"][0].checked
        assert by_id["reasoning"][0].checked, "switching one review off unchecked another"

    def test_a_left_click_does_something(self):
        """On Windows a left-click invokes the menu's DEFAULT item and nothing else. With
        no default the icon does not answer a click at all, which is what a user calls a
        broken tray icon — this replacement shipped that way once."""
        tray = pytest.importorskip("craft.review_tray")
        items = list(tray.menu())
        defaults = [i for i in items if i.default]
        assert len(defaults) == 1, "exactly one default action, or a click does nothing"

        for r in review.REVIEWS:
            r.set(True)
        assert "off" in str(defaults[0].text).lower(), "it should offer to turn them off"
        tray._flip_all(None)
        assert review.state()["on"] == [], "a click with everything on turned nothing off"

        items = list(tray.menu())
        assert "on" in str([i for i in items if i.default][0].text).lower()
        tray._flip_all(None)
        assert len(review.state()["on"]) == len(review.REVIEWS)

    def test_the_tooltip_never_exceeds_what_the_shell_will_show(self):
        tray = pytest.importorskip("craft.review_tray")
        for r in review.REVIEWS:
            r.set(True)
        assert len(tray.title(review.state())) <= 127
        review.BY_ID["record"].set(False)
        assert len(tray.title(review.state())) <= 127
