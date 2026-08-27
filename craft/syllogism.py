"""Syllogistic validity, COMPUTED from the form -- so `scheme: deduction` stops being
a label the author asserts and becomes a claim the code can refuse.

WHY THIS EXISTS. craft/account.py's first version read two fields an author chose:
`scheme` and `strength`. Everything followed from `scheme`, and nothing checked it.
Label Barbara `sign` and it convicted; label an analogy `deduction` and it passed. The
prose sat in `text`, carried and unread. The owner named it on 2026-08-27: what was
filed was not a formal representation of the argument, it was two labels beside a
quotation.

For defeasible argument that gap is real and stays open -- Greenwell et al.'s 16
"vocab" fallacies are exactly it. But ONE region is decidable and has been since the
Prior Analytics, and it is the region where the strongest word (`robust`) is claimed.
So a `deduction` that declares a syllogistic form is checked against the form.

NOT A TABLE OF THE 24 VALID MOODS. A lookup would be a list of answers with the reason
left out, and a reader could not tell a typo from a theory. The five rules below are
the decision procedure as the tradition states it, each one applied to the parsed form,
and each conviction names the rule it broke. The 24 come out as a consequence, and
`--alarm` checks exactly that: the procedure must accept 24 of the 256 mood/figure
pairs and no others.

THE VOCABULARY, standard since the medieval schools:

  A  universal affirmative   every S is P     subject distributed, predicate not
  E  universal negative      no S is P        both distributed
  I  particular affirmative  some S is P      neither distributed
  O  particular negative     some S is not P  predicate distributed, subject not

  Figures, by where the middle term M sits:
    1  M-P  S-M       2  P-M  S-M       3  M-P  M-S       4  P-M  M-S

A term is DISTRIBUTED in a proposition when the proposition says something about every
member of it. That one notion carries three of the five rules.

    python -m craft.syllogism --alarm     the procedure against the known 24
    python -m craft.syllogism AAA 1       judge one mood and figure
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

TYPES = ("A", "E", "I", "O")
FIGURES = (1, 2, 3, 4)

# Which places a form distributes: (subject, predicate).
_DISTRIBUTES = {"A": (True, False), "E": (True, True),
                "I": (False, False), "O": (False, True)}

_NEGATIVE = {"E", "O"}
_PARTICULAR = {"I", "O"}

# Where the terms sit in each figure: (major premise, minor premise) as
# (subject, predicate) pairs over the terms M (middle), P (major), S (minor).
_PLACES = {
    1: (("M", "P"), ("S", "M")),
    2: (("P", "M"), ("S", "M")),
    3: (("M", "P"), ("M", "S")),
    4: (("P", "M"), ("M", "S")),
}


@dataclass
class Verdict:
    valid: bool
    broke: list[str]
    note: str = ""


def distributed(form: str, places: tuple[str, str]) -> set[str]:
    """The terms this proposition speaks of exhaustively."""
    ds, dp = _DISTRIBUTES[form]
    out = set()
    if ds:
        out.add(places[0])
    if dp:
        out.add(places[1])
    return out


def judge(mood: str, figure: int, existential_import: bool = False) -> Verdict:
    """Is this mood in this figure a valid syllogism? The five rules, in order.

    `existential_import` is the one place the tradition and modern logic part: the
    medieval 24 assume every term names something, which licenses the five
    'subaltern' moods (Barbari, Celaront, Cesaro, Camestros, Camenos) and Darapti,
    Felapton, Bramantip, Fesapo. Modern predicate logic rejects those nine. The
    default here is the modern reading (15 valid); pass True for the medieval 24.
    The disagreement is real and is a choice, so it is a parameter and not a
    silent constant."""
    mood = mood.upper()
    if len(mood) != 3 or any(c not in TYPES for c in mood) or figure not in FIGURES:
        return Verdict(False, ["not-a-syllogistic-form"],
                       f"mood {mood!r} figure {figure!r} is not a form")
    maj, min_, con = mood
    (maj_places, min_places) = _PLACES[figure]
    con_places = ("S", "P")

    dist = (distributed(maj, maj_places) | distributed(min_, min_places))
    dist_in_conclusion = distributed(con, con_places)
    broke = []

    # 1. The middle term must be distributed at least once.
    if "M" not in dist:
        broke.append("undistributed-middle")

    # 2. A term distributed in the conclusion must be distributed in its premise.
    for term in dist_in_conclusion:
        if term not in dist:
            broke.append("illicit-major" if term == "P" else "illicit-minor")

    # 3. Two negative premises yield nothing.
    negatives = sum(1 for f in (maj, min_) if f in _NEGATIVE)
    if negatives == 2:
        broke.append("two-negative-premises")

    # 4. A negative premise requires a negative conclusion, and vice versa.
    if negatives == 1 and con not in _NEGATIVE:
        broke.append("affirmative-conclusion-from-a-negative-premise")
    if negatives == 0 and con in _NEGATIVE:
        broke.append("negative-conclusion-from-affirmative-premises")

    # 5. Two universal premises yield no particular conclusion -- unless the terms
    #    are assumed to name something (the existential-import reading).
    if not existential_import:
        if maj not in _PARTICULAR and min_ not in _PARTICULAR and con in _PARTICULAR:
            broke.append("existential-fallacy")
    if (maj in _PARTICULAR or min_ in _PARTICULAR) and con not in _PARTICULAR:
        broke.append("universal-conclusion-from-a-particular-premise")

    return Verdict(not broke, broke)


def valid_forms(existential_import: bool = False) -> list[str]:
    return [f"{m}-{f}" for f in FIGURES
            for m in ("".join((a, b, c)) for a in TYPES for b in TYPES for c in TYPES)
            if judge(m, f, existential_import).valid]


# The names the tradition gives the forms the procedure accepts, used only to make a
# report readable. They are not consulted by any rule.
NAMES = {
    "AAA-1": "Barbara", "EAE-1": "Celarent", "AII-1": "Darii", "EIO-1": "Ferio",
    "EAE-2": "Cesare", "AEE-2": "Camestres", "EIO-2": "Festino", "AOO-2": "Baroco",
    "IAI-3": "Disamis", "AII-3": "Datisi", "OAO-3": "Bocardo", "EIO-3": "Ferison",
    "AEE-4": "Camenes", "IAI-4": "Dimaris", "EIO-4": "Fresison",
    "AAI-1": "Barbari", "EAO-1": "Celaront", "EAO-2": "Cesaro", "AEO-2": "Camestros",
    "AAI-3": "Darapti", "EAO-3": "Felapton", "AAI-4": "Bramantip", "AEO-4": "Camenos",
    "EAO-4": "Fesapo",
}


def _alarm() -> int:
    """The procedure must produce the tradition's own list, and nothing else."""
    modern = set(valid_forms(False))
    medieval = set(valid_forms(True))
    dead = []
    if len(modern) != 15:
        dead.append(f"unconditional forms: got {len(modern)}, the tradition says 15")
    if len(medieval) != 24:
        dead.append(f"with existential import: got {len(medieval)}, tradition says 24")
    unnamed = medieval - set(NAMES)
    if unnamed:
        dead.append(f"accepted a form the tradition does not name: {sorted(unnamed)}")
    missing = set(NAMES) - medieval
    if missing:
        dead.append(f"rejected a named traditional form: {sorted(missing)}")
    # and it must convict the classic invalidities
    for bad, why in (("AAA-2", "undistributed-middle"),
                     ("AAA-3", "illicit-minor"),
                     ("EEE-1", "two-negative-premises"),
                     ("AAE-1", "negative-conclusion-from-affirmative-premises")):
        m, f = bad.split("-")
        v = judge(m, int(f))
        if v.valid or why not in v.broke:
            dead.append(f"{bad} should break {why}, got {v.broke}")
    print(f"  {'DEAD' if dead else 'ok  '} 15 unconditional forms")
    print(f"  {'DEAD' if dead else 'ok  '} 24 with existential import")
    print(f"  {'DEAD' if dead else 'ok  '} the classic invalidities convict, by name")
    for d in dead:
        print("\nDEAD ALARM  " + d)
    if dead:
        return 1
    print(f"\nthe procedure yields exactly the tradition's forms: "
          f"{len(modern)} unconditional, {len(medieval)} with existential import, "
          f"out of {4 ** 3 * 4} mood/figure pairs.")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.syllogism",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("mood", nargs="?", help="three letters from AEIO, e.g. AAA")
    ap.add_argument("figure", nargs="?", type=int, choices=FIGURES)
    ap.add_argument("--alarm", action="store_true")
    ap.add_argument("--import", dest="ei", action="store_true",
                    help="the medieval reading: every term names something")
    args = ap.parse_args(argv)
    if args.alarm:
        return _alarm()
    if not args.mood or not args.figure:
        ap.error("give a mood and a figure, or --alarm")
    v = judge(args.mood, args.figure, args.ei)
    key = f"{args.mood.upper()}-{args.figure}"
    if v.valid:
        print(f"{key} valid{' (' + NAMES[key] + ')' if key in NAMES else ''}")
        return 0
    print(f"{key} INVALID: {', '.join(v.broke)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


# --- deriving the form from the propositions ------------------------------------------
#
# WHY THIS EXISTS, and it is the second time the same defect was caught. The first
# version of craft/account.py let the author write `scheme: "deduction"` and checked
# nothing. The fix asked for `mood` and `figure` -- and the owner showed, on 2026-08-27,
# that this was the same defect one layer down: changing "figure": 2 to "figure": 1, with
# every proposition byte-identical, turned a conviction into a pass. Two labels instead
# of one is not a formalisation.
#
# So mood and figure are no longer accepted. Each proposition carries its own parts:
#
#     {"quantity": "all" | "some", "quality": "affirmative" | "negative",
#      "subject": "<term>", "predicate": "<term>"}
#
# and the form is COMPUTED from the three of them. The author still translates the
# sentence into quantity, quality and two terms -- that step is the irreducible reading,
# and no machine does it -- but it is now atomic and local per proposition. Which mood,
# which figure, and whether it holds are consequences, and an author who wants a
# different verdict has to change what a premise SAYS.

QUANTITIES = ("all", "some")
QUALITIES = ("affirmative", "negative")

_TYPE_OF = {("all", "affirmative"): "A", ("all", "negative"): "E",
            ("some", "affirmative"): "I", ("some", "negative"): "O"}


class FormError(ValueError):
    """These propositions do not compose into a syllogism, and the reason says why."""


def type_of(prop: dict) -> str:
    """A, E, I or O, from the proposition's own quantity and quality."""
    q, k = prop.get("quantity"), prop.get("quality")
    if q not in QUANTITIES or k not in QUALITIES:
        raise FormError(f"quantity {q!r} / quality {k!r} is not one of "
                        f"{QUANTITIES} x {QUALITIES}")
    for t in ("subject", "predicate"):
        if not str(prop.get(t) or "").strip():
            raise FormError(f"the proposition names no {t}")
    return _TYPE_OF[(q, k)]


def derive(premises: list[dict], conclusion: dict) -> tuple[str, int]:
    """(mood, figure), computed. Raises FormError when the propositions are not a
    syllogism at all -- which is itself a finding, not a silence."""
    if len(premises) != 2:
        raise FormError(f"a syllogism has two premises, not {len(premises)}")
    con_t = type_of(conclusion)
    S, P = conclusion["subject"], conclusion["predicate"]
    if S == P:
        raise FormError("the conclusion's subject and predicate are the same term")

    terms = [{p["subject"], p["predicate"]} for p in premises]
    middles = (terms[0] & terms[1]) - {S, P}
    if len(middles) != 1:
        raise FormError(
            "no single middle term: the premises share "
            f"{sorted(terms[0] & terms[1]) or 'nothing'} outside the conclusion, "
            "so they never meet")
    M = middles.pop()

    major = [p for p in premises if P in (p["subject"], p["predicate"])]
    minor = [p for p in premises if S in (p["subject"], p["predicate"])]
    if len(major) != 1 or len(minor) != 1 or major[0] is minor[0]:
        raise FormError("the conclusion's terms do not sit in one premise each")
    maj, min_ = major[0], minor[0]
    for p, name in ((maj, "major"), (min_, "minor")):
        if M not in (p["subject"], p["predicate"]):
            raise FormError(f"the {name} premise does not carry the middle term")

    # The figure is where the middle term sits: subject of the major or predicate of it,
    # crossed with subject or predicate of the minor.
    if maj["subject"] == M and min_["predicate"] == M:
        figure = 1
    elif maj["predicate"] == M and min_["predicate"] == M:
        figure = 2
    elif maj["subject"] == M and min_["subject"] == M:
        figure = 3
    elif maj["predicate"] == M and min_["subject"] == M:
        figure = 4
    else:
        raise FormError("the middle term sits in no recognised figure")
    return type_of(maj) + type_of(min_) + con_t, figure
