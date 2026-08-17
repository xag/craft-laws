# craft-laws

The rules of good interfaces, as **data a machine can check** instead of prose a person has to remember. Say what the button does; never contradict your own empty state. Resolve plurals through the language's own rules; put the error beside the field. Rules of that kind — each held in a form that can convict.

## The problem

A real app shipped a French localisation with hundreds of tests passing. Every string key was covered in both directions, syntax-checked and encoding-verified, and a dozen tapes replayed bit-for-bit. Every check was green. **None of them reads.** The empty screen told the user *"there is nothing to add"* — forty pixels above a button marked **AJOUTER**.

Nothing in an ordinary test suite reads the screen. The rules that decide whether a screen is any good exist: WCAG, GOV.UK, RGAA and Baymard have stated them, with research attached. But they live in style guides, and a style guide is prose. Prose cannot fire. So the rules are enforced by whoever remembers them, on whatever screens somebody looks at — which is how that sentence reached production.

## What this is

A catalogue of those rules as checkable data. Each **law** carries:

- a **falsifier** — the observation that would convict it, stated so a verdict can be `fail` and never merely *I don't like it*;
- **triggers** — the properties of an app that switch it on;
- a **citation** — the authority that stated it, quoted verbatim (chosen for authority and falsifiability, never fame — `docs/sources.md` is the catalogue, with the overlap map so every law cites its strongest root);
- **sightings** — the real defects it has caught. A law that has never caught anything is a law nobody should trust, and each law's sighting is why it is in the file.

An app declares what it is in plain sentences: *"used on a phone"*, *"translated into a second language"*, *"has a zero state"*. The laws whose triggers fire arrive; no app reads the whole catalogue.

## How checking works

The expensive judgment happens **once, at authoring time**; everything recurring is mechanical:

1. **The app authors its twin** — a machine-readable description of its interface, written once in the `interface@` vocabulary this repo publishes: which screens exist, the elements they show, the catalogue keys those bind, and per-element facts (this input is required, this control opens a sheet, this count stands beside a noun). This description is called the **drawing**, because that is what it is: the interface drawn as data rather than rendered as pixels.
2. **The decidable laws compile against the drawing** and are proved over *every reachable UI state* — a violation carries the click-path that reaches it. Subsecond, on every commit, and **retroactive: a law mined next year applies to a drawing made today, for free.** The simplest laws skip the state space entirely and run as **deciders** — pattern checks over the rendered words that convict with certainty or stay silent.
3. **The drawing is licensed by evidence, never trusted.** A **walk** — one cheap recorded pass over the real screens, depositing what a person would read there ([surface-tape](https://github.com/xag/surface-tape)'s artifact) — is reconciled against the drawing mechanically, so a proof can never shine green over a description the app has drifted away from.
4. **What no machine can decide** — does the metaphor land, does the tone survive translation — goes to a reading queue as packed, self-contained questions. That residue is measured and expected to shrink as the vocabulary grows; if it stops shrinking, a recorded falsifier says the whole approach is failing.

An app's score is **coverage**: how much of the app its twin describes (surfaces drawn over surfaces walked, strings bound over strings shipped). At 100%, every law — current and future — applies wholesale and for free. Laws are never the app's grade; they are probes of whether the vocabulary suffices (`docs/mechanization.md` tracks that bet, with its own kill-criterion).

## Adopting, in one command

```bash
uv add surface-tape        # pin by rev; surface-tape pins this repo
uv run python -m surface_tape.adopt .
```

The survey computes your coverage and prints the ladder: each gap, its exact next artifact, and a worked example to copy. `--scaffold` writes the template-shaped artifacts for you.

An app pins [surface-tape](https://github.com/xag/surface-tape), and surface-tape pins this repo — **one dependency is the whole entry**. That package carries the walk artifact, the deciders, the survey, and the **critic**. The critic packs each screen owed a reading into a self-contained question, and records the verdict. [vigil](https://github.com/xag/vigil), the watch loop that fires when a walk's prose changes, rides along.

The prover ([epure](https://github.com/xag/epure)) and the tree substrate ([quern](https://github.com/xag/quern)) join only when the app authors its drawing. The dependency points one way: this library knows no consumer by design.

## The pieces, and where each lives

- **The laws** — `craft/laws.py`. Sources and the overlap map: `docs/sources.md`. [`LAWS.md`](LAWS.md) is a rendered *view* of the data — CI regenerates it and fails if view and data disagree, so the prose and the check cannot drift apart.
- **The vocabulary** — `craft/interface.py`, published as **interface@**: surfaces, elements, bindings, witnesses (a witness names the tape record a walk deposits for a surface — the bridge from proof to evidence), terms (the glossary as data), voice (the register as data).
- **The compilers and solvers** — `craft/compile.py` (laws into invariants), `craft/lexicon.py` (glossary, ellipsis, voice checks), `craft/layout.py` (fits and target sizes solved over viewport intervals from measured premises), `craft/instruments.py` (the rendered-world probes: orientation, grayscale signal, touch phases, tab stops, RTL, truncation, text-in-images — pure functions any adopter's walker feeds).
- **The doctrine** — `docs/mechanization.md` and the ledger in `craft/tree.py`: the convergence hypothesis, its falsifier, and the marginal-vocabulary series recorded per mechanization.

## Why the check is red, on purpose

```bash
$ uv run python -m craft.check
...
  no-calque: ... I have not found it stated as a rule ...
  untranslatable-tone: ... Source it or drop it.
  empty-state-never-contradicts: ... It stays, uncited and red ...
```

A handful of laws cite nobody — carried because they caught real defects, and visibly ungrounded until somebody sources or deletes them. `a-law-cites-a-source` names them, the publish gate — the rule that decides what may ship to adopters as settled — refuses them, and the check exits 1. This repo holds itself to its own standard: a rule that cannot go red is an opinion with formatting.

How many laws, and how many are red, this file refuses to say. `counts-are-computed` earned its place when this very README said "twelve" long after the answer had changed. Run the check; it counts.

## The loop that grows this

Every defect a person finds passes through one question before it is fixed: *what valid generic rule did it break?* The answer lands here as a law or a refinement. The fix then ships with a regression check for every adopter, not just the app that bled. The question may honestly answer "app taste, no law", and then nothing is minted here — the adopter's own law set keeps it, enforced locally. A package that absorbs every preference becomes a checklist, and checklists are ignored.

## License

Apache-2.0.
