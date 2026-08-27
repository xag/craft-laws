"""The fifth cost-blind census: every fallacy in Aristotle's Sophistical Refutations.

The founding catalogue -- thirteen fallacies, stated by the author as a complete
enumeration, fetched verbatim from the Pickard-Cambridge translation
(classics.mit.edu/Aristotle/sophist_refut.html). Adopted WHOLE per the estate's
sourcing rule: every row is here with a route, and the laws mechanized in
craft/account.py are exactly the rows routed decidable, no more.

  covered  existing machinery already decides it
  zero     decidable from the account graph with no new vocabulary
  vocab    needs a fact the graph does not carry
  judge    stays with a reader

The routes are one reader's application of the criterion the owner set on
2026-08-27 -- a rule detects a reasoning flaw, never demands paperwork -- and
tests/test_law_registry.py holds the account laws to this table.
"""

from __future__ import annotations

SOURCE = ("Aristotle, On Sophistical Refutations, tr. W. A. Pickard-Cambridge "
          "(classics.mit.edu)")
SOURCE_URL = "https://classics.mit.edu/Aristotle/sophist_refut.1.1.html"
SOURCE_COUNT = 13

# The enumeration, verbatim from the text:
#   dependent on language: "They are ambiguity, amphiboly, combination, division of
#   words, accent, form of expression."
#   independent of language: "there are seven kinds: (1) that which depends upon
#   Accident: (2) the use of an expression absolutely or not absolutely but with some
#   qualification of respect or place, or time, or relation: (3) that which depends
#   upon ignorance of what 'refutation' is: (4) that which depends upon the
#   consequent: (5) that which depends upon assuming the original conclusion:
#   (6) stating as cause what is not the cause: (7) the making of more than one
#   question into one."

CENSUS = {
    # -- dependent on language: the account carries controlled propositions, not the
    #    natural prose these fallacies live in; they stay with a reader of the reply.
    #    The one structural surface: an equivocated middle term is FOUR terms, and
    #    craft/syllogism.derive already refuses premises that never meet.
    "Ambiguity": ("judge", "same word, two senses -- meaning; the four-term surface "
                           "of an equivocated middle is covered by derive()"),
    "Amphiboly": ("judge", "syntactic ambiguity in natural prose"),
    "Combination": ("judge", "words true separately, combined falsely -- meaning"),
    "Division of words": ("judge", "the converse of combination -- meaning"),
    "Accent": ("judge", "spoken emphasis; nothing the account carries"),
    "Form of expression": ("judge", "grammatical form suggesting a wrong category"),
    # -- independent of language
    "Accident": ("judge", "predicating of the accident what holds of the subject -- "
                          "needs a sense of essential vs accidental no graph carries"),
    "Secundum quid": ("vocab", "absolute vs qualified assertion wants a qualifier "
                               "vocabulary the account does not carry; the claims "
                               "lane's gap fields are the nearest existing shape"),
    "Ignoratio elenchi": ("covered", "the RA names its conclusion and Z3 judges that "
                                     "conclusion; proving something else cannot pass "
                                     "as proving the named one"),
    "Consequent": ("covered", "supposing the relation of consequence convertible is "
                              "an invalid entailment, and Z3 refutes it with a "
                              "counter-model"),
    "Begging the question": ("covered", "assuming the original conclusion is "
                                        "no-claim-supports-itself"),
    "Non-cause as cause": ("zero", "a premise inserted as though the conclusion "
                                   "depended on it, when the verified entailment "
                                   "holds without it -- decidable by re-asking Z3 "
                                   "with the premise removed"),
    "Many questions": ("judge", "accounts carry no questions"),
}


def main() -> int:
    routes: dict[str, int] = {}
    for _, (route, _why) in CENSUS.items():
        routes[route] = routes.get(route, 0) + 1
    print(f"{SOURCE}: {len(CENSUS)} fallacies, the author's own complete enumeration")
    print()
    for r in ("covered", "zero", "vocab", "judge"):
        print(f"  {r:<8} {routes.get(r, 0)}")
    n = routes.get("covered", 0) + routes.get("zero", 0)
    print()
    print(f"  decidable from the account graph: {n} of {len(CENSUS)}.")
    if len(CENSUS) != SOURCE_COUNT:
        print(f"  DEAD: the census holds {len(CENSUS)} rows; the source states "
              f"{SOURCE_COUNT}.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
