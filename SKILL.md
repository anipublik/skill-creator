---
name: skill-forge
description: Build a complete, portable AI skill from a rough idea, whether it's one skill or a whole batch of them. Use this whenever someone wants to create a skill, capability pack, custom instruction set, agent playbook, or reusable "how-to" file for an AI to follow, or wants to turn a workflow, process, or repeated task into something an AI can do consistently. Trigger this even when the person does not say the word "skill" - phrases like "make the AI do X every time," "turn this workflow into instructions," "package this process," "I keep re-explaining this to ChatGPT," or "build me a reusable prompt for Y" all mean this skill. Also trigger it for scale asks like "build skills for all of these," "turn our SOPs into a skill library," "set up a suite of skills for the team," or "scaffold a skill for each of these workflows." It produces a folder of files (a SKILL.md plus optional references, scripts, and assets), splitting content across files by how often each part is needed, so the result works in any AI tool, not just one vendor's.
---

# Skill forge

This is a meta-skill. Its job is to help you build another skill: a self-contained bundle of instructions and resources that any capable AI can load and follow to do a task well, over and over, the same way.

Read this whole file before you start building anything. Then work through the phases in order. Do not skip the interview and jump straight to writing files. The single most common failure mode is writing a skill for a task you only half understand, and it shows.

## What a skill actually is

A skill is a folder. At minimum it has one file, `SKILL.md`, which starts with a small block of metadata (name and description) and then contains instructions written for an AI to read and act on. Optionally it has supporting files split into three buckets:

- `references/` - documents the AI reads into context only when it needs them. Deep detail, edge cases, lookup tables, long specs.
- `scripts/` - code the AI runs to do deterministic work reliably instead of doing it by hand each time.
- `assets/` - files the skill uses in its output. Templates, boilerplate, config stubs, letterheads, starter files.

The whole point of splitting things up is a pattern called progressive disclosure, covered below. Get this right and everything else follows.

## The core idea: progressive disclosure

An AI has a limited context window. Every word you put in front of it costs attention and money. So a good skill loads information in layers, cheapest first, and only pulls in the expensive stuff when the task at hand actually needs it.

There are three layers:

1. **The description** (in the metadata block). Always loaded, for every request, whether or not the skill ends up being used. This is roughly one to three sentences. Its only job is to make the AI recognize "this task is one I should use this skill for." Keep it dense with trigger cues.

2. **The SKILL.md body.** Loaded whenever the skill is triggered. This is the main playbook: the workflow, the rules, the decision logic, small examples. Aim to keep it under about 500 lines. If it is getting longer, that is a signal that some of it belongs in a reference file.

3. **Bundled resources** (references, scripts, assets). Loaded or executed only when the workflow explicitly reaches for them. This is where unlimited detail lives, because none of it costs anything until it is needed.

The mental test for where a piece of content goes: **how often is it needed?** Needed every single time to decide whether to even use the skill, put it in the description. Needed every time the skill runs, put it in the body. Needed only in specific branches or for deep detail, put it in a reference. Needed as raw material for the output, put it in assets. Needed as a repeatable computation, put it in a script.

## Phase 1: Interview

Do not write anything yet. First, understand the task. If the person already described a workflow earlier in the conversation ("turn what we just did into a skill"), mine that for answers before asking. Fill gaps by asking. Get answers to these before proceeding:

1. **What should the skill enable the AI to do?** In one plain sentence. If they can't say it in one sentence, the skill is probably two skills.
2. **When should it trigger?** What would a user actually type or ask that means "use this now"? Collect real phrasings, including ones that don't name the skill directly.
3. **What does good output look like?** Ask for an example of a great result and, if possible, a bad one. The gap between them is what the skill has to enforce.
4. **What are the steps?** Walk through the task as if teaching a sharp new hire. Note the order, the decision points, and the places where people usually screw it up.
5. **What varies?** Are there different modes, frameworks, or domains the skill has to handle (e.g. "same idea but for AWS vs GCP vs Azure")? Those become separate reference files.
6. **Any real resources?** Existing templates, code that already does part of this, style rules, lookup data, example files. These become scripts and assets rather than being reinvented in prose.
7. **What tools does the AI need?** Does the task require running code, web access, file creation, a specific library? Note dependencies so the skill can state them.

Push on edge cases and failure modes here, not later. The interview is cheap. Rewrites are not.

If you're building a batch of skills at once rather than a single one, read "Building many skills at once" near the end of this file before you start interviewing - it changes how you run this phase.

## Phase 2: Choose the shape

Based on the interview, decide the file layout before writing. Most skills are one of these shapes:

- **Single file.** Just `SKILL.md`. Correct for most skills. If the whole thing fits comfortably under ~500 lines and has no reusable code or templates, stop here. Do not manufacture complexity.
- **Body plus references.** Use when there is deep detail that is only sometimes needed, or when the skill spans multiple variants/domains (one reference file per variant). The body holds the workflow and the logic for *choosing* which reference to read; each reference holds one variant's specifics.
- **Body plus scripts.** Use when part of the task is deterministic and error-prone to do by hand each time (parsing, format conversion, validation, generation from a template). Write the script once; have the skill call it.
- **Body plus assets.** Use when the output is built from a fixed template or starter file. Ship the template as an asset; have the skill fill it in.
- **The works.** Larger skills combine all of the above. Organize by domain when there are variants (see the layout in `references/anatomy.md`).

When in doubt, start smaller. It is far easier to split a file later than to explain to a user why their simple skill became a directory tree.

## Phase 3: Write the SKILL.md

Write the metadata block first, then the body.

### The metadata block

At the very top of the file, between two lines of three dashes, put the name and description. Nothing else is required. Example:

```
---
name: invoice-parser
description: Extract structured line items from PDF and image invoices into a clean spreadsheet. Use whenever someone uploads an invoice, receipt, or bill and wants the amounts, dates, vendor, or line items pulled out, tabulated, totaled, or reconciled - even if they just say "get the numbers out of this" or "what did we spend here."
---
```

Rules for the two fields:

- **name**: short, lowercase, hyphenated, memorable. It is the identifier.
- **description**: this is the most important sentence you will write, because it alone decides whether the skill ever gets used. It must say both *what the skill does* and *when to reach for it*, packed with the concrete phrasings and contexts a real user would use. AIs tend to *under*-trigger skills - to not use them when they should - so lean slightly pushy. Name the situations explicitly, including the ones where the user won't say the skill's name. Put every "when to use this" cue here, not in the body. See `references/descriptions.md` for how to write and stress-test these.

### The body

The body is a playbook written for an AI to execute. Guiding principles, in priority order:

**Explain the why, not just the what.** Modern AIs are smart and have good theory of mind. An instruction with a reason behind it ("sort by date descending, because users scan for the most recent entry first") generalizes to situations you didn't foresee. A bare command ("ALWAYS sort by date descending") does not, and it breaks the moment reality differs slightly from your example. If you find yourself stacking up ALL-CAPS MUSTs and NEVERs, stop: that is usually a sign you are compensating for an instruction you failed to explain. Reframe it as reasoning.

**Write in the imperative.** "Extract the vendor name from the header block," not "The skill should extract..." You are talking to the executor, so talk to it directly.

**Show, don't only tell.** A worked example is worth a paragraph of description. Include one or two small input/output examples for anything with a specific format. Keep them short and representative, not exhaustive - the reference files are where exhaustive lives.

**Generalize past your examples.** You are writing something meant to run on thousands of inputs you will never see. If the skill only works on the three examples in front of you, it is worthless. Prefer patterns and reasoning over rules pinned to specific cases.

**Stay lean.** Every line should earn its place. Cut anything that doesn't change what the AI does. A tight skill is easier to follow than a bloated one, and it leaves more context budget for the actual task.

**Point clearly to resources.** When the workflow needs a reference, script, or asset, say so explicitly and say when: "For Azure deployments, read `references/azure.md` before proceeding." "Run `scripts/validate.py` on the output and fix anything it flags." The AI won't open a file you don't tell it to open.

A typical body structure, which you should adapt rather than follow rigidly:

```
# Skill name

One or two sentences on what this does and the mindset to bring.

## When to use which approach   (only if there are variants)
Decision logic for picking a path / reference file.

## Workflow
The ordered steps. Decision points called out. Failure modes flagged.

## Output format
The exact shape of a good result, shown concretely.

## Examples
One or two short worked examples.

## Resources                     (only if bundled files exist)
What each reference/script/asset is and when to reach for it.
```

### Safety and honesty

Do not build skills whose real purpose is hidden or harmful: no malware, no credential theft, no data exfiltration, nothing that would surprise the user if you described it plainly. If a request's stated purpose and actual effect don't match, don't build it. Ordinary things like "roleplay as a support agent" or "always answer in the style of a pirate" are completely fine.

## Phase 4: Write the bundled files

Only create the files the shape you chose calls for.

**References** go in `references/`. Each is a focused document on one topic or variant. If a reference is long (say over ~300 lines), give it a short table of contents at the top so the AI can navigate it. The body of the skill should tell the AI which reference to read and when, so it never has to load all of them at once.

**Scripts** go in `scripts/`. Write the script to do one job well, with clear inputs and outputs, so the skill can invoke it without the AI re-deriving the logic each time. State any dependencies. Prefer scripts for anything deterministic and repetitive - it is faster, more reliable, and cheaper than having the AI redo the reasoning on every run. A good signal that something should be a script: if you imagine the skill running a hundred times and the AI writing basically the same helper code each time, bundle that code.

**Assets** go in `assets/`. These are files that end up *in* the output or are used to produce it: templates, boilerplate documents, starter configs, icons, fonts. The skill fills them in or builds on them rather than generating them from scratch.

Templates you can copy as starting points live in `templates/` in this skill (a starter `SKILL.md`, a reference file, and a script header). Use them to save time; adapt freely.

## Phase 5: Test it, at least by hand

You do not need a formal eval harness to sanity-check a skill, and in a plain chat you won't have one. But you must not hand over an untested skill. At minimum:

1. Invent two or three realistic prompts - the kind a real user would actually type, not clean textbook cases. Show them to the person and ask if they're representative.
2. For each, read the skill fresh and follow it exactly as written to produce a result. Pretend you don't already know the intent; only use what the skill says. This catches instructions that only make sense because *you* wrote them.
3. Look hard at each result against the "good output" the person described in the interview. Where it falls short, the fix is almost always in the skill, not the run.

Two things to specifically probe:

- **Does the description trigger correctly?** Would this skill actually get picked for the phrasings the user gave, and *not* get picked for near-miss phrasings that need something else? A description that fires on everything is as useless as one that fires on nothing.
- **Does the skill generalize?** Try a prompt that differs from your examples. If it only works on the examples, revise toward reasoning and patterns.

## Phase 6: Iterate

Improve based on what the test runs and the person's feedback reveal. When you revise:

- **Generalize from the feedback, don't overfit to it.** One example failing usually points to a general gap, not a need for a special case. Fix the underlying reasoning, not the symptom.
- **Cut before you add.** If the skill made the AI waste effort, the fix might be removing an instruction, not adding one.
- **Watch for repeated work.** If every test run had the AI writing the same helper code or doing the same multi-step dance, that is a script waiting to be born.
- **Re-read with fresh eyes.** Draft, walk away, come back, and read it as if you'd never seen it. The awkward instructions jump out.

Repeat until the person is satisfied and the outputs are reliably good across varied prompts.

## Phase 7: Package and hand off

The deliverable is the skill folder. Structure:

```
skill-name/
├── SKILL.md
├── references/   (if any)
├── scripts/      (if any)
└── assets/       (if any)
```

If you are in an environment with a file-delivery mechanism, zip the folder and hand it over. If you are in a plain chat with no file tools, print the full contents of every file, clearly labeled with its path, so the person can save each one into the right place by hand. Either way, tell them where each file goes.

## Building many skills at once

Sometimes the ask isn't one skill, it's a batch: a stack of SOPs to convert, a whole team's workflows, or a library you're growing over time. The phases above still apply to each skill, but run them at the batch level too, or you end up with ten skills that don't feel like they belong together.

- **Batch the interview.** Don't run Phase 1 at full depth for each skill in sequence. First pass: get the one-sentence "what it does" and rough trigger phrasings for every skill in the batch, side by side. This surfaces overlap and gaps you'd miss doing them one at a time. Second pass: go deep - steps, examples, variants - only on the skills that actually need it.
- **Check for collisions before writing anything.** Once you have draft descriptions for the whole batch, read them together and ask: could two of these fire on the same real request? If an "expense-report" skill and a "receipt-parser" skill would both claim "get the numbers off this receipt," narrow one with an explicit boundary (see `references/descriptions.md`). This check only works with the full set in view - it's worthless done per skill.
- **Keep naming and shape consistent.** Pick one naming convention and apply it across the batch. Reuse the same shape (Phase 2) for skills that are structurally similar, so the set reads like it was written by one person with one standard, not assembled from ten one-off jobs.
- **Maintain a catalog.** Past a handful of skills, keep an index: a single file (e.g. `CATALOG.md` at the root of the skills collection) listing each skill's name, one-line description, and folder path. Update it whenever you add or change a skill, and read it before starting a new one - that's how you catch a near-duplicate before you build it instead of after.
- **Scaffold the boring parts.** Once specs for the batch are settled (name, description, shape, which references/scripts/assets each needs), don't hand-type the same directory tree ten times. Run `scripts/scaffold_skills.py` on a JSON list of specs to generate the folders and starter files, then fill in the real content per skill. If you can't run code, build each folder by hand from `templates/` instead - the scaffolder only saves typing, it doesn't change what a correct skill looks like.

## Reference files in this skill

- `references/anatomy.md` - the full anatomy of a skill, directory layouts, and the multi-variant organization pattern, with examples.
- `references/descriptions.md` - how to write the description field so the skill triggers correctly, with good and bad examples and a stress-test method.
- `references/portability.md` - how to keep a skill vendor-agnostic so it runs on any AI, and what to do when a target tool has quirks.

## Templates in this skill

- `templates/SKILL.template.md` - a starter SKILL.md with the structure filled in as prompts.
- `templates/reference.template.md` - a starter reference file with a table of contents stub.
- `templates/script.template.py` - a starter script with a documented input/output contract.

## Scripts in this skill

- `scripts/scaffold_skills.py` - generates starter folders for a batch of skills from a JSON list of specs. Run it when you're building many skills at once and the specs (name, description, shape) are settled. See "Building many skills at once" above.

Read the reference files when the moment calls for them, per progressive disclosure - not all upfront. Now go build the thing.
