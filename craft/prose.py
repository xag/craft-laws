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
# The shape craft/lexicon.py already uses for terms and voices. Two rule tables are keyed
# by language: _ABBREV (dots that end no sentence) and _ACRONYM_PROSE (words this language
# writes in capitals). The language is DECLARED (--lang, default "en"), never sniffed:
# guessing a document's language from its bytes is a prediction, and a wrong prediction
# reports the wrong rules as authoritative.
#
# A missing table for a language makes a decider convict MORE, never fall silent: without
# an abbreviation guard the splitter counts "e.g." as a sentence end and over-counts, and
# without an acronym list more capitalised words are flagged. Both are false positives a
# reader can see. There is no decider left here that goes quiet in an unruled language,
# which is why nothing reports "did not run" any more - the word lists that had that
# failure mode were removed on 2026-08-27.

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

CHECKS = (check_paragraph_length, check_repetition, check_acronyms, check_anchors)

# --- why there is no word list here ---------------------------------------------------
#
# a-word-list-is-a-reading-not-a-mechanization: "A law checked by matching words in prose
# is unmechanized, and says so - it does not get a decider." Three checks here were
# exactly that shape (time anchors, positional references, trailing conditions). They
# gated the build for a week, were demoted to reporting-only on 2026-08-24, and were
# REMOVED on 2026-08-27 at the owner's direction.
#
# What the demotion measured, over 87 markdown files across the estate: time-anchors 2
# hits, positional 1, trailing 0 - and two of those three were LAWS.md convicting the
# law's own statement. That is the structural defect, not a tunable one: a rule that
# forbids a word cannot be written down without using it, so any word list convicts its
# own statement and every document discussing it.
#
# The one true positive they ever produced was a README clause that said "thin as it
# currently is". Rewriting it to keep the word list happy produced "thin as it is", which
# means nothing; the clause was carrying no information and the fix was to delete it.
# Three word lists, 87 files, one hit, and the hit's remedy was a deletion.
#
# The three LAWS stay in the package. What they no longer have is a decider, which is
# the accurate position rather than a gap: unmechanized, not faked.








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
          f"and one clean one, and {len(_MODEL)} pin(s) on the paragraph model.")
    return 0



def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.prose",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="markdown files to hold to the laws")
    ap.add_argument("--alarm", action="store_true",
                    help="prove every decider can convict, then exit")
    ap.add_argument("--lang", default="en",
                    help="the language the documents are written in (default en); it "
                         "selects the abbreviation and acronym tables, and an absent "
                         "table makes a decider convict more, never fall silent")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.files:
        ap.error("give at least one file, or --alarm")
    findings: list[DocFinding] = []
    for f in args.files:
        path = Path(f)
        text = path.read_text(encoding="utf-8", errors="replace")
        for check in CHECKS:
            findings.extend(check(path.name, text, path.parent, args.lang))
    for fd in findings:
        print(f"  RED {fd.law} [{fd.where}] «{fd.quote}»\n      {fd.why}")
    if not findings:
        print(f"{len(args.files)} file(s): no prose decider convicts.")
    else:
        print(f"\n{len(findings)} finding(s) across {len(args.files)} file(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
