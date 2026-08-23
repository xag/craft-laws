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
# sentence-splitter guards: dots that end no sentence
_ABBREV = re.compile(r"\b(e\.g|i\.e|vs|etc|cf|Mr|Ms|Dr|St|no)\.", re.IGNORECASE)


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


def sentences(prose: str) -> list[str]:
    # markdown notation comes off first: a '?' closed by an italic marker is still
    # the end of a sentence, and the first version of this splitter missed it
    guarded = _ABBREV.sub(lambda m: m.group(0).replace(".", "․"), _plain(prose))
    # a period inside a closing quote or bracket still ends the sentence
    parts = re.split(r"(?<=[.!?])[\"'”’)\]]*\s+", guarded)
    return [p.replace("․", ".").strip() for p in parts if p.strip()]


def _plain(prose: str) -> str:
    """Prose with markdown notation removed, so word counts count words."""
    s = _INLINE_CODE.sub(" ", prose)
    s = _MD_LINK.sub(lambda m: m.group(1), s)
    return re.sub(r"[*_]{1,3}", "", s)


# --- the deciders --------------------------------------------------------------------

def check_paragraph_length(name: str, text: str, ceiling: int = 5
                           ) -> list[DocFinding]:
    """paragraphs-stay-under-five-sentences (GOV.UK: 'no more than 5 sentences
    each')."""
    law = _law("paragraphs-stay-under-five-sentences")
    out = []
    for n, prose in paragraphs(text):
        count = len(sentences(prose))
        if count > ceiling:
            out.append(DocFinding(
                law=law, where=f"{name} ¶{n}",
                quote=_plain(prose)[:100] + "…",
                why=f"{count} sentences in one paragraph, against the ceiling of "
                    f"{ceiling} — split it, or let a reader defend it."))
    return out


def check_sentence_length(name: str, text: str, ceiling: int = 25
                          ) -> list[DocFinding]:
    """sentences-stay-under-twenty-five-words, applied to documentation prose."""
    law = _law("sentences-stay-under-twenty-five-words")
    out = []
    for n, prose in paragraphs(text):
        for s in sentences(prose):
            words = len(_plain(s).split())
            if words > ceiling:
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}",
                    quote=_plain(s)[:120] + ("…" if len(s) > 120 else ""),
                    why=f"{words} words in one sentence, against the {ceiling}-word "
                        "ceiling."))
    return out


_TIME_ANCHORS = ("currently", "at the time of writing", "coming soon",
                 "will soon", "recently added", "as of today")


def check_time_anchors(name: str, text: str) -> list[DocFinding]:
    """docs-do-not-date-themselves: the words that anchor a document to the day it
    was written."""
    law = _law("docs-do-not-date-themselves")
    out = []
    for n, prose in paragraphs(text):
        low = _plain(prose).lower()
        for word in _TIME_ANCHORS:
            if re.search(rf"\b{re.escape(word)}\b", low):
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}", quote=word,
                    why="a sentence pre-written to go stale — describe what the "
                        "product is, not how it just changed."))
    return out


_POSITIONAL = (r"\bas (mentioned|described|noted|shown|discussed) "
               r"(above|earlier|previously)\b",
               r"\bsee (above|below)\b",
               r"\b(the|this) section (above|below)\b",
               r"\bmentioned (above|below)\b")


def check_positional_references(name: str, text: str) -> list[DocFinding]:
    """references-name-their-target-not-its-position: 'above' breaks the day a
    paragraph moves, which is every day a machine edits."""
    law = _law("references-name-their-target-not-its-position")
    out = []
    for n, prose in paragraphs(text):
        low = _plain(prose).lower()
        for pat in _POSITIONAL:
            m = re.search(pat, low)
            if m:
                out.append(DocFinding(
                    law=law, where=f"{name} ¶{n}", quote=m.group(0),
                    why="a positional reference — name the section instead, so the "
                        "reference survives the next edit that moves things."))
    return out


def check_repetition(name: str, text: str, floor_words: int = 8
                     ) -> list[DocFinding]:
    """say-it-once: two sentences saying the same thing in the same words — the
    signature of an edit appended instead of integrated. Convicts only on a
    normalized exact match of a substantial sentence: certainty, not similarity."""
    law = _law("say-it-once")
    seen: dict[str, str] = {}
    out = []
    for n, prose in paragraphs(text):
        for s in sentences(prose):
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
# source's own carve-out, carried visibly.
ACRONYM_EXEMPT = frozenset({
    "API", "URL", "URI", "JSON", "JSONL", "HTML", "CSS", "HTTP", "HTTPS", "CLI",
    "CI", "CD", "PDF", "README", "TODO", "UI", "UX", "SDK", "ID", "IDS", "OK",
    "FAQ", "RTL", "LTR", "ASCII", "UTF", "PNG", "SVG", "DOM", "SEO", "MIT",
    "NOTE", "WARNING", "MUST", "SHOULD", "MAY", "NOT", "AI", "LLM", "MCP",
})


def check_acronyms(name: str, text: str) -> list[DocFinding]:
    """acronyms-spell-out-on-first-reference — the certain half: an acronym the
    document itself later expands with '(ACRO)' was, provably, this document's own
    term to introduce, and every bare use before that expansion met a reader who
    had not been told. An acronym never expanded anywhere is left to a reader:
    it may be as standard as the exempt list's."""
    law = _law("acronyms-spell-out-on-first-reference")
    plain = "\n".join(p for _, p in paragraphs(text))
    out = []
    for m in re.finditer(r"\(([A-Z][A-Za-z]{1,7})\)", plain):
        acro = m.group(1)
        if acro.upper() in ACRONYM_EXEMPT or not acro.isupper():
            continue
        first_bare = re.search(rf"\b{acro}\b", plain)
        if first_bare and first_bare.start() < m.start() - len(acro) - 2:
            out.append(DocFinding(
                law=law, where=name, quote=acro,
                why=f"used bare before the sentence that expands it as "
                    f"'({acro})' — the definition exists and arrives too late."))
    return out


_TRAILING = (r"^see .{3,80} for more information\.?$",
             r"^(click|run|use|call|open|press|select)\b[^.]*\bif you want\b")


def check_trailing_conditions(name: str, text: str) -> list[DocFinding]:
    """conditions-come-before-instructions: the source's own not-recommended
    shapes, matched as patterns."""
    law = _law("conditions-come-before-instructions")
    out = []
    for n, prose in paragraphs(text):
        for s in sentences(prose):
            low = _plain(s).lower().strip()
            for pat in _TRAILING:
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


def check_anchors(name: str, text: str, root: Path | None = None
                  ) -> list[DocFinding]:
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


# --- one file, every decider ---------------------------------------------------------

def check_file(path: Path) -> list[DocFinding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    name = path.name
    return (check_paragraph_length(name, text)
            + check_sentence_length(name, text)
            + check_time_anchors(name, text)
            + check_positional_references(name, text)
            + check_repetition(name, text)
            + check_acronyms(name, text)
            + check_trailing_conditions(name, text)
            + check_anchors(name, text, root=path.parent))


# --- the alarm -----------------------------------------------------------------------

def _alarm() -> int:
    rings: list[tuple[str, bool, bool]] = []
    six = "One. Two. Three. Four. Five. Six sentences here."
    rings.append(("paragraphs", bool(check_paragraph_length("t", six)),
                  not check_paragraph_length("t", "One. Two.")))
    long_s = "word " * 26 + "end."
    rings.append(("sentences", bool(check_sentence_length("t", long_s)),
                  not check_sentence_length("t", "Short enough.")))
    rings.append(("time-anchors",
                  bool(check_time_anchors("t", "This is currently supported.")),
                  not check_time_anchors("t", "This is supported.")))
    rings.append(("positional",
                  bool(check_positional_references("t", "As mentioned above, x.")),
                  not check_positional_references("t", "See the Adopting "
                                                       "section.")))
    twice = ("The survey computes coverage and prints the ladder of gaps today.\n\n"
             "The survey computes coverage and prints the ladder of gaps today.")
    rings.append(("repetition", bool(check_repetition("t", twice)),
                  not check_repetition("t", "Said once. Said differently twice.")))
    late = "The RGAA test came first. Later we meet the framework (RGAA) again."
    early = "The framework (RGAA) is introduced, and RGAA travels alone after."
    rings.append(("acronyms", bool(check_acronyms("t", late)),
                  not check_acronyms("t", early)))
    rings.append(("conditions",
                  bool(check_trailing_conditions(
                      "t", "See the manual for more information.")),
                  not check_trailing_conditions(
                      "t", "For more information, see the manual.")))
    # the marker distinction, both ways: bold-led prose is judged, a list item is not
    bold_led = "**Note.** " + "word " * 26 + "end."
    listed = "- " + "word " * 26 + "end."
    rings.append(("bold-led-prose", bool(check_sentence_length("t", bold_led)),
                  not check_sentence_length("t", listed)))
    anchored = "# A Heading\n\n[good](#a-heading) and [bad](#gone)"
    rings.append(("anchors",
                  bool(check_anchors("t", anchored)),
                  len(check_anchors("t", anchored)) == 1))
    dead = [n for n, rang, clean in rings if not (rang and clean)]
    for n, rang, clean in rings:
        state = "ok " if rang and clean else "DEAD"
        print(f"  {state} {n}: convicting example "
              f"{'convicts' if rang else 'PASSES'}, clean example "
              f"{'passes' if clean else 'CONVICTS'}")
    if dead:
        print(f"\nthe alarm is DEAD for: {', '.join(dead)}")
        return 1
    print(f"\nevery alarm rings: {len(rings)} prose decider(s), each seen red "
          "and each seen green.")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.prose",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="markdown files to hold to the laws")
    ap.add_argument("--alarm", action="store_true",
                    help="prove every decider can convict, then exit")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.files:
        ap.error("give at least one file, or --alarm")
    findings: list[DocFinding] = []
    for f in args.files:
        findings += check_file(Path(f))
    for fd in findings:
        print(f"  RED {fd.law} [{fd.where}] «{fd.quote}»\n      {fd.why}")
    if not findings:
        print(f"{len(args.files)} file(s): no prose decider convicts.")
    else:
        print(f"\n{len(findings)} finding(s) across {len(args.files)} file(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
