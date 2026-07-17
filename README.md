# craft-laws

**This repo does not pass its own check today — on purpose.**

```bash
$ uv run python -m craft.check
...
4 of 37 rule(s) RED.
  no-calque: ... I have not found it stated as a rule ...
  untranslatable-tone: ... Source it or drop it.
  empty-state-never-contradicts: ... It stays, uncited and red ...
  publish: Red, and correctly so: three of the twelve laws cite nobody.
```

Twelve laws of interface and copy, as **checkable data**: each carries the observation
that would convict it (a falsifier), the property of an app that switches it on (a
trigger), the authority that stated it (a citation, with the quote), and a real defect it
caught (a sighting). Three of the twelve cite nobody — so the rule `a-law-cites-a-source`
is red, the publish gate refuses to let them travel as settled, and the check exits 1.
That is not a bug in the repo. It is the repo's entire argument: **a style guide is prose,
and prose cannot fire.** These three sat in a markdown file for weeks inside a sentence
that said they were unsourced — a sentence that was true, and that nothing could act on.
As data, the same fact is a red check that will not go away until somebody finds the
source or deletes the law.

```bash
uv run python -m craft.check          # the laws' own rules. Exit 1 while any is red.
uv run python -m craft.render         # the markdown view, generated from the data
```

[`LAWS.md`](LAWS.md) is the rendered view, stamped with the rev it came from; CI
regenerates it and fails if the view and the data disagree.

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

## License

Apache-2.0 — see [LICENSE](LICENSE).

© 2026 Xavier Grehant
