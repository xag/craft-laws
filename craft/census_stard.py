"""The fourth practice census: every item of STARD 2015, none skipped.

STARD 2015 rooted a-rate-names-the-population-it-was-computed-over, and one item of a
thirty-item checklist is not a reading of a source -- it is the item that happened to say
what was wanted. `a-census-is-read-from-its-source` exists because a catalogue filtered
by what was feasible to build reports the builder's hand. So the whole list is here.

THE ANALOGY, stated once and applied throughout. A diagnostic accuracy study asks how
well a test identifies a condition, against a reference standard, in a population. A
CHECK in this estate asks the same question with different words: how well a decider
identifies a defect, against a person's ruling, over a corpus. Every STARD item is read
as a demand on a check's report, and where the analogy does not carry, the item is SET
ASIDE and says so -- an item ruled out is a number too.

  covered      an existing law or existing machinery already demands it
  owed         the demand carries and nothing here makes it; a law candidate
  set aside    clinical or publishing machinery with no counterpart in a check

The checklist is quoted from the EQUATOR-hosted STARD 2015 checklist; the rationale for
each item is Cohen et al., BMJ Open 2016;6:e012799.

    python -m craft.census_stard
    python -m craft.census_stard --owed
"""

from __future__ import annotations

# item -> (route, the source's own words, what it means for a check)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- title and abstract ----------------------------------------------------------
    "1": ("set aside", "Identification as a study of diagnostic accuracy using at least "
          "one measure of accuracy",
          "how a paper announces itself in a database; a check is not indexed"),
    "2": ("set aside", "Structured summary of study design, methods, results, and "
          "conclusions",
          "abstract format"),
    # --- introduction ----------------------------------------------------------------
    "3": ("covered", "Scientific and clinical background, including the intended use and "
          "clinical role of the index test",
          "what the check is for and where it applies — a-law-is-switched-on-by-something "
          "makes the trigger mandatory"),
    "4": ("covered", "Study objectives and hypotheses",
          "the falsifier, stated before the evidence arrives; the hypothesis and "
          "kill-criterion kinds carry it and a-hypothesis-is-falsifiable enforces it"),
    # --- methods: study design -------------------------------------------------------
    "5": ("owed", "Whether data collection was planned before the index test and "
          "reference standard were performed (prospective study) or after (retrospective)",
          "whether the check's expectation was formed before its output was seen. An "
          "expectation written after the answer agrees with whatever happened; nothing "
          "here demands a check say which it did"),
    # --- methods: participants -------------------------------------------------------
    "6": ("covered", "Eligibility criteria",
          "which items the check can convict — a-rate-names-the-population-it-was-"
          "computed-over, the law this source rooted"),
    "7": ("owed", "On what basis potentially eligible participants were identified",
          "how the corpus a check ran over was assembled. A check reporting findings "
          "over a corpus somebody chose reports the choosing as much as the corpus"),
    "8": ("covered", "Where and when potentially eligible participants were identified "
          "(setting, location and dates)",
          "sightings-name-the-app: the app's name and the date stay on the evidence, "
          "because evidence anonymised cannot be asked 'did this really happen'"),
    "9": ("owed", "Whether participants formed a consecutive, random or convenience "
          "series",
          "THE COST-BLIND CENSUS DOCTRINE, unstated as a law. This package learned it "
          "the hard way — the convergence series was impeached because 'the miner picked "
          "laws it could see the compile route for' — and the remedy became a habit "
          "rather than a rule. The habit has no falsifier"),
    # --- methods: test methods -------------------------------------------------------
    "10a": ("owed", "Index test, in sufficient detail to allow replication",
            "a check's own predicate, published well enough that somebody else could "
            "run it and get the same verdict"),
    "10b": ("owed", "Reference standard, in sufficient detail to allow replication",
            "what the check is measured AGAINST — the ruling that says a finding was "
            "real. rulings.py records verdicts; nothing requires the standard be stated "
            "before a check claims accuracy against it"),
    "11": ("owed", "Rationale for choosing the reference standard (if alternatives "
           "exist)",
           "why a person's ruling is the ground truth rather than some other test"),
    "12a": ("owed", "Definition of and rationale for test positivity cut-offs or result "
            "categories of the index test, distinguishing pre-specified from exploratory",
            "every threshold a decider carries — 25 words, five sentences, six words for "
            "a run-in label — and whether it was set before or after seeing what it "
            "caught. The six-word bound was set after"),
    "12b": ("set aside", "Definition of and rationale for test positivity cut-offs or "
            "result categories of the reference standard",
            "a person's ruling has no cut-off; it is the standard"),
    "13a": ("owed", "Whether clinical information and reference standard results were "
            "available to the performers/readers of the index test",
            "blinding. Whether the decider's author knew the answer while writing it — "
            "and the alarm corpora in this package were written by the same hand as the "
            "deciders they exercise"),
    "13b": ("owed", "Whether clinical information and index test results were available "
            "to the assessors of the reference standard",
            "whether the person ruling saw the check's verdict first. The adjudicator "
            "reads the finding before ruling on it, always, and that is not recorded "
            "anywhere as a limitation"),
    # --- methods: analysis -----------------------------------------------------------
    "14": ("set aside", "Methods for estimating or comparing measures of diagnostic "
           "accuracy",
           "statistical machinery for a paper; a check's arithmetic is its code"),
    "15": ("owed", "How indeterminate index test or reference standard results were "
           "handled",
           "what a decider does when it cannot decide. The convention here is convict "
           "with certainty or stay silent, and silence is indistinguishable from a clean "
           "corpus unless the report says how much it could not judge"),
    "16": ("owed", "How missing data on the index test and reference standard were "
           "handled",
           "harness.check reports an unreadable ledger as UNKNOWN rather than gone, "
           "which is exactly this item obeyed — as a decision in one module, not as a "
           "law any other check inherits"),
    "17": ("set aside", "Any analyses of variability in diagnostic accuracy, "
           "distinguishing pre-specified from exploratory",
           "subgroup analysis; no counterpart"),
    "18": ("owed", "Intended sample size and how it was determined",
           "how much corpus a check was calibrated on, decided before running it. The "
           "first version of the turn checker calibrated on one session with one hit and "
           "reported zero false positives"),
    # --- results: participants -------------------------------------------------------
    "19": ("covered", "Flow of participants, using a diagram",
           "the item that rooted a-rate-names-the-population-it-was-computed-over: the "
           "diagram exists so a reader can find the correct denominator"),
    "20": ("set aside", "Baseline demographic and clinical characteristics of "
           "participants",
           "who the patients were; a corpus has no demographics"),
    "21a": ("set aside", "Distribution of severity of disease in those with the target "
            "condition",
            "clinical severity; no counterpart"),
    "21b": ("set aside", "Distribution of alternative diagnoses in those without the "
            "target condition",
            "clinical differential; no counterpart"),
    "22": ("set aside", "Time interval and any clinical interventions between index test "
           "and reference standard",
           "clinical timing; no counterpart"),
    # --- results: test results -------------------------------------------------------
    "23": ("owed", "Cross tabulation of the index test results by the results of the "
           "reference standard",
           "THE CONFUSION MATRIX. A check reports what it caught and never what it "
           "missed or wrongly convicted. The turn checker recorded '18 candidates over "
           "158 turns, all cleared' and said in the same breath that its false-negative "
           "rate was unmeasured — which is this item, obeyed once, by hand, in prose"),
    "24": ("covered", "Estimates of diagnostic accuracy and their precision (such as 95% "
           "confidence intervals)",
           "grounding@'s Quantity carries tolerance and grounded, and "
           "a-qualifier-is-licensed-by-the-evidence refuses a bare number where the "
           "evidence does not settle it"),
    "25": ("set aside", "Any adverse events from performing the index test or the "
           "reference standard",
           "harm from testing a patient; a check harms nobody"),
    # --- discussion ------------------------------------------------------------------
    "26": ("covered", "Study limitations, including sources of potential bias, "
           "statistical uncertainty, and generalisability",
           "the `gap` field on grounds, and a-remainder-names-its-debt: what a "
           "done-claim leaves undone is carried by a debt it names"),
    "27": ("set aside", "Implications for practice, including the intended use and "
           "clinical role of the index test",
           "a discussion section; the trigger already states where a law applies"),
    # --- other information -----------------------------------------------------------
    "28": ("set aside", "Registration number and name of registry",
           "trial pre-registration; the ledger is the register and it is in the repo"),
    "29": ("set aside", "Where the full study protocol can be accessed",
           "as above — the protocol is the code"),
    "30": ("set aside", "Sources of funding and other support; role of funders",
           "conflict-of-interest disclosure; no counterpart"),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_ROWS = 34


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_stard",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--owed", action="store_true",
                    help="only the items whose demand carries and is unmet")
    args = ap.parse_args(argv)

    if len(CENSUS) != SOURCE_ROWS:
        print(f"the census carries {len(CENSUS)} of the checklist's {SOURCE_ROWS} rows")
        return 1

    if args.owed:
        for item, (route, quote, means) in CENSUS.items():
            if route == "owed":
                print(f"  {item:4} {quote}")
                print(f"       -> {means}\n")
        return 0

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"STARD 2015, every row of the checklist: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    print(f"\n  One item rooted a law. {tally['owed']} more carry to a check and are "
          f"unmet;\n  {tally['set aside']} are clinical or publishing machinery with no "
          f"counterpart.\n  Run --owed for the list, which is the law queue this source "
          f"actually offers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
