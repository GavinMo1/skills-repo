# Alternative Route: Explore Other Solutions

## Definition and Boundary

The Alternative route explores solutions other than the current plan. It uses three tiers by the size of the change; see "Three Tiers" below.

Tier A adds one route to the current route count. It starts from the User goal and the hard constraints. It does not adopt the architecture, the mechanism, or the steps of the current plan in advance. Tier B and Tier C add no route. An existing review route can do them.

The route judges one point: can another solution remove the problem that the current plan cannot solve? Start Tier A as soon as its trigger is true: a Core Precondition is false, or the plan has no workable repair. Do not wait for a fixed round. Start Tier B and Tier C by the routing rules of the main file. The start time, the rounds, and the exit conditions follow the [main file](../SKILL.md). The cooperation of the routes is in [Multi-Route Review](multi-route-review.md).

| Dimension | Adversarial route | Alternative route |
|---|---|---|
| Main question | Under what condition does the current plan fail? | Is there a better path to the same goal? |
| Starting point | The current plan and its assumptions | The User goal, the hard constraints, and the raw facts |
| Main product | A counterexample, its trigger path, the effect, and a check | A candidate, its evidence, a comparison, and a recommendation |
| Size of change | A local repair of a failure | A new mechanism, duty, dependency, or implementation order |

## Three Tiers

An alternative solution is not only "replace the whole plan". The tiers use the size of the change relative to the object that the tier replaces. They do not use the size relative to the whole plan.

| Tier | Object replaced | What to judge | Example |
|---|---|---|---|
| **A: change the approach** | The technical approach, the architecture | Does the new approach remove the Core Precondition that the old approach cannot meet? Which conditions does it add? | The old plan keeps repairing "how to compensate a double write". Explore "one authoritative source plus a derived view". Check the delay, the migration, and the compatibility cost. |
| **B: change one component** | **One** decision point of the Decision Table | If one implementation is replaced at that decision point, do the properties of the plan still hold? What is the cost? | A quota model: counter, reserve with conditional release, or periodic scan. An ownership boundary: exact match, path prefix, or a predicate of the upstream. A frame boundary: a random nonce, a fenced block, or a full escape. |
| **C: do less, or do nothing** | The requirement | How much do the existing mechanisms cover? Is the smaller goal still worth the work? | Does an existing cross-session message mechanism already cover most of the goal? Can "any session" become "the same project"? |

Use the tier that fits the size. Do not test all three with one rule.

- **Tier A** needs the high standard "a real difference from the current plan". It is also the only tier that needs a blind review at the start.
- **Tier B** replaces one decision point, so it is a real difference by nature. It needs no separate exploration. Judge two points: is the replaced element really gone, and does the property that the plan needs from it still hold? A new boundary condition, a new name, or new wording is not an alternative solution.
- **Tier C** answers two questions only: how much is covered, and what is missing. It gives no new plan.

One round may hold Tier B candidates and a revision proposal for the current plan. A Tier B recommendation does not lose value because it changes one point only.

Keep the User goal and the hard constraints. The route may select a different technical approach. If a candidate needs more authorization, a lower goal, or a change to a confirmed User decision, mark it a conditional proposal. State the change. Do not claim that it meets the current constraints.

## Rounds and Route Accounting

- **Tier B and Tier C add no review route and use no round.** An existing route does them. The blind stage and the comparison stage of Tier A together are one route of that round.
- If the User fixes the route count, obey that number. State that no alternative route was added for this reason.

## First Blind Review and Later Reuse

Tier B and Tier C go directly to the comparison review. They select inside a known plan. To hide the plan gives no value, and it gives no comparable candidate.

Tier A does one blind review at its **first start**. The Author gives the goal, the hard constraints, the position of the raw material, and this file only. The Author does not give the current plan, the reason of the Author, or the old problems. The reviewer returns candidate directions with the facts and the key assumptions. The Author then gives the common snapshot and the open problems. The same reviewer compares the candidates with the current plan and uses the common output format.

After that, reuse the same reviewer. Update the comparison with each new snapshot and each confirmed fact. Do not explore from zero again. If the tool cannot isolate the context, state which material is exposed. Do not claim a blind review.

## Candidate Quality and Output

For each candidate, state the mechanism, the change positions, the existing code to reuse, the new dependencies, and the possible failures. State how it removes the blocker of the current plan. Propose a minimum experiment or check that tests the key assumption. An architecture name, or "change the technology", is not enough to judge feasibility.

In the comparison stage, read the Core Task and the Core Preconditions of the [main file](../SKILL.md). Check whether the candidate avoids a Core Precondition that the current path cannot meet. State which conditions the new approach makes unnecessary, and the evidence for each new condition. A necessary condition of the User goal still holds. Do not lower the goal and claim that the blocker is gone.

Give each candidate with evidence and a real difference. For Tier A, the difference is the whole technical approach. For Tier B, the difference is the replaced decision point. For Tier C, the difference is the scope of the requirement. If you find no candidate, state which directions you explored, why you rejected each, and which uncertainties remain. Do not invent a candidate. You may recommend to continue the revision of the current plan, with evidence.

In addition to the common output of the main file, give four items.

1. **Goal and blocker**: which goals and hard constraints must stay, and which problem blocks the implementation of the current plan.
2. **Candidates**: the mechanism, the key steps, the existing code to reuse, and how the candidate removes the blocker. If no candidate works, give the reason for each rejection.
3. **Comparison**: goal coverage, constraint fit, complexity, implementation and migration cost, compatibility and rollback, main risks. Support each point with a fact. Do not use a subjective score to look exact.
4. **Check and recommendation**: the minimum check; the unverified items and the open decisions by owner; the recommendation to keep, partly adopt, or switch the path, with its conditions. Keep the optional experiment of the candidate separate from the mandatory check of the current plan.

Add the tier-specific items.

- **Tier B** gives three items. First, the replaced decision point and its current implementation. Second, a "holds when" line: which facts the choice depends on, and which change of evidence forces a new choice. Third, the **cross list with the other rules of the plan**: the properties, assertions, and acceptance items that must change after the replacement. The cross list is more useful than the candidate. A decision point that is repaired again and again almost always has an incomplete cross list.
- **Tier C** gives four items: the current coverage of the existing mechanisms; which component or entry point covers what; the gap; the Core Preconditions that still hold after the scope shrinks.
- **Tier A** follows "First Blind Review and Later Reuse" above. It needs no cross list, because the whole approach changes.

## Decision and Later Work

The Author checks the evidence, then keeps the current plan, adopts part of a candidate, or switches to a candidate. Write the reason in the record. Then handle the check, the authorization, and the re-review as the main file says. A reviewer reports the plan problems and the exploration proposals separately. A candidate that the Author does not adopt does not change the pass conclusion.

In a later re-review, the Alternative route checks whether a candidate still works after the constraints or the plan changed. Keep, adjust, or withdraw the recommendation with evidence. Do not require a new direction each round.
