"""The ruling-card pipeline: standing convictions, carded for an owner, verdicts consulted.

The checks convict; only the owner rules. This module is the generic half of that loop: it
reads a drawing (interface@ surfaces), findings (whatever instruments convicted), and a
rulings file (the owner's recorded verdicts), and turns them into judgeable cards — one
card per DECISION, not one per finding — then consults the recorded rulings so a ruled
card is settled or marked, never dealt again (see `settle`).

It knows no app. The app brings what only the app can know:

  - its findings, fed through `add_finding` under its own instrument names;
  - its GROUPS — ``(law, where-prefix) -> (group id, authored question)`` — because which
    findings are one decision is the app's to say (six menu entries are one ruling, not six);
  - its QUESTIONS — per-law authored question texts, in the words of the person answering,
    where the generic template would say less than the app knows;
  - its drawing's surfaces, handed to `element_names` / `surface_index` for names and sketches;
  - its paths — where convictions and rulings live is the app's ledger, not this module's.

The verdict vocabulary is the ruling's, not the sheet's: **stand** (the red stays,
acknowledged — the repo carries it visibly, the uncited-law pattern), **exempt** (this
instance stops counting, and every check that hides it must SAY it hid it, with the
ruling's id), **fix** (the red stays until the code moves; the verdict is the instruction).
A ruling never sharpens or blunts the law itself — laws move in this package, through the loop.

    python -m craft.rulings --alarm    every transformer against a guilty and a clean case
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# The app's grouping: (law, where-prefix) -> (group id, authored question). One card per
# DECISION: findings whose element id matches a prefix collapse into the named group,
# because the ruling is one act however many controls carry it.
Groups = dict[tuple[str, str], tuple[str, str]]


def group_for(law: str, where: str, groups: Groups) -> tuple[str | None, str | None]:
    for (g_law, prefix), (gid, text) in groups.items():
        if law == g_law and where.startswith(prefix):
            return gid, text
    return None, None


def card_id(law: str, where: str, groups: Groups) -> str:
    gid, _ = group_for(law, where, groups)
    return f"ruling:{gid or (law + '--' + where)}"


# WHAT A PERSON CAN JUDGE FROM, ranked. A card shows its first couple of findings and
# counts the rest, so the order decides what the owner actually reads. A quoted string
# off a real screen is evidence anybody can rule on; a prover's replay is a machine's
# sentence about a machine's state, and it goes last (see `human_quote`).
EVIDENCE_RANK = {"lexicon": 0, "critic": 0, "decider": 1, "solver": 2, "probe": 3}


def add_finding(cards: dict, law: str, where: str, quote: str, why: str,
                source: str, groups: Groups) -> dict:
    """One finding onto its card — creating the card if this is its first."""
    gid, gtext = group_for(law, where, groups)
    cid = f"ruling:{gid or (law + '--' + where)}"
    c = cards.setdefault(cid, {
        "id": cid, "law": law,
        "text": gtext or "", "findings": [], "source": source,
    })
    c["findings"].append({"where": where, "quote": quote, "why": why,
                          "source": source})
    c["findings"].sort(key=lambda f: EVIDENCE_RANK.get(f.get("source"), 9))
    return c


def human_quote(replay: str) -> str:
    """The prover's replay, as the click path it actually names.

    A replay reads ``invariant 'x--y' fails after a -> b -> c in state {...}``: the
    invariant is already the card's law, the state dict is a debugger's, and what is
    left — the path — is the one part a person can walk. Shipped whole, it put a raw
    state dump on a card and asked an owner to rule on it, which is this package's own
    no-system-vocabulary law, broken by its adopter, on a card about breaking laws
    (chores, 2026-08).
    """
    s = str(replay)
    if " fails after " not in s:
        return s
    path = s.split(" fails after ", 1)[1].split(" in state ", 1)[0]
    return " → ".join(part.strip() for part in path.split("->"))


def readable(quote: str) -> str:
    """The walker writes a screen in its own notation — ⟦select: «1» | 2 | 3⟧ for a
    dropdown, ⟦input: [Enter a name]⟧ for a field, « » around a rendered string, ·
    between elements. Precise, and not reading: an owner met «Every · ⟦select: «1» |
    2 | …⟧» as the evidence they were asked to rule on. A dropdown reads as its
    current choice with a wheel mark, a field as its box, a separator as a space."""

    def one(m):
        inner = m.group(1)
        kind, _, body = inner.partition(":")
        kind, body = kind.strip().lower(), (body or inner).strip()
        if kind == "input":
            return "[" + body.strip("[]«» ").strip() + "]"
        opts = [o.strip() for o in body.split("|")]
        chosen = next((o for o in opts if o.startswith("«")), opts[0] if opts else "")
        return "[" + chosen.strip("«»").strip() + " ▾]"

    # The walk marks a control's STATE in its own shorthand — «GRISÉ» for greyed,
    # «✓» for pressed — appended to the label. On a card that reads as though the
    # app said it: an owner, meeting «OK GRISÉ», asked 'what's this?'. The state
    # is real and worth showing; the shorthand is the instrument's.
    quote = re.sub(r"\s*GRISÉ\b", " (greyed out)", quote)
    quote = re.sub(r"\s*✓", " (on)", quote)
    out = re.sub(r"⟦([^⟧]*)⟧", one, quote)
    out = out.replace("«", "").replace("»", "")
    out = re.sub(r"\s*·\s*", " ", out)
    return re.sub(r"\s{2,}", " ", out).strip()


# THE JARGON A CHECK SPEAKS TO ITS AUTHOR, and the sentence a person can act on.
# A finding's `why` is written by the check, for whoever maintains the check: «the
# GNOME rule is a biconditional, and this is its first half», «no state may render
# it», «its guard passes through no confirmation variable». An owner met those on
# the judgment surface and said: 'I don't understand the card.' The check keeps its
# words in the journal; the card gets these. Pairs here translate this package's own
# checks; an app adds pairs for the jargon its own notes carry (`extra`).
_PLAINER = (
    ("— the GNOME rule is a biconditional, and this is its first half.",
     "— the usual signal for that is «…» at the end of the label, and it is not there."),
    ("and its guard passes through no confirmation variable — it fires wherever "
     "offered, one tap from loss.",
     "and nothing asks first: wherever it appears, one tap is the loss."),
    ("— no state may render it.",
     "— and there is no version of the screen where it comes out right."),
    ("the state where it is 1 shows the disagreement.",
     "at 1 the number and the word beside it disagree."),
)


def plainer(text: str, extra: tuple[tuple[str, str], ...] = ()) -> str:
    for jargon, plain in _PLAINER + tuple(extra):
        text = text.replace(jargon, plain)
    # The checks name their subjects the way the build does — a catalogue key, a
    # quoted binding, a law id trailing the sentence that reported it. None of those
    # is a thing a person can go and look at, so they leave the card. (Each of these
    # was convicted by craft.cards on the module that first carried them, which is
    # the arrangement working: the deciders found them, not the owner.)
    text = re.sub(r"\s*\(add\.[^)]*\)", "", text)
    # a parenthetical that is a list of catalogue keys — dotted, snake_cased —
    # is the check speaking to its author; the card reader gets the sentence
    text = re.sub(r"\s*\((?:[a-z][a-z0-9_]*\.[a-z0-9_.]+)(?:,\s*[a-z][a-z0-9_.]*)*\)",
                  "", text)
    if "catalogue keys" in text:
        text = re.sub("[^—]*catalogue keys",
                      "one line assembled from several separate strings", text, count=1)
    text = re.sub(r"'[a-z][a-z0-9]*(?:_[a-z0-9]+)+'", "the number", text)
    text = re.sub(r"\s*Reported with the law's [^.]*\.", "", text)
    # The app's own machinery, named as the app names it: a silent focus(), the
    # catalogue of strings, the sheet's healthy state. Each is precise to whoever
    # maintains the check and unreadable to whoever must rule.
    text = text.replace("the refusal is a silent focus()",
                        "the cursor simply moves to the box")
    text = re.sub(r"the catalogue's own ([a-z.\-]+) \(", r"the app's own message (", text)
    text = text.replace("the catalogue's own", "the app's own")
    text = text.replace(" the catalogue", " the app's own words")
    text = text.replace("its healthy state", "the way it looks when nothing is wrong")
    text = text.replace("which is exactly what a string catalogue cannot contain",
                        "which is why reading the strings one by one cannot find it")
    text = re.sub(r"\s*—?\s*\b[a-z]+(?:-[a-z]+){3,}\b\s*$", ".", text.rstrip())
    return text.strip()


def speak(text: str, names: dict[str, str]) -> str:
    """Element ids in a finding's prose become the element's name: 'header-all'
    reads as nothing to a person; «the All toggle beside the date» is the thing
    they can go look at."""
    for ident, name in names.items():
        text = text.replace(f"'{ident}'", name)
    return text


def dedupe(findings: list[dict]) -> list[dict]:
    """One defect, one line. A bilingual app finds every string defect twice, and a
    card that lists «Chore» and «Tâche» as two findings with the SAME sentence under
    each says everything twice. Same place and same reason is one finding, quoting
    both strings."""
    out: list[dict] = []
    by_key: dict[tuple, dict] = {}
    for f in findings:
        key = (f.get("where"), f.get("why"))
        first = by_key.get(key)
        if first is None:
            by_key[key] = dict(f)
            out.append(by_key[key])
            continue
        quotes = [q.strip() for q in first["quote"].split(" / ")]
        if f.get("quote") and f["quote"] not in quotes:
            first["quote"] = " / ".join(quotes + [f["quote"]])
    return out


def collapse(findings: list[dict]) -> list[dict]:
    """One SENTENCE, however many places it convicts.

    Deduping identical findings still leaves lines that say the same thing about a
    different noun — «the chore entry opens further input and its label does not say
    so», then the category entry, then the tag entry. A card showing two of those and
    counting four more is a card that repeats itself and hides its own scope. So
    findings whose explanation ends the same way become ONE line: the shared sentence,
    and every place it fires quoted beside it.
    """
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for f in findings:
        tail = (f.get("why") or "").split(" — ")[-1].strip()
        groups.setdefault(tail, []).append(f)
        if tail not in order:
            order.append(tail)

    out: list[dict] = []
    for tail in order:
        group = groups[tail]
        if len(group) < 2:
            out.extend(group)
            continue
        # NEVER SYNTHESIZE A SENTENCE. Merging heads at their longest shared suffix
        # turned «Nothing states what happened…» into «each states what happened…» —
        # the exact opposite of the finding, on a card asking somebody to rule. So the
        # only merge is the one that invents nothing: the shared closing sentence,
        # said once, with every place quoted beside it.
        quotes = " · ".join(dict.fromkeys(f.get("quote", "") for f in group
                                          if f.get("quote")))
        if len(tail) >= 25:
            out.append({"where": group[0].get("where", ""), "quote": quotes,
                        "why": tail[0].upper() + tail[1:],
                        "source": group[0].get("source", ""), "places": len(group)})
        else:
            out.extend(group)
    return out


def sentence_cut(text: str, limit: int) -> str:
    """Never mid-word, never mid-sentence: a card once read '…the button that
    cannot work sh Stand, exempt, or fix?'."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for stop in (". ", "! ", "? "):
        i = cut.rfind(stop)
        if i > limit // 2:
            return cut[: i + 1]
    return cut.rsplit(" ", 1)[0] + " …"


def _cap(s: str) -> str:
    # str.capitalize() lowercases the REST — it turned «the All toggle» into
    # «The all toggle», renaming the very control the card asks about
    return s[0].upper() + s[1:] if s else s


def ask(card: dict, names: dict[str, str],
        questions: dict[str, str] | None = None) -> str:
    """One question per convicting law, in the words of the person answering.

    `questions` is the app's authored texts, keyed by law — consulted first, because
    the app knows things the template cannot (what its refusal actually looks like on
    the screen the owner will check the card against). Then the generic per-law
    templates, speaking through the drawing's names. A law with neither gets a plain
    generic — never its id.
    """
    f0 = card["findings"][0]
    law, quote, why = card["law"], f0["quote"], f0["why"]
    if questions and law in questions:
        return questions[law]
    name = names.get(f0["where"]) or names.get(quote) or None

    if law == "destructive-is-set-apart":
        return (f"{_cap(name or 'this control')} deletes with one tap — "
                "nothing stands between the tap and the loss. Fine as it is (stand), "
                "or put a confirmation in the way (fix)?")
    if law == "targets-are-thumb-sized":
        m = re.search(r"renders ([\d.]+)x([\d.]+)px", why)
        size = (f"about {round(float(m.group(1)))}×{round(float(m.group(2)))} pixels"
                if m else "smaller than the 24-pixel floor")
        return (f"{_cap(name or 'this control')} is a small target for a "
                f"thumb — it measures {size}, and a fingertip needs 24. Live with it "
                "(stand), or make it bigger (fix)?")
    if law == "ellipsis-promises-more-input":
        return (f"{_cap(name or 'this control')} says «{quote}» and opens a "
                "sheet asking for more — the label does not warn that more is coming. "
                "House style (stand), fine just here (exempt), or add the … (fix)?")
    return (f"A check convicted «{sentence_cut(quote, 60)}»: "
            f"{sentence_cut(speak(why, names), 180)} "
            "Keep it as it is (stand), silence this one place (exempt), "
            "or change it (fix)?")


def element_names(surfaces) -> dict[str, str]:
    """Every element's human name, keyed by its id AND its action — a prover convicts
    by action id, a lexicon by element id, and both must land on the same words."""
    out: dict[str, str] = {}

    def walk(node):
        if getattr(node, "kind", "") == "element" and getattr(node, "name", ""):
            out[node.id] = node.name
            act = (node.payload or {}).get("action")
            if act:
                out[act] = node.name
        for k in getattr(node, "children", []) or []:
            walk(k)

    for s in surfaces:
        walk(s)
    return out


def surface_index(surfaces) -> dict:
    """Every element id and action, mapped to the surface that holds it — so a card
    can show the screen its findings live on."""
    index: dict[str, object] = {}
    for s in surfaces:
        def walk(node):
            for k in getattr(node, "children", []) or []:
                if getattr(k, "kind", "") == "element":
                    index.setdefault(k.id, s)
                    act = (k.payload or {}).get("action")
                    if act:
                        index.setdefault(act, s)
                walk(k)
        walk(s)
    return index


def sketch(card: dict, index: dict) -> dict | None:
    """A picture of the screen the conviction is about, drawn from the drawing.

    Not a photograph: the drawing is what convicted, so the drawing is what a person
    should see — the surface's own rows, in order, with the convicted ones marked.
    The judgment surface renders it as elements (never markup, never a fetched image),
    so no CSP rule and no cache stands between a conviction and the thing it is about.
    No surface resolves, no sketch: silence beats a picture of the wrong screen.
    """
    ids = set()
    for f in card["findings"]:
        where = (f.get("where") or "").split("[")[0]
        ids.add(where)
        ids.update(part for part in where.split("--") if part)
    surface = next((index[i] for i in ids if i in index), None)
    if surface is None:
        return None

    rows = []

    def walk(node):
        for k in getattr(node, "children", []) or []:
            if getattr(k, "kind", "") == "element":
                rows.append({"label": k.name or k.id,
                             "marked": k.id in ids
                             or (k.payload or {}).get("action") in ids})
            walk(k)

    walk(surface)
    if not rows:
        return None
    return {"title": getattr(surface, "name", None) or getattr(surface, "id", ""),
            "rows": rows[:9]}


def finish(cards: dict, names: dict[str, str], index: dict,
           shots: dict | None = None, questions: dict[str, str] | None = None,
           plainer_extra: tuple[tuple[str, str], ...] = ()) -> None:
    """The finishing pass: every card's findings made readable, merged, weighed,
    illustrated, and given its question. HUMANS DO NOT READ CODE TO DECIDE — an
    ungrouped card once got `law-id: «raw finding» — why[:160]` on the surface whose
    whole job is judgment. The drawing already names every element in the owner's
    words; the cards consult it, and each convicting law gets its question in the
    language of the person answering it. Mutates `cards` in place.
    """
    shots = shots or {}
    for c in cards.values():
        for f in c["findings"]:
            f["why"] = plainer(speak(f["why"], names), plainer_extra)
            f["quote"] = readable(f["quote"])
        # the weight is PLACES, counted before the lines are merged: a card that
        # convicts twelve strings is heavier than one convicting one, however tidily
        # the twelve are said
        c["findings_total"] = len(c["findings"])
        c["findings"] = collapse(dedupe(c["findings"]))
        # what the photograph was VERIFIED to contain, straight from the instrument
        # that took it — the card may not claim an illustration it cannot vouch for
        shot = shots.get(c["id"])
        if shot and shot.get("shows"):
            c["shows"] = shot["shows"]
        sk = sketch(c, index)
        if sk:
            c["sketch"] = sk
        if not c["text"]:
            c["text"] = ask(c, names, questions)


def settle(cards: list[dict], recorded: dict[str, dict]
           ) -> tuple[list[dict], list[dict], list[str]]:
    """The consultation that makes a ruling a decision rather than a display mark.

    Without it, a refresh rebuilds the deck from the checks alone: a judged card stays
    settled only because the sheet re-attaches its verdict by id, and the pipeline
    itself happily deals a ruled conviction again. Here every fresh card meets the
    recorded rulings, whatever lane convicted it:

      stand / exempt   settled — off the to-judge deck, carried under `ruled` with its
                       ruling attached, never re-asked
      fix              stays on the deck, its ruling attached, until the check goes
                       green and the card stops being generated at all

    A ruling whose card no longer exists is returned as an orphan, to be said out loud:
    for a fix that is the fix landing; for anything else either the red is gone or the
    card's id drifted — and an id drift silently orphaning a ruling is the exact failure
    this consultation exists to end.
    """
    deck, ruled = [], []
    for c in cards:
        r = recorded.get(c["id"]) or {}
        v = r.get("verdict")
        entry = ({**c, "ruling": {k: r.get(k) for k in ("verdict", "note", "by", "at")}}
                 if v in ("stand", "exempt", "fix") else c)
        (ruled if v in ("stand", "exempt") else deck).append(entry)
    fresh = {c["id"] for c in cards}
    orphans = [
        f"{rid} ({r.get('verdict', '?')}) — "
        + ("the check went green; the fix landed"
           if r.get("verdict") == "fix" else
           "no fresh conviction carries this id: the red is gone, or the card's id "
           "drifted and the ruling is orphaned")
        for rid, r in sorted(recorded.items()) if rid not in fresh
    ]
    return deck, ruled, orphans


def read_rulings(path: Path) -> dict[str, dict]:
    """The recorded rulings, for any check that must consult them. Missing file
    means no rulings, never an error — a check that cannot run without rulings
    would make the rulings a gate on the checks, which is backwards."""
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def verdict_for(law: str, where: str, groups: Groups,
                recorded: dict[str, dict]) -> dict | None:
    """The ruling covering this finding, if the owner has made one. `where` is
    the element or key the finding fired on — the same identity `add_finding`
    carded it under, so a check and its card can never disagree about which
    ruling applies."""
    return recorded.get(card_id(law, where, groups))


# --------------------------------------------------------------------------------------
# The alarms. A checker that has never been seen red is relocated guessing — every
# transformer here faces a guilty case it must change and a clean case it must not.

class _Node:
    def __init__(self, kind="element", id="", name="", payload=None, children=None):
        self.kind, self.id, self.name = kind, id, name
        self.payload, self.children = payload or {}, children or []


def _alarm() -> int:
    dead: list[str] = []

    def alarm(name: str, fired: bool, held: bool):
        if not fired:
            dead.append(f"{name} missed the guilty case")
        if not held:
            dead.append(f"{name} touched the clean case")

    # readable: walker notation becomes reading; plain prose passes untouched
    g = readable("Every · ⟦select: «1» | 2 | 3⟧ · ⟦input: [Enter a name]⟧ · OK GRISÉ")
    alarm("readable",
          g == "Every [1 ▾] [Enter a name] OK (greyed out)",
          readable("Every 3 days") == "Every 3 days")

    # human_quote: a prover replay becomes the click path; a screen quote passes
    g = human_quote("invariant 'x--y' fails after open -> tap-ok in state {'a': 1}")
    alarm("human_quote", g == "open → tap-ok",
          human_quote("«Ajouter»") == "«Ajouter»")

    # plainer: package jargon translated, catalogue-key parentheticals dropped,
    # app pairs consulted — and a sentence with none of it passes whole
    g = plainer("The label never warns — the GNOME rule is a biconditional, "
                "and this is its first half.")
    g2 = plainer("Twelve strings disagree (add.chore_name, add.tag_name).")
    g3 = plainer("An old lesson.", extra=(("old lesson", "translated lesson"),))
    clean = "The empty screen contradicts the button forty pixels below it."
    alarm("plainer",
          "…" in g and "biconditional" not in g
          and "(add." not in g2 and "translated lesson" in g3,
          plainer(clean) == clean)

    # speak: an id in quotes becomes the drawing's name; prose without ids passes
    names = {"header-all": "the All toggle"}
    alarm("speak", speak("'header-all' hides the date", names)
          == "the All toggle hides the date",
          speak("nothing to rename here", names) == "nothing to rename here")

    # dedupe: same place and reason merge, quoting both strings; distinct stay
    two = [{"where": "w", "quote": "Chore", "why": "y", "source": "lexicon"},
           {"where": "w", "quote": "Tâche", "why": "y", "source": "lexicon"}]
    distinct = [{"where": "w1", "quote": "a", "why": "y1"},
                {"where": "w2", "quote": "b", "why": "y2"}]
    alarm("dedupe",
          [f["quote"] for f in dedupe(two)] == ["Chore / Tâche"],
          dedupe(distinct) == distinct)

    # collapse: a shared long tail becomes one line counting its places; short
    # tails and singletons pass through
    tail = "the label does not say that further input is coming"
    many = [{"where": f"w{i}", "quote": q, "why": f"«{q}» — {tail}", "source": "lexicon"}
            for i, q in enumerate(["Chore", "Category", "Tag"])]
    got = collapse(many)
    single = [{"where": "w", "quote": "q", "why": "one thing — short"}]
    alarm("collapse",
          len(got) == 1 and got[0]["places"] == 3
          and got[0]["why"] == _cap(tail) and "Chore · Category · Tag" == got[0]["quote"],
          collapse(single) == single)

    # sentence_cut: never mid-word, never mid-sentence; short text passes whole
    long = ("The button greys out and cannot be pressed. The app decides for you "
            "that there is nothing to try.")
    cut = sentence_cut(long, 60)
    alarm("sentence_cut",
          cut == "The button greys out and cannot be pressed." and len(cut) <= 60,
          sentence_cut("Short.", 60) == "Short.")

    # grouping: a prefixed where lands in its group; an unmatched one keeps law--where
    groups: Groups = {("composed-prose", "fold:"): ("composed-form-rows", "q?")}
    alarm("card_id",
          card_id("composed-prose", "fold:add-sheet", groups)
          == "ruling:composed-form-rows",
          card_id("composed-prose", "tab:today", groups)
          == "ruling:composed-prose--tab:today")

    # add_finding: findings sort by what a person can judge from — the probe's
    # replay never outranks a quoted string
    cards: dict = {}
    add_finding(cards, "l", "w1", "replay", "y", "probe", {})
    c = add_finding(cards, "l", "w1", "«quoted»", "y", "lexicon", {})
    alarm("add_finding",
          [f["source"] for f in c["findings"]] == ["lexicon", "probe"],
          len(cards) == 1)

    # ask: the app's authored text wins; the template speaks the drawing's name and
    # the measured size; a law with neither gets the generic, never its id
    tgt = {"id": "ruling:targets-are-thumb-sized--pill", "law": "targets-are-thumb-sized",
           "text": "", "source": "solver",
           "findings": [{"where": "pill", "quote": "3px margin",
                         "why": "renders 50.0x21.0px", "source": "solver"}]}
    authored = ask(dict(tgt), {}, {"targets-are-thumb-sized": "The app's own words?"})
    template = ask(dict(tgt), {"pill": "the door pill"})
    generic = ask({"id": "ruling:x--w", "law": "x", "text": "", "source": "lexicon",
                   "findings": [{"where": "w", "quote": "q", "why": "y",
                                 "source": "lexicon"}]}, {})
    alarm("ask",
          authored == "The app's own words?"
          and template.startswith("The door pill")
          and "50×21" in template.replace("50×21", "50×21")
          and "21 pixels" in template,
          "x" != generic[:1] and generic.startswith("A check convicted"))

    # the drawing readers: names keyed by id and action, the index finds the
    # surface, the sketch marks the convicted row — and no surface means no sketch
    el = _Node(id="pill", name="the door pill", payload={"action": "open-door"})
    other = _Node(id="row", name="a row")
    surf = _Node(kind="surface", id="deck", name="The deck", children=[el, other])
    names2 = element_names([surf])
    idx = surface_index([surf])
    card = {"findings": [{"where": "pill"}]}
    sk = sketch(card, idx)
    alarm("element_names",
          names2 == {"pill": "the door pill", "open-door": "the door pill",
                     "row": "a row"},
          element_names([_Node(kind="surface", id="s")]) == {})
    alarm("sketch",
          sk is not None and sk["title"] == "The deck"
          and [r["marked"] for r in sk["rows"]] == [True, False],
          sketch({"findings": [{"where": "nowhere"}]}, idx) is None)

    # settle: stand settles, fix stays marked, an orphan is named out loud —
    # and an unruled card is dealt untouched
    RULING = {"verdict": "stand", "by": "o", "at": "t", "note": ""}
    mk = lambda cid: {"id": cid, "law": "l", "text": "q?", "source": "lexicon",
                      "findings": []}
    deck, ruled, orphans = settle(
        [mk("ruling:a"), mk("ruling:b"), mk("ruling:c")],
        {"ruling:a": RULING, "ruling:b": {**RULING, "verdict": "fix"},
         "ruling:gone-fix": {**RULING, "verdict": "fix"},
         "ruling:gone-stand": RULING})
    alarm("settle",
          [c["id"] for c in ruled] == ["ruling:a"]
          and [c["id"] for c in deck] == ["ruling:b", "ruling:c"]
          and deck[0]["ruling"]["verdict"] == "fix" and "ruling" not in deck[1]
          and len(orphans) == 2
          and any("the fix landed" in o for o in orphans if o.startswith("ruling:gone-fix"))
          and any("drifted" in o for o in orphans if o.startswith("ruling:gone-stand")),
          settle([mk("ruling:a")], {})[0] == [mk("ruling:a")])

    # verdict_for: the check and the card land on the same identity
    alarm("verdict_for",
          verdict_for("composed-prose", "fold:add-sheet", groups,
                      {"ruling:composed-form-rows": RULING}) == RULING,
          verdict_for("composed-prose", "tab:today", groups,
                      {"ruling:composed-form-rows": RULING}) is None)

    for d in dead:
        print(f"DEAD ALARM  {d}")
    print("all alarms live" if not dead else f"{len(dead)} dead alarm(s)")
    return 1 if dead else 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m craft.rulings",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--alarm", action="store_true")
    ns = ap.parse_args(argv)
    if ns.alarm:
        return _alarm()
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
