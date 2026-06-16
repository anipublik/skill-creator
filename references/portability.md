# Portability

Read this when the skill needs to run on more than one AI tool, or when you don't know which tool will run it. The whole value of a packaged skill is that you write it once and hand it to anything. A skill welded to one vendor's quirks defeats that.

## Contents

- The portability principle
- What is safe to assume
- What is not safe to assume
- Degrading gracefully
- Handling tool-specific quirks
- Running a skill in a plain chat

## The portability principle

Write the skill against *capabilities*, not against a specific product's implementation of them. "Read the uploaded file" is portable. "Use the `view` tool on `/mnt/user-data/uploads/`" is not - that path and tool name belong to one environment. State what needs to happen and let the executing AI map it to whatever tools it has.

## What is safe to assume

Almost every capable AI that could run a skill can:

- Read text you give it and follow multi-step instructions.
- Reason about a task and adapt to inputs it hasn't seen.
- Produce text output in whatever format you specify.
- Follow a reference to "read file X" if the file is available to it.

Build the core of the skill on these, and it will run nearly anywhere.

## What is not safe to assume

Do not assume, without checking, that the target AI has:

- **Code execution.** Many chat contexts can't run scripts. If your skill relies on a script, say what the script does in enough detail that an AI *without* execution could do the work by hand, or clearly mark the script path as the fast route with a prose fallback.
- **Web access.** Don't assume it can fetch a URL or search unless you know it can.
- **File creation or a filesystem.** Some environments return text only. If the skill "produces a file," describe the fallback: print the file's full contents, labeled, for the user to save.
- **Specific tool names or paths.** `view`, `bash`, `str_replace`, `/mnt/...` - these are environment-specific. Refer to the action ("open the file," "run the validator"), not the vendor's tool name.
- **Subagents, background jobs, or a browser.** Advanced orchestration is not universal. Keep the required path linear and doable by a single agent in one conversation.

## Degrading gracefully

The pattern that keeps a skill portable is: **describe the ideal path, then describe the fallback.** For anything that depends on a capability the target might lack, write it so a leaner AI can still get the job done, just less conveniently.

Example, for a skill that validates its output with a bundled script:

> Validate the result. If you can run code, run `scripts/validate.py` on the output and fix anything it reports. If you cannot run code, check the output by hand against these rules: [list the rules the script enforces]. Either way, the output must satisfy every rule before you hand it over.

The script is the fast path; the inline rules are the fallback; the requirement is the same. Any AI can meet it.

## Handling tool-specific quirks

Sometimes you *know* the skill will often run in a particular tool that has a specific behavior worth accommodating (a formatting convention, a file-delivery mechanism, a length limit). Handle this without breaking portability by scoping the advice:

> If you are running in a tool that can present files to the user directly, deliver the folder that way. Otherwise, print each file's contents inline, labeled with its path.

You are giving the AI a conditional, not a hard dependency. It takes the branch that fits its environment. Keep these conditionals rare and clearly optional; the default path should assume the least.

## Running a skill in a plain chat

The most constrained realistic target is a bare chat window: no file tools, no code execution, no web. A well-built skill still works there. To make sure yours does:

- The `SKILL.md` body must contain enough to do the task from text alone. References and scripts are enhancements, not load-bearing secrets.
- If the skill has scripts, their essential logic must also be recoverable from the prose, so a chat-only AI isn't blocked.
- Delivery falls back to printed, labeled file contents the user copies by hand.

If your skill can be pasted into a plain chat and still produce a good result, it is genuinely portable. That is the bar.
