# Multi-Route Review: Duties, Dispatch, and Summary

## Duties

Give each route to a different agent. The number of routes comes from the level that the main file selects. A duty sets what a route checks first. It does not limit what a route may report.

**A Light-level plan has the Adversarial route only.** The table below and the "first two routes" text apply to the Standard and Deep levels only.

| Route | Check focus | Evidence to deliver |
|---|---|---|
| Goal and Implementation | Does the plan solve the correct problem, and can it really work? Goal coverage, facts and assumptions, entry points, division of duties, reuse of existing mechanisms, key paths, strength of the acceptance items. | The mapping from goal to steps; source or document evidence; a missing path or constraint; whether the acceptance items prove the goal |
| Operation and Evolution | Does the plan hold during operation, a gradual cutover, and later maintenance? State changes, dependencies and consumers, compatibility, partial failure and recovery, migration and rollback, maintenance cost. | The affected consumers and lifecycle cases; the state and version transition; the failure, recovery, and rollback evidence; a repeatable check |
| Adversarial | Use counterexamples to test the key assumptions and the failure paths of the plan. | Counterexample, evidence, and check method, as in [Adversarial Route](adversarial-review.md) |
| Alternative | Three tiers by the size of the change: A change the approach, B change one component, C do less or nothing. | Candidates, comparison, and recommendation, as in [Alternative Route](alternative-review.md). Tier B also gives the "conditions that make this decision point valid" and the "cross list with the other rules". |

The Operation and Evolution route checks the whole lifecycle. The Adversarial route builds concrete counterexamples. Both routes may touch the same subject. They differ by focus and by method. Their conclusions may differ, or they may agree.

Use the Core Task and the Core Preconditions of the main file to set the check. The Goal and Implementation route judges three points: whether the Core Task is correct, whether each necessary condition has evidence, and whether the key steps give the goal. The Operation and Evolution route judges whether those conditions hold during a cutover, during operation, and during maintenance. The methods of the other two routes are in their own files.

### Task variants for the first two routes

The Author may narrow the focus of the first two routes for one task. State the question of each route in the dispatch. The table is an example. It adds no role. It is not mandatory for each task.

| Task | Goal and Implementation focus | Operation and Evolution focus |
|---|---|---|
| Data migration | Data meaning, correctness of the conversion, whether the target data meets the business constraints | The cutover, compatibility, incremental sync, failure recovery, and rollback |
| Interface change | The interface contract, the call chain, the target behavior, and the link to the implementation | Consumer compatibility, version coexistence, the release transition, and rollback |

### A focused check, and problems outside the duty

Each route checks its own duty first. It does not repeat the checks of another route. If a route finds a high or medium problem with evidence outside its duty, it must report it. The completion test of a reused route is in section 2 of the main file. This rule does not require a full scan. A route must not skip a problem because the duty belongs to another route. A route must not assume that another route reports the problem.

Two routes may find the same problem. Their conclusions may differ, or they may agree. Do not invent a problem to look different from another route. When you judge the division of duties, check three points. Does each route finish its focus check? Does it give independent evidence? Does it add a subject that no other route checked? Do not require a count of unique problems. Do not require a rate of overlap.

## Dispatch and Added Routes

Give the version, the material, and the input and output format as in [Review Protocol](review-protocol.md). Add the duty of the route. Before you dispatch the Adversarial route, the Author and that route agent must read [Adversarial Route](adversarial-review.md). When you increase the level, keep the duty of each existing route and add the missing independent reviewer. Read the file of the Alternative route before it starts.

### Reuse or a new agent

**Reuse**: the same route keeps the agent of an earlier round.
**New agent**: a reviewer for that route that has not seen an earlier version.

| Duty | Who | Reason |
|---|---|---|
| All routes of round one | A new agent is mandatory | A new agent raises the blindness only. The dispatch message decides the blindness: does it hold a reason of the Author? See section 2 of the main file. |
| Re-check "was my problem really fixed?" | Reuse | Only that agent holds the evidence chain and the old version. A new agent repeats the check. |
| Re-check "does this version add a new problem?" | At least one route with a new agent this round | A reused reviewer has a blind area for a design it approved: it remembers "I passed this design" and stops asking "what else does this design need?". **This row does not apply to a one-route Light level.** |
| Cross-version consistency (is the predicate line unchanged, did a truth table flip?) | Reuse | A reviewer with no old version cannot do this. **This row does not apply to a one-route Light level.** |
| Re-check "does a closed item still hold its sentence?" | Reuse. When no route is reusable, see "When no route can be reused" below. | A scan route does not get the old positions, so this damage is invisible to it. |
| A route with no high or medium problem for two rounds | A new agent next round | The reuse value is used up. A new agent also tests one point: was there really no problem, or did the reviewer get used to the plan? |
| A large version span (the technical approach changed) | All routes with new agents | The old snapshot gives no reference. |

**Reuse is a safety duty, and the economy is a side effect.** A scan route does not get the old problems, so a regression in an item that is already closed is invisible to it. The reused route is the only reviewer that reads the position of a closed item. That damage is the usual one: a repair moves or drops a line that an earlier repair put there, and the Closure Table still says resolved. The saving in cost is the side effect.

The minimum setup of each round is in section 2 of the main file: one route with a new agent does the full scan for new problems. Each reused route checks every position that the Closure Table cites, including the rows whose status is resolved. This completion test lives in two places, here and section 2 of the [main file](../SKILL.md): change both together. Replacing a test with a pointer once lost two tests. A new agent must get the full plan text. It does not need the old problems. Write in the record which routes are reused and which are new, and which material each new agent saw.

### When no route can be reused

The table above assumes that the agent of an earlier round still answers. It fails when the rounds run in another session, in another sub-agent tree, or after the old agents are gone. Test it before you dispatch round two: name the agent of each route of the earlier round, and try to address it. If you cannot address one of them, that route is new this round and its duty loses its reader.

When no route can be reused, the regression check has no owner. Repair it in this order.

- Send each new agent a **closed-position list**: the positions of the closed items only, written as `file :: symbol` or as a section number of the plan. The list holds no history, no conclusion, no problem ID, and no wording of the original problem. Its one question is: "does this position still hold the sentence that the Closure Table cites?"
- If you cannot build that list, write "this round has no regression protection" in the record, and add one open item for each closed item whose position you could not check.

**The closed-position list does not break the blindness of a scan route.** The blindness rule protects the conclusion, the history, and the account of the Author. A position that the plan text already holds is none of those three: the reviewer of a scan route finds it in the plan alone, and the list adds no word of what was decided about it.

Each route forms its own conclusion on the common text before the summary. Do not share the problems of the current round early. Write the real check scope, the version, and the limits of each route in the record. Separate a new check from reused evidence.

## Summary and Re-Check

Merge duplicate problems about one problem. Keep the original problem ID, the route that reported it, and the new evidence, trigger condition, and effect of each route. If two problems need different repairs, do not merge them only because the subject is the same. Keep a problem or an objection that only one route reported. Do not remove it by a vote count. Settle a dispute about a fact with code, a constraint, or a check that has authorization. Ask the related reviewers to re-check a dispute about severity. The Author selects a preference inside the established constraints and the authorization.

**When two routes give one problem different severities, use the higher severity.** Write the reason of the lower route next to it. A second case is different: the routes give opposite judgments about the feasibility of one conclusion. One says "this cannot work", the other says "there is a workable path". Do not use this rule for that case. Use the dispute table in section 3 of the main file.

You may reduce a severity in one case only: the route gives evidence after a re-check, for example "this passage is wording only and changes no refusal condition". The Author must not reduce the severity by "most routes judge it low". In the other direction, a route that judged high must withdraw its problem if it cannot give a concrete trigger condition. The Author does not withdraw it for that route. Give a business goal, more authorization, or a confirmed decision to the User. If a substantive dispute has no new evidence and no executable action, write it as open in the record. Do not dispatch the same dispute again.

For a re-review, give each route the new full snapshot, the merged problems, and the handling evidence. A scan route checks the full text and the effect of each change. A reused route checks the positions that the Closure Table cites, and their related preconditions. A route may reuse evidence for an unchanged part. It must confirm that the evidence still applies, and write the original version and the coverage. Each route then gives a conclusion for the current version. A reviewer must check the real handling result. Do not accept the "handled" claim of the Author. Do not forward an old pass conclusion.

A re-review output must hold the **Closure Table**. A reused route owns this table. For each old problem, give resolved, partly resolved, or unresolved, with the evidence position. A scan route that got no old problem writes "this route has no old problem". **A resolved problem with no evidence position counts as unresolved.** If a report says "fixed" and points to no rule, count the problem as open.
