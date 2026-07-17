# A style guide cannot fire

*Draft launch post for craft-laws. Publish alongside the repo flip; trim to taste.*

On the 13th of July I shipped a French localisation with 486 tests passing. Every string
key was covered in both directions — 303 of 303. The syntax checker was clean. The
encoding was verified. Twelve flight-recorder tapes replayed the app's real behavior
bit for bit.

It was incredibly bad.

The empty screen greeted returning users with « Il n'y a rien à ajouter » — *there is
nothing to add* — forty pixels above a button marked **AJOUTER**. A section was headed
« Les murs », a literal rendering of the codebase's own internal metaphor, which no
French parent has ever said. A countdown rendered « Encore encore 3 min pour contester »
because two strings, each perfectly correct in isolation, had been composed into one
sentence no person would write. The submit button under the heading « Absence » was
labelled « Absence » — and when I checked the English original, it said *Away* under
*Away*, so the defect predated the translation entirely and every test it ever met was
green.

Not one of my 486 checks could see any of this. They were all checking the catalogue —
and the catalogue was perfect. The defects existed only **on the rendered screen, in
place**: a sentence next to a button, a heading over a form, a fragment inside a
sentence. No string table contains position.

## Writing the rules down didn't work either

The obvious move is a style guide: a markdown file of lessons. I wrote one. It was good.
It even contained this sentence:

> A law with no source is a hypothesis, and is labelled so. Three of the ten are. Source
> them or delete them; do not let them harden into laws by sitting here.

That sentence was true the day I wrote it, and it would have stayed true — quietly,
indefinitely — because prose cannot fire. Nothing reads a style guide back. A checklist
is ignored precisely when you need it; a caveat in a document is a caveat with good
manners and no hands.

## So the laws are data

[craft-laws](https://github.com/xag/craft-laws) is that file, rebuilt as something that
can refuse. Twelve laws of interface and copy, each a node in a tree with rules over it.
Each law carries:

- a **falsifier** — the observation that would convict it, so a verdict can be *fail*
  rather than *I don't like it*;
- a **trigger** — the property of an app that switches it on ("the app is translated",
  "a surface has a zero state"), because a law that applies always applies never;
- a **citation** — publisher, title, URL, *and the quote*, because a citation without
  the words is one nobody can check;
- a **sighting** — a real defect it actually caught, because a law that has never
  caught anything is a law nobody should trust.

A rule (`a-law-cites-a-source`) checks the citations. A publish gate refuses to let an
uncited law travel as settled. The markdown you read is *generated* from the data,
stamped with the revision it came from, and CI fails if the view and the data disagree —
a style guide and its checker can no longer drift apart, because they are the same
object.

## Three of the twelve are red, and that is the point

Run the repo's own check and it fails:

```
4 of 37 rule(s) RED.
  no-calque: ...
  untranslatable-tone: ...
  empty-state-never-contradicts: ...
  publish: Red, and correctly so: three of the twelve laws cite nobody.
```

Three laws — including the one that caught the worst defect of the run, the empty state
contradicting the button below it — cite no authority. I looked. I did not find them
stated. The old style guide would have let them harden into laws by sitting there; this
one carries them visibly red, refuses to publish them as settled, and exits 1 in my face
until I find the source or delete the law.

That is what "a caveat that fires" means, and it is the difference between knowledge you
wrote down and knowledge you can lean on. If you know where one of the three is stated
by someone reputable — I would genuinely like to close the red.
