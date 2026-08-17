"""The third cost-blind census: every page of Google's documentation style guide.

The doc lane's turn. The guide is not numbered, so the census unit is the source's
own table of contents — every page, none skipped, including the ones that state no
rule (route `meta`, so the accounting stays whole). Page-level on purpose: a page
is the guide's own unit of prescription, and a finer grain would re-introduce the
picking hand the census exists to remove.

    python -m craft.census_editorial
    python -m craft.census_editorial --vocab
"""

from __future__ import annotations

CENSUS: dict[str, tuple[str, str]] = {
    # --- front matter ---------------------------------------------------------------
    "About this guide": ("meta", "states no rule"),
    "Highlights": ("meta", "an index of the rules, not a rule"),
    "What's new": ("meta", "a changelog"),
    "Philosophy of this guide": ("meta", "states no rule"),
    "Key resources": ("meta", "a link list"),
    "Word list": ("zero", "IS a wordlist — the voice/term machinery consumes it "
                          "directly"),
    "Product names": ("zero", "name-form decider against a declared list"),
    "Text-formatting summary": ("meta", "an index of other pages' rules"),
    # --- general principles ---------------------------------------------------------
    "Accessibility": ("zero", "restates the a11y family this catalogue already "
                              "roots in WCAG"),
    "Excessive claims": ("covered", "the voice kind's never-words: 'best', "
                                    "'world-class' are declared-off vocabulary"),
    "Future features": ("covered", "docs-do-not-date-themselves"),
    "Global audience": ("judge", "plain-construction advice; the mechanical "
                                 "edges live in the sentence and paragraph "
                                 "ceilings"),
    "Inclusive language": ("zero", "a wordlist — the voice kind's shape exactly"),
    "Jargon": ("covered", "terms-defined-before-use"),
    "Prescriptive documentation": ("meta", "meta-guidance about how to write "
                                          "guidance"),
    "Third-party content": ("meta", "policy, not prose rules"),
    "Timeless documentation": ("covered", "docs-do-not-date-themselves — its "
                                          "citation"),
    "Voice and tone": ("covered", "the voice kind"),
    # --- language and grammar -------------------------------------------------------
    "Abbreviations": ("covered", "acronyms-spell-out-on-first-reference — its "
                                 "citation"),
    "Active voice": ("judge", "passive detection by wordlist is a radar, not a "
                              "decider — a certain check would convict honest "
                              "passives"),
    "Anthropomorphism": ("judge", "whether 'the service wants' reads as "
                                  "anthropomorphic is a reading; a verb wordlist "
                                  "is radar material"),
    "Articles (a, an, the)": ("judge", "grammar judgment"),
    "Capitalization": ("zero", "sentence-case checks — "
                               "sentence-labels-take-sentence-case's machinery "
                               "over doc headings"),
    "Contractions": ("zero", "a wordlist decider"),
    "Pluralization": ("zero", "the parenthesised-plural decider already in the "
                              "estate"),
    "Possessives": ("judge", "grammar judgment"),
    "Prepositions": ("judge", "grammar judgment"),
    "Present tense": ("judge", "'will' is radar material — future tense is often "
                               "legitimate"),
    "Pronouns": ("covered", "speaks-to-you"),
    "Second person": ("covered", "speaks-to-you — its citation"),
    "Sentence structure": ("covered", "conditions-come-before-instructions — its "
                                      "citation"),
    "Verbs in reference documents": ("judge", "grammar judgment"),
    # --- punctuation ----------------------------------------------------------------
    "Colons": ("judge", "usage judgment"),
    "Commas": ("judge", "usage judgment; the serial-comma half is a decider "
                        "somebody could mint"),
    "Dashes": ("zero", "em-dash-with-spaces and hyphen-as-dash: pattern "
                       "deciders"),
    "Ellipses": ("zero", "a wordlist/pattern decider ('avoid in running text')"),
    "Hyphens": ("judge", "compound-word judgment"),
    "Parentheses": ("judge", "usage judgment"),
    "Periods and end punctuation": ("zero", "list-item and heading terminal "
                                           "punctuation: pattern deciders"),
    "Quotation marks": ("zero", "curly-vs-straight and placement: pattern"),
    "Semicolons": ("judge", "usage judgment"),
    "Slashes": ("zero", "'and/or' and date slashes: a wordlist decider"),
    # --- formatting and organization ------------------------------------------------
    "Dates and times": ("zero", "format patterns are deciders"),
    "Examples": ("judge", "whether an example teaches is a reading"),
    "Figures and other images": ("zero", "alt and caption requirements: the "
                                         "image family's checks"),
    "Footnotes": ("zero", "'avoid footnotes': a presence decider"),
    "Headings and titles": ("covered", "front-load-first-words + sentence-case "
                                       "machinery"),
    "Italics with terms": ("zero", "pattern over term introductions"),
    "Lists": ("zero", "structure checks are mechanical; parallelism stays a "
                      "reading"),
    "Mathematical notation": ("meta", "notation reference"),
    "Notes and other notices": ("zero", "notice-type vocabulary: pattern"),
    "Numbers": ("zero", "spell-below-ten and numeral patterns: deciders"),
    "Paragraphs": ("covered", "paragraphs-stay-under-five-sentences' family — "
                              "the guide says short, GOV.UK gives the number"),
    "Phone numbers": ("zero", "format pattern"),
    "Procedures": ("zero", "one-instruction-per-step and condition-first: "
                           "pattern + the conditions law"),
    "Tables": ("zero", "structure checks over markup"),
    "Units of measurement": ("zero", "format patterns"),
    # --- linking --------------------------------------------------------------------
    "Cross-references and linking": ("covered", "links-say-where-they-lead + "
                                                "internal-references-resolve"),
    "Headings as link targets": ("covered", "internal-references-resolve's "
                                            "anchor half"),
    # --- computer interfaces --------------------------------------------------------
    "API reference code comments": ("judge", "reference prose quality is a "
                                            "reading"),
    "Code in text": ("zero", "backtick-for-code: pattern decider"),
    "Code samples": ("vocab", "'test your samples' needs an `example` artifact "
                              "kind — an executable example the checks can run, "
                              "the doc lane's twin of the pinned scenes"),
    "Command-line syntax": ("zero", "placeholder and bracket patterns"),
    "Placeholder formatting": ("zero", "pattern decider"),
    "UI elements and interaction": ("zero", "bold-UI-names and click-vs-tap "
                                            "wordlists"),
    # --- html and css ---------------------------------------------------------------
    "HTML and semantic tagging": ("zero", "DOM checks"),
    "HTML formatting": ("zero", "markup patterns"),
    "Markdown versus HTML": ("meta", "a choice, not a rule over prose"),
    # --- names and naming -----------------------------------------------------------
    "Example domains and names": ("zero", "example.com/reserved-name wordlist"),
    "Filenames": ("zero", "filename patterns"),
    "Trademarks": ("zero", "a wordlist against a declared mark list"),
}

ROUTES = ("covered", "zero", "vocab", "judge", "meta")


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_editorial",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--vocab", action="store_true")
    args = ap.parse_args(argv)
    if args.vocab:
        for page, (route, note) in CENSUS.items():
            if route == "vocab":
                print(f"  {page}: {note}")
        return 0
    tally = Counter(route for route, _ in CENSUS.values())
    print(f"Google developer documentation style guide, every page of its own "
          f"table of contents: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    print("\n  the doc lane's shape: heavy on zero (wordlists and patterns), a "
          "real judge share (grammar), one vocabulary gap (executable "
          "examples), and the meta pages counted so the accounting is whole.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
