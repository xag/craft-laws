"""A grammar for categorical propositions, and a parser that accepts or refuses.

THE THIRD TIME THE SAME DEFECT WAS CAUGHT, and the owner caught it each time.

  1. `scheme: "deduction"` -- a label. Nothing checked it.
  2. `mood: "AAA", figure: 2` -- two labels. Editing one digit, with every proposition
     byte-identical, turned a conviction into a pass.
  3. `prop: {"quantity": "all", "quality": "affirmative", "subject": ..., "predicate": ...}`
     -- four labels, hand-assembled into a record, validated by set membership. Still
     nothing a grammar had accepted; still the author writing the answer's parts.

So the proposition is now WRITTEN IN A LANGUAGE and parsed. The author types a sentence
in the controlled form; this module's grammar accepts it or refuses it with a position;
quantity, quality, subject and predicate come out of the parse tree. There is no field
in which to put the answer.

THE GRAMMAR, in EBNF, and it is the whole language:

    proposition = "every" term "is" term
                | "no"    term "is" term
                | "some"  term "is" term
                | "some"  term "is" "not" term
    term        = word , { word }
    word        = letter , { letter | digit | "-" | "'" }

Read off the four forms the tradition names:

    every S is P   A  universal affirmative
    no    S is P   E  universal negative
    some  S is P   I  particular affirmative
    some  S is not P   O  particular negative

WHAT THE GRAMMAR DOES NOT DO, said plainly so nobody mistakes the boundary: it does not
translate. Turning "the rule of the soul over the body is natural and expedient" into
`every soul-over-body-difference is natural-rule` is the author's reading, and no
machine here does it. What the grammar removes is the step AFTER that one -- the author
no longer states the form, only the sentence, and every structural fact is derived.

    python -m craft.categorical --alarm          the grammar against its own corpus
    python -m craft.categorical "every B is A"   parse one proposition
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

QUANTIFIERS = ("every", "no", "some")
COPULA = "is"
NEGATOR = "not"

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'-]*")


class ParseError(ValueError):
    """The proposition is not in the language, and the message says where."""


@dataclass(frozen=True)
class Proposition:
    quantity: str      # "all" | "some"
    quality: str       # "affirmative" | "negative"
    subject: str
    predicate: str
    source: str

    @property
    def type(self) -> str:
        return {("all", "affirmative"): "A", ("all", "negative"): "E",
                ("some", "affirmative"): "I", ("some", "negative"): "O"}[
                    (self.quantity, self.quality)]

    def __str__(self) -> str:
        return self.source


def tokenize(text: str) -> list[tuple[str, int]]:
    """Words with their offsets. Anything that is not a word is a parse error at the
    place it appears, rather than something quietly skipped."""
    out, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        m = _WORD.match(text, i)
        if not m:
            raise ParseError(f"unexpected character {text[i]!r} at position {i}")
        out.append((m.group(0), i))
        i = m.end()
    return out


def parse(text: str) -> Proposition:
    """proposition = quantifier term "is" ["not"] term. Refuses everything else."""
    toks = tokenize(text)
    if not toks:
        raise ParseError("empty proposition")
    head, at = toks[0]
    q = head.lower()
    if q not in QUANTIFIERS:
        raise ParseError(
            f"expected one of {QUANTIFIERS} at position {at}, found {head!r}")

    copulas = [i for i, (w, _) in enumerate(toks) if w.lower() == COPULA]
    if not copulas:
        raise ParseError(f"no {COPULA!r}: a proposition joins two terms with it")
    if len(copulas) > 1:
        raise ParseError(
            f"{len(copulas)} occurrences of {COPULA!r}: the language joins exactly "
            "two terms, so a term may not contain it")
    c = copulas[0]

    subject = toks[1:c]
    rest = toks[c + 1:]
    if not subject:
        raise ParseError(f"no subject term between {head!r} and {COPULA!r}")

    negated = bool(rest) and rest[0][0].lower() == NEGATOR
    if negated:
        rest = rest[1:]
        if q != "some":
            raise ParseError(
                f"{head!r} ... {NEGATOR!r} is not in the language: write "
                f"'no <term> is <term>' for a universal negative")
    if not rest:
        raise ParseError(f"no predicate term after {COPULA!r}")

    quantity = "all" if q in ("every", "no") else "some"
    quality = "negative" if (q == "no" or negated) else "affirmative"
    return Proposition(quantity=quantity, quality=quality,
                       subject=" ".join(w for w, _ in subject),
                       predicate=" ".join(w for w, _ in rest),
                       source=text.strip())


# --- the alarm ------------------------------------------------------------------------
#
# Every form the language admits must parse to the type the tradition gives it, and a
# corpus of near-misses must be refused. A parser never seen to refuse is a parser that
# accepts anything.

ACCEPTS = [
    ("every B is A", "A", "B", "A"),
    ("no B is A", "E", "B", "A"),
    ("some B is A", "I", "B", "A"),
    ("some B is not A", "O", "B", "A"),
    ("every natural-slave-case is natural-rule", "A",
     "natural-slave-case", "natural-rule"),
    ("some things that are pleasant is good", "I", "things that are pleasant", "good"),
]

REFUSES = [
    ("all B is A", "expected one of"),
    ("B is A", "expected one of"),
    ("every B A", "no 'is'"),
    ("every is A", "no subject term"),
    ("every B is", "no predicate term"),
    ("every B is not A", "not in the language"),
    ("every B is A is C", "occurrences of"),
    ("every B is A.", "unexpected character"),
    ("", "empty proposition"),
]


def _alarm() -> int:
    dead = []
    for text, want_type, subj, pred in ACCEPTS:
        try:
            p = parse(text)
        except ParseError as e:
            dead.append(f"refused a proposition in the language: {text!r} ({e})")
            continue
        if (p.type, p.subject, p.predicate) != (want_type, subj, pred):
            dead.append(f"{text!r} parsed as {p.type} {p.subject!r}/{p.predicate!r}, "
                        f"wanted {want_type} {subj!r}/{pred!r}")
    for text, fragment in REFUSES:
        try:
            parse(text)
        except ParseError as e:
            if fragment not in str(e):
                dead.append(f"{text!r} refused for the wrong reason: {e}")
            continue
        dead.append(f"accepted {text!r}, which is not in the language")
    print(f"  {'DEAD' if dead else 'ok  '} {len(ACCEPTS)} proposition(s) in the "
          "language parse to the tradition's four types")
    print(f"  {'DEAD' if dead else 'ok  '} {len(REFUSES)} near-miss(es) refused, "
          "each for its own reason")
    for d in dead:
        print("\nDEAD ALARM  " + d)
    return 1 if dead else 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.categorical",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("proposition", nargs="?")
    ap.add_argument("--alarm", action="store_true")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.proposition:
        ap.error("give a proposition, or --alarm")
    try:
        p = parse(args.proposition)
    except ParseError as e:
        print(f"REFUSED: {e}")
        return 1
    print(f"{p.type}  {p.quantity} {p.quality}  "
          f"subject={p.subject!r}  predicate={p.predicate!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
