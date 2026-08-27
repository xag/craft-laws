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

import sys
from dataclasses import dataclass
from pathlib import Path

from lark import Lark
from lark.exceptions import LarkError, UnexpectedInput

QUANTIFIERS = ("every", "no", "some")
COPULA = "is"
NEGATOR = "not"

_GRAMMAR = Path(__file__).with_suffix(".lark")

# Lark builds the parser FROM the grammar file. There is no second implementation to
# drift: the .lark file is the only statement of the language.
_PARSER = Lark(_GRAMMAR.read_text(encoding="utf-8"), start="proposition",
               parser="earley", propagate_positions=True)

_FORM = {
    "universal_affirmative": ("all", "affirmative"),
    "universal_negative": ("all", "negative"),
    "particular_affirmative": ("some", "affirmative"),
    "particular_negative": ("some", "negative"),
}


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


def parse(text: str) -> Proposition:
    """Parse with Lark, against craft/categorical.lark. Every structural fact below
    comes out of the tree; none of it is read from a field."""
    if not text or not text.strip():
        raise ParseError("empty proposition")
    try:
        tree = _PARSER.parse(text)
    except (UnexpectedInput, LarkError) as e:
        col = getattr(e, "column", None)
        where = f" at position {col - 1}" if isinstance(col, int) else ""
        expected = ""
        allowed = getattr(e, "expected", None) or getattr(e, "accepts", None)
        if allowed:
            words = sorted({str(t).replace("__ANON_0", "WORD") for t in allowed})
            expected = f"; expected one of {words}"
        raise ParseError(f"not in the language{where}: {e.__class__.__name__}"
                         f"{expected}") from None
    quantity, quality = _FORM[tree.data]
    terms = [" ".join(str(tok) for tok in sub.children) for sub in tree.children]
    if len(terms) != 2:
        raise ParseError(f"a proposition joins exactly two terms, found {len(terms)}")
    return Proposition(quantity=quantity, quality=quality,
                       subject=terms[0], predicate=terms[1], source=text.strip())


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

# Each near-miss must be refused, and the reason is Lark's, not one written here.
REFUSES = [
    "all B is A",            # not a quantifier of this language
    "B is A",                # no quantifier at all
    "every B A",             # no copula
    "every is A",            # no subject term
    "every B is",            # no predicate term
    "every B is not A",      # universal negative is written "no B is A"
    "every B is A is C",     # a term may not contain the copula
    "every B is A.",         # not a word character
    "",                      # empty
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
    for text in REFUSES:
        try:
            parse(text)
        except ParseError:
            continue
        dead.append(f"accepted {text!r}, which is not in the language")
    print(f"  {'DEAD' if dead else 'ok  '} {len(ACCEPTS)} proposition(s) in the "
          "language parse to the tradition's four types")
    print(f"  {'DEAD' if dead else 'ok  '} {len(REFUSES)} near-miss(es) refused by "
          "the grammar")
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
