"""The account family's laws: every one rooted in a source adopted WHOLE, or absent.

THE RULE THIS FILE EXISTS TO ENFORCE, set by the owner on 2026-08-27: no rule is ever
added by hand or ad hoc, and no rule is adopted in isolation -- when a source is
adopted, all of it is fetched and censused, and the laws mechanized here are exactly
the rows the census routes as decidable. tests/test_law_registry.py is the gate: an
account decider convicting under an id this registry does not carry, a registered law
without a fetched citation, or a law claiming a census row the census routes to a
reader, turns CI red.

THE SOURCES, each adopted whole:

  Greenwell, Knight, Holloway & Pease 2006 (ISSC; the DSN 2005 taxonomy) -- 33
      fallacies, all censused in craft/census_argument.py with a route each; the paper
      is captured at docs/sources/greenwell-knight-holloway-pease-2006.pdf. The laws
      below are its graph-decidable rows and nothing more.
  Aristotle, Prior Analytics (Jenkinson tr.) -- the categorical forms; the whole
      catalogue is decided, all 256 mood/figure pairs, by craft/entailment.py, and the
      15/24 cross-check in tests is that census.
  SEP, Logical Consequence (Beall, Restall & Sagi) -- the model-theoretic definition
      Z3 decides; total by construction, nothing to cherry-pick.
  IPCC AR5 uncertainty guidance (Mastrandrea et al. 2010) -- adopted by the practice
      family; the account deciders REUSE its law ids rather than minting doubles:
      calibration-is-agreed-before-the-case and a-qualifier-is-licensed-by-the-evidence
      convict here too, under the practice family's own citations.
  AIF (Chesnevar et al. 2006) -- the graph ontology. Its citation is the estate's
      captured reading in quality-harness/harness/argument.py, marked as such: the
      paper's own sentence has not been fetched, and the provenance says so rather
      than dressing a paraphrase as a quotation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from craft.practice import IPCC, IPCC_URL

GREENWELL = ("Greenwell, Knight, Holloway & Pease, A Taxonomy of Fallacies in System "
             "Safety Arguments (2006; captured at "
             "docs/sources/greenwell-knight-holloway-pease-2006.pdf)")
GREENWELL_URL = "https://ntrs.nasa.gov/api/citations/20060027794/downloads/20060027794.pdf"

ARISTOTLE = "Aristotle, Prior Analytics, tr. A. J. Jenkinson"
ARISTOTLE_URL = "https://classics.mit.edu/Aristotle/prior.1.i.html"

SEP_LC = "Stanford Encyclopedia of Philosophy, Logical Consequence, section 3.1"
SEP_LC_URL = "https://plato.stanford.edu/entries/logical-consequence/"

AIF = ("Chesnevar et al. 2006, the Argument Interchange Format, as recorded in the "
       "estate's implementation (quality-harness/harness/argument.py) -- an estate "
       "capture, not the paper's own sentence")
AIF_URL = "https://github.com/xag/quality-harness"


@dataclass(frozen=True)
class AccountLaw:
    id: str
    statement: str
    source: str
    source_item: str                     # the catalogue row this law mechanizes
    citations: tuple = field(default_factory=tuple)   # (source, url, verbatim quote)


ACCOUNT = (
    AccountLaw(
        "an-account-is-an-aif-graph",
        "An account is an AIF graph in this format: I-nodes carry propositions, RA and "
        "CA nodes carry inference and conflict, and what the format does not admit -- "
        "an unknown node type, an edge to no node, a declared mood or figure -- is not "
        "an account",
        source=AIF, source_item="I-node / S-node ontology",
        citations=((AIF, AIF_URL,
                    "an argument graph has I-NODES carrying propositional information "
                    "and S-NODES carrying the application of a scheme -- RA for "
                    "inference, CA for conflict, PA for preference. Edges run between "
                    "them; an I-node never points straight at another I-node."),),
    ),
    AccountLaw(
        "a-proposition-is-in-the-language",
        "A proposition offered for entailment is a sentence of the categorical "
        "language, parsed against craft/categorical.lark; what the grammar refuses is "
        "not a proposition",
        source=ARISTOTLE, source_item="the four categorical forms",
        citations=((ARISTOTLE + ", I.1", ARISTOTLE_URL,
                    "A syllogism is discourse in which, certain things being stated, "
                    "something other than what is stated follows of necessity from "
                    "their being so."),),
    ),
    AccountLaw(
        "the-premises-entail-the-conclusion-or-they-do-not",
        "A declared deduction is decided by the model-theoretic definition: Z3 asks "
        "whether any model makes the premises true and the conclusion false, and "
        "reports the counter-model when one exists",
        source=SEP_LC, source_item="the model-theoretic account",
        citations=((SEP_LC, SEP_LC_URL,
                    "an argument is valid if in any model in which the premises are "
                    "true (or in any interpretation of the premises according to which "
                    "they are true), the conclusion is true too."),
                   (GREENWELL + ", p.5", GREENWELL_URL,
                    "Formal and syllogistic fallacies, which occur in deductive "
                    "arguments, are unlikely to appear in safety arguments because "
                    "purely deductive arguments may be expressed formally and "
                    "verified mechanically."),),
    ),
    AccountLaw(
        "no-claim-supports-itself",
        "A claim reasserted as its own premise, directly or through the support graph, "
        "is a circular argument",
        source=GREENWELL, source_item="Circular Argument",
        citations=((GREENWELL + ", p.7", GREENWELL_URL,
                    "Circular reasoning occurs when an argument is structured so that "
                    "it reasserts its claim as a premise or defines a key term in a "
                    "way that makes its claim trivially true."),),
    ),
    AccountLaw(
        "a-conclusion-names-its-warrant",
        "A conclusion no inference concludes is an unsupported assertion, not an "
        "argument",
        source=GREENWELL, source_item="Unsupported Assertions",
        citations=((GREENWELL + ", p.7", GREENWELL_URL,
                    "Unsupported assertions are claims stated without evidence."),),
    ),
    AccountLaw(
        "absence-of-evidence-concludes-nothing",
        "A conclusion warranted only by the absence of counter-evidence convicts -- "
        "unless a grounded premise documents the search that turned up none, which is "
        "the source's own exemption",
        source=GREENWELL, source_item="Arguing from Ignorance",
        citations=((GREENWELL + ", Figure 2", GREENWELL_URL,
                    "An argument supports a claim by citing a lack of evidence that "
                    "the claim is false. The argument does not exhibit the fallacy if "
                    "it cites as evidence a sufficiently-exhaustive search for "
                    "counter-evidence that has turned up none."),),
    ),
    AccountLaw(
        "counter-evidence-is-answered",
        "A conclusion is flawed while a well-formed attack on it, or on anything "
        "transitively supporting it, stands unanswered - answered meaning the "
        "attacker is itself attacked (Dung's defense)",
        source=GREENWELL, source_item="Ignoring Available Counter-Evidence",
        citations=((GREENWELL + ", p.7", GREENWELL_URL,
                    "An argument ignores available counter-evidence when it makes a "
                    "claim for which there exists refuting evidence but fails to "
                    "address that evidence."),),
    ),
    AccountLaw(
        "a-conclusion-stands-on-its-own-feet",
        "Support consisting only of attacks on the alternatives, with nothing standing "
        "on its own, damns the alternatives instead of arguing",
        source=GREENWELL, source_item="Damning the Alternatives",
        citations=((GREENWELL + ", Table 6 and p.7", GREENWELL_URL,
                    "Anecdotal arguments show that their claims hold in some "
                    "circumstances but fail to generalize their validity."),),
    ),
    AccountLaw(
        "a-ground-is-a-quotation-from-the-record",
        "A grounded premise quotes, verbatim, the turn's own record -- the traceable "
        "account, mechanized: tool results for producer and stand-in, the user's "
        "messages for given and user-surface; a quote the record does not hold, or no "
        "record to check against, convicts",
        source=IPCC, source_item="paragraph 2, the traceable account",
        citations=((IPCC + ", paragraph 2", IPCC_URL,
                    "Be prepared to make expert judgments in developing key findings, "
                    "and to explain those judgments by providing a traceable account: "
                    "a description in the chapter text of your evaluation of the "
                    "type, amount, quality, and consistency of evidence and the "
                    "degree of agreement, which together form the basis for a given "
                    "key finding."),),
    ),
)

# Practice-family law ids the account deciders also convict under. They are not
# re-registered here -- one law, one home -- but the gate verifies they exist in
# craft.practice with citations, so a rename there goes red here.
PRACTICE_REUSED = ("calibration-is-agreed-before-the-case",)

# Which census rows of the whole-source adoption these laws mechanize. The gate holds
# this mapping against craft.census_argument.CENSUS: the row must exist, and its route
# must be one the census says is decidable from the graph.
GREENWELL_ROWS = {
    "no-claim-supports-itself": "Circular Argument",
    "absence-of-evidence-concludes-nothing": "Arguing from Ignorance",
    "counter-evidence-is-answered": "Ignoring Available Counter-Evidence",
    "a-conclusion-stands-on-its-own-feet": "Damning the Alternatives",
}
