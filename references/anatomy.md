# Skill anatomy

Read this when you need to decide how to lay out a skill's files, especially one that spans multiple variants or domains.

## Contents

- The three resource buckets
- Single-file skills
- Skills with references
- Skills with scripts
- Skills with assets
- The multi-variant pattern
- How the layers load

## The three resource buckets

Everything beyond `SKILL.md` falls into one of three folders, distinguished by *how the AI uses the content*, not by file type:

- **references/** - content the AI *reads* to inform its work, pulled into context on demand. It is knowledge. Specs, edge-case handling, lookup tables, style guides, per-variant detail.
- **scripts/** - content the AI *runs*. It is executable. The output matters, not the source. Parsers, validators, converters, generators.
- **assets/** - content that becomes part of, or seeds, the *output*. It is raw material. Templates, boilerplate, config stubs, images, fonts.

A quick disambiguation, because these get confused: a Word template the skill fills in is an **asset** (it goes into the output). A document explaining the house style for Word documents is a **reference** (the AI reads it to decide how to write). A Python file that stamps data into the template is a **script** (the AI runs it).

## Single-file skills

Most skills should be exactly this:

```
skill-name/
└── SKILL.md
```

If the whole playbook fits comfortably under about 500 lines, has no reusable code, and needs no external template, do not add folders. Structure that isn't needed is just friction.

## Skills with references

```
skill-name/
├── SKILL.md          (workflow + logic for which reference to read)
└── references/
    ├── topic-a.md
    └── topic-b.md
```

Use when there is detail that is deep but only sometimes relevant. The body stays lean and routes to the right reference. The AI never loads `topic-b.md` on a `topic-a` task.

## Skills with scripts

```
skill-name/
├── SKILL.md          (workflow that calls the script)
└── scripts/
    └── do_the_thing.py
```

Use when part of the task is deterministic and repetitive. The script encodes it once. The skill body tells the AI when and how to run it and what to do with the result.

## Skills with assets

```
skill-name/
├── SKILL.md          (workflow that fills in the template)
└── assets/
    └── report-template.docx
```

Use when the output is built on a fixed starting file. The skill populates the asset rather than generating structure from nothing.

## The multi-variant pattern

This is the most important layout to get right, because it is where progressive disclosure pays off most. When one skill has to handle several parallel variants - the same task across different frameworks, cloud providers, document types, languages - do **not** cram all of them into the body. Put the shared workflow and the selection logic in the body, and give each variant its own reference file:

```
cloud-deploy/
├── SKILL.md          (shared workflow + "which provider?" decision logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The body reads something like: "Determine the target provider from the user's request or config. Then read the matching reference file - `references/aws.md`, `references/gcp.md`, or `references/azure.md` - and follow it. Do not read the others." An AWS task then loads only the AWS detail. This keeps every run lean no matter how many providers you support, and adding a fourth provider is just a new file plus one line in the selector, not a rewrite of the body.

The same shape works for any "one concept, many flavors" skill: a testing skill with `jest.md` / `pytest.md` / `rspec.md`; a legal-doc skill with `nda.md` / `msa.md` / `sow.md`; a translation skill with a reference per language pair.

## How the layers load

To keep the mental model straight:

| Layer | When it enters context | Budget | What lives here |
|---|---|---|---|
| description | every request, always | ~1-3 sentences | trigger cues: what + when |
| SKILL.md body | when the skill triggers | ~500 lines | workflow, rules, small examples, routing |
| references | when the body sends the AI to one | unlimited | deep detail, per-variant specifics |
| scripts | when the body has the AI run one | unlimited (source never loads unless read) | deterministic computation |
| assets | when the body pulls one into the output | unlimited | templates, boilerplate, media |

The design goal for every skill: the common path stays cheap, and cost is only paid for depth exactly when depth is needed.
