"""Compile the decidable craft laws against an interface@ tree.

The prover's invariants deliberately see only state variables — the walk of a model
offers no bridge to content. So a law is applied at COMPILE time: the static facts an
interface@ tree carries (bindings, denials, sentence composition, fixed plurals)
select WHICH invariants exist, and the visibility conditions become the exprs. One
invariant per (law, element), because each conviction deserves its own counterexample
click-path.

Only some laws compile, and the split is honest: a law compiles when its falsifier is
a function of the drawing (composition, agreement with a count, contradiction of an
offered action). A law whose falsifier needs a reading — metaphor, tone, calque —
compiles to nothing and stays with the judge; asking this module for it is refused,
never silently skipped.

Host code, not package content: the compilers are Python that travels with the repo,
the way vigil's natives do. What they emit is plain invariant nodes in épure's model
idiom, so any consumer that can prove a model can prove a drawing.
"""

from __future__ import annotations

import re

from quern import Node

from craft.laws import LAWS

_LAW_IDS = {law.id for law in LAWS}


def elements(surface: Node) -> list[Node]:
    return [c for c in surface.children if c.kind == "element"]


def bindings(element: Node) -> list[Node]:
    return [c for c in element.children if c.kind == "binding"]


def denials(element: Node) -> list[Node]:
    return [c for c in element.children if c.kind == "denial"]


def witness(surface: Node) -> Node | None:
    return next((c for c in surface.children if c.kind == "witness"), None)


def when(surface: Node, element: Node) -> str:
    """The full visibility condition: the surface's reachability AND the element's
    own narrowing, either of which may be absent."""
    parts = [p for p in (surface.payload.get("when"), element.payload.get("when")) if p]
    return " and ".join(f"({p})" for p in parts) if parts else "true"


def _law(law_id: str) -> str:
    if law_id not in _LAW_IDS:
        raise ValueError(f"no law '{law_id}' in craft@ — a compiler for a law nobody "
                         "ships would convict against a standard nobody stated")
    return law_id


def _empty_state_never_contradicts(surfaces: list[Node], **_: object) -> list[Node]:
    law = _law("empty-state-never-contradicts")
    # Controls are collected ACROSS surfaces, deliberately: a screen a person sees is
    # several model surfaces at once (a tab and the header above it), and whether a
    # denial and an offer are co-visible is not a modeling convention — it is exactly
    # what the prover decides from the `when` exprs. The invariant states the pair;
    # the state walk finds the overlap or proves there is none.
    controls = [(s, e) for s in surfaces for e in elements(s)
                if e.payload.get("action")]
    out: list[Node] = []
    for s in surfaces:
        for e in elements(s):
            for d in denials(e):
                action = d.payload.get("action", "")
                for cs, c in controls:
                    if c.payload.get("action") != action:
                        continue
                    keys = ", ".join(b.payload.get("key", "?") for b in bindings(e))
                    # The id names the PAIR: one denial can contradict several
                    # controls, each conviction deserves its own counterexample, and
                    # the prover keeps one path per invariant id.
                    out.append(Node(
                        id=f"{law}--{e.id}--{c.id}", kind="invariant",
                        payload={
                            "expr": f"not (({when(s, e)}) and ({when(cs, c)}))",
                            "note": f"'{keys}' asserts action '{action}' is moot; "
                                    f"'{c.id}' offers it in the same state. No "
                                    "state may show both.",
                            "law": law,
                        }))
    return out


def _composed_prose(surfaces: list[Node], **_: object) -> list[Node]:
    law = _law("composed-prose")
    out: list[Node] = []
    for s in surfaces:
        for e in elements(s):
            bs = bindings(e)
            if e.payload.get("sentence") and len(bs) >= 2:
                keys = ", ".join(b.payload.get("key", "?") for b in bs)
                out.append(Node(
                    id=f"{law}--{e.id}", kind="invariant",
                    payload={
                        "expr": f"not ({when(s, e)})",
                        "note": f"one sentence, {len(bs)} catalogue keys ({keys}) — "
                                "no state may render it.",
                        "law": law,
                    }))
    return out


def _plurals_and_agreement(surfaces: list[Node], **_: object) -> list[Node]:
    law = _law("plurals-and-agreement")
    out: list[Node] = []
    for s in surfaces:
        for e in elements(s):
            var = e.payload.get("count_var")
            if var and e.payload.get("fixed_plural"):
                out.append(Node(
                    id=f"{law}--{e.id}", kind="invariant",
                    payload={
                        "expr": f"not (({when(s, e)}) and {var} == 1)",
                        "note": f"'{var}' renders beside a fixed-plural noun; the "
                                "state where it is 1 shows the disagreement.",
                        "law": law,
                    }))
    return out


def _one_surface_one_job(surfaces: list[Node], **_: object) -> list[Node]:
    law = _law("one-surface-one-job")
    out: list[Node] = []
    for s in surfaces:
        marked = [e for e in elements(s) if e.payload.get("intent")]
        for i, e1 in enumerate(marked):
            for e2 in marked[i + 1:]:
                a, b = e1.payload["intent"], e2.payload["intent"]
                if a == b:
                    continue
                out.append(Node(
                    id=f"{law}--{s.id}--{e1.id}--{e2.id}", kind="invariant",
                    payload={
                        "expr": f"not (({when(s, e1)}) and ({when(s, e2)}))",
                        "note": f"'{e1.id}' serves '{a}' and '{e2.id}' serves "
                                f"'{b}' — a person arriving to do one meets the "
                                "other. No state may show both.",
                        "law": law,
                    }))
    return out


def _rare_action_folds_away(surfaces: list[Node], *,
                            disclosures: frozenset[str] = frozenset(),
                            **_: object) -> list[Node]:
    """A rare element must sit behind a disclosure: its visibility must pass through
    one of the state variables named in `disclosures` (the fold/expand booleans of
    the operational half). One that does not is visible the moment its surface is —
    the conviction, with the path to the surface as the repro. The reference check is
    lexical (a word-boundary match of the variable name in the element's own `when`),
    which is honest at this size: a `when` that names a fold it does not actually
    gate on is a drawing lying about itself, and the walks convict that separately."""
    law = _law("rare-action-folds-away")
    out: list[Node] = []
    for s in surfaces:
        for e in elements(s):
            if e.payload.get("frequency") != "rare":
                continue
            own = e.payload.get("when", "")
            behind = any(re.search(rf"\b{re.escape(d)}\b", own) for d in disclosures)
            if behind:
                continue
            out.append(Node(
                id=f"{law}--{s.id}--{e.id}", kind="invariant",
                payload={
                    "expr": f"not ({when(s, e)})",
                    "note": f"'{e.id}' is a rare act with no disclosure between it "
                            "and the surface — it is met by everyone who arrives, "
                            "in every state that shows the surface.",
                    "law": law,
                }))
    return out


COMPILABLE = {
    "empty-state-never-contradicts": _empty_state_never_contradicts,
    "composed-prose": _composed_prose,
    "plurals-and-agreement": _plurals_and_agreement,
    "one-surface-one-job": _one_surface_one_job,
    "rare-action-folds-away": _rare_action_folds_away,
}


def compile_invariants(surfaces: list[Node], laws: list[str] | None = None,
                       disclosures: frozenset[str] | set[str] = frozenset()
                       ) -> list[Node]:
    """Every invariant the compilable laws produce over these surfaces. Naming a law
    that does not compile is refused out loud — its falsifier needs a reading, and
    pretending otherwise would report the judge's work as done. `disclosures` names
    the operational model's fold/expand state variables — what rare-action-folds-away
    means by 'a second layer'."""
    chosen = list(COMPILABLE) if laws is None else laws
    out: list[Node] = []
    for law_id in chosen:
        _law(law_id)
        if law_id not in COMPILABLE:
            raise ValueError(f"'{law_id}' does not compile — its falsifier needs a "
                             "reading, and that seat belongs to the judge")
        out.extend(COMPILABLE[law_id](surfaces,
                                      disclosures=frozenset(disclosures)))
    return out


def bound_keys(surfaces: list[Node]) -> dict[str, list[str]]:
    """Every catalogue key the drawing binds, key -> element ids. The input to the
    totality question a consumer asks its own catalogue: does each of these resolve,
    in every language the app ships?"""
    out: dict[str, list[str]] = {}
    for s in surfaces:
        for e in elements(s):
            for b in bindings(e):
                key = b.payload.get("key")
                if key:
                    out.setdefault(key, []).append(e.id)
    return out
