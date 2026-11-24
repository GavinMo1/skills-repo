# Review Protocol: Snapshots, Records, and Tool Recovery

Read "Version and Snapshot" and "Dispatch Material" when you freeze a plan or dispatch a review. Read "Dispatch to Implementation" before the work starts. Read "Isolated Run of an Executable Precondition" when you check the runtime behavior of a script, a command, a tool, or a configuration. Read the related section when you audit, change an agent, or recover from a failure. The [main file](../SKILL.md) decides the route selection, the rounds, and the pass conditions.

## Version and Snapshot

Give the frozen text one version number, for example v1 or v2. Record the version and the round separately. An added route or a new agent does not create a new version.

Save the full text as a frozen copy, or put it in the dispatch message. Keep the state and the review record separate from the text. Do not require a special marker. Each route gets the same content in one round. If a dispatch message cites a shared file that an agent can edit, keep one more copy that no agent changes in that round. Do not overwrite the text before all results arrive.

A change to behavior, a constraint, a precondition, a step, or an acceptance item opens a new version. A layout change or a typo repair may state the difference only, and it must confirm that the technical meaning does not change. If the User changes the requirement in the middle, keep the reviewed version and put the new requirement into the next version. Do not mix the pass conclusions of two versions.

**Substantive Change**: a change to behavior, a constraint, a precondition, a step, or an acceptance item. Save a new version and re-review it. Check that the text equals the last reviewed version before delivery. A **Contract-Precision Revision** does not change the technical meaning: it removes an ambiguity, repairs a reference, makes a constant agree, or tightens an assertion. It still opens a new version and goes through the normal re-review. It has no fast path. Test: treat a change as a Substantive Change in two cases: it turns an existing red assertion to green; or it changes a default value, a threshold, or a refusal condition. Both kinds open a new version and recompute the hash.

**Round archive**: obey the project rule. A rule that gives a path and a line number (`AGENTS.md`, `README.md`, `docs/CONVENTIONS.md`, or an equivalent file) is the project rule. If no rule gives them, use the five rules in section 1 of the [main file](../SKILL.md), "File location": the directory, the two file names, the `archive/` directory, and the version position.

This section gives the version convention only: one version, one text, and the text does not change after the freeze.

The required fields of the two products are in section 1 of the [main file](../SKILL.md). This protocol does not repeat them.

## Audit Snapshot and Hash

Add a SHA256 when the review uses several files, an asynchronous handover, or an explicit audit. If the User forbids a file, use the full chat transcript and state that you made no file hash. Do not write a file to obey this protocol against the User.

For one file, you may separate the text from the record with two lines, one each: `<!-- plan:start -->` and `<!-- plan:end -->`. If you use the markers, each appears once and in the right order. Compute the hash of the text between the marker lines. Convert CRLF or CR to LF. Use UTF-8 without BOM. Do not remove white space. State the newline convention at the end of the record. Without markers, state the range that you hash. Do not reformat an existing file to fit this protocol.

For several files, record the relative path, the version, and the hash of each file. Use the same text convention. Give every route the same list and the same content. Record the raw evidence apart from the plan file. If the evidence or the environment changes, re-check the conclusions that depend on it.

A hash confirms the identity of the content. It does not prove that an agent read the plan, and it does not prove that the plan is correct. Do not keep only the version number and the hash.

## Isolated Run of an Executable Precondition

**Read this section when** a Core Precondition concerns the **runtime behavior** of a script, a command, a tool, or a configuration: the exit code, the written fields, a state transition, an error path, or a skipped branch. The test is one sentence: **can one command show it? If yes, run it. If no, mark "to verify" and write that one command.** A source anchor alone is not proof. An anchor proves "the code says this". It does not prove "the run goes this way". A static fact (structure, contract, meaning) needs no run.

### Build an isolated environment

1. Make a temporary directory (`mktemp -d`, `tempfile.mkdtemp()`, or the equivalent of your client). **Do not** run a write command in the directory of the object under review.
2. Copy the scripts of the object, with the smallest fixture that the run needs: an empty record, a sample configuration, a sample input. Keep the relative path structure, or the relative references of the script break.
3. Record the fingerprint of the original files: a SHA256 of each original script and each target directory that the run writes, or the output of `git status --porcelain`. Take the fingerprint again after the run. Only two equal values prove "the original files did not change".
4. Write a summary of the fixture in the record. A note such as "a hand-made v2 record" must let a reviewer judge the representativeness. Do not write "sample data" only.

### What to run, and what to record

- **One command for each precondition**, and the command must give a true or false answer. Do not run every subcommand to "see the whole picture".
- To cover a full path, use two batches. First run the read-only check commands: verify the state, list the failures. Then run the commands that write: register, freeze, advance the state. Record the exit code of each batch.
- **Four evidence items**. (1) The command text, ready to copy and run again. (2) The exit code. (3) The key output passage, cut to the lines that hold the mismatch. Do not write "success" or "normal". (4) The list of written field names, or the state difference. Example: "written fields: actors, files, next_action, reviews, revision_limit".
- If the last command runs a final check (for example `--final`), record its exit code and its failure list as they are. This is the key evidence of the judgment.

One table is enough:

| Precondition | Command | exit | Key output or written difference | Conclusion |
|---|---|---|---|---|
| 1: the check script finds a missing snapshot field | `python scripts/check-state.py --final` | 2 | `missing pass record for the current content`; `unchecked: [...]` | not met |
| 2: the register subcommand writes the actors field | `python scripts/state.py actor ...` | 0 | the written fields hold `actors` | proved |

### Judge and write back

- Write "not met" when the exit code is not 0, a field is missing, or the behavior differs from the precondition. State the difference in the note. **Do not write "partly met", "mostly holds", or "roughly usable".** Such wording sends a false precondition into the later steps.
- A false precondition has two exits, as in "Core Task and Core Preconditions" of the [main file](../SKILL.md): remove the dependency, or downgrade to a disclosed residual risk with a checkable acceptance item. Put the run evidence into the risk list. Do not use it to claim that the precondition still holds.
- Write the conclusion into the precondition item or the number of the Decision Table. The plan text cites the number and one summary sentence. Put the full command, the output, and the temporary path in the experiment area of the record.
- If you keep the temporary directory, write its path in the record so a reviewer can run it again. If you remove it, state the removal in the record.

### Actions that are not allowed

- Do not run a write or delete command inside the original skill or project directory. Do not change the sample data of the original directory "to check it".
- Do not replace a run with source reading. Do not treat "the code holds this if" as "the run takes this branch".
- Do not adjust the fixture, widen a threshold, or skip the final check to make a precondition true. Record the fixture and the parameters as they are.
- If you cannot isolate the run (real data, a production credential, an external network, an unrecoverable write), do not force it. Mark "to verify" and write the missing condition, the minimum command, and who verifies it by when.
- Do not extend one run result to a state that the fixture does not cover: concurrency, recovery after a failure, an old version. List each such state as its own precondition.

## Dispatch Material

Each route gets the material below, and checks it against its own duty.

```text
Goal: the User requirement, the hard constraints, the confirmed decisions and authorizations.
Duty: the check focus of this route.
Version: the round, the frozen version. Add a hash or a file list when it applies.
Plan: the full text, with the Core Task, the failure symptom, the start instructions, the steps, the no-go items, the acceptance items, the stop conditions, and the blind spot names.
Record (decision half): the Decision Table and the Choice List, the status and the anchor of each Core Precondition, the open items.
Record (review history): the Revision Table, the Closure Table, the version history, and the limits of each route. Give this half to a reused route only. Do not give it to a scan route. A scan route that gets it is not blind.
An agent reads the half that its duty needs. The Execution Agent reads the plan only and gets neither half. See "Dispatch to Implementation".
Raw material: the readable entry points of the requirement, the implementation, the configuration, and the documents.
Re-review material: for a reused route, the old problems, the change note, the handling evidence, and the effect scope. For a scan route, the change list and the change surface only. No old problems.
Output: the conclusion; the value of question 1 and question 2 for each open item (true or false), with the evidence position and the reading for each; the count of high, medium, and low problems as a summary; each problem with a stable ID, a severity, a position, a trigger condition, an effect, evidence, and a proposal; the handling of old problems as a Closure Table (resolved, partly resolved, or unresolved, with the evidence position), which is the duty of a reused route; "this route has no old problem" when a scan route got none; the unverified items, the open decisions, and the limits. This route does not judge a close, a pass, or a partial delivery. The Author judges them by section 4 of the main file, and this protocol does not repeat the tests. Do not copy an old conclusion as the conclusion of this round. You may reuse evidence for an unchanged part after stating the original version and the coverage. Do not repeat the detail of a closed item.
Boundary: read the plan and record only. Change no file. Run no proposed implementation. Dispatch no agent. Do not take the place of the User authorization.
```

Five hard requirements for a dispatch:

1. **Each route gets at least one directed question**, and a concrete input can express the question: "test this: if the target is busy, does the delivery fail?". A general "please review" finds much less. A directed question narrows the view, so use three at most. Write one sentence beside it: "report a new finding outside your duty too". A reused route follows the completion test in section 2 of the [main file](../SKILL.md). This sentence does not turn a reused route into a full scan.
2. **The re-review message to a scan route must say "read the frozen file again; do not use the version in your memory".** A reused route must also read the positions that the Closure Table cites. Do not work from memory. A review from memory misses a shifted rule number and a constant that no longer agrees. Only a full-text search finds them.
3. **A reused agent must not claim a blind review.** Its memory of the old version is exposed material. Write in the record: "this route is a reused reviewer and has seen the earlier versions".
4. Give the **change list and the change surface** before the full text. The change surface is the count that the Author reports; its format is in section 3 of the [main file](../SKILL.md). A reviewer still judges the crossing points itself.
5. **Each problem must give four evidence items**: (1) `file :: symbol`, where a line number is a hint only and moves between versions; (2) a passage from that symbol; (3) a **falsifiable condition**, written as "if you cannot find X in this symbol, this item is false"; (4) when the conclusion depends on a call, a reference, or a configuration relation, an anchor that shows the relation exists. Do not list every relation.

   The requirement depends on the severity. **A high or medium problem must give all four items.** The Author's check is fixed: "open that symbol, read the whole symbol, and check each relation anchor". A passage confirms the position only. **It does not replace the reading**: code next to a passage in the same file can reject the conclusion that the passage supports. **A low problem gives items 1 and 3 only.** The Author's check is "look whether the anchor points to the right place". A low problem does not block the implementation, so it needs no full reading and no relation anchor. Do not write every low problem into the Revision Table. A check may show that a low problem changes the implementation action. Treat it as a medium problem at once, and add items 2 and 4. **If the problem concerns runtime behavior (exit code, written field, state transition, error path), the anchor is not enough. Add the command of an isolated run and its exit code, and see "Isolated Run of an Executable Precondition". Without a run, mark the item "plan reasoning".**

Tier A of the Alternative route does one blind review at its first start. Give the material that the candidate direction needs, and no current plan. After the direction exists, add the common text and the open problems. Reuse the same reviewer to update the comparison. Do not explore from zero again. **Tier B and Tier C** hide nothing. Give the full text and the candidate list of that decision point.

## Re-Review and Evidence Reuse

Give each route the new full text and the change note. A scan route judges the effect of the change from the full text. A reused route judges it from the positions that the Closure Table cites. Neither route accepts the Author's judgment of the effect only.

For a changed part, check the new content, the related preconditions, the key steps, and the old problems. For an unchanged part, you may reuse evidence. State the original version, the coverage, and why the evidence still applies.

Each route gives a full conclusion for the current version. Do not copy an old count only. A first check that is not complete does not count as reused evidence. Do not narrow your duty to avoid a new problem inside the completion test of your route. The two completion tests are in section 2 of the [main file](../SKILL.md).

Keep a stable ID for each problem. Give the evidence when you close an old problem. Give a new problem a new ID. An open dispute about a fact or a severity needs three records: the evidence of both sides, the check that was run, and the evidence that is missing. Do not replace a solution with the decision of the Author, and do not ask for a new review again and again.

**A reviewer checks the completeness of the affected positions.** For each rule that this round changed, the Author gives the search command and every matching line. The pattern must hold the old wording and the action verb of that rule. The Author writes the disposition of each line: change, merge, delete, point to another file, or state that the text does not repeat it. Use one value for each line. Every line outside the list must have a disposition. A reviewer checks the completeness of the list with a third, adjacent pattern. The check of the Author is not enough. A Light level searches the directory of the changed file only.

## Minimum Record

Reuse the record area of the plan, or an existing project log. Do not make a second approval file. **The record is the only source of the decisions.** The plan cites a decision by number only. This record holds the full reason. The reader reads the parts it needs, not the whole file. The Author reads the conclusion, the rounds, the open items, and the implementation deviations. The User reads the conclusion, the level evidence, and the open items. The record holds:

- **Conclusion**: pass, partial delivery, or exit without convergence, with one sentence of reason.
- The current version, the finished rounds, and the round in progress; **the review level, the route count, and the reason for them**; the `delivery point` (`plan only` or `with implementation`, with the words of the User beside it); the hash or the file list when it applies. Record the review status and the implementation status separately.
- **The Decision Table**, with its appendix rows, and the Choice List as its derived view; the candidates of an alternative solution and the reason to reject each. This is the only home of "why we decided this". **The plan fails if it holds this material.** Move it back before delivery.

  The table holds three to five key decision points. Give each point a stable number (`Decision 1`, `Decision 2`, ...). The Evidence column holds two parts, separated by a semicolon: (1) the evidence itself, an anchor or a command with its exit code and the conclusion; (2) the property and the level, one of three values, written as one sentence:
  - `property: fact | destination: text, blind spot, one test, or a constant`
  - `property: preference | level: blocking or list`
  - `property: to verify | check: <what to run or where to read> | result: <the result>`

  A choice point may not meet the key definition, and still change the product. Put it in the table as an **appendix row** (`Appendix 1`, ...) with the same fields. It does not use one of the three to five places.

  **The Choice List is a derived view of the Decision Table.** Do not keep it as a second source. Sort the Evidence column into three groups. When the Decision Table changes, the list changes with it: **asked** `Decision N | you chose Y | rejected Z`; **default, not asked** `Decision N | chose X, rejected Y, did not ask, because <reason>`; **fact or to verify** `Decision N | chose X, rejected Y | not asked, property is fact or to verify, destination <text, blind spot, one test, or a constant>`. Add the result for an item to verify.
- **The evidence and the status of each Core Precondition**: an anchor or run evidence; the unverified list.
- **The four items of a known blind spot**: the name, why you do not handle it now, the cost, and the condition that must bring you back. The plan keeps the first and the last item only.
- **The level re-check of this round** (one line): the same level, or a new level. A new level must state three points. First, which criteria changed, and which route takes over the duty of each removed route. Second, whether the scan route is new this round, done by an existing route, or missing. Third, whether this round uses the "limit reached" exception (yes or no, once in the whole loop).
- The identity, the duty, and the status of each route (not started, in progress, finished, failed). Add the check coverage, the original version of the reused evidence, the limits, and the problem count.
- The stable problem IDs, the handling evidence, and the open items with their owner.
- **The run record**: which executable preconditions you tested in isolation; the command; the exit code; the key output; the fixture summary; the temporary path; the result of the before-and-after fingerprint check.
- **The change surface of this round**: report the three items of section 3 of the [main file](../SKILL.md): the decision points the change touches; the **new position list**, which rules now sit where the earlier version had nothing; the **deleted or merged list**, which rules. Keep the two lists apart. **Do not merge the counts and do not offset one with the other.** Write "deleted 0" when the count is zero, and state why only an addition can answer the finding. When the new positions are not zero, state why you cannot merge them into one position. Add two items: did you answer the new finding with a new rule, and how many mechanisms this round adds.
- **The unverified item list**: for each item, who found it, why you cannot verify it, and who verifies it by when. The handling value has three options only: to do during the implementation with its check steps, checked by the Author with the result, or still open with a recovery condition. Do not repeat an item unchanged from round to round.
- The next executable action, or the exit reason and the recovery condition.

The record often sits outside the hash boundary. Any claim that affects trust ("this ran", "the main repair came from the review") must hold checkable evidence. Without it, mark the claim "for reference only".

A change of route under the same goal does not reset the budget. When the User replaces the Core Task, record the new loop and its reason. Do not reset the round count by a change of name.

## Concurrency and Failure Recovery

Run the routes in parallel or in sequence, as the tools allow. If you have too few agents, save the finished problems first, then free a resource in the way that the client supports. If the client has no release call, continue the remaining routes in sequence, or report the limit. Do not skip a route. Do not write a sequential run as a parallel run.

When one route clearly fails, or a bounded wait shows no progress:

1. Check the real state first. A route that runs and makes progress is not a failure.
2. Add at most two recovery attempts for that route in that round. A new agent and a reconnect share this budget. Do not add a round.
3. Give the taking-over reviewer the original duty, the common snapshot, the finished checks, and the open items. That reviewer must not record the unchecked conclusion of another agent as a finished check.
4. If the recovery budget is used, or the environment cannot run the needed routes, save the result and exit as "review incomplete". An incomplete route is not a route with zero problems.

If you have no independent agent at all, use "no independent review is possible" in section 5 of the [main file](../SKILL.md). Write "no independent review", which is not a pass. Do not fake a review pass.

## Delivery Check

Check that the final text and the newest conclusion of each route belong to the same version. A layout or typo difference must be stated and must not change the technical meaning. In hash mode, check the text range, the list, and the hash again. A change must leave an update record. Do not claim that an old hash matches.

If a substantive change has no re-review, open the next round. If the budget is used, judge the delivery form by section 4 of the [main file](../SKILL.md). There are three delivery forms only: **pass, partial delivery, and exit without convergence**. The tests are in section 4 of the main file, and this protocol does not repeat them.

**The four values that count as an action** are in section 4 of the [main file](../SKILL.md), "Conditions that open no new round". This section judges the delivery form only.

## Dispatch to Implementation

When the work really starts after a pass, the implementation dispatch and the review dispatch are **two different things**. Do not mix them.

```text
Goal: what the User wants (one quoted line), and how far this authorization goes.
Plan: the full text of <prefix>-v<version>.md.
Boundary: do the plan. Come back and ask when a stop condition of the plan is true. Decide the rest yourself. Do not invent a specification.
```

Delete each item below before the dispatch. Keep none of them:

- the Review Record, the Closure Table, the Revision Table, the unverified list, the limits of each route;
- the review history and the version history, and any sentence of the form "this came in round N";
- the dispute record, a rejected candidate, the argument for a conclusion;
- the high, medium, and low counts, the round count, the route count, and the level;
- every sentence that starts with "because".

The test, in one sentence: **the plan text already holds the action and the test, so the dispatch message needs no reason.** If a reason appears in the message, that reason belongs in an action item of the plan, or the Execution Agent does not need it.

When the Execution Agent asks "why did we decide this", the Author takes the answer from the record and turns it into one sentence: "so do step N". **Do not send the history back and do not paste the record.** If the same question comes a third time, the action items or the no-go items of the plan are not good enough. Change the plan, not the dispatch wording.

If the tool cannot stop the Execution Agent from reading the record, write in the dispatch message: "the record content about the decision history is not your basis for a judgment", and state that it is exposed.

Write an implementation deviation into the record as section 5 of the [main file](../SKILL.md) says. If the deviation changes what the Execution Agent is doing, it is a new version of the plan. Deliver it again. Do not add a note to the old plan.
