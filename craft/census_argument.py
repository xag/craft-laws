"""The fourth cost-blind census: every fallacy in the safety-argument taxonomy.

Greenwell, Holloway and Knight surveyed five general fallacy taxonomies, then read
three industrial safety cases to see which fallacies actually occur, and consolidated
the result into 33 fallacies in 8 categories (DSN 2005, Table 6). It is the closest
published thing to this estate's subject: claims that a system is adequately safe,
supported by evidence, reviewed by somebody who was not there.

The question this census answers is NOT "are these good rules". It is: **if an
argument were drawn as a graph — AIF's I-nodes and S-nodes, or GSN's goals,
strategies and solutions — which of these 33 could a check decide from the drawing,
and which need something the drawing does not carry?** That is the same question the
RGAA and WCAG censuses ask of the interface twin, asked of an argument twin, and the
route names are theirs unchanged.

  covered  an existing law or existing machinery already decides it
  zero     decidable from the argument graph with no new vocabulary
  vocab    needs a fact the graph does not carry (a typed scheme, a quantity, a
           part-whole relation, a glossary link)
  judge    stays with a reader

THE PRIOR ART SAYS WHERE THE LINE FALLS, and it is not encouraging. Yuan, Manandhar,
Kelly and Wells built this in 2016 over GSN and reported the boundary directly: "the
representation treats the content inside each GSN node as black-box and as a result
any argument flaws related to the content of the element cannot be detected by an
automatic means". Their fix was predicate logic inside the nodes, with an ontology
built by domain analysis of one safety case — hand-authored, per domain. Every `vocab`
row below is a row that lands on the far side of that boundary.

Read the tally before the rows. It is the evidence for or against
quality-harness's `an-argument-is-checkable-against-vocabularies-that-already-exist`,
and a census that flattered the hypothesis would be worth nothing.

    python -m craft.census_argument
    python -m craft.census_argument --vocab
"""

from __future__ import annotations

# The source's own list, in the source's own order and words (Table 6). Category
# headings are carried as comments, never as entries: the census unit is a fallacy.
CENSUS: dict[str, tuple[str, str]] = {
    # --- Circular Reasoning ----------------------------------------------------------
    "Circular Argument": ("zero", "a claim reasserted as its own premise is a cycle "
                                  "in the support graph — reachability, nothing else"),
    "Circular Definition": ("vocab", "needs the term's definition linked to its uses; "
                                     "interface@'s `term` kind is the shape, unbound "
                                     "to argument nodes today"),
    # --- Diversionary Arguments ------------------------------------------------------
    "Irrelevant Premise": ("judge", "relevance is a relation between meanings; the "
                                    "graph says a premise is attached, never whether "
                                    "it bears"),
    "Verbose Argument": ("judge", "excess irrelevant material — countable only once "
                                  "relevance is decided, so it inherits the row above"),
    # --- Fallacious Appeals ----------------------------------------------------------
    "Appeal to Common Practice": ("vocab", "the tell is the WARRANT's type; needs the "
                                           "inference scheme named on the S-node"),
    "Appeal to Improper/Anonymous Authority": ("vocab", "Yuan et al. detected exactly "
                                                        "this, and needed a database "
                                                        "of who is an expert in what"),
    "Appeal to Money": ("vocab", "scheme typing, as above"),
    "Appeal to Novelty": ("vocab", "scheme typing, as above"),
    "Association Fallacy": ("vocab", "scheme typing, as above"),
    "Genetic Fallacy": ("vocab", "scheme typing, as above"),
    # --- Mathematical Fallacies ------------------------------------------------------
    "Faith in Probability": ("vocab", "needs the number and what it was computed "
                                      "over; a Quantity on an evidence node"),
    "Gambler's Fallacy": ("vocab", "needs independence between the events, which no "
                                   "argument graph states"),
    "Insufficient Sample Size": ("vocab", "needs n on the evidence node; then it is a "
                                          "threshold"),
    "Pseudo-Precision": ("zero", "precision beyond what the measurement supports IS "
                                 "grounding@'s `tolerance` and `trusted_within` — the "
                                 "predicate exists, it wants an argument to run on"),
    "Unrepresentative Sample": ("judge", "whether the sample resembles the population "
                                         "is a claim about the world, not the graph"),
    # --- Unsupported Assertions ------------------------------------------------------
    "Arguing from Ignorance": ("zero", "a goal whose only support is the absence of "
                                       "counter-evidence — a solution set that is "
                                       "empty or negative"),
    "Unjustified Comparison": ("judge", "whether two things are alike enough to "
                                        "compare is not in the drawing"),
    "Unjustified Distinction": ("judge", "the converse, and equally not in it"),
    # --- Anecdotal Arguments ---------------------------------------------------------
    "Correlation Implies Causation": ("vocab", "needs the inference type on the "
                                               "S-node; Bradford Hill is the source "
                                               "for the criteria if it is ever built"),
    "Damning the Alternatives": ("zero", "support consisting only of attacks on the "
                                         "alternatives, and nothing standing on its "
                                         "own — this estate's `alternative` nodes with "
                                         "their `why` are that shape exactly"),
    "Destroying the Exception": ("judge", "whether an exception was legitimate is a "
                                          "reading"),
    "Destroying the Rule": ("judge", "the converse, and equally a reading"),
    "False Dichotomy": ("judge", "needs to know an option was omitted, which is a "
                                 "fact about the world and not about the graph"),
    # --- Omission of Key Evidence ----------------------------------------------------
    "Omission of Key Evidence": ("vocab", "needs a completeness reference — the set of "
                                          "evidence that SHOULD be there. The RGAA and "
                                          "WCAG censuses are that shape for interfaces"),
    "Fallacious Composition": ("vocab", "inferring a whole's property from its parts "
                                        "needs the part-whole relation stated"),
    "Fallacious Division": ("vocab", "the converse, and the same missing relation"),
    "Ignoring Available Counter-Evidence": ("zero", "refuting evidence present in the "
                                                    "graph and attached to nothing — a "
                                                    "CA-node with no edge is Dung's "
                                                    "input, unconsumed"),
    "Oversimplification": ("covered", "citing evidence from a MODEL without showing "
                                      "the model matches the system is what witness, "
                                      "walk and the drift check already refuse: a "
                                      "drawing is licensed by evidence, never trusted"),
    # --- Linguistic Fallacies --------------------------------------------------------
    "Ambiguity": ("judge", "two readings of one sentence; the drawing records the "
                           "reading somebody already chose"),
    "Equivocation": ("vocab", "one term, two meanings across the argument — needs "
                              "term-use tracking against a glossary; `term` and its "
                              "`strays` are the near miss"),
    "Suppressed Quantification": ("vocab", "'the tests pass' with no quantifier needs "
                                           "the quantifier as a fact on the claim"),
    "Vacuous Explanation": ("judge", "an explanation that explains nothing is read, "
                                     "not computed"),
    "Vagueness": ("judge", "as above, and the reason the reading residue exists"),
}

ROUTES = ("covered", "zero", "vocab", "judge")

# The source's own categories, in the source's own order, with the count it states.
CATEGORIES = ("Circular Reasoning", "Diversionary Arguments", "Fallacious Appeals",
              "Mathematical Fallacies", "Unsupported Assertions",
              "Anecdotal Arguments", "Omission of Key Evidence",
              "Linguistic Fallacies")
SOURCE_COUNT = 33


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_argument",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--vocab", action="store_true",
                    help="only the rows needing a fact the graph does not carry")
    args = ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the source's {SOURCE_COUNT} — a "
              "catalogue that claims to enumerate a source carries every item it lists")
        return 1

    if args.vocab:
        for name, (route, note) in CENSUS.items():
            if route == "vocab":
                print(f"  {name}: {note}")
        return 0

    tally = Counter(route for route, _ in CENSUS.values())
    decidable = tally["covered"] + tally["zero"]
    print(f"Greenwell, Holloway & Knight, the safety-argument fallacy taxonomy "
          f"(DSN 2005, Table 6): {len(CENSUS)} fallacies in {len(CATEGORIES)} "
          f"categories, all classified\n")
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    pct = round(100 * decidable / len(CENSUS))
    print(f"\n  decidable from the argument graph: {decidable} of {len(CENSUS)} "
          f"({pct}%).")
    print("  The rest split between a fact the graph does not carry and a reader.")
    print("  Yuan et al. 2016 predicted this shape: the graph decides STRUCTURE, and "
          "content\n  flaws need a per-domain ontology inside the nodes. This census "
          "counts the price.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
