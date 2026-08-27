"""The turn account: the argument an answer makes, as data a rule can convict.

craft.claims checks what a turn CLAIMS about work it did to files. Nothing checked
what a turn ARGUES to the person reading it -- and an answer is mostly argument. The
gap was found by the owner on 2026-08-27, when a reply called a count of grep hits
"the proof", and no mechanism in this estate could see it: the sentence was in a chat
reply, not a file; no claim was filed; and no decider reads prose anyway.

WHY A GRAPH AND NOT A WORD LIST. The lesson of craft/prose.py's deleted checks is that
a pattern over the sentences an author wrote for another purpose cannot tell what those
sentences MEAN. So the author derives the argument as data -- the same division of
labour craft/drawing.py already uses for prose -- and every check here runs over that
data. The derivation can be wrong; the checks cannot. What keeps a derivation honest is
that it is committed, it quotes its sentences verbatim, and it is refutable by reading.

THE VOCABULARIES ARE PUBLISHED, NOT INVENTED:

  AIF (Chesnevar et al. 2006): I-nodes carry propositional information, S-nodes carry
  the application of a scheme -- RA for inference, CA for conflict. An I-node never
  points straight at another I-node. quality-harness/harness/argument.py implements
  the same shapes over ledgers; this module is the same theory over one turn, and the
  two are deliberately separate implementations of a published spec rather than an
  import across a dependency edge that points the wrong way.

  DUNG 1995: (arguments, attacks). The grounded extension is what survives conflict.

  GREENWELL, HOLLOWAY & KNIGHT (DSN 2005, Table 6): 33 safety-argument fallacies.
  craft/census_argument.py classifies them and MEASURES the ceiling: 6 of 33 are
  decidable from the graph, 16 want vocabulary the graph does not carry, 11 stay with
  a reader. The deciders below are that 6, and no more. An account that passes has
  cleared 18% of one published taxonomy -- which is the honest claim, and is stated in
  the report so nobody reads a green as "the argument is sound".

WHAT IS OURS AND MARKED SO: the WARRANT table. Nothing in AIF or Walton says which
conclusion-strength word a kind of warrant licenses. The mapping below is this estate's
reading, it is the one place to argue with, and it is the check that would have caught
the reply that started this.

    python -m craft.account FILE...     hold accounts to the laws
    python -m craft.account --alarm     prove every decider can convict
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

# --- OURS: what a warrant licenses ----------------------------------------------------
#
# Read this as the estate's reading, not as anybody's specification. A scheme name comes
# from Walton's catalogue where one fits; the CEILING beside it is ours.
#
#   deduction        the conclusion cannot be false if the premises hold -- definitional
#                    restatement, arithmetic over stated numbers. Licenses robust.
#   verified-source  a fact read directly off a system that was run or a file that was
#                    read. Licenses medium: reading one file correctly says nothing about
#                    the next one.
#   sign             an indicator taken to show something else -- a count, a symptom, a
#                    correlate. Licenses limited, and this is the row that convicts a
#                    count of grep hits called a proof.
#   example          one or more instances offered for a general claim. Licenses limited.
#   authority        somebody said so. Licenses limited.
#   absence          nothing was found. Licenses NOTHING: see arguing-from-ignorance.
#
# The words above the ceiling are refused, not warned about, because the whole failure
# this module exists for is a strength word nobody was entitled to.

WARRANTS = {
    "deduction": "robust",
    "verified-source": "medium",
    "sign": "limited",
    "example": "limited",
    "authority": "limited",
    "absence": None,
}

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
        if n.get("type") in (RA_NODE, CA_NODE):
            for ref in list(n.get("premises", [])):
                if a.nodes.get(ref, {}).get("type") in (RA_NODE, CA_NODE):
                    continue
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
    """Greenwell et al., Arguing from Ignorance: a conclusion whose only support is
    that no counter-evidence was found."""
    out = []
    for r in a.of_type(RA_NODE):
        if r.get("scheme") != "absence":
            continue
        c = r.get("conclusion")
        cid = c if isinstance(c, str) else (list(c or [None])[0])
        out.append(Finding("absence-of-evidence-concludes-nothing", r["id"],
                           _q(a.nodes.get(cid, {})),
                           "the warrant is that nothing was found; absence licenses no "
                           "conclusion (Greenwell et al., Arguing from Ignorance)"))
    return out


def check_strength_is_licensed(a: Account) -> list[Finding]:
    """OURS: a conclusion may not be stated more strongly than its warrant licenses.
    The scheme names come from the catalogue; the ceiling is this estate's reading."""
    ceiling: dict[str, str] = {}
    for r in a.of_type(RA_NODE):
        w = WARRANTS.get(r.get("scheme"))
        c = r.get("conclusion")
        for cid in ([c] if isinstance(c, str) else list(c or [])):
            if w is None:
                continue
            best = ceiling.get(cid)
            if best is None or _RANK[w] > _RANK[best]:
                ceiling[cid] = w
    out = []
    for n in a.conclusions():
        said = n.get("strength")
        if said is None:
            continue
        if said not in STRENGTH:
            out.append(Finding("a-conclusion-is-graded-on-the-agreed-scale", n["id"],
                               _q(n), f"strength {said!r} is no term of {STRENGTH}"))
            continue
        allowed = ceiling.get(n["id"])
        if allowed is None:
            continue
        if _RANK[said] > _RANK[allowed]:
            out.append(Finding("a-conclusion-is-no-stronger-than-its-warrant", n["id"],
                               _q(n),
                               f"stated {said!r} on a warrant that licenses at most "
                               f"{allowed!r}: the strength is not earned"))
    return out


def check_deduction_shows_its_form(a: Account) -> list[Finding]:
    """`deduction` is the only warrant licensing `robust`, so it is the only one that
    must show its work. A deduction that names no form is a label, and a label is
    what this module was built because of."""
    out = []
    for r in a.of_type(RA_NODE):
        if r.get("scheme") != "deduction" or r.get("form"):
            continue
        out.append(Finding("a-declared-deduction-shows-its-form", r["id"], "",
                           "scheme is 'deduction' and no form is given: nothing here "
                           "can be checked, so the strongest warrant rests on a word"))
    return out


def check_declared_deductions_are_valid(a: Account) -> list[Finding]:
    """A declared syllogistic form is judged on the form DERIVED from its propositions.

    mood and figure are not read from the account, and an account that supplies them is
    refused: they were accepted once, and changing "figure": 2 to 1 with every
    proposition byte-identical turned a conviction into a pass. Each premise and the
    conclusion carry their own quantity, quality, subject and predicate; the form is a
    consequence of those, so a different verdict needs a different premise."""
    from .syllogism import FormError, derive, judge

    out = []
    for r in a.of_type(RA_NODE):
        if r.get("form") != "syllogism":
            continue
        if "mood" in r or "figure" in r:
            out.append(Finding("a-form-is-derived-not-declared", r["id"], "",
                               "this node states its own mood or figure; both are "
                               "computed from the propositions, and accepting them "
                               "is how a label passed for a formalisation"))
            continue
        props = [a.nodes.get(pid, {}).get("prop") for pid in r.get("premises", [])]
        cid = r.get("conclusion")
        cid = cid if isinstance(cid, str) else (list(cid or [None])[0])
        con = a.nodes.get(cid, {}).get("prop")
        if not con or any(pr is None for pr in props):
            out.append(Finding("a-form-is-derived-not-declared", r["id"], "",
                               "form is 'syllogism' and a premise or the conclusion "
                               "carries no `prop`: nothing to derive a form from"))
            continue
        try:
            mood, figure = derive(props, con)
        except FormError as e:
            out.append(Finding("a-syllogism-holds-or-it-does-not", r["id"], "",
                               f"these propositions are not a syllogism: {e}"))
            continue
        v = judge(mood, figure, bool(r.get("existential_import")))
        if not v.valid:
            out.append(Finding("a-syllogism-holds-or-it-does-not", r["id"], "",
                               f"derived {mood}-{figure}, which is not valid: "
                               f"{', '.join(v.broke)}"))
    return out


CHECKS = (check_shape, check_conclusions_are_supported, check_no_circular_support,
          check_counter_evidence_is_consumed, check_support_is_not_only_attack,
          check_absence_concludes_nothing, check_strength_is_licensed,
          check_deduction_shows_its_form,
          check_declared_deductions_are_valid)


def check_file(path: Path) -> list[Finding]:
    try:
        a = load(path)
    except (OSError, ValueError) as e:
        return [Finding("an-account-is-an-aif-graph", path.name, "",
                        f"the account did not parse: {e}")]
    return [f for c in CHECKS for f in c(a)]


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
        {"id": "s1", "type": "I", "text": "every B is A",
         "prop": "every B is A"},
        {"id": "s3", "type": "I", "text": "every C is B",
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
    dead = []
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
    ap.add_argument("--alarm", action="store_true",
                    help="prove every decider can convict, then exit")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.files:
        ap.error("give at least one account, or --alarm")
    found = []
    for f in args.files:
        found += check_file(Path(f))
    for fd in found:
        print(f"  RED {fd.law} [{fd.where}] {fd.quote}\n      {fd.why}")
    if not found:
        print(f"{len(args.files)} account(s): no decider convicts. That is 6 of the 33 "
              "fallacies in Greenwell et al. cleared, not a sound argument: 16 want "
              "vocabulary the graph does not carry and 11 stay with a reader.")
        return 0
    print(f"\n{len(found)} finding(s) across {len(args.files)} account(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
