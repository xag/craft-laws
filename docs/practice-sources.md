# The practice sources: where laws about the WORK come from

Surveyed 2026-08-22. The interface family was mined from a catalogue chosen deliberately ([sources.md](sources.md)); the practice family was not — it grew from defects, one session at a time, and cites nothing. Five of its laws stand red on `a-law-cites-a-source`. This is the catalogue that fixes that, ranked by the same two criteria, stated because they are the bias-guards: **authority** (standard, statute, or published empirical research — never fame) and **falsifiability** (can a breach be observed, or does the rule need interpretation?).

One difference from the interface catalogue is worth stating up front. There is no WCAG for the practice of building: no single body publishes numbered, testable rules about how an engineer should reason, claim or report. The authority here is spread across uncertainty communication, statistical reporting, plain language, safety engineering and human-factors research, and much of it is principle-shaped. Where a source needs interpretation, it is cited as a root and the law carries the falsifier — never the other way round.

## The mining shortlist, in order

1. **IPCC AR5 Guidance Note on Consistent Treatment of Uncertainties** (Mastrandrea et al., 2010) — 11 numbered paragraphs, 6 lettered criteria and two calibrated scales, written to stop authors picking a confidence term the evidence does not license. Publicly available, quotable, and unusually operational for a document about judgement. **Censused below.** https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf
2. **Eidelman, Crandall & Pattershall, "The existence bias"** (*Journal of Personality and Social Psychology* 97(5), 765–775, 2009) — five studies establishing that mere existence is taken as evidence of goodness, and that the effect appears in aesthetic judgment where no choice among alternatives was ever made. Published empirical research, which is the authority; the finding is about people rather than about work, so it roots a law and does not state one. **Censused below.** Full text paywalled; the census is read from the abstract, which enumerates the studies. https://doi.org/10.1037/a0017058
3. **Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules"** (*Communications of the ACM* 15(12), 1053–1058, 1972) — the foundational statement of where a thing belongs: decompose by the design decisions each part hides, never by the steps of processing. Freely available, quotable, and it gives an observable criterion rather than a principle. **Censused below.** https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf
4. **Agans, *Debugging: The 9 Indispensable Rules*** (2002) — already the root of four practice laws; nine rules, each a command with an observable breach. Copyrighted, so cite the rule name and quote briefly.
5. **STARD 2015** (Cohen et al., *BMJ Open* 2016;6:e012799; checklist hosted by the EQUATOR Network) — 30 numbered items, 34 rows, stating what a report of a diagnostic accuracy study must contain. A reporting standard for measurement claims, from a community that had to make them auditable because careers rest on them, and unusually falsifiable: each item is either present in a report or it is not. Already the root of `a-rate-names-the-population-it-was-computed-over`. **Censused whole:** `python -m craft.census_stard`. https://doi.org/10.1136/bmjopen-2016-012799
6. **Federal plain language guidelines** (Plain Writing Act 2010; canonical pages now under digital.gov) — statutory, public domain, sentence-level and checkable. Already source #10 of the interface catalogue; the practice family needs the parts about writing for a reader who is not you.
7. **ISO/IEC/IEEE 15289 and 26515** — what a work product must contain to be a record rather than a note. Paywalled: cite clause numbers, quote briefly.
8. **CONSORT / ARRIVE / STROBE reporting checklists** — the strongest available model for "a claim carries what it rests on", each item numbered and each breach observable in a manuscript. Free, widely adopted, and about reporting rather than about our subject matter, so they transfer by analogy and must be cited as such.
9. **Kahneman, Slovic & Tversky and successors on overconfidence and anchoring** — published empirical research, the root beneath IPCC paragraph 3. Principle-shaped; cite for the finding, never for a rule.
10. **NASA/ESA anomaly-reporting standards and the Swiss-cheese/HFACS literature** — the root for "instrument before the second theory" if one exists outside Agans. Not yet read.
11. **GOV.UK Service Manual** — "do the hard work to make it simple" and the service-assessment criteria; already the ancestor of much of the interface catalogue, and the plausible root for the laws about spending someone else's attention. Principle-shaped; the design system's numbered patterns are the falsifiable part.

Excluded despite fame, with reasons: **Clean Code / SOLID / most engineering-practice books** (assertions without an authority, and their empirical support is thin or contested); **Agile manifesto and derivatives** (values, not rules — nothing observable); **Google's SRE book** (excellent and specific to running services, not to claiming work done; CC BY-NC-ND).

## Gaps found

- **Nothing authoritative was found on delegating a decision.** The laws about spending a person's attention (`the-users-attention-is-not-a-test-harness`, and the one the corrections named about asking for a decision the evidence settles) have no obvious root. Automation-levels research (Parasuraman/Sheridan) describes the design space without prescribing; GOV.UK prescribes for services, not for a working relationship. Searched and thin — recorded as a boundary chosen, not one fallen into.
- **The longevity half is unread.** Eidelman, Pattershall & Crandall, "Longer is better" (*Journal of Experimental Social Psychology*, 2010, DOI 10.1016/j.jesp.2010.07.008) is the companion finding — the longer something is thought to have existed, the better it is judged. Elsevier, paywalled, and the abstract was not retrieved. Named here so its absence is a record rather than an oversight; the law it would strengthen cites only the 2009 paper.
- **Nothing was found on context leaking between records.** The interface family states it for strings (`no-cross-context-string-reuse`); the practice analogue — reasoning from one context written into another's record — is asserted from the estate's own rule that a library never names a client. Owed.

---

# Census: IPCC AR5 Guidance Note, read whole

Every item the source states, each mapped. `covered` — a law here carries it. `owed` — it applies to this practice and no law carries it yet. `set aside` — it is about the source's own subject (climate assessment) and does not transfer.

The Guidance Note states 11 numbered paragraphs, 6 lettered criteria (A–F) under paragraph 11, a 5-term confidence scale, a 10-term likelihood scale, and the evidence/agreement summary terms. That is **21 items**.

| # | What it states | Status |
|---|---|---|
| 1 | Consider, at an early stage, how to communicate the degree of certainty; agree the process in advance of the specific case | owed — the estate has no agreed calibration vocabulary, which is why each turn improvises one |
| 2 | Provide a *traceable account*: a description of the evaluation of type, amount, quality and consistency of evidence, and the degree of agreement, which together form the basis for the finding | covered — `done-is-observed-where-the-user-stands` demands the evidence beside the claim, and the claims ledger's `evidence.where` is the traceable account in data. Since 2026-08-24 also the root of the `confirmation` kind's decider: an agreement is a finding, and one filed with nothing in `checked` has no account, convicting under `a-qualifier-is-licensed-by-the-evidence` |
| 3 | Beware group convergence and overconfidence; beware anchoring on previous versions to a greater extent than is justified | owed — directly applicable to an agent that anchors on its own earlier turn, and nothing here carries it |
| 4 | Framing changes interpretation (10% chance of dying vs 90% of surviving); consider reciprocal statements | set aside — about presenting risk to a public, not about reporting work |
| 5 | **"Consider that, in some cases, it may be appropriate to describe findings for which evidence and understanding are overwhelming as statements of fact without using uncertainty qualifiers."** | **covered — `a-qualifier-is-licensed-by-the-evidence`** |
| 6 | Consider all plausible sources of uncertainty; experts tend to underestimate structural uncertainty from incomplete understanding | owed — the mirror of item 5 and the reason the law must cut both ways |
| 7 | Assess uncertainty and risk to the extent possible; attend to high-consequence outcomes | set aside — a risk-management instruction about the subject matter |
| 8 | Evaluate validity on two dimensions — evidence (limited/medium/robust) and agreement (low/medium/high) — and provide a traceable account of both | owed — the estate has one dimension (was it observed) and no vocabulary for agreement |
| 9 | Confidence is five qualifiers (very low → very high); low and very low confidence should be reserved for areas of major concern and the reasons explained; confidence is not probabilistic | owed — the scale itself does not transfer, but "reserve the low end and explain it" does |
| 10 | Likelihood is calibrated language for quantified uncertainty; where there is sufficient information it is preferable to give the probability directly rather than the term; "about as likely as not" must not stand in for a lack of knowledge | owed — the last clause transfers exactly: a hedge must not stand in for not having looked |
| 11 | Characterize findings using the language that conveys the most information, per criteria A–F | covered in part by item 5's law; the criteria are set aside individually below |
| 11-A | Ambiguous or unmeasurable variable: assign no confidence; give evidence and agreement terms | set aside |
| 11-B | Sign known, magnitude poorly known: assign confidence when possible | set aside |
| 11-C | Order of magnitude available: assign confidence; state assumptions | set aside |
| 11-D | A range can be given: assign likelihood for that range when possible | set aside |
| 11-E | A likelihood or probability can be determined | set aside |
| 11-F | A probability distribution or set of distributions can be determined | set aside |
| S1 | Confidence scale: very low, low, medium, high, very high | set aside — the estate's finding is observed or not; a five-term scale would invite invented middles |
| S2 | Likelihood scale: virtually certain (99–100%) … exceptionally unlikely (0–1%) | set aside — quantified probability has no meaning for a claim about whether work was done |
| S3 | Evidence summary terms: limited, medium, robust | owed — with item 8 |
| S4 | Agreement summary terms: low, medium, high | owed — with item 8 |
| S5 | Findings conditional on other findings are evaluated and reported separately | owed — an estate whose checks are chains of pins has exactly this problem and no rule for it |

**Counted:** 21 items — 3 covered, 8 owed, 10 set aside. The count is read from the source, not from the laws built.


---

# Census: Eidelman, Crandall & Pattershall (2009), read from the abstract

The full text is paywalled. The abstract enumerates the paper's whole structure — five studies and the conclusion drawn from them — so that is the unit censused, and the fact that it is the abstract and not the paper is stated rather than glossed. **6 items.**

| # | What it states | Status |
|---|---|---|
| 1 | Study 1: an existing state is evaluated more favorably than an alternative | covered — `what-exists-is-not-thereby-chosen` |
| 2 | Study 2: the same, replicated | covered — same law |
| 3 | Study 3: imagining an event increases estimates of its likelihood, which in turn leads to favorable evaluation; the more likely something will be, the more positively it is evaluated | owed — the mechanism by which a plan already sketched starts to look right, which is a distinct defect from defending what exists |
| 4 | Study 4: the more a form is described as prevalent, the more aesthetically attractive that form is — a causal relationship between aesthetic judgment and existence *in a domain lacking choice among alternatives* | covered — the naming sighting is exactly this case |
| 5 | Study 5: the bias extends to gustatory evaluation and is not moderated by valence | set aside — establishes generality, prescribes nothing |
| 6 | Conclusion: mere existence leads to assumptions of goodness; the status quo is seen as good, right, attractive, tasty, and desirable | covered — the law's statement |

**Counted:** 6 items — 4 covered, 1 owed, 1 set aside.


---

# Census: Parnas (1972), read whole

Six pages, and the paper's structure is a worked comparison of two decompositions of one program followed by a list of criteria and a conclusion. **9 items.**

| # | What it states | Status |
|---|---|---|
| 1 | Modularization is a mechanical decomposition into work assignments, and the criteria used to divide are the subject | set aside — framing |
| 2 | Decomposition 1: modules follow the steps of processing (a flowchart) | set aside — the example |
| 3 | Decomposition 2: each module is characterized by a design decision it hides from all others; its interface reveals as little as possible about its inner workings | covered — `a-thing-is-built-where-its-subject-lives` |
| 4 | Changeability: a change to a hidden decision touches one module in the second decomposition and many in the first | owed — no law states that the cost of misplacement is measured in what a change touches |
| 5 | Independent development: interfaces between modules must be defined so work can proceed separately | owed |
| 6 | Comprehensibility: a module can be understood without understanding the others | owed |
| 7 | Data representations, character codes and orderings should be hidden in a module | set aside — a programming instruction, not a practice one |
| 8 | The sequence in which items are processed should as far as practical be hidden within a single module | set aside |
| 9 | Conclusion: it is almost always incorrect to begin decomposition on the basis of a flowchart; begin with a list of difficult decisions or ones likely to change | covered — the second citation on the same law |

**Counted:** 9 items — 2 covered, 3 owed, 4 set aside.


## STARD 2015, censused whole (2026-08-24)

The law `a-rate-names-the-population-it-was-computed-over` was rooted in item 19. One item of thirty is not a reading of a source — it is the item that happened to say what was wanted, which is the defect `a-census-is-read-from-its-source` names. So the checklist was read in full: **34 rows, 7 covered, 13 owed, 14 set aside.** Run `python -m craft.census_stard`; the counts are computed there, and `--owed` prints the queue.

The analogy the census applies throughout, stated once: a diagnostic accuracy study asks how well a test identifies a condition, against a reference standard, in a population. A check in this estate asks how well a decider identifies a defect, against a person's ruling, over a corpus. Where the analogy does not carry, the item is set aside and says why — 14 of them are clinical or publishing machinery (adverse events, trial registration, funder disclosure) with no counterpart in a check.

**What the census found that mining one item would not.** Four of the thirteen owed items name things this estate has already learned as habits and never wrote down as laws:

- **Item 9** (consecutive, random or convenience series) is the cost-blind census doctrine. This package impeached its own convergence series because *"the miner picked laws it could see the compile route for"*, adopted blind sampling as the remedy, and left the remedy a habit. A habit has no falsifier.
- **Item 23** (cross tabulation of index test against reference standard) is the confusion matrix. Every check here reports what it caught and none reports what it missed or wrongly convicted. The turn checker recorded *"18 candidates over 158 turns, all cleared"* and admitted its false-negative rate was unmeasured — item 23 obeyed once, by hand, in prose.
- **Item 18** (intended sample size and how it was determined) is the calibration corpus, chosen before the run. The first turn checker calibrated on one session with one hit and reported zero false positives.
- **Items 5, 12a** (pre-specified versus exploratory) ask whether a threshold was set before or after seeing what it caught. The six-word bound on a run-in heading was set after.

Two more are uncomfortable and worth keeping uncomfortable. **Item 13a** asks whether the reader of the index test was blinded: the alarm corpora in this package are written by the same hand as the deciders they exercise. **Item 13b** asks the same of the assessor: the adjudicator reads the finding before ruling on it, always, and that is nowhere recorded as a limitation.
