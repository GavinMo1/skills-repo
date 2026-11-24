# Design Notes: Reasons, History, and Deleted Rules

**This file is not a runtime instruction.** Read it in two cases only: you change a rule, or you delete a rule. The reasons are here. The rules are in the [main file](../SKILL.md). If the two disagree, the main file wins, and you update this file.

## The Failure That Each Hard Rule Prevents

Before you change a rule, check whether the failure it prevents still occurs. "It looks verbose" is not a reason to delete it.

**Rules with a real anchor**. Read the anchor column before you delete one.

| Rule | Failure prevented | Anchor |
|---|---|---|
| The routing table for a new finding: testable or not, and how many failures | Every new finding becomes a new paragraph, and the plan becomes impossible to implement | The change of this skill itself: the plan grew from 11,784 bytes to 29,768 bytes, and 17 versions only added text |
| The Author does not enumerate the consistency conclusions | The Author lists only the cases it thought of, and a new problem usually sits at the boundary between two rules | Two real problems out of eight implementation deviations came from the reviewer: the Choice List written twice, and the round archive that contradicted itself. The Author's own check found neither. |
| The change surface reports new positions and deleted or merged rules, with no offset between the counts | One rule spreads to N places and each place changes on its own. A count of rules does not show it, and two counts offset each other do not show it either. | The "three capacity items" of `user-profile-repo` v1.0 sat in three places |
| A fixed budget of ten rounds, the same for all levels | "Count it against the round limit" gave no number, so the person at that step invented one, and nobody checked it | Before the change, the main file cited the limit in four places and gave no digit. The User set ten rounds on the spot. |
| Two products by reader: the plan holds actions and tests, the record holds reasons and history | The decision history fills the context of the Execution Agent. In the other direction, the record grows into a file that nobody reads. | The User said on 2026-11-24 that the earlier goal named "the User" as the reader |

**Rules with an inference only**. Each one is a **deletion candidate, not a reason to keep it**.

| Rule | Failure prevented |
|---|---|
| An anchor and a falsifiable condition for a Core Precondition | "It looks supported" instead of support. A passage supports a conclusion that the full text rejects. |
| Run an executable precondition in an isolated directory | Reading the source and inferring "the script runs this way", when the run takes another branch |
| The Blind Spot List, and the rule that a blind spot is not a new rule | The Author cannot say "I do not know this", so the deletions never stop |
| The Closure Table with a position evidence | The Author forwards "fixed" and points to no rule |
| No pass by vote count or average score | "Most routes judged it low" hides a real problem, and the cheapest close becomes the default |
| A minimum check when two routes disagree | A disagreement about feasibility is treated as a disagreement about severity, and "use the higher" closes it |
| The dispatch message defines the blindness | A new agent is called a blind review, and the independent review becomes a second echo |
| One full scan route each round | Every route re-reads everything, the cost separates from the value, and "was the full check really done" is not observable |
| Three levels, with the four Light criteria written down | A three-line change starts a table and two routes, and the cost is high enough that people avoid the review |
| Partial delivery | A plan that is 80 percent ready is returned whole, and the User gets no usable part |
| Run a to-verify fact by default instead of parking it on a list | A fact that one command can show becomes a question for the User. The User cannot answer, and the same wrong conclusion returns. |
| Three tiers for an alternative solution | One switch, "add a route or not", handles three sizes of change |

**How to use the anchor column**: write an anchor when you have a case. Write "inference" when you have none. Do not invent a case to fill the column. A rule marked "inference" is a deletion candidate: if it stops a real failure once, come back and add the anchor. If no anchor arrives, delete that rule the next time you change this file. Do not invent a failure for it. **Exception for a new rule**: a rule that is new and has not met a real use gets the mark "inference (new, not observed yet)". Give it one chance first.

## History: 2026-11-24

The table keeps the points that someone could change back by mistake.

| Change | Why the earlier form was not worth it |
|---|---|
| The pass test went from six lists to two groups: the plan is ready to start (three questions and a gate), and the record is auditable | Process lists became the pass test, and "the tables exist" took the place of "the work can start" |
| Six tables each round became the Closure Table and the Revision Table | The real risk is the Author approving its own work. One Closure Table covers it. The other four tables were the Author's own proof. |
| A low problem needs no check of each item | Full cost for noise that decides nothing |
| A reviewer reports problems and the two gate values, and gives no close decision | The close test and the pass test had different sources, so one state had two answers |
| **The three end questions use the execution view**: where to start, how to judge a step, what not to touch and when to stop | The old third question, "why did we decide this", is the question of an auditor. In the execution product it forces the plan to hold history, which fights the rule "the plan becomes shorter". |
| **The whole Decision Table moved into the record**. The plan keeps `Decision N` only. | The anchors, the properties, and the rejection conditions used too much of the Execution Agent context |
| A Light level no longer exempts the Decision Table | After the table moved into the record, the exemption saved plan space only, and it hid the case "a Light level cannot say why we decided this" |
| The rule "context isolation at implementation dispatch" and the test "the two products agree" are new | The rules said what to give a reviewer, and nothing about the implementer. A changed decision left the sentences that cite it in the plan with no owner. |
| The record splits into what the Author reads and what the User reads | The required fields had no reader, so the record grew into a file that nobody reads |
| Terms: released item, trigger item, dead state, judged item became disclosed item, must change, uncleared, one test | Four invented terms explained each other, and a rule gave no action |

The second pass **added no new mechanism**. It added three rules only: context isolation, the cross-check of the two products, and the full format of the start instructions. It changed no round rule, no level rule, no gate, and no tier.

### Third pass: move the details down, change no test

The User said that the main file was too large. This pass **deleted no test and added no mechanism**. It moved the sections that "serve one test only" into `references/`, and deleted the copies that repeated a reference. The main file went from 356 lines and 13,487 characters to 326 lines and 12,562 characters. The references grew by about 1,300 characters: one rule used to live in two places, and one copy is left, but the moved text gained the trigger and the reading rule.

| Change | Why the earlier form was not worth it |
|---|---|
| The code samples of the failure-mode table, the field rules of the Revision Table, and the three hard rules of an acceptance assertion: deleted, with one test and a pointer left | The checklist sections A, C, and D already held the full text. The three lines in the main file were a second copy. |
| The six archive rules, the Evidence templates and the Choice List groups, and the search discipline of affected positions: moved to the Review Protocol sections "Version and Snapshot", "Minimum Record", and "Re-Review and Evidence Reuse" | The Author uses them only when it writes a file, writes the record, or re-checks a changed rule. They are not on the round path. |
| The three rules of "context isolation at implementation dispatch": moved to the Protocol section "Dispatch to Implementation", which already held the full text | One rule had two owners, and the protocol version was more complete |
| The round arithmetic of the Alternative route: moved to the Alternative file, "Rounds and Route Accounting" | The Author uses it only when it starts an alternative solution. The main file needs the tier table and the test "select by the size of the change". |
| The four values of "the round has no executable action": moved to the Protocol section "Delivery Check" | The Author uses them only at the moment of the stop decision |
| The dispute table became four short rows | Only the clauses went. "No vote count, no higher severity" must stay in the "two routes disagree" row: `multi-route-review.md` and this table both point to it, so the position must not move. It went missing once during a compression pass, and a read-only re-review found it. |

**The lesson of this pass**, for the next one: a pointer silently removes a test. In the first version, two tests went missing while the sentences were shortened: "no vote count, no higher severity" and "handle each new high or medium problem". Reading the main file and the references once each does not show it. Only an independent read-only review that compares each line with the backup found it. **A move down must have that check.** The test of the check is one line: is the completion test of each rule still there?

**The fourth pass** changed wording only. The strength words became five, each with one form: must, must not, should, may, only. Before that, nine forms expressed two levels of strength, and a script reads the five forms now. Two heavy sentences came apart at the clause boundary: the average sentence length went from 33.0 to 28.1 characters of the same measure, and long sentences from 27 to 1. Then the six reference files took the same treatment: 46 long sentences became 28.

**Four kinds of damage that a wording pass causes** (each found by a read-only re-review, never by the Author's own check): a prohibition becomes neutral guidance; a clause of a list goes missing; a conjunction becomes a disjunction, so a trigger widens; an exception test becomes an example, so the boundary moves again. Check for these four before you deliver a wording pass.

**What the pass did not do**: it did not expand the three-character connectors ("it is false, so use Standard" stays short). It also did not delete a condition or an exception to reach a sentence length. Sentence length is not the test. The test is whether the completion condition of each rule is still there.

**The fifth pass: two blocks came back.** The User asked why a block that every round reads should sit in its own file. Two tests replaced "how often is it read". First, does every branch read it? Second, is it a test or a format? Only two blocks came back: the five file-location rules, and the four values of an executable action. Each round needs both, both are small, and both are tests. The rest stays in `references/`, because a round reads it by section, or one route agent reads it. The main file went from 32.7 to 33.6 KB, and the protocol from 21.4 to 20.4 KB.

**If the file must become smaller again**, the remaining text is the rules that every round judges: the three levels, the eight plan items, the two gates, and the routing table. Only deleting a rule can make it smaller, and that is a content decision. Walk the maintenance list below, item 1 and item 5. Do not let a word count decide.

## Deleted Rules: Do Not Add Them Back

Each deletion kept its protection aim, but the mechanism changed.

- **A fixed three routes** ("use three routes even for a simple plan"). The aim holds and the mechanism was wrong: it removed the judgment instead of recording it. Three levels carry it now. A silent skip is still a violation, and the cost follows the risk. **A Light level is not its return**: a Light level needs all four criteria to hold, each with evidence.
- **A diff re-review after the budget (at most two rounds)**. It overlapped two other rules: "a Contract-Precision Revision goes through the normal re-review" and "a used budget delivers without convergence". One state had three answers, and the reader takes the cheapest. The cost side is already down: one full scan route each round. A second exit is not needed.
- **Area that does not grow** (rule count, parameter count, acceptance item count). A count invites merge and rewording to avoid it, and "rule" has no countable definition. One ignored rule is the result. The content test carries it now: if you delete this rule, will the Execution Agent make a wrong decision?
- **"Two points met in round 3 adds route four"**. It reads only whether the plan passes, not the nature of the problem. So it forces a new approach on a plan that has the right direction and needs precision. "Select the tier by the size of the change" carries it now.
- **A pass gate written as "zero high, zero medium on each route"**. A count is a finish line and a forbidden target at the same time. The usual result is a lower severity. The Closure Table carries it now: each problem needs a resolved or unresolved value, and a resolved problem points to a rule. The count became a summary.
- **Two hints for the stop tests**: "freeze for a run after two rounds with no high or medium problem resolved"; "when no rule can be deleted, add only". The first one contradicts "true means continue" at the same state. Its closing action, "write a blind spot", is forbidden in section 1 of the main file. The second one points the same way as "do not answer a new finding with a new rule", so it is a second copy. "The round has no executable action" carries both.
- **Route names A, B, C**. After Tier A, B, and C arrived, the letter map was gone. To keep it would let "route C" and "Tier C" read as one thing.
- **A score, a weight, and a vote count** (not adopted; never deleted). A score replaces "can the work start" with a number that has no stable relation to it. The Author then improves the number, the reviewer improves the number, and nobody owns the question "can this plan be implemented". A vote count treats "nobody objected" as "no problem". A real problem that one route finds is the problem with the fewest votes.

**The lesson of the eight passes on 2026-11-22 and 2026-11-23** is more useful than the seven attempts: **to judge whether a test can be used, first check whether all its operands sit inside the text under review.** Question 2 of the gate needed four versions before anyone saw that it asked "what did the User say", which is not in the text. Question 1 never had this problem, because its operands (rule, object, acceptance) all sit in the text. The rule added on 2026-11-24, "how to judge when the note holds no words of the User", is the second repair of the same lesson.

**A rejected proposal: an exit that skips the review** ("a single-point change that one command verifies and that has no decision point goes straight to work"). The User calls this skill by hand, so no task pulls it in automatically. The failure "a small change enters the full loop" does not occur. One more exit only makes "I do not want a review today" the default. **Do not add it back.** If the skill ever starts automatically (for example as a permanent rule in `AGENTS.md`), judge this proposal again.

## Maintenance List

1. **Does the failure that this rule prevents still occur?** If it does, keep the rule and write the trigger condition. If the rule only sounds safe, delete it. A new rule has one chance.
2. **Does the rule give a different answer from an existing rule?** If one state has two answers, the person at that step takes the easier one. Remove the conflict before you add content.
3. **Is the basis of the judgment observable?** "Is it really independent" and "did the reviewer understand" are not observable. "Does the dispatch message hold a reason of the Author" is observable. An unobservable test gets bypassed.
4. **Is the completion test checkable?** "Covered well enough" is not checkable. "Each problem has a resolved or unresolved value, and each resolved problem has a position" is checkable.
5. **Who keeps the aim of a deleted rule?** If nobody keeps it, do not delete the rule. If someone keeps it, write one line in this file. Without that line, the next maintainer fills the gap back in.
6. **Can one sentence state which judgment this change alters?** If not, the change is wording only. Do not change the structure.
7. **One rule has one maintenance point.** Put the detailed branches in `references/`. The main file keeps the action, the condition, and the completion test. The main file holds no explanation. The reasons are here.
8. **Do all the operands of a new test sit inside the text under review?** A test that needs outside information becomes a new review again and again.
9. **Which reader owns this content?** The plan holds only what "the Execution Agent does a wrong action without it". Everything else goes into the record. A rule names the Execution Agent, the User, or the Author. It names no "person", "reader", or "implementer".

## Known Residual Risks

- **The main file has 329 lines and about 13,000 characters**, and it is no longer one page. Do not use a word count as a reason to split it. To split it, find the section that "serves one test only". The test is always the same: is the completion test of each rule clear? A split brings a new risk: **nobody reads a pointer**. When someone says "I followed the main file and never opened a reference", add the trigger to the table "Which file to read, and when". Do not move the section back.
- **The two products drift apart.** The cross-check runs once, at delivery. An implementation deviation can make a number in the plan out of date in the record. Watch two failures: the plan holds evidence, reasons, or review history (the record owns them); or the record holds an action list for the Execution Agent only (the plan owns it). Move the content back. Do not keep one copy in each place "just in case".
- **"A reviewer reads the plan and the decision half; the Execution Agent reads the plan" fails easily.** A scan route that gets the review history is no longer blind, and a busy Author puts the whole record into the Execution Agent context. Both rules name an action, and both depend on a person who does the check once. No mechanism catches the failure. When material goes missing or extra, add a dispatch template. Do not merge the two products.
- **The level depends on the cost of a wrong action.** The tests are lists now: four for Light, five classes for Deep. A combination of tests still goes wrong. Watch one failure: "a Light level is a reason to do less". If a shared interface gets a Light level, change those tests. Do not replace them with a more abstract principle, and do not return to "three routes always".
- **The boundary between partial delivery and an exit without convergence** can split a plan that is "a little wrong everywhere" into a partial delivery. When that happens, tighten the rule: each of the three end questions for the ready part must have a direct answer. If one has none, exit the whole plan without convergence.
- **Tier B "change one component" overlaps "local repair" of the Adversarial route.** The overlap is not a problem. When the two routes agree, merge the two problems.
- **One limit of ten rounds lets a Light level use all ten.** The limit is not a permission. A plan that meets the pass test should stop at once. Watch the failure "we still have rounds, so review once more". Do not change the limit when you see it. Check first whether that round has an executable action.
