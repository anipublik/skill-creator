---
name: graph-forge
description: Design and package the orchestration topology connecting multiple nodes - agents, loops, skills, or tools - into a controlled flow. Use when someone needs a multi-step pipeline, a supervisor/worker system, branching logic, parallel fan-out and fan-in, or an explicit wiring diagram for how several steps hand off work and state to each other. Trigger for requests like "wire these agents together," "I need a pipeline with a branch," "how do these steps hand off to each other," "design a workflow with a retry," or "build a multi-agent system." Produces a portable GRAPH.md with node contracts, routing rules, a shared state schema, and cycle budgets for any retry or replan edge.
---

# Graph forge

A graph is what you build when one node isn't enough - when the outcome needs more than one actor, more than one decision point, or work that can genuinely run at the same time. A graph owns the wiring: who runs after whom, on what condition, sharing what state, and what happens when a node fails.

Read this whole file before drawing anything. Name the nodes and edges from the actual outcome, not from an org chart or a list of tools you happen to have.

## What a graph actually is

A graph is nodes connected by edges, where the edges carry control (what runs next) and state (what the next node gets to work with).

**Node types:**

- **Loop node** - a single unit iterating on its own convergence. See `loop/LOOP.md`.
- **Agent node** - owns a sub-outcome and makes its own decisions within it.
- **Skill node** - performs one bounded, reusable kind of work and returns.
- **Router node** - makes a pure routing decision based on state; does no other work.
- **Human-gate node** - the graph pauses here for approval before continuing.
- **Tool node** - a deterministic external call (an API, a database write, a script).

**Edge types:**

- **Sequential** - A always leads to B.
- **Conditional** - A leads to B or C depending on state.
- **Parallel fan-out** - A triggers B and C at the same time.
- **Fan-in** - D waits for B and C (some or all of them) before it runs.
- **Cycle-back** - control returns to an earlier node: a retry, a replan, an escalate-then-retry.

## A graph cycle is not the same as a loop

A loop is one node re-entering itself. A graph cycle can span several nodes before control comes back around - plan, execute, evaluate, back to plan - and it needs exactly the same wired-exit discipline a loop needs: a bounded number of times around the cycle, checked and enforced, not just described. See Phase 3, "cycle budgets." If a cycle-back edge has no cap of its own, a single stuck cycle can quietly consume the entire run's budget while every individual node reports success.

## Where a graph sits relative to a skill, agent, or loop

- A **skill** is reusable know-how - what to do.
- An **agent** owns a goal over time - who's responsible.
- A **loop** is how one node converges through repeated action.
- A **graph** is how several nodes, of any of the above kinds, cooperate to produce an outcome none of them owns alone.

An agent team - several `AGENT.md` files handing work to each other - is a graph. The handoff contract each agent already defines (sender, receiver, payload, timeout, fallback owner, per `agent/references/anatomy.md`) is the same information a graph's edge contract needs, described from the agent's point of view instead of the system's. Don't define it twice; see "Graphs as agent teams" near the end of this file.

## Phase 1: Interview

1. **What's the end-to-end outcome, and what are its real intermediate checkpoints?** Name the moments where state materially changes or a decision gets made. Don't design nodes yet.
2. **Which of those moments genuinely need a different actor, authority, or context?** Those become separate nodes. Moments that are just steps inside one actor's own work stay inside that one node.
3. **Where does work branch?** What decides the branch, and what are the possible destinations?
4. **Where does work need to run in parallel, and where must it rejoin before continuing?** Independent subtasks that don't need each other's results are fan-out candidates. At the rejoin point, decide the join policy explicitly: wait for all branches, wait for a quorum (say, 2 of 3 independent checks), or take the first N to complete and ignore the rest. "Fan-in" does not default to "wait for everything" - state which policy applies, because it changes both the node contract and what counts as a failure.
5. **Where does something need to retry, replan, or loop back?** How many times before it should stop trying and escalate instead?
6. **What state has to survive a hop between nodes?** Separate what's local to one node's own work from what has to travel with the edge, and from what has to be durable across the whole run.
7. **Where does a human actually have to be in the loop** - as an approval gate partway through, not just a recipient of the final output?
8. **What happens when a node fails outright** - timeout, error, no response? Does control move to a fallback node, retry the same node, or halt the whole graph?
9. **Does this run once per trigger, or does it need to resume after a crash or a pause?** That determines whether you need checkpointing.
10. **Does the target runtime support true cycles, or only a strict forward-only sequence?** Some platforms can't natively loop back. That changes which topologies are actually available to you - see `references/portability.md` before committing to a cyclic design.

## Phase 2: Choose the topology

Read `references/anatomy.md` for the full treatment and common failure patterns per shape. The short version:

- **Pipeline.** A strict sequence, A then B then C. Simplest to build and debug. Forces everything through one path even where a path never needed to diverge.
- **Branch / router.** One node's output decides which of several next nodes runs. Use where paths genuinely diverge, whether or not they reconverge later at a join.
- **Fan-out / fan-in.** One node triggers several in parallel, and a join node waits for some or all of them. Use for genuinely independent work - parallel validation checks, independent research subtasks.
- **Supervisor / worker.** One central node assigns and reviews work from several worker nodes it can call in any order, chosen by its own judgment. This is what `AGENT.md`'s capability map looks like once you draw the edges explicitly instead of leaving them as a table.
- **State machine (cyclic).** Nodes are states, edges are guarded transitions, and the graph can revisit earlier nodes. Most real systems that replan, retry, or escalate-then-retry end up here whether or not anyone designed it on purpose.
- **Hierarchical (graph of graphs).** A node in one graph is itself the entry point of another graph. Use when a sub-outcome is complex enough to deserve its own topology and flattening it into the parent would just hide the complexity, not remove it. A sub-graph's internal cycle budgets are local to it and are not automatically visible to or bounded by the parent - if the parent needs an overall cap on the total time or cost a hierarchical node can consume, including whatever retries happen inside its sub-graph, state that cap explicitly at the parent level too. Don't assume it's inherited.

Most real systems are more than one of these layered together - a pipeline with one branch point and one retry cycle is extremely common. Don't force the whole thing into a single named shape if it isn't one.

## Phase 3: Design nodes, edges, and state

### Node contracts

For every node, define:

| Field | Question |
|---|---|
| Purpose | What is this node for? |
| Kind | Loop, agent, skill, tool, router, or human-gate? |
| Inputs | What does it require to start, and from where? |
| Outputs | What does it produce, and in what shape? |
| Failure behavior | Timeout, error, fallback node, or retry - which, and how many times? |

A node without a contract is a name on a diagram with no way to build or test it. A fan-in node's contract additionally needs a stated join policy - wait for all, wait for a quorum (N of M), or take the first N and proceed - plus what happens to results that arrive after the join has already fired. "Waits for the parallel branches" is not a join policy; "waits for 2 of 3, discards or logs whichever result arrives late" is.

### Edges and routing rules

Write routing conditions as explicit checks on state: "route to the human-gate node if `confidence_score < 0.7`" is a rule. "Route to a human if it seems uncertain" is not - it just moves the judgment call into whichever node evaluates it, unstated. See `references/state-and-routing.md` for more good and bad examples.

A node's failure behavior (in its contract, above) covers its own execution going wrong - it ran long, it errored, it returned garbage. That's a different failure from a handoff going wrong: the sending node finished and passed control along, but nothing confirms the receiving node actually picked it up - a dropped message, a crash between send and receive, a queue nobody's draining. The first is the node's problem to declare. The second belongs to the edge: give any edge where silent drops are possible its own acknowledgment timeout and fallback owner, separate from what the receiving node does once it's actually running.

### Shared state schema

Define the payload that travels along edges. For every field: its owner (which node writes it), its readers (which nodes read it), and whether it's durable (must survive a pause or crash) or ephemeral (this run only). A field with no defined owner is the most common source of two nodes silently overwriting each other's work.

### Checkpointing and resumability

If the graph can be paused - a human gate, a long-running node, a crash - it needs enough persisted state to resume without repeating side effects that already happened. Define what a checkpoint actually captures: the current node, a snapshot of the shared state, and which upstream nodes' outputs already exist and shouldn't be regenerated.

### Cycle budgets

Every cycle-back edge needs its own iteration cap, evaluated and enforced at that specific edge - not just a global timeout on the whole graph. A global timeout catches a stuck cycle eventually, but only after it's burned the budget every other node in the graph was counting on. Give the cap a concrete number and a defined consequence (escalate, fall back, hard stop) when it's hit, exactly as `loop/references/exit-conditions.md` requires for a loop's budget exit - a graph cycle needs the same discipline, just enforced by the edge instead of by a node's internal check.

## Phase 4: Write the GRAPH.md

Start with metadata:

```yaml
---
name: incident-triage-graph
description: Route an incoming incident through classification, automated remediation attempts, and human escalation. Use when an incident-handling agent needs to branch between auto-remediation and human paging based on severity and remediation confidence.
---
```

A useful body usually contains:

1. **Topology** - which Phase 2 shape or combination, with a small diagram (ASCII or mermaid) showing nodes and edges.
2. **Nodes** - the node contracts table.
3. **Edges and routing** - the concrete routing rules.
4. **Shared state** - the schema: field, owner, readers, durability.
5. **Failure and recovery** - per-node fallback behavior, cycle budgets, checkpoint behavior.
6. **Examples** - one or two worked traces through the graph: a normal path, and a branch or failure path.

## Phase 5: Test it

1. **The straight-line happy path.** Confirms the base topology actually connects end to end.
2. **A branch condition right at its threshold, on both sides.** Confirms routing rules are precise, not approximate.
3. **A parallel fan-out where one branch fails and others succeed.** Confirms the fan-in has a defined partial-result policy instead of hanging.
4. **A cycle-back that should eventually succeed.** Confirms it exits on success before exhausting its budget.
5. **A cycle-back that never succeeds.** Confirms the cycle's own budget stops it - not the graph's outer timeout catching it later than it should have.
6. **A crash or pause mid-graph.** Confirms resume-from-checkpoint doesn't repeat side effects that already completed.
7. **A node timeout.** Confirms control actually moves to the defined fallback instead of the graph hanging silently.

## Phase 6: Package

Deliver a self-contained graph folder:

```text
graph-name/
├── GRAPH.md
├── references/   (if any - project-specific detail beyond this base file)
└── templates/     (if any)
```

For a multi-agent system, also keep the individual `agents/<name>/AGENT.md` files this graph connects, and a `CATALOG.md` if the system is large enough that a flat list of nodes stops being easy to scan.

## Graphs as agent teams

This is the file `agent/references/anatomy.md` points to for the "agent team" layout, alongside `CATALOG.md`. When several agents hand off work to each other, each agent's own handoff contract (sender, receiver, payload, timeout, fallback owner) and this graph's edge contract describe most of the same thing from two different vantage points - keep the payload and fallback-owner fields consistent between them rather than defining them twice. They're not fully identical, though: an agent's handoff timeout is specifically about whether the receiver ever acknowledged the baton, which is an edge-level concern (see "edges and routing rules" above), while a node's own failure behavior is about that node's execution going wrong once it's running. Don't collapse the two into one field just because they're both called "timeout."

The nodes in this kind of graph are the agents, workflows, and human gates that actually hand work to each other - not every skill an agent uses along the way. A skill an agent invokes as part of doing its own job stays inside that agent's node; it doesn't become a separate node in the team's graph unless something outside that agent also needs to call it directly.

## Resources in this graph

- `references/anatomy.md` - the full node and edge taxonomy, topology diagrams, and common failure patterns per shape.
- `references/state-and-routing.md` - designing the shared state schema and writing routing rules, with good and bad worked examples.
- `references/portability.md` - how the graph concept maps onto different runtimes, including platforms that can't natively cycle.
- `templates/GRAPH.template.md` - a starter GRAPH.md with the structure filled in as prompts.
- `scripts/validate_graph.py` - checks a JSON graph spec for orphan nodes, unreachable nodes, and cycles with no iteration budget. Run it once the node and edge list is drafted, before writing the full prose contract.

Now go build the smallest topology that produces the outcome, and complicate it only where the interview actually found a real branch, a real parallel need, or a real retry.
