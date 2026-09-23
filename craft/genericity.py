"""The genericity gate: a law is a proposition, never an app spec in a law's clothes.

Five laws were minted on 2026-08-18 whose subject was one surface of one app — a ruling
card — and the founder ruled the failure was at generalization: «a rule about a card is
not generic and should not go to craft laws». The bar set that day: a law is a
proposition somebody OUTSIDE that surface would recognize; otherwise it is the app's own
spec and belongs in the app. The five were folded the same day, and the founder's next
sentence is why this module exists: «we really need to gate craft laws' CI by a
genericity check».

The bar has a mechanical shadow. A law states itself in its id, its statement, its
falsifier, and its triggers — and a GENERAL proposition has no reason to speak this
estate's vocabulary there: no project names, no coinages like «card», «deck»,
«conviction» or «founder». Sightings, notes and citations are exempt from the coinage
scan on purpose: their job is to be specific about the surface and the day.

They are not exempt from the client scan. A library knows nothing of its consumers - the
dependency points one way, from the app to the library - so no word of this library, a
sighting's included, names a project that uses it: a sighting names the KIND of app («a
chore-sharing app, 2026-07-13, the member sheet»), which is as specific as the law needs.
The client names are not listed here, since listing them would be naming them: they come
from outside, as CRAFT_CLIENT_NAMES (comma-separated; CI reads it from the repository's
variables), and `--clients` reads every law and every text file of the library for them.

    python -m craft.genericity            # judge every law in laws.py + practice.py
    python -m craft.genericity --clients  # no word of the library names a client project
    python -m craft.genericity --alarm    # prove the check can convict at all

A hit here is not always a conviction of the LAW — sometimes the word is the defect and
the proposition is fine, and the fix is restating it in the world's vocabulary. That is
still worth failing the build for: the estate word in the statement is exactly where
tomorrow's reader decides the law is about our app and stops citing it.

The term lists are judgments, kept deliberately short. A false positive at mint time is
cheap — the minting session sees it and either rewords the law or, if the word has
genuinely entered the world's vocabulary, removes it here in the same commit, on the
record. A false negative is the five-laws day again.
"""

from __future__ import annotations

import re

# The estate's own tools, matched as substrings of the lowered text (they are hyphenated or
# unmistakable). A law that names one in its own statement is that tool's spec.
_PROJECTS = (
    "craft-laws", "craft laws", "surface-tape", "surface tape", "flight-recorder",
    "flight recorder", "dev-tools", "tape-store", "quern",
)


def client_names() -> tuple[str, ...]:
    """The projects that use this library, from outside it (CRAFT_CLIENT_NAMES), lowered."""
    import os
    raw = os.environ.get("CRAFT_CLIENT_NAMES", "")
    return tuple(n.strip().lower() for n in raw.split(",") if n.strip())

# The estate's coinages, matched as whole words. Each is a word WE use as if it were
# common; outside this estate a reader would not recognize the proposition through it.
# «widget» is deliberately absent: W3C's ARIA APG says «composite widget» — the world
# owns that word, and the first run of this gate proved it by convicting a W3C-cited law.
_COINAGES = frozenset({
    "card", "cards", "deck", "decks",
    "conviction", "convictions", "convicted", "convicts",
    "ruling", "rulings", "founder",
    "chore", "chores", "household", "households",
    "twin", "twins", "decider", "deciders", "critic", "critics",
    "witness", "witnesses", "drawing", "drawings",
})

# Phrases in which a listed word is the WORLD's usage, not ours — stripped before the
# word scan. «card number» is what everybody calls it; banning it would rule the world's
# vocabulary out of the laws, which is this gate's failure mode inverted.
_WORLDS_PHRASES = ("card number", "credit card", "bank card")


def _words(text: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ][a-zà-ÿ'-]*", text.lower())


def _self_fields(law) -> list[tuple[str, str]]:
    """The places a law states ITSELF — id, statement, falsifier, triggers. Sightings,
    notes and citations stay out: specificity is their job."""
    out = [("id", law.id.replace("-", " ")), ("statement", law.name)]
    for child in law.children:
        if child.kind == "falsifier":
            out.append(("falsifier", child.payload.get("claim", "")))
        elif child.kind == "trigger":
            out.append(("trigger", child.payload.get("when", "")))
    return out


def check_law(law) -> list[tuple[str, str, str, str]]:
    """Every estate word in a place the law states itself: (law id, field, term, text)."""
    found = []
    for field, text in _self_fields(law):
        low = text.lower()
        for phrase in _WORLDS_PHRASES:
            low = low.replace(phrase, " ")
        for name in _PROJECTS + client_names():
            if name in low:
                found.append((law.id, field, name, text))
        for word in _words(low):
            if word in _COINAGES:
                found.append((law.id, field, word, text))
    return found


def _all_words(node) -> list[str]:
    """Every string a node and its children carry: names and payload values."""
    out = [node.name or ""]
    for v in (node.payload or {}).values():
        if isinstance(v, str):
            out.append(v)
    for child in node.children:
        out.extend(_all_words(child))
    return out


def check_clients(law, names=None) -> list[tuple[str, str]]:
    """Every client name anywhere in a law, sightings and notes included: (law id, name)."""
    names = client_names() if names is None else names
    text = " ".join(_all_words(law)).lower()
    return [(law.id, n) for n in names if n in text]


def check_files(names=None, root=None) -> list[tuple[str, str]]:
    """Every client name in the library's own text - its code, its docs, its READMEs:
    (path, name). The dated records - claims.jsonl, the critic's accounts, the published
    package snapshots - say what happened when, and are not rewritten."""
    from pathlib import Path
    names = client_names() if names is None else names
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    paths = list((root / "craft").rglob("*.py")) + list((root / "docs").glob("*.md"))
    paths += [root / p for p in ("README.md", "CONTRIBUTING.md", "LAWS.md") if (root / p).exists()]
    out = []
    for p in paths:
        low = p.read_text(encoding="utf-8", errors="replace").lower()
        out.extend((str(p.relative_to(root)), n) for n in names if n in low)
    return out


def check_all() -> list[tuple[str, str, str, str]]:
    from .laws import LAWS
    from .practice import PRACTICE
    out = []
    for law in LAWS + PRACTICE:
        out.extend(check_law(law))
    return out


def _alarm() -> int:
    """The check convicts a law shaped like the five that were folded, and passes a law
    shaped like the ones that stood — or the build says the alarm is dead."""
    from .laws import _law, _uncited
    guilty = _law(
        "one-card-one-screen",
        "A ruling card shows exactly one screen of the deck",
        _uncited(),
        falsifier="A conviction whose card carries two screens.",
        triggers=["a card is dealt to the founder"],
    )
    clean = _law(
        "say-nothing-twice",
        "A document states each fact once",
        _uncited(),
        falsifier="The same fact stated in two places of one document.",
        triggers=["any document at all"],
    )
    dead = []
    hits = check_law(guilty)
    if len(hits) < 4:  # id, statement, falsifier and trigger all speak estate words
        dead.append(f"missed the guilty law (only {len(hits)} hit(s): {hits})")
    if check_law(clean):
        dead.append(f"convicted the clean law: {check_law(clean)}")
    # The client scan: a sighting naming a client convicts; one naming the kind of app passes.
    named = _law("say-it-once-too", "A document states each fact once", _uncited(),
                 falsifier="The same fact stated in two places of one document.",
                 triggers=["any document at all"],
                 sightings=[("some-client-app, 2026-01-01", "the page said it twice")])
    kind = _law("say-it-once-three", "A document states each fact once", _uncited(),
                falsifier="The same fact stated in two places of one document.",
                triggers=["any document at all"],
                sightings=[("a note-taking app, 2026-01-01", "the page said it twice")])
    if not check_clients(named, ("some-client-app",)):
        dead.append("missed a client named in a sighting")
    if check_clients(kind, ("some-client-app",)):
        dead.append("convicted a sighting that names only the kind of app")
    for d in dead:
        print(f"DEAD ALARM  {d}")
    print("all alarms live" if not dead else f"{len(dead)} dead alarm(s)")
    return 1 if dead else 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.genericity",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--alarm", action="store_true")
    ap.add_argument("--clients", action="store_true")
    ns = ap.parse_args(argv)
    if ns.alarm:
        return _alarm()
    if ns.clients:
        names = client_names()
        if not names:
            print("CRAFT_CLIENT_NAMES is empty: nothing to look for, and that is a failure")
            return 1
        from .laws import LAWS
        from .practice import PRACTICE
        hits = [h for law in LAWS + PRACTICE for h in check_clients(law, names)]
        hits += check_files(names)
        for where, name in hits:
            print(f"{where}  names a client project: «{name}»")
        if not hits:
            print(f"{len(names)} client name(s): none appears in the library's laws or text.")
        return 1 if hits else 0
    found = check_all()
    for law_id, field, term, text in found:
        print(f"{law_id}  speaks the estate's vocabulary in its {field}: "
              f"«{term}»\n  {text}")
    if not found:
        from .laws import LAWS
        from .practice import PRACTICE
        print(f"{len(LAWS) + len(PRACTICE)} law(s): every one states itself in the "
              "world's vocabulary.")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
