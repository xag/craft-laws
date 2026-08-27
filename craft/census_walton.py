"""The seventh census: Walton's argumentation schemes, via the Carneades encoding.

Source: Walton, Reed & Macagno 2008, Argumentation Schemes (Cambridge UP), as encoded
machine-readably for the Carneades system -- captured whole at
docs/sources/walton-reed-macagno-2008-carneades.yml, 24 schemes. The encoding's own
words: "Here we illustrate one way to represent many of the argumentation schemes of
Doug Walton, including critical questions."

THE FINDING THIS CENSUS EXISTS TO STATE: the rows do not need individual routes,
because the encoding is UNIFORM. Every scheme is one structure --

    premises      what instantiates the scheme
    exceptions    critical questions whose mere raising defeats the inference
                  until answered (undercutters)
    assumptions   critical questions whose burden sits with the proponent
    conclusion    what the scheme licenses, defeasibly

-- 24 schemes, 56 premises, 29 exceptions, 12 assumptions. One generic decider over
that structure covers all 24 and any scheme added later: an exception raised in the
graph and unanswered defeats the inference; an assumption attacked and undischarged
suspends it. That is the structured-argumentation reading (Carneades; the ASPIC+
family), with strict inference staying Z3 and acceptability staying Dung -- the one
formalism the owner asked for, instead of 41 hand-written critical-question deciders.

The quality-harness kill-criterion that wanted "the first thirty critical questions"
sampled is superseded by this complete count: 41 critical questions are encoded, and
ALL of them are decidable in structure once the account carries scheme instances --
what stays with a reader is never the question's mechanics, only whether the
exception's FACT holds when the record does not show it.
"""

from __future__ import annotations

SOURCE = ("Walton, Reed & Macagno 2008, Argumentation Schemes, via the Carneades "
          "encoding (captured at docs/sources/walton-reed-macagno-2008-carneades.yml)")
SOURCE_URL = ("https://raw.githubusercontent.com/carneades/carneades-4/master/"
              "examples/AGs/YAML/walton.yml")
SOURCE_COUNT = 24

# id: (premises, exceptions, assumptions), parsed from the capture on 2026-08-27 and
# pinned here so a drifted capture is a visible diff, not a silent one.
CENSUS = {
    "abduction": (3, 1, 0),
    "analogy": (2, 2, 0),
    "appearance": (1, 0, 0),
    "cause_to_effect": (2, 1, 0),
    "correlation_to_cause": (1, 1, 1),
    "credible_source": (3, 3, 0),
    "definition_to_verbal_classification": (2, 1, 0),
    "defeasible_modus_ponens": (2, 0, 0),
    "established_rule": (2, 0, 1),
    "ethotic1": (2, 0, 1),
    "ethotic2": (2, 0, 1),
    "expert_opinion": (3, 2, 1),
    "ignorance": (2, 1, 0),
    "negative_consequences": (2, 0, 0),
    "position_to_know": (3, 1, 0),
    "positive_consequences": (2, 0, 0),
    "practical_reasoning1": (4, 4, 3),
    "practical_reasoning2": (3, 5, 2),
    "precedent": (3, 2, 0),
    "slippery_slope_base_case": (2, 0, 0),
    "slippery_slope_inductive_step": (2, 0, 0),
    "sunk_costs": (2, 1, 1),
    "verbal_classification": (2, 0, 0),
    "witness_testimony": (4, 4, 1),
}


def main() -> int:
    import re
    from pathlib import Path
    capture = Path(__file__).resolve().parents[1] / "docs" / "sources" / \
        "walton-reed-macagno-2008-carneades.yml"
    print(f"{SOURCE}")
    print()
    p = sum(v[0] for v in CENSUS.values())
    e = sum(v[1] for v in CENSUS.values())
    a = sum(v[2] for v in CENSUS.values())
    print(f"  schemes {len(CENSUS)}  premises {p}  exceptions {e}  assumptions {a}")
    print(f"  critical questions encoded as typed attack slots: {e + a}")
    print()
    print("  one structure covers every row; the decider count for all of them is 1.")
    dead = []
    if len(CENSUS) != SOURCE_COUNT:
        dead.append(f"census holds {len(CENSUS)} schemes, expected {SOURCE_COUNT}")
    if not capture.exists():
        dead.append("the capture is missing from docs/sources/")
    else:
        ids = re.findall(r"^  - id: (\S+)", capture.read_text(encoding="utf-8"),
                         re.MULTILINE)
        if sorted(ids) != sorted(CENSUS):
            dead.append("the capture's scheme ids drifted from this census")
    for d in dead:
        print("  DEAD: " + d)
    return 1 if dead else 0


if __name__ == "__main__":
    raise SystemExit(main())
