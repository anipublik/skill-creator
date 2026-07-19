# everythingAI

A running collection of portable AI builders. Each one is a self-contained playbook you hand to any capable AI to help you build a specific kind of thing well, instead of re-explaining the same design discipline from scratch every time.

This isn't a tightly matched set of pairs. It's a dumping ground with a standard, not a framework with a fixed shape. New builders get added as they're needed. The only rule is every builder follows the same internal pattern, described below, so the collection stays usable instead of turning into ten one-off folders that don't share a grammar.

See `CATALOG.md` for the current index.

## What's in a builder

Every folder in this repo is a builder: a meta-playbook whose job is to help you produce another artifact - a skill, an agent, a loop, a graph, whatever comes next. At minimum, a builder has one file (`SKILL.md`, `AGENT.md`, `LOOP.md`, `GRAPH.md` - named for what it produces) with a metadata block and a phased playbook. Most also have:

- `references/` - deep detail, loaded only when the playbook points to it.
- `templates/` - starter files to copy instead of writing from a blank page.
- `scripts/` - deterministic checks or scaffolding, run rather than reasoned through by hand each time.

Load the main file into your AI tool of choice, or hand it the whole folder, and describe what you're trying to build.

## What's here now

- **`skill/`** - turns a rough idea, workflow, or SOP into a reusable `SKILL.md`: know-how an AI can follow the same way every time. Answers *how should this task be done*.
- **`agent/`** - turns a role or a set of responsibilities into an `AGENT.md`: something that owns a goal over time, makes decisions, uses tools within limits, and knows when to stop or hand off. Answers *who owns this outcome and what may it do*.
- **`loop/`** - hardens the internal iteration of a single unit of work into a `LOOP.md`: an archetype, a round, and exit conditions that are wired, not just named. Answers *how does one node converge through repeated action*.
- **`graph/`** - wires multiple nodes - agents, loops, skills, tools - into a `GRAPH.md`: explicit routing, parallel branches, shared state, and cycle budgets. Answers *how do several nodes cooperate to produce an outcome none of them owns alone*.

Skill and agent are about content: what kind of thing you're building and who's responsible for it. Loop and graph are about execution: how it actually runs once you press go, inside one node and across many. They're not the same axis, and this repo doesn't pretend they are - it just puts all four in one place because you need all four eventually.

## How they connect

- An agent's operating loop is a loop. Once an agent's actions carry real cost or can't be undone, write that loop as a proper `LOOP.md` instead of leaving it as a vague list of steps.
- An agent team is a graph. The handoffs each `AGENT.md` already defines and a `GRAPH.md`'s edges are the same contract seen from two angles - keep them in sync rather than defining the same thing twice.
- A loop is often one node inside a graph, wired back to itself. A retry or replan that spans more than one node is a graph cycle, not a loop, and needs a budget of its own.
- A skill can be the thing a graph's skill node runs, or the thing a loop's round invokes on each pass.

None of these replace the others. Use the smallest one that actually fits before reaching for the next.

## Portability

Every builder here targets capabilities, not one vendor's tool names or file formats. `SKILL.md`, `AGENT.md`, `LOOP.md`, and `GRAPH.md` are portable source documents. If your target platform wants a different filename, schema, or config format, render a thin adapter for it during packaging and keep the portable file as the source of truth. Don't drop a safeguard - a budget, a boundary, an approval gate - just because the target platform makes it inconvenient to express. Reduce scope or flag the gap instead.

## Adding a new builder

1. Name it for what it produces, lowercase, one word if possible.
2. Write the main file with the same shape the existing builders use: metadata block, phases, a packaging section, a resources list at the end.
3. Only add `references/`, `templates/`, or `scripts/` if there's real reusable detail. Don't manufacture structure a single-file builder doesn't need.
4. Add it to `CATALOG.md`.
5. If it relates to an existing builder (composes with it, replaces part of it, sits above or below it), say so explicitly in both files. That's how this stays a system instead of a pile.

## License

Provided as-is. Adapt freely.
