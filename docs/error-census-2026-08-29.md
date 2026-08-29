# The 2026-08-29 error inventory, reclassified against Croskerry and MAST

The session that commissioned the two error-taxonomy censuses (`craft/census_croskerry.py`, `craft/census_mast.py`) also supplied the first corpus: its own errors. This document classifies each observed error of that session against both taxonomies and records who caught it. The question it answers is the one the owner posed: which error classes are frequent-and-decidable, so that the next decider is aimed by frequency rather than by what is feasible to build.

**Honesty box.** This is an exploratory reading, not a prespecified measurement: the corpus is one session (convenience), the classifier is the session's own author, the reference standard is that same author's reading, and the miss row is unmeasured — errors the author never noticed are absent by construction. The matching claims record carries these fields; treat every count below as a lower bound with n too small for rates.

## The inventory

| # | Error (what actually happened) | Croskerry CDR | MAST mode | Caught by |
|---|---|---|---|---|
| 1 | Four quotes filed as verbatim that were paraphrases (case changed, markdown stripped, lines reflowed) | — (a slip, not a disposition; neither taxonomy carries fidelity slips) | — | machine (anchoring decider), 4/4 |
| 2 | Three inferences labeled `deduction` with nothing checkable exhibited | overconfidence-bias | — | machine (entailment decider), 3/3 |
| 3 | A conclusion worded to carry two readings (sandbox *exists* vs *runs today*), the caveat filed as an attack on the wrong reading | framing-effect | — | machine surfaced the tension (unanswered-attack decider); the owner dissolved it |
| 4 | A checker invoked through the wrong constructor parsed zero nodes and its all-pass output was trusted twice | search-satisfying | fm-3.3-incorrect-verification | the author, on a third look — after reporting the wrong result |
| 5 | The account hook believed to be running all session while its wiring made it find nothing; its silence read as passes | premature-closure, overconfidence-bias | fm-3.2-no-or-incomplete-verification | the owner ("does it work?") |
| 6 | The account checker run by hand after the owner said the hook is there for that — side-effecting the throttle's seen-state, eating one live delivery | — | fm-1.1-disobey-task-specification | the owner |
| 7 | A `git add`/`commit` executed in the wrong repo because a `cd` earlier in the compound command moved the cwd | — (slip) | — | tool error (empty staging), immediately |
| 8 | The transponder session-id typed with a character missing, all session | — (slip) | — | nobody (benign: the claims stayed self-consistent) |

## What the counts say

- **Fidelity slips are the most frequent caught class (4) and sit outside both taxonomies.** They are already decided (the anchoring check) — the harness's one unambiguous win. Slips of this family (7, 8) suggest the missing third source is a slips taxonomy (Reason's slips/lapses/mistakes), not more disposition rows.
- **The costliest class is verification failure (4, 5): MAST FC3, Croskerry premature-closure/search-satisfying.** Two occurrences, both escaped every decider, both caught by a human, and both are the same shape: *an instrument trusted without observing it observe*. The laws exist (`done-is-observed-where-the-user-stands`, `a-check-reports-what-it-could-not-judge`) but bind claims and published checks; the in-session ad-hoc check and the silently-dead hook are held to neither. This is the frequent-and-costly-and-undecided cell.
- **The disposition rows the account lane caught (2, 3) are real but cheap** — they were errors *of the formalization itself*, repaired in minutes.
- **One scope breach (6) matches the owed rows fm-1.1/fm-2.3** — the ask-versus-acts comparison nobody computes.

## The aimed next step (not built, by instruction)

One decider shape covers both instances of the costly class: **a check must exhibit what it read** — a checker's verdict travels with the count of units it actually judged (accounts parsed, nodes seen, corpus size), and a verdict over zero units convicts instead of passing. Instance 4 (zero nodes parsed → "0 findings") and instance 5 (zero accounts found → silence read as pass) both fall to it, and it is the mechanized form of the standing hypothesis `a-defect-in-what-a-check-reads-is-invisible-to-that-check`. Frequency says build this before any further argument-structure machinery.

**Postscript, same day.** The owner read the counts and said build it. `a-check-exhibits-what-it-read` is now law (practice.py, cited to MAST FM-3.3, both instances above as its founding sightings) and fires in three places: an account parsing to zero nodes convicts instead of passing, the account hook says once per session when it finds zero accounts instead of exiting silently, and the claims CLI prints the claim count beside its verdict with a zero-claim run reported as "nothing judged", never as a pass. The MAST census row fm-3.3 moved from owed to covered, its meaning text keeping the gap's history.
