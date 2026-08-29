"""The fifth practice census: every cognitive disposition to respond in Croskerry 2003,
none skipped.

The source is Croskerry P., The Importance of Cognitive Errors in Diagnosis and
Strategies to Minimize Them, Academic Medicine 78(8):775-780, August 2003 — List 1, the
catalogue of cognitive dispositions to respond (CDRs), captured whole at
docs/sources/croskerry-2003-cognitive-errors.pdf (text extraction beside it). It is the
closest published taxonomy to the errors an agent actually makes in this estate:
diagnostic work under uncertainty, where the failure is rarely a wrong deduction and
usually a disposition — locking onto the first theory, calling off the search at the
first find, closing before verifying.

THE ANALOGY, stated once and applied throughout. A physician diagnoses a patient from
signs, tests and history; an agent here diagnoses a system from symptoms, checks and
tapes, and reports work with a confidence grade. Every CDR is read as a disposition the
agent can exhibit in that work, and where the analogy does not carry, the row is SET
ASIDE and says so — an item ruled out is a number too.

  covered      an existing law or decider already targets the disposition
  owed         the disposition carries to this estate's work and nothing fires on it;
               a law candidate
  set aside    clinical or interpersonal machinery with no counterpart in an agent's
               work here

This census was commissioned by the 2026-08-29 session that found the estate's heaviest
checker (Z3 entailment) guarding an error class observed zero times in fifteen filed
accounts, while the session's two costliest errors — a vacuous check trusted, a silent
instrument believed — belonged to dispositions this list names (search satisfying,
premature closure, overconfidence). The census exists so the next decider is aimed by
frequency, not by what was feasible to build.

    python -m craft.census_croskerry
    python -m craft.census_croskerry --owed
"""

from __future__ import annotations

from collections import Counter

# CDR -> (route, the source's own words (opening clause), what it means for the work)
CENSUS: dict[str, tuple[str, str, str]] = {
    "aggregate-bias": (
        "owed",
        "when physicians believe that aggregated data, such as those used to develop "
        "clinical practice guidelines, do not apply to individual patients",
        "'this project is the exception, the general rule does not apply here' — a law "
        "or convention waved off for the case in hand without evidence of atypicality. "
        "Nothing fires when an agent exempts the current repo from an estate rule"),
    "anchoring": (
        "covered",
        "the tendency to perceptually lock onto salient features in the patient's "
        "initial presentation too early in the diagnostic process",
        "locking onto the first theory. instrument-before-the-second-theory forces an "
        "observation between theories, and a-hunt-narrows-the-space demands the search "
        "shrink rather than orbit the first idea"),
    "ascertainment-bias": (
        "covered",
        "occurs when a physician's thinking is shaped by prior expectation",
        "a corpus assembled by expectation reports the expectation — "
        "a-corpus-names-its-assembly and a-corpus-of-reports-carries-its-reporting-bias "
        "make the assembly and its bias declarable"),
    "availability": (
        "owed",
        "the disposition to judge things as being more likely, or frequently "
        "occurring, if they readily come to mind",
        "the recently-seen failure shape diagnosed again because it is recent, not "
        "because it is likely. The base-rate law weighs how often a cause occurs; "
        "nothing weighs whether the agent's likelihood came from recency"),
    "base-rate-neglect": (
        "covered",
        "the tendency to ignore the true prevalence of a disease, either inflating or "
        "reducing its base-rate, and distorting Bayesian reasoning",
        "a-cause-is-weighed-by-how-often-not-only-how-alike — the diagnosis kind "
        "carries base_rate and the decider convicts resemblance without it"),
    "commission-bias": (
        "owed",
        "the tendency toward action rather than inaction",
        "the unrequested fix: editing what was not asked, widening scope because "
        "acting feels like progress. The estate forbids it in prose (the requested "
        "scope is the deliverable) and no check fires on a diff wider than its ask"),
    "confirmation-bias": (
        "covered",
        "the tendency to look for confirming evidence to support a diagnosis rather "
        "than look for disconfirming evidence to refute it",
        "counter-evidence-is-answered in the account lane; make-it-fail-before-you-"
        "fix-it forces the disconfirming observation first; a falsifier is the "
        "refuting shape stated in advance"),
    "diagnosis-momentum": (
        "owed",
        "once diagnostic labels are attached to patients they tend to become stickier "
        "and stickier",
        "a theory hardening as it is restated across turns and records until nobody "
        "re-derives it. The ledger records decisions with grounds, but nothing "
        "notices a hypothesis cited as fact after enough repetitions"),
    "feedback-sanction": (
        "covered",
        "Making a diagnostic error may carry no immediate consequences, as "
        "considerable time may elapse before the error is discovered",
        "the reason sightings, claims and tapes exist: the error's consequence is "
        "routed back to its author's record. The claims ledger is the calibration "
        "loop the source says is missing"),
    "framing-effect": (
        "owed",
        "how diagnosticians see things may be strongly influenced by the way in which "
        "the problem is framed",
        "the bug report's own words steering the investigation; an ambiguous "
        "conclusion carrying two readings (this session's existence-vs-runnable-now). "
        "No check reads a conclusion for the frames it smuggles"),
    "fundamental-attribution-error": (
        "set aside",
        "the tendency to be judgmental and blame patients for their illnesses",
        "blaming persons for circumstances; the near analogue — blaming the user's "
        "report rather than reading the tape — is carried by "
        "the-systems-own-record-is-read-first, and the interpersonal core has no "
        "counterpart here"),
    "gamblers-fallacy": (
        "set aside",
        "the belief that if a coin is tossed ten times and is heads each time, the "
        "11th toss has a greater chance of being tails",
        "expecting independent events to compensate; the diagnostic work here rarely "
        "presents runs of independent identical cases, and the sequence-continuation "
        "twin is routed at posterior-probability-error"),
    "gender-bias": (
        "set aside",
        "the tendency to believe that gender is a determining factor in the "
        "probability of diagnosis of a particular disease when no such "
        "pathophysiological basis exists",
        "demographic stereotyping of patients; no counterpart in judging checks and "
        "code. Where a fairness question arises in a product it is that product's "
        "domain, not this harness's"),
    "hindsight-bias": (
        "covered",
        "knowing the outcome may profoundly influence the perception of past events "
        "and prevent a realistic appraisal of what actually occurred",
        "prespecified-is-distinguished-from-exploratory and "
        "a-protocol-is-an-artifact-before-the-run: the expectation is an artifact "
        "dated before the outcome, so the after-the-fact story is checkable"),
    "multiple-alternatives-bias": (
        "owed",
        "a multiplicity of options on a differential diagnosis may lead to "
        "significant conflict and uncertainty",
        "reverting to the familiar three when the differential is wide — the "
        "candidate-fix shortlist that quietly drops the unfamiliar tail. "
        "structural-unknowns-are-considered is adjacent but fires on unknowns, not "
        "on a trimmed differential"),
    "omission-bias": (
        "owed",
        "the tendency toward inaction",
        "the unflagged remainder: work silently scaled down because acting felt "
        "riskier than skipping. a-remainder-names-its-debt covers the claim's text; "
        "nothing compares what was asked against what was delivered"),
    "order-effects": (
        "set aside",
        "information transfer is a U-function: we tend to remember the beginning "
        "part (primacy effect) or the end (recency effect)",
        "primacy and recency in human memory during handoffs; an agent's context "
        "loss is real but mechanically different (truncation, not U-shaped recall) "
        "and is routed in the MAST census at loss-of-conversation-history"),
    "outcome-bias": (
        "owed",
        "the tendency to opt for diagnostic decisions that will lead to good "
        "outcomes, rather than those associated with bad outcomes",
        "preferring the diagnosis that would be convenient — the flaky test, the "
        "stale cache — because the alternative means real work. No check weighs a "
        "diagnosis against the cost of its being true"),
    "overconfidence-bias": (
        "covered",
        "a universal tendency to believe we know more than we do. Overconfidence "
        "reflects a tendency to act on incomplete information, intuitions, or hunches",
        "the calibration family: a-qualifier-is-licensed-by-the-evidence, "
        "validity-is-evidence-and-agreement, low-confidence-is-reserved-and-explained, "
        "and the closed strength scale in accounts. This session's over-claimed "
        "deduction labels were this CDR and were convicted"),
    "playing-the-odds": (
        "owed",
        "the tendency in equivocal or ambiguous presentations to opt for a benign "
        "diagnosis on the basis that it is significantly more likely than a serious "
        "one",
        "'probably flaky' as the benign read of a red test. The base-rate law demands "
        "frequency for the cause named; nothing demands the serious alternative be "
        "priced before the benign one is filed"),
    "posterior-probability-error": (
        "covered",
        "occurs when a physician's estimate for the likelihood of disease is unduly "
        "influenced by what has gone on before for a particular patient",
        "the sixth headache diagnosed as the first five were — "
        "regression-is-the-null-after-an-extreme and the base-rate law both press "
        "the estimate back toward the population instead of the streak"),
    "premature-closure": (
        "covered",
        "the tendency to apply premature closure to the decision-making process, "
        "accepting a diagnosis before it has been fully verified",
        "'when the diagnosis is made, the thinking stops' — done-is-observed-where-"
        "the-user-stands and make-it-fail-before-you-fix-it exist for exactly this, "
        "and both convicted claims in this estate this month"),
    "psych-out-error": (
        "owed",
        "comorbid medical conditions may be overlooked or minimized",
        "the marginalized subject: the intermittent, environment-dependent failure "
        "dismissed as noise, where real defects hide behind the label already "
        "attached (flaky, known-issue). Nothing audits what the label excused"),
    "representativeness-restraint": (
        "owed",
        "the representativeness heuristic drives the diagnostician toward looking "
        "for prototypical manifestations of disease",
        "pattern-matching to the prototypical bug; the atypical variant missed "
        "because it does not look like its class. The base-rate law corrects the "
        "likeness weight but nothing prompts the atypical differential"),
    "search-satisfying": (
        "covered",
        "reflects the universal tendency to call off a search once something is "
        "found",
        "the first bug found ends the sweep; the second foreign body is missed. "
        "a-check-reports-its-misses demands the other row of the cross-tab, and "
        "a-check-reports-what-it-could-not-judge demands the unsearched remainder "
        "be named — this session's vacuous zero-node check was this CDR escaping "
        "both, because the ad-hoc check was not held to either law"),
    "suttons-slip": (
        "owed",
        "The slip occurs when possibilities other than the obvious are not given "
        "sufficient consideration",
        "going for the obvious cause without pricing the rest; the single-theory "
        "hunt. instrument-before-the-second-theory fires only once a second theory "
        "exists — the slip is stopping at the first"),
    "sunk-costs": (
        "owed",
        "the more clinicians invest in a particular diagnosis, the less likely they "
        "may be to release it and consider alternatives",
        "the fix iterated on for hours because abandoning it wastes the hours. "
        "a-resisting-failure-gets-fresh-eyes is the antidote law but keys on the "
        "failure resisting, not on the investment growing"),
    "triage-cueing": (
        "owed",
        "the triage process occurs throughout the health care system... Many CDRs "
        "are initiated at triage",
        "'geography is destiny': the issue's title, label or first assignment cueing "
        "everything downstream. Nothing re-derives whether the ticket's frame "
        "matches the evidence once work begins"),
    "unpacking-principle": (
        "covered",
        "failure to elicit all relevant information (unpacking) in establishing a "
        "differential diagnosis may result in significant possibilities being missed",
        "the history not taken: the-systems-own-record-is-read-first and "
        "the-baseline-assumption-is-verified both force the elicitation before the "
        "differential narrows"),
    "vertical-line-failure": (
        "owed",
        "routine, repetitive tasks often lead to thinking in silos — predictable, "
        "orthodox styles that emphasize economy, efficacy, and utility",
        "'what else might this be?' never asked; the orthodox procedure run because "
        "it is the procedure. No check prompts the lateral question on a stuck hunt"),
    "visceral-bias": (
        "owed",
        "the influence of affective sources of error on decision-making has been "
        "widely underestimated",
        "sycophancy is this CDR in an agent: the user's frustration or enthusiasm "
        "steering the verdict. a-view-moves-on-observation-not-on-company convicts "
        "the moved view when filed; nothing watches the unfiled agreement"),
    "yin-yang-out": (
        "set aside",
        "when patients have been subjected to exhaustive and unavailing diagnostic "
        "investigations, they are said to have been worked up the Yin-Yang",
        "abandoning diagnosis because everything was tried; the near analogue — a "
        "stopped hunt saying why — is already law (a-stopped-run-says-why), and the "
        "exhausted-workup social dynamic has no further counterpart"),
}

SOURCE_ROWS = 32
ROUTES = ("covered", "owed", "set aside")


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--owed", action="store_true",
                    help="only the dispositions that carry and are unmet")
    args = ap.parse_args(argv)

    if len(CENSUS) != SOURCE_ROWS:
        print(f"the census carries {len(CENSUS)} of the source's {SOURCE_ROWS} CDRs")
        return 1

    if args.owed:
        for item, (route, quote, means) in CENSUS.items():
            if route == "owed":
                print(f"  {item}")
                print(f"       -> {means}\n")
        return 0

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Croskerry 2003, every CDR of List 1: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    print()
    print(f"  {tally['covered']} carry to the work and a law covers each; "
          f"{tally['owed']} are owed;")
    print(f"  {tally['set aside']} are clinical or interpersonal machinery with no "
          f"counterpart.")
    print("  Run --owed for the queue — it is the law-candidate list, to be drained "
          "by frequency, not by buildability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
