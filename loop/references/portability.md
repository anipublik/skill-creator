# Portability

Read this when you don't know which runtime will execute the loop, or when a target platform's limits are shaping the design more than the convergence logic is.

## Contents

- What's safe to assume
- What's not safe to assume
- Mapping table: loop concept to runtime
- A note on unbounded loops

## What's safe to assume

Nearly every execution environment - plain code, a graph runtime, a workflow engine, a plain chat with a capable model - can express "do a thing, check a condition, decide whether to do it again." That's the one primitive `LOOP.md` actually depends on. Build the design against that, and it will port almost anywhere with only the exit-condition mechanics changing.

## What's not safe to assume

- **Unlimited iteration.** Several managed runtimes cap how many times a construct can loop, or how much history a single execution can accumulate, before you have to explicitly restart it. Don't assume your iteration cap is the only limit in play - check the platform's own ceiling and design under it.
- **State persistence across rounds for free.** Some environments hold state in memory naturally across a loop; others need it written to an explicit external store (a database row, a file, a workflow's durable state) or it's gone the moment execution pauses.
- **A distinction between "paused" and "dead."** In code, a paused loop is just a thread waiting. In some serverless or workflow platforms, a long pause between rounds is a different execution entirely, reconstructed from checkpointed state - which matters for how you implement the human-gated archetype.
- **Free retries.** A tool loop's retries might carry real cost (API calls, compute) that a platform meters separately from its own iteration limits. Don't let a platform's generous iteration cap hide a budget problem the design was supposed to catch.

## Mapping table: loop concept to runtime

| Loop concept | Plain code | Graph runtime (for example a state-graph framework) | Durable workflow engine | Managed workflow / state-machine service |
|---|---|---|---|---|
| The round | One pass through a `while` or `for` body | One node's execution | One activity or step inside the workflow function | One state execution |
| The cycle-back | The loop construct itself | A conditional edge routing back to the same node | A loop inside workflow code, or a re-invocation of the workflow | A choice state routing back to an earlier state, watching the platform's own iteration ceiling |
| Iteration cap | A counter variable checked each pass | A counter carried in shared state, checked by the routing condition | A counter in workflow state; some engines require periodically restarting the workflow run to avoid unbounded history | A counter in the state machine's data, compared in a choice state |
| State across rounds | In-memory variables | The graph's shared state object | The workflow's durable state, survives process restarts natively | The state machine's execution input/output, passed explicitly between states |
| Human-gated pause | Blocking on external input, or a persisted flag checked on resume | A node that halts execution pending an external signal | A native "wait for signal" or "wait for external event" primitive | A native "wait for task token" or callback pattern |

## A note on unbounded loops

The watchdog / reconciliation archetype is intentionally unbounded - it's supposed to run indefinitely. On some platforms "indefinitely" isn't actually available as a native concept; you get periodic re-invocation instead (a scheduled trigger that re-runs a short-lived check rather than one long-lived process). That's a fine substitute mechanically, but make sure the "state hasn't narrowed for N consecutive checks" logic from `references/exit-conditions.md` is tracked across those separate invocations, not reset each time - otherwise the platform's re-invocation model quietly breaks your stagnation detection.
