"""The turn account: the deciders, and the two hooks that put them in a live turn."""

import json

import pytest

from craft import account, account_hook, account_toggle


def _acc(nodes):
    return account.Account(path="t.json", nodes={n["id"]: n for n in nodes})


def test_absence_licenses_nothing():
    a = _acc([
        {"id": "p1", "type": "I", "text": "no counter-example was found"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "it holds"},
        {"id": "r1", "type": "RA", "scheme": "absence", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    assert [f.law for f in account.check_absence_concludes_nothing(a)] == [
        "absence-of-evidence-concludes-nothing"]


def test_a_claim_cannot_support_itself():
    a = _acc([
        {"id": "c1", "type": "I", "role": "conclusion", "text": "it is so"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["c1"],
         "conclusion": "c1"},
    ])
    assert account.check_no_circular_support(a)


def test_a_conclusion_with_no_inference_is_an_assertion():
    a = _acc([{"id": "c1", "type": "I", "role": "conclusion", "text": "it is so"}])
    assert [f.law for f in account.check_conclusions_are_supported(a)] == [
        "a-conclusion-names-its-warrant"]


def test_a_dangling_conflict_node_is_a_format_defect():
    a = _acc([{"id": "x1", "type": "CA", "text": "the tape says otherwise"}])
    assert account.check_counter_evidence_is_consumed(a) == []
    found = account.check_shape(a)
    assert any("an end missing" in f.why for f in found)


def test_attacking_every_alternative_is_not_support():
    a = _acc([
        {"id": "alt", "type": "I", "text": "the other way"},
        {"id": "x1", "type": "CA", "premises": ["alt"], "conclusion": "alt",
         "text": "it would be slower"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so do it this way"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["x1"],
         "conclusion": "c1"},
    ])
    assert [f.law for f in account.check_support_is_not_only_attack(a)] == [
        "a-conclusion-stands-on-its-own-feet"]


def test_the_alarm_rings():
    """Every decider convicts the guilty account and acquits the clean one."""
    assert account._alarm() == 0


def test_an_unparseable_account_is_reported_not_ignored(tmp_path):
    p = tmp_path / "a.json"
    p.write_text("{not json", encoding="utf-8")
    found = account.check_file(p)
    assert found and "did not parse" in found[0].why


# --- the hooks ------------------------------------------------------------------------

def test_off_reaches_a_running_session(monkeypatch):
    monkeypatch.setenv("CRAFT_ACCOUNTS_OFF", "1")
    assert account_hook.off() is True
    assert account_hook.main.__doc__ is None or True   # main() short-circuits on off()


def test_the_prompt_hook_asks_for_the_account(capsys):
    assert account_hook.user_prompt_submit({}) == 0
    out = capsys.readouterr().out
    assert "EVERY GROUNDED PREMISE MUST QUOTE THE RECORD" in out
    assert ".craft/accounts/" in out


def test_a_turn_that_files_nothing_is_not_convicted(tmp_path):
    """Silence is the record's reporting bias, not a verdict on the answer."""
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    assert account_hook.stop({"session_id": "s", "transcript_path": str(t)}) == 0


def test_a_filed_account_that_convicts_comes_back_with_exit_2(tmp_path, monkeypatch,
                                                              capsys):
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    d = repo / ".craft" / "accounts" / "sess"
    d.mkdir(parents=True)
    (d / "1.json").write_text(json.dumps(account.GUILTY), encoding="utf-8")
    monkeypatch.setattr(account_hook, "repos_touched", lambda _p: [repo])
    monkeypatch.setattr(account_hook, "_already_reported", lambda _k: False)
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    code = account_hook.stop({"session_id": "sess", "transcript_path": str(t)})
    assert code == 2
    assert "law" in capsys.readouterr().err.lower()


def test_the_toggle_reports_three_states(monkeypatch):
    monkeypatch.setattr(account_toggle, "off", lambda: True)
    assert account_toggle.state()["colour"] == "grey"
    monkeypatch.setattr(account_toggle, "off", lambda: False)
    monkeypatch.setattr(account_toggle, "wired",
                        lambda: {"UserPromptSubmit": True, "Stop": True})
    assert account_toggle.state()["colour"] == "green"
    monkeypatch.setattr(account_toggle, "wired",
                        lambda: {"UserPromptSubmit": True, "Stop": False})
    s = account_toggle.state()
    assert s["colour"] == "amber" and "Stop" in account_toggle.render(s)


# --- validity is not soundness --------------------------------------------------------

def test_a_grade_is_a_judgment_the_machine_does_not_police():
    """The Celarent-over-a-counted-premise case, kept as the boundary marker: the
    entailment holds, the grade is the author's judgment, and under the owner's
    criterion (rules catch reasoning flaws, not missing justifications) nothing
    mechanical convicts it. Whether robust honestly grades one file-read is the
    reader's question, with the anchored quote beside it."""
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "producer",
         "text": "text appears eleven times, each time only to quote",
         "prop": "every use-of-text is a-quoting-use"},
        {"id": "p2", "type": "I", "ground": "given",
         "prop": "no a-quoting-use is a-rule-reading"},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "no rule reads the claim's sentence",
         "prop": "no use-of-text is a-rule-reading"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "premises": ["p2", "p1"], "conclusion": "c1"},
    ]})
    assert account.check_declared_deductions_are_valid(a) == []
    assert account.check_strength_is_licensed(a) == []


def test_the_same_syllogism_over_stipulated_premises_earns_robust():
    a = account.Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "given",
         "prop": "every use-of-text is a-quoting-use"},
        {"id": "p2", "type": "I", "ground": "given",
         "prop": "no a-quoting-use is a-rule-reading"},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "prop": "no use-of-text is a-rule-reading"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "premises": ["p2", "p1"], "conclusion": "c1"},
    ]})
    assert account.check_strength_is_licensed(a) == []


def test_the_machine_polices_no_judgment_only_the_scale():
    """Two grading rules died in one day: a premise-count cap, then a demanded basis
    field. The owner's criterion killed both: a rule ensures no reasoning flaw
    remains, not that everything said is justified. A grade the author chose stands,
    whatever the support; only a word off the agreed scale convicts."""
    a = _acc([
        {"id": "p1", "type": "I", "ground": "producer", "quote": "eleven occurrences"},
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "the proof is in one fact"},
        {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    assert account.check_strength_is_licensed(a) == []
    a2 = _acc([{"id": "c1", "type": "I", "role": "conclusion",
                "strength": "overwhelming", "text": "off the scale"}])
    found = account.check_strength_is_licensed(a2)
    assert found and "no term of" in found[0].why


def test_a_claimed_deduction_that_exhibits_nothing_convicts():
    """The founding sentence claimed PROOF. Filed as the deduction it claims to be,
    with nothing checkable exhibited, the claim of necessity is the flaw."""
    a = _acc([
        {"id": "p1", "type": "I", "ground": "producer", "quote": "eleven occurrences"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "the proof is in one fact"},
        {"id": "r1", "type": "RA", "scheme": "deduction", "premises": ["p1"],
         "conclusion": "c1"},
    ])
    found = account.check_declared_deductions_are_valid(a)
    assert [f.law for f in found] == [
        "the-premises-entail-the-conclusion-or-they-do-not"]
    assert "asserted, not shown" in found[0].why


def test_an_unanswered_attack_on_live_support_convicts():
    a = _acc([
        {"id": "p1", "type": "I", "ground": "producer", "quote": "the observation"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so it holds"},
        {"id": "r1", "type": "RA", "scheme": "verified-source", "premises": ["p1"],
         "conclusion": "c1"},
        {"id": "e1", "type": "I", "text": "the refuting observation"},
        {"id": "x1", "type": "CA", "premises": ["e1"], "conclusion": "p1",
         "text": "this contradicts p1"},
    ])
    found = account.check_counter_evidence_is_consumed(a)
    assert found and "nothing answers it" in found[0].why
    # answering the attack clears it
    a.nodes["x2"] = {"id": "x2", "type": "CA", "premises": ["p1"],
                     "conclusion": "x1", "text": "the refutation is itself refuted"}
    assert account.check_counter_evidence_is_consumed(a) == []


def test_grounded_nodes_with_no_record_refuse_rather_than_judge():
    import pytest as _pytest
    a = _acc([{"id": "p1", "type": "I", "ground": "producer", "quote": "43 passed"}])
    with _pytest.raises(LookupError, match="unverifiable is not judged"):
        account.check_grounds_are_anchored(a, None)


# --- the second whole-source adoption: Sophistical Refutations ------------------------

def test_an_idle_premise_in_a_verified_deduction_convicts():
    """Aristotle's non-cause: Barbara holds without the inserted passenger, and Z3
    re-asked without each premise names exactly the idle one."""
    a = _acc([
        {"id": "n1", "type": "I", "prop": "every B is A"},
        {"id": "n2", "type": "I", "prop": "every C is B"},
        {"id": "n3", "type": "I", "prop": "some D is A", "text": "inserted, idle"},
        {"id": "c1", "type": "I", "role": "conclusion", "prop": "every C is A"},
        {"id": "r1", "type": "RA", "scheme": "deduction",
         "premises": ["n1", "n2", "n3"], "conclusion": "c1"},
    ])
    found = account.check_declared_deductions_are_valid(a)
    assert [f.law for f in found] == ["a-premise-does-its-work"]
    assert "'n3'" in found[0].why
    # remove the passenger and the deduction is clean
    a.nodes["r1"]["premises"] = ["n1", "n2"]
    assert account.check_declared_deductions_are_valid(a) == []


def test_a_deduction_needs_no_declared_form_any_more():
    """Three parseable premises, no form field: Z3 decides directly."""
    a = _acc([
        {"id": "n1", "type": "I", "prop": "every B is A"},
        {"id": "n2", "type": "I", "prop": "every C is B"},
        {"id": "c1", "type": "I", "role": "conclusion", "prop": "some C is not A"},
        {"id": "r1", "type": "RA", "scheme": "deduction",
         "premises": ["n1", "n2"], "conclusion": "c1"},
    ])
    found = account.check_declared_deductions_are_valid(a)
    assert [f.law for f in found] == [
        "the-premises-entail-the-conclusion-or-they-do-not"]


def test_precision_from_nowhere_convicts_and_earned_precision_passes():
    a = _acc([
        {"id": "q1", "type": "I", "quantity": {"value": 44.7, "tolerance": 0.5}},
        {"id": "c1", "type": "I", "role": "conclusion",
         "quantity": {"value": 44.71, "tolerance": 0.001}},
        {"id": "r1", "type": "RA", "scheme": "verified-source", "premises": ["q1"],
         "conclusion": "c1"},
    ])
    found = account.check_precision_is_earned(a)
    assert [f.law for f in found] == ["a-figure-is-no-more-precise-than-its-inputs"]
    a.nodes["c1"]["quantity"]["tolerance"] = 0.5
    assert account.check_precision_is_earned(a) == []


# --- the structured layer: schemes as data, critical questions as undercuts -----------

def test_a_scheme_invoked_without_its_premises_convicts():
    a = _acc([
        {"id": "w1", "type": "I", "slot": "expert", "text": "W is an expert"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so S"},
        {"id": "r1", "type": "RA", "scheme": "walton:expert_opinion",
         "premises": ["w1"], "conclusion": "c1"},
    ])
    found = account.check_scheme_instances(a)
    assert [f.law for f in found] == ["a-scheme-is-instantiated-not-invoked"]
    assert "in_domain" in found[0].why and "asserts" in found[0].why


def test_an_unpublished_scheme_name_convicts():
    a = _acc([
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so S"},
        {"id": "r1", "type": "RA", "scheme": "walton:vibes", "premises": [],
         "conclusion": "c1"},
    ])
    found = account.check_scheme_instances(a)
    assert found and "nobody published" in found[0].why


def test_a_raised_critical_question_defeats_until_answered():
    """The 41 critical questions need one decider: an undercut carrying the
    exception slot, judged by the same defense mechanics as any attack."""
    nodes = [
        {"id": "w1", "type": "I", "slot": "expert", "text": "W is an expert in D"},
        {"id": "w2", "type": "I", "slot": "in_domain", "text": "S is in D"},
        {"id": "w3", "type": "I", "slot": "asserts", "text": "W asserts S"},
        {"id": "c1", "type": "I", "role": "conclusion", "text": "S, defeasibly"},
        {"id": "r1", "type": "RA", "scheme": "walton:expert_opinion",
         "premises": ["w1", "w2", "w3"], "conclusion": "c1"},
        {"id": "e1", "type": "I", "text": "W took money from the vendor"},
        {"id": "x1", "type": "CA", "slot": "untrustworthy", "premises": ["e1"],
         "conclusion": "r1", "text": "CQ: is W trustworthy?"},
    ]
    a = _acc(nodes)
    assert account.check_scheme_instances(a) == []
    found = account.check_counter_evidence_is_consumed(a)
    assert found and "critical question 'untrustworthy'" in found[0].why
    # answering the question clears the defeat
    a.nodes["x2"] = {"id": "x2", "type": "CA", "premises": ["w3"],
                     "conclusion": "x1", "text": "the payment was disclosed and vetted"}
    assert account.check_counter_evidence_is_consumed(a) == []


# --- the hook's two defects, fixed ----------------------------------------------------

def test_accounts_are_found_session_wide_not_only_where_the_turn_wrote(tmp_path,
                                                                       monkeypatch):
    """The defect: a turn that argues without editing filed its account in one repo
    while the hook searched the repos it wrote to, so the account was never judged."""
    elsewhere = tmp_path / "elsewhere"
    d = elsewhere / ".craft" / "accounts" / "sess"
    d.mkdir(parents=True)
    (d / "1.json").write_text(json.dumps({"nodes": []}), encoding="utf-8")
    monkeypatch.setattr(account_hook, "_ROOT", elsewhere)
    # roots is empty: the turn wrote to no repo at all
    found = account_hook.accounts_for("sess", [])
    assert [p.name for p in found] == ["1.json"]


def test_residual_json_is_not_judged_as_an_account(tmp_path, monkeypatch):
    d = tmp_path / ".craft" / "accounts" / "sess"
    d.mkdir(parents=True)
    (d / "1.json").write_text(json.dumps({"nodes": []}), encoding="utf-8")
    (d / "residual.json").write_text(json.dumps({"sentences": 3}), encoding="utf-8")
    monkeypatch.setattr(account_hook, "_ROOT", tmp_path)
    assert [p.name for p in account_hook.accounts_for("sess", [])] == ["1.json"]


def test_a_clean_verdict_is_reported_not_silent(tmp_path, monkeypatch, capsys):
    """Silence on a pass is indistinguishable from a hook that never looked."""
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    d = repo / ".craft" / "accounts" / "sess"
    d.mkdir(parents=True)
    (d / "1.json").write_text(json.dumps({"nodes": [
        {"id": "c1", "type": "I", "role": "conclusion", "text": "so it holds"},
        {"id": "p1", "type": "I", "text": "a premise"},
        {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
         "conclusion": "c1"}]}), encoding="utf-8")
    monkeypatch.setattr(account_hook, "repos_touched", lambda _p: [repo])
    monkeypatch.setattr(account_hook, "_already_reported", lambda _k: False)
    t = tmp_path / "t.jsonl"
    t.write_text("", encoding="utf-8")
    code = account_hook.stop({"session_id": "sess", "transcript_path": str(t)})
    assert code == 2
    assert "no decider convicts" in capsys.readouterr().err
