# Adversarial Route: Test the Plan with Counterexamples

## Definition and Boundary

The Adversarial route tests the current plan. It looks for a concrete input, state, or operation sequence that makes a key assumption, an expected result, or a failure handler fail. It answers one question: under what condition does this plan fail, and what is the evidence?

The route tests the conditions that make the plan work. It may also show that the main direction cannot work. It does not assume that the plan has a problem.

The common input and output format, the severity, the authorization, the rounds, and the re-review rules are in the [main file](../SKILL.md). The cooperation of the routes is in [Multi-Route Review](multi-route-review.md). This file gives the adversarial method only.

The Adversarial route delivers checkable counterexamples and the conditions that a repair needs. The [Alternative Route](alternative-review.md) explores other solutions and compares them. The Adversarial route may propose a local repair, and it may show that a local repair is not sufficient. If it finds another direction, it lists the lead. A full redesign is not a required product of this route.

## How to Build a Useful Counterexample

Read the Core Task and the Core Preconditions of the [main file](../SKILL.md#core-task-and-core-preconditions). First try a concrete case that rejects a Core Precondition or a key cause-and-effect link. If each step follows the plan, can the core result still fail? Then build a failure path from the real implementation or the real material. Do not check the listed assumptions only. Select the entry points that fit the task. Do not walk the full list of the checklist.

| Entry point | Assumption to test | Case to build |
|---|---|---|
| Input and state | The input is always complete and legal. The current state is as expected. | An empty value, duplicate data, an old record, a mixed version |
| Order and concurrency | The steps run in the stated order, one time only. | A retry, a second trigger, a wrong order, a state change between two steps |
| Partial failure | The system recovers, or stays consistent, after an interruption. | A half-finished write, a timeout whose operation really succeeded, a rollback that fails |
| Boundary and dependency | The permission, the external contract, or the resource always holds. | A permission change, an unavailable dependency, a capacity or time limit reached |
| Acceptance and observability | A passing acceptance proves the goal. | A test passes but misses a consumer; the check reads a claim or a surface state |
| **Internal consistency of one item** | The rule, the property, and the assertion agree. | Put the "rule" of a section and its "property" or "assertion" into one input. Example: the rule says `has(x) means reject`, but the property says `has(x) means allow and do not charge`. Or the rule says "a failure charges nothing", but one dimension charges by a state change. |

**Check "internal consistency of one item" as a separate case.** Do not expect another entry point to cover it. This problem needs no external input. Two sentences are enough. Each other entry point starts from "how does the outside world break it?", so it goes around this problem. When one document is repaired again and again, new problems usually sit here: the repairer reads only the passage that it changed.

For each candidate counterexample, check three points.

1. Can the case occur inside the current scope?
2. Does the execution path exist, or does the plan miss a required handler?
3. Does the result violate the goal, a constraint, or a promise of the plan?

Do not declare a problem from "it is possible in theory". Do not ignore a serious result with evidence because the probability is low.

If the plan is not implemented yet, derive the result from the existing implementation, the agreements of the dependency owners, and the planned steps. Mark the conclusion "plan reasoning". Do not write it as a reproduced runtime result. If the evidence is short, list the unverified assumptions and the minimum check. Do not invent a call path or a test result.

## Counterexample Output

Use the problem item format of the main file. Add this evidence chain. Do not build a second count.

> The promise or assumption under test; the trigger input or the initial state; the operation or call order; the failure point and the observable result; the raw evidence; the minimum check; the conditions that a repair needs.

Example. The plan says "a retry after a failure does not charge twice", and gives one rule: "call the charge, then write the done mark". The reviewer builds this order: the charge succeeds, the process stops before the mark, the system recovers and retries. Check whether an idempotency key or a dedup record exists. Then judge whether the second charge occurs. If a mechanism already prevents the second charge, give that evidence. Do not list the case as a problem.

## Discipline and Re-Review

- Test an assumption with concrete evidence. Do not use a strong tone, a general risk list, or a rewording of another route's conclusion as a counterexample. If you find the same problem as another route, give independent evidence. Do not invent a new problem to look unique.
- "Another implementation exists" is not a problem. The review intensity is not the problem count. If no counterexample holds, state the key assumptions you checked, the cases you rejected, and the limits of the check.
- For a check, use a read-only check, a reasoning step, or an isolated sample. These answer the current question. If an operation is necessary, obey the authorization and the run-for-agent rules of the main file. Do not use damage to real data, or a run of the planned implementation, as proof of a point.
- A re-review checks the original trigger again, and checks whether the repair adds a new failure path. Do not close a counterexample only because the plan now adds one sentence "handle the exception".
