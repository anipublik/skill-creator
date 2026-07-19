# Catalog

Index of every builder in this repo. Update this whenever a builder is added, renamed, or its relationship to another builder changes. Read it before starting a new builder so you catch overlap before you build it instead of after.

| Builder | Produces | Answers | Path |
|---|---|---|---|
| skill-forge | `SKILL.md` | How should this task be done? | `skill/` |
| agent-forge | `AGENT.md` | Who owns this outcome and what may it do? | `agent/` |
| loop-forge | `LOOP.md` | How does one node converge through repeated action? | `loop/` |
| graph-forge | `GRAPH.md` | How do several nodes cooperate to produce an outcome none of them owns alone? | `graph/` |

## Composition notes

- `agent/`'s operating loop should be written as a `loop/` when actions carry real cost or can't be undone.
- `agent/`'s "agent team" layout is a `graph/` - the same handoff contract, described twice, should stay in sync.
- `loop/` nodes and `graph/` cycle-back edges share the same wired-exit and budget discipline; don't relax it just because it moved from a node's internals to an edge.
- `skill/` is the thing a `graph/` skill node runs, or the thing a `loop/` round invokes each pass.
