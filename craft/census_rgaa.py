"""The cost-blind census: every RGAA 4.1 criterion classified, none skipped.

The convergence series was accused, correctly, of selection bias: the miner picked
laws it could already see the compile route for, so a run of +0s measured the
sampling, not the vocabulary. The remedy is a census that is blind to cost — one
authoritative source's ENTIRE numbered set, every criterion accounted for, and the
distribution published whatever it says. RGAA 4.1 is the source: 106 numbered test
criteria, the most operationally falsifiable accessibility catalogue there is.

Each criterion gets one route:

  covered  a shipped craft law already carries the rule (the law is named)
  zero     expressible today at +0 vocabulary — the route is named (a decider, the
           DOM instrument, the layout solver, the model) but the law is NOT yet
           minted; the census is not a mining run
  vocab    NOT expressible today: the missing fact or kind is named. This is the
           category the biased series never met, and the reason it never met it is
           visible in the names — media, tables, dynamic reveals: content the
           estate's own apps do not have
  judge    a pertinence question — mechanics can hold the artifact, only a reader
           can hold its quality; the permanent residue, carried honestly

    python -m craft.census_rgaa          # the tallies, computed
    python -m craft.census_rgaa --vocab  # only what the vocabulary cannot yet say

Counts live nowhere but the run. The census is data so the next repin can re-ask
it; the day a `media` kind lands, criteria flip from vocab to zero here, visibly.
"""

from __future__ import annotations

# (route, note) per criterion. The headline texts are RGAA's own (Licence Ouverte);
# the notes are this census's judgment, made once, arguable line by line.
CENSUS: dict[str, tuple[str, str]] = {
    # --- 1. Images -------------------------------------------------------------------
    "1.1": ("zero", "alt present: the DOM instrument reads img/[role=img] attributes"),
    "1.2": ("zero", "area alt present: same instrument, same sweep"),
    "1.3": ("judge", "alt PERTINENT: quality of the words is a reading"),
    "1.4": ("vocab", "needs a `challenge` fact (CAPTCHA/test image) before anything "
                     "can trigger; pertinence stays a reading"),
    "1.5": ("vocab", "same `challenge` fact; then compiles — a challenge must offer "
                     "an alternative path, an invariant over the drawing"),
    "1.6": ("judge", "'si nécessaire' — whether a detailed description is owed is "
                     "a judgment about the image"),
    "1.7": ("judge", "description pertinent: a reading"),
    "1.8": ("covered", "no-text-baked-into-images (+ the per-locale digest decider)"),
    "1.9": ("zero", "figcaption association: DOM instrument"),
    # --- 2. Cadres -------------------------------------------------------------------
    "2.1": ("zero", "iframe title present: DOM instrument"),
    "2.2": ("judge", "frame title pertinent: a reading"),
    # --- 3. Couleurs -----------------------------------------------------------------
    "3.1": ("covered", "colour-is-never-the-only-signal (+ the grayscale decider)"),
    "3.2": ("zero", "text contrast: computed styles + luminance arithmetic — the "
                    "measured-premise route thumb-size already walks"),
    "3.3": ("zero", "UI component contrast: same arithmetic, same route"),
    # --- 4. Multimédia ---------------------------------------------------------------
    "4.1": ("zero", "the `media` kind (interface@0.4.0) declares alternatives as "
                    "resolvable references — 'a transcript exists' is a tree query"),
    "4.2": ("judge", "transcript pertinent: a reading (media is sayable now)"),
    "4.3": ("zero", "captions in the media kind's `alternatives`; presence compiles"),
    "4.4": ("judge", "subtitles pertinent: a reading"),
    "4.5": ("zero", "audiodescription in `alternatives`; presence compiles"),
    "4.6": ("judge", "audiodescription pertinent: a reading"),
    "4.7": ("judge", "media clearly identifiable: a reading, media-fact-triggered"),
    "4.8": ("zero", "the media kind's `temporal: False` says non-temporal media; "
                    "its alternative is a resolvable reference"),
    "4.9": ("judge", "alternative pertinent: a reading"),
    "4.10": ("zero", "the media kind's `autoplay` fact; compiles — sound started "
                     "by nobody must be controllable"),
    "4.11": ("zero", "the media kind's `controllable` fact plus the existing "
                     "event-probe route"),
    "4.12": ("zero", "same, `temporal: False`"),
    "4.13": ("zero", "media kind plus the DOM instrument"),
    # --- 5. Tableaux -----------------------------------------------------------------
    "5.1": ("zero", "the `table` kind's `complex` fact (interface@0.4.0) is the "
                    "seat for that authoring-time judgment; a complex table with "
                    "no summary binding then convicts"),
    "5.2": ("judge", "summary pertinent: a reading"),
    "5.3": ("zero", "layout table linearizes: DOM instrument reads source order"),
    "5.4": ("zero", "caption association: DOM instrument"),
    "5.5": ("judge", "table title pertinent: a reading"),
    "5.6": ("zero", "th/scope declared: DOM instrument, pure markup"),
    "5.7": ("zero", "cell-header association technique: DOM instrument"),
    "5.8": ("zero", "layout tables free of data-table markup: DOM instrument"),
    # --- 6. Liens --------------------------------------------------------------------
    "6.1": ("covered", "links-say-where-they-lead (pertinence residue stays a "
                       "reading, as the law itself says)"),
    "6.2": ("zero", "every link has an accessible name: every-input-labeled's link "
                    "sibling, DOM instrument"),
    # --- 7. Scripts ------------------------------------------------------------------
    "7.1": ("zero", "widget ARIA states/roles: DOM instrument; the 'si nécessaire' "
                    "half stays a reading"),
    "7.2": ("judge", "script alternative pertinent: a reading"),
    "7.3": ("covered", "touch-commits-on-release + one-tab-stop-per-widget + the "
                       "event probes — the operability family"),
    "7.4": ("vocab", "needs an `unprompted` fact on context changes; then compiles "
                     "against the action graph the model already holds"),
    "7.5": ("zero", "status messages via aria-live/role=status: DOM instrument, "
                    "status-is-visible's restitution half"),
    # --- 8. Éléments obligatoires ----------------------------------------------------
    "8.1": ("zero", "doctype present: repo-static"),
    "8.2": ("zero", "source valid for its doctype: a standard validator, run as an "
                    "instrument"),
    "8.3": ("covered", "language-declared"),
    "8.4": ("zero", "lang code valid and matching: decider against the catalogue's "
                    "own language list"),
    "8.5": ("covered", "the-title-names-the-place (presence half)"),
    "8.6": ("covered", "the-title-names-the-place (pertinence half, its stated "
                       "judge residue)"),
    "8.7": ("zero", "language changes marked: DOM + the walker knows both "
                    "catalogues' words"),
    "8.8": ("zero", "change-of-language code valid: same decider as 8.4"),
    "8.9": ("zero", "no presentational markup: DOM static"),
    "8.10": ("covered", "base-direction-in-markup"),
    # --- 9. Structuration ------------------------------------------------------------
    "9.1": ("zero", "heading hierarchy monotone and present: decider over the DOM; "
                    "whether the headings STRUCTURE the information stays a reading"),
    "9.2": ("zero", "landmark structure (header/nav/main/footer once): DOM"),
    "9.3": ("zero", "lists marked as lists: DOM"),
    "9.4": ("zero", "citations marked: DOM"),
    # --- 10. Présentation ------------------------------------------------------------
    "10.1": ("zero", "CSS controls presentation: repo-static"),
    "10.2": ("zero", "content survives styles-off: a bare-render walker lane, the "
                     "erring lane's pattern"),
    "10.3": ("judge", "comprehensible styles-off: a reading of that lane"),
    "10.4": ("covered", "text-survives-doubling"),
    "10.5": ("zero", "bg/fg declared together: static CSS check"),
    "10.6": ("zero", "links distinguishable from text: computed-style arithmetic"),
    "10.7": ("zero", "focus visible: focus-walk instrument reads outline/style "
                     "deltas"),
    "10.8": ("zero", "hidden content aria-coherent: DOM"),
    "10.9": ("covered", "instructions-point-by-name-not-by-place"),
    "10.10": ("judge", "its pertinence half: a reading"),
    "10.11": ("zero", "reflow at 320px without two-axis scroll: the layout solver "
                      "over measured premises — the fits machinery verbatim"),
    "10.12": ("zero", "text-spacing overrides survive: the doubling machinery with "
                      "spacing multipliers"),
    "10.13": ("zero", "the element's `reveals` fact (interface@0.4.0) says a "
                      "tooltip: dismissable, hoverable, persistent each compile"),
    "10.14": ("zero", "CSS-revealed content keyboard-reachable: event probe"),
    # --- 11. Formulaires -------------------------------------------------------------
    "11.1": ("covered", "every-input-labeled"),
    "11.2": ("judge", "label pertinent: the covered law's stated residue"),
    "11.3": ("covered", "one-act-one-name, applied to repeated fields"),
    "11.4": ("zero", "label adjacent to its field: box arithmetic, the layout "
                     "solver route"),
    "11.5": ("zero", "same-nature fields grouped: DOM fieldset presence; the 'si "
                     "nécessaire' stays a reading"),
    "11.6": ("zero", "grouping has a legend: DOM"),
    "11.7": ("judge", "legend pertinent: a reading"),
    "11.8": ("judge", "choice-list grouping pertinent: a reading"),
    "11.9": ("covered", "says-what-happens (pertinence residue a reading, as "
                        "stated)"),
    "11.10": ("covered", "the four error laws, evidenced by the erring lane"),
    "11.11": ("covered", "error-says-the-fix"),
    "11.12": ("covered", "check-before-commit (financial/legal: reversible, "
                         "checkable, confirmable)"),
    "11.13": ("covered", "the `collects` fact is exactly input purpose — the "
                         "autocomplete/keyboard family compiles from it"),
    # --- 12. Navigation --------------------------------------------------------------
    "12.1": ("vocab", "'two navigation systems' is a site-level fact no kind "
                      "carries — needs a navigation-systems declaration"),
    "12.2": ("covered", "navigation-keeps-its-order; the same-place half is box "
                        "arithmetic on the existing route"),
    "12.3": ("judge", "sitemap pertinent: a reading"),
    "12.4": ("zero", "sitemap reachable identically: site-static"),
    "12.5": ("zero", "search reachable identically: site-static"),
    "12.6": ("zero", "landmark regions skippable: DOM"),
    "12.7": ("zero", "skip link present: DOM (chores ships nav.skip today)"),
    "12.8": ("zero", "tab order coherent: the focus walk against visual order"),
    "12.9": ("covered", "no-keyboard-trap (model half proved per overlay in two "
                        "apps)"),
    "12.10": ("zero", "single-key shortcuts controllable: key-handler probe"),
    "12.11": ("zero", "hover/focus content keyboard-reachable: event probe (the "
                      "`reveals` fact of 10.13 would let it compile too)"),
    # --- 13. Consultation ------------------------------------------------------------
    "13.1": ("zero", "time limits controllable: the model's own idiom — a timed "
                     "transition is an action, the control invariant compiles"),
    "13.2": ("zero", "no unprompted window: the `opens` fact plus the instrument"),
    "13.3": ("vocab", "downloadable office documents: no artifact kind says a "
                      "document travels with the interface"),
    "13.4": ("judge", "accessible version equivalent: a reading"),
    "13.5": ("judge", "cryptic content (ASCII art, emoticons) detection is itself "
                      "a judgment — a decider would convict art and miss art"),
    "13.6": ("judge", "its alternative's pertinence: a reading"),
    "13.7": ("zero", "flash/luminance limits: shot arithmetic over frames"),
    "13.8": ("zero", "moving/blinking controllable: animation probe — mineable at "
                     "+0, not yet mined"),
    "13.9": ("covered", "works-both-ways-up"),
    "13.10": ("covered", "gesture-has-a-plain-alternative"),
    "13.11": ("covered", "touch-commits-on-release"),
    "13.12": ("zero", "the element's `motion` fact (interface@0.4.0) says an act "
                      "listens to device motion, names its conventional "
                      "alternative, and says whether it can be turned off"),
}

ROUTES = ("covered", "zero", "vocab", "judge")


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_rgaa",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--vocab", action="store_true",
                    help="print only what the vocabulary cannot yet say")
    args = ap.parse_args(argv)

    if args.vocab:
        for num, (route, note) in CENSUS.items():
            if route == "vocab":
                print(f"  {num:<6} {note}")
        return 0

    tally = Counter(route for route, _ in CENSUS.values())
    print(f"RGAA 4.1, every criterion, none skipped: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    facts = sorted({note.split("`")[1] for route, note in CENSUS.values()
                    if route == "vocab" and "`" in note})
    print(f"\n  missing facts/kinds named by the vocab rows: "
          f"{', '.join(facts) if facts else '(see notes)'}")
    print("\n  (this census is cost-blind on purpose: the biased series measured "
          "the miner's sampling, this measures the vocabulary — see "
          "docs/mechanization.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
