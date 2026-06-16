# Writing the description

Read this when writing or fixing the `description` field. It is the highest-leverage sentence in the whole skill, because it alone determines whether the skill ever gets used. A perfect playbook with a weak description is dead code.

## Contents

- What the description is for
- The two jobs every description must do
- Why to lean pushy
- Good and bad examples
- Stress-testing a description
- Common mistakes

## What the description is for

When an AI is deciding how to handle a request, it sees a list of available skills, each represented by just its name and description. It does not see the bodies. It picks which skill (if any) to consult based on that description alone. So the description is not a summary for humans, it is a matcher for the AI. Write it to be recognized, not to sound nice.

## The two jobs every description must do

1. **State what the skill does.** Plainly. The capability, the output.
2. **State when to reach for it.** The concrete situations, phrasings, and contexts that mean "now." This is the part people skip, and it is the part that matters most.

Put *all* the "when to use this" information in the description, never in the body. The body is only read after the skill is already chosen, so a trigger cue hidden in the body never fires.

## Why to lean pushy

Empirically, AIs tend to *under*-trigger skills: they default to handling things themselves and forget the skill exists. So bias the description toward being slightly aggressive about claiming its territory. Name the situations explicitly, and specifically name the ones where the user won't say the skill's name or the obvious keyword.

Weak: `A tool for building dashboards.`

Strong: `Build a fast, clean dashboard for internal metrics. Use this whenever someone wants to visualize data, display company numbers, track KPIs, or show any kind of metrics or internal data - even if they don't use the word "dashboard," e.g. "can you show me how our signups are trending" or "put our sales figures somewhere the team can see them."`

The strong version enumerates the disguised requests. That is what makes it fire when it should.

## Good and bad examples

**Bad** (vague, no triggers, human-summary tone):
```
description: Helps with resumes.
```

**Good** (capability + explicit, varied triggers):
```
description: Turn a rough work history into a polished, ATS-friendly resume tailored to a target role. Use whenever someone shares their experience, an old resume, or a job posting and wants it written, rewritten, tightened, reformatted, or tailored - including vaguer asks like "make me look good for this job," "fix my resume," or "help me apply to X."
```

**Bad** (fires on anything with the keyword, no boundary):
```
description: Use this for anything involving data.
```

**Good** (scoped, with the boundary made explicit):
```
description: Clean and restructure messy tabular data files (CSV, TSV, XLSX) into tidy spreadsheets - fixing malformed rows, stray headers, merged cells, and junk values. Use when the deliverable is a corrected spreadsheet file. Do not use for building charts, writing SQL, or database work; those are different tasks even though they also touch data.
```

Note how the good scoped example says what it is *not* for. Explicit boundaries prevent a greedy skill from swallowing adjacent requests it would handle badly.

## Stress-testing a description

Before you ship it, run this cheap test in your head or on paper. Write down ~10 prompts that *should* trigger the skill and ~10 that should *not* but are near-misses (they share keywords or concepts but actually need something else). Then, reading only the description, decide for each: would this fire?

- If a should-trigger prompt wouldn't fire, the description is missing that phrasing or context. Add it.
- If a should-not-trigger near-miss *would* fire, the description is too greedy. Add a boundary.

The valuable test cases are the near-misses, not the obvious ones. "Write a fibonacci function" is a useless negative test for a PDF skill because nothing about it tempts a match. "Extract the tables from this scanned contract and total the payment column" is a great test - it is genuinely ambiguous between a PDF skill, a spreadsheet skill, and a data skill, and the description has to make the right one win.

## Common mistakes

- **Summarizing instead of triggering.** "This skill provides comprehensive support for document generation workflows." Says nothing about *when*. Useless.
- **Only listing formal phrasings.** Real users are casual, terse, and don't name file types or skills. Cover "get the numbers out of this" alongside "extract structured line items."
- **Hiding triggers in the body.** They never fire there. Move them up.
- **No boundary on a broad domain.** If the skill touches a big area (data, writing, code), say what it does *not* cover, or it will get picked for tasks it botches.
- **One flavor of phrasing.** Include formal and casual, long and short, keyword-present and keyword-absent. Coverage beats polish.
