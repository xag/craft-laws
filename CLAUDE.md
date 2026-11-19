# NO HACKS. THIS IS A QUALITY HARNESS.

This project exists to hold work to checkable claims. A hack inside the thing that checks quality is worse than a hack anywhere else, because it teaches every reader that the checks themselves are theater. These rules are absolute in this repo and in what it runs: the hooks, the deciders, their tests.

**NEVER match words over prose.** Not in a checker, not in a proposer, not in a test assertion. `assert "correct" in text`, a regex over a reply, a keyword list over an instruction — all of it is a word list wearing a mechanism, and it passes on text that says the opposite. If the input is prose, derive its structure as a committed data artifact and check the data exactly (verbatim-quote anchoring, hash pinning, reference resolution). If the prose embeds something executable — a command, a path, an id — execute or resolve it and assert on the outcome. What prose persuades a reader to do is observable only in live behavior; a check that cannot reach that says so instead of pretending.

**NEVER ship a mechanism with known false positives**, even labeled "informational". A checker that can raise a wrong flag gets ignored, and then nothing is checked. Deterministic checks over data are acceptable; heuristics that can only fail toward silence are acceptable; anything that can cry wolf is not.

**NEVER substitute a weaker thing that looks like the strong thing.** A test that pins tokens instead of behavior, a stub that was never verified against the real client, a self-graded label chosen by the checked party — each is relocated guessing. If a reliable design does not exist yet, say so and stop; the fallbacks are thinking further outside the box or going back to Xavier. Shipping the hack is not among them.

These were each stated by Xavier after a live failure: a regex "radar" with 70 false alarms in 176 hits (2026-08-25, "never make hacks that work kind of"), and word-match test assertions over a conviction contract (2026-08-30, "NEVER DO THAT STUPID THING. DO NOT DO HACKS. WE'RE DEVELOPING A QUALITY HARNESS").
