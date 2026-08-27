"""The turn account: the argument an answer makes, as data a rule can convict --
rebuilt anchored, after the first version was removed for grading its own author.

THE CONSTRAINT THIS DESIGN IS BUILT TO (the-turn-account-lane-is-removed): a checker
fed only by the checked party's labels reports those labels. Five versions failed that
way in one day, each moving the author-chosen word one field deeper. The lanes that
work in this repository hold a filing to something its author cannot retro-fit -- a
field's shape, a source hash, a verbatim quote -- and the first account had no anchor.

THIS ONE HAS ONE. Every grounded premise must carry `quote`: a verbatim stretch of the
turn's own record (craft/record.py), which the author does not write. `producer` and
`stand-in` quote tool results the harness wrote; `given` and `user-surface` quote the
user's own messages. A fabricated quote is unanchored and convicts; relabelling a
counted observation as `given` now demands words the user actually said. What stays
the author's -- selection and translation -- is the same declared residue as
drawing.py's authored derivation, and staging a command to print a wanted sentence
stays possible but visible, since the record keeps the command beside its output.

THE VOCABULARIES ARE PUBLISHED, NOT INVENTED: AIF for the graph (I/RA/CA nodes), Z3
entailment over Lark-parsed propositions for declared deductions, Greenwell, Holloway
& Knight (DSN 2005) for the graph-decidable fallacies -- 6 of 33, per
craft/census_argument.py, and the pass report says so, so a green is never read as
"the argument is sound". Every law a decider convicts under is registered and cited in
craft/account_laws.py, sources adopted whole; tests/test_law_registry.py is the gate
that makes an ad-hoc rule a red build. Strength is never computed by the machine -- counting premise nodes is not counting
evidence. A grade above limited carries `basis`, the note's traceable account, or
convicts; a verified entailment from given premises needs none, being necessity.

    python -m craft.account --transcript T FILE...   hold accounts to the laws
    python -m craft.account --alarm                  prove every decider can convict
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# --- AIF node types, as the specification names them ----------------------------------

I_NODE = "I"    # propositional information: a premise, a datum, a conclusion
RA_NODE = "RA"  # inference: a scheme application concluding one thing from others
CA_NODE = "CA"  # conflict: one thing attacking another

NODE_TYPES = (I_NODE, RA_NODE, CA_NODE)

# --- the ground an I-node stands on ---------------------------------------------------
#
# The same three words craft/claims.py uses for evidence, for the same reason: where a
# thing was observed decides what may be concluded from it. `given` is the fourth and it
# is not an observation -- it is something the user said, or a definition, which needs no
# evidence and licenses nothing empirical.

GROUNDS = ("user-surface", "stand-in", "producer", "given")

# --- conclusion strength: the closed scale, from the IPCC note this estate already pins -
#
# craft/practice.py's the-calibration-vocabulary adopted these for findings. A conclusion
# in an account grades itself on the same scale, so one vocabulary covers both.

STRENGTH = ("limited", "medium", "robust")

_RANK = {"limited": 1, "medium": 2, "robust": 3}


@dataclass
class Finding:
    law: str
    where: str
    quote: str
    why: str


@dataclass
class Account:
    path: str
    nodes: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict)

    def of_type(self, t):
        return [n for n in self.nodes.values() if n.get("type") == t]

    def conclusions(self):
        return [n for n in self.of_type(I_NODE) if n.get("role") == "conclusion"]


def load(path: Path) -> Account:
    raw = json.loads(path.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in raw.get("nodes", []) if "id" in n}
    for n in nodes.values():
        if "mood" in n or "figure" in n:
            raise ValueError(f"node {n['id']!r} declares its own mood or figure; the "
                             "format does not admit them -- both are computed from "
                             "the propositions")
    return Account(path=path.name, nodes=nodes, raw=raw)


def _q(node) -> str:
    return str(node.get("text", ""))[:110]


# --- the deciders ---------------------------------------------------------------------

def check_shape(a: Account) -> list[Finding]:
    """Before any law can speak, the graph has to be one: known types, edges that
    land, and AIF's own rule that an I-node never points straight at an I-node."""
    out = []
    for n in a.nodes.values():
        if n.get("type") not in NODE_TYPES:
            out.append(Finding("an-account-is-an-aif-graph", n.get("id", "?"), _q(n),
                               f"node type {n.get('type')!r} is not one of {NODE_TYPES}"))
        if n.get("type") == I_NODE and n.get("ground") not in GROUNDS + (None,):
            out.append(Finding("an-account-is-an-aif-graph", n.get("id", "?"), _q(n),
                               f"ground {n.get('ground')!r} is not one of {GROUNDS}"))
        for ref in list(n.get("premises", [])) + list(n.get("conclusion", []) if
                                                      isinstance(n.get("conclusion"), list)
                                                      else [n["conclusion"]] if
                                                      n.get("conclusion") else []):
            if ref not in a.nodes:
                out.append(Finding("an-account-is-an-aif-graph", n.get("id", "?"), _q(n),
                                   f"edge names {ref!r}, which is not a node here"))
    # AIF's "an I-node never points straight at another I-node" holds by
    # construction in this format: only RA and CA nodes carry edges.
    return out


def check_conclusions_are_supported(a: Account) -> list[Finding]:
    """A conclusion with no RA concluding it is an assertion, not an argument."""
    concluded = set()
    for r in a.of_type(RA_NODE):
        c = r.get("conclusion")
        concluded.update([c] if isinstance(c, str) else list(c or []))
    return [Finding("a-conclusion-names-its-warrant", n["id"], _q(n),
                    "stated as a conclusion with no RA node concluding it: an "
                    "assertion wearing an argument's place")
            for n in a.conclusions() if n["id"] not in concluded]


def check_no_circular_support(a: Account) -> list[Finding]:
    """Greenwell et al., Circular Argument: a claim reasserted as its own premise.
    Reachability over premise -> conclusion, nothing else."""
    edges: dict[str, set] = {}
    for r in a.of_type(RA_NODE):
        c = r.get("conclusion")
        targets = [c] if isinstance(c, str) else list(c or [])
        for p in r.get("premises", []):
            edges.setdefault(p, set()).update(targets)
    out = []
    for start in list(edges):
        seen, stack = set(), [start]
        while stack:
            cur = stack.pop()
            for nxt in edges.get(cur, ()):
                if nxt == start:
                    n = a.nodes.get(start, {})
                    out.append(Finding("no-claim-supports-itself", start, _q(n),
                                       "this node supports itself through the graph: a "
                                       "circular argument (Greenwell et al., DSN 2005)"))
                    stack = []
                    break
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return out


def check_counter_evidence_is_consumed(a: Account) -> list[Finding]:
    """Greenwell et al., Ignoring Available Counter-Evidence: a CA-node present in the
    graph and attached to nothing is Dung's input, unconsumed."""
    out = []
    for n in a.of_type(CA_NODE):
        if not n.get("premises") or not n.get("conclusion"):
            out.append(Finding("counter-evidence-is-answered", n["id"], _q(n),
                               "a conflict node with an end missing: counter-evidence "
                               "recorded and attached to nothing"))
    return out


def check_support_is_not_only_attack(a: Account) -> list[Finding]:
    """Greenwell et al., Damning the Alternatives: support consisting only of attacks
    on the alternatives, with nothing standing on its own."""
    attacked = {n.get("conclusion") for n in a.of_type(CA_NODE)}
    out = []
    for r in a.of_type(RA_NODE):
        prem = list(r.get("premises", []))
        if prem and all(a.nodes.get(p, {}).get("type") == CA_NODE or p in attacked
                        for p in prem):
            c = r.get("conclusion")
            cid = c if isinstance(c, str) else (list(c or [None])[0])
            out.append(Finding("a-conclusion-stands-on-its-own-feet", r["id"],
                               _q(a.nodes.get(cid, {})),
                               "every premise of this inference is an attack on an "
                               "alternative: damning the alternatives (Greenwell et al.)"))
    return out


def check_absence_concludes_nothing(a: Account) -> list[Finding]:
    """Greenwell et al., Arguing from Ignorance -- with the source's own exemption:
    the argument does not exhibit the fallacy if it cites a sufficiently-exhaustive
    search for counter-evidence that turned up none. A grounded premise on the same
    inference documents that search; whether it was exhaustive stays with a reader."""
    out = []
    for r in a.of_type(RA_NODE):
        if r.get("scheme") != "absence":
            continue
        searched = any(a.nodes.get(pid, {}).get("ground")
                       in ("producer", "stand-in", "user-surface")
                       for pid in r.get("premises", []))
        if searched:
            continue
        c = r.get("conclusion")
        cid = c if isinstance(c, str) else (list(c or [None])[0])
        out.append(Finding("absence-of-evidence-concludes-nothing", r["id"],
                           _q(a.nodes.get(cid, {})),
                           "the warrant is that nothing was found, and no grounded "
                           "premise documents the search (Greenwell et al., Arguing "
                           "from Ignorance, exemption unmet)"))
    return out


def check_strength_is_licensed(a: Account) -> list[Finding]:
    """The machine never computes a grade -- counting premise nodes is not counting
    evidence, as the owner showed within an hour of the count-based version shipping:
    one premise can quote a 254-run suite, and one quote split across two nodes is not
    two lines of evidence. What the note actually instructs is mechanizable with no
    false positives: every graded finding carries a traceable account of the judgment.

    So: `limited` claims little and needs nothing. `medium` or `robust` on empirical
    support demands `basis` -- the author's stated evaluation, prose, beside the
    grade. A verified entailment from given premises needs no basis: the proof is the
    basis, and necessity is not an empirical grade. Whether a stated basis is honest
    stays with a reader, who has the anchors beside it; a missing one is a fact."""
    from .categorical import ParseError, parse
    from .entailment import entails

    out = []
    for n in a.conclusions():
        said = n.get("strength")
        if said is None:
            continue
        where, quote = n["id"], _q(n)
        if said not in STRENGTH:
            out.append(Finding("calibration-is-agreed-before-the-case", where, quote,
                               f"strength {said!r} is no term of {STRENGTH}"))
            continue
        if said == "limited":
            continue
        ras = [r for r in a.of_type(RA_NODE)
               if n["id"] in ([r.get("conclusion")] if isinstance(r.get("conclusion"),
                                                                  str)
                              else list(r.get("conclusion") or []))]
        necessary = False
        for r in ras:
            pids = list(r.get("premises", []))
            if not pids or any(a.nodes.get(pid, {}).get("ground") != "given"
                               for pid in pids):
                continue
            try:
                prem = [parse(str(a.nodes[pid].get("prop"))) for pid in pids]
                con = parse(str(n.get("prop")))
            except (ParseError, KeyError, TypeError):
                continue
            if entails(prem, con,
                       nonempty_terms=bool(r.get("existential_import"))).valid:
                necessary = True
                break
        if necessary:
            continue
        if not str(n.get("basis") or "").strip():
            out.append(Finding("a-qualifier-is-licensed-by-the-evidence", where, quote,
                               f"graded {said!r} with no basis: the note requires a "
                               "traceable account of the evaluation behind every "
                               "graded finding -- state it, or grade limited"))
    return out


def check_declared_deductions_are_valid(a: Account) -> list[Finding]:
    """A declared deduction is decided by Z3, over first-order logic.

    Nothing here knows what a syllogism is. Each proposition is parsed by Lark against
    craft/categorical.lark, translated to FOL, and the solver is asked whether premises
    AND NOT conclusion is unsatisfiable. When it is satisfiable the solver's own
    counter-model is reported, which is a refutation a reader can check rather than a
    rule name they have to trust.

    Four earlier versions of this check read a label: `scheme`, then `mood`+`figure`,
    then a record of parts, then rules transcribed by hand. Each was caught by the
    owner. This one asks a prover."""
    from .categorical import ParseError, parse
    from .entailment import entails

    out = []
    for r in a.of_type(RA_NODE):
        if r.get("form") != "syllogism":
            continue
        cid = r.get("conclusion")
        cid = cid if isinstance(cid, str) else (list(cid or [None])[0])
        texts = [a.nodes.get(pid, {}).get("prop") for pid in r.get("premises", [])]
        con_text = a.nodes.get(cid, {}).get("prop")
        if not con_text or any(t is None for t in texts):
            out.append(Finding("a-proposition-is-in-the-language", r["id"], "",
                               "form is 'syllogism' and a premise or the conclusion "
                               "carries no `prop` written in the language: nothing "
                               "here can be parsed, so nothing can be decided"))
            continue
        try:
            premises = [parse(t) for t in texts]
            conclusion = parse(con_text)
        except ParseError as e:
            out.append(Finding("a-proposition-is-in-the-language", r["id"], "",
                               f"the grammar refused a proposition: {e}"))
            continue
        result = entails(premises, conclusion,
                         nonempty_terms=bool(r.get("existential_import")))
        if result.valid:
            continue
        label = ""
        try:
            from .syllogism import derive
            mood, figure = derive(texts, con_text)
            label = f" (the form is {mood}-{figure})"
        except Exception:
            pass
        out.append(Finding("the-premises-entail-the-conclusion-or-they-do-not",
                           r["id"], "",
                           f"Z3 finds the premises do not entail the conclusion"
                           f"{label}; it satisfies them with the conclusion false: "
                           f"{result.counter_model.replace(chr(10), ' ')[:200]}"))
    return out


def check_grounds_are_anchored(a: Account, corpus=None) -> list[Finding]:
    """A grounded premise quotes the record, or it convicts. The corpus is the turn's
    transcript read by craft.record -- tool results for producer/stand-in, the user's
    messages for given/user-surface. With no corpus supplied, every grounded node is
    reported unverifiable rather than passed: a check that could not check is not a
    pass."""
    out = []
    for n in a.of_type(I_NODE):
        g = n.get("ground")
        if g not in ("producer", "stand-in", "given", "user-surface"):
            continue
        quote = str(n.get("quote") or "")
        if not quote.strip():
            out.append(Finding("a-ground-is-a-quotation-from-the-record",
                               n.get("id", "?"), _q(n),
                               f"ground {g!r} with no quote: a ground is a verbatim "
                               "stretch of the record, not a word the author picks"))
            continue
        if corpus is None:
            out.append(Finding("a-ground-is-a-quotation-from-the-record",
                               n.get("id", "?"), _q(n),
                               "no record supplied, so this quote could not be "
                               "checked -- and unchecked is not anchored"))
            continue
        if not corpus.anchors(g, quote):
            pool = ("tool results" if g in ("producer", "stand-in")
                    else "the user's messages")
            out.append(Finding("a-ground-is-a-quotation-from-the-record",
                               n.get("id", "?"), _q(n),
                               f"the quote does not appear in {pool} for this turn: "
                               f"ground {g!r} asserts words the record does not hold"))
    return out


CHECKS = (check_shape, check_conclusions_are_supported, check_no_circular_support,
          check_counter_evidence_is_consumed, check_support_is_not_only_attack,
          check_absence_concludes_nothing, check_strength_is_licensed,
          check_declared_deductions_are_valid)


def check_file(path: Path, corpus=None) -> list[Finding]:
    try:
        a = load(path)
    except (OSError, ValueError) as e:
        return [Finding("an-account-is-an-aif-graph", path.name, "",
                        f"the account did not parse: {e}")]
    return ([f for c in CHECKS for f in c(a)]
            + check_grounds_are_anchored(a, corpus))


# --- the alarm ------------------------------------------------------------------------
#
# Every decider faces a guilty account it must convict and a clean one it must not. A
# checker never seen red is relocated guessing.

GUILTY = {
    "nodes": [
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "no decider reads the claim's sentence"},
        {"id": "p1", "type": "I", "ground": "producer",
         "text": "text is read eleven times, each time only to quote"},
        {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
         "conclusion": "c1"},
        {"id": "c2", "type": "I", "role": "conclusion", "text": "unsupported"},
        {"id": "l1", "type": "I", "text": "loop"},
        {"id": "r2", "type": "RA", "scheme": "deduction", "premises": ["l1"],
         "conclusion": "l1"},
        {"id": "s1", "type": "I", "text": "every P is M",
         "prop": "every P is M"},
        {"id": "s3", "type": "I", "text": "every S is M",
         "prop": "every S is M"},
        {"id": "s2", "type": "I", "role": "conclusion", "text": "so every S is P",
         "prop": "every S is P"},
        {"id": "r5", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "premises": ["s1", "s3"], "conclusion": "s2"},
        {"id": "s4", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "an empirical premise stated as necessary"},
        {"id": "s5", "type": "I", "ground": "producer", "quote": "one run",
         "text": "one observation"},
        {"id": "r6", "type": "RA", "scheme": "verified-source", "premises": ["s5"],
         "conclusion": "s4"},
        {"id": "x1", "type": "CA", "text": "dangling conflict"},
        {"id": "a1", "type": "I", "text": "nothing was found"},
        {"id": "r3", "type": "RA", "scheme": "absence", "premises": ["a1"],
         "conclusion": "c1"},
        {"id": "alt1", "type": "I", "text": "the alternative design"},
        {"id": "x2", "type": "CA", "premises": ["p1"], "conclusion": "alt1",
         "text": "the alternative would be slower"},
        {"id": "c3", "type": "I", "role": "conclusion", "text": "so do it this way"},
        {"id": "r4", "type": "RA", "scheme": "deduction", "premises": ["x2"],
         "conclusion": "c3"},
        {"id": "bad", "type": "Z", "text": "not an AIF type"},
    ]
}

CLEAN = {
    "nodes": [
        {"id": "c1", "type": "I", "role": "conclusion", "strength": "limited",
         "text": "no decider reads the claim's sentence"},
        {"id": "p1", "type": "I", "ground": "producer",
         "text": "text is read eleven times, each time only to quote"},
        {"id": "r1", "type": "RA", "scheme": "sign", "premises": ["p1"],
         "conclusion": "c1"},
        {"id": "s1", "type": "I", "ground": "given", "text": "every B is A",
         "prop": "every B is A"},
        {"id": "s3", "type": "I", "ground": "given", "text": "every C is B",
         "prop": "every C is B"},
        {"id": "s2", "type": "I", "role": "conclusion", "strength": "robust",
         "text": "every C is A",
         "prop": "every C is A"},
        {"id": "r2", "type": "RA", "scheme": "deduction", "form": "syllogism",
         "premises": ["s1", "s3"], "conclusion": "s2"},
    ]
}


def _alarm() -> int:
    import tempfile

    from .record import Corpus
    dead = []
    # the anchor decider, against a synthetic record
    corpus = Corpus(tool_text="43 passed in 1.52s", user_text="build something that works")
    anchored = Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "producer", "quote": "43 passed in 1.52s"},
        {"id": "p2", "type": "I", "ground": "given",
         "quote": "build something that works"},
    ]})
    fabricated = Account(path="t", nodes={n["id"]: n for n in [
        {"id": "p1", "type": "I", "ground": "producer", "quote": "999 passed"},
        {"id": "p2", "type": "I", "ground": "given", "quote": "43 passed in 1.52s"},
        {"id": "p3", "type": "I", "ground": "producer"},
    ]})
    bad = []
    if check_grounds_are_anchored(anchored, corpus):
        bad.append("check_grounds_are_anchored convicted quotes the record holds")
    got = {f.where for f in check_grounds_are_anchored(fabricated, corpus)}
    if got != {"p1", "p2", "p3"}:
        bad.append(f"check_grounds_are_anchored missed a fabrication: convicted {got}, "
                   "wanted p1 (invented), p2 (wrong pool), p3 (no quote)")
    if len(check_grounds_are_anchored(anchored, None)) != 2:
        bad.append("with no record, grounded nodes must be reported unverifiable")
    dead += bad
    print(f"  {'DEAD' if bad else 'ok  '} check_grounds_are_anchored")
    with tempfile.TemporaryDirectory() as d:
        g, c = Path(d) / "guilty.json", Path(d) / "clean.json"
        g.write_text(json.dumps(GUILTY), encoding="utf-8")
        c.write_text(json.dumps(CLEAN), encoding="utf-8")
        ga, ca = load(g), load(c)
        for check in CHECKS:
            bad = []
            if not check(ga):
                bad.append(f"{check.__name__} missed the guilty account")
            if check(ca):
                bad.append(f"{check.__name__} convicted the clean account")
            dead += bad
            print(f"  {'DEAD' if bad else 'ok  '} {check.__name__}")
    for d_ in dead:
        print("\nDEAD ALARM  " + d_)
    if dead:
        return 1
    print(f"\nevery alarm rings: {len(CHECKS)} decider(s) over one guilty account "
          "and one clean one.")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.account",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="turn accounts to hold to the laws")
    ap.add_argument("--transcript", type=Path,
                    help="the session transcript the grounds must quote; without it "
                         "every grounded node is reported unverifiable, not passed")
    ap.add_argument("--alarm", action="store_true",
                    help="prove every decider can convict, then exit")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.files:
        ap.error("give at least one account, or --alarm")
    corpus = None
    if args.transcript:
        from .record import read
        corpus = read(args.transcript)
        print(f"record: {corpus.counts.get('tool_results', 0)} tool result(s), "
              f"{corpus.counts.get('user_texts', 0)} user text(s)")
    found = []
    for f in args.files:
        found += check_file(Path(f), corpus)
    for fd in found:
        print(f"  RED {fd.law} [{fd.where}] {fd.quote}\n      {fd.why}")
    if not found:
        print(f"{len(args.files)} account(s): no decider convicts. That clears the "
              "graph-decidable 6 of Greenwell et al.'s 33 fallacies and anchors every "
              "ground to the record; selection, translation and a staged record stay "
              "with a reader.")
        return 0
    print(f"\n{len(found)} finding(s) across {len(args.files)} account(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
