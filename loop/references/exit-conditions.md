# Exit conditions

Read this before you consider Phase 3 of `LOOP.md` finished. This is the part of a loop design most likely to be half-done, and it's the part that actually matters when something goes wrong at 2am.

## Contents

- Wired versus named, with a concrete test
- Stagnation detection patterns
- Budget types, including costly and irreversible actions
- Escalation thresholds that aren't vibes
- Worked examples: bad exit conditions and their fixes

## Wired versus named, with a concrete test

A named exit condition is a sentence describing when the loop should stop. A wired exit condition is code, a graph edge, or an evaluated check that actually runs every round and actually halts execution when it's true.

The test: point at the exact place in the implementation where the condition gets checked. If you can point at a line of code, a conditional edge, or a gate that runs unconditionally every round, it's wired. If the answer is "the prompt tells it to stop when it's done" and nothing external verifies that, it's named. A named exit relies on the same reasoning process that might be stuck or wrong to also correctly notice it should stop - which is exactly the case it needs to protect against.

Every exit condition in a loop's design should pass this test before the loop ships. If any of the four exit types below (success, budget, stagnation, escalation) is only named, treat the loop as unfinished - except stagnation for a fixed-step archetype, where repeating the identical action every round is the design, not a symptom to catch. See `LOOP.md` Phase 3 for that carve-out.

## Stagnation detection patterns

Pick a detection method that matches what "the same thing again" actually means for this loop:

- **Exact match.** Compare round N's action and output byte-for-byte to round N-1's. Cheap, catches simple retry loops (an agent calling the same failing tool with identical arguments). Misses cosmetic variation.
- **Structural match.** Compare the *shape* of the action - same tool, same target, materially the same arguments - even if some surface text differs. Catches an agent that reworded its reasoning but is functionally repeating itself.
- **State-delta check.** After each round, compare the piece of state the loop is trying to converge on to its value before the round. If it hasn't moved (numerically, or by some similarity measure for text) for N consecutive rounds, that's stagnation regardless of whether the actions looked identical.
- **Oscillation check.** Track the last several actions or states and check for a short repeating cycle (A, B, A, B) rather than a flat repeat. Common in loops that overcorrect - fix X, which breaks Y, fix Y, which breaks X again.

Default to the state-delta check when you're unsure. It measures the thing that actually matters - is the loop making progress toward its convergence target - rather than a proxy for it.

## Budget types, including costly and irreversible actions

Every loop needs at least one budget type that's independent of the success check:

- **Iteration cap.** A hard maximum round count. The simplest backstop and the minimum bar for any loop.
- **Cost cap.** A maximum spend - tokens, dollars, API calls - for loops where rounds have variable cost.
- **Wall-clock cap.** A maximum elapsed time, for loops where a single round could hang rather than fail cleanly.
- **Action-count cap.** A maximum number of a specific kind of action, separate from the overall iteration cap. This is the one that matters most for costly or irreversible actions: a loop might reasonably get twenty read-only observation rounds but only one write action without a human approval in between. Set the write cap far lower than the overall iteration cap, and make crossing it trigger escalation rather than just stopping silently.

A loop whose rounds include an irreversible action (sending a message, executing a payment, deleting a resource) should never rely on the success or stagnation exit alone to prevent repeated execution of that action. Give the irreversible action its own explicit cap, checked before the action runs, not after.

## Escalation thresholds that aren't vibes

"Escalate if it seems stuck" is not a threshold. "Escalate after two consecutive rounds where the stagnation check fires" is. Write every escalation condition as a specific count, value, or event, matched to a named recipient - a person, a queue, a fallback process - not just "alert someone."

State what the escalation payload contains: what was attempted, what state the loop was in when it gave up, and what a human needs to pick up where it left off. An escalation that just says "loop failed" forces the person receiving it to reconstruct the whole history before they can act.

## Worked examples: bad exit conditions and their fixes

**Bad:** "The loop keeps refining the draft until it's good enough."
**Fix:** "The loop stops when a scoring function returns 0.85 or higher on the rubric in `references/scoring.md` (success), after 6 rounds regardless of score (budget), or if two consecutive scores differ by less than 0.02 (stagnation)."

**Bad:** "If the agent can't fix the bug after a while, let a human know."
**Fix:** "After 4 failed test runs, or after the agent proposes the same patch twice, stop and open an escalation with the failing test output, the last patch attempted, and the diff history attached."

**Bad:** "The reconciliation loop runs until the system is healthy."
**Fix:** "The reconciliation loop runs continuously with no completion state. It pages a human if the gap between desired and actual state hasn't narrowed for 3 consecutive checks, and it hard-stops taking corrective action - falling back to alert-only - if it has taken more than 10 corrective actions in the last hour, since that rate itself indicates something upstream is wrong that more reconciliation won't fix."

Notice the fix in every case replaces a description of intent with a number, a comparison, and a named consequence. That's the whole discipline.
