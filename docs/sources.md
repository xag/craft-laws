# The sources: where craft laws come from, chosen by authority and falsifiability

Surveyed 2026-08-16, deliberately category-exhaustive so the package's coverage is chosen rather than accidental. Two ranking criteria, stated because they are the bias-guards: **authority** (standard, statute, platform owner, or published empirical research — never fame) and **falsifiability** (can a breach be observed, or does the rule need interpretation?). Gaps found are recorded at the bottom; a category we searched and found thin is a boundary we chose, not one we fell into.

## The mining shortlist, in order

1. **WCAG 2.2** (W3C Recommendation) — 87 success criteria, every one already a law with a falsifier; free, versioned URLs, universal legal authority. https://www.w3.org/TR/WCAG22/
2. **Unicode CLDR + UAX #9** — plural categories for 200+ locales and the bidi algorithm as machine-readable data; breaches are mechanically detectable; permissive license. https://cldr.unicode.org/index/cldr-spec/plural-rules
3. **GOV.UK Design System + style guide** — per-pattern published research, rules phrased as commands ("do not use placeholder text"); OGL/MIT, quotable sentence-by-sentence. https://design-system.service.gov.uk/
4. **USWDS** — public domain (CC0); per-component accessibility tests are pre-written falsifiers. https://designsystem.digital.gov/
5. **Baymard free article corpus** — the deepest empirical base for forms/checkout/search (4,400+ test sessions behind ~700 guidelines); the full catalogue is paywalled, the ~500 free articles expose a substantial subset — mine only what is free and cite the study. https://baymard.com/
6. **ISO 9241-143 (Forms)** — the only formal standard whose subject is form UI; conditional shall-statements with a conformance procedure. Paywalled: cite clause numbers, quote briefly. https://www.iso.org/standard/53590.html
7. **ARIA APG** — exact keyboard tables per widget are ready-made falsifiers; W3C but non-normative, flag that in each citation. https://www.w3.org/WAI/ARIA/apg/
8. **RGAA 4** (France) — accessibility as 106 numbered test procedures, arguably more operationally falsifiable than WCAG itself; Licence Ouverte; the package's best non-English root, proof the laws are not anglophone artifacts. https://accessibilite.numerique.gouv.fr/
9. **Mozilla l10n best practices** — short, blunt, falsifiable ("never concatenate strings"); already the root of composed-prose. https://mozilla-l10n.github.io/documentation/localization/dev_best_practices.html
10. **plainlanguage.gov** — statute-backed (Plain Writing Act 2010), public domain, checkable sentence-level rules. https://www.plainlanguage.gov/guidelines/
11. **Material Design 3** — the platform HIG with real numbers (48dp targets, contrast, type scale) and a CC BY 4.0 license — the only big-tech HIG quotable freely. https://m3.material.io/
12. **BBC Mobile Accessibility Guidelines** — WCAG bridged to native mobile as per-platform testable techniques, from a broadcaster with a statutory duty. https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/

Excluded from the shortlist despite fame, with reasons: **Apple HIG** (restrictive license, silently-updated URLs — cite only where it is the root, e.g. the 44pt target); **NN/g heuristics** (principles needing interpretation — ISO 9241-110 is the citable form; NN/g articles only where they state a concrete finding); **Mailchimp** (CC BY-NC, principle-shaped).

## The full catalogue by category

**Standards bodies:** WCAG 2.2; ARIA APG (non-normative); W3C i18n; ISO 9241 family — 110 (interaction principles, needs interpretation), 143 (forms, conformance-checkable), 171 (software a11y), 112, 125; all ISO paywalled. Unicode CLDR / UAX #9 / UAX #14 / UTS #35. EN 301 549 (EU harmonized standard, free PDF, covers non-web ICT WCAG lacks).

**Platform HIGs:** Apple HIG (44pt, Dynamic Type — restrictive license); Material 3 (48dp, HCT contrast, real content-design section — CC BY 4.0); Microsoft Fluent 2 / Windows (Learn pages CC BY 4.0); GNOME HIG (surprisingly falsifiable writing rules — CC BY-SA); KDE HIG (2024 rewrite aiming at "100% actionable").

**Government design systems:** GOV.UK (+NHS, +Home Office satellites) — the visible ancestor of most others, research attached per pattern; USWDS (CC0, statutory backing); DSFR France (legally mandatory for the state, 100% RGAA-audited components; visual identity restricted to the French state); RGAA 4; NL Design System (richtlijnen mapped 1:1 onto WCAG plus research additions); Designers Italia (legally binding, ISO-directive drafting so must/should is formal); Canada.ca (mandatory C&IA spec; the rare fully bilingual EN/FR rule set); Japan DADS (rare CJK-specific rules); KRDS Korea; secondary: Denmark, Norway (Digdir + NAV Aksel), Finland, Estonia Veera, Switzerland, Brazil GOVBR-DS, Singapore SGDS; Australia's official system decommissioned 2021, community successor GOLD (weaker authority now).

**Research organizations:** NN/g (10 heuristics + article corpus; methodology rarely published in full; strictly copyrighted); Baymard (the largest empirical rule base; premium catalogue paywalled, ~500 free articles).

**Corporate systems with prescriptive content guidance:** Shopify Polaris (strongest corporate content rules, do/don't pairs); Atlassian; IBM Carbon (Apache 2.0); Adobe Spectrum (writing-for-errors pages); GitHub Primer; GitLab Pajamas (unusually explicit do/don'ts); Salesforce Lightning (thin on copy rules).

**Writing/copy:** Microsoft Writing Style Guide (word-level falsifiable; © Microsoft); Google developer style guide (CC BY 4.0); plainlanguage.gov (public domain, statutory); ISO 24495-1 plain language (international, 19 languages, paywalled); non-English plain-language rule sets: Leichte Sprache (DIN SPEC 33429 — concrete sentence rules), FALC (French), Klarspråk (Sweden — legally required in public administration).

**Localization:** Mozilla l10n; W3C i18n; Unicode; Apple and Android localization guides (pseudolocale testing is itself a falsification method); Microsoft Globalization docs (text expansion ~40-70%).

**Accessibility beyond WCAG:** BBC Mobile Accessibility Guidelines; platform a11y docs (Android's 48dp + contentDescription rules are concrete); EN 301 549; Section 508 (restates WCAG 2.0 AA); RGAA (the test procedures).

**Interaction/forms specialists:** GOV.UK form patterns (today's strongest maintained set); Baymard; ISO 9241-143 (formal root); Luke Wroblewski's form research (empirical, aging, pre-mobile caveat); touch-target research roots (MIT Touch Lab; Parhi/Karlson/Bederson 2006) beneath the platform numbers.

**Boundary categories, noted so the boundary is chosen:** gaming (Xbox Accessibility Guidelines — 23 numbered, checkable; Game Accessibility Guidelines — community tiers); automotive HMI (NHTSA distraction guidelines — quantified glance budgets; ISO 15008/26022); aviation (FAA HF-STD-001 — massive public-domain quantified HCI rulebook, underused); medical (IEC 62366-1 — process, not artifact rules); voice (both platform guides frozen or deprecated — the category is decaying, out of scope).

## Editorial, readability and documentation clarity (surveyed 2026-08-17)

The doc lane's own catalogue, added when the doc laws arrived. Ranked by the same two criteria as everything above.

1. **ASD-STE100 Simplified Technical English** — issue 9 (2025): **53 numbered writing rules** plus a ~900-word controlled dictionary. The most falsifiable editorial standard in existence (sentence caps by text type, one instruction per sentence, one approved meaning per word) and a NUMBERED set, which makes it the next cost-blind census target. Access: free on request from ASD; do not quote until the official text is in hand — the rules are widely paraphrased and paraphrase is how fabrication starts. https://www.asd-ste100.org/
2. **Google developer documentation style guide** — CC BY 4.0, page-per-rule, already the root of four shipped laws. Census'd whole: `python -m craft.census_editorial`.
3. **GOV.UK writing guidelines** — the root of the sentence and paragraph ceilings and of say-it-once; the A-to-Z is a dictionary, not a ruleset, and is treated as one.
4. **Readability Guidelines (Content Design London)** — a community style guide with usability evidence attached per rule, plus a checklist page that is nearly a falsifier list. Wiki frozen since 2020, still served; cite the evidence page, not the rule alone. https://readabilityguidelines.co.uk/
5. **Federal plain language guidelines** — statutory (Plain Writing Act 2010), public domain; the canonical pages now live under digital.gov and several old plainlanguage.gov paths redirect or render client-side, so fetch carefully and keep the caught text.
6. **18F Content Guide** — US government, CC0, concrete do/don't pairs; a good operational second citation.
7. **Readability formulas** (Flesch, Flesch–Kincaid, SMOG) — research-rooted arithmetic over prose; WCAG's own Reading Level criterion (3.1.5) makes them law-adjacent, and they are decider material by construction.
8. **Diátaxis** — the tutorial/how-to/reference/explanation structure doctrine; falsifiable at the document-purpose level ("a tutorial that explains is failing"), weaker per-sentence. CC BY-SA.
9. **Microsoft Writing Style Guide** — word-level falsifiable, © Microsoft, quote briefly.
10. **EU "How to write clearly"** — multilingual (24 languages), free; useful as the non-English root the doc lane otherwise lacks.
11. **Write the Docs** — community practice, weak authority; mine for candidates, cite something stronger.

## Survey methodology (added 2026-08-19, with the-answers-span-the-question)

The discipline that studies closed questions — the natural root for every law about questions and answer sets rather than about controls, a lane the catalogue did not carry until a law needed it.

1. **Krosnick & Presser, Question and Questionnaire Design** (Handbook of Survey Research, 2010, ch. 9) — the conventional-wisdom list is eight numbered design principles («Make response options exhaustive and mutually exclusive» is item 5, quoted verbatim from the Stanford-hosted PDF); the rest of the chapter is the empirical case. Free, quotable, and the root of the-answers-span-the-question. https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2010/2010%20Handbook%20of%20Survey%20Research.pdf
2. **US federal statistical agencies** (BLS, Census) — public-domain empirical work on classification error when response options fail exhaustiveness; chase Bosley/Fricker/Gillman (BLS 2012) for the measured consequence before citing it.
3. **AAPOR best practices** — states the same requirement; only secondhand versions found so far, so it stays unquoted until the primary text is in hand — paraphrase is how fabrication starts.

## Gaps found (searched, thin)

Sweden and Spain lack national design systems with stated rules (Sweden has Klarspråk for language); voice UX has no living authoritative source; PlayStation/Nintendo guidelines are NDA'd; no third empirical org at NN/g/Baymard scale (academic HCI is paper-by-paper, not a catalogue); corporate content-design culture is anglophone — no non-English corporate style guide of note; Germany's KERN is real but young.

## The overlap map: always cite the strongest root

Accessibility → WCAG (rule), RGAA (test procedure), EN 301 549 (non-web clauses only). Touch targets → WCAG 2.5.5/2.5.8 + Apple 44pt / Material 48dp as platform roots. Forms → ISO 9241-143 (formal), GOV.UK + Baymard (empirical); NN/g, Polaris, Silver restate. Plain language → ISO 24495-1 (international), plainlanguage.gov (operational, public domain). Plurals/l10n → Unicode CLDR; Mozilla/Apple/Android/Microsoft operationalize. Keyboard → ARIA APG; HIGs copy its tables. Government systems → GOV.UK is the ancestor of NL, GOLD, NHS, Home Office, and influenced DSFR/DADS/KRDS: when two state the same rule, GOV.UK usually stated it first, with research. Heuristics → NN/g ≈ ISO 9241-110; ISO is the citable standard, NN/g the readable version.
