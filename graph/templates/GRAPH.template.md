---
name: [short, lowercase, hyphenated]
description: [The outcome this topology produces, and when to reach for it. One to three sentences.]
---

# [Graph name]

[One or two sentences: the outcome this topology exists to produce, and why one node wasn't enough.]

## Topology

[Which shape(s) from GRAPH.md Phase 2, and a small diagram.]

```text
[node] -> [node] -> [node]
```

## Nodes

| Node | Kind | Purpose | Inputs | Outputs | Failure behavior |
|---|---|---|---|---|---|
| [name] | [loop / agent / skill / tool / router / human-gate] | | | | |

For any fan-in node, state its join policy in Purpose or Inputs: wait for all, wait for a quorum (N of M), or take the first N. "Waits for the branches" is not a policy.

## Edges and routing

| From | To | Condition | Notes |
|---|---|---|---|
| | | | |

## Shared state

| Field | Owner | Readers | Durability |
|---|---|---|---|
| | | | |

## Failure and recovery

[Per-node fallback behavior. Cycle budgets for any cycle-back edge, with the exact cap and the consequence of hitting it. Checkpoint behavior if the graph can be paused or resumed.]

## Examples

[One or two worked traces: a normal path through the graph, and a branch or failure path, showing what state looked like at each node.]
