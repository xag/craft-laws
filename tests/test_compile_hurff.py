"""The deciders of the laws rooted in Hurff's UI Stack, each seen red and seen clean.

A checker that has never been seen red is relocated guessing: every compiler here convicts
the drawing that breaks its law and says nothing of the one that keeps it. They read the
facts the drawing already states - an input's `asks` and `action`, `content` for text no
catalogue carries - and the three interface@0.5.0 adds: `fails`, `commits`, `kept`."""

from quern import Node

from craft.compile import compile_error_is_human, compile_error_keeps_input, compile_work_kept


def _surface(*elements, when="screen == 'sign-up'"):
    return Node(id="sign-up", kind="surface", payload={"when": when}, children=list(elements))


def _input(kept=False):
    payload = {"asks": "email", "action": "type-email"}
    if kept:
        payload["kept"] = True
    return Node(id="email-field", kind="element", payload=payload)


def _act(id_, **payload):
    return Node(id=id_, kind="action", payload=payload)


TYPE = _act("type-email", updates=[{"var": "email"}])
SEND = _act("send", commits=True, guard="screen == 'sign-up'", updates=[{"var": "email"}])


def test_a_failing_act_that_clears_the_input_is_refused():
    failing = _act("send-fails", fails=True, guard="screen == 'sign-up'",
                   updates=[{"var": "email"}, {"var": "error"}])
    out = compile_error_keeps_input([_surface(_input())], [TYPE, failing])
    assert [n.id for n in out] == ["an-error-keeps-what-the-user-entered--send-fails"]
    assert out[0].payload["expr"] == "not (screen == 'sign-up')"


def test_a_failing_act_that_leaves_the_input_is_clean():
    failing = _act("send-fails", fails=True, updates=[{"var": "error"}])
    assert compile_error_keeps_input([_surface(_input())], [TYPE, failing]) == []


def test_an_act_that_is_neither_the_entry_nor_the_sending_harms_the_work():
    reset = _act("start-over", guard="true", updates=[{"var": "email"}])
    out = compile_work_kept([_surface(_input(kept=True))], [TYPE, SEND, reset])
    assert [n.id for n in out] == [
        "the-users-work-is-never-harmed-by-an-act-or-by-inaction--start-over"]


def test_work_not_kept_beyond_the_page_is_lost_by_inaction():
    out = compile_work_kept([_surface(_input())], [TYPE, SEND])
    assert [n.id for n in out] == [
        "the-users-work-is-never-harmed-by-an-act-or-by-inaction--email-field--kept"]


def test_work_entered_sent_and_kept_is_clean():
    assert compile_work_kept([_surface(_input(kept=True))], [TYPE, SEND]) == []


def test_a_failures_own_text_is_refused_and_a_catalogue_line_is_not():
    failing = _act("send-fails", fails=True, updates=[{"var": "send_failed"}])
    raw = Node(id="failure-text", kind="element", payload={"when": "send_failed"}, children=[
        Node(id="failure-text-content", kind="content", payload={"source": "the response"})])
    human = Node(id="failure-line", kind="element", payload={"when": "send_failed"}, children=[
        Node(id="failure-line-text", kind="binding",
             payload={"key": "errors.send_failed", "role": "text"})])
    elsewhere = Node(id="chore-title", kind="element", payload={"when": "true"}, children=[
        Node(id="chore-title-content", kind="content", payload={"source": "the household"})])
    out = compile_error_is_human([_surface(raw, human, elsewhere)], [failing])
    assert [n.id for n in out] == ["an-error-message-is-human-not-technical--failure-text"]
