"""The sixth practice census: every failure mode of MAST, none skipped.

The source is Cemri, Pan, Yang et al., Why Do Multi-Agent LLM Systems Fail? (arXiv
2503.13657v3, October 2025) — the Multi-Agent System Failure Taxonomy: 14 failure
modes in 3 categories, derived from annotated agent traces. Captured whole at
docs/sources/cemri-2025-mast.pdf. Where Croskerry catalogues the *dispositions* behind
a wrong judgment, MAST catalogues the *observable trajectory failures* of agents — the
two censuses meet at verification, which is where this estate's costliest 2026-08-29
errors sat.

THE ANALOGY, stated once. MAST describes multi-agent systems; this estate mostly runs
one agent per session beside hooks, checkers and a human. The mapping reads
"inter-agent" as any boundary between parties — agent and hook, agent and subagent,
agent and human — and a mode that only exists with two or more coordinating LLM agents
is SET ASIDE and says so.

  covered      an existing law, decider or protocol already fires on the mode
  owed         the mode occurs in this estate's work and nothing fires on it;
               a law candidate
  set aside    exists only in multi-agent coordination this estate does not run

    python -m craft.census_mast
    python -m craft.census_mast --owed
"""

from __future__ import annotations

from collections import Counter

# mode -> (route, the source's own definition, what it means for the work here)
CENSUS: dict[str, tuple[str, str, str]] = {
    # --- FC1: system design issues ---------------------------------------------------
    "fm-1.1-disobey-task-specification": (
        "owed",
        "Failure to adhere to the specified constraints or requirements of a given "
        "task",
        "the ask narrowed, widened or transformed. This session's instance: the "
        "checker run by hand after the owner said the hook is for that. The scope "
        "doctrine is prose; nothing compares the diff or the acts against the ask"),
    "fm-1.2-disobey-role-specification": (
        "covered",
        "Failure to adhere to the defined responsibilities and constraints of an "
        "assigned role",
        "the state machines: invest's daemon cannot transition a thesis, arming is "
        "refused to non-humans, verdicts propose and never dispose — role walls "
        "enforced in code where they matter most"),
    "fm-1.3-step-repetition": (
        "owed",
        "Unnecessary reiteration of previously completed steps in a process",
        "the re-run of a finished step because its result fell out of view; billed "
        "twice, sometimes side-effecting twice. Tapes record repetition but nothing "
        "flags it"),
    "fm-1.4-loss-of-conversation-history": (
        "covered",
        "Unexpected context truncation, disregarding recent interaction history",
        "reasoning from one context written into another's record is already a "
        "recorded correction (corrections-outrun-the-laws), and the account lane "
        "anchors every ground to the transcript so a claim from a lost context "
        "fails to quote it"),
    "fm-1.5-unaware-of-termination-conditions": (
        "covered",
        "Lack of recognition of criteria that should trigger interaction termination",
        "a-stopped-run-says-why and the ruling-lifetime debt carry both directions: "
        "stopping without saying why, and continuing past a boundary a ruling set"),
    # --- FC2: inter-agent misalignment -----------------------------------------------
    "fm-2.1-conversation-reset": (
        "set aside",
        "Unexpected or unwarranted restarting of a dialogue, potentially losing "
        "context and progress",
        "a coordinating-agents phenomenon; the single-session analogue is context "
        "truncation, routed at fm-1.4"),
    "fm-2.2-fail-to-ask-for-clarification": (
        "owed",
        "Inability to request additional information when faced with unclear or "
        "incomplete data",
        "proceeding under an assumption where different readings diverge materially. "
        "The estate's prose says ask at the divergence; no check notices an "
        "assumption that should have been a question"),
    "fm-2.3-task-derailment": (
        "owed",
        "Deviation from the intended objective or focus of a given task",
        "the session that wanders from the ask into adjacent work. Same gap as "
        "fm-1.1 seen from the trajectory side: nothing compares what was done "
        "against what was asked"),
    "fm-2.4-information-withholding": (
        "covered",
        "Failure to share important data or insights that could impact other "
        "agents' decision-making",
        "the transponder protocol: work declared before it starts, changes said "
        "aloud on the channel, and a claim that omits its remainder is convicted "
        "by a-remainder-names-its-debt"),
    "fm-2.5-ignored-other-agents-input": (
        "covered",
        "Disregarding or failing to adequately consider input from other agents",
        "counter-evidence-is-answered: an attack filed and unanswered convicts. "
        "The human's correction entering as a law (a-human-found-defect-enters-as-"
        "a-law) is the same rule at the human boundary"),
    "fm-2.6-reasoning-action-mismatch": (
        "covered",
        "Discrepancy between logical reasoning and actual actions taken by the agent",
        "the claims lane exists for this: what was said is checked against what the "
        "tools actually did (evidence where the user stands, the says-residual, "
        "flight tapes under semantic spans)"),
    # --- FC3: task verification ------------------------------------------------------
    "fm-3.1-premature-termination": (
        "covered",
        "Ending interaction before all necessary information has been exchanged or "
        "objectives met",
        "finish-the-whole-task is doctrine and a-remainder-names-its-debt makes the "
        "undone part a named debt on the claim; the done-claim gate refuses "
        "producer-only evidence of completion"),
    "fm-3.2-no-or-incomplete-verification": (
        "covered",
        "Omission of proper checking or confirmation of task outcomes or system "
        "outputs",
        "done-is-observed-where-the-user-stands and make-it-fail-before-you-fix-it "
        "are this mode's laws, and both have convicted here. This session's silent "
        "hook believed working was this mode ESCAPING them: the laws bind claims, "
        "and no claim about the hook was ever filed — the mode's cost lands "
        "where its laws do not reach"),
    "fm-3.3-incorrect-verification": (
        "owed",
        "Failure to adequately validate or cross-check crucial information or "
        "decisions",
        "the verification that ran and verified nothing: this session's zero-node "
        "check read as all-pass. a-defect-in-what-a-check-reads-is-invisible-to-"
        "that-check states the class as a hypothesis; a-check-reports-what-it-"
        "could-not-judge is law for published checks — but an ad-hoc check "
        "assembled in-session is held to neither. The costliest owed row of both "
        "censuses"),
}

SOURCE_ROWS = 14
ROUTES = ("covered", "owed", "set aside")


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--owed", action="store_true",
                    help="only the modes that occur here and are unmet")
    args = ap.parse_args(argv)

    if len(CENSUS) != SOURCE_ROWS:
        print(f"the census carries {len(CENSUS)} of the taxonomy's {SOURCE_ROWS} modes")
        return 1

    if args.owed:
        for item, (route, quote, means) in CENSUS.items():
            if route == "owed":
                print(f"  {item}")
                print(f"       -> {means}\n")
        return 0

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"MAST, every failure mode of the taxonomy: {len(CENSUS)} classified\n")
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    print()
    print(f"  {tally['covered']} occur here and a law or protocol fires on each; "
          f"{tally['owed']} are owed;")
    print(f"  {tally.get('set aside', 0)} exist only in coordination this estate "
          f"does not run.")
    print("  Run --owed for the queue — drained by frequency, not by buildability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
