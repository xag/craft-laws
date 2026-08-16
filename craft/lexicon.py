"""The language laws, compiled against the glossary: terms × catalogues → findings.

glossary-first has always demanded the glossary as an ARTIFACT — settled terms,
settled by someone who speaks the language. interface@0.2.0's `term` kind makes it
data, and these compilers run the two language laws' mechanical halves over it:

  - COVERAGE (glossary-first): every term speaks every language the app ships. A
    concept with no settled word in some shipped language is exactly the state in
    which ad-hoc translation happens, so the gap itself convicts, before any wrong
    word is even chosen.
  - STRAYS (glossary-first): a word the glossary rejects for a concept, found in a
    catalogue string — the settled term exists and the copy drifted past it.
  - CALQUES (no-calque): a literal translation the glossary marks as translationese,
    found in a catalogue string.

The judgment of WHICH words are settled, strayed, or calqued is made once, at
authoring time, per language, by someone who speaks it — the twin's standing trade.
What these compilers cannot catch is the stray nobody pre-listed: that residue stays
with the reader and must SHRINK as terms accrete, or the convergence hypothesis's
falsifier (the-marginal-vocabulary-stops-shrinking) fires.

Host code, like the other compilers: findings are plain data (no surface-tape import
— the dependency points the other way), keyed by catalogue entry so every conviction
quotes the string it stands in.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from quern import Node

from craft.laws import LAWS

_LAW_IDS = {law.id for law in LAWS}


@dataclass
class LexFinding:
    law: str
    concept: str
    lang: str
    key: str          # catalogue key the conviction stands in; "" for coverage gaps
    quote: str        # the offending word as found, or the missing-language notice
    why: str


def _law(law_id: str) -> str:
    if law_id not in _LAW_IDS:
        raise ValueError(f"no law '{law_id}' in craft@")
    return law_id


def _hits(word: str, catalogue: dict[str, str]) -> list[tuple[str, str]]:
    """(key, matched text) for every catalogue string carrying the word, matched on
    word boundaries and case-insensitively — 'task' must not convict 'multitasking'."""
    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
    out = []
    for key, text in catalogue.items():
        m = pattern.search(text)
        if m:
            out.append((key, m.group(0)))
    return out


def check_verbs(surfaces: list[Node], terms: list[Node],
                catalogues: dict[str, dict[str, str]],
                generic_keys: frozenset[str] | set[str] = frozenset()
                ) -> list[LexFinding]:
    """says-what-happens, compiled against the glossary: a control whose element
    declares `verb` (the term concept its act is named by) must wear that term's
    word, in every language — the label's key resolves per catalogue and the settled
    word must appear in it. Generic confirms (the app's declared generic_keys) claim
    no act and are exempt, per one-act-one-name's own ruling. A control with an
    action but NO verb declared is not convicted — it is unclaimed coverage, the
    caller's to count and this function's to leave visible, never to guess."""
    law = _law("says-what-happens")
    words_by_concept = {t.payload.get("concept", t.id): t.payload.get("words", {})
                        for t in terms if t.kind == "term"}
    findings: list[LexFinding] = []
    for s in surfaces:
        for e in (c for c in s.children if c.kind == "element"):
            verb = e.payload.get("verb")
            if not e.payload.get("action") or not verb:
                continue
            if verb not in words_by_concept:
                findings.append(LexFinding(
                    law=law, concept=verb, lang="", key="",
                    quote=f"(element '{e.id}' names verb '{verb}' and the "
                          "glossary has no such term)",
                    why="A verb claimed against no settled term is a check that "
                        "cannot run — settle the term or drop the claim."))
                continue
            words = words_by_concept[verb]
            for b in (c for c in e.children if c.kind == "binding"):
                key = b.payload.get("key", "")
                if not key or key in generic_keys \
                        or b.payload.get("role") != "text":
                    continue
                for lang, cat in catalogues.items():
                    text = cat.get(key)
                    word = words.get(lang)
                    if text is None or word is None:
                        continue    # coverage gaps are check_glossary's findings
                    if not re.search(rf"\b{re.escape(word)}\b", text,
                                     re.IGNORECASE):
                        findings.append(LexFinding(
                            law=law, concept=verb, lang=lang, key=key,
                            quote=text,
                            why=f"'{e.id}' commits '{verb}' and its label does "
                                f"not say so: the settled {lang} word is "
                                f"'{word}'."))
    return findings




def check_ellipsis(surfaces: list[Node],
                   catalogues: dict[str, dict[str, str]],
                   generic_keys: frozenset[str] | set[str] = frozenset()
                   ) -> list[LexFinding]:
    """ellipsis-promises-more-input (GNOME, a biconditional): a control whose
    `opens` fact names further input needs the ellipsis on its label, and a label
    ending in one without `opens` is a decorative promise. Per language — the
    ellipsis lives in the string."""
    law = _law("ellipsis-promises-more-input")
    findings: list[LexFinding] = []
    for s in surfaces:
        for e in (c for c in s.children if c.kind == "element"):
            if not e.payload.get("action"):
                continue
            opens = bool(e.payload.get("opens"))
            for b in (c for c in e.children if c.kind == "binding"):
                key = b.payload.get("key", "")
                if not key or key in generic_keys \
                        or b.payload.get("role") != "text":
                    continue
                for lang, cat in catalogues.items():
                    text = cat.get(key)
                    if text is None:
                        continue
                    dots = text.rstrip().endswith(("…", "..."))
                    if opens and not dots:
                        findings.append(LexFinding(
                            law=law, concept=str(e.payload.get("opens")),
                            lang=lang, key=key, quote=text,
                            why=f"'{e.id}' opens further input and its label "
                                "does not say so — the GNOME rule is a "
                                "biconditional, and this is its first half."))
                    elif dots and not opens:
                        findings.append(LexFinding(
                            law=law, concept="", lang=lang, key=key, quote=text,
                            why=f"'{e.id}' promises further input with an "
                                "ellipsis and commits directly — the signal is "
                                "load-bearing, a decorative one is a lie."))
    return findings


_TITLE_CASE = re.compile(r"^(?:[A-Z][a-z]+\s+)+[A-Z][a-z]+$")


def check_label_case(surfaces: list[Node],
                     catalogues: dict[str, dict[str, str]]) -> list[LexFinding]:
    """sentence-labels-take-sentence-case (GNOME + GitLab): an input's label never
    wears Title Case. Convicts only the unmistakable shape — two-plus capitalized
    dictionary-shaped words — so proper nouns and single words never
    false-positive."""
    law = _law("sentence-labels-take-sentence-case")
    findings: list[LexFinding] = []
    for s in surfaces:
        for e in (c for c in s.children if c.kind == "element"):
            if not e.payload.get("collects"):
                continue
            for b in (c for c in e.children if c.kind == "binding"):
                key = b.payload.get("key", "")
                if not key or b.payload.get("role") != "text":
                    continue
                for lang, cat in catalogues.items():
                    text = cat.get(key, "")
                    if _TITLE_CASE.match(text.strip()):
                        findings.append(LexFinding(
                            law=law, concept=str(e.payload.get("collects")),
                            lang=lang, key=key, quote=text,
                            why="A field label in Title Case — sentence case "
                                "for labels that run into text, per GNOME and "
                                "GitLab both."))
    return findings


def check_voice(voices: list[Node],
                catalogues: dict[str, dict[str, str]]) -> list[LexFinding]:
    """untranslatable-tone's and speaks-to-you's wordlist halves: a word the app's
    declared voice never uses, found in a catalogue string. The voice node is the
    app's own register, declared once by whoever owns it — this enforces a
    declaration, it does not invent taste."""
    tone = _law("untranslatable-tone")
    findings: list[LexFinding] = []
    for v in voices:
        if v.kind != "voice":
            continue
        for lang, words in (v.payload.get("never") or {}).items():
            cat = catalogues.get(lang, {})
            for word in words:
                for key, hit in _hits(word, cat):
                    findings.append(LexFinding(
                        law=tone, concept=v.id, lang=lang, key=key, quote=hit,
                        why=f"'{hit}' is outside the voice this app declared "
                            f"({v.id}) — off-register here, off-register or "
                            "untranslatable everywhere else."))
    return findings


def check_glossary(terms: list[Node],
                   catalogues: dict[str, dict[str, str]]) -> list[LexFinding]:
    """Every conviction the glossary supports against these catalogues. `catalogues`
    maps language -> {key: string} — the same tables drift and generation read."""
    glossary_first = _law("glossary-first")
    no_calque = _law("no-calque")
    findings: list[LexFinding] = []
    for t in terms:
        if t.kind != "term":
            continue
        concept = t.payload.get("concept", t.id)
        words = t.payload.get("words", {})
        for lang in catalogues:
            if lang not in words:
                findings.append(LexFinding(
                    law=glossary_first, concept=concept, lang=lang, key="",
                    quote=f"(no settled word for '{concept}' in {lang})",
                    why="The app ships this language and the glossary has not "
                        "settled this concept's word in it — the exact state in "
                        "which ad-hoc translation happens."))
        for lang, strays in (t.payload.get("strays") or {}).items():
            cat = catalogues.get(lang, {})
            for stray in strays:
                for key, hit in _hits(stray, cat):
                    findings.append(LexFinding(
                        law=glossary_first, concept=concept, lang=lang, key=key,
                        quote=hit,
                        why=f"The glossary settles '{concept}' as "
                            f"'{words.get(lang, '?')}' in {lang}; '{hit}' is the "
                            "ad-hoc synonym it exists to prevent."))
        for lang, calques in (t.payload.get("calques") or {}).items():
            cat = catalogues.get(lang, {})
            for calque in calques:
                for key, hit in _hits(calque, cat):
                    findings.append(LexFinding(
                        law=no_calque, concept=concept, lang=lang, key=key,
                        quote=hit,
                        why=f"A literal translation the glossary marks as "
                            f"translationese for '{concept}' ({lang}: the settled "
                            f"word is '{words.get(lang, '?')}')."))
    return findings
