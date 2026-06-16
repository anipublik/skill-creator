---
name: your-agent-name
description: [What outcome this agent owns.] Use when [events, requests, or situations that should select it]. [State the most important scope or authority boundary.]
---

# Your agent name

## Mission

[One measurable outcome this agent owns.]

## Responsibilities

- [What it must notice.]
- [What it must decide.]
- [What it may do.]
- [What it must verify and report.]

## Inputs and triggers

| Input or trigger | Required | Source | What to verify |
|---|---|---|---|
| [Input] | [Yes/No] | [User, event, system, agent] | [Validation] |

## Skills and workflows

| Capability | Use when | Do not use when |
|---|---|---|
| `skills/example/SKILL.md` | [Selection rule] | [Boundary] |
| `workflows/example/WORKFLOW.md` | [Selection rule] | [Boundary] |

[Delete this section if the agent has no bundled capabilities.]

## Tools and permissions

| Tool | Purpose | Permissions | Approval | Success check | Failure behavior |
|---|---|---|---|---|---|
| [Tool] | [Why it is needed] | [Read/write scope] | [When and from whom] | [How to verify] | [Fallback or escalation] |

[Delete this section if the agent does not use tools.]

## Operating loop

1. Observe the trigger and gather required context.
2. Confirm the goal, current state, and applicable boundaries.
3. Choose the matching skill or workflow.
4. Plan the next safe action.
5. Get approval when required.
6. Act with the narrowest suitable permission.
7. Verify the result.
8. Record relevant state and evidence.
9. Continue, hand off, escalate, or stop.
10. Report the outcome and next owner.

[Adapt this loop to the role.]

## Decision rules

- If [condition], then [action], because [reason].
- If [ambiguous condition], ask [person or role] for [specific information].
- If [threshold], hand off or escalate to [owner] with [payload].

## Boundaries and approvals

- Never [prohibited action].
- Require approval from [role] before [high-impact action].
- Stop when [stop condition].
- Refuse or redirect requests involving [out-of-scope area].

## State and memory

| State | Lifetime | Source of truth | Update rule | Sensitivity |
|---|---|---|---|---|
| [Field] | [Run/durable/evidence] | [System or file] | [Who and when] | [Classification] |

[Delete this section if no state persists between runs.]

## Handoffs and escalation

| Condition | Receiver | Payload | Acceptance | Timeout | Fallback owner |
|---|---|---|---|---|---|
| [Condition] | [Person or agent] | [Required context and evidence] | [How receipt is confirmed] | [Duration] | [Owner] |

## Output and reporting

[Show the exact result shape, including status, actions taken, evidence, unresolved risks, and next owner.]

## Failure recovery

- If a tool fails, [retry or fallback policy].
- If data conflicts, [source precedence or escalation].
- If verification fails, [rollback, stop, or handoff].
- Never claim success without [required evidence].

## Examples

### Normal case

**Trigger:** [Realistic request or event]

**Expected behavior:** [Decisions, capabilities, actions, verification, and report]

### Boundary case

**Trigger:** [Request that crosses a limit]

**Expected behavior:** [Approval, refusal, escalation, or handoff]

## Test scenarios

- [Happy path]
- [Missing information]
- [Tool failure]
- [Below an approval threshold]
- [Above an approval threshold]
- [Out-of-scope request]
- [Boundary bypass attempt]
