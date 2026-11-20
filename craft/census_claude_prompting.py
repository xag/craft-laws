"""A census: Anthropic, Claude Docs, Prompting best practices, whole.

The review's address,
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts, served on
2026-11-20 the whole "Prompting best practices" page
(https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices),
of which "Chain complex prompts" is one section; the page is what was read. A source is adopted
entire or not at all (the source-the-rule protocol). The census unit is each guideline the page
states for current models: each bold lead or bullet of its techniques and its migration list,
and each sample prompt it offers as one unit. The model-specific table points to other pages;
the code samples and the sentences explaining a guideline state none of their own. Its rules
are for writing prompts and briefing agents, which is practice work here; those that configure
the API for a named model, and the blocks it offers for applications handling payments or
medicine, are set aside.

What prompted it: the review of a written design for listing a design's flaws, 2026-11-20, which relied on
"Explicit prompt chaining [...] is still useful when you need to inspect intermediate outputs" for why a request per flaw lets a person inspect the work in between.

    python -m craft.census_claude_prompting
"""

from __future__ import annotations

# guideline -> (route, the law that carries it or "", one line on the mapping)
CENSUS: dict[str, tuple[str, str, str]] = {
    'Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals before applying it to another.': (
        'owed', '', "a technique's population named and re-checked; a-rate-names-the-population-it-was-computed-over holds the stating half"),
    'If you want Claude to do more than the task strictly requires, explicitly request it rather than relying on the model to infer this from vague prompts.': (
        'owed', '', 'a brief that states its scope; a reading of the brief'),
    'Key test: Show your prompt to a colleague with minimal context on the task and ask them to follow it.': (
        'owed', '', 'a brief tried on a reader without its context'),
    'Be specific about the output format and constraints you want.': (
        'owed', '', 'a reading of the brief'),
    'Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters.': (
        'owed', '', "decidable from the brief's form once its order matters"),
    'Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can give Claude more information about your goals': (
        'owed', '', 'an instruction carries its reason; a reading'),
    'When adding examples, make them: Relevant [...] Diverse [...] Structured: Wrap examples in <example> tags': (
        'owed', '', 'the tags are decidable; relevance and diversity are readings'),
    'Include 3–5 examples for best results.': (
        'owed', '', 'decidable by counting'),
    'Use consistent, descriptive tag names across your prompts.': (
        'owed', '', 'decidable across a set of prompts'),
    'Nest tags when content has a natural hierarchy': (
        'owed', '', "decidable from the prompt's structure"),
    "Setting a role in the system prompt focuses Claude's behavior and tone for your use case.": (
        'set aside', '', 'an option, not a requirement'),
    'Put long-form data at the top: Place your long documents and inputs near the top of your prompt, above your query, instructions, and examples.': (
        'owed', '', "decidable from the prompt's order"),
    'Structure document content and metadata with XML tags': (
        'owed', '', "decidable from the prompt's structure"),
    'Ground responses in quotes: For long document tasks, ask Claude to quote relevant parts of the documents first before carrying out its task.': (
        'owed', '', 'a ground quoted from the record; the account law a-ground-is-a-quotation-from-the-record holds it for arguments'),
    'If you would like Claude to identify itself correctly in your application or use specific API strings: [sample prompts]': (
        'set aside', '', 'application configuration'),
    "After completing a task that involves tool use, provide a quick summary of the work you've done.": (
        'set aside', '', 'an option, for those who want it'),
    'Tell Claude what to do instead of what not to do': (
        'owed', '', 'a reading of the brief'),
    'Use XML format indicators': (
        'owed', '', 'decidable from the brief'),
    'Match your prompt style to the output you want': (
        'owed', '', 'a reading of the brief'),
    'Use detailed prompts for specific formatting preferences': (
        'owed', '', 'a reading of the brief'),
    'If you prefer plain text, add the following instructions to your prompt: Format your response in plain text only. Do not use LaTeX': (
        'set aside', '', 'an option'),
    'Create a professional presentation on [topic]. Include thoughtful design elements, visual hierarchy, and engaging animations where appropriate.': (
        'set aside', '', 'a sample for one kind of output'),
    'For Claude to take action, be more explicit: [...] Change this function to improve its performance.': (
        'owed', '', 'a brief names the act it wants; a reading'),
    '<default_to_action> [...] </default_to_action> / <do_not_act_before_instructions> [...] </do_not_act_before_instructions>': (
        'set aside', '', 'two opposite options'),
    'The fix is to soften any aggressive language. Where you might have said “CRITICAL: You MUST use this tool when...,” you can use more normal prompting such as “Use this tool when...” instead.': (
        'owed', '', 'a reading of the brief, for the models named'),
    'If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. [...] Never use placeholders or guess missing parameters in tool calls.': (
        'owed', '', 'decidable from a transcript: independent calls sent together'),
    'Replace blanket defaults with more targeted instructions.': (
        'owed', '', 'a reading of the brief'),
    'Remove over-prompting. [...] Instructions such as “If in doubt, use [tool]” cause overtriggering.': (
        'owed', '', 'a reading of the brief'),
    'Use effort as a fallback. If Claude continues to be overly aggressive, use a lower setting for effort.': (
        'set aside', '', 'API configuration for named models; not a rule of the work'),
    "When you're deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning.": (
        'set aside', '', 'an option against long thinking; a-view-changes-on-new-observation-not-to-agree is its neighbour'),
    'Prefer lowering the effort setting or using max_tokens as a hard limit with adaptive thinking. [...] Consider moving to adaptive thinking.': (
        'set aside', '', 'API configuration for named models; not a rule of the work'),
    'After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding.': (
        'set aside', '', 'an option'),
    'Prefer general instructions over prescriptive steps. A prompt such as “think thoroughly” often produces better reasoning than a hand-written step-by-step plan.': (
        'owed', '', 'a reading of the brief; it pulls against the numbered-steps guideline where order does not matter'),
    'Multishot examples work with thinking. [...] Present each example as a problem, the method to apply, and the expected answer.': (
        'owed', '', "decidable from the examples' parts"),
    'Manual chain-of-thought (CoT) prompting as a fallback. When thinking is off, you can still encourage step-by-step reasoning': (
        'set aside', '', 'API configuration for named models; not a rule of the work'),
    'Ask Claude to self-check. Append something like “Before you finish, verify your answer against [test criteria].”': (
        'owed', '', "a self-check against stated criteria; not the user's surface that done-is-observed-where-the-user-stands asks for"),
    'When extended thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word “think” and its variants.': (
        'set aside', '', "one model's behaviour"),
    'If you are using Claude in an agent harness that compacts context or allows saving context to external files (as in Claude Code), consider adding this information to your prompt': (
        'set aside', '', 'harness configuration'),
    'Use a different prompt for the very first context window: Use the first context window to set up a framework (write tests, create setup scripts), then use future context windows to iterate on a todo-list.': (
        'owed', '', "a long task's first session sets up its tests and scripts"),
    'Have the model write tests in a structured format: Ask Claude to create tests before starting work and keep track of them in a structured format (for example, tests.json).': (
        'owed', '', 'decidable from the repository: tests before the work, in a structured record'),
    'Set up convenience tools: Encourage Claude to create setup scripts (for example, init.sh) to gracefully start servers and run test suites and linters.': (
        'owed', '', 'decidable from the repository'),
    'Choose between starting fresh and compacting: [...] Be prescriptive about how it should start': (
        'owed', '', 'a reading of the brief'),
    'Provide verification tools: As the length of autonomous tasks grows, Claude needs to verify correctness without continuous human feedback. Tools that let Claude verify UI work are helpful': (
        'covered', 'done-is-observed-where-the-user-stands', 'the observation of the surface the law asks for needs such a tool'),
    'Encourage complete usage of context: Prompt Claude to efficiently complete components before moving on': (
        'set aside', '', 'an option'),
    'Use structured formats for state data: When tracking structured information (such as test results or task status), use JSON or other structured formats': (
        'owed', '', "decidable from the state's files"),
    'Use unstructured text for progress notes: Freeform progress notes work well for tracking general progress and context.': (
        'owed', '', "the-trail-is-written-as-it-happens holds the trail of a failure; this is a long task's"),
    "Use git for state tracking: Git provides a log of what's been done and checkpoints that can be restored.": (
        'owed', '', "decidable from the repository's history"),
    'Emphasize incremental progress: Explicitly ask Claude to keep track of its progress and focus on incremental work.': (
        'owed', '', 'a reading of the brief'),
    "Consider the reversibility and potential impact of your actions. [...] for actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding. [...] don't bypass safety checks (e.g. --no-verify)": (
        'owed', '', "decidable from a transcript: a destructive or shared act preceded by the person's yes"),
    'If your agent handles payments, account numbers, or figures that other people rely on, Anthropic recommends adding the following block to your system prompt.': (
        'set aside', '', "a block for agents handling payments and records; its 'Say a check was done only if a tool result in this session showed it' is done-is-observed-where-the-user-stands' neighbour"),
    'Provide clear success criteria: Define what constitutes a successful answer to your research question.': (
        'covered', 'a-protocol-is-an-artifact-before-the-run', 'what counts as success fixed before the run'),
    'Encourage source verification: Ask Claude to verify information across multiple sources.': (
        'owed', '', 'decidable from a research record: a claim and its sources'),
    'Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration.': (
        'owed', '', 'what-else-might-this-be-is-asked-before-closing and calibration-is-agreed-before-the-case are its neighbours'),
    'Ensure well-defined subagent tools [...] Let Claude orchestrate naturally': (
        'set aside', '', 'harness configuration'),
    "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating.": (
        'owed', '', 'decidable from a transcript once each delegated task records why'),
    'Explicit prompt chaining (breaking a task into sequential API calls) is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure.': (
        'set aside', '', 'when chaining helps; a reading'),
    'The most common chaining pattern is self-correction: generate a draft → have Claude review it against criteria → have Claude refine based on the review.': (
        'set aside', '', 'describes a pattern'),
    'If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task.': (
        'set aside', '', 'an option'),
    'Avoid over-engineering. Only make changes that are directly requested or clearly necessary.': (
        'covered', 'the-work-is-compared-against-the-ask', 'work the ask did not require, recorded and questioned'),
    'Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values [...] If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them.': (
        'owed', '', 'a-detour-is-announced-as-a-detour holds the reporting half; a special-cased test is decidable from the diff'),
    'Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering.': (
        'covered', 'the-systems-own-record-is-read-first', 'the record read before the first theory'),
    'One technique that has proven effective to further boost performance is to give Claude a crop tool or agent skill.': (
        'set aside', '', 'harness configuration'),
    '<frontend_aesthetics> [...] </frontend_aesthetics>': (
        'set aside', '', 'a taste prompt for front ends'),
    'If people might ask your application about medicine doses, add the following block for the model your application calls to your system prompt, exactly as written.': (
        'set aside', '', 'a block for applications answering about medicine'),
    "Be specific about the behavior you want: Consider describing exactly what you'd like to see in the output.": (
        'owed', '', "the migration list's restatement of being specific"),
    'Frame your instructions with modifiers: Adding modifiers that encourage Claude to increase the quality and detail of its output': (
        'set aside', '', 'an option'),
    'Request specific features explicitly: Ask explicitly for animations and interactive elements when you want them.': (
        'owed', '', "the migration list's restatement of asking for more explicitly"),
    'Update thinking configuration': (
        'set aside', '', 'API configuration for named models; not a rule of the work'),
    'Migrate away from prefilled responses: Prefilled responses on the last assistant turn are no longer supported': (
        'set aside', '', "API configuration for named models; not a rule of the work; the section's replacements for each prefill use go with it"),
    'Tune anti-laziness prompting: If your prompts previously encouraged the model to be more thorough or use tools more aggressively, reduce that guidance.': (
        'owed', '', 'a reading of the brief'),
    'Pass thinking blocks back unchanged and keep history append-only': (
        'set aside', '', 'API configuration for named models; not a rule of the work'),
}

ROUTES = ("covered", "owed", "set aside")
SOURCE_COUNT = 71


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter
    ap = argparse.ArgumentParser(prog="python -m craft.census_claude_prompting",
                                 description=__doc__.splitlines()[0])
    ap.parse_args(argv)

    if len(CENSUS) != SOURCE_COUNT:
        print(f"the census carries {len(CENSUS)} of the page's {SOURCE_COUNT} guidelines")
        return 1

    from craft.laws import LAWS
    from craft.practice import PRACTICE
    ids = {l.id for l in PRACTICE} | {l.id for l in LAWS}
    missing = [(rule, law) for rule, (route, law, _) in CENSUS.items()
               if route == "covered" and law not in ids]

    tally = Counter(route for route, _, _ in CENSUS.values())
    print(f"Anthropic, Claude Docs, Prompting best practices: {len(CENSUS)} classified\n")
    for rule, (route, law, note) in CENSUS.items():
        print(f"  {route:<9} {rule}")
        if law:
            print(f"            -> {law}")
    print()
    for route in ROUTES:
        print(f"  {route:<10} {tally.get(route, 0)}")
    if missing:
        for rule, law in missing:
            print(f"\n  BROKEN  {rule} names law {law!r} and no such law exists")
        return 1
    print("\n  Every covered guideline names a law that exists - checked against the "
          "laws, not asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
