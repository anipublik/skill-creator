---
name: [short, lowercase, hyphenated]
description: [What this loop converges on, and when to reach for it. One to three sentences.]
---

# [Loop name]

[One or two sentences: what this loop converges on, and why it needs to iterate rather than run once.]

## Archetype

[Which shape from LOOP.md Phase 2 - fixed-step, converge-on-metric, tool loop, plan-execute-replan, human-gated, or watchdog/reconciliation - and one sentence on why it fits this convergence.]

## Round

[What exactly happens once per iteration. Be specific about the observe step, the decide step, and the act step, in that order.]

1. Observe: [what state or result gets read at the start of the round]
2. Decide: [what determines the next action]
3. Act: [what actually happens]
4. Check: [what gets evaluated against the exit conditions before the round is considered closed]

## Exit conditions

- **Success:** [the exact, concrete check]
- **Budget:** [iteration cap / cost cap / wall-clock cap / action-count cap - name at least one, independent of the success check]
- **Stagnation:** [how repeated or non-progressing rounds are detected, and after how many - or "not applicable, fixed-step archetype" if repeating the same action every round is intentional]
- **Escalation:** [the specific threshold that hands off to a human or another process, and who receives it]

Confirm each of the above is wired, not named - point at where in the implementation it actually gets checked.

## State carried between rounds

| Field | Updated by | Read by | Notes |
|---|---|---|---|
| [state field] | [which step in the round] | [which step reads it to decide the next action] | [durable or single-run only] |

## Examples

[One or two short worked rounds: state going in, action taken, state coming out, and whether an exit condition fired.]
