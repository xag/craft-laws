"""The deciders of the laws rooted in Hurff's UI Stack, each seen red and seen clean.

A checker that has never been seen red is relocated guessing: every compiler here convicts
the drawing that breaks its law and says nothing of the one that keeps it."""

from quern import Node

from craft.compile import (COMPILABLE, compile_error_keeps_input, compile_invariants,
                           compile_work_kept)


def _surface(*elements, when="screen == 'sign-up'"):
    return Node(id="sign-up", kind="surface", payload={"when": when}, children=list(elements))


def _input(kept=False):
    payload = {"asks": "email", "holds": "email_text"}
    if kept:
        payload["kept"] = True
    return Node(id="email-field", kind="element", payload=payload)


def _act(id_, **payload):
    return Node(id=id_, kind="action", payload=payload)


TYPE = _act("type-email", enters="email_text", updates=[{"var": "email_text"}])
SEND = _act("send", commits=True, guard="screen == 'sign-up'", updates=[{"var": "email_text"}])


def test_a_failing_act_that_clears_the_input_is_refused():
    failing = _act("send-fails", fails=True, guard="screen == 'sign-up'",
                   updates=[{"var": "email_text"}, {"var": "error"}])
    out = compile_error_keeps_input([_surface(_input())], [TYPE, failing])
    assert [n.id for n in out] == ["an-error-keeps-what-the-user-entered--send-fails"]
    assert out[0].payload["expr"] == "not (screen == 'sign-up')"


def test_a_failing_act_that_leaves_the_input_is_clean():
    failing = _act("send-fails", fails=True, updates=[{"var": "error"}])
    assert compile_error_keeps_input([_surface(_input())], [TYPE, failing]) == []


def test_an_act_that_is_neither_the_entry_nor_the_sending_harms_the_work():
    reset = _act("start-over", guard="true", updates=[{"var": "email_text"}])
    out = compile_work_kept([_surface(_input(kept=True))], [TYPE, SEND, reset])
    assert [n.id for n in out] == [
        "the-users-work-is-never-harmed-by-an-act-or-by-inaction--start-over"]


def test_work_not_kept_beyond_the_page_is_lost_by_inaction():
    out = compile_work_kept([_surface(_input())], [TYPE, SEND])
    assert [n.id for n in out] == [
        "the-users-work-is-never-harmed-by-an-act-or-by-inaction--email-field--kept"]


def test_work_entered_sent_and_kept_is_clean():
    assert compile_work_kept([_surface(_input(kept=True))], [TYPE, SEND]) == []


def test_a_raw_binding_on_an_error_is_refused_and_a_catalogue_one_is_not():
    raw = Node(id="save-failed", kind="element", payload={"when": "error"}, children=[
        Node(id="save-failed-text", kind="binding", payload={"raw": True, "role": "text"})])
    human = Node(id="save-failed-kind", kind="element", payload={"when": "error"}, children=[
        Node(id="save-failed-kind-text", kind="binding",
             payload={"key": "errors.save_failed", "role": "text"})])
    assert "an-error-message-is-human-not-technical" in COMPILABLE
    out = compile_invariants([_surface(raw, human)],
                             laws=["an-error-message-is-human-not-technical"])
    assert [n.id for n in out] == ["an-error-message-is-human-not-technical--save-failed"]
