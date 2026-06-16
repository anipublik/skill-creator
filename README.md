# Skill Forge

Skill Forge helps you build portable AI skills, one at a time or in a batch. Give it a rough idea or a workflow you keep re-explaining, and it gives you back a folder of instructions and resources that any capable AI can load and follow to do a task well, consistently, every time. Give it a whole stack of workflows, and it builds a coherent library instead of a pile of one-offs.

It's a skill for making skills.

## What a skill is

A skill is a folder with at least one file, `SKILL.md`. That file has a small metadata block (name and description) followed by a playbook written for an AI to execute. It can also include supporting files in three folders:

| Folder | What's in it | When the AI uses it |
|---|---|---|
| `references/` | Deep detail, edge cases, lookup tables, per-variant specs | Only when the workflow routes to it |
| `scripts/` | Deterministic code: parsers, validators, converters, generators | When the workflow calls it |
| `assets/` | Templates, boilerplate, config stubs, media | When the output is built from it |

The core idea is **progressive disclosure**. Load information in layers, cheapest first, and only pull in the heavy stuff when the task actually needs it.

- **Layer 1, the description** (metadata block): always loaded. Its only job is to make the AI recognize that this task is one it should use this skill for.
- **Layer 2, the `SKILL.md` body**: loaded when the skill triggers. The main playbook with the workflow, rules, decision logic, and small examples. Try to keep it under ~500 lines.
- **Layer 3, bundled resources**: loaded or run only when the workflow reaches for them. Unlimited detail, zero cost until needed.

## Repository structure

```
skill-forge/
├── SKILL.md                          # The skill itself: the 7-phase build process, plus batch guidance
├── references/
│   ├── anatomy.md                    # File layouts, the multi-variant pattern, how layers load
│   ├── descriptions.md               # Writing the description field so the skill triggers correctly
│   └── portability.md                # Keeping a skill vendor-agnostic and degrading gracefully
├── templates/
│   ├── SKILL.template.md             # Starter SKILL.md with structure as prompts
│   ├── reference.template.md         # Starter reference file with a table-of-contents stub
│   └── script.template.py            # Starter script with a documented input/output contract
├── scripts/
│   ├── scaffold_skills.py            # Generates starter folders for a batch of skills from a JSON spec list
│   └── example_specs.json            # Sample specs file showing the expected JSON format
└── README.md                         # This file
```

## The build process

`SKILL.md` walks through seven phases in order:

1. **Interview.** Understand the task before writing anything. What should the skill do, when should it trigger, what does good output look like, what are the steps, what varies, what resources exist, what tools are needed.
2. **Choose the shape.** Decide the file layout: single file, body + references, body + scripts, body + assets, or the works. Start smaller than you think.
3. **Write the `SKILL.md`.** Metadata block first (name and description), then the body. Explain the *why*, write in the imperative, show don't just tell, generalize past your examples, stay lean, point clearly to resources.
4. **Write the bundled files.** Only the files the chosen shape calls for. References, scripts, and assets each have their own guidelines.
5. **Test it, at least by hand.** Invent realistic prompts, follow the skill fresh as written, probe whether the description triggers correctly and whether the skill generalizes.
6. **Iterate.** Generalize from feedback, cut before you add, watch for repeated work that should become a script, re-read with fresh eyes.
7. **Package and hand off.** Deliver the skill folder, zipped or printed file-by-file with paths.

## Building at scale

Skill Forge isn't limited to one skill per run. For a batch of workflows, SOPs, or a whole team's processes, it interviews across the set instead of one at a time, checks the draft descriptions against each other so two skills don't end up fighting over the same trigger phrases, keeps naming and structure consistent, and can scaffold all the folders at once with `scripts/scaffold_skills.py`. See "Building many skills at once" in `SKILL.md` for the full approach.

## Key principles

- **The description is the most important sentence in the whole skill.** It alone determines whether the skill ever gets used. Pack it with concrete trigger cues: the situations and phrasings (including casual, keyword-free ones) that mean "use this now." See `references/descriptions.md`.
- **Explain the why, not just the what.** An instruction with a reason generalizes. A bare ALL-CAPS rule breaks the moment reality differs.
- **Start smaller than you think.** It's easier to split a file later than to explain why a simple skill became a directory tree.
- **Write against capabilities, not vendors.** "Read the uploaded file" is portable. "Use the `view` tool on `/mnt/user-data/uploads/`" is not. See `references/portability.md`.
- **Degrade gracefully.** Describe the ideal path, then the fallback. If your skill can be pasted into a plain chat with no tools and still produce a good result, it's genuinely portable.

## How to use Skill Forge

Load `SKILL.md` into your AI and ask it to build a skill. You can say things like:

- "Turn this workflow into a reusable skill"
- "Package this process so the AI does it consistently"
- "Build me a reusable prompt for X"
- "I keep re-explaining this to ChatGPT, make it a skill"
- "Turn our SOPs into a skill library"
- "Build a skill for each of these workflows"

The AI will interview you, choose a shape, write the files, test them, iterate, and hand off a packaged skill folder (or a whole set of them).

## Templates

The `templates/` folder has starters you can copy and adapt:

- **`SKILL.template.md`**: a skeleton `SKILL.md` with the standard sections (when-to-use, workflow, output format, examples, resources) filled in as prompts.
- **`reference.template.md`**: a skeleton reference file with a table-of-contents stub.
- **`script.template.py`**: a skeleton Python script with a documented input/output contract and a fallback note for AIs that can't run code.

## Scripts

- **`scaffold_skills.py`**: takes a JSON file listing skill specs (name, description, references, scripts, assets) and generates the folder structure and starter files for all of them at once. Run it once the specs for a batch are settled:

  ```
  python3 scripts/scaffold_skills.py specs.json --out ./skills
  ```

- **`example_specs.json`**: a sample specs file with three example skills of varying shapes (single file, body + assets, body + references + scripts). Copy it, edit the specs to match your batch, and run the scaffolder.

## License

Provided as-is. Adapt freely.
