---
name: plan-review-loop-en
description: "Writes a work plan for an agent to execute. Runs a loop of independent review, revision, and re-review. Gives two products: a work plan that an execution agent can start without more questions, and a review record for audit. Use it to write a plan, to design before you start work, or when an agent must review a plan."
---

# Plan Review Loop

The Author writes the plan, checks the review problems, and selects a solution within the authorization. An independent Reviewer Agent finds evidence, reports problems, and re-checks each change. A review does not replace user authorization.

## Terms

There are three roles.

- **Execution Agent**: does the work from the plan. Reads the plan only. Does not read the record.
- **User**: gives the authorization and accepts the result.
- **Author**: writes the plan, keeps the record, dispatches the reviews, and makes the decisions. The Author is the main session.

Do not write "person", "reader", or "implementer" in a rule. Write one of the three roles.

There are two products. Each product has one reader.

| | Work Plan | Review Record |
|---|---|---|
| Reader | Execution Agent | Author and User |
| Answers only | Where to start, in what order, how to judge each step, what not to touch, when to stop and ask | Why we decided this, what was reviewed, what is still open, what the conclusion is |
| Test | Delete this line. Will the Execution Agent do a wrong action? If no, move the line to the record. | Delete this line. Can you still answer "why did we decide this"? If no, add the line back. |

Use these five strength words only.

- **must**: a hard gate. If the rule is not obeyed, the round fails.
- **must not**: a prohibition.
- **should**: the default. You may deviate. Write the reason in the record.
- **may**: optional.
- **only**: the one permitted option.

Write an ordinary step as an imperative: "Read the record." Write a negative step as "Do not" plus the verb. A hard-gate sentence uses must or must not. Do not use another form of a requirement or a prohibition. A banned form is "have to", "need to", "shall", "ought to", "is required to", "make sure", or "always".

Keep a hard gate and a default in separate sentences. A hard-gate sentence gives the rule only. Put the reason, the history, and the words "why we decided this" in two places: the record, and the design notes. The record fields are in [Review Protocol](references/review-protocol.md) "Minimum Record". Do not put them in a hard-gate sentence.

Use one word for one concept. Keep "downgrade" for a Core Precondition only. For a severity, write "reduce the severity".

A change to a strength word is a Substantive Change. It opens a new version and a re-review.

Other terms:

- **Route**: one independent review duty. One agent does one route.
- **Reviewer**: the common name of one agent of one route. It is never the Author.
- **Must-change**: the status of an open item after its falsifiable test fires. The plan text must change before delivery.
- **Round**: all routes finish their review of one frozen version.
- **Level**: the review intensity: light, standard, or deep.
- **Tier**: the size of an alternative solution: A, B, or C.
- **Close**: stop the revisions for this round and go to delivery or a test. A close is not a pass.
- **Disclosed item**: a problem that was judged, that fails both gate questions, and that is still open.
- **Landing anchor**: the position that a step changes, written as `file :: symbol` plus one sentence that names the symbol where the decision happens. It lives in the plan.
- **Decision-evidence anchor**: the anchor behind a decision or behind a reported problem: the position, the passage, and the falsifiable condition. It lives in the record and in the report of a route. A landing anchor is not a decision-evidence anchor.

## Start

- If a plan or a record already exists, read both first. Check the goal, the scope, the constraints, and the confirmed decisions. Start work when the information is sufficient. Ask the User only when the missing information changes the plan.
- An instruction from the User about the number of reviewers, the severity levels, the rounds, or the exit condition has priority. If the User names a formal domain process, use its duties and its checks. Do not add a second approval process.
- Select the review level by the cost of a wrong action. Do not select it by the size of the plan. Write the reason in the record.

| Level | Criterion | Routes |
|---|---|---|
| **Light** | All four are true: (1) the change is reversible, and a wrong result can be reverted directly; (2) the change touches no user-visible data, no external behavior, and no published contract; (3) there is no migration, no cutover, and no new dependency; (4) there is no decision point that changes all later steps. | One route: Adversarial |
| **Standard** | The change is reversible and stays in one file or one module. It changes no user-visible behavior. It has no migration and no cutover. It has at least one key decision point. | Two routes: Goal and Implementation, and Adversarial |
| **Deep** | The change touches a shared interface, a data migration, a cutover with a rollback, an irreversible action, or more than one person. | Three routes: Goal and Implementation, Operation and Evolution, and Adversarial |

- For a Light level, write the evidence for each of the four criteria. If one criterion fails, or if you cannot write the evidence, or if you cannot estimate the cost, use Standard. When the User fixes a single route, write the evidence for all four criteria.
- The level selects the number of routes only. The Decision Table, the unverified list, and the Blind Spot List must go into the record. They use no plan space. A Light level needs no exemption from them.
- To change the level, write which tests changed. Also name the route that takes over the duties of each removed route. Record both an increase and a decrease.
- Do not reduce the number of routes when the four Light tests fail.
- Write route names as words. Do not write A, B, or C for a route. Letters clash with the Tier A, B, and C of alternative solutions.
- A Light level has one route from the start. That route may do the scan and the Closure Table check. Write "this route does both; independence is dropped" in the record.

Budget: ten rounds maximum for all levels. If the User gives a smaller number, use it. Do not reset the count after a change of agent, an added route, a new solution, or a resumed run.

### Which file to read, and when

| File | Read it when | How much to read | Cost of a wrong read |
|---|---|---|---|
| [Multi-Route Review](references/multi-route-review.md) | You divide the duties. You combine the problems. | Read all of it. | Overlapping duties. A vote count instead of a judgment. |
| [Review Protocol](references/review-protocol.md) | You freeze or archive a version. You dispatch. You write a record field. You have a dispute. You decide to stop. You audit. You recover from a failure. You test a runtime precondition. | Read the section the trigger names, to the end. | A wrong snapshot. A re-review from memory. A missing record field. The record goes to the Execution Agent. |
| [Adversarial Route](references/adversarial-review.md) | Before you dispatch the Adversarial route. The Author and the route agent both read it. | Read all of it. | A risk list with no counterexample. |
| [Alternative Route](references/alternative-review.md) | You start any tier of an alternative solution. You count the routes for a round. | Read all of it. | Candidates you cannot compare. A wrong round count. |
| [Review Checklists](references/review-checklists.md) | You write a guard, a cleanup table, an acceptance assertion, or a Revision Table. The Adversarial route reads section A each round. | Read the section you hit, to the end. | An assertion that checks the exit code only. A table with the wrong row count. |
| [Design Notes](references/loop-design.md) | You change a rule of this skill, or you delete a rule. | Read all of it. | You delete a defense that an earlier failure built. |

A daily review does not read the full checklists or the design notes. When you reach a section, read that section to the end. Do not use one sentence from it.

## Core Task and Core Preconditions

**Core Task**: the result the User must get.
**Core Precondition**: a condition that the result needs. If the condition is false, a correct step still does not give the result.

Split the two by reader.

- The **plan** gives the Core Task, the failure symptom of the Core Task, and one stop-and-ask action for a false precondition.
- The **record** gives the evidence, the status, and the property of each precondition.

A precondition has one of three statuses: **proved**, **to verify**, or **not met**. For a proved precondition, give an anchor `file :: symbol` and one falsifiable condition: "if you cannot find X in this symbol, this item is false". For the other statements, write the evidence class only. Do not anchor every statement. Do not write every step or every quality preference as a precondition.

Separate the necessary condition of the goal from a condition of the current solution. An alternative solution can remove the second one. It cannot lower the first one.

A false Core Precondition has two exits. Do not pass it without one of them.

- **Remove the dependency**: use a solution that does not need the precondition.
- **Downgrade to a disclosed residual risk**: use this exit only when the goal cannot meet the precondition. The upstream meaning or the confirmed scope of the User decides this. Give three items: the reason it cannot be met, the mitigation, and an acceptance item that shows the mitigation works. Write them into the risk list of the record. Do not claim that the precondition is true. Do not write it as "partly met".

A reviewer must not ask again for a precondition that was downgraded correctly. The Author must not use a downgrade to avoid a dependency that can be removed.

## Rounds and Alternative Solutions

One route uses one agent. Different routes use different agents. The Author's own review is not an independent route. Stop when the pass conditions are true. Ten rounds is a ceiling, not a target.

An alternative solution has three tiers, selected by the size of the change. Do not use one switch ("do we add a route?") for all three.

| Tier | Start it when | Cost |
|---|---|---|
| **A: change the approach** | The evidence shows that a Core Precondition of the current solution is false. Or the current solution has no executable repair, but another mechanism can meet the goal. | High: one blind review at the start |
| **B: change one component** | Any round. In particular, when one decision point was repaired two or more times and is still unstable. | Low: give the candidates and the conditions that reject them |
| **C: do less, or do nothing** | Ask once at the first dispatch. Then use it as needed. | Very low |

- Select the tier by the size of the change, not by the pass state of the plan. Start Tier A at once when its trigger is true. Otherwise, each round the Author asks: "does the dispute stay in one decision point?" If yes, start Tier B and write the reason in the record.
- If a necessary condition of the goal needs a User decision or external evidence, do not force an alternative solution around it. Deliver a blocked status.
- Which tier uses a route, which tier uses a round, and what to do when the User fixes the route count: see [Alternative Route](references/alternative-review.md) "Rounds and Route Accounting".
- An added route after a round counts in the next round. If a route fails, the new route of the next round takes over its duties. Write that round as incomplete. Do not write a failed route as "no problems".

## 1. Write and Freeze the Plan

Check the request, the current implementation, and the existing mechanisms. Separate proved facts, unverified assumptions, and intended behavior. Write two products at the same time: the plan for the Execution Agent and the record for the Author and the User. Before you write a line, ask which side it belongs to:

> Will the Execution Agent do a wrong action if this line is absent? Yes: the plan. No: the record.

### Plan items, in this order

1. **What the User wants**: one line quoted from the User. Use it to set the scope.
2. **Core Task and failure symptom**: the symptom that shows the Core Task is not met.
3. **Start instructions**: the first step; the order of the later steps; the completion test of each step; and, for each step, whether being stuck means stop and ask, or continue by default.
4. **Steps**: the location to change or reuse, the action, and the handling of compatibility and failure. Give the location as a **landing anchor**, in two parts: `file :: symbol`, and one sentence that names the symbol where the decision happens, with the call-chain line that shows the relation. **A name that exists is not a landing point.** A step that says "change `onInbound`" passes a search for `onInbound`, and the decision can sit in `route`. The sentence that names the deciding symbol is the part a reviewer can check.
5. **No-go items**: the locked constraints and the confirmed decisions of the User. Cite the number (`Decision 3`).
6. **Acceptance**: a table of assertions that an agent can run.
7. **When to stop and ask**: a false precondition, a scope beyond the authorization, and an open dispute.
8. **Blind Spot List**: write the name of the blind spot and the condition that must bring you back.

The plan holds no decision-evidence anchors, no property judgments, no review history, no dispute record, no problem count, no Choice List, and no version history. A landing anchor is not a decision-evidence anchor: the plan holds the landing anchor, and the record holds the evidence behind that decision. The first line of the plan gives the version number and one sentence: "This plan is self-contained. The implementation does not read the review record."

**File location**: if the project has a disk rule that gives a path and a line number, obey that rule. The rule may sit in `AGENTS.md`, `README.md`, `docs/CONVENTIONS.md`, or an equivalent file. If the project has no such rule, use these five rules.

- Put the files in `plans/<short-topic>/`. Use lower case and hyphens in the directory name. Fix the file prefix the first time you set it in that directory. The default prefix is the short topic name.
- **Two files for each version**: `<prefix>-v<version>.md` for the Work Plan (reader: the Execution Agent), and `<prefix>-v<version>-record.md` for the Review Record (reader: the Author and the User). Write one record for each version, and do not change it after you write it.
- The `archive/` directory holds the text of each earlier version. **Move the previous version into it as soon as you write a new version.**
- Write the version number in the text. Give the record the name of the version that produced it. Write the reviewed version in the first line of the record title. **A file name used as a version number goes one version out of step.**
- If the User forbids a file, or wants a chat transcript only, this section does not apply. Use "Three simplifications" in section 5.

Do not make a second rule in the plan.

### Record items

The record is the only source of the decisions. The plan cites a decision by number only. The sections and the minimum fields are in [Review Protocol](references/review-protocol.md) "Minimum Record". This section gives what the record must answer.

1. **Conclusion**: pass, partial delivery, or exit without convergence. Add one sentence with the reason.
2. **Why we decided this**: the Decision Table. Use three to five key decision points: a wrong choice here changes all later steps. Give each point a stable number (`Decision 1`, `Decision 2`, ...). Four columns:

| No. | Selected implementation | Evidence | What would reject it, or the alternative |
|---|---|---|---|
| Decision 1 | ... | ... | ... |

The Evidence column has two parts, separated by a semicolon.

- Part 1: the evidence itself: an anchor, or a command with its exit code and the conclusion.
- Part 2: the property and its grade, as one full sentence: fact, preference, or to verify.

The templates, the appendix rows, and the Choice List as a derived view are in [Review Protocol](references/review-protocol.md) "Minimum Record".

The Decision Table and the rejected candidates are the only home of "why we decided this". The plan holds neither.

**How to judge a property**: if one command, one search, or one symbol read gives the answer, the property is a fact. Run it now. Do not leave it as a to-do item.

If you cannot get the answer and later steps need it, the property is a blocking preference. Stop and ask the User. Give two concrete options and a default. For all other items, use the default, and report it in the Choice List at delivery. If you cannot decide, try the command first. If you still cannot decide, use the blocking grade.

These items are "hard to verify": an irreversible action, a User authorization, an external account, or a wait of one day or more. Put them in the unverified list with a recovery condition. Do not write an unverified fact as a constant.

If a decision deserves a User question and you do not ask it, write the reason in the table, not in the plan.

3. **What is still open**: the disclosed items and the open items at the stop. For each item, give the reason not to change it, one falsifiable test, and a recovery condition.

Do not read the full record. The Author reads the conclusion, the rounds, the open items, and the implementation deviations. The User reads the conclusion, the level evidence, and the open items. See [Review Protocol](references/review-protocol.md) "Minimum Record".

### Preconditions and versions

Record the plan status and the implementation status separately. The snapshot is the full text of the round: the plan and the record. Do not change it before all results arrive. Write the snapshot scope in the first line of the record. The definitions of **Substantive Change** and **Contract-Precision Revision**, the new version, and the re-review are in [Review Protocol](references/review-protocol.md) "Version and Snapshot".

**Do not enlarge a blind spot**: if a tool command can clear the condition, do not write it as unclear. A written "unclear" makes the Execution Agent abandon a path it can use. Write a blind spot only when no tool can clear it. Write why in the record. If a person must repair the item, give a traceable placeholder such as `unknown-<source>-<date>`, and write "not verified" in the plan. Do not invent a value that looks real. A blind spot is not a new rule. "I do not know this" is always cheaper than "add one more mechanism". This holds only when the gap does not make the Execution Agent do a wrong action. If it does, treat the item as a medium problem.

### Acceptance assertions

Write each acceptance item as one line that an agent can run. The table must have four columns:

| Recipe (the operation sequence) | Where the state and the input come from | Expected exit code | Expected output message set |
|---|---|---|---|

The second column gives one of three values: **production path**, **hand-made fixture**, or **real machine**. Two sentences decide the value, and they are not one sentence.

- **A state that the assertion verifies is written by the production path.** A fixture that hand-writes that state moves the test to a path the product does not take. The cell then names the producer as `file :: symbol`, in the form a landing anchor uses.
- **An illegal or boundary input is hand-made.** The fail-open guard, the collapse of "absent" and "null", and the falsy merge have no legal producer. A fixture is the only way to build their input. The cell then names the fixture or the script that builds it.
- **A cell that names neither counts as hand-made.** A claim of the production path with no producer is a claim that no search can check.

Make one test here: **an assertion that checks the exit code only is not acceptable**. Two different causes often give the same code. Give the message set, or a measurement that separates the two causes. The other five rules are in [Review Checklists](references/review-checklists.md) "Acceptance Assertions": the message count, the source of the state and the input, the existence of the cited test cases, the content markers of a diff assertion, and the coverage self-check. For where an inserted guard lands, and its exemption, see section A4 of the same file. Read that section to the end when you write an assertion.

## 2. Dispatch the Independent Review

A reviewer reads the full plan, plus the decision half of the record: the Decision Table and the Choice List, the evidence and the status of each Core Precondition, and the open items. The other half of the record is the review history: the Revision Table, the Closure Table, the version history, and the limits of each route. Give the second half to a reused route only. Do not give it to a scan route. A scan route that reads it inherits the conclusions of other routes. The Execution Agent reads the plan only. Do not give it either half.

**Minimum setup for each round**: one reviewer that has not seen an earlier version does a full scan for new problems. It reads the full text and reports new problems. Each reused route checks the Closure Table only. It reads the plan text to check the cited positions. It does not do a full scan. The completion test of a scan route is the full text. The completion test of a reused route is every position that the Closure Table cites, including the rows whose status is resolved. The test for reuse or a new agent, and the handling of a round where no route can be reused, is in [Multi-Route Review](references/multi-route-review.md). The completion test of a reused route lives in two places, here and there: change both together. Replacing a test with a pointer once lost two tests.

**The dispatch message decides the independence, not the change of agent.** Put these items in the message: the goal, the constraints, the entry point of the material, the duty of the route, the frozen text, and the Core Preconditions with their evidence. Leave out these items: the review history, the Author's account of the problems, and the current conclusions of other routes. Delete every sentence of the form "after we discussed it, we decided". If a tool cannot isolate the context, state which material is exposed. This rule covers the first dispatch and the scan route of each round. A reused route always holds old problems.

**A reviewer does three things**: report a problem with evidence, give the two gate values of each open item, and state the check scope and the limits. The Author makes every close, pass, and partial-delivery decision. A reviewer does not produce a "can we close" conclusion.

### Failure modes to test each round

Each route must build an input and test the three code patterns below. Do not wait for the Author to list a suspect.

| Failure mode | One test |
|---|---|
| Fail-open guard | Put the illegal input in. Does the guard refuse it or let it pass? A pass is a problem. |
| Existence and null collapse | Record "absent" and "content is null" as two states. Assert each state. |
| Falsy merge that loses data | An empty container is also falsy. Test the read path and the write path separately. |

The code samples, the requirement for each mode, and two documentation rules (the row count is not the item count; an unclear scope grows too large) are in [Review Checklists](references/review-checklists.md) section A and section B. A scan route reads section A to the end each round. Other routes read it as needed.

A scan route states an explicit result for each item above each round. Other routes may check the changed surface only. Report a problem as soon as you see it.

The five hard requirements for a dispatch are in [Review Protocol](references/review-protocol.md) "Dispatch Material": a directed question; no re-review from memory; no blind-review claim by a reused reviewer; the changed surface before the full text; the four evidence items graded by severity.

A reviewer output has: the conclusion; the count of high, medium, and low problems, as a summary only; each problem with a stable ID and its evidence; the check scope and the limits. A reviewer reads the plan and the record only. It changes no file, runs no proposed implementation, dispatches no agent, and approves no release for the User.

A problem has one of three severities.

- **High**: the main direction cannot work, the plan clearly violates the goal or the authorization, or the plan can cause severe damage.
- **Medium**: the plan leads to a wrong implementation, breaks a key compatibility, or cannot be accepted, and the gap is concrete.
- **Low**: a clarity or maintenance suggestion that does not prevent a correct implementation.

Report only a problem with evidence. No count is required. If a reviewer needs a command but has no tool, list the command and its purpose. The Author runs it only inside the existing authorization and returns the raw result.

## 3. Verify, Revise, and Re-Review

Check the evidence of each **high** and **medium** problem. A **low** problem does not need an item-by-item evidence check. You may move a low problem to the blind spot or the Choice List. A low problem that you move there decides nothing. A problem that trips a gate changes the full plan: change the steps and the acceptance items. If both gate questions are false, register the item as a disclosed item in section 4. Do not change the plan text. When you merge duplicate problems, keep the source and the new evidence of each route. Do not ignore a problem that only one route reported.

For each revision, decide the side first. A change to an action, an order, a test, or a no-go item changes the plan. A change to "why we decided this", or new evidence, changes the record.

### Closure Table (in the record)

Write one row for each open item. Record how it was resolved.

| Problem ID | Source route | Status | Evidence position | Next step |
|---|---|---|---|---|
| R1F-02 | Adversarial | Resolved | Section 3, "three-state guard", item 2 | - |
| R2G-01 | Goal and Implementation | Open | - | Decision 4 decides again |

A status has three values: **resolved**, **partly resolved**, or **unresolved**. For "partly resolved", write what is still missing. The Evidence position of a resolved item must point to a named position in the plan text. If it does not, count the item as open. The whole work of a reused route is to check the positions that this table cites.

### Revision Table (in the record)

Each round, compress the problems into one table, one row each.

| Source | Revision | Changes the implementation action? |
|---|---|---|
| R1F-02 | The state-entry guard becomes three tests: exists, content, version. Section 4 adds an `__init__` item. | Yes (mechanism) |
| R2F-03 | The cleanup table adds one row, "the current content has no pass record", and merges it with an equivalent neighbor. | No (wording) |

What each column holds is in [Review Checklists](references/review-checklists.md) section D: the route name and the stable ID, the landing position of the revision, and the boundary of the two values. **If every row is "No", the round has no action.** If you cannot decide, write "Yes".

### Disputes (the process goes into the record, the conclusion into the plan)

Do not use a vote count. Do not use the higher severity.

| Case | Action |
|---|---|
| A dispute about a fact or a severity | Give the raw evidence. Ask the reporter to re-check. If the evidence is short or the dispute is substantive, keep the item open. Do not reduce the severity yourself. Do not delete the problem. |
| A preference that meets the existing constraints | The Author selects it inside the authorization and gives the reason. A better alternative does not make the current plan problemive. |
| Two routes give opposite conclusions | Each route gives one testable minimum check: one command, one input, or one symbol to read. The Author runs it once and returns the raw result to both routes. If they still disagree, keep the item open and list it in the delivery. |
| A business goal, more authorization, or a reversal of a User decision | List the options and the effects. Give them to the User. Continue the work that does not depend on the decision. |

After each substantive change, give the new full text and the change note to every route. A scan route reads the full text again. A reused route checks the positions that the Closure Table cites.

**Report the change surface in three items, each with its list. Do not merge the counts.** Write them into the record.

1. Which decision points the change touches.
2. Which positions are new this round: the rules that now sit where the earlier version had nothing.
3. Which rules this round deleted or merged.

If the deleted count is zero, write "deleted 0" and state why only an addition can answer the finding. If the new positions are not zero, state why you cannot merge them into one position.

Before you decide where a new finding goes, ask two questions. **Can one command test it? Is a failure single or catastrophic?**

| Can you test it? | Failure count and severity | Destination |
|---|---|---|
| No (authorization, meaning, data model) | Many, or one catastrophic | Write it in the plan text |
| No | Single, not catastrophic | One line in the Blind Spot List. The plan gives the name; the record gives the reason. |
| Yes | Any | Write **one test**: which input or state fails, plus one fallback action. Write no mechanism. |
| Yes, and you know the answer | - | Write a constant or a default. Do not discuss it. |

This table is the main control against growth. Almost every finding that "looks like it belongs in the plan" becomes one test, one constant, or one blind spot. It does not become a new rule.

**Two hard lines**

- **Do not answer a new finding with a new rule.** The test is the content, not a count: if you delete the rule, will the Execution Agent make a wrong decision? If no, do not add it. If two rules say the same thing, merge them before you change them. When a finding asks to "add X", first answer: **why is X missing here?** If a deletable item caused the gap, delete that item first. The gap disappears and you do not add X. Deleting the cause changes the plan text. Open a round for it. Do not count it as handled this round.
- **Add at most one mechanism per round.** A mechanism needs a new state, a new parameter, a new dependency, or a new order. A plain action step is not a mechanism. If one round adds more than two action steps, merge them first.

If the plan crosses a hard line, delete or merge first. Do not write "watch this next round".

**A reviewer checks the completeness of the affected positions.** The Author gives the search command and all matching lines, and writes the disposition of each line. The completeness of the list is checked by the reviewer with a third, adjacent pattern. The Author's own check is not sufficient. The search pattern and the allowed dispositions are in [Review Protocol](references/review-protocol.md) "Re-Review and Evidence Reuse".

Evidence for an unchanged part may be reused. Check that it still applies. Write the original version and the coverage. A forwarded "pass" is not a re-review of the current version. The related routes must widen the check in two cases: the change touches more than one module; or it changes a Core Precondition and the technical approach together. They must also handle each new high or medium problem. A reviewer must check the real change. Do not accept a "fixed" claim.

Write the record of each round as in [Review Protocol](references/review-protocol.md) "Minimum Record". If the User interrupts the work, or the context is restored, continue from the record and the real state of each agent. Do not dispatch the same route again.

## 4. Decide: Continue, Pass, Partial Delivery, or Exit

**Pass = the plan is ready to start (gate 1 and gate 2) AND the record is auditable (gate 3).** The two groups serve different readers. Do not convert one into the other. A correct plan with a record that cannot answer "why we decided this" is not a pass. A complete record with a plan that leads the Execution Agent to a wrong action is not a pass. If one group fails, continue the revisions.

### Gate 1: the plan is ready to start (for the Execution Agent)

Use the plan text only. Can an Execution Agent that took no part in the review answer these three questions? **A number with no answer counts as not answered.** If one question has no answer, stop the check.

1. **Where do I start, and in what order?** The first step, and the dependency order of the later steps.
2. **How do I judge each step?** The observable result that shows the step is correct: the command output, the written field, or the error text.
3. **What must I not touch, and when must I stop?** The locked constraints. The precondition that is false, the action without authorization, or the open dispute that must stop the work. The agent must not invent a specification.

Write one direct answer for each question that a reader can understand alone, and point to a named position in the plan: a step number, a section title, or a decision number. A position such as "as needed" or "it depends" counts as not answered.

### Gate 2: the gate test

No open item passes either question below.

- **Question 1**: does the current text make the Execution Agent do an action that is opposite to a written rule? These conditions also make the question true:
  - The action breaks a key compatibility, or the result cannot be accepted.
  - The agent must invent a specification.
  - **The scope of the changed object (skill, interface, or published contract) changes without a User confirmation.**
- **Question 2**: can the Core Task stay unimplemented, with no error and no red acceptance item? The question is also true when the Core Task clearly fails and an error appears. The phrase "no error and no red acceptance item" makes the case worse. It is not part of the test.
  - If the Core Task itself gives no symptom that shows failure, count the question as true. An unclear Core Task is a problem.
  - **Read only the line that the plan itself contains.** If the note holds the words of the User, split them into clauses of "what is wanted". Ask for each clause: does the Core Task cover it? One missing clause makes the question true. A sentence that gives no requirement (greeting, exclamation, complaint without effect) does not count. State why it does not count. **If the note has no words of the User, judge by one point only: does the Core Task give an observable failure symptom?**

**Who gives the values**: the route that reports a new item gives values for questions 1 and 2 in the same output. A reused route gives the values of the old items. The scan route of the round gives the values of the Author's own items. If the reporting route failed or is new, the taking-over route gives the values and writes "self-judged; the original route is lost". If two routes disagree, use the dispute table in section 3. That conclusion also counts as a value. If the case is a business goal, or a reversal of a User decision, give it to the User. Keep the item open until the answer arrives. **A missing value, or a value that does not show "both questions are false", is not a judgment.**

### Gate 3: the record is auditable (for the Author and the User)

- **Evidence complete**: each row of the Decision Table has the Evidence parts of section 1 and a property, or a checkable anchor. If it has neither, the row is not complete.
- **Each open item is judgeable**: each disclosed item, and each item open at the stop, has two parts: a **reason not to change it**, and **one falsifiable test**. The test reads "if X occurs, this item changes to must-change". If the second part is missing, count the item as must-change. With a reason only, "I found nothing" takes the place of "it is false".
- **The two products agree**: each `Decision N` in the plan has a row in the Decision Table. The sentence that the plan derives from that decision agrees with the "Selected implementation" of the row. If a number has no row, or the two texts disagree, the plan fails and the round does not pass.

**Conditions that open no new round**

- **Ten rounds are used.** If the User gave a smaller number, use that number. **Exception**: at the limit, open one more round in three conditions. Gate 1 is true. Gate 2 has exactly one failing item. That item needs three or fewer edit points. List the edit points and write them in the record before the round. The round counts in the budget. **Use this exception once in the whole loop.** Mark it after you use it.
- **The round has no executable action.** Judge the effect, not the action. Four values count as an action. (1) A value changes from "cannot judge" to a certain value: one symbol read, one command run, or one document section read counts. (2) A position, an anchor, or an acceptance check that failed before now passes: "I added it" does not count, and you must show the earlier failure and the current pass. (3) The cause of a gap is deleted. (4) The handling requirement of a must-change item is met, and you can show the text before and after. **A change of wording is not an action.** "Waiting for a User decision" is no action. The blocking grade of that item only decides whether the delivery form says "blocked" or "no convergence".

**Complete the small items before you stop.** If one command, one search, one symbol read, one document section, or one check conclusion can settle an item, do it. It opens no round. Then decide.

When you open no more rounds, write each open item into the record under "open items at the stop". Give the reason it is still open and the recovery condition. In the plan, write only which scopes cannot start and which acceptance items you cannot judge.

**Three delivery forms**

- **Pass**: both groups of gate tests are true. A pass means only this: inside the checked scope and the current evidence, no open problem prevents the start. It does not prove completeness. It does not prove that the implementation, the test, or the release is finished. Do not declare a pass by a vote count or an average score.
- **Partial delivery**: the two groups cannot both be true for the whole plan. One part of the plan can still meet both alone, and it does not depend on an open item. Split the plan into "ready to start" and "held by open items". For each held item, write the failed gate, the problem, or the unverified item. Write the recovery condition in the record: who does what, and what result lets the part join the delivery. The start instructions of the ready part must be complete and must hold no unstated assumption. If you cannot do this, exit the whole plan without convergence. Partial delivery is a delivery form, not a pass, and it uses no round.
- **Exit without convergence**: you cannot split out such a part. Write the reason: blocked, budget used, or review incomplete. Write the recovery condition in the record. **Do not write the exit as a pass.**

Show the high, medium, and low counts as a summary only. They do not decide a continuation or a close. Do not open a round to drive a count to zero.

**A candidate solution does not block a pass.** Write each accepted or rejected candidate and the reason into the Decision Table. A candidate with no record counts as not handled. Exception: a candidate that shows "the current plan would be wasted work" is a problem. A Tier A candidate that shows a false Core Precondition is the usual case. The Author may block the pass. For an accepted candidate, check the conditions its implementation needs.

## 5. Delivery and Later Authorization

Deliver two products. The first is the **Work Plan** for the Execution Agent. It should become shorter. The second is the **Review Record** for the Author and the User. Write one record for each version, and do not change it after you write it.

Each line of the plan must answer "what does the Execution Agent do with it?". Move every line that cannot answer this into the record. **This is the only test of "shorter". Do not use a word count.**

Keep one copy of the conclusion and the counts, in the record. The plan text holds no high, medium, or low count, no round count, and no route count.

### Context isolation at implementation dispatch

When the work really starts after delivery, give the Execution Agent the **plan text only**, plus the necessary goal and authorization limits. Do not give any of these items: the record, the review history, the dispute record, the counts, the rejected candidates, or the version history. Read [Review Protocol](references/review-protocol.md) "Dispatch to Implementation" for the message format. That section also gives the items to delete, and the answer to "why did we decide this". That section also gives the test: the plan already holds the action, so the message needs no reason.

### After a pass

A task of the form "write a plan first" ends here. The `delivery point` must quote the words of the original User task next to it. If you cannot point to those words, treat the task as "plan only" and wait for one word of release from the User. If the task declares `with implementation` and the original task already gave the authorization, continue after the pass. Add no confirmation step. A partial delivery may start the "ready to start" part inside the original authorization and continue the held part. An exit without convergence does not start the implementation. A commit, an external write, and a release obey the existing authorization limits.

During the implementation, a deviation from the reviewed text has two cases. If it touches a Core Precondition or the technical approach, save a new version and open a round. For the other deviations (a step detail, a local order, an equivalent replacement), change the text in place and add one line to the record: "implementation deviation: what changed, why, and which acceptance items it affects". Give it to one route to check. Do not use "we found this during implementation" to bypass a reviewed constraint. Do not open a full round for each implementation detail.

### Three simplifications

- If the User forbids a file, or wants a chat transcript only, put both products at the end of the transcript under two headings. The `archive/` rule does not apply. All other tests stay.
- A Light-level plan may compress the record into three lines: conclusion; decisions with evidence; open items. The plan side still has all eight items. Do not shorten it for a Light level.
- Partial-delivery admission uses gate 1 only. Do not lower it for a Light level or a tight budget.

**If no independent review is possible** (no sub-agent, or the tools do not work): use the "single route self-check with a clear mark of no independent review" only. Write "no independent review" in the first line of the record conclusion. Such a review is not a pass. Judge the delivery form as partial delivery or exit without convergence. Do not write a self-check as a pass. Do not claim an independent review.
