# craft-laws

**`craft@0.1.0`** — the laws of interface and copy, as data a rule can go red on.

```bash
uv run python -m craft.check          # the laws' own rules. Exit 1 while any is red.
uv run python -m craft.render         # the markdown view, generated from the data
```

## Why this is not a style guide

A style guide is prose, and **prose does not fire**.

These laws began as bullets in a markdown file. That file contained this sentence:

> *A law with no source is a hypothesis, and is labelled so. Three of the ten are. Source them or
> delete them; do not let them harden into laws by sitting here.*

The sentence was true. It would have gone on being true, silently, for as long as anybody left it
there — which is precisely the failure that [`ledger@0.1.0`](https://github.com/xag/quern) exists to
prevent, reproduced inside the artifact that teaches it.

So the laws are data. `a-law-cites-a-source` is a rule now, and it is **red**, and it names the
three laws that cite nobody. `LAWS.md` is a rendered *view* of that data, stamped with the rev it
came from — so the prose and the check can no longer disagree.

## Why it builds on `ledger` rather than reinventing it

An uncited law **is** a ledger hypothesis — exactly, not by analogy: a belief held provisionally,
carrying the observation that would kill it. So a law's `authority` is a `grounding` Quantity,
grounded when somebody reputable has actually said this and ungrounded when it is an opinion
wearing a lab coat. Then `nothing-unsound-passes-a-gate` — which `ledger` already ships — asks the
publication gate whether an uncited law is about to travel as though it were settled. It does not
need to be told what a law is. It only asks whether the thing resting on it was ever checked.

`invest` re-authored the ledger's kinds and Home Hub rolled its own. The point of a package is
that the third project does not make the same mistake a third time.

## Why it does not live inside quern

`ledger@0.1.0` lives in `src/quern/ledger.py`, and its own docstring calls that siting wrong: a
package inside the substrate means refining a vocabulary requires **a quern release** — the exact
pathology quern exists to dissolve ([xag/quern#19](https://github.com/xag/quern/issues/19)).

Putting a set of UX laws in there would reproduce that error knowingly, and would mean that a
better citation for a button label waits on a substrate release. So `craft` roots itself in its
own `Library`, in its own repo, on its own clock — the third route, which #19 will make ordinary,
and which is possible today only because quern already lets a project's own vocabulary stand
alongside a package's.

**`craft` is therefore the second independent consumer wanting that channel.** One is a special
case. Two is evidence.

## The laws

Twelve. Nine cite a source; three do not, and are carried visibly as hypotheses. Each carries:

| | |
|---|---|
| **falsifier** | the observation that constitutes a violation — so a verdict can be `fail`, not *I don't like it* |
| **trigger** | the property of an app's *intent* that switches the law on. A law with no trigger is a checklist item, and checklists are ignored |
| **citation** | publisher, title, URL, **and the quote**. A citation without the words is one nobody can check |
| **sighting** | a real defect it actually caught. A law that has never caught anything is a law nobody should trust |

Sources: Nielsen Norman Group, GOV.UK Design System, Mozilla L10n, Unicode CLDR, W3C/IBM,
Lionbridge.

## Where they came from

One run. `chores`, 2026-07-13 — a French localisation that shipped to production with **486 tests
passing, 303/303 string keys covered in both directions, `node --check` clean, cp1252 verified,
and twelve flight-recorder tapes replaying bit-for-bit.**

Every check was green. **None of them reads.** The empty screen told the user *"there is nothing
to add"* — forty pixels above a button marked **AJOUTER**.

The sightings in `craft/laws.py` are that run. They are not decoration; they are why each law is
in the file.

## Consumers

- [`blind-usability`](https://github.com/xag/claude-plugins) — step 3b turns these laws into
  expectations, triggered by an app's intent, confronted by reading the rendered screens.
