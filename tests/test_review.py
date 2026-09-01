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
    assert {r.id for r in review.REVIEWS} == {"claims", "argument", "intake"}
    for r in review.REVIEWS:
        assert r.what.strip() and r.cost.strip()


def test_a_review_is_switched_on_its_own():
    review.BY_ID["argument"].set(False)
    assert review.state()["on"] == ["claims", "intake"]
    assert review.state()["off"] == ["argument"]
    assert review.state()["colour"] == "amber", "some on, some off is the middle state"
    review.BY_ID["argument"].set(True)
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
    r = review.BY_ID["claims"]
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
                        lambda p: ran.append(("claims", tuple(p.get("_reviews") or ()))))
    monkeypatch.setattr("craft.account_hook.spawn_critic",
                        lambda s, t: ran.append(("argument", ())))
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    payload = {"session_id": "s", "transcript_path": str(t)}

    review.run(payload)
    assert [k for k, _ in ran] == ["claims", "argument"]
    assert ran[0][1] == ("claims", "intake")

    ran.clear()
    review.BY_ID["argument"].set(False)
    review.run(payload)
    assert [k for k, _ in ran] == ["claims"], "the argument review still ran when off"

    ran.clear()
    review.BY_ID["intake"].set(False)
    review.run(payload)
    assert ran[0][1] == ("claims",), "intake was switched off and still asked for"

    ran.clear()
    review.BY_ID["claims"].set(False)
    review.run(payload)
    assert ran == [], "everything is off and something still ran"


def test_the_claims_lane_honours_a_half_selection(tmp_path, monkeypatch):
    """claims and intake share one transcript parse but are two reviews; a user who
    switched one off means it."""
    from craft import claims_hook
    t = tmp_path / "t.jsonl"
    t.write_text(json.dumps({"type": "assistant", "message": {"content": []}}),
                 encoding="utf-8")
    seen = {}
    monkeypatch.setattr(claims_hook, "silent_repos",
                        lambda p: seen.setdefault("silent", True) or [])
    monkeypatch.setattr(claims_hook, "touched", lambda p: [])
    claims_hook.run({"transcript_path": str(t), "session_id": "s",
                     "_reviews": ["claims"]})
    assert "silent" not in seen, "intake was not asked for and ran anyway"


class TestTheTray:
    """The icon is a face on the registry. It owns no state and shows three states."""

    def test_it_shows_a_state_for_every_shape_of_the_registry(self):
        tray = pytest.importorskip("craft.review_tray")
        for r in review.REVIEWS:
            r.set(True)
        assert review.state()["colour"] == "green"
        review.BY_ID["argument"].set(False)
        assert review.state()["colour"] == "amber"
        for r in review.REVIEWS:
            r.set(False)
        assert review.state()["colour"] == "grey"
        for name in ("green", "amber", "grey"):
            assert tray.image(name).mode == "RGBA"

    def test_the_menu_carries_one_checkbox_per_review(self):
        tray = pytest.importorskip("craft.review_tray")
        items = list(tray.menu())
        labelled = [i for i in items if any(r.id in str(i.text) for r in review.REVIEWS)]
        assert len(labelled) == len(review.REVIEWS)
        for r in review.REVIEWS:
            r.set(True)
        assert all(i.checked for i in labelled)
        review.BY_ID["claims"].set(False)
        unchecked = [i for i in labelled if "claims" in str(i.text)]
        assert unchecked and not unchecked[0].checked

    def test_the_tooltip_never_exceeds_what_the_shell_will_show(self):
        tray = pytest.importorskip("craft.review_tray")
        for r in review.REVIEWS:
            r.set(True)
        assert len(tray.title(review.state())) <= 127
        review.BY_ID["claims"].set(False)
        assert len(tray.title(review.state())) <= 127
