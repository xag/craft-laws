# Contributing

A new law needs a **falsifier** (the observation that would convict it), at least one
**trigger** (what switches it on), a **citation** with the quote, and a **sighting** (a
real defect it caught) — or it will be red, and the publish gate will refuse to let it
travel as settled. That is not a review queue; it is the contribution gate working as
designed. An uncited law may still enter, visibly red, if it has caught something real — the check names the ones standing that way today (never trust a count in prose here; `counts-are-computed` is itself one of the laws, minted when this repo's own docs went stale).

`uv run python -m craft.check` runs the laws' own rules; `uv run python -m craft.render`
regenerates `LAWS.md` (never edit the view by hand — CI compares it against the data).
