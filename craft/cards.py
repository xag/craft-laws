"""The card deciders: what a surface that asks a person to JUDGE may put in front of them.

A judgment card is not a screen like any other. Its whole purpose is that somebody reads
it and decides, so every defect in it costs a decision — and the defects are specific
enough to be caught mechanically:

  * it repeats itself (the same sentence under six quotes, or twice per language),
  * it speaks the check's language rather than the reader's (law ids, identifiers,
    selectors, «biconditional», «no state may render it»),
  * it shows a picture that does not contain what it convicts.

Every one of those shipped to a founder on 2026-08-18, on the surface built to enforce
laws, and each was found by the founder rather than by CI: "there is duplication", "I
don't understand the card", "I don't see how the screen captures illustrate anything
related to the conviction".

    python -m craft.cards ledger/convictions.json
    python -m craft.cards --alarm

These deciders enforce GENERAL laws in the card context — say-it-once,
one-surface-one-job, no-system-vocabulary, what-accompanies-a-claim-supports-it. No law
is card-specific: five were minted that way first, and the founder ruled the failure
was at generalization. The input is a card file: `{"cards": [{id, law, text,
findings: [{where, quote, why}], sketch?, shows?}]}`. `shows` is what the card's picture was VERIFIED to contain — the
capture instrument writes it, and a picture that cannot say what it shows is treated as
showing nothing, because an illustration nobody checked is decoration.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CardFinding:
    law: str
    where: str
    quote: str
    why: str


# The shapes a machine's sentence takes when it leaks onto a person's screen. Each is a
# thing no reader can act on: an identifier only the code uses, a selector, a law's own
# id, or a term of art from the rule rather than from the world.
_JARGON = (
    (r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b", "a code identifier (snake_case)"),
    (r"[#.][a-zA-Z][\w-]*\s*(?:>|\{|$)", "a CSS selector"),
    (r"\bbiconditional\b", "a term of art from the rule, not the world"),
    (r"\bno state may render it\b", "the prover's phrasing"),
    (r"\bguard\b|\bvariable\b|\binvariant\b", "the checker's vocabulary"),
    (r"\bcatalogue\b", "the build's word for the file of strings"),
    (r"#\d{2,}", "an issue number"),
    (r"[a-zA-Z_]\w*\(\)", "a function call, verbatim from the code"),
)

# Words a judgment card is allowed to keep even though they look like ids: the verdict
# vocabulary itself, and the estate's own names for what a person is doing.
_ALLOWED = ("stand", "exempt", "fix", "keep", "drop", "unclear")


def _law_ids() -> set[str]:
    """The actual law ids, so a card is convicted for naming a LAW rather than for
    hyphenating English: «the take-it-off button» is a name a person can read, and
    «rare-action-folds-away» is this package talking to itself."""
    from craft.laws import LAWS
    from craft.practice import PRACTICE
    return {law.id for law in LAWS} | {law.id for law in PRACTICE}


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]


def check_no_repetition(name: str, cards: list[dict]) -> list[CardFinding]:
    """One defect, one line. Two findings whose explanation ends the same way are one
    thing said twice — the bilingual app finds every string defect in two languages, and
    six menu entries carry one sentence about six nouns."""
    out = []
    for c in cards:
        tails: dict[str, int] = {}
        for f in c.get("findings") or []:
            tail = (f.get("why") or "").split(" — ")[-1].strip().lower()
            if tail:
                tails[tail] = tails.get(tail, 0) + 1
        for tail, n in tails.items():
            if n > 1:
                out.append(CardFinding(
                    "say-it-once", c.get("id", name), tail[:80],
                    f"{n} findings on one card end with the same sentence — one defect "
                    "said {n} times is a card that repeats itself and hides its scope"
                    .replace("{n}", str(n))))
    return out


def check_no_jargon(name: str, cards: list[dict]) -> list[CardFinding]:
    """The card speaks to the person deciding, not to the check's author."""
    out = []
    for c in cards:
        parts = [("the question", c.get("text") or "")]
        for i, f in enumerate(c.get("findings") or []):
            parts.append((f"finding {i + 1}", f.get("why") or ""))
        for where, text in parts:
            plain = text
            for word in _ALLOWED:
                plain = plain.replace(word, "·")
            hit = next((lid for lid in _law_ids() if lid in plain), None)
            if hit:
                out.append(CardFinding(
                    "no-system-vocabulary", f"{c.get('id', name)} / {where}", hit,
                    "a law's own id on a surface whose only job is a person deciding"))
                continue
            for pattern, what in _JARGON:
                m = re.search(pattern, plain)
                if m:
                    out.append(CardFinding(
                        "no-system-vocabulary", f"{c.get('id', name)} / {where}",
                        m.group(0)[:60],
                        f"{what} on a surface whose only job is a person deciding"))
                    break
    return out


def check_pictures_show_the_defect(name: str, cards: list[dict]) -> list[CardFinding]:
    """A picture beside a conviction claims to be the evidence. One that does not
    contain what the card convicts is decoration, and decoration next to a question
    is worse than nothing: it answers a question nobody asked."""
    out = []
    for c in cards:
        if not (c.get("has_screen") or c.get("sketch")):
            continue
        shows = [s for s in (c.get("shows") or []) if s]
        if not shows:
            out.append(CardFinding(
                "what-accompanies-a-claim-supports-it", c.get("id", name),
                "(no record of what the picture contains)",
                "the card carries an illustration that never said what it shows — an "
                "illustration nobody verified is decoration"))
            continue
        wheres = {(f.get("where") or "").split("[")[0] for f in c.get("findings") or []}
        parts = set()
        for w in wheres:
            parts.update(p for p in w.split("--") if p)
        if parts and not (parts & set(shows)):
            out.append(CardFinding(
                "what-accompanies-a-claim-supports-it", c.get("id", name),
                ", ".join(sorted(shows))[:60],
                "the picture contains none of the places this card convicts "
                f"({', '.join(sorted(parts))[:60]})"))
    return out


def check_one_card_one_screen(name: str, cards: list[dict]) -> list[CardFinding]:
    """One card is one decision, and a decision lives on one screen.

    A card grouped by law alone gathered the chore form's rhythm line and the Today
    tab's swap line under one question, with a photograph that could only show one of
    them — so half the evidence had nothing to do with the picture, and the two halves
    had nothing to do with each other. The founder: 'the two items are not related and
    the second is not related to the snapshot'.

    Walk surfaces are named `tab:x`, `sheet:x`, `fold:x/y`; findings from the prover
    and the solver name elements instead and are exempt, since an element belongs to
    whatever surface shows it.
    """
    out = []
    for c in cards:
        seen = set()
        for f in c.get("findings") or []:
            where = (f.get("where") or "").split("[")[0]
            if ":" not in where:
                continue
            seen.add(where.split("/")[0])
        if len(seen) > 1:
            out.append(CardFinding(
                "one-surface-one-job", c.get("id", name), ", ".join(sorted(seen))[:70],
                f"{len(seen)} different screens under one question — a person ruling "
                "on this must hold two unrelated places in mind, and any picture can "
                "show at most one of them"))
    return out


# What a card may not claim while its own evidence says otherwise. Each pair is
# (a claim the question makes, a thing the evidence shows) — narrow on purpose: a
# decider that guesses at meaning convicts good cards and teaches everyone to ignore it.
_CONTRADICTIONS = (
    (r"\bsays nothing\b|\bno message\b|\bnothing happens\b|\bin silence\b",
     r"already taken|please fill|required|\bsays so\b|\berror\b|refus",
     "the question says the app is silent while the evidence quotes what it says"),
)


def check_no_self_contradiction(name: str, cards: list[dict]) -> list[CardFinding]:
    """A question may not contradict its own evidence.

    A card asked whether to keep a button that «greys out and says nothing», beside a
    photograph of the app saying «That name is already taken» in red. A person cannot
    rule on that — they can only correct it, which is the founder's work done by the
    founder. The claim and the evidence are both in the record, so the check is cheap.
    """
    out = []
    for c in cards:
        claim = (c.get("text") or "").lower()
        shown = " ".join([(f.get("quote") or "") + " " + (f.get("why") or "")
                          for f in c.get("findings") or []]).lower()
        for says, shows, why in _CONTRADICTIONS:
            if re.search(says, claim) and re.search(shows, shown):
                out.append(CardFinding(
                    "what-accompanies-a-claim-supports-it", c.get("id", name),
                    (re.search(says, claim).group(0) + " / "
                     + re.search(shows, shown).group(0))[:60], why))
                break
    return out


CHECKS = (check_no_repetition, check_no_jargon, check_pictures_show_the_defect,
          check_one_card_one_screen, check_no_self_contradiction)


def check_file(path: Path) -> list[CardFinding]:
    cards = json.loads(path.read_text(encoding="utf-8")).get("cards", [])
    out: list[CardFinding] = []
    for check in CHECKS:
        out.extend(check(path.name, cards))
    return out


def _alarm() -> int:
    """Each decider against a guilty card and a clean one. A checker never seen red is
    relocated guessing — this repo's own screenshot harness re-taught that on its first
    CI run, and these deciders exist because three defects reached a founder."""
    guilty = [
        {"id": "ruling:a", "text": "ellipsis-promises-more-input fires here. Stand?",
         "findings": [
             {"where": "menu-item-chore", "quote": "Chore",
              "why": "the chore entry opens further input — the GNOME rule is a "
                     "biconditional, and this is its first half."},
             {"where": "menu-item-chore", "quote": "Tâche",
              "why": "the category entry opens further input — the GNOME rule is a "
                     "biconditional, and this is its first half."}],
         "has_screen": True},
        {"id": "ruling:b", "text": "The take-it-off button deletes with one tap. Fix?",
         "findings": [{"where": "edit-remove", "quote": "Remove",
                       "why": "nothing asks first: one tap is the loss."}],
         "has_screen": True, "shows": ["header-add"]},
        {"id": "ruling:e",
         "text": "The OK button greys out and says nothing. Keep it?",
         "findings": [{"where": "cat-commit", "quote": "OK (greyed out)",
                       "why": "the name is already taken and the app says so."}]},
        {"id": "ruling:d", "text": "Two screens, one question. Stand?",
         "findings": [{"where": "fold:ajouter-une-tache/when[empty]", "quote": "a",
                       "why": "one line reads as a fragment."},
                      {"where": "tab:today[seeded]", "quote": "b",
                       "why": "another line reads as a fragment."}]},
    ]
    clean = [
        {"id": "ruling:c",
         "text": "The six entries in the add menu each open a form asking for more, and "
                 "none ends in «…». Leave them, or add it?",
         "findings": [{"where": "menu-item-chore", "quote": "Chore / Tâche",
                       "why": "each opens further input and its label does not say so "
                              "— the usual signal is «…» at the end, and it is absent."}],
         "has_screen": True, "shows": ["menu-item-chore", "menu-item-category"]},
    ]
    dead = []
    for check in CHECKS:
        if not check("guilty", guilty):
            dead.append(f"{check.__name__} missed the guilty card")
        if check("clean", clean):
            dead.append(f"{check.__name__} convicted the clean card: "
                        f"{[f.why for f in check('clean', clean)]}")
    for d in dead:
        print(f"DEAD ALARM  {d}")
    print("all alarms live" if not dead else f"{len(dead)} dead alarm(s)")
    return 1 if dead else 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.cards",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--alarm", action="store_true")
    ns = ap.parse_args(argv)
    if ns.alarm:
        return _alarm()
    total = 0
    for f in ns.files:
        for x in check_file(f):
            total += 1
            print(f"{x.law}  {x.where}\n  «{x.quote}»\n  {x.why}")
    if not total:
        print(f"{len(ns.files)} file(s): no card decider convicts.")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
