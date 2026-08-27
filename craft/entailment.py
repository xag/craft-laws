"""Validity decided by a theorem prover, not by rules written here.

THE FOURTH TIME, and the owner caught each one.

  1. `scheme: "deduction"`            one label, checked by nothing.
  2. `mood: "AAA", figure: 2`         two labels; one digit flipped the verdict.
  3. `prop: {"quantity": ...}`        four labels, a record typed by hand.
  4. an EBNF docstring beside a hand-rolled tokenizer, and five distribution rules
     I wrote out myself. The grammar was decoration -- nothing executed it -- and the
     "decision procedure" was Aristotle transcribed by me, which is exactly the kind
     of artifact this estate refuses everywhere else.

So: the grammar is now a Lark file that Lark executes (craft/categorical.lark), and
validity is decided by Z3. Nothing in this module knows what a syllogism is. It
translates each parsed proposition into first-order logic and asks the solver whether
the premises entail the conclusion:

    every S is P   ->  ForAll x. S(x) -> P(x)
    no    S is P   ->  ForAll x. S(x) -> Not P(x)
    some  S is P   ->  Exists x. S(x) & P(x)
    some  S is not P   ->  Exists x. S(x) & Not P(x)

An argument is valid when premises AND NOT conclusion is UNSATISFIABLE. That is the
definition of entailment, and Z3 answers it.

EXISTENTIAL IMPORT FALLS OUT INSTEAD OF BEING CODED. The medieval 24 and the modern 15
differ because Darapti and its kin need every term to name something. Here that is an
AXIOM the caller may add -- Exists x. T(x) for each term -- not a flag in a hand-written
rule. The disagreement becomes a premise, which is what it always was.

This module knows nothing about figures, moods, or the four Aristotelian forms beyond
the translation above. Feed it propositions that form no syllogism at all and it still
answers, because entailment is a more general question than syllogistic validity.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Entailment:
    valid: bool
    counter_model: str = ""
    terms: tuple = field(default_factory=tuple)


def _sorted_terms(props) -> list[str]:
    seen = []
    for p in props:
        for t in (p.subject, p.predicate):
            if t not in seen:
                seen.append(t)
    return seen


def entails(premises, conclusion, nonempty_terms: bool = False) -> Entailment:
    """Do the premises entail the conclusion? Decided by Z3 over first-order logic.

    `nonempty_terms` adds `Exists x. T(x)` for every term, which is the existential-
    import reading. It is an axiom, not a special case."""
    import z3

    props = list(premises) + [conclusion]
    terms = _sorted_terms(props)
    U = z3.DeclareSort("U")
    pred = {t: z3.Function(f"P{i}", U, z3.BoolSort()) for i, t in enumerate(terms)}
    x = z3.Const("x", U)

    def render(p):
        s, q = pred[p.subject], pred[p.predicate]
        body = q(x) if p.quality == "affirmative" else z3.Not(q(x))
        if p.quantity == "all":
            return z3.ForAll([x], z3.Implies(s(x), body))
        return z3.Exists([x], z3.And(s(x), body))

    solver = z3.Solver()
    for p in premises:
        solver.add(render(p))
    if nonempty_terms:
        for t in terms:
            solver.add(z3.Exists([x], pred[t](x)))
    solver.add(z3.Not(render(conclusion)))

    result = solver.check()
    if result == z3.unsat:
        return Entailment(True, terms=tuple(terms))
    if result == z3.sat:
        return Entailment(False, counter_model=str(solver.model()),
                          terms=tuple(terms))
    return Entailment(False, counter_model=f"the solver returned {result}",
                      terms=tuple(terms))
