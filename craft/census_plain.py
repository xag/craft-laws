"""The Federal Plain Language Guidelines, re-read at the guideline grain and made checkable.

This source was already censused whole, in prose, on 2026-08-24: 44 rows in
docs/practice-sources.md, five laws minted from it that day. Nothing here reopens that
verdict. Two things this module adds, and it exists for the second one:

  * the routes become data, and every `covered` row names a law id that is CHECKED against
    laws.py and practice.py — so renaming a law breaks this census instead of silently
    orphaning the guideline it was carrying, the way census_agans already guards its nine;
  * the unit goes finer. The prose census grouped rows (III.a.3.i-ii, III.d.1-7, IV.a-g,
    all of V); this one carries the table of contents entry by entry, 65 of them, section
    headings included so the accounting is whole.

One route changed, and it is why the re-read happened. On 2026-08-31 the owner read a
report written in ornament - "the throttle brakes on engagement, not on emission", "the
gate doesn't bite" - and answered "Plain English please". III.a.3.i-ii (short simple
words; omit unnecessary words) had been routed `judge` in the first reading, on the ground
that necessity is a reading. That holds for a word in a document. It does not hold for an
answer written to one person who then says they could not read it: there the breach is
observable, and the observer is the person who asked. The row now roots
`an-answer-is-plain-on-first-reading`.

Everything else agrees with the first reading. Where this one says something the prose
census did not, the note says so in place.

    python -m craft.census_plain
    python -m craft.census_plain --vocab
"""

from __future__ import annotations

# route -> what it means, the five this repo's censuses share:
#   covered  an existing law states it; the law id is named and checked
#   zero     decidable with machinery the estate already has (a wordlist, a count, a pattern)
#   vocab    needs a fact nobody records yet — the artifact is named, and it is unbuilt
#   judge    stays a reading; never wired to a checker
#   meta     states no rule (front matter, a section heading, a case study)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- front matter ----------------------------------------------------------------
    "Introduction": ("meta", "", "states no rule"),
    "Revision 1 Changes": ("meta", "", "a changelog"),
    # --- I. Think about your audience -------------------------------------------------
    "I. Think about your audience": ("meta", "", "a section heading"),
    "I.a Identify and write for your audience": (
        "judge", "", "audience fit is a reading — the 2026-08-24 route, unchanged"),
    "I.b Address separate audiences separately": (
        "judge", "", "the same reading; whether two audiences were served separately is "
                     "read, not counted"),
    # --- II. Organize ------------------------------------------------------------------
    "II. Organize": ("meta", "", "a section heading"),
    "II.a Organize to meet your readers' needs": ("judge", "", "a reading"),
    "II.b Address one person, not a group": ("covered", "speaks-to-you", ""),
    "II.c Use lots of useful headings": (
        "covered", "front-load-first-words", "with the heading machinery behind it"),
    "II.d Write short sections": (
        "vocab", "", "the first reading's one OWED row, restated in this vocabulary: the "
                     "source gives no ceiling, and a length law without its number is a "
                     "taste. The missing fact is the number, and nobody has declared it"),
    # --- III. Write your document ------------------------------------------------------
    "III. Write your document": ("meta", "", "a section heading"),
    "III.a Words": ("meta", "", "a section heading"),
    "III.a.1 Verbs": ("meta", "", "a section heading"),
    "III.a.1.i Use active voice": (
        "judge", "", "passive detection by wordlist is radar, not a decider — the "
                     "editorial census's ruling, for which this source is the second root"),
    "III.a.1.ii Use the simplest form of a verb": ("judge", "", "grammar judgment"),
    "III.a.1.iii Avoid hidden verbs": ("covered", "a-verb-travels-as-a-verb", "minted 2026-08-24"),
    "III.a.1.iv Use \"must\" to indicate requirements": (
        "covered", "must-marks-a-requirement", "minted 2026-08-24"),
    "III.a.1.v Use contractions when appropriate": (
        "zero", "", "a wordlist decider, the editorial census's route"),
    "III.a.2 Nouns and pronouns": ("meta", "", "a section heading"),
    "III.a.2.i Don't turn verbs into nouns": (
        "covered", "a-verb-travels-as-a-verb", "the source states one rule twice"),
    "III.a.2.ii Use pronouns to speak directly to readers": ("covered", "speaks-to-you", ""),
    "III.a.2.iii Minimize abbreviations": (
        "covered", "acronyms-spell-out-on-first-reference", "decided in craft/prose.py"),
    "III.a.3 Other word issues": ("meta", "", "a section heading"),
    "III.a.3.i Use short, simple words": (
        "covered", "an-answer-is-plain-on-first-reading",
        "ROUTE CHANGED 2026-08-31, from judge. Fowler's five preferences, which this "
        "guideline quotes, are readings about a document and an observable about an "
        "answer: the person who asked says whether they could read it"),
    "III.a.3.ii Omit unnecessary words": (
        "covered", "an-answer-is-plain-on-first-reading",
        "ROUTE CHANGED 2026-08-31, from judge — the same law's second root"),
    "III.a.3.iii Dealing with definitions": ("covered", "terms-defined-before-use", ""),
    "III.a.3.iv Use the same term consistently for a specific thought or object": (
        "covered", "glossary-first",
        "the STRAYS check in craft/lexicon.py is this guideline mechanised"),
    "III.a.3.v Avoid legal, foreign, and technical jargon": (
        "covered", "no-system-vocabulary",
        "for what a screen says; an-answer-is-plain-on-first-reading carries what an "
        "assistant says. PLAIN's own gloss: 'used to impress, rather than to inform'"),
    "III.a.3.vi Don't use slashes": ("zero", "", "a character pattern"),
    "III.b Sentences": ("meta", "", "a section heading"),
    "III.b.1 Write short sentences": (
        "covered", "sentences-stay-under-twenty-five-words", ""),
    "III.b.2 Keep subject, verb, and object close together": (
        "judge", "", "no distance the source states, and no parse in the estate"),
    "III.b.3 Avoid double negatives and exceptions to exceptions": (
        "covered", "a-negative-is-not-stacked", "minted 2026-08-24"),
    "III.b.4 Place the main idea before exceptions and conditions": (
        "covered", "conditions-come-before-instructions", "second root"),
    "III.b.5 Place words carefully": ("judge", "", "a misplaced modifier is read, not counted"),
    "III.c Paragraphs": ("meta", "", "a section heading"),
    "III.c.1 Have a topic sentence": (
        "covered", "a-paragraph-opens-with-its-topic", "minted 2026-08-24"),
    "III.c.2 Use transition words": ("judge", "", "whether a joint needs marking is a reading"),
    "III.c.3 Write short paragraphs": (
        "covered", "paragraphs-stay-under-five-sentences", "decided in craft/prose.py"),
    "III.c.4 Cover only one topic in each paragraph": (
        "covered", "one-topic-per-paragraph", "minted 2026-08-24"),
    "III.d Other aids to clarity": ("meta", "", "a section heading"),
    "III.d.1 Use examples": (
        "vocab", "", "the `example` artifact census_editorial named for code samples: an "
                     "example that can be run, so a check can tell a live one from a stale one"),
    "III.d.2 Use lists": ("covered", "list-patterns-not-commas", ""),
    "III.d.3 Use tables to make complex material easier to understand": (
        "judge", "", "whether material needs a table is a reading"),
    "III.d.4 Consider using illustrations": ("judge", "", "the guideline says 'consider'"),
    "III.d.5 Use emphasis to highlight important concepts": (
        "judge", "", "which concept is important is a reading, and the source sets no "
                     "ceiling for the overuse half"),
    "III.d.6 Minimize cross-references": (
        "covered", "internal-references-resolve",
        "with references-name-their-target-not-its-position for the form half; the count "
        "half waits on a ceiling nobody has declared"),
    "III.d.7 Design your document for easy reading": ("covered", "type-stays-legible", ""),
    # --- IV. Write for the web ---------------------------------------------------------
    "IV. Write for the web": ("meta", "", "a section heading"),
    "IV.a How do people use the web?": ("meta", "", "background, not a rule"),
    "IV.b Write for your users": ("judge", "", "restates I.a as advice"),
    "IV.c Identify your users and their top tasks": (
        "judge", "", "set aside in the first reading as web-writing operations; kept there"),
    "IV.d Write web content": ("meta", "", "points back at section III"),
    "IV.e Repurpose print material for the web": ("judge", "", "a reading"),
    "IV.f Avoid PDF overload": (
        "judge", "", "set aside in the first reading; countable over a link inventory, "
                     "but the estate publishes no site this would run against"),
    "IV.g Use plain-language techniques on the web": ("meta", "", "points back at section III"),
    "IV.h Avoid meaningless formal language": (
        "zero", "", "a declared never-word list — the machinery the voice kind already "
                    "runs for excessive claims"),
    "IV.i Write effective links": ("covered", "links-say-where-they-lead", ""),
    # --- V. Test ------------------------------------------------------------------------
    "V. Test": ("meta", "", "a section heading"),
    "V.a Paraphrase Testing": (
        "vocab", "", "NEW IN THIS READING: the first census set all of V aside as method "
                     "rather than rule. Paraphrase testing does name an artifact the "
                     "estate lacks — a reader's restatement of a text, filed beside it, so "
                     "intent can be checked against what was understood. Screens are "
                     "tested this way here; prose is not tested at all"),
    "V.b Usability Testing": (
        "judge", "", "covered in doctrine by the walks and the blind-usability pipeline; "
                     "no law, because the source prescribes a method, not a breach"),
    "V.c Controlled Comparative Studies": (
        "judge", "", "the claims ledger's protocol and measurement kinds are this shape, "
                     "but the source prescribes a study, not an observable breach"),
    "V.d Testing Successes": ("meta", "", "case studies"),
    "V.d.1 Paraphrase Testing from the Veterans Benefits Administration": (
        "meta", "", "a case study"),
    "V.d.2 Usability Testing from the National Cancer Institute": ("meta", "", "a case study"),
}

ROUTES = ("covered", "zero", "vocab", "judge", "meta")


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_plain",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--vocab", action="store_true")
    args = ap.parse_args(argv)

    if args.vocab:
        for entry, (route, _law, note) in CENSUS.items():
            if route == "vocab":
                print(f"  {entry}: {note}")
        return 0

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {law.id for law in LAWS} | {law.id for law in PRACTICE}
    missing = [(entry, law) for entry, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]
    unnamed = [entry for entry, (route, law, _) in CENSUS.items()
               if route == "covered" and not law]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Federal Plain Language Guidelines (March 2011, Rev. 1 May 2011), every entry "
          f"of its own table of contents: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<8} {tally.get(route, 0)}")
    if unnamed:
        for entry in unnamed:
            print(f"\n  BROKEN  {entry} is covered and names no law")
        return 1
    if missing:
        for entry, law in missing:
            print(f"\n  BROKEN  {entry} names law {law!r} and no such law exists")
        return 1
    print(f"\n  Every covered entry names a law that exists — checked against laws.py and "
          f"practice.py, not asserted.\n"
          f"  Against the prose census of 2026-08-24 (44 grouped rows): one route changed "
          f"(III.a.3.i-ii, judge -> an-answer-is-plain-on-first-reading, after a reader "
          f"could not read a report) and one row is new (V.a, the unbuilt paraphrase "
          f"record). The rest agrees.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
