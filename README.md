# craft-laws

**This repo does not pass its own check today — on purpose.**

```bash
$ uv run python -m craft.check
...
  no-calque: ... I have not found it stated as a rule ...
  untranslatable-tone: ... Source it or drop it.
  empty-state-never-contradicts: ... It stays, uncited and red ...
```

Laws of interface and copy as **checkable data**: each carries the observation that would convict it (a falsifier), the property of an app that switches it on (a trigger), the authority that stated it (a citation, with the verbatim quote), and the real defects it has caught (sightings). A handful cite nobody — so `a-law-cites-a-source` is red, the publish gate refuses to let them travel as settled, and the check exits 1. That is not a bug. It is the repo's entire argument: **a style guide is prose, and prose cannot fire.** How many laws, and how many are red, are exactly the kind of numbers this file refuses to state — the law `counts-are-computed` earned its place when this very README said "twelve" long after the answer had changed. Run the check; it counts.

```bash
uv run python -m craft.check          # the laws' own rules; counts itself. Exit 1 while any is red.
uv run python -m craft.render         # regenerates LAWS.md, the human view, stamped with its rev
```

[`LAWS.md`](LAWS.md) is a rendered *view* of the data — CI regenerates it and fails if view and data disagree, so the prose and the check cannot drift apart. An uncited law is not a special mechanism: it **is** a ledger hypothesis in quern's sense — a belief carried with the observation that would kill it — and the gate that blocks it is `nothing-unsound-passes-a-gate`, which ledger already ships. This repo did not invent its own rigor; it imported it.

## This is the front door of a verification framework

Point an agent here first. The pieces, and where each lives:

- **The laws** (`craft/laws.py`) — mined from authoritative sources chosen for authority and falsifiability, never fame: `docs/sources.md` is the catalogue, with the overlap map so every law cites its strongest root and the gaps recorded as gaps.
- **The vocabulary** (`craft/interface.py`, published as **interface@**) — an app's *semantic twin*: surfaces, elements, bindings, witnesses, terms (the glossary as data), voice (the register as data), constraints. An app authors its drawing once; every law that can compile then applies over **every reachable UI state**, with a click-path per conviction.
- **The compilers and solvers** (`craft/compile.py`, `craft/lexicon.py`, `craft/layout.py`) — laws become épure invariants, glossary checks, layout claims solved over viewport intervals from measured premises.
- **The doctrine** (`docs/mechanization.md` + the ledger in `craft/tree.py`) — the two claims under permanent test: *there is no judge-forever category* (any law compiles against a sufficient twin, and the vocabulary needed converges — the marginal-cost series is recorded per mechanization, with a standing falsifier), and *coverage is the metric* (an app is scored by how much of it its twin describes, toward 100%; laws are the vocabulary's probes, not the app's grade).

## Adopting, in one command

An app does not read all this. It runs the survey, which computes its coverage and prints the ladder — each gap with the exact next artifact and a worked example to copy:

```bash
uv add surface-tape        # pin by rev; surface-tape pins this repo
uv run python -m surface_tape.adopt .
```

**One dependency is the whole entry**: an app pins [surface-tape](https://github.com/xag/surface-tape) (the walk artifact, the critic, the deciders, the survey), which pins this repo; [vigil](https://github.com/xag/vigil) (the watch loop) rides along. The prover ([epure](https://github.com/xag/epure)) and the tree substrate ([quern](https://github.com/xag/quern)) join only when the app draws its twin. The repos are many because each is one idea pinned by digest; the *adoption* surface is one pin and one command.

The survey's rungs each carry a worked example to copy, and the laws' own sightings name the real runs where each law drew blood — those, not this README, are where adopting apps appear. The dependency points one way: this library knows no consumer by design.

## Where the laws came from

One run. A French localisation shipped to production with **hundreds of tests passing, every string key covered in both directions, syntax-checked, encoding-verified, and a dozen flight-recorder tapes replaying bit-for-bit.** Every check was green. **None of them reads.** The empty screen told the user *"there is nothing to add"* — forty pixels above a button marked **AJOUTER**. The sightings in `craft/laws.py` are runs like that one. They are not decoration; a law that has never caught anything is a law nobody should trust, and each law's sighting is why it is in the file.

## The loop that grows this

Every defect a person finds passes through one question before it is fixed: *what valid generic rule did it break?* The answer lands here as a law or a refinement — so the fix ships with a regression check for every adopter, not just the app that bled. The question may honestly answer "app taste, no law", and then nothing is minted: a package that absorbs every preference becomes a checklist, and checklists are ignored.

## License

Apache-2.0.
