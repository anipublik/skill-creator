# Graph anatomy

Read this when choosing between topologies that both seem to fit, or when a graph you built is failing in a way that looks like a wiring problem rather than a node problem.

## Contents

- The parts of a graph
- Topology diagrams
- Common failure patterns by topology
- When a graph is actually two graphs

## The parts of a graph

| Part | Purpose |
|---|---|
| Node | One unit of work - a loop, an agent, a skill, a tool, a router, or a human gate |
| Edge | A path control and state can travel, sequential, conditional, parallel, or cycle-back |
| Entry node | Where the graph starts |
| Terminal node | Where a given path through the graph ends |
| Shared state | The payload that travels along edges, distinct from any one node's private working memory |
| Checkpoint | A saved point the graph can resume from after a pause or crash |

## Topology diagrams

**Pipeline**

```text
[A] -> [B] -> [C]
```

**Branch / router**

```text
              -> [B]
[A] -> router
              -> [C]
```

**Fan-out / fan-in**

```text
        -> [B] ->
[A]                [D]
        -> [C] ->
```

**Supervisor / worker**

```text
        [worker-1]
[super] [worker-2]
        [worker-3]
```
The supervisor calls workers in whatever order and combination its own judgment picks; workers don't call each other.

**State machine (cyclic)**

```text
[plan] -> [execute] -> [evaluate] -+
   ^                                |
   +--------------------------------+  (cycle-back on failed evaluation)
```

**Hierarchical**

```text
[A] -> [sub-graph entry ... sub-graph exit] -> [C]
```

## Common failure patterns by topology

- **Pipeline:** a step gets added mid-sequence "temporarily" for a special case, and six months later the pipeline is really a branch that nobody ever formalized. If you find yourself describing a pipeline with "except when," it's a branch, draw it as one.
- **Branch / router:** the router node quietly starts doing judgment work beyond picking a destination - scoring, partial processing, decision-making that belongs in an agent node. A router should route. If it's doing more than that, split it.
- **Fan-out / fan-in:** the fan-in node waits for all branches with no timeout and no partial-result policy, so one slow or stuck branch stalls a result that was otherwise ready. Every fan-in needs an explicit answer to "what if branch B never finishes" - and often the right answer isn't a timeout bolted onto an all-wait design, it's designing the join as a quorum (2 of 3) or a race (first N) from the start, because that's a cleaner fit for genuinely independent checks than treating a slow branch as an exception case.
- **Supervisor / worker:** workers start calling each other directly to save a round trip through the supervisor, which erodes the supervisor's ability to see or control what's actually happening. If workers need to coordinate with each other, that coordination should be visible to the supervisor, not routed around it.
- **State machine (cyclic):** a cycle-back edge gets added to handle a retry, and nobody gives it its own budget - so it inherits whatever the graph's outer timeout is, which is usually far too generous for what should have been a fast, bounded retry.
- **Hierarchical:** the parent graph's state schema and the sub-graph's state schema aren't reconciled, so data silently doesn't make it across the boundary in one direction or the other. Treat the sub-graph's entry and exit like any other node contract - explicit inputs, explicit outputs. Separately, the sub-graph's own cycle budgets are invisible to the parent by default - a parent-level timeout doesn't know the sub-graph already spent most of its allowance retrying internally. If the hierarchical node needs an overall cap, state it at the parent level explicitly rather than assuming the sub-graph's internal budget covers it.

## When a graph is actually two graphs

If two clusters of nodes share no state, no failure recovery path, and would never need to route into each other, they're not one graph with a wide topology - they're two graphs that happen to be described in the same document. Split them. A single graph should represent one outcome with one owner for the overall goal, matching the same principle `agent/AGENT.md` applies to agent teams: adding more to a system should make responsibility clearer, not harder to trace.

"Shares state" here means shared mutable state within one run - a field one cluster writes and the other reads *during the same execution*, as part of reaching the same outcome. It doesn't mean one graph's completed output being read later as input to a separate graph's separate run. A weekly report generator that reads yesterday's moderation decisions from a log isn't sharing state with the moderation pipeline; it's consuming a finished artifact, the same way any two independent systems can have a data dependency without being one system. If the two clusters run on different triggers, at different times, toward different outcomes, and neither waits on the other mid-run, they're still two graphs - split them even if one happens to read the other's output.
