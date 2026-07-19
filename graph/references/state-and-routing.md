# State and routing

Read this when designing the shared state schema or writing the routing rules for a graph's conditional edges.

## Contents

- Designing the shared state schema
- Writing routing rules
- Worked examples: bad and fixed

## Designing the shared state schema

For every field in the payload that travels along a graph's edges, answer four questions before writing the graph body:

- **Owner.** Which node writes this field? Two nodes writing the same field is only a problem when both could run in the same execution - a branch and its sibling that reconverge later (auto-decide or human-review, never both) aren't in conflict, since the topology itself guarantees only one runs. Reserve "define who wins" for fields two nodes could genuinely write in the same run - true parallel branches, or a cycle-back that revisits a node that already wrote the field once.
- **Readers.** Which nodes read it to make a decision? A field nothing reads is dead weight; remove it or find what's supposed to use it.
- **Durability.** Does it need to survive a checkpoint and resume, or is it only meaningful within the current run?
- **Sensitivity.** Does it contain anything that shouldn't be logged, persisted longer than necessary, or passed to a node that doesn't need to see it?

Keep the schema as small as the routing rules and node contracts actually require. A bloated shared state object is the graph equivalent of an agent that was handed every tool "just in case" - it makes every node harder to reason about and gives failures more places to hide.

## Writing routing rules

A routing rule is a condition on state, evaluated at a specific edge, that determines which node runs next. Write it so someone could implement it without asking what you meant:

- Name the exact field being checked.
- Name the exact comparison and threshold.
- Name the destination for every outcome, including the case nobody expects. A router with three destinations and only two defined conditions has an implicit fourth destination - whatever happens when neither condition matches - and that implicit path is where bugs live.

## Worked examples: bad and fixed

**Bad:** "If the response looks risky, send it to review."
**Fixed:** "If `risk_score >= 0.6`, route to the human-review node. If `risk_score < 0.6`, route to the auto-approve node. `risk_score` is written by the risk-assessment node and is required before this edge evaluates; if it's missing, route to human-review as the safe default rather than failing the edge."

**Bad:** "The graph waits for the parallel checks to finish, then continues."
**Fixed:** "The fan-in node requires results from `check_a` and `check_b`. If both return within 30 seconds, continue with both results. If one times out, continue with the completed result and flag `partial_result: true` in shared state for the downstream node to handle. If both time out, route to the escalation node."

**Bad:** "State gets passed along as the conversation goes."
**Fixed:** "`case_id`, `customer_tier`, and `risk_score` are durable and persist across a pause. `draft_response` is ephemeral and is cleared once the response node completes. `internal_reasoning_notes` is never persisted past the run that produced it and is not passed to the human-review node's display, only to its context."

Every fix replaces an implicit assumption with a name, a value, and an explicit answer for the case that wasn't the main path.
