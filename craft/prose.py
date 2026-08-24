"""The prose deciders: the documentation laws' checks, run on files instead of walks.

Documentation is the lane machine edits damage most and machines checked least: an
edit appends instead of integrating, restates what a neighbouring paragraph already
says, points 'above' at a paragraph that moved, defines a term three sections after
using it — and until this module, every one of those was found by a person rereading
the whole document. These are pure functions over markdown text, one per decidable
documentation law, with the decider discipline throughout: convict with certainty
or stay silent, and never guess.

    python -m craft.prose README.md docs/*.md
    python -m craft.prose --alarm

The `--alarm` form runs every check against a convicting example and a clean one
and exits 1 if any alarm is dead — a checker that has never been seen red is
relocated guessing. What stays with a reader, on purpose: whether a repetition is
rhetorical, whether the flow of an argument survives an edit, whether a heading
keeps its section's promise. The checks below take the mechanical share so the
reader's attention is spent only where reading is the instrument.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from craft.laws import LAWS

_LAW_IDS = {law.id for law in LAWS}


# --- language is a parameter of the DATA, never of the machinery ---------------------
#
# The shape craft/lexicon.py already uses for terms and voices, brought here because this
# lane did not have it: every rule table below is keyed by language, and a decider whose
# table has no entry for the document's language DOES NOT RUN and is reported by
# unruled(). That report is the whole point. A word list that speaks only English,
# pointed at a French README, finds nothing -- and "found nothing" is byte-identical to
# "this document is clean". This repository's founding defect was a French screen that
# every green check had missed, so a lane that goes quiet in French is the same failure
# wearing the same green.
#
# The language is DECLARED (--lang, default "en"), never sniffed. Guessing a document's
# language from its bytes is a prediction, and a prediction that is wrong reports the
# wrong rules as authoritative rather than reporting that it has none.
#
# Three deciders need no language at all and always run: check_anchors (markdown
# structure), check_repetition (two spans of text are equal or they are not), and
# check_paragraph_length (counting stops between .!?). The last is Latin-script rather
# than universal, and its abbreviation guard is per-language: without one it over-counts
# sentences, which is a false positive a reader can see, not a silence they cannot.

@dataclass
class DocFinding:
    law: str
    where: str       # file and paragraph ordinal, so the quote can be found again
    quote: str
    why: str


def _law(law_id: str) -> str:
    if law_id not in _LAW_IDS:
        raise ValueError(f"no law '{law_id}' in craft@")
    return law_id


# --- markdown, reduced to what the laws read -----------------------------------------

_FENCE = re.compile(r"^(```|~~~)")
_HEADING = re.compile(r"^#{1,6}\s+(.*)$")
# A bullet marker is a marker only when whitespace follows it. Without that space the `**` of
# a bold run read as a bullet, so EVERY paragraph opening in bold left the prose lane before
# any decider saw it -- and the checks then reported green over text they had never been
# handed, which is worse than reporting nothing. Thematic breaks are matched on their own:
# they carry no space either, and they genuinely are not prose.
_NONPROSE = re.compile(r"^(\s*([-*+]\s|\d+\.\s|\||>)|\s*[-*_]{3,}\s*$|\s*$)")
_INLINE_CODE = re.compile(r"`[^`]*`")
_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
# sentence-splitter guards: dots that end no sentence. Keyed by language like every
# other rule table here -- an abbreviation list is a fact about a language, and using
# English's on French text splits « cf. » into two sentences and over-counts.
_ABBREV = {
    "en": re.compile(r"\b(e\.g|i\.e|vs|etc|cf|Mr|Ms|Dr|St|no)\.", re.IGNORECASE),
}


def paragraphs(text: str) -> list[tuple[int, str]]:
    """(ordinal, prose) per prose paragraph — code fences, headings, lists, tables
    and quotes are not prose and are not judged as prose."""
    out: list[tuple[int, str]] = []
    block: list[str] = []
    in_fence = False
    n = 0
    for line in text.splitlines() + [""]:
        if _FENCE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.strip() and not _NONPROSE.match(line) and not _HEADING.match(line):
            block.append(line.strip())
            continue
        if block:
            n += 1
            out.append((n, " ".join(block)))
            block = []
    return out


# A paragraph may open with a RUN-IN HEADING -- `**Pointers.** A reference to an entry...`.
# Markdown has no syntax for one, so authors write bold, and the splitter counted the label as a
# sentence: every labelled paragraph started with four of its five sentences left, and the
# paragraph law convicted the signpost rather than the density it is about. Same family as the
# `**` that read as a bullet -- a structural device mistaken for content.
#
# Two things must both hold, or it is not a label: the bold run ends the way a label ends, and
# PROSE FOLLOWS IT in the same paragraph. A paragraph that is one whole bold sentence is a
# sentence and stays one. The six-word bound is what keeps an emphasised opening SENTENCE from
# being swallowed as a heading; a real run-in heading is a couple of words.
_RUN_IN = re.compile(r"^\*\*(?P<label>[^*]+?[.!?:])\*\*\s+(?=\S)")


def _strip_run_in(prose: str) -> str:
    m = _RUN_IN.match(prose)
    return prose[m.end():] if m and len(m.group("label").split()) <= 6 else prose


def sentences(prose: str, lang: str = "en") -> list[str]:
    # markdown notation comes off first: a '?' closed by an italic marker is still
    # the end of a sentence, and the first version of this splitter missed it
    plain = _plain(_strip_run_in(prose))
    abbrev = _ABBREV.get(lang)
    guarded = (abbrev.sub(lambda m: m.group(0).replace(".", "․"), plain)
               if abbrev else plain)
    # a period inside a closing quote or bracket still ends the sentence
    parts = re.split(r"(?<=[.!?])[\"'”’)\]]*\s+", guarded)
    return [p.replace("․", ".").strip() for p in parts if p.strip()]


def _plain(prose: str) -> str:
    """Prose with markdown notation removed, so word counts count words."""
    s = _INLINE_CODE.sub(" ", prose)
    s = _MD_LINK.sub(lambda m: m.group(1), s)
    return re.sub(r"[*_]{1,3}", "", s)


# --- the deciders --------------------------------------------------------------------

def check_paragraph_length(name: str, text: str, root: Path | None = None,
                           lang: str = "en", ceiling: int = 5) -> list[DocFinding]:
    """paragraphs-stay-under-five-sentences (GOV.UK: 'no more than 5 sentences
    each')."""
    law = _law("paragraphs-stay-under-five-sentences")
    out = []
    for n, prose in paragraphs(text):
        count = len(sentences(prose, lang))
        if count > ceiling:
            out.append(DocFinding(
                law=law, where=f"{name} ¶{n}",
                quote=_plain(prose)[:100] + "…",
                why=f"{count} sentences in one paragraph, against the ceiling of "
                    f"{ceiling} — split it, or let a reader defend it."))
    return out


# sentences-stay-under-twenty-five-words HAS NO DECIDER HERE, and it is not an oversight.
# It is an INTERFACE law: its statement says 'interface prose', its falsifier says 'a sentence
# in UI copy', and its trigger is 'the app's voice does work of its own (dry, terse, no
# explaining text)'. None of that fires on a README. Every other decider in this lane runs a
# law whose trigger names documentation read long after it is written; this one was picked
# because it was countable, which is a property of the check and not of the law.
#
# The same mistake was made in craft/answer.py and fixed there (claims.jsonl: 'the law set was
# chosen by keyword - is this law about words - instead of by reading each law's trigger').
# It survived here because each caller hand-picks its own set, which is the recorded debt
# triggers-are-prose-so-applicability-cannot-be-computed: 'selecting by keyword picks laws
# whose own statements name a different surface'. Until a trigger is an expression, the only
# defence is to read the trigger of every law a lane runs. The eight above were read.
#
# The source it came from says 'TRY to split up sentences that are over 25 words long' -
# guidance for public service copy, with deliberate exceptions going to a judge. It was wired
# as an unconditional counter with no judge, twice.


_TIME_ANCHORS = {
    "en": ("currently", "at the time of writing", "coming soon",
           "will soon", "recently added", "as of today"),
}


def check_time_anchors(name: str, text: str, root: Path | None = None,
                       lang: str = "en") -> list[DocFinding]:
    """docs-do-not-date-themselves: the words that anchor a document to the day it
    was written."""
    law = _law("docs-do-not-date-themselves")
    anchors = _TIME_ANCHORS.get(lang)
    if anchors is None:
        return []                    # no rules for this language; unruled() says so
    out = []
    for n, prose in paragraphs(text):
        low = _plain(prose).lower()
        for word in anchors:
            if re.search(rf"\b{re.escape(word)}\b", low):
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}", quote=word,
                    why="a sentence pre-written to go stale — describe what the "
                        "product is, not how it just changed."))
    return out


_POSITIONAL = {
    "en": (r"\bas (mentioned|described|noted|shown|discussed) "
           r"(above|earlier|previously)\b",
           r"\bsee (above|below)\b",
           r"\b(the|this) section (above|below)\b",
           r"\bmentioned (above|below)\b"),
}


def check_positional_references(name: str, text: str, root: Path | None = None,
                               lang: str = "en") -> list[DocFinding]:
    """references-name-their-target-not-its-position: 'above' breaks the day a
    paragraph moves, which is every day a machine edits."""
    law = _law("references-name-their-target-not-its-position")
    patterns = _POSITIONAL.get(lang)
    if patterns is None:
        return []                    # no rules for this language; unruled() says so
    out = []
    for n, prose in paragraphs(text):
        low = _plain(prose).lower()
        for pat in patterns:
            m = re.search(pat, low)
            if m:
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}", quote=m.group(0),
                    why="a positional reference — name the section instead, so the "
                        "reference survives the next edit that moves things."))
    return out


def check_repetition(name: str, text: str, root: Path | None = None,
                     lang: str = "en", floor_words: int = 8) -> list[DocFinding]:
    """say-it-once: two sentences saying the same thing in the same words — the
    signature of an edit appended instead of integrated. Convicts only on a
    normalized exact match of a substantial sentence: certainty, not similarity."""
    law = _law("say-it-once")
    seen: dict[str, str] = {}
    out = []
    for n, prose in paragraphs(text):
        for s in sentences(prose, lang):
            norm = re.sub(r"[^a-z0-9 ]", "", _plain(s).lower())
            norm = " ".join(norm.split())
            if len(norm.split()) < floor_words:
                continue
            if norm in seen:
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}",
                    quote=_plain(s)[:120],
                    why=f"already said, word for word, at {seen[norm]} — an edit "
                        "integrated nothing and the reader now wonders which copy "
                        "is current."))
            else:
                seen[norm] = f"{name} ¶{n}"
    return out


# Standard short forms the audience reads faster than their expansions — the
# source's own carve-out, carried visibly. Split in two because the halves are not the
# same kind of fact: the technical set travels between languages unchanged (a French
# README says API and JSON too), while the prose words are English and have French
# counterparts nobody has written down.
_ACRONYM_TECHNICAL = frozenset({
    "API", "URL", "URI", "JSON", "JSONL", "HTML", "CSS", "HTTP", "HTTPS", "CLI",
    "CI", "CD", "PDF", "README", "TODO", "UI", "UX", "SDK", "ID", "IDS", "OK",
    "FAQ", "RTL", "LTR", "ASCII", "UTF", "PNG", "SVG", "DOM", "SEO", "MIT",
    "AI", "LLM", "MCP",
})

_ACRONYM_PROSE = {
    "en": frozenset({"NOTE", "WARNING", "MUST", "SHOULD", "MAY", "NOT"}),
}


def acronym_exempt(lang: str) -> frozenset[str]:
    """What this language leaves alone: the shared technical set plus its own words."""
    return _ACRONYM_TECHNICAL | _ACRONYM_PROSE.get(lang, frozenset())


def check_acronyms(name: str, text: str, root: Path | None = None,
                   lang: str = "en") -> list[DocFinding]:
    """acronyms-spell-out-on-first-reference — the certain half: an acronym the
    document itself later expands with '(ACRO)' was, provably, this document's own
    term to introduce, and every bare use before that expansion met a reader who
    had not been told. An acronym never expanded anywhere is left to a reader:
    it may be as standard as the exempt list's."""
    law = _law("acronyms-spell-out-on-first-reference")
    plain = "\n".join(p for _, p in paragraphs(text))
    exempt = acronym_exempt(lang)
    out = []
    for m in re.finditer(r"\(([A-Z][A-Za-z]{1,7})\)", plain):
        acro = m.group(1)
        if acro.upper() in exempt or not acro.isupper():
            continue
        first_bare = re.search(rf"\b{acro}\b", plain)
        if first_bare and first_bare.start() < m.start() - len(acro) - 2:
            out.append(DocFinding(
                law=law, where=name, quote=acro,
                why=f"used bare before the sentence that expands it as "
                    f"'({acro})' — the definition exists and arrives too late."))
    return out


_TRAILING = {
    "en": (r"^see .{3,80} for more information\.?$",
           r"^(click|run|use|call|open|press|select)\b[^.]*\bif you want\b"),
}


def check_trailing_conditions(name: str, text: str, root: Path | None = None,
                              lang: str = "en") -> list[DocFinding]:
    """conditions-come-before-instructions: the source's own not-recommended
    shapes, matched as patterns."""
    law = _law("conditions-come-before-instructions")
    patterns = _TRAILING.get(lang)
    if patterns is None:
        return []                    # no rules for this language; unruled() says so
    out = []
    for n, prose in paragraphs(text):
        for s in sentences(prose, lang):
            low = _plain(s).lower().strip()
            for pat in patterns:
                if re.match(pat, low):
                    out.append(DocFinding(
                        law=law, where=f"{name} ¶{n}", quote=_plain(s)[:100],
                        why="the condition trails the instruction — lead with "
                            "the goal, so a reader it does not concern can "
                            "skip."))
    return out


def _slug(heading: str) -> str:
    s = _INLINE_CODE.sub(lambda m: m.group(0).strip("`"), heading)
    s = re.sub(r"[*_`]", "", s).strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def check_anchors(name: str, text: str, root: Path | None = None,
                  lang: str = "en") -> list[DocFinding]:
    """internal-references-resolve: every anchor matches a heading, every relative
    link a file. The doc-lane twin of drift."""
    law = _law("internal-references-resolve")
    slugs = {_slug(m.group(1)) for m in
             (_HEADING.match(line) for line in text.splitlines()) if m}
    out = []
    for m in _MD_LINK.finditer(text):
        target = m.group(2)
        if target.startswith("#"):
            if target[1:].lower() not in slugs:
                out.append(DocFinding(
                    law=law, where=name, quote=target,
                    why="an anchor with no matching heading — it scrolls nowhere."))
        elif root is not None and not re.match(r"^[a-z]+:", target):
            if not (root / target.split("#")[0]).exists():
                out.append(DocFinding(
                    law=law, where=name, quote=target,
                    why="a relative link to a file that is not there."))
    return out


# terms-defined-before-use HAS NO DECIDER, and this note is why it should not get the
# one it used to have. That check took the document's terms as a comma-separated string
# typed at the call site, and identified a term's DEFINITION as its first **bold**
# occurrence -- a typographic convention no document here ever declared, and one this
# repo's own README breaks (**data a machine can check** is emphasis, not a definition).
#
# The consequence was worse than the crudeness. `if bold and plain_use and ...` means a
# term that is NEVER defined -- the maximal breach of 'a reader never meets a word whose
# definition is still ahead of them' -- produced no finding at all. It convicted documents
# that had followed the convention and stayed silent on the ones that had not, which is
# precision bought by aiming away from the violation. It also convicted this repo on its
# own H1, because `laws?` matches after the hyphen in `craft-laws`.
#
# The law states the mechanism it actually wants: the terms are DECLARED, the way
# interface@'s `term` kind declares the app's glossary. Until a document declares its own
# coinages, this one is read by a person. See a-word-list-is-a-reading-not-a-mechanization.


# --- the deciders, as data ------------------------------------------------------------
#
# A tuple, not a hand-written call list, and the same tuple the alarm walks. This is the
# shape craft/claims.py already uses, copied rather than re-invented: adding a decider is
# one entry, and the alarm then DEMANDS a violation of it in the guilty document or
# reports itself dead. The red example stops being something a person remembers to write.
# Every decider takes (name, text, root) so the loop needs no special case for the one
# that reads the filesystem.

CHECKS = (check_paragraph_length, check_time_anchors, check_positional_references,
          check_repetition, check_acronyms, check_trailing_conditions, check_anchors)

# --- what may hold a handback, and what may only report -------------------------------
#
# a-word-list-is-a-reading-not-a-mechanization: "A law checked by matching words in prose
# is unmechanized, and says so - it does not get a decider, and it never holds a
# handback." Three of the checks above are exactly that shape, and for a week they gated
# this repository's build in contradiction of its own decision.
#
# MEASURED BEFORE DEMOTING, because the decision was made on a number and these three had
# none (2026-08-24, 87 markdown files across the estate):
#
#   time-anchors 2 hits, positional 1, trailing 0 - three in eighty-seven files
#   two of the three are LAWS.md convicting the law's own statement: "never 'now', no
#   'new', no 'currently'" and "never 'above', 'below', or 'as mentioned earlier'"
#   on the 31 READMEs the build actually gates: one hit, arguably true
#
# So they are not wrong seven times in eight. They are nearly inert, and wrong two times
# in three when they fire - and the false positives are STRUCTURAL rather than tunable: a
# rule that forbids a word cannot be written down without using it, so any wordlist law
# convicts its own statement and every document that discusses it. No word list escapes
# that, which is the decision's point restated by measurement.
#
# The remedy is the decision's own: they keep running and reporting, and they stop holding
# the build. A reading that fires once in eighty-seven files is worth a reader's glance and
# is not worth a red build, and the exit status is the difference between the two.
READINGS = frozenset({check_time_anchors, check_positional_references,
                      check_trailing_conditions})


def holds_the_build(check) -> bool:
    """Structural checks convict; readings report. The split is the decision above."""
    return check not in READINGS

# Which decider is nothing without its language, and where its rules live. A decider
# absent from this map runs in every language.
_NEEDS_RULES = {
    check_time_anchors: _TIME_ANCHORS,
    check_positional_references: _POSITIONAL,
    check_trailing_conditions: _TRAILING,
}

LANGS = sorted({lang for table in _NEEDS_RULES.values() for lang in table})


def unruled(lang: str) -> list[str]:
    """The deciders that have no rules for this language, and so said nothing without
    having looked. Their silence is not a clean document, and a report that does not
    print this is claiming a check it never ran."""
    return sorted(c.__name__ for c, table in _NEEDS_RULES.items() if lang not in table)


def check_file(path: Path, lang: str = "en") -> list[DocFinding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out: list[DocFinding] = []
    for check in CHECKS:
        out.extend(check(path.name, text, path.parent, lang))
    return out


# --- the alarm -----------------------------------------------------------------------

# One document carrying a breach of every decider, and one carrying none. A decider added
# to CHECKS whose violation is absent here reports DEAD -- which is the point: the corpus
# is the thing that must grow, and it grows where a reader can see every breach at once.
GUILTY = """# Guilty

One. Two. Three. Four. Five. Six sentences in one paragraph here.

This feature is currently supported, and as mentioned above it works.

The survey computes coverage and prints the ladder of gaps today.

The survey computes coverage and prints the ladder of gaps today.

The ACME test came first. Later we meet the consortium (ACME) again.

See the manual for more information.

A link that goes [nowhere](#missing).
"""

CLEAN = """# Clean

One sentence. Two sentences. Three of them.

This feature is supported, and the section on adoption explains it.

For more information, read the manual.

A link that goes [home](#clean).
"""

# The paragraph MODEL is not a decider and gets its own pins: what counts as prose, and
# what counts as a sentence. Both were wrong in ways no decider could have reported,
# because a skipped paragraph and a miscounted label leave no finding to be wrong about.
_MODEL = (
    ("a bold-led paragraph is read", "**Note.** One. Two. Three. Four. Five. Six.", 1),
    ("a list item is not prose", "- One. Two. Three. Four. Five. Six. Seven.", 0),
    ("a run-in heading is not a sentence", "**Note.** One. Two. Three. Four. Five.", 0),
    ("a whole bold sentence still is",
     "**One.** **Two.** Three. Four. Five. Six. Seven.", 1),
)


def _alarm() -> int:
    dead: list[str] = []
    for check in CHECKS:
        bad = []
        if not check("guilty.md", GUILTY, None, "en"):
            bad.append(f"{check.__name__} missed the guilty document")
        if check("clean.md", CLEAN, None, "en"):
            bad.append(f"{check.__name__} convicted the clean document")
        dead += bad
        print(f"  {'DEAD' if bad else 'ok  '} {check.__name__}")
    # A language with no rules must produce no findings AND be named by unruled(). The
    # pair is the point: silence alone is what a clean document looks like.
    lang_bad = []
    want_named = sorted(c.__name__ for c in _NEEDS_RULES)
    convicted = [c.__name__ for c in _NEEDS_RULES
                 if c("guilty.md", GUILTY, None, "zz")]
    if convicted:
        lang_bad.append(f"convicted in a language it has no rules for: {convicted}")
    named = unruled("zz")
    if named != want_named:
        lang_bad.append(f"unruled('zz') said {named}, expected {want_named}")
    dead += lang_bad
    print(f"  {'DEAD' if lang_bad else 'ok  '} language: an unruled language "
          "convicts nothing and is named")

    for what, text, want in _MODEL:
        got = len(check_paragraph_length("t", text))
        state = "ok  " if got == want else "DEAD"
        if got != want:
            dead.append(f"model: {what} (wanted {want} finding(s), got {got})")
        print(f"  {state} model: {what}")
    if dead:
        for d in dead:
            print()
            print("DEAD ALARM  " + d)
        return 1
    print()
    print(f"every alarm rings: {len(CHECKS)} decider(s) over one guilty document "
          f"and one clean one, {len(_MODEL)} pin(s) on the paragraph model, and "
          f"one on language. Rules exist for: {', '.join(LANGS)}.")
    return 0



def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.prose",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="markdown files to hold to the laws")
    ap.add_argument("--alarm", action="store_true",
                    help="prove every decider can convict, then exit")
    ap.add_argument("--lang", default="en",
                    help=f"the language the documents are written in (default en; "
                         f"rules exist for: {', '.join(LANGS)})")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.files:
        ap.error("give at least one file, or --alarm")
    findings: list[DocFinding] = []
    readings: list[DocFinding] = []
    for f in args.files:
        path = Path(f)
        text = path.read_text(encoding="utf-8", errors="replace")
        for check in CHECKS:
            got = check(path.name, text, path.parent, args.lang)
            (findings if holds_the_build(check) else readings).extend(got)
    silent = unruled(args.lang)
    if silent:
        print(f"  NO RULES for {args.lang!r}, so these did not run: "
              f"{', '.join(silent)}")
        print("  Their silence is not a verdict. Rules exist for: "
              f"{', '.join(LANGS)}.")
    for fd in findings:
        print(f"  RED {fd.law} [{fd.where}] «{fd.quote}»\n      {fd.why}")
    for fd in readings:
        print(f"  reading {fd.law} [{fd.where}] «{fd.quote}»\n      {fd.why}")
    if readings:
        print(f"\n  {len(readings)} reading(s) above hold nothing. They are word lists "
              f"over prose, and\n  a-word-list-is-a-reading-not-a-mechanization says such "
              f"a law never holds a handback.\n  Measured 2026-08-24: three hits in "
              f"eighty-seven files, two of them the laws quoting\n  the words they "
              f"forbid. Worth a glance, not worth a red build.")
    if not findings:
        print(f"{len(args.files)} file(s): no prose decider convicts.")
    else:
        print(f"\n{len(findings)} finding(s) across {len(args.files)} file(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
