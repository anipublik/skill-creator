---
name: agent-forge
description: Design and package a focused AI agent from a role, goal, workflow, or set of responsibilities. Use when someone wants a specialized agent, assistant, operator, copilot, reviewer, coordinator, or autonomous worker with defined tools, skills, boundaries, handoffs, and outputs. Trigger for requests like "build an agent for this," "make a support bot," "create an agent that handles releases," "turn this role into an AI worker," or "set up a team of agents." Produces a portable AGENT.md with optional skills, workflows, references, scripts, and assets.
---

# Agent forge

Build a focused agent that can own a goal, choose the right action, use tools safely, and know when to stop or ask for help. An agent should have a job, authority, and boundaries. It should not be a personality wrapped around a vague prompt.

Read this whole file before creating anything. Work through the phases in order. Do not start by writing a role prompt. First learn what the agent is responsible for and what it is allowed to do.

## Skill, workflow, and agent

These are related, but they solve different problems:

- A **skill** is reusable know-how for a type of task. It explains how to do something well when invoked.
- A **workflow** is an ordered process. It defines stages, decisions, approvals, inputs, and outputs.
- An **agent** owns a goal over time. It decides which skills and workflows to use, operates tools within explicit limits, keeps relevant state, and hands work off when it reaches a boundary.

Use a skill when the user needs repeatable expertise. Use a workflow when the order and checkpoints matter. Use an agent when something must observe, decide, act, and remain responsible for an outcome across multiple steps.

Do not turn every prompt into an agent. If the task is one-shot and has no decisions, tools, state, or ongoing responsibility, a skill is probably enough.

## What an agent contains

At minimum, an agent has an `AGENT.md` with a metadata block and an operating contract. It may also use:

- `skills/` for reusable capabilities the agent can invoke.
- `workflows/` for ordered processes the agent runs.
- `references/` for policies, domain knowledge, schemas, and detailed rules it reads when needed.
- `scripts/` for deterministic operations it runs.
- `assets/` for templates and files used in outputs.

Keep the agent body focused on decisions and responsibility. Put task-specific instructions in skills, fixed sequences in workflows, deep knowledge in references, and exact repeated operations in scripts.

## Phase 1: Interview

Understand the job before designing the agent. Mine existing requirements, SOPs, role descriptions, examples, and earlier conversation before asking questions. Fill the remaining gaps:

1. **What outcome does the agent own?** State it in one sentence. If the sentence contains unrelated outcomes, split the agent.
2. **Who uses it and who receives its work?** Identify the user, stakeholders, and any downstream agents or people.
3. **What starts its work?** A direct request, an event, a schedule, a queue item, a changed file, or another agent's handoff.
4. **What inputs does it receive?** Include required fields, files, context, and what may be missing.
5. **What decisions must it make?** Capture decision criteria, ambiguity, and situations that require judgment.
6. **What actions may it take?** List tools, APIs, files, systems, and communication channels.
7. **How much autonomy does it have?** Decide whether it advises, drafts, acts after approval, or acts independently within limits.
8. **What must it never do?** Record privacy, security, financial, legal, brand, and operational boundaries.
9. **When must it ask, escalate, or hand off?** Define concrete thresholds and the recipient of each handoff.
10. **What state must persist?** Separate durable facts from temporary run context. Do not collect state without a reason.
11. **What does a good result look like?** Get examples, acceptance criteria, service levels, and a bad result if possible.
12. **Where will it run?** Note the target platform and available capabilities without making the core design vendor-specific.

Push on failure cases now. Ask what happens when a tool is unavailable, data conflicts, an approval is delayed, or the agent cannot meet its goal.

## Phase 2: Choose the architecture

Pick the smallest shape that can own the outcome:

- **Single agent.** One `AGENT.md`, no bundled capabilities. Use for a narrow role with a short operating contract.
- **Agent plus skills.** Use when the agent performs several reusable kinds of work. Each skill should remain independently useful.
- **Agent plus workflows.** Use when work has fixed stages, approvals, or handoffs that should not depend on improvisation.
- **Agent plus tools.** Use when the agent acts on external systems. Define each tool's purpose, required inputs, expected output, permissions, and failure behavior.
- **Agent team.** Use only when roles need genuinely different context, permissions, or evaluation criteria. Multiple names are not a reason for multiple agents.

For complex agents, read `references/anatomy.md` before choosing the layout.

## Phase 3: Design the operating model

Write the design before the prose. Capture these elements:

### Mission

One measurable outcome the agent owns. Prefer "keep production releases safe and traceable" over "help with releases."

### Responsibilities

List what the agent is expected to notice, decide, do, verify, and report. Each responsibility should support the mission.

### Autonomy level

Choose the default level and define exceptions:

1. **Advise:** analyze and recommend, but take no action.
2. **Draft:** prepare changes or messages for approval.
3. **Act with approval:** execute only after a named approval point.
4. **Act within bounds:** execute independently while every stated limit is satisfied.

Do not use "fully autonomous" as a substitute for boundaries. Independent action still needs limits, auditability, and a stop condition.

### Capability map

Map responsibilities to skills and workflows. Reuse an existing capability when possible instead of copying its instructions into the agent.

```text
release-manager
├── skill: release-notes
├── skill: risk-review
├── workflow: production-release
└── workflow: rollback
```

### Tool contracts

For every tool, define:

- What the agent uses it for.
- Inputs it must verify before calling it.
- Read and write permissions.
- Whether approval is required.
- What success and failure look like.
- What to do when the result is partial or ambiguous.

Least privilege is the default. Do not give write access when read access can complete the job.

### Boundaries and escalation

Write boundaries as decision rules, not slogans. "Escalate refunds over $500 to the support manager" is actionable. "Be careful with large refunds" is not.

### State

Define what the agent needs during a run, what persists between runs, who can update it, and when it expires. Never treat conversation history as a reliable database.

## Phase 4: Write the AGENT.md

Start with metadata:

```yaml
---
name: release-manager
description: Coordinate safe software releases from readiness review through deployment and verification. Use when a release needs planning, approvals, execution, rollback decisions, or status communication. Operates deployment and monitoring tools only within the stated release policy and escalates blocked approvals, failed health checks, and high-risk changes.
---
```

Use a short lowercase hyphenated name. Keep the description concrete: what outcome the agent owns, when it should be selected, and its most important boundary.

A useful body usually contains:

1. **Mission**
2. **Responsibilities**
3. **Inputs and triggers**
4. **Skills and workflows**
5. **Tools and permissions**
6. **Operating loop**
7. **Decision rules**
8. **Boundaries and approvals**
9. **State and memory**
10. **Handoffs and escalation**
11. **Output and reporting**
12. **Failure recovery**
13. **Examples**

Write in the imperative. Explain the reason behind important constraints so the agent can generalize. Keep identity and tone brief unless they materially affect the work.

### The operating loop

Give the agent a clear loop it can repeat:

1. Observe the trigger and gather required context.
2. Confirm the goal, current state, and applicable boundaries.
3. Choose the matching skill or workflow.
4. Plan the next safe action.
5. Get approval if the action crosses an approval boundary.
6. Act using the narrowest suitable tool permission.
7. Verify the result instead of trusting the tool call alone.
8. Record relevant state and evidence.
9. Continue, hand off, escalate, or stop according to the decision rules.
10. Report the outcome, remaining risks, and next owner.

Adapt this loop to the role. Do not force it onto a simple advisory agent that never acts.

This ten-step list is a starting shape, not a substitute for real exit-condition design. Once the agent's actions carry real cost or can't be undone, harden this into a proper `loop/LOOP.md` in this repository: pick an archetype, and replace "continue, hand off, escalate, or stop according to the decision rules" with exit conditions that are wired, not just named.

## Phase 5: Add supporting files

Create only what the design requires:

- Put reusable task expertise in `skills/<skill-name>/SKILL.md`.
- Put fixed processes in `workflows/<workflow-name>/WORKFLOW.md` and include a machine-readable definition when a runtime needs one.
- Put policies, schemas, and detailed domain knowledge in `references/`.
- Put repeatable deterministic operations in `scripts/`.
- Put output templates and starter files in `assets/`.

The `AGENT.md` must say exactly when to load or run each resource. A resource the agent is never told to use is dead weight.

## Phase 6: Test the agent

Do not test only the happy path. Run scenarios that probe judgment and restraint:

1. A normal request with complete inputs.
2. A request with missing or conflicting information.
3. A tool failure or partial result.
4. An action just below an approval threshold.
5. An action just above the threshold.
6. A request outside the agent's scope.
7. An attempt to bypass a boundary.
8. A handoff where the receiving person or agent is unavailable.
9. A repeated run that tests whether state is handled correctly.

For each scenario, check:

- Did it select the right skill or workflow?
- Did it use only allowed tools and permissions?
- Did it ask for approval at the right point?
- Did it verify the action?
- Did it preserve only useful state?
- Did it stop or escalate instead of guessing?
- Did it produce the expected report and evidence?

Fix the operating contract when behavior is wrong. Do not patch every failed scenario with a special case.

## Phase 7: Package and hand off

Deliver a self-contained agent folder:

```text
agent-name/
├── AGENT.md
├── skills/       (if any)
├── workflows/    (if any)
├── references/   (if any)
├── scripts/      (if any)
└── assets/       (if any)
```

Include setup requirements, credentials the user must provide, target-platform installation steps, and a short list of tested scenarios. Never include secrets in the package.

If the target platform uses a different filename or configuration format, render the portable design into that format during packaging. Keep `AGENT.md` as the readable source of truth unless the user explicitly chooses a platform-specific package only.

## Building agent systems at scale

When creating several agents, design the system before writing each agent:

- List every proposed agent with its mission, inputs, outputs, tools, and boundaries in one table.
- Merge agents whose missions and permissions substantially overlap.
- Separate agents when they require different authority, context, security boundaries, or evaluation criteria.
- Build shared skills once and reference them instead of copying instructions.
- Give every handoff a sender, receiver, payload, success condition, timeout, and fallback owner.
- Prevent delegation loops by recording who currently owns the goal and limiting how work may be delegated.
- Keep a catalog of agents, skills, workflows, and their dependencies.
- Test the system end to end, including failed and delayed handoffs.

A multi-agent system should make responsibility clearer. If adding agents makes ownership harder to explain, simplify it.

## Safety and honesty

Do not create agents whose purpose or authority is hidden from the people affected by them. Do not grant tools or permissions beyond what the mission requires. Do not disguise irreversible actions as recommendations, fabricate tool results, or claim an action succeeded without verification.

For high-impact domains, keep a person in the approval path unless the user has supplied clear policy, authority, safeguards, and audit requirements that support bounded independent action.

## Resources in this agent

- `references/anatomy.md` explains agent layouts, capability composition, tool contracts, state, handoffs, and portability. Read it for complex or multi-agent designs.
- `templates/AGENT.template.md` is a starter operating contract. Copy it and remove sections that do not apply.

Now build the smallest agent that can safely own the outcome.
