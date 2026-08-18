"""The second cost-blind census: every WCAG 2.2 success criterion, none skipped.

The convergence falsifier's own cadence demands a second source before any public
claim — this is it. All 87 success criteria of WCAG 2.2 (every level, A through
AAA, including the one the spec itself removed), each classified against the
current vocabulary exactly as the RGAA census classifies its 106: covered / zero /
vocab / judge, with the route or the missing kind named.

    python -m craft.census_wcag
    python -m craft.census_wcag --vocab

The two censuses overlap by design — RGAA is WCAG operationalized — so their vocab
buckets should name the SAME missing kinds. If they do not, one census is wrong,
which is itself a finding.
"""

from __future__ import annotations

CENSUS: dict[str, tuple[str, str, str]] = {
    # num: (name, route, note)
    "1.1.1": ("Non-text Content", "zero",
              "alt sweep via the DOM instrument; pertinence stays a reading"),
    "1.2.1": ("Audio-only and Video-only (Prerecorded)", "zero",
              "the `media` kind (interface@0.4.0): alternatives are resolvable "
              "references, presence compiles"),
    "1.2.2": ("Captions (Prerecorded)", "zero",
              "captions in the media kind's `alternatives`"),
    "1.2.3": ("Audio Description or Media Alternative", "zero",
              "either alternative in the same list"),
    "1.2.4": ("Captions (Live)", "zero", "the `live` fact narrows the trigger"),
    "1.2.5": ("Audio Description (Prerecorded)", "zero", "same route"),
    "1.2.6": ("Sign Language (Prerecorded)", "zero",
              "sign-language in `alternatives`"),
    "1.2.7": ("Extended Audio Description", "zero", "same route"),
    "1.2.8": ("Media Alternative (Prerecorded)", "zero",
              "media-alternative in `alternatives`"),
    "1.2.9": ("Audio-only (Live)", "zero", "`live` plus `temporal`"),
    "1.3.1": ("Info and Relationships", "zero",
              "structure carried in markup: DOM instrument over headings, lists, "
              "tables, label associations"),
    "1.3.2": ("Meaningful Sequence", "zero",
              "source order vs visual order: the linearization check"),
    "1.3.3": ("Sensory Characteristics", "covered",
              "instructions-point-by-name-not-by-place"),
    "1.3.4": ("Orientation", "covered", "works-both-ways-up"),
    "1.3.5": ("Identify Input Purpose", "covered",
              "the `collects` fact is input purpose; the autocomplete family "
              "compiles from it"),
    "1.3.6": ("Identify Purpose", "zero",
              "landmark/purpose semantics: DOM instrument"),
    "1.4.1": ("Use of Color", "covered", "colour-is-never-the-only-signal"),
    "1.4.2": ("Audio Control", "zero",
              "the media kind's `autoplay` fact (interface@0.4.0); compiles"),
    "1.4.3": ("Contrast (Minimum)", "zero",
              "luminance arithmetic over computed styles — the measured-premise "
              "route"),
    "1.4.4": ("Resize Text", "covered", "text-survives-doubling"),
    "1.4.5": ("Images of Text", "covered", "no-text-baked-into-images"),
    "1.4.6": ("Contrast (Enhanced)", "zero", "same arithmetic, higher ratio"),
    "1.4.7": ("Low or No Background Audio", "judge",
              "the media kind gives it a trigger; the mix itself is a listening"),
    "1.4.8": ("Visual Presentation", "zero",
              "line length, spacing, justification: layout premises + computed "
              "styles"),
    "1.4.9": ("Images of Text (No Exception)", "covered",
              "no-text-baked-into-images, stricter trigger"),
    "1.4.10": ("Reflow", "zero",
               "the layout solver at 320px — the fits machinery verbatim"),
    "1.4.11": ("Non-text Contrast", "zero",
               "component contrast: the same luminance arithmetic"),
    "1.4.12": ("Text Spacing", "zero",
               "the doubling machinery with spacing multipliers"),
    "1.4.13": ("Content on Hover or Focus", "zero",
               "the element's `reveals` fact (interface@0.4.0): dismissable, "
               "hoverable, persistent each compile"),
    "2.1.1": ("Keyboard", "zero",
              "operability via the event and focus probes"),
    "2.1.2": ("No Keyboard Trap", "covered",
              "no-keyboard-trap — model half proved per overlay in two apps"),
    "2.1.3": ("Keyboard (No Exception)", "zero", "2.1.1 without the exception"),
    "2.1.4": ("Character Key Shortcuts", "zero", "key-handler probe"),
    "2.2.1": ("Timing Adjustable", "zero",
              "a timed transition is an action in the model; the control "
              "invariant compiles"),
    "2.2.2": ("Pause, Stop, Hide", "zero",
              "the animation probe — mineable, not yet mined"),
    "2.2.3": ("No Timing", "zero",
              "an invariant over the action graph: no timed transitions at all"),
    "2.2.4": ("Interruptions", "vocab",
              "needs the `unprompted` fact on content changes"),
    "2.2.5": ("Re-authenticating", "vocab",
              "needs a `preserves` fact: data survives the re-auth"),
    "2.2.6": ("Timeouts", "zero",
              "a warning element gated on the timeout state variable: drawing + "
              "model"),
    "2.3.1": ("Three Flashes or Below Threshold", "zero",
              "luminance-delta arithmetic over frames"),
    "2.3.2": ("Three Flashes", "zero", "same, stricter"),
    "2.3.3": ("Animation from Interactions", "zero",
              "motion probe + prefers-reduced-motion check"),
    "2.4.1": ("Bypass Blocks", "zero", "skip link and landmarks: DOM"),
    "2.4.2": ("Page Titled", "covered", "the-title-names-the-place"),
    "2.4.3": ("Focus Order", "zero", "the focus walk against visual order"),
    "2.4.4": ("Link Purpose (In Context)", "covered",
              "links-say-where-they-lead"),
    "2.4.5": ("Multiple Ways", "vocab",
              "the site-level navigation-systems declaration RGAA 12.1 also "
              "wants"),
    "2.4.6": ("Headings and Labels", "judge",
              "descriptiveness is a reading; front-load and says-what-happens "
              "hold the mechanical edges"),
    "2.4.7": ("Focus Visible", "zero", "focus style probe"),
    "2.4.8": ("Location", "zero",
              "breadcrumb/location presence: DOM over the nav structure"),
    "2.4.9": ("Link Purpose (Link Only)", "covered",
              "links-say-where-they-lead, stricter"),
    "2.4.10": ("Section Headings", "zero", "headings per section: DOM"),
    "2.4.11": ("Focus Not Obscured (Minimum)", "zero",
               "focused box not covered: layout arithmetic + focus walk"),
    "2.4.12": ("Focus Not Obscured (Enhanced)", "zero", "same, no exception"),
    "2.4.13": ("Focus Appearance", "zero", "focus outline arithmetic"),
    "2.5.1": ("Pointer Gestures", "covered", "gesture-has-a-plain-alternative"),
    "2.5.2": ("Pointer Cancellation", "covered", "touch-commits-on-release"),
    "2.5.3": ("Label in Name", "zero",
              "accessible name contains the visible label: a decider over the "
              "DOM"),
    "2.5.4": ("Motion Actuation", "zero",
              "the element's `motion` fact (interface@0.4.0): names the "
              "conventional alternative and whether it can be turned off"),
    "2.5.5": ("Target Size (Enhanced)", "covered",
              "targets-are-thumb-sized machinery at the 44px floor"),
    "2.5.6": ("Concurrent Input Mechanisms", "zero",
              "no input-type lockout: event probe"),
    "2.5.7": ("Dragging Movements", "covered",
              "gesture-has-a-plain-alternative's shape: a drag needs a "
              "single-pointer alternative"),
    "2.5.8": ("Target Size (Minimum)", "covered",
              "targets-are-thumb-sized — this criterion is its citation"),
    "3.1.1": ("Language of Page", "covered", "language-declared"),
    "3.1.2": ("Language of Parts", "zero",
              "lang spans: DOM + the catalogues' own language list"),
    "3.1.3": ("Unusual Words", "judge",
              "the glossary's strays are the mechanical edge; 'unusual' for an "
              "audience is a reading"),
    "3.1.4": ("Abbreviations", "covered",
              "acronyms-spell-out-on-first-reference, the doc lane's law"),
    "3.1.5": ("Reading Level", "zero",
              "readability formulas are arithmetic over prose — a decider "
              "nobody has minted yet"),
    "3.1.6": ("Pronunciation", "vocab",
              "pronunciation/ruby semantics: no kind carries them"),
    "3.2.1": ("On Focus", "zero",
              "no context change on focus: event probe + the action graph"),
    "3.2.2": ("On Input", "zero", "same for input"),
    "3.2.3": ("Consistent Navigation", "covered", "navigation-keeps-its-order"),
    "3.2.4": ("Consistent Identification", "covered", "one-act-one-name"),
    "3.2.5": ("Change on Request", "zero",
              "every context change rides a user action: the model's own idiom"),
    "3.2.6": ("Consistent Help", "zero",
              "help element in the same relative order: the nav machinery "
              "reused"),
    "3.3.1": ("Error Identification", "covered",
              "error-names-the-culprit, evidenced by the erring lane"),
    "3.3.2": ("Labels or Instructions", "covered", "every-input-labeled"),
    "3.3.3": ("Error Suggestion", "covered", "error-says-the-fix"),
    "3.3.4": ("Error Prevention (Legal, Financial, Data)", "covered",
              "check-before-commit"),
    "3.3.5": ("Help", "zero",
              "context help presence per form: drawing + DOM"),
    "3.3.6": ("Error Prevention (All)", "covered",
              "check-before-commit, generalized trigger"),
    "3.3.7": ("Redundant Entry", "covered",
              "never-ask-twice — this criterion is its citation"),
    "3.3.8": ("Accessible Authentication (Minimum)", "vocab",
              "the `challenge` fact RGAA's CAPTCHA rows also want"),
    "3.3.9": ("Accessible Authentication (Enhanced)", "vocab", "same"),
    "4.1.1": ("Parsing (obsolete, removed in 2.2)", "zero",
              "kept so the census is the whole numbered set; a validator settles "
              "what remains of it"),
    "4.1.2": ("Name, Role, Value", "zero", "ARIA states and roles: DOM"),
    "4.1.3": ("Status Messages", "zero",
              "aria-live/role=status: DOM — status-is-visible's restitution "
              "half"),
}

ROUTES = ("covered", "zero", "vocab", "judge")


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_wcag",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--vocab", action="store_true")
    args = ap.parse_args(argv)
    if args.vocab:
        for num, (name, route, note) in CENSUS.items():
            if route == "vocab":
                print(f"  {num:<8} {name}: {note}")
        return 0
    tally = Counter(route for _, route, _ in CENSUS.values())
    print(f"WCAG 2.2, every success criterion, every level, none skipped: "
          f"{len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    facts = sorted({note.split("`")[1] for _, route, note in CENSUS.values()
                    if route == "vocab" and "`" in note})
    print(f"\n  missing facts/kinds named: {', '.join(facts)}")
    print("  cross-check: these should be the RGAA census's names — two blind "
          "samples, one boundary. Run both; compare.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
