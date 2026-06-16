# Skill Forge

A meta-skill for building portable AI skills. Give it a rough idea or a workflow you keep re-explaining, and it produces a self-contained folder of instructions and resources that any capable AI can load and follow to do a task well, consistently, every time.

Skill Forge is itself a skill — it's the thing it teaches you to build.

## What a skill is

A **skill** is a folder with at least one file, `SKILL.md`, containing a small metadata block (name + description) and a playbook written for an AI to execute. Optionally, it includes supporting files split into three buckets:

| Bucket | Purpose | When the AI uses it |
|---|---|---|
| `references/` | Knowledge the AI reads on demand — deep detail, edge cases, lookup tables, per-variant specs | Only when the workflow routes to it |
| `scripts/` | Deterministic code the AI runs — parsers, validators, converters, generators | When the workflow calls it |
| `assets/` | Raw material for the output — templates, boilerplate, config stubs, media | When the output is built from it |

The organizing principle is **progressive disclosure**: load information in layers, cheapest first, and only pull in the expensive stuff when the task actually needs it.

- **Layer 1 — the description** (metadata block): always loaded. Its only job is to make the AI recognize "this task is one I should use this skill for."
- **Layer 2 — the `SKILL.md` body**: loaded when the skill triggers. The main playbook: workflow, rules, decision logic, small examples. Aim for under ~500 lines.
- **Layer 3 — bundled resources**: loaded or executed only when the workflow reaches for them. Unlimited detail, zero cost until needed.

## Repository structure

```
skill-forge/
├── SKILL.md                          # The skill itself: the 7-phase build process
├── references/
│   ├── anatomy.md                    # File layouts, the multi-variant pattern, how layers load
│   ├── descriptions.md               # Writing the description field so the skill triggers correctly
│   └── portability.md                # Keeping a skill vendor-agnostic and degrading gracefully
├── templates/
│   ├── SKILL.template.md             # Starter SKILL.md with structure as prompts
│   ├── reference.template.md         # Starter reference file with a table-of-contents stub
│   └── script.template.py            # Starter script with a documented input/output contract
└── README.md                         # This file
```

## The build process

`SKILL.md` walks through seven phases in order:

1. **Interview** — Understand the task before writing anything. What should the skill do, when should it trigger, what does good output look like, what are the steps, what varies, what resources exist, what tools are needed.
2. **Choose the shape** — Decide the file layout: single file, body + references, body + scripts, body + assets, or the works. Start smaller than you think.
3. **Write the `SKILL.md`** — Metadata block first (name + description), then the body. Explain the *why*, write in the imperative, show don't just tell, generalize past your examples, stay lean, point clearly to resources.
4. **Write the bundled files** — Only the files the chosen shape calls for. References, scripts, and assets each have their own guidelines.
5. **Test it, at least by hand** — Invent realistic prompts, follow the skill fresh as written, probe whether the description triggers correctly and whether the skill generalizes.
6. **Iterate** — Generalize from feedback, cut before you add, watch for repeated work that should become a script, re-read with fresh eyes.
7. **Package and hand off** — Deliver the skill folder, zipped or printed file-by-file with paths.

## Key principles

- **The description is the highest-leverage sentence in the whole skill.** It alone determines whether the skill ever gets used. Pack it with concrete trigger cues — the situations and phrasings (including casual, keyword-free ones) that mean "use this now." See `references/descriptions.md`.
- **Explain the why, not just the what.** An instruction with a reason generalizes; a bare ALL-CAPS rule breaks the moment reality differs.
- **Start smaller than you think.** It's easier to split a file later than to explain why a simple skill became a directory tree.
- **Write against capabilities, not vendors.** "Read the uploaded file" is portable. "Use the `view` tool on `/mnt/user-data/uploads/`" is not. See `references/portability.md`.
- **Degrade gracefully.** Describe the ideal path, then the fallback. If your skill can be pasted into a plain chat with no tools and still produce a good result, it's genuinely portable.

## How to use Skill Forge

Load `SKILL.md` into your AI and ask it to build a skill. You can say things like:

- "Turn this workflow into a reusable skill"
- "Package this process so the AI does it consistently"
- "Build me a reusable prompt for X"
- "I keep re-explaining this to ChatGPT — make it a skill"

The AI will interview you, choose a shape, write the files, test them, iterate, and hand off a packaged skill folder.

## Templates

The `templates/` folder contains starters you can copy and adapt:

- **`SKILL.template.md`** — a skeleton `SKILL.md` with the standard sections (when-to-use, workflow, output format, examples, resources) filled in as prompts.
- **`reference.template.md`** — a skeleton reference file with a table-of-contents stub.
- **`script.template.py`** — a skeleton Python script with a documented input/output contract and a fallback note for AIs that can't run code.

## License

This repository is provided as-is for building and sharing AI skills. Adapt freely.
