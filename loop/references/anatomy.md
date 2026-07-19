# Loop anatomy

Read this when you need the full case for an archetype choice, when you're explaining to someone else why their "loop" isn't one, or when a loop nests inside other loops and you need to keep the rings straight.

## Contents

- The true loop test, in depth
- Why fan-out isn't a loop
- Loops nest - keep each ring's exit separate
- The archetype table, with failure modes
- Choosing between two archetypes that both seem to fit

## The true loop test, in depth

A loop exists when the outcome of round N changes what happens in round N+1. That's not a vibe check, it's a mechanical question: pick a specific piece of state, and ask whether round N actually writes to it, and whether round N+1 actually reads it before deciding its action.

If you can't point to that piece of state, you don't have a loop. You have one action wrapped in a `for` statement, running the same way every time regardless of what came before. That's not wrong to build - sometimes running the same deterministic check three times and taking a majority vote is exactly right - but it's a fixed-step archetype with no real feedback, and you should design it as one rather than dressing it up as an adaptive loop it isn't.

The test also catches the opposite mistake: a "loop" that reads state but never actually changes its action based on it. If round 4 does the exact same thing round 1 did, no matter what happened in between, the feedback path is decorative.

## Why fan-out isn't a loop

Firing off several independent workers - three research subtasks, five parallel validation checks - and collecting their results looks a lot like a loop from a distance: multiple rounds of work, a result at the end. It isn't one. None of the workers' outputs change what the other workers do. There's no round N+1 whose action depends on round N's outcome, because the workers don't have rounds relative to each other at all - they run once, in parallel, done.

This matters because designing fan-out as if it were a loop produces the wrong exit-condition thinking: you end up writing a stagnation check for something that was never going to stagnate, or a per-round budget for work that has no rounds. Fan-out and fan-in are graph shapes. See `graph/GRAPH.md` in this repository, Phase 2.

The one place these blend: a supervisor node that fans work out, collects results, and then - based on what came back - decides to fan out again with different instructions. That supervisor has a real loop (its own decide-observe cycle), and the fan-out is a graph shape nested inside one of its rounds. Two different things, correctly kept separate.

## Loops nest - keep each ring's exit separate

Rarely does one loop stand alone. A small loop that retries a single flaky tool call often sits inside a larger loop that retries a whole task, which in turn might sit inside a longer-running process that periodically adjusts how the task loop behaves based on results across many runs.

Each ring needs its own exit condition, evaluated at its own level. A failure inside the smallest ring should be handled - retried, escalated, or given up on - by that ring's own exit logic before it ever becomes something the outer ring, or a human, has to notice. When a small ring doesn't have a real exit, its failures leak upward: what should have been "retry this API call three times and move on" becomes "the whole task hung and someone had to go look."

Practical implication: when you're designing a loop and realize its "round" secretly contains its own retry behavior, that inner retry is very likely its own loop with its own LOOP.md, not a paragraph buried inside the outer loop's round description.

## The archetype table, with failure modes

| Archetype | Converges on | Common failure mode |
|---|---|---|
| Fixed-step | A predetermined round count | Wastes rounds on easy cases, gives up on hard ones at the same point regardless of difficulty |
| Converge-on-metric | A scored threshold or plateau | The scorer gets gamed or drifts, so the loop "succeeds" against a metric that stopped meaning what it did |
| Tool loop (observe-decide-act) | A goal state reachable through tool actions | Repeats a failing action with cosmetic variation instead of genuinely changing approach; needs stagnation detection more than any other archetype |
| Plan - execute - replan | Completion of a fixed plan, replanned on failure | The plan goes stale silently when the environment shifts in a way nothing is watching for, so it keeps executing a plan that no longer fits |
| Human-gated | Explicit approval at each checkpoint | The gate becomes a rubber stamp because the person approving never sees enough context to actually evaluate the round, defeating the point of the gate |
| Watchdog / reconciliation | Ongoing drift toward a desired state, never "finishes" | No completion check to misfire, but the kill switch is often missing entirely - it runs forever by design and nobody wired the thing that's supposed to stop it under bad conditions |

## Choosing between two archetypes that both seem to fit

When a tool loop and a plan-execute-replan both seem plausible, the deciding question is usually: does the next best action depend on information you only get by observing the environment fresh each round (tool loop), or can you commit to a sequence up front and only deviate on failure (plan-execute-replan)? Debugging is almost always the former - you don't know what's broken until you look. Multi-step data migrations are often the latter - you know the steps, you just need to handle a step failing partway through.

When converge-on-metric and human-gated both seem plausible, the deciding question is whether you trust the metric to catch the failure modes that matter. If the answer is "mostly, but not for the expensive mistakes," don't pick one - use converge-on-metric for ordinary rounds and add a human gate specifically at the point where the action becomes costly or irreversible, per `references/exit-conditions.md`.
