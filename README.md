# Skill and Agent Forge

This repository contains two portable builders:

- `skill/` helps you turn knowledge, workflows, and repeated tasks into reusable AI skills.
- `agent/` helps you turn a role, goal, or set of responsibilities into a focused AI agent with clear tools, permissions, boundaries, and handoffs.

Use either folder on its own, or use both to build an agent that is composed from reusable skills.

## Skill or agent?

A skill and an agent are not interchangeable.

| | Skill | Agent |
|---|---|---|
| Main question | How should this task be done? | Who owns this outcome and what may it do? |
| Purpose | Reusable expertise for a type of task | Ongoing responsibility for a goal |
| Behavior | Runs when invoked | Observes, decides, acts, verifies, and stops or escalates |
| Usually contains | Instructions, references, scripts, assets | Mission, responsibilities, skills, workflows, tools, state, boundaries, handoffs |
| Best for | Reviewing code, parsing invoices, writing reports | Managing releases, handling support cases, coordinating an operational process |

Choose a **skill** when you need repeatable know-how. Choose an **agent** when something must own an outcome across multiple steps, select capabilities, operate tools, and work within explicit authority.

Do not create an agent for every prompt. If the work is one-shot and needs no tools, state, approvals, or ongoing decisions, a skill is simpler and easier to reuse.

### How they work together

Agents should compose skills instead of copying their instructions. For example:

```text
release-manager agent
├── release-notes skill
├── risk-review skill
├── production-release workflow
└── rollback workflow
```

The agent owns the release outcome. Skills explain how to perform specific tasks. Workflows preserve required order, checks, and approvals.

## Repository structure

```text
skill-forge/
├── skill/
│   ├── SKILL.md                       # Playbook for designing one skill or a skill library
│   ├── references/
│   │   ├── anatomy.md                 # Skill layouts and progressive disclosure
│   │   ├── descriptions.md            # Trigger descriptions and collision testing
│   │   └── portability.md             # Cross-platform design and fallbacks
│   ├── templates/
│   │   ├── SKILL.template.md
│   │   ├── reference.template.md
│   │   └── script.template.py
│   └── scripts/
│       ├── scaffold_skills.py         # Batch skill scaffolder
│       └── example_specs.json         # Example input for the scaffolder
├── agent/
│   ├── AGENT.md                       # Playbook for designing one agent or an agent system
│   ├── references/
│   │   └── anatomy.md                 # Tools, state, handoffs, composition, and portability
│   └── templates/
│       └── AGENT.template.md          # Starter agent operating contract
└── README.md
```

## Use the skill creator

Load `skill/SKILL.md` into your AI tool or upload the entire `skill/` folder. If a registry expects `SKILL.md` at the package root, upload the `skill/` folder itself rather than the whole repository.

Use requests such as:

- "Turn this workflow into a reusable skill."
- "Package this process so an AI follows it consistently."
- "Build a skill for each of these SOPs."
- "Create a shared skill library for the team."

The creator interviews you, chooses the smallest useful layout, writes the files, tests realistic prompts, and packages the result. It also handles batches, naming consistency, and trigger collisions across a skill library.

## Use the agent creator

Load `agent/AGENT.md` into your AI tool or provide the entire `agent/` folder. Then describe the role or outcome you want the agent to own.

Use requests such as:

- "Build a release manager agent."
- "Turn this support role into an AI agent."
- "Create an agent that reviews invoices and escalates exceptions."
- "Design a team of agents for this operational process."

The creator defines the agent's mission, autonomy, tools, permissions, skills, workflows, state, approval gates, failure recovery, and handoffs. It tests normal cases as well as missing data, tool failures, boundary violations, and escalation paths.

`AGENT.md` is this repository's portable source format. Agent platforms do not all use the same filename or schema, so the final package may need a thin adapter for the target platform.

## Templates and batch scaffolding

Copy `skill/templates/SKILL.template.md` when you already understand the skill and only need the file structure. Copy `agent/templates/AGENT.template.md` when you already understand the role and need a structured operating contract.

To scaffold several skills from JSON:

```bash
python3 skill/scripts/scaffold_skills.py skill/scripts/example_specs.json --out ./generated-skills
```

The script creates starter folders. It does not replace the interview, writing, collision review, or testing in `skill/SKILL.md`.

## Portability

The files use capabilities and plain-language contracts instead of depending on one vendor's tool names. When a target platform has its own format, keep the portable source and render an adapter for that platform. If the platform lacks required permissions, approvals, state, or handoff controls, reduce the agent's autonomy rather than silently dropping a safeguard.

## License

Provided as-is. Adapt freely.
