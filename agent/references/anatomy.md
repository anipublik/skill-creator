# Agent anatomy

Read this when an agent needs tools, reusable skills, workflows, durable state, handoffs, or multiple cooperating roles.

## Contents

- The parts of an agent
- Common layouts
- Capability composition
- Tool contracts
- State and memory
- Handoffs
- Multi-agent boundaries
- Portability

## The parts of an agent

An agent combines several kinds of material that should not be collapsed into one prompt:

| Part | Purpose |
|---|---|
| Mission | The outcome the agent owns |
| Responsibilities | What it must notice, decide, do, verify, and report |
| Skills | Reusable know-how it invokes for a type of task |
| Workflows | Ordered processes with stages, decisions, and approvals |
| Tools | External actions it may take under defined permissions |
| References | Policies, schemas, and domain knowledge loaded when needed |
| State | Facts needed during or between runs |
| Boundaries | Conditions that require refusal, approval, escalation, or handoff |
| Reports | Evidence of what happened, what remains, and who owns the next step |

The agent file owns orchestration and judgment. Skills own expertise. Workflows own sequence. Tool contracts own permission and failure behavior.

## Common layouts

### Single agent

```text
agent-name/
└── AGENT.md
```

Use this for a narrow advisory or drafting role with no reusable supporting content.

### Agent with skills

```text
agent-name/
├── AGENT.md
└── skills/
    ├── capability-a/
    │   └── SKILL.md
    └── capability-b/
        └── SKILL.md
```

Use this when the agent performs several distinct kinds of work. The agent selects a capability; each skill explains how to perform it.

### Agent with workflows

```text
agent-name/
├── AGENT.md
└── workflows/
    ├── standard-process/
    │   └── WORKFLOW.md
    └── exception-process/
        └── WORKFLOW.md
```

Use this when order, approvals, or handoffs matter. The agent decides which workflow applies and follows it without silently skipping checkpoints.

### Agent with tools and references

```text
agent-name/
├── AGENT.md
├── references/
│   ├── policy.md
│   └── data-schema.md
└── scripts/
    └── validate_input.py
```

Use references for knowledge and scripts for deterministic operations. External APIs and platform tools usually remain outside the folder, but their contracts belong in `AGENT.md` or a focused reference.

### Agent team

```text
agent-system/
├── CATALOG.md
├── GRAPH.md
├── agents/
│   ├── intake/
│   │   └── AGENT.md
│   └── resolver/
│       └── AGENT.md
├── skills/
└── workflows/
```

Use a team only when roles need meaningfully different context, permissions, or measures of success. Keep shared capabilities at the system level rather than copying them into each agent.

## Capability composition

Map each responsibility to a skill, workflow, tool, or direct operating rule. If a responsibility has no implementation, the agent cannot actually own it. If several capabilities implement the same responsibility, define how the agent chooses among them.

Example:

| Responsibility | Capability | Selection rule |
|---|---|---|
| Assess release risk | `skills/risk-review` | Run for every production release |
| Deploy safely | `workflows/standard-release` | Use when all health checks pass |
| Recover service | `workflows/rollback` | Use after a failed verification gate |
| Notify stakeholders | communication tool | Run after deployment or rollback completes |

Avoid embedding a skill's full instructions inside the agent. That creates two sources of truth and makes updates drift.

## Tool contracts

A tool contract should answer:

| Field | Question |
|---|---|
| Purpose | Why does the agent need this tool? |
| Inputs | What must be present and verified before use? |
| Permissions | What may it read, create, update, or delete? |
| Approval | Which calls require human or policy approval? |
| Success | How does the agent verify the intended effect? |
| Failure | What should happen on timeout, partial output, or error? |
| Evidence | What result, identifier, or log must be recorded? |

Do not define tools as a loose list. A name without a contract tells the agent that a capability exists but not how to use it safely.

## State and memory

Separate three kinds of context:

- **Run context:** temporary inputs, plans, tool results, and decisions for the current job.
- **Durable state:** facts that future runs need, such as an approved preference, ownership record, or unresolved case status.
- **Evidence:** immutable or append-only records needed to explain what happened.

For every durable field, define its source, owner, update rule, expiration, and sensitivity. Do not persist chain-of-thought, unverified guesses, credentials, or data unrelated to the mission.

When a platform lacks persistent memory, tell the agent where state actually lives, such as a ticket, database, repository file, or user-provided record. Conversation history is context, not durable storage.

## Handoffs

Every handoff needs a contract:

- Sender and receiver
- Reason for the handoff
- Required payload
- Current state and actions already attempted
- Evidence and unresolved risks
- Success acknowledgment
- Timeout
- Fallback owner

The sender retains responsibility until the receiver accepts the handoff. This prevents work from disappearing between agents or between an agent and a person.

## Multi-agent boundaries

Define one owner for the overall goal and one owner for each active task. Agents may delegate work, but delegation must not erase ownership.

Prevent common failures:

- **Delegation loops:** Record the delegation chain and limit repeated reassignment.
- **Duplicate action:** Use task identifiers, locks, or status checks before acting.
- **Conflicting authority:** Give each decision one final owner.
- **Context flooding:** Send only the handoff payload, not every agent's full history.
- **Hidden failure:** Require acknowledgment, timeouts, and a fallback owner.

If two agents use the same tools, context, policies, and evaluation criteria, they may be one agent with two workflows.

## Portability

`AGENT.md` is a portable source document, not a universal platform standard. Target systems may require different filenames, YAML fields, system prompts, tool declarations, or directory locations.

Keep the core design portable by describing capabilities rather than vendor tool names. During packaging, create a thin adapter for the target platform that maps:

- Mission to the platform's instruction or system-prompt field
- Skills to its capability-loading mechanism
- Workflows to its orchestration format
- Tools to its tool or function schema
- State to its supported storage mechanism
- Approvals to its human-in-the-loop controls

Do not weaken a boundary because the target platform lacks a matching feature. Use a safer fallback, reduce autonomy, or state that the agent cannot be deployed correctly on that target.
