---
name: loop-forge
description: Design and harden the internal iteration control of a single reasoning unit, retry mechanism, or converging process. Use when someone wants an agent, script, or workflow step to try, check, and try again - a retry loop, a draft-critique-revise cycle, a debugging loop, a reconciliation loop, or any "keep going until X" behavior. Trigger for requests like "make it keep trying until it gets this right," "build a retry loop for this," "how do I stop this from looping forever," or "give this agent a real stop condition." Produces a portable LOOP.md that defines the archetype, the round, and - most importantly - wired exit conditions instead of a vague "stop when done."
---

# Loop forge

A loop is one process that acts, observes what happened, and lets that observation change what it does next. That's the whole definition. If round two of something doesn't actually change because of what round one produced, you don't have a loop. You have a pipeline that ran twice and got lucky, or unlucky, on the second pass.

Most broken "agentic loops" aren't broken because the archetype was wrong. They're broken because the exit condition was *named* - a comment, a docstring, a line in a prompt saying "stop when the task is done" - but never *wired*: never turned into a check that actually runs every round and actually halts execution. This file exists to stop you from shipping a named exit and calling it a stop condition.

Read this whole file before writing anything. The interview and the exit-condition design come before the archetype gets picked, not after.

## What a loop actually is

Three things distinguish a real loop from things that look like one:

- **The true loop test.** Does the outcome of round N change what happens in round N+1? If yes, it's a loop. If every round would produce the same action regardless of what the previous round returned, it's not a loop, it's the same step running repeatedly with no feedback.
- **Fan-out is not a loop.** Firing off five independent workers in parallel and collecting their results is not a loop, even if it feels like one. None of those workers' outputs change what the others do. That's a graph shape (fan-out / fan-in) - see `graph/GRAPH.md` in this repository. If you catch yourself calling a parallel batch a "loop," you're about to build the wrong thing.
- **A loop needs an exit that runs, not an exit that's named.** Covered in full in Phase 3. It's the single most common failure mode, so it gets its own phase instead of a bullet point.

## Where a loop sits relative to a skill, agent, or graph

These solve different problems and none of them replaces the others:

- A **skill** is reusable know-how for a type of task - what to do.
- An **agent** owns a goal over time and decides what to do next - who's responsible.
- A **loop** is how a single unit of work converges through repeated action - how one node gets to done.
- A **graph** is how multiple units, including loops, wire together into a controlled flow - how many nodes cooperate.

An agent's operating loop (see `agent/AGENT.md`, Phase 3) is a loop. Writing it as one - with an archetype and wired exits, instead of a generic ten-step list - is exactly what turns a vague agent prompt into something that reliably stops. A loop is also frequently one node inside a larger graph, connected back to itself by a cycle edge. See "Loops inside graphs" near the end of this file.

## Phase 1: Interview

Understand the convergence before you pick a shape. Mine any existing code, prompt, or description of the current behavior before asking questions. Fill the remaining gaps:

1. **What is this loop trying to converge on?** State it as a single measurable condition, not a feeling. "The generated SQL runs without error and returns at least one row" is measurable. "The answer is good" is not.
2. **What changes between rounds?** Name the specific piece of state that gets updated by the observation and feeds the next action. If you can't name it, you don't need a loop - you need one attempt with a single retry, or nothing at all.
3. **What archetype fits the convergence?** Answered in Phase 2.
4. **What ends it on success?** The exact check, described concretely enough that someone else could implement it without asking you what "good" means.
5. **What ends it on failure or exhaustion?** Every loop needs at least one hard cap that doesn't depend on the success check being correct: an iteration cap, a cost cap, a wall-clock cap, or an action-count cap. If the success check has a bug, this is the only thing standing between the loop and running forever.
6. **What counts as stagnation?** Two or more rounds that produce the same action, the same output, or no measurable change in state. Decide how you'll detect it before you need it.
7. **What can interrupt it mid-flight, and what happens to state when it does?** A human abort, an external cancel signal, an upstream timeout. Decide whether a partial round completes or aborts cleanly.
8. **What is allowed to happen on each round?** Read-only observation is cheap to retry. Sending an email or writing to a database is not. If a round can take an irreversible or costly action, that changes the exit-condition bar - see `references/exit-conditions.md`.
9. **Where does it report state while running, and its result when it stops?** Someone watching this loop from outside needs to know it's alive and making progress, not just see a result at the end or a timeout with no explanation.

Push on the failure and exhaustion questions now. An interview that only covers the happy path produces a loop that only handles the happy path.

## Phase 2: Choose the archetype

Pick the shape that matches how convergence actually happens. Read `references/anatomy.md` for the full table with failure modes; the short version:

- **Fixed-step.** A predetermined number of rounds, then stop - N-of-M sampling, majority vote over several attempts. Cheapest to reason about. No adaptive stopping, so it wastes rounds on easy cases and gives up on hard ones at exactly the same point.
- **Converge-on-metric.** Keeps going until a scored quality or confidence value crosses a threshold or plateaus - draft, critique, revise, re-score. Needs a scoring function you actually trust; a bad or gameable scorer makes this archetype worse than fixed-step, not better.
- **Tool loop (observe - decide - act).** Observe the environment or a tool's result, decide the next action, act, repeat until the goal state is reached or no useful action remains. The standard shape for debugging loops, research loops, and most agent tool use.
- **Plan - execute - replan.** Build a plan up front, execute its steps, and replan only when a step fails or the environment changes underneath it. Cheaper than re-planning every round; brittle if the environment changes in ways the plan didn't anticipate and nothing notices.
- **Human-gated.** The loop pauses at a checkpoint and waits for approval before the next round runs. Required whenever a round's action is costly, irreversible, or outside the loop's authority to decide alone.
- **Watchdog / reconciliation.** Continuously compares a desired state against actual state and nudges toward it. Doesn't "finish" in the normal sense - it runs indefinitely, so its exit condition is a health or kill switch rather than a completion check. Different exit-condition discipline than the other five archetypes; see `references/exit-conditions.md`.

## Phase 3: Design the exit conditions

This is the part most loops get wrong, so do it deliberately rather than as an afterthought to Phase 2.

- **Success exit.** The exact check from interview question 4. Write it as something you could implement today, not a description you'll refine later.
- **Budget exit.** At minimum one of: an iteration cap, a cost cap, a wall-clock cap, an action-count cap. This exit must not depend on the success check being correct - it's the backstop for when the success check has a bug or the task is genuinely unsolvable.
- **Stagnation exit.** Detect when round N looks like round N-1: same action chosen, same output produced, no change in the state that's supposed to be converging. Stop instead of burning the rest of the budget on rounds that were never going to help. This exit applies to archetypes that adapt their action based on feedback - tool loops, converge-on-metric, plan-execute-replan. It does not apply to fixed-step: a fixed-step retry that repeats the identical action every round is working as designed, not stagnating, and the budget exit alone is enough to bound it.
- **Escalation exit.** The condition under which the loop stops trying and hands off to a human or another process, instead of either continuing or failing silently. Write it as a threshold, not a vibe: "hand off after two consecutive failed attempts at the same action," not "hand off if it seems stuck."

The distinction that matters most: a **named** exit is a comment or a line in a prompt that says the loop should stop under some condition. A **wired** exit is a check that actually executes every round and actually halts the loop when it's true. Most loops that run away have a named exit and no wired one. Before you consider this phase done, point at the exact place in the design where each exit condition gets evaluated, every round, without exception.

Read `references/exit-conditions.md` for stagnation-detection patterns, budget types for costly or irreversible actions, and worked good/bad examples.

## Phase 4: Write the LOOP.md

Start with metadata:

```yaml
---
name: sql-repair-loop
description: Iteratively fix a generated SQL query until it executes successfully against the target database or the retry budget is exhausted. Use after SQL generation whenever the first attempt might fail on syntax, missing columns, or type mismatches.
---
```

A useful body usually contains:

1. **Archetype** - which of the Phase 2 shapes, and why it fits this convergence.
2. **Round** - what happens exactly once per iteration: observe, act, check.
3. **Exit conditions** - success, budget, stagnation, escalation, each concrete.
4. **State carried between rounds** - what updates each round versus what's fixed context.
5. **Examples** - one or two short worked rounds showing state before and after.

Write in the imperative, explain the reasoning behind non-obvious caps (why five iterations and not fifty), and keep it short enough that someone implementing this in code or in a prompt doesn't have to guess at anything load-bearing.

## Phase 5: Test it

Run the design, on paper or for real, against these cases before calling it done:

1. **The case that should converge quickly.** Confirms the success exit actually fires on a clean win.
2. **The case that never converges.** Confirms the budget exit fires - not the success exit failing to fire, the budget exit actually stopping execution.
3. **A stagnating case**, where two rounds in a row produce the same action or output. Confirms stagnation is detected and the loop stops instead of grinding through the rest of its budget.
4. **An interrupted case.** A human or external signal aborts mid-round. Confirms state doesn't end up half-updated or inconsistent.

If any of these four don't behave as designed, the fix is almost always in the exit conditions from Phase 3, not in the archetype.

## Phase 6: Package

Deliver a self-contained loop folder:

```text
loop-name/
├── LOOP.md
├── references/   (if any - project-specific detail beyond this base file)
└── templates/     (if any)
```

For most single loops, `LOOP.md` alone is enough. Add supporting files only when there's genuinely reusable detail - a shared stagnation-detection routine used by several loops, or a set of domain-specific convergence checks.

## Loops inside agents

An agent's operating loop is a loop. If an agent's actions have any real cost or reversibility risk attached, write its operating loop as a proper `LOOP.md` - archetype chosen deliberately, exits wired rather than named - instead of leaving it as a generic observe-decide-act list. The agent owns the goal; the loop is how it gets there each time it acts.

## Loops inside graphs

A loop is frequently just one node in a larger graph, wired back to itself with a cycle edge. When a retry or replan needs to span more than one node - fail in node B, go back to node A - that's a graph-level cycle, not a loop, and it needs the same wired-exit discipline applied at the graph level. See `graph/GRAPH.md`, Phase 3, "cycle budgets."

## Resources in this loop

- `references/anatomy.md` - the true loop test in depth, the archetype table with failure modes, and why fan-out isn't a loop.
- `references/exit-conditions.md` - stagnation detection, budget types for costly or irreversible actions, and good/bad worked examples of exit-condition writing.
- `references/portability.md` - how the loop concept maps onto different runtimes, and what each one won't let you assume.
- `templates/LOOP.template.md` - a starter LOOP.md with the structure filled in as prompts.

Now go build the smallest loop that reliably knows when to stop.
