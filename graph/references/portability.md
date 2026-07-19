# Portability

Read this before committing to a cyclic topology on a platform you haven't verified supports one, and before assuming checkpointing works the same way everywhere.

## Contents

- What's safe to assume
- What's not safe to assume
- The DAG constraint
- Mapping table: graph concept to runtime

## What's safe to assume

Almost any orchestration environment can express nodes and directed edges - work happening in some order, sometimes conditionally. Build the design against nodes, edges, and a state schema first, described independently of any one platform's syntax, and adapt it during packaging.

## What's not safe to assume

- **Native cycles.** Some platforms are strictly directed-acyclic - a workflow can move forward through steps but cannot route back to an earlier one within the same execution. This is the single biggest portability constraint for graphs and is covered on its own below.
- **A shared state object for free.** Some platforms pass output from one step directly into the next step's input and nothing else; anything meant to be read several steps later has to be explicitly threaded through every step in between, or written to external storage.
- **True parallelism.** Some workflow engines simulate "parallel" branches by running them sequentially and only presenting the result as if they'd run together. If timing or true concurrency matters, check what the platform actually does under the label "parallel."
- **Checkpointing as a given.** Some platforms checkpoint automatically after every step; others require you to explicitly persist state if the graph needs to survive a pause or crash.

## The DAG constraint

Platforms built around directed acyclic graphs cannot natively express a cycle-back edge - there's no "go back to step 2" within one execution. When you need retry, replan, or state-machine behavior on one of these platforms, you have two honest options:

1. **Model the retry as a bounded, unrolled sequence.** Instead of "go back to execute," define execute-attempt-1, evaluate-1, execute-attempt-2, evaluate-2, up to your iteration cap, each a distinct step. This works cleanly for small, known caps and keeps the platform's native guarantees intact.
2. **Wrap the DAG in an outer loop.** Run the whole DAG as one unit, inspect its result, and re-invoke it from outside if the evaluation says to retry - with the iteration cap enforced by the calling code or workflow, not by the DAG itself, since the DAG has no way to enforce it internally.

Do not silently drop the cycle budget because the platform made cycles inconvenient. The two options above still need the same cap and the same wired-exit discipline from `loop/references/exit-conditions.md` - they just live in a different place in the implementation than they would on a natively cyclic platform.

## Mapping table: graph concept to runtime

| Graph concept | Cyclic graph runtime (for example a state-graph framework) | Durable workflow engine | Managed DAG / pipeline service | Managed state-machine service |
|---|---|---|---|---|
| Node | A function or class registered against a node name | An activity or a sub-workflow call | A task or operator | A state |
| Conditional edge | A routing function returning the next node name | An `if` branch in workflow code | A branch operator, or a separate DAG triggered conditionally | A choice state |
| Fan-out / fan-in | Multiple edges from one node, a join node waiting on all or some | Parallel activity calls, awaited together | Parallel task groups with defined downstream dependencies | A parallel state, or a map state over a collection |
| Cycle-back | A native conditional edge back to an earlier node | A loop inside workflow code, budget enforced in that code | Not natively supported - see "the DAG constraint" above | A choice state routing backward, watched against the platform's own execution-history limits |
| Shared state | An explicit state object threaded through every node | The workflow's durable execution state | Data passed between tasks via the platform's data-passing mechanism, or an external store | The state machine's input/output payload |
| Checkpoint | Depends on the framework; often needs an explicit persistence layer | Native - the engine persists state automatically | Depends on the service; some checkpoint per task, some do not | Native - the service tracks execution state per step |
