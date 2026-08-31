# The practice sources: where laws about the WORK come from

Surveyed 2026-08-22. The interface family was mined from a catalogue chosen deliberately ([sources.md](sources.md)); the practice family was not — it grew from defects, one session at a time, and cites nothing. Five of its laws stand red on `a-law-cites-a-source`. This is the catalogue that fixes that, ranked by the same two criteria, stated because they are the bias-guards: **authority** (standard, statute, or published empirical research — never fame) and **falsifiability** (can a breach be observed, or does the rule need interpretation?).

One difference from the interface catalogue is worth stating up front. There is no WCAG for the practice of building: no single body publishes numbered, testable rules about how an engineer should reason, claim or report. The authority here is spread across uncertainty communication, statistical reporting, plain language, safety engineering and human-factors research, and much of it is principle-shaped. Where a source needs interpretation, it is cited as a root and the law carries the falsifier — never the other way round.

## The mining shortlist, in order

1. **IPCC AR5 Guidance Note on Consistent Treatment of Uncertainties** (Mastrandrea et al., 2010) — 11 numbered paragraphs, 6 lettered criteria and two calibrated scales, written to stop authors picking a confidence term the evidence does not license. Publicly available, quotable, and unusually operational for a document about judgement. **Censused below.** https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf
2. **Eidelman, Crandall & Pattershall, "The existence bias"** (*Journal of Personality and Social Psychology* 97(5), 765–775, 2009) — five studies establishing that mere existence is taken as evidence of goodness, and that the effect appears in aesthetic judgment where no choice among alternatives was ever made. Published empirical research, which is the authority; the finding is about people rather than about work, so it roots a law and does not state one. **Censused below.** Full text paywalled; the census is read from the abstract, which enumerates the studies. https://doi.org/10.1037/a0017058
3. **Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules"** (*Communications of the ACM* 15(12), 1053–1058, 1972) — the foundational statement of where a thing belongs: decompose by the design decisions each part hides, never by the steps of processing. Freely available, quotable, and it gives an observable criterion rather than a principle. **Censused below.** https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf
4. **Agans, *Debugging: The 9 Indispensable Rules*** (2002) — the root of nine practice laws; nine rules, each a command with an observable breach. Copyrighted, so cite the rule name and quote briefly. **Censused whole:** `python -m craft.census_agans`, from the author's own chapter-2 PDF; the census checks its law ids against practice.py, so a renamed law breaks it rather than silently orphaning a rule.
5. **STARD 2015** (Cohen et al., *BMJ Open* 2016;6:e012799; checklist hosted by the EQUATOR Network) — 30 numbered items, 34 rows, stating what a report of a diagnostic accuracy study must contain. A reporting standard for measurement claims, from a community that had to make them auditable because careers rest on them, and unusually falsifiable: each item is either present in a report or it is not. Already the root of `a-rate-names-the-population-it-was-computed-over`. **Censused whole:** `python -m craft.census_stard`. https://doi.org/10.1136/bmjopen-2016-012799
6. **Federal plain language guidelines** (Plain Writing Act 2010; the official March 2011 document, Rev. 1, fetched from the Internet Archive after plainlanguage.gov folded into digital.gov) — statutory, public domain, sentence-level and checkable. **Censused below**, and re-read at the guideline grain as data: `python -m craft.census_plain` (65 entries, every `covered` row naming a law id the module checks). The document itself is captured at `docs/sources/plain-2011-federal-guidelines.pdf`.
7. **ISO/IEC/IEEE 15289 and 26515** — what a work product must contain to be a record rather than a note. Paywalled: cite clause numbers, quote briefly. **Census blocked, stated rather than glossed:** the text is not in hand and a census from summaries is how fabrication starts; this row stays unread until somebody buys the standard or finds a lawful copy.
8. **CONSORT / ARRIVE / STROBE reporting checklists** — the strongest available model for "a claim carries what it rests on". **All three censused below** (CONSORT 2025's 41 rows, STROBE's 34, ARRIVE's Essential 10; ARRIVE's Recommended Set was censused 2026-08-25 in its recorded second sitting — no new law, two new roots). The finding is corroboration: the STARD-rooted measurement laws are independently demanded by all three, and the only new demands were the stopped-early row and the null-statement rule that became `a-null-is-stated-not-implied`.
9. **Tversky & Kahneman 1974, "Judgment under Uncertainty"** (*Science* 185:1124–1131) — the empirical root beneath several laws, exactly as this row predicted. **Censused below** from a full-text mirror: 3 heuristics, 13 biases, 8 rooting laws, 3 roots waiting. Principle-shaped; cite for the finding, never for a rule.
10. **NASA/ESA anomaly-reporting standards and the Swiss-cheese/HFACS literature** — this row existed as "the root for instrument-before-the-second-theory if one exists outside Agans", and its purpose is served: Agans is censused whole and roots it directly. Downgraded to optional; no census, and the reason is recorded here rather than left to look like an oversight.
11. **GOV.UK Service Manual** — the Service Standard's **14 points censused below**; the practice-shaped points were already covered and the rest are the interface catalogue's ancestry, confirmed.
12. **Model Cards for Model Reporting** (Mitchell et al., FAT* 2019) and **Datasheets for Datasets** (Gebru et al., CACM 2021) — **read and censused below**, closing the reinvention question with the papers instead of a flag: the measurement kind's fields are independently demanded by both, and the one demand they add (per-factor disaggregation) is recorded as the kind's known gap.
13. **SPIRIT 2025** (PLOS Medicine, April 2025, open access) — 34 protocol items, the before side of CONSORT. **Censused below**: five laws gained their before-side citations, and `a-protocol-is-an-artifact-before-the-run` was minted — prespecification as a dated document, never a recollection. https://doi.org/10.1371/journal.pmed.1004589
14. **PRISMA 2020** (BMJ 2021, open access) — 27 items and a four-phase flow diagram for reporting **systematic reviews**. **Censused below**, and the prediction held: it is the root of `a-census-is-read-from-its-source`, which left the red set the same day, and of `a-corpus-of-reports-carries-its-reporting-bias`. https://doi.org/10.1136/bmj.n71
15. **GUM (JCGM 100) and VIM (JCGM 200)** — the BIPM's uncertainty guide and metrology vocabulary, official PDFs free. **The GUM is censused below** — it rooted `an-uncertainty-names-its-components` and left three roots recorded for grounding@. **The VIM is censused below** (2026-08-25): no law minted, six chapter-2 terms landing on four laws — verification versus validation being `done-is-observed-where-the-user-stands` in metrology's own words. https://www.bipm.org/en/committees/jc/jcgm/publications
16. **TOP Guidelines** (Center for Open Science; TOP 2025) — **censused below from the live framework**, which had reorganised the 2015 paper's eight standards into seven Research Practices while this entry sat unread: the census records the move. Everything corroborates; the level-3 ladder rung (independent certification) is recorded as the estate's stated ceiling. https://www.cos.io/initiatives/top-guidelines

Excluded despite fame, with reasons: **Clean Code / SOLID / most engineering-practice books** (assertions without an authority, and their empirical support is thin or contested); **Agile manifesto and derivatives** (values, not rules — nothing observable); **Google's SRE book** (excellent and specific to running services, not to claiming work done; CC BY-NC-ND).

## Gaps found

- **Nothing authoritative was found on delegating a decision.** The laws about spending a person's attention (`the-users-attention-is-not-a-test-harness`, and the one the corrections named about asking for a decision the evidence settles) have no obvious root. Automation-levels research (Parasuraman/Sheridan) describes the design space without prescribing; GOV.UK prescribes for services, not for a working relationship. Searched and thin — recorded as a boundary chosen, not one fallen into.
- **The longevity half is unread.** Eidelman, Pattershall & Crandall, "Longer is better" (*Journal of Experimental Social Psychology*, 2010, DOI 10.1016/j.jesp.2010.07.008) is the companion finding — the longer something is thought to have existed, the better it is judged. Elsevier, paywalled, and the abstract was not retrieved. Named here so its absence is a record rather than an oversight; the law it would strengthen cites only the 2009 paper.
- **Nothing was found on context leaking between records.** The interface family states it for strings (`no-cross-context-string-reuse`); the practice analogue — reasoning from one context written into another's record — is asserted from the estate's own rule that a library never names a client. Owed.

---
17. **Nygard, “Documenting Architecture Decisions”** (Cognitect blog, 2011-11-15) — the canonical statement that significant decisions are kept as records with their rationale; captured verbatim 2026-08-25, roots `deliberate-names-its-decision`. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
18. **Cunningham, OOPSLA 1992 experience report** (c2.com) — the debt metaphor at its origin: unpaid remainder accrues interest; captured verbatim 2026-08-25, roots `a-remainder-names-its-debt`. http://c2.com/doc/oopsla92.html
19. **ITIL 4 glossary (Axelos)** — defines a workaround as a solution for which a full resolution is not yet available: definitionally not a fix, which is `a-detour-is-announced-as-a-detour` stated by a standard. **Capture blocked, per the ISO precedent:** the official glossary is paywalled and the text is not in hand; secondary glossaries agree on the wording and are not the authority. The law stays red until the sentence is captured.

*(2026-08-25, same sitting: Agans rule 3 — already censused whole at row 4 — gained a second law: `the-users-attention-is-not-a-test-harness` is the delegation face of the observing duty, and cites the rule the way the census's other laws do.)*


# Census: IPCC AR5 Guidance Note, read whole

Every item the source states, each mapped. `covered` — a law here carries it. `owed` — it applies to this practice and no law carries it yet. `set aside` — it is about the source's own subject (climate assessment) and does not transfer.

The Guidance Note states 11 numbered paragraphs, 6 lettered criteria (A–F) under paragraph 11, a 5-term confidence scale, a 10-term likelihood scale, and the evidence/agreement summary terms. That is **21 items**.

| # | What it states | Status |
|---|---|---|
| 1 | Consider, at an early stage, how to communicate the degree of certainty; agree the process in advance of the specific case | covered — `calibration-is-agreed-before-the-case` (2026-08-24) |
| 2 | Provide a *traceable account*: a description of the evaluation of type, amount, quality and consistency of evidence, and the degree of agreement, which together form the basis for the finding | covered — `done-is-observed-where-the-user-stands` demands the evidence beside the claim, and the claims ledger's `evidence.where` is the traceable account in data. Since 2026-08-24 also the root of the `confirmation` kind's decider: an agreement is a finding, and one filed with nothing in `checked` has no account, convicting under `a-qualifier-is-licensed-by-the-evidence` |
| 3 | Beware group convergence and overconfidence; beware anchoring on previous versions to a greater extent than is justified | covered — `a-view-moves-on-observation-not-on-company` (2026-08-24), both directions: folding is convergence, stonewalling is anchoring |
| 4 | Framing changes interpretation (10% chance of dying vs 90% of surviving); consider reciprocal statements | set aside — about presenting risk to a public, not about reporting work |
| 5 | **"Consider that, in some cases, it may be appropriate to describe findings for which evidence and understanding are overwhelming as statements of fact without using uncertainty qualifiers."** | **covered — `a-qualifier-is-licensed-by-the-evidence`** |
| 6 | Consider all plausible sources of uncertainty; experts tend to underestimate structural uncertainty from incomplete understanding | covered — `structural-unknowns-are-considered` (2026-08-24) |
| 7 | Assess uncertainty and risk to the extent possible; attend to high-consequence outcomes | set aside — a risk-management instruction about the subject matter |
| 8 | Evaluate validity on two dimensions — evidence (limited/medium/robust) and agreement (low/medium/high) — and provide a traceable account of both | covered — `validity-is-evidence-and-agreement` (2026-08-24) |
| 9 | Confidence is five qualifiers (very low → very high); low and very low confidence should be reserved for areas of major concern and the reasons explained; confidence is not probabilistic | covered — `low-confidence-is-reserved-and-explained` (2026-08-24); the five-term scale itself stays set aside |
| 10 | Likelihood is calibrated language for quantified uncertainty; where there is sufficient information it is preferable to give the probability directly rather than the term; "about as likely as not" must not stand in for a lack of knowledge | covered — `sufficient-information-gives-the-number` (2026-08-24) |
| 11 | Characterize findings using the language that conveys the most information, per criteria A–F | covered in part by item 5's law; the criteria are set aside individually below |
| 11-A | Ambiguous or unmeasurable variable: assign no confidence; give evidence and agreement terms | set aside |
| 11-B | Sign known, magnitude poorly known: assign confidence when possible | set aside |
| 11-C | Order of magnitude available: assign confidence; state assumptions | set aside |
| 11-D | A range can be given: assign likelihood for that range when possible | set aside |
| 11-E | A likelihood or probability can be determined | set aside |
| 11-F | A probability distribution or set of distributions can be determined | set aside |
| S1 | Confidence scale: very low, low, medium, high, very high | set aside — the estate's finding is observed or not; a five-term scale would invite invented middles |
| S2 | Likelihood scale: virtually certain (99–100%) … exceptionally unlikely (0–1%) | set aside — quantified probability has no meaning for a claim about whether work was done |
| S3 | Evidence summary terms: limited, medium, robust | covered — with item 8, `validity-is-evidence-and-agreement` |
| S4 | Agreement summary terms: low, medium, high | covered — with item 8, `validity-is-evidence-and-agreement` |
| S5 | Findings conditional on other findings are evaluated and reported separately | covered — `a-conditional-finding-grades-its-condition` (2026-08-24) |

**Counted:** 21 items — 11 covered, 0 owed, 10 set aside (as of 2026-08-24; the owed queue was drained in one tranche). The count is read from the source, not from the laws built.


---

# Census: Eidelman, Crandall & Pattershall (2009), read from the abstract

The full text is paywalled. The abstract enumerates the paper's whole structure — five studies and the conclusion drawn from them — so that is the unit censused, and the fact that it is the abstract and not the paper is stated rather than glossed. **6 items.**

| # | What it states | Status |
|---|---|---|
| 1 | Study 1: an existing state is evaluated more favorably than an alternative | covered — `what-exists-is-not-thereby-chosen` |
| 2 | Study 2: the same, replicated | covered — same law |
| 3 | Study 3: imagining an event increases estimates of its likelihood, which in turn leads to favorable evaluation; the more likely something will be, the more positively it is evaluated | covered — `an-imagined-plan-is-not-thereby-likely` (2026-08-24) |
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
| 4 | Changeability: a change to a hidden decision touches one module in the second decomposition and many in the first | covered — `a-boundary-is-judged-by-what-a-change-touches` (2026-08-24) |
| 5 | Independent development: interfaces between modules must be defined so work can proceed separately | covered — same law |
| 6 | Comprehensibility: a module can be understood without understanding the others | covered — same law |
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


---

# Census: CONSORT 2025, read whole (2026-08-24)

The current statement (BMJ 2025;388:e081123, open access; the 2010 version's 25 items became 30, with an open-science section). The unit is the checklist's own rows — items with a/b/c splits counted as the table lists them, **41 rows**. Read as the practice family's cross-check on STARD: two reporting standards, censused independently, should demand the same things of a measurement's report — the same corroboration the interface catalogue got from censusing RGAA and WCAG blind.

| rows | what they state | status |
|---|---|---|
| 1a, 1b | identification and structured summary | set aside — how a paper announces itself |
| 2, 3, 4 | registration; where protocol and analysis plan can be accessed; where data, code and materials can be accessed | set aside for the register (the repo is the registry and the protocol is the code) — but row 3's demand is `a-check-is-stated-to-replication`, corroborated |
| 5a, 5b | funding and conflicts | set aside — no counterpart |
| 6, 7 | background; specific objectives | covered — the falsifier stated in advance (`a-hypothesis-is-falsifiable`, kill-criterion kinds) |
| 8 | patient and public involvement | set aside |
| 9 | trial design and framework | covered — `the-reference-standard-is-named-with-its-rationale`'s ground |
| 10 | important changes after commencement, **including any outcomes or analyses that were not prespecified, with reason** | covered — `prespecified-is-distinguished-from-exploratory`, corroborated in stronger words than STARD's |
| 11, 12a, 12b | setting; eligibility | covered — `a-corpus-names-its-assembly`, `a-rate-names-the-population-it-was-computed-over` |
| 13 | intervention **with sufficient details to allow replication** | covered — `a-check-is-stated-to-replication`, near-verbatim corroboration |
| 14 | prespecified outcomes with measurement variable, metric, aggregation, time point | covered — the measurement kind's fields are this row's shape |
| 15, 27 | harms, defined and assessed; all harms in each group | set aside — clinical |
| 16a | **how sample size was determined, including all assumptions** | covered — `calibration-size-is-declared-before-the-run`, corroborated |
| 16b | interim analyses and stopping guidelines | owed — nothing here says when a running check may be stopped early, and stopping on a peek is the tuning defect in disguise |
| 17a, 17b, 18, 19 | randomisation, concealment, implementation | set aside — allocation machinery; the census notes `a-corpus-names-its-assembly` carries the random/convenience half |
| 20a, 20b | who was blinded, how | covered — `blindness-is-disclosed`, corroborated |
| 21a, 21b, 21c, 21d | statistical methods; who is in each analysis; **how missing data were handled**; additional analyses, **distinguishing prespecified from post hoc** | covered — `missing-input-is-reported-with-its-handling`, `prespecified-is-distinguished-from-exploratory`, and 21b is the rate law's denominator demand |
| 22a, 22b | participant flow; losses and exclusions **with reasons** | covered — `a-rate-names-the-population-it-was-computed-over` (STARD's flow diagram, same demand) |
| 23a, 23b | recruitment dates; why the trial ended or was stopped | 23a set aside; 23b owed with 16b — the stopped-early row |
| 24a, 24b | intervention as actually administered (fidelity); concomitant care | covered — the drift half: what ran is reported, not what was intended (witness/walk doctrine, corroborated from outside) |
| 25 | baseline characteristics table | set aside — clinical |
| 26 | per outcome: **numbers analysed, available data, effect size and its precision** | covered — `a-check-reports-its-misses` and grounding@'s tolerance |
| 28 | ancillary analyses, prespecified vs post hoc | covered — with 21d |
| 29 | **interpretation consistent with results, balancing benefits and harms** | covered — `a-qualifier-is-licensed-by-the-evidence`, corroborated |
| 30 | limitations: bias, imprecision, generalisability | covered — the `gap` field on grounds; `a-remainder-names-its-debt` |

**Counted: 41 rows — 26 covered, 3 owed (16b, 23b as one demand: a stopped run says why; and nothing else), 12 set aside.** The cross-check the census was for: every measurement-protocol law minted from STARD is independently demanded by CONSORT, none contradicted.

# Census: STROBE (observational studies), read whole (2026-08-24)

The combined checklist (cohort, case-control, cross-sectional), **22 items, 34 rows** with splits. Same verdict at every transferable row as CONSORT, so the table records only where it differs; rows not listed are the same demand as the CONSORT row above and carry its status.

| rows | what they state | status |
|---|---|---|
| 4–8 | design, setting, participants, variables, measurement | covered — corpus/assembly/reference-standard family |
| 9 | **efforts to address potential sources of bias** | covered — `structural-unknowns-are-considered`, corroborated |
| 10 | how the study size was arrived at | covered — `calibration-size-is-declared-before-the-run` |
| 12(a–e), 13, 16 | statistical methods, missing data, participant numbers | covered — as CONSORT 21/22/26 |
| 14–15, 17–18 | descriptive/outcome data, other analyses | set aside / covered as CONSORT |
| 19 | limitations | covered — as CONSORT 30 |
| 21 | generalisability | covered — the `gap` field |
| 22 | funding | set aside |

**Counted: 34 rows — no demand found that CONSORT does not make; 0 owed beyond CONSORT's. The corroboration is the finding.**

# Census: ARRIVE 2.0 Essential 10, read whole (2026-08-24)

The author consortium's own PDF. The Essential 10 is the set the guidelines name as the minimum, and the unit here; the Recommended Set exists and is recorded as **not censused** — a second sitting, stated rather than glossed.

| item | what it states | status |
|---|---|---|
| 1 | study design: groups compared, **rationale if no control group**, the experimental unit | covered — reference-standard and corpus family |
| 2 | exact n per group; **how the sample size was decided, a priori calculation if done** | covered — `calibration-size-is-declared-before-the-run` |
| 3 | inclusion/exclusion criteria, **established a priori; "If no criteria were set, state this explicitly ... If there were no exclusions, state so"** | covered — roots `a-null-is-stated-not-implied`, minted 2026-08-24 from this row |
| 4 | randomisation and confounder strategy, **"If confounders were not controlled, state this explicitly"** | covered — the same law's second verbatim demand |
| 5 | who was aware of group allocation at each stage | covered — `blindness-is-disclosed` |
| 6 | all outcome measures defined; the primary named | covered — reference-standard family |
| 7 | statistical methods, the unit of analysis | covered — as CONSORT 21 |
| 8 | experimental animals: species, strain, sex, age/weight | set aside — the subject's biology |
| 9 | procedures: what, when, where, why | covered — `the-trail-is-written-as-it-happens` |
| 10 | results: summary statistics **with a measure of variability** | covered — grounding@'s tolerance |

**Counted: 10 items — 9 covered, 1 set aside, 0 owed.** Item 3 is the one row in all three trial standards that states the null-reporting rule outright, which is why the law roots here and not in CONSORT.

# Census: Tversky & Kahneman 1974, read whole (2026-08-24)

*Judgment under Uncertainty: Heuristics and Biases* (Science 185:1124–1131), from a full-text university mirror. The paper's own unit: **three heuristics and the thirteen biases it enumerates under them.** The shortlist's warning holds — this source ROOTS laws and states none, so the census records which law each bias grounds; a row with no law is a root waiting.

| # | bias | status |
|---|---|---|
| R1 | insensitivity to prior probability of outcomes | roots `a-cause-is-weighed-by-how-often-not-only-how-alike` (2026-08-25), with a decider: a diagnosis saying `resembles` carries `base_rate`, computable from the filed diagnoses themselves |
| R2 | **insensitivity to sample size** | roots `calibration-size-is-declared-before-the-run` (second, empirical root beside STARD 18) |
| R3 | misconceptions of chance (gambler's fallacy) | recorded in the argument census (Greenwell row) — vocab lane |
| R4 | insensitivity to predictability | roots `a-qualifier-is-licensed-by-the-evidence` (cited 2026-08-25): confidence unaffected by the reliability of its inputs is the unlicensed qualifier's empirical mechanism |
| R5 | the illusion of validity | roots `blindness-is-disclosed`'s worry: consistency of inputs breeds confidence regardless of accuracy |
| R6 | **misconceptions of regression** | roots `regression-is-the-null-after-an-extreme`, minted 2026-08-24 from this row |
| A1 | biases due to the retrievability of instances | roots `an-imagined-plan-is-not-thereby-likely`'s family (availability) |
| A2 | biases due to the effectiveness of a search set | roots `a-corpus-names-its-assembly` (cited 2026-08-25): the search set organizes what is found, which is why a corpus states whether it was exhaustive, random or convenient |
| A3 | biases of **imaginability** | roots `an-imagined-plan-is-not-thereby-likely` (second, older root beside Eidelman study 3) |
| A4 | illusory correlation | argument-lane (Greenwell: correlation family) — vocab lane |
| An1 | **insufficient adjustment** from an anchor | roots `a-view-moves-on-observation-not-on-company`'s anchoring half (the empirical root beneath IPCC ¶3, exactly as the shortlist predicted) |
| An2 | biases in the evaluation of **conjunctive and disjunctive events** | roots `a-conditional-finding-grades-its-condition` — chained pins are a conjunctive event, overestimated exactly as the paper says |
| An3 | anchoring in the assessment of subjective probability distributions | with An1 |

**Counted: 3 heuristics, 13 biases — 11 rooting laws, 2 recorded in the argument lane, 0 roots waiting** (R1, R4 and A2 landed 2026-08-25: one as a new law with a decider, two as the empirical roots beneath standing laws).

# Census: Model Cards and Datasheets, read whole (2026-08-24)

The reinvention question's answer, now from the read papers instead of a flag. Model Cards (Mitchell et al., FAT* 2019): **nine sections, 4.1–4.9.** Datasheets for Datasets (Gebru et al.): **seven workflow sections.** Unit: the papers' own section lists.

| section | status |
|---|---|
| MC 4.1 Model Details / 4.2 Intended Use | covered — the trigger states where a law applies; `a-check-is-stated-to-replication` |
| MC 4.3 **Factors** (disaggregation of performance across groups and conditions) | covered — roots `a-figure-is-broken-down-by-its-declared-factors` (2026-08-25): the protocol declares its factors before the run, the measurement reports per-factor rows after it, and the aggregate-only report of a factor-declaring protocol convicts in code |
| MC 4.4 Metrics / 4.5 Evaluation Data | covered — measurement kind fields (`reference_standard`, `corpus`) |
| MC 4.6 Training Data | set aside — no counterpart (the checks are not trained) |
| MC 4.7 Quantitative Analyses | covered — `a-check-reports-its-misses` |
| MC 4.8 Ethical Considerations | set aside |
| MC 4.9 Caveats and Recommendations | covered — the `gap` field, `a-remainder-names-its-debt` |
| DS Motivation / Uses / Distribution / Maintenance | set aside — dataset lifecycle |
| DS **Composition** and **Collection Process** | covered — `a-corpus-names-its-assembly` in another field's words, exactly as flagged; the corroboration that answers the reinvention question |
| DS Preprocessing/cleaning/labelling | covered — `missing-input-is-reported-with-its-handling`'s ground |

**Counted: 16 rows — 11 covered, 0 owed, 5 set aside** (the disaggregation row moved owed → covered on 2026-08-25, when the gap it recorded was closed by law and decider). The measurement kind reinvented nothing: its fields are STARD's, and the one demand the ML community's shapes added is now carried.

# Census: GOV.UK Service Standard, read whole (2026-08-24)

**14 points**, from the live service manual. The interface catalogue already descends from GOV.UK's design system; this census asks only what the *Standard* says about the practice of building.

| # | point | status |
|---|---|---|
| 1–5 | understand users; solve a whole problem; joined-up experience; simple to use; everyone can use it | set aside for the practice family — the interface catalogue's ground (accessibility rows censused under WCAG/RGAA) |
| 6, 7 | multidisciplinary team; agile ways of working | set aside — organisational |
| 8 | **iterate and improve frequently** | covered — `make-it-fail-before-you-fix-it` and the loop doctrine; principle-shaped here |
| 9 | secure service, privacy | set aside — subject-matter |
| 10 | **define what success looks like and publish performance data** | covered — the measurement kind is this point as data; the falsifier stated in advance is `a-hypothesis-is-falsifiable` |
| 11 | choose the right tools | set aside |
| 12, 13 | make source open; use open standards and common patterns | covered in practice — the estate's registries and this catalogue's own citation rule (`a-law-cites-a-source` is point 13 applied to laws) |
| 14 | operate a reliable service | set aside — operations |

**Counted: 14 points — 4 covered, 10 set aside, 0 owed.** The Standard's value to this catalogue was always ancestry, and the census confirms that: the practice-shaped points were already here.


# Census: Federal Plain Language Guidelines, read whole (2026-08-24)

The official document (March 2011, Rev. 1 May 2011), fetched from the Internet Archive after plainlanguage.gov folded into four guide pages on digital.gov. The unit is the document's own table of contents at the guideline grain — the lettered and numbered rules, **44 rows** across five chapters. This is the doc lane's second blind source, and most rows corroborate laws the Google editorial census already routed — which is the point of a second census, not a disappointment.

| rows | what they state | status |
|---|---|---|
| I.a, I.b | identify and write for your audience; address separate audiences separately | judge — audience fit is a reading, as the editorial census already ruled for the same ground |
| II.a | organize to meet your readers' needs | judge |
| II.b | address one person, not a group | covered — `speaks-to-you` |
| II.c | use lots of useful headings | covered — `front-load-first-words` and the heading machinery |
| II.d | write short sections | owed, unminted with the reason stated: the source gives no ceiling, and a length law without its number is a taste — the sentence and paragraph laws have their numbers from GOV.UK, this has none |
| III.a.1.i | use active voice | covered — the editorial census's ruling stands: passive detection by wordlist is a radar, not a decider; this source is its second root |
| III.a.1.ii | use the simplest form of a verb | judge — grammar judgment |
| III.a.1.iii | **avoid hidden verbs** | covered — roots `a-verb-travels-as-a-verb`, minted 2026-08-24 from this row |
| III.a.1.iv | **use "must" to indicate requirements** | covered — roots `must-marks-a-requirement`, minted 2026-08-24 |
| III.a.1.v | use contractions when appropriate | covered — editorial census route (wordlist radar) |
| III.a.2.i | don't turn verbs into nouns | covered — the same hidden-verbs law; the source states one rule twice |
| III.a.2.ii | use pronouns to speak directly | covered — `speaks-to-you` |
| III.a.2.iii | minimize abbreviations | covered — `acronyms-spell-out-on-first-reference` |
| III.a.3.i–ii | short, simple words; omit unnecessary words | **covered since 2026-08-31** — roots `an-answer-is-plain-on-first-reading`. Routed judge here on the ground that necessity is a reading; that holds for a word in a document and not for an answer written to one person, who says whether they could read it |
| III.a.3.iii | dealing with definitions | covered — `terms-defined-before-use` |
| III.a.3.iv | **use the same term consistently** | covered — `glossary-first` and the term kind, corroborated |
| III.a.3.v | avoid jargon | covered — `no-system-vocabulary` |
| III.a.3.vi | don't use slashes | covered — wordlist radar route |
| III.b.1 | write short sentences | covered — `sentences-stay-under-twenty-five-words` (scope per the standing ruling: interfaces) and the paragraph law's family for docs |
| III.b.2 | keep subject, verb, and object close together | judge — no distance the source states |
| III.b.3 | **avoid double negatives and exceptions to exceptions** | covered — roots `a-negative-is-not-stacked`, minted 2026-08-24 |
| III.b.4 | place the main idea before exceptions and conditions | covered — `conditions-come-before-instructions`, second root |
| III.b.5 | place words carefully | judge |
| III.c.1 | **have a topic sentence** | covered — roots `a-paragraph-opens-with-its-topic`, minted 2026-08-24 |
| III.c.2 | use transition words | judge |
| III.c.3 | write short paragraphs | covered — `paragraphs-stay-under-five-sentences` |
| III.c.4 | **cover only one topic in each paragraph** | covered — roots `one-topic-per-paragraph`, minted 2026-08-24 |
| III.d.1–7 | examples, lists, tables, illustrations, emphasis, cross-references, document design | covered where a law exists (`internal-references-resolve`, `references-name-their-target-not-its-position` for cross-references; list/table structure is the editorial census's zero route), judge for the rest |
| IV.a–g | write for the web: how people use the web, users and top tasks, web content, repurposing print, avoid PDF overload, plain-language techniques | set aside — web-writing operations; the doc lane's laws already carry the transferable parts |
| V | test your content: paraphrase testing, usability testing, controlled comparative studies | covered in doctrine — testing content on the person who reads it is the walk and the blind-usability practice; no law minted because the source prescribes methods, not observable breaches of a document |

**Counted: 44 rows — 5 minted this day, 18 covered before it, 12 judge, 8 set aside, 1 owed with its reason (short sections, no ceiling given).** The five minted rows are the ones where the source states the rule as an observable: a verb hidden in a noun, "shall" where "must" belongs, stacked negatives, a paragraph without its topic sentence, a paragraph with two topics.

**Re-read 2026-08-31, at the guideline grain, as `craft/census_plain.py`** — 65 entries where this table groups 44, section headings counted so the accounting is whole: covered 22, judge 17, meta 20, zero 3, vocab 3. The re-read was forced by a correction, not by doubt about the first reading: the owner was handed a report written in ornament and answered "Plain English please", and III.a.3.i–ii was the row that had been left as a reading. Two differences from this table, and no others. **The changed route** is that row, now rooting `an-answer-is-plain-on-first-reading`. **The new row** is V.a, paraphrase testing: all of V was set aside here as method rather than rule, which is right about the method and misses the artifact — a reader's restatement of a text, filed beside it, is a fact the estate does not record for prose, though it records the equivalent for screens. It is listed unbuilt (`python -m craft.census_plain --vocab`).


# Census: PRISMA 2020, read whole (2026-08-24)

The statement (BMJ 2021;372:n71, open access, read from PubMed Central's hosting), **27 items, 37 rows** with splits. A systematic review IS a census — sources identified, screened, included or excluded with reasons — so this is the source closest to the method that produced every table in this document, and it rooted the law that demanded them.

| rows | what they state | status |
|---|---|---|
| 1, 2 | title; abstract | set aside — how a paper announces itself |
| 3, 4 | rationale; explicit objective | covered — the motivating debt and the falsifier stated in advance |
| 5 | **inclusion and exclusion criteria** | covered — roots `a-census-is-read-from-its-source`, with items 6 and 16b |
| 6 | **all sources searched or consulted** | covered — the same law's root; this catalogue's shortlist is item 6 practised |
| 7 | full search strategies, including filters and limits | covered — `a-check-is-stated-to-replication` and `a-corpus-names-its-assembly`: the search is the assembly |
| 8, 9 | methods to decide inclusion; methods to collect data | covered — the same two laws |
| 10a, 10b | all outcomes and variables **for which data were sought** | covered — `prespecified-is-distinguished-from-exploratory`; sought-but-not-found pairs with `a-null-is-stated-not-implied` |
| 11 | risk of bias in included studies | covered — `structural-unknowns-are-considered`, `blindness-is-disclosed` |
| 12 | effect measures per outcome | covered — the measurement kind |
| 13a–13f | synthesis eligibility, preparation, display, methods with rationale, heterogeneity, sensitivity | covered — replication and nulls carry the "describe any" rows; 13e's heterogeneity is `validity-is-evidence-and-agreement`'s disagreement dimension |
| 14 | **methods to assess risk of bias due to missing results** | covered — roots `a-corpus-of-reports-carries-its-reporting-bias`, minted 2026-08-24 from this row |
| 15, 22 | certainty in the body of evidence, assessed and presented | covered — the calibration vocabulary and its decider |
| 16a | the flow from records identified to studies included | covered — `a-rate-names-the-population-it-was-computed-over` (the flow diagram, third standard to demand it) |
| 16b | **near-misses cited and excluded, with reasons** | covered — the census law's root; this document's judge and set-aside columns are 16b practised |
| 17, 18, 19 | per-study characteristics, bias, estimates with precision | covered — grounds, grades, grounding@'s tolerance |
| 20a–20d | synthesis results, heterogeneity, sensitivity | covered — with 13 |
| 21 | **reporting-bias assessments presented per synthesis** | covered — the new law's second citation |
| 23a–23d | interpretation; limitations of the evidence; **limitations of the review process itself**; implications | covered — `a-qualifier-is-licensed-by-the-evidence`, the `gap` field, and 23c is the why_low this catalogue's own claims already carry |
| 24a | registration | set aside — the repo is the register |
| 24b | protocol accessible **or state that a protocol was not prepared** | covered — `a-null-is-stated-not-implied`, corroborated; the before-half itself is the SPIRIT sitting |
| 24c | amendments to registration or protocol | covered — `prespecified-is-distinguished-from-exploratory` |
| 25, 26 | funding; competing interests | set aside |
| 27 | which materials are publicly available and where | covered — the TOP lane's subject; here, the repo |

**Counted: 37 rows — 31 covered, 6 set aside, 0 owed.** Two firsts: the law that drove every census in this document was rooted BY one — uncited from its minting until this table — and the intake debt's premise (self-report catches the already-noticed) became a falsifiable law with a standing authority behind it.


# Census: SPIRIT 2025, read whole (2026-08-25)

The protocol standard (PLOS Medicine 2025;22:e1004589, open access), **34 items, 46 rows** with splits. SPIRIT is CONSORT's mirror: what a trial declares *before* it runs, from the same consortium, sharing a website. For this catalogue it is the before side of every after-side law STARD and CONSORT rooted — which is exactly what the shortlist predicted, and the census confirms it row by row rather than by trust.

| rows | what they state | status |
|---|---|---|
| 1a, 1b, 2 | title, structured summary, protocol version and date | set aside — announcement and versioning (the estate's versioning is git and the lock) |
| 3a–3d, 7a, 7b, 8, 11 | roles, sponsors, funding, conflicts, dissemination, public involvement | set aside — organisational |
| 4 | registration, **"If not yet registered, name of intended registry"** | covered — `a-null-is-stated-not-implied`'s shape at the registry |
| 5 | **where the protocol and analysis plan can be accessed** | covered — roots `a-protocol-is-an-artifact-before-the-run`, minted 2026-08-25 from this census |
| 6 | where data, code and materials will be accessible | covered — the TOP lane's subject; here, the repo |
| 9a | background including **published and unpublished** studies | covered — `a-corpus-of-reports-carries-its-reporting-bias`, corroborated from the before side |
| 9b | **explanation for choice of comparator** | covered — `the-reference-standard-is-named-with-its-rationale`, before side |
| 10, 12 | objectives; design and framework including exploratory | covered — the falsifier in advance; `prespecified-is-distinguished-from-exploratory` |
| 13, 14a, 14b | setting; eligibility | covered — `a-corpus-names-its-assembly`, declared rather than reported |
| 15a | intervention **with sufficient details to allow replication** | covered — `a-check-is-stated-to-replication`, before side |
| 15b | **criteria for discontinuing or modifying, declared in advance** | covered — `a-stopped-run-says-why`'s before half |
| 15c, 15d | adherence strategies; concomitant care | set aside — clinical conduct |
| 16 | outcomes with variable, metric, aggregation, time point | covered — the measurement kind's fields, declared before |
| 17 | harms | set aside |
| 18 | participant timeline, schematic recommended | set aside — scheduling |
| 19 | **how sample size was determined, all assumptions** | covered — `calibration-size-is-declared-before-the-run` gains this as its before-side citation, which is the side the law's own name promises |
| 20 | recruitment strategies | set aside |
| 21a–24c | randomisation, concealment, implementation, blinding plans and unblinding circumstances | covered — `blindness-is-disclosed`, declared rather than disclosed after |
| 25a | instruments **with their reliability and validity, if known** | covered — the reference standard's ground; the if-known clause is the null-statement shape |
| 25b | retention plans; **outcome data for those who discontinue** | covered — `missing-input-is-reported-with-its-handling`, planned rather than reported |
| 26 | data management and quality (double entry, range checks) | judge — process quality plans; the estate's analogue is schema checks, no law states the demand |
| 27a–27d | statistical methods; who is in each analysis; missing data; additional analyses | covered — as CONSORT 21, declared before |
| 28a | data monitoring committee, **"or an explanation of why a DMC is not needed"** | covered — `a-null-is-stated-not-implied` gains this citation |
| 28b | **interim analyses and stopping guidelines, and who decides** | covered — `a-stopped-run-says-why` gains this as its before-side citation |
| 29 | monitoring frequency, **"If there is no monitoring, give explanation"** | covered — the null-statement law's third verbatim demand in one standard |
| 30, 32a, 32b, 33, 34 | ethics approval, consent, confidentiality, post-trial care | set aside — human-subjects machinery |
| 31 | **plans for communicating protocol modifications** | covered — the protocol-artifact law's second citation: an amended declaration is announced, never silently edited |

**Counted: 46 rows — 26 covered, 19 set aside, 1 judge, 0 owed after the mint.** What the census delivered: the before side of five laws now cited from the before-standard itself (calibration size, stopping, nulls, reporting bias, replication), and one new law — prespecification is an accessible dated artifact, not a memory — which is the demand that gives `prespecified-is-distinguished-from-exploratory` something checkable to stand on.


# Census: the GUM (JCGM 100:2008), read whole (2026-08-25)

The BIPM's Guide to the Expression of Uncertainty in Measurement, official PDF, 134 pages. The unit is the document's own structure: **nine chapters and ten annexes, 19 rows.** Most of the GUM is the mathematics of propagating uncertainty — method, not reporting rules — and the census says so row by row instead of mining only the reporting clause and calling it the document.

| rows | what they hold | status |
|---|---|---|
| 0, 1, 2 | introduction, scope, definitions | set aside — front matter; the definitions are Annex B/C's subject |
| 3 | basic concepts: measurement, **errors versus uncertainty**, corrections | covered as doctrine — error is what a correction fixes and uncertainty is what remains; grounding@'s split between a value and its trustworthiness practises this, and the root is recorded here for grounding@ to cite when it is next published |
| 4 | evaluating standard uncertainty: **Type A (statistical) versus Type B (other means, including judgment)** | covered — the provenance split (measured versus asserted) that grounding@'s `provenance` field and the claims record's `where` grading both practise; the root recorded for both |
| 5 | combined standard uncertainty: **propagation from input quantities, correlated and not** | covered — `a-conditional-finding-grades-its-condition`'s quantitative sibling: a chained result's uncertainty is computed from its inputs', which is what that law demands in words |
| 6 | expanded uncertainty and **the coverage factor** | covered — the root `trusted_within` gestures at: a tolerance means nothing without its coverage, recorded for grounding@ |
| 7 | **reporting uncertainty** | covered — roots `an-uncertainty-names-its-components`, minted 2026-08-25: clause 7.1.4's budget demand, with 7.1.2's keep-references-consistent as the drift clause |
| 8 | summary of procedure | set aside — a recap of 4–7 |
| A | the CIPM recommendations the GUM implements | set aside — provenance of the method |
| B, C | metrological and statistical terms | set aside — the vocabulary lane's subject (VIM is the fuller form, unread) |
| D | "true" value, error, and uncertainty | covered as doctrine — with chapter 3 |
| E | motivation for Recommendation INC-1: "safe", "random", and "systematic"; **the case against deliberately pessimistic uncertainties** | covered — `low-confidence-is-reserved-and-explained`'s metrology twin: padding an uncertainty to be safe is the same defect as routine lowballing, and the annex argues it at length |
| F, G | practical guidance on components; degrees of freedom and confidence levels | set aside — method detail |
| H, J | worked examples; glossary of symbols | set aside |
| bibliography | — | set aside |

**Counted: 19 rows — 6 covered, 13 set aside, 0 owed after the mint.** Three roots recorded for grounding@ (error-versus-uncertainty, Type A/B provenance, coverage), to be cited there when that package is next published; recording them here rather than editing another repository mid-census is the boundary, stated.

# Census: TOP Guidelines, read whole (2026-08-25)

**The source moved while it sat on the shortlist**: the entry promised the 2015 paper's eight standards, and the Center for Open Science's live framework is **TOP 2025 — seven Research Practices, three implementation levels, plus verification practices** — reorganised from the eight. The census reads the live framework from cos.io and records the reorganisation instead of censusing the version that no longer governs; the 2015 paper stays citable as history.

| row | what it states | status |
|---|---|---|
| Study Registration | the study is registered, discoverably, before it runs | covered — `a-protocol-is-an-artifact-before-the-run` |
| Study Protocol | the protocol exists and is accessible | covered — the same law; SPIRIT is the protocol's own standard |
| Analysis Plan | the analysis is planned before the data | covered — `prespecified-is-distinguished-from-exploratory` and the artifact law |
| Materials Transparency | materials shared and cited from trusted repositories | covered — `a-check-is-stated-to-replication`; the estate's materials are the repo |
| Analysis Code Transparency | code shared and cited | covered — the check IS code in the repo |
| Data Transparency | data shared and cited | covered — tapes, claims and censuses are committed; the citation half is `a-law-cites-a-source`'s ground |
| Reporting Transparency | reporting follows the relevant standard | covered — the measurement protocol, which is STARD-CONSORT-SPIRIT censused into fields |
| Levels 1–3: **disclosed < shared-and-cited < independently certified** | the ladder itself | covered as a shape — the published form of how a rule hardens: the demoted word lists report (level 1), the deciders require (level 2), and nothing here certifies independently (level 3 is the estate's recorded ceiling, unclaimed) |
| Verification practices (results transparency, computational reproducibility; verification studies) | independent re-execution | covered in vocabulary — the agreement dimension's "independent judges concur"; no law requires a second runner, and the calibration scales cap an unreplicated figure at medium agreement rather than demanding more |

**Counted: 9 rows — 9 covered, 0 owed, 0 set aside.** The whole framework corroborates laws already minted, which is the right result for the last source on a shortlist that the earlier censuses drove: by the fourteenth source a new demand should be rare — and the one thing TOP adds that nothing here claims, level-3 independent certification, is recorded as the estate's stated ceiling rather than silently absorbed.


# Census: the VIM (JCGM 200:2012), read whole (2026-08-25)

The International Vocabulary of Metrology, third edition, official BIPM PDF, 108 pages. The unit is the document's own structure: **five chapters of numbered terms plus the concept-diagram annex, 8 rows** — with the per-chapter term counts computed from the text (highest term index seen per chapter: 30, 53, 12, 31, 34, roughly 160 terms). A vocabulary prescribes nothing term by term, so the chapter is the honest grain, and the terms that transfer are named inside their rows rather than silently summarised.

| rows | what they hold | status |
|---|---|---|
| front matter, conventions, scope | — | set aside |
| 1 (30 terms) | quantities and units: the SI machinery | set aside — the measurand's algebra, no practice content |
| 2 (53 terms) | **measurement**: the terms this catalogue has been reaching for | covered — six terms land on laws. **2.44/2.45 verification versus validation** is `done-is-observed-where-the-user-stands` in metrology's own words (a green suite verifies; only the user's surface validates), added as that law's citation. **2.21/2.25 repeatability versus reproducibility** are the agreement dimension's observables (same hand versus different hands and conditions), added to `validity-is-evidence-and-agreement`. **2.41 metrological traceability** — "a documented unbroken chain of calibrations, each contributing to the measurement uncertainty" — is the pin-chain doctrine stated whole: `the-reference-standard-is-named-with-its-rationale` plus `a-conditional-finding-grades-its-condition` carry it, and the census records the term as their joint metrology name. **2.26 measurement uncertainty** is the GUM census's subject |
| 3 (12 terms) | devices for measurement | set aside — hardware |
| 4 (31 terms) | properties of measuring devices | set aside as a chapter, with one term named: **4.21 instrumental drift** — the estate's drift doctrine (witness, walk, the GUM's 7.1.2) has metrology's own word for it, recorded here for whoever next needs to cite that a measuring instrument's relation to truth decays between calibrations |
| 5 (34 terms) | measurement standards, etalons, calibration hierarchies | set aside — the institution of reference standards; the transferable part is 2.41's chain, already carried |
| Annex A | concept diagrams | set aside |
| bibliography | — | set aside |

**Counted: 8 rows — 1 covered (chapter 2, six terms landing on four laws), 7 set aside, 0 owed.** No law minted, and that is the finding: the VIM is a vocabulary, and its value to this catalogue is words for things already ruled — verification versus validation being the pair the practice family was founded on without knowing metrology had already named it.


# Census: ARRIVE 2.0 Recommended Set, read whole (2026-08-25)

The second sitting the Essential 10 census recorded as owed, now sat: **items 11–21, 16 rows** with splits, from the same author-consortium PDF. The set "complements the Essential 10 and adds important context", and for this catalogue it is a corroboration pass — which the census demonstrates row by row rather than asserts.

| rows | what they state | status |
|---|---|---|
| 11 | abstract | set aside — announcement |
| 12a | scientific background and rationale | covered — the motivating debt; CONSORT 6's ground |
| 12b | **how the animal model addresses the objectives, and its relevance to human biology** | covered — the stand-in's charter: why the model is faithful and for what, which is `evidence.where: stand-in` with its `gap`, stated by the standard that governs model organisms |
| 13 | research question, objectives, hypotheses | covered — the falsifier stated in advance |
| 14 | ethical approval; **"If ethical approval was not sought or granted, provide a justification"** | set aside — subjects machinery; the null-statement shape noted |
| 15 | housing and husbandry | set aside |
| 16a | steps to reduce pain and distress | set aside — welfare conduct |
| 16b | **expected or unexpected adverse events, reported** | covered — `the-trail-is-written-as-it-happens`: the unexpected event is precisely what a reconstructed account loses |
| 16c | **humane endpoints, the signs monitored, the frequency; "If the study did not have humane endpoints, state this"** | covered — `a-stopped-run-says-why` gains this as a citation: the stopping rule declared with its signs and monitoring cadence, and the null stated |
| 17a | interpretation against objectives, theory, and the literature | covered — `a-qualifier-is-licensed-by-the-evidence` |
| 17b | **limitations: bias, limitations of the animal model, imprecision** | covered — the `gap` field and `structural-unknowns-are-considered`; "limitations of the animal model" is the stand-in's gap in the source's own words |
| 18 | generalisability to other species and conditions | covered — as CONSORT 30, the `gap`'s reach |
| 19 | **whether a protocol was prepared before the study, and if and where registered** | covered — `a-protocol-is-an-artifact-before-the-run` gains this as a citation: its third standard in two days |
| 20 | data access statement | covered — the TOP lane; here, the repo |
| 21a | conflicts; **"If none exist, this should be stated"** | set aside — disclosure machinery; the third null-statement clause in this one set, noted for the law's census trail |
| 21b | funding and the funder's role | set aside |

**Counted: 16 rows — 9 covered, 7 set aside, 0 owed.** The set's fingerprint: three of its sixteen rows restate the null-statement rule, and two rows landed as citations on laws minted this week — the stopping law and the protocol-artifact law, the latter now carried by SPIRIT, TOP and ARRIVE independently. A recorded second sitting that produced no new law and two new roots is the census discipline working exactly as intended.
