# The practice sources: where laws about the WORK come from

Surveyed 2026-08-22. The interface family was mined from a catalogue chosen deliberately ([sources.md](sources.md)); the practice family was not — it grew from defects, one session at a time, and cites nothing. Five of its laws stand red on `a-law-cites-a-source`. This is the catalogue that fixes that, ranked by the same two criteria, stated because they are the bias-guards: **authority** (standard, statute, or published empirical research — never fame) and **falsifiability** (can a breach be observed, or does the rule need interpretation?).

One difference from the interface catalogue is worth stating up front. There is no WCAG for the practice of building: no single body publishes numbered, testable rules about how an engineer should reason, claim or report. The authority here is spread across uncertainty communication, statistical reporting, plain language, safety engineering and human-factors research, and much of it is principle-shaped. Where a source needs interpretation, it is cited as a root and the law carries the falsifier — never the other way round.

## The mining shortlist, in order

1. **IPCC AR5 Guidance Note on Consistent Treatment of Uncertainties** (Mastrandrea et al., 2010) — 11 numbered paragraphs, 6 lettered criteria and two calibrated scales, written to stop authors picking a confidence term the evidence does not license. Publicly available, quotable, and unusually operational for a document about judgement. **Censused below.** https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf
2. **Agans, *Debugging: The 9 Indispensable Rules*** (2002) — already the root of four practice laws; nine rules, each a command with an observable breach. Copyrighted, so cite the rule name and quote briefly.
3. **Federal plain language guidelines** (Plain Writing Act 2010; canonical pages now under digital.gov) — statutory, public domain, sentence-level and checkable. Already source #10 of the interface catalogue; the practice family needs the parts about writing for a reader who is not you.
4. **ISO/IEC/IEEE 15289 and 26515** — what a work product must contain to be a record rather than a note. Paywalled: cite clause numbers, quote briefly.
5. **CONSORT / ARRIVE / STROBE reporting checklists** — the strongest available model for "a claim carries what it rests on", each item numbered and each breach observable in a manuscript. Free, widely adopted, and about reporting rather than about our subject matter, so they transfer by analogy and must be cited as such.
6. **Kahneman, Slovic & Tversky and successors on overconfidence and anchoring** — published empirical research, the root beneath IPCC paragraph 3. Principle-shaped; cite for the finding, never for a rule.
7. **NASA/ESA anomaly-reporting standards and the Swiss-cheese/HFACS literature** — the root for "instrument before the second theory" if one exists outside Agans. Not yet read.
8. **GOV.UK Service Manual** — "do the hard work to make it simple" and the service-assessment criteria; already the ancestor of much of the interface catalogue, and the plausible root for the laws about spending someone else's attention. Principle-shaped; the design system's numbered patterns are the falsifiable part.

Excluded despite fame, with reasons: **Clean Code / SOLID / most engineering-practice books** (assertions without an authority, and their empirical support is thin or contested); **Agile manifesto and derivatives** (values, not rules — nothing observable); **Google's SRE book** (excellent and specific to running services, not to claiming work done; CC BY-NC-ND).

## Gaps found

- **Nothing authoritative was found on delegating a decision.** The laws about spending a person's attention (`the-users-attention-is-not-a-test-harness`, and the one the corrections named about asking for a decision the evidence settles) have no obvious root. Automation-levels research (Parasuraman/Sheridan) describes the design space without prescribing; GOV.UK prescribes for services, not for a working relationship. Searched and thin — recorded as a boundary chosen, not one fallen into.
- **Nothing was found on context leaking between records.** The interface family states it for strings (`no-cross-context-string-reuse`); the practice analogue — reasoning from one context written into another's record — is asserted from the estate's own rule that a library never names a client. Owed.

---

# Census: IPCC AR5 Guidance Note, read whole

Every item the source states, each mapped. `covered` — a law here carries it. `owed` — it applies to this practice and no law carries it yet. `set aside` — it is about the source's own subject (climate assessment) and does not transfer.

The Guidance Note states 11 numbered paragraphs, 6 lettered criteria (A–F) under paragraph 11, a 5-term confidence scale, a 10-term likelihood scale, and the evidence/agreement summary terms. That is **21 items**.

| # | What it states | Status |
|---|---|---|
| 1 | Consider, at an early stage, how to communicate the degree of certainty; agree the process in advance of the specific case | owed — the estate has no agreed calibration vocabulary, which is why each turn improvises one |
| 2 | Provide a *traceable account*: a description of the evaluation of type, amount, quality and consistency of evidence, and the degree of agreement, which together form the basis for the finding | covered — `done-is-observed-where-the-user-stands` demands the evidence beside the claim, and the claims ledger's `evidence.where` is the traceable account in data |
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
