---
name: source-a-law
description: How a rule enters this estate's checkers - never by hand. Use whenever adding, changing, or removing a law any decider convicts under, in any lane (claims, prose, account, cards). The registry gate (tests/test_law_registry.py) is the checkable half and CI goes red when this protocol is skipped.
---

# A rule enters by source, whole - never by hand

The owner's standing order (2026-08-27): no rule is ever added ad hoc, and no rule is
adopted in isolation. A rule you can defend but not cite is an opinion with a gate in
front of it, and a source mined for one convenient rule is a word list one level up.

## The protocol

1. **Name the source, then fetch the whole of it.** A published catalogue, taxonomy,
   spec, or guidance note - authority and falsifiability over fame
   (docs/practice-sources.md ranks the existing ones). Fetch the actual document.
   Capture it under `docs/sources/` so the quotes stay checkable offline.

2. **Census every item, not the one you came for.** One row per item the source
   states, each routed: `covered` (existing machinery decides it), `zero` (decidable
   from existing data), `vocab` (needs a fact nothing carries), `judge` (stays with a
   reader). craft/census_argument.py is the worked example - 33 rows, counts printed,
   the ceiling measured before any decider was written.

3. **Register the laws the census says are decidable.** One registry entry per law:
   id, statement, source, the census row it mechanizes, and citations whose quotes
   are VERBATIM from the fetched document. A paraphrase is marked as a capture with
   its provenance, never dressed as a quotation - one pass caught the fetch tool
   fabricating a spec sentence, which is the whole argument for quotes.

4. **Take the source's exemptions with its rules.** Arguing-from-Ignorance ships an
   exemption clause in its own definition; adopting the conviction without the
   exemption is authoring a stricter rule and signing the source's name to it.

5. **Reuse before minting.** If an adopted source already carries the law (the IPCC
   note in craft/practice.py), the new decider convicts under the existing id.
   One law, one home; the gate verifies the reuse still resolves.

6. **Run the gate.** `uv run python -m pytest tests/test_law_registry.py` - it fails
   on an unregistered decider id, an uncited account law, a cherry-picked row, a
   decider on a judge-routed row, a dead registry entry, and a missing capture. CI
   runs it on every push, so skipping this protocol is a red build, not a habit.

## What the gate cannot check, so you must

Whether the census's routes are honest readings of the source, and whether a quote's
surrounding context supports the law drawn from it. Both are readings; both are why
the capture is committed - a reader can refute you from the file.
