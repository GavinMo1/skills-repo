# Design Notes: Failure Classes, Reasons, and Deleted Rules

**This file is not a runtime instruction.** Read it in two cases only: you change a rule, or you delete a rule. The reasons are here. The rules are in the [main file](../SKILL.md). If the two disagree, the main file wins, and you update this file.

A rule restated here in one line keeps its strength word and names the file that owns the wording. That file is the authority. This file keeps the reason, the strength, and the case.

## How this file is organised

Seventy recorded failures, grouped by **cause** into fourteen classes. Each class gives four things:

- **Cause**: the one mechanism that produced every failure in the class.
- **Test**: the question that decides whether a new failure belongs here. If the answer is no, it is another class.
- **Rules**: what the class holds, at the strength the main file gives it, with the place the wording lives.
- **Cases**: the ID of every recorded failure that belongs to this class, in one line, then a pointer to the one-line record of each in [Design Cases](loop-design-cases.md). No case is dropped.

**Two accidents can share a detector and still belong to two classes.** The test of a merge is the cause, not the symptom, and the two tests differ in shape: a shared symptom invites a merge, while a shared cause is what makes one class out of two. Two classes in this file share one detector, C01 and C07, because both are found by a line-by-line read against a backup. They stay apart because the cause of C01 is a fact that lives in two places and the cause of C07 is a text operation that dropped a test. A merge would keep the detector and lose both rules. **A shared detector is not a shared cause.**

A class is not a summary of its cases. A class is the smallest statement whose rules a reader can derive from it. **The test of a class is the test of a rule**: name one rule under the class; can a reader who obeys a neighbour under the same class violate it? If yes, the class is a heading, and the rules stay separate under it. If a merge would let a reader satisfy one rule and violate a neighbour, the merge failed: split it back.

A rule appears under two classes when it defends two causes. It is still one rule, with one maintenance point (C01).

**The cases live in a second file.** Each class ends with the list of its case IDs. The one-line record of each case — what happened, and the rule it produced — is in [Design Cases](loop-design-cases.md), under the same class name. The list of IDs is here so that a reader of this file still sees everything the class holds; the detail is a lookup, not a passage to read on a round.

A case marked **†** belongs to a rule that is new and has no anchor yet ("inference, new, not observed yet"). Give it one chance. Two cases carry no mark and no chance: F62 and F63 were written as new on 2026-11-27, and a live task observed both in the same week, so each carries a real anchor now and the ledger says so. A case marked **✗** is a proposal that would bring a deleted failure back. A case marked **⋄** is a near miss seen while the 2026-11-27 change was written; the rule closed it in the same change, and this file records it first.

## C01 · One fact, more than one authoritative copy

**Cause**: one fact is written in more than one place, and nothing forces the copies to agree. A repair reaches the copy that the finding named, and no other.

**Test**: does the failure come from the same fact living in two places at once — two files, two owners, two positions, two products, a plan sentence and the decision it cites?

**Rules**

- Report the change surface as three items, each with its own list: the decision points the change touches; the positions that are new this round; the rules this round deleted or merged. **Do not merge the counts.** Write "deleted 0" when the deleted count is zero, and state why only an addition can answer the finding. When the new positions are not zero, state why you cannot merge them into one position. — SKILL.md section 3.
- One rule has one maintenance point. The main file keeps the action, the condition, and the completion test; the branches live in `references/`. — Maintenance 7.
- The record is the only source of the decisions. The plan cites a decision by number only. The Decision Table and the rejected candidates are the only home of "why we decided this". A landing anchor is not a decision-evidence anchor: the plan holds the landing anchor, the record holds the evidence behind that decision. — SKILL.md Terms, section 1; protocol "Minimum Record".
- The Choice List is a derived view of the Decision Table, not a second source. When the table changes, the list changes with it. — protocol "Minimum Record".
- The two products agree: each `Decision N` in the plan has a row, and the sentence the plan derives from its decision agrees with the Selected implementation of the row. If a number has no row, or the two texts disagree, the plan fails. — SKILL.md section 4, gate 3.
- If two rules say the same thing, merge them before you change them. — SKILL.md section 3.
- The completion test of a reused route lives in two places, section 2 of the main file and multi-route-review.md. Change both together. — SKILL.md section 2.
- Do not keep one copy in each place "just in case". — Known residual risk, two products.
- A reviewer checks the completeness of the affected positions: the Author gives the search command and every matching line with a disposition for each, and a reviewer checks the list with a third, adjacent pattern. The Author's own check is not sufficient. — SKILL.md section 3; protocol "Re-Review and Evidence Reuse".

**Cases** (9): F03 · F25b · F28 · F30 · F45 · F51 · F66 ✗ · F67 ⋄ · F70 ⋄

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C01.

## C02 · The producer certifies its own work

**Cause**: the Author's check of the Author's work is accepted as evidence. The gaps are where the Author did not think to look, so the check cannot find them.

**Test**: is the evidence for this failure a verdict that the Author produced about its own text?

**Rules**

- The Author does not enumerate the consistency conclusions. The Author's own check is not sufficient; a reviewer checks the completeness of the affected positions with a third, adjacent pattern. — SKILL.md section 3.
- One Closure Table covers "did the Author approve its own work". The other four tables of the Author's own proof are gone. — SKILL.md section 3.
- At least one route of each round is an agent that has not seen an earlier version, and it does the full scan. — SKILL.md section 2.
- A reviewer must check the real change. Do not accept a "fixed" claim, and do not forward an old pass conclusion. — SKILL.md section 3; multi-route-review.md "Summary and Re-Check".
- A route with no high or medium problem for two rounds gets a new agent in the next round. It tests one point: was there really no problem, or did the reviewer get used to the plan? — multi-route-review.md "Reuse or a new agent".
- The Blind Spot List is writable: write the name of the blind spot and the condition that must bring you back. — SKILL.md section 1; the destination half of the same rule is C12.

**Cases** (2): F02 · F19

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C02.

## C03 · One state, more than one answer

**Cause**: a state admits two or more answers — two rules, two roles, two exits — and the person at that step takes the cheaper one.

**Test**: at this state, can two rules, two roles, or two exits both be applied without either being violated?

**Rules**

- A reviewer reports problems, the two gate values of each open item, and the check scope and limits. The Author makes every close, pass, and partial-delivery decision. A reviewer does not produce a "can we close" conclusion. — SKILL.md section 2.
- Do not use a vote count. Do not use the higher severity to settle a disagreement about feasibility: the higher severity applies only when two routes agree on the problem and differ on its severity. One route that says "this cannot work" and one that says "there is a workable path" give opposite judgments, and that case goes to the dispute table. — SKILL.md section 3; multi-route-review.md "Summary and Re-Check".
- The dispute table gives one answer per case. A fact or a severity: give the raw evidence, and the reporter re-checks. Two routes with opposite conclusions: each gives one testable minimum check, the Author runs it once and returns the raw result to both, and an item that is still open stays open. — SKILL.md section 3.
- A reused route owns the Closure Table, and a resolved item with no evidence position counts as unresolved. — SKILL.md section 3; multi-route-review.md.
- A failed route: the new route of the next round takes over its duties, and the round is written as incomplete. Do not write a failed route as "no problems". An incomplete route is not a route with zero problems. — SKILL.md Rounds; protocol "Concurrency and Failure Recovery".
- The taking-over route gives the gate values and writes "self-judged; the original route is lost". — SKILL.md section 4.
- The conditions that open no new round give one answer each: the ten-round limit with its one-time exception, and "the round has no executable action". — SKILL.md section 4.
- When no route can be reused, the regression check has no owner, and it is repaired in one order: send each new agent a **closed-position list** (the positions of the closed items only, with no history, no conclusion, no problem ID, and no wording of the original problem, asking one question: does this position still hold the sentence that the Closure Table cites). If you cannot build the list, write "this round has no regression protection" in the record and open one item for each position you could not check. — multi-route-review.md "When no route can be reused".

**Cases** (7): F11 · F21 · F40 · F44 · F49 ✗ · F63 · F64 ✗

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C03.

## C04 · A cheaper proxy takes the judge's seat

**Cause**: the decision is made by something easier to observe than the question it stands for — a count, a score, a finished artifact, a pass state — and that thing then becomes the target.

**Test**: is the deciding input a proxy (a count, a score, a completed artifact, a pass state) rather than the property the decision depends on?

**Rules**

- Pass = the plan is ready to start (gate 1 and gate 2) and the record is auditable (gate 3). The two groups serve different readers. Do not convert one into the other. — SKILL.md section 4.
- Do not declare a pass by a vote count or an average score. — SKILL.md section 4.
- The high, medium, and low counts are a summary only. They do not decide a continuation or a close. Do not open a round to drive a count to zero. — SKILL.md section 4.
- The plan text holds no high, medium, or low count, no round count, and no route count. — SKILL.md section 5.
- Select the review level by the cost of a wrong action, not by the size of the plan. — SKILL.md Start.
- Select the alternative tier by the size of the change, not by the pass state of the plan. Do not use one switch ("do we add a route?") for all three tiers. — SKILL.md Rounds.
- The routing table sends a finding by two questions: can one command test it, and is a failure single or catastrophic. — SKILL.md section 3.
- The test for a rule is its content, not a count of rules: if you delete the rule, will the Execution Agent make a wrong decision? — SKILL.md section 3.
- No count is a gate: no "area that does not grow", no "zero high, zero medium on each route", no score, no weight, no vote count. The Closure Table carries what the count carried: each problem has a resolved or unresolved value, and a resolved problem points to a position. — Deleted Rules.

**Cases** (9): F10 · F17 · F18 · F39 · F41 · F42 · F43 · F47 · F65 ✗

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C04.

## C05 · The cost of the review separates from the value, and the person skips the review

**Cause**: material or effort is delivered where nobody consumes it. The step then costs more than it returns, and the cheapest path is to skip it.

**Test**: does the failure come from reading, carrying, or writing something at a moment when nobody uses it?

**Rules**

- Minimum setup each round: one reviewer that has not seen an earlier version does a full scan; each reused route checks every position that the Closure Table cites, including the rows whose status is resolved, and does not re-scan. — SKILL.md section 2.
- A **low** problem does not need an item-by-item evidence check. — SKILL.md section 3.
- The level table carries the four Light criteria and their evidence. If one criterion fails, or you cannot write the evidence, or you cannot estimate the cost, use Standard. — SKILL.md Start; the selection property is C04.
- The table "Which file to read, and when" gives a trigger, how much to read, and the cost of a wrong read. A daily review does not read the full checklists or the design notes. When you reach a section, read it to the end; do not use one sentence from it. — SKILL.md "Which file to read, and when".
- The placement test for a block: does every branch read it? is it a test or a format? A block that every round reads at two crossing points belongs in the main file. — the fifth pass.
- A pointer is not a delivery. When someone says "I followed the main file and never opened a reference", add the trigger to the table. Do not move the section back. — Known residual risk, main-file size.
- If the main file must become smaller, the remaining text is the rules that every round judges: the three levels, the eight plan items, the two gates, and the routing table. Only deleting a rule can make it smaller, and that is a content decision. Walk maintenance items 1 and 5. Do not let a word count decide. — the fifth pass.
- Complete the small items before you stop: one command, one search, one symbol read, one document section, or one check conclusion settles the item and opens no round. — SKILL.md section 4.

**Cases** (8): F13 · F14 · F20 · F29 · F31 · F32 · F38 · F50

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C05.

## C06 · A boundary that lives only in a sentence decays

**Cause**: the isolation is stated as an instruction with nothing behind it, so it holds only while one person remembers to perform it once.

**Test**: is the defense an action that a person performs once, from memory, with no artifact that carries it?

**Rules**

- The dispatch message decides the independence, not the change of agent. Put in the message: the goal, the constraints, the entry point, the duty, the frozen text, and the Core Preconditions with their evidence. Leave out: the review history, the Author's account of the problems, and the current conclusions of other routes. Delete every sentence of the form "after we discussed it, we decided". If a tool cannot isolate the context, state which material is exposed. — SKILL.md section 2.
- A reused agent must not claim a blind review. Write in the record: "this route is a reused reviewer and has seen the earlier versions". — SKILL.md section 2; protocol "Dispatch Material".
- Write which routes are reused and which are new, and which material each new agent saw. — multi-route-review.md.
- Five hard requirements for a dispatch: one to three directed questions, each with a concrete input; read the frozen file again, not the version in memory; no blind-review claim by a reused agent; the change list and the change surface before the full text; four evidence items graded by severity. — protocol "Dispatch Material".
- The implementation dispatch and the review dispatch are two different things. Give the Execution Agent the plan text only, plus the necessary goal and authorization limits. Delete the record, the review history, the dispute record, the counts, the rejected candidates, the version history, and every sentence that starts with "because". The test: the plan already holds the action and the test, so the message needs no reason. — SKILL.md section 5; protocol "Dispatch to Implementation".
- When the Execution Agent asks "why did we decide this" a third time, the action items or no-go items of the plan are not good enough. Change the plan, not the dispatch wording. — protocol "Dispatch to Implementation".
- Do not merge the two products. When material goes missing or extra, add a dispatch template. — Known residual risk, isolation.

**Cases** (4): F12 · F25a · F52 · F69 ⋄

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C06.

## C07 · A repair or a text operation silently removes a completion test

**Cause**: a move, a merge, a shortening, a wording pass, or a repair is treated as a neutral act, while it is the very act that carries or drops the test.

**Test**: does the failure come from an edit that was meant to touch one place, or the form only?

**Rules**

- A move down must have an independent read-only re-review that compares each line with the backup. Reading the main file and the references once each does not show the loss. The test of the check is one line: is the completion test of each rule still there? — the third pass.
- Check four kinds of damage before you deliver a wording pass: a prohibition becomes neutral guidance; a clause of a list goes missing; a conjunction becomes a disjunction, so a trigger widens; an exception test becomes an example, so the boundary moves. — the fourth pass.
- Sentence length is not the test. Do not delete a condition or an exception to reach a length. The test is whether the completion condition of each rule is still there. — the fourth pass.
- Keep a hard gate and a default in separate sentences. A hard-gate sentence gives the rule only; the reason goes into the record or into this file. — SKILL.md Terms.
- A change to a strength word is a Substantive Change: it opens a new version and a re-review. — SKILL.md Terms.
- **Reuse is a safety duty, and the economy is a side effect.** A scan route does not get the old problems, so a regression in a closed item is invisible to it. The reused route is the only reviewer that reads the position of a closed item. — multi-route-review.md "Reuse or a new agent".
- Can one sentence state which judgment this change alters? If not, the change is wording only, and it must not change the structure. — Maintenance 6.
- Does the rule give a different answer from an existing rule? Remove the conflict before you add content. — Maintenance 2.

**Cases** (5): F33 · F34 · F36 · F37 · F62

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C07.

## C08 · The rule text does not fix the reader's action

**Cause**: the text leaves a value, a form, a term, or a symbol to the reader, and each reader supplies a different one.

**Test**: can two compliant readers produce two different actions from this text?

**Rules**

- Use these five strength words only: must, must not, should, may, only. Write a negative step as "Do not" plus the verb. A banned form is "have to", "need to", "shall", "ought to", "is required to", "make sure", or "always". — SKILL.md Terms.
- Use one word for one concept. Keep "downgrade" for a Core Precondition only; for a severity, write "reduce the severity". — SKILL.md Terms.
- Write route names as words. Do not write A, B, or C for a route: the letters clash with Tier A, B, and C. — SKILL.md Start.
- Budget: ten rounds maximum for all levels. If the User gives a smaller number, use it. Do not reset the count after a change of agent, an added route, a new solution, or a resumed run. — SKILL.md Start.
- A rule gives an action. Do not build terms that explain each other. — SKILL.md Terms; the 2026-11-24 history.

**Cases** (4): F04 · F27 · F35 · F46

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C08.

## C09 · The basis of a judgment is not observable inside the material under review

**Cause**: a claim is admitted without a basis that a second person can check inside the frozen text, or a basis that covers another path or another channel than the one the claim names. A test whose operand sits outside becomes a new review again and again, and a fact that one command can show is parked on a list, where it returns as the same wrong conclusion.

**Test**: can a second person see, inside the frozen text or in one command, the thing that the claim is about?

**Rules**

- A proved precondition gives an anchor `file :: symbol` and one falsifiable condition: "if you cannot find X in this symbol, this item is false". For the other statements, write the evidence class only. — SKILL.md section 1.
- A **landing anchor** has two parts: `file :: symbol`, and one sentence that names the symbol where the decision happens, with the call-chain line that shows the relation. **A name that exists is not a landing point.** — SKILL.md section 1, plan item 4; Terms.
- Every name in the plan carries a mark at its first appearance: `(new)`, or `(existing: <file> :: <symbol>)`. **A name with no owner reads exactly like a real one.** — SKILL.md section 1, plan items.
- A source anchor proves "the code says this". It does not prove "the run goes this way". A runtime precondition runs in an isolated directory, with four evidence items: the command, the exit code, the key output passage, and the written fields or the state difference. Write "not met" as not met; do not write "partly met". — protocol "Isolated Run of an Executable Precondition".
- If one command, one search, or one symbol read gives the answer, run it now. Do not leave it as a to-do item. — SKILL.md section 1.
- The Evidence position of a resolved item points to a named position in the plan text. If it does not, count the item as open. — SKILL.md section 3.
- The acceptance table has four columns, and the second names where the state and the input come from: **production path**, **hand-made fixture**, or **real machine**. A state that the assertion verifies is written by the production path, and the cell names the producer as `file :: symbol`. An illegal or boundary input is hand-made, and the cell names the fixture. **A cell that names neither counts as hand-made.** — SKILL.md section 1; checklist C1.
- An assertion names the channel that its recipe reads and the channel under test. Evidence read from the read-back interface does not prove the event channel. — checklist C5. This rule has no row in the anchor ledger yet.
- Four evidence items for a problem, graded by severity: `file :: symbol`; a passage from that symbol; a falsifiable condition; a relation anchor when the conclusion depends on a call, a reference, or a configuration relation. A high or medium problem gives all four. A low problem gives the first and the third. A problem about runtime behavior adds the command and its exit code, or it is marked "plan reasoning". — protocol "Dispatch Material".
- Every row of the Decision Table has the evidence and a property, or a checkable anchor. If it has neither, the row is not complete. — SKILL.md section 4, gate 3.
- Is the basis of the judgment observable? "Is it really independent" and "did the reviewer understand" are not observable; "does the dispatch message hold a reason of the Author" is. — Maintenance 3.
- Is the completion test checkable? "Each problem has a resolved or unresolved value, and each resolved problem has a position" is checkable. — Maintenance 4.
- Do all the operands of a new test sit inside the text under review? Read only the line that the plan itself contains. If the note holds no words of the User, judge by one point only: does the Core Task give an observable failure symptom? — Maintenance 8; SKILL.md section 4, gate 2.

**Cases** (9): F06 · F07 · F09 · F16 · F48 · F60 † · F61 † · F68 ⋄ · F71

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C09.

## C10 · A two-valued decision is applied to a result that is partly good

**Cause**: the decision has two forms while the result has two halves, so the usable half is thrown away with the unusable one.

**Test**: does the failure come from choosing between "all" and "nothing" for a result that is part good?

**Rules**

- Three delivery forms only: pass, partial delivery, and exit without convergence. Do not write the exit as a pass. — SKILL.md section 4.
- Partial delivery: split the plan into "ready to start" and "held by open items". The start instructions of the ready part are complete and hold no unstated assumption. If you cannot do this, exit the whole plan without convergence. — SKILL.md section 4.
- A pass means only this: inside the checked scope and the current evidence, no open problem prevents the start. It does not prove completeness. — SKILL.md section 4.
- Partial-delivery admission uses gate 1 only. Do not lower it for a Light level or a tight budget. — SKILL.md section 5.
- When the boundary lets a plan that is "a little wrong everywhere" split into a partial delivery, tighten it: each of the three end questions for the ready part has a direct answer. If one has none, exit the whole plan without convergence. — Known residual risk, delivery boundary.

**Cases** (2): F15 · F54

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C10.

## C11 · Content with no named reader has no owner

**Cause**: content is written for "the reader", so no role owns it. It then either fills a context that does not need it, or grows into a file nobody reads.

**Test**: does the failure come from content sitting with a reader who will not use it, or with no reader at all?

**Rules**

- Two products, each with one reader: the plan for the Execution Agent, the record for the Author and the User. The test for a line: delete this line. Will the Execution Agent do a wrong action? If no, move the line to the record. — SKILL.md Terms.
- Write one of the three roles: the Execution Agent, the User, the Author. Do not write "person", "reader", or "implementer". — SKILL.md Terms; Maintenance 9.
- The only test of "shorter" is "what does the Execution Agent do with it?". Do not use a word count. — SKILL.md section 5.
- The plan holds no decision-evidence anchors, no property judgments, no review history, no dispute record, no problem count, no Choice List, and no version history. — SKILL.md section 1.
- The record splits by reader: the Author reads the conclusion, the rounds, the open items, and the implementation deviations; the User reads the conclusion, the level evidence, and the open items. Do not read the full record. — SKILL.md section 1; protocol "Minimum Record".
- The three end questions of gate 1 use the execution view: where to start and in what order, how to judge each step, what not to touch and when to stop. — SKILL.md section 4.
- Each line of the plan answers "what does the Execution Agent do with it?". Move every line that cannot answer this into the record. — SKILL.md section 5.

**Cases** (4): F05 · F22 · F23 · F26

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C11.

## C12 · A new finding has no cheap destination, so every answer is more text

**Cause**: a finding arrives with no default destination, so the default becomes another paragraph or another mechanism. The plan grows monotonically and stops being implementable.

**Test**: does the failure come from answering a finding with more text, or with a mechanism that outlives the finding?

**Rules**

- Before you decide where a new finding goes, ask: can one command test it, and is a failure single or catastrophic. No and many (or one catastrophic) → the plan text. No and single → one line in the Blind Spot List. Yes → one test: which input or state fails, plus one fallback action, and no mechanism. Yes and you know the answer → a constant or a default. — SKILL.md section 3.
- Do not answer a new finding with a new rule. When a finding asks to "add X", first answer why X is missing here: if a deletable item caused the gap, delete that item first, and open a round for it. — SKILL.md section 3.
- Add at most one mechanism per round. A mechanism needs a new state, a new parameter, a new dependency, or a new order. If one round adds more than two action steps, merge them first. — SKILL.md section 3.
- If the plan crosses a hard line, delete or merge first. Do not write "watch this next round". — SKILL.md section 3.
- A blind spot is not a new rule. "I do not know this" is cheaper than "add one more mechanism", and it holds only when the gap does not make the Execution Agent do a wrong action. — SKILL.md section 1; the list itself is C02.
- Tier C asks one question at the first dispatch and then as needed: how much do the existing mechanisms cover, and is the smaller goal still worth the work? — SKILL.md Rounds; alternative-review.md.
- The plan should become shorter. — SKILL.md section 5.
- The record carries two items: did you answer the new finding with a new rule, and how many mechanisms this round adds. — protocol "Minimum Record".

**Cases** (2): F01 · F08

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C12.

## C13 · A relaxation, or a leftover budget, is read as a permission

**Cause**: a narrowing of scope is read as a reduction of duty.

**Test**: does the failure come from someone using "fewer routes", "a lighter level", "a smaller scope", or "rounds left" as an authorisation to do less?

**Rules**

- A Light level needs all four criteria, each with evidence. If one criterion fails, or you cannot write the evidence, or you cannot estimate the cost, use Standard. — SKILL.md Start.
- The level selects the number of routes only. The Decision Table, the unverified list, and the Blind Spot List go into the record; they use no plan space, and a Light level needs no exemption from them. — SKILL.md Start.
- Do not reduce the number of routes when the four Light tests fail. — SKILL.md Start.
- Ten rounds is a limit, not a permission. A plan that meets the pass test stops at once. When you see "we still have rounds, so review once more", check first whether that round has an executable action, and do not change the limit. — SKILL.md Start; Known residual risk, round limit.
- A Light-level plan may compress the record into three lines. The plan side holds all eight items. — SKILL.md section 5.
- A Light level has one route from the start; that route may do the scan and the Closure Table check, and the record says "this route does both; independence is dropped". — SKILL.md Start; multi-route-review.md.

**Cases** (3): F24 · F53 · F56

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C13.

## C14 · A deletion loses the failure that the deleted rule guarded

**Cause**: a rule is removed without a record of the failure it answered, so the next maintainer restores the mechanism.

**Test**: does the failure come from a rule or a mechanism that was removed earlier, coming back?

**Rules**

- Each deletion keeps its protection aim, with a named carrier. Write one line here for each deleted rule; without that line, the next maintainer fills the gap back in. — Maintenance 5.
- Does the failure that this rule prevents still occur? If it does, keep the rule and write the trigger condition. If the rule only sounds safe, delete it. A new rule has one chance. — Maintenance 1.
- Write an anchor when you have a case, and "inference" when you have none. Do not invent a case to fill the column. A rule marked "inference" is a deletion candidate, not a reason to keep it: if it stops a real failure once, add the anchor; if no anchor arrives, delete it the next time you change this file. A rule that is new and has met no real use gets "inference (new, not observed yet)" and one chance. — the anchor column.
- The list "Deleted Rules: Do Not Add Them Back" below carries the carrier and the reason of each deletion. — Deleted Rules.

The anchor ledger, with the status of each rule as anchored or inference only, is in [Design Cases](loop-design-cases.md).

**Cases** (2): F57 · F58

One line for each: the phenomenon and the rule it produced, in [Design Cases](loop-design-cases.md), class C14.

## One trade, two rules

**F13** (one full scan route each round) and **F40** (a diff re-review after the budget, deleted) are one decision, not two. The full scan is the price paid for "no second exit": it lowers the cost per round, so the loop needs no cheap exit at the end of the budget. A proposal that re-adds "review only the diff each round" while keeping "a high-problem majority turns to implementation" re-creates the configuration this file deleted twice — a cheap round plus a cheap exit (F64, F65). When someone proposes either half, read the other half.

The diff cannot see the damage that this skill exists to catch. The live task's two families are cross-text properties: section 2 said "no delivery" and section 6 said "delivery", and one version dropped the `+1` that the earlier version had put in. A reader of the diff sees neither. The method file already says it: when one document is repaired again and again, the new problems sit in the internal consistency of one item, because the repairer reads only the passage that it changed (C07, F62).

## The narrow executable surface

**One shape, three homes.** A new rule states an intent that covers a surface, and it nails down one part of that surface. The rest is left to the reader, and the reader supplies what costs least. Three instances arrived with the 2026-11-27 change, and each one was closed by naming the part that had no rule:

| Instance | The intent covered | The rule pinned down | What nobody owned |
|---|---|---|---|
| F67 | "the acceptance rules are listed here" | the old set of rules | the new member of the set |
| F68 | "a production path names its producer" | the case where a producer can be written | the case where it cannot |
| F69 | "send the new agent a closed-position list" | what the list carries | what the list must not carry |

**This shape is not a class, and it is not an unmerged singleton.** It decomposes into three classes, and each class carries the part that has to be checked: C01 for the set and its copy, C09 for the claim and its basis, C06 for the boundary and the artifact. A fifteenth class named "the executable surface is narrower than the intent" would hold thirty rules and derive none of them: its test is "is this rule incomplete?", and every rule answers yes to that somewhere. That class would let a reader satisfy a neighbour and violate the rule it was reading. So the shape stays a way of reading these notes, not a category.

**How to use it when you write a rule.** Read the intent, then ask for the surface it covers: the set and every list of the set; the good case and the empty case; what the artifact must carry and what it must not. One more test ends the pass: can a reader who wants to comply avoid the rule by saying nothing? If yes, the part that silence covers has no rule yet.

## Deleted Rules: Do Not Add Them Back

Each deletion kept its protection aim, and the mechanism changed. The class names the cause; the carrier is what holds the aim now.

- **A fixed three routes** ("use three routes even for a simple plan"). C04. Carrier: the three levels, selected by the cost of a wrong action. The mechanism was wrong because it removed the judgment instead of recording it. **A Light level is not its return**: a Light level needs all four criteria to hold, each with evidence.
- **A diff re-review after the budget (at most two rounds)**. C03. Carrier: "one full scan route each round" plus "a used budget delivers without convergence". It overlapped two other rules, so one state had three answers and the reader took the cheapest. See "One trade, two rules".
- **Area that does not grow** (rule count, parameter count, acceptance item count). C04. Carrier: the content test, "if you delete this rule, will the Execution Agent make a wrong decision". A count invites merge and rewording to avoid it, and "rule" has no countable definition; one ignored rule is the result.
- **"Two points met in round 3 adds route four"**. C04. Carrier: "select the tier by the size of the change". It read whether the plan passes, not the nature of the problem, so it forced a new approach on a plan that had the right direction and needed precision.
- **A pass gate written as "zero high, zero medium on each route"**. C04. Carrier: the Closure Table, with a resolved or unresolved value per problem and a position for each resolved one. A count is a finish line and a forbidden target at the same time; the usual result is a lower severity.
- **Two hints for the stop tests** ("freeze for a run after two rounds with no high or medium problem resolved"; "when no rule can be deleted, add only"). C03 and C01. Carrier: "the round has no executable action", with its four values. The first contradicted "true means continue" at the same state, and its closing action, "write a blind spot", is forbidden in section 1. The second was a second copy.
- **Route names A, B, C**. C08. Carrier: route names as words. To keep the letters would let "route C" and "Tier C" read as one thing.
- **A score, a weight, and a vote count** (not adopted; never deleted). C04. Carrier: the substantive question. A score replaces "can the work start" with a number that has no stable relation to it; the Author improves the number, the reviewer improves the number, and nobody owns the question. A vote count treats "nobody objected" as "no problem", and a real problem that one route finds is the problem with the fewest votes.
- **An exit that skips the review** ("a single-point change that one command verifies and that has no decision point goes straight to work"). C03. Carrier: the ten-round limit and the three levels. The User calls this skill by hand, so no task pulls it in automatically and the failure "a small change enters the full loop" does not occur; one more exit only makes "I do not want a review today" the default. Judge it again only if the skill starts automatically, for example as a permanent rule in `AGENTS.md`.

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

Each risk stays open. The parenthetical is the class whose rules it strains.

- **The main file is no longer one page** (C05, C01). **To judge whether to split it, measure it now: do not trust a number written here.** A hand-maintained measurement owes an update at every change, and a stale fact is exactly the failure this file warns about (F70). Do not use a word count as a reason to split it. To split it, find the section that serves one test only. The test is always the same: is the completion test of each rule clear? A split brings a new risk: nobody reads a pointer. When someone says "I followed the main file and never opened a reference", add the trigger to the table "Which file to read, and when". Do not move the section back.
- **The two products drift apart** (C01). The cross-check runs once, at delivery, and an implementation deviation can make a number in the plan out of date in the record. Watch two failures: the plan holds evidence, reasons, or review history; or the record holds an action list for the Execution Agent only. Move the content back, and do not keep one copy in each place "just in case".
- **"A reviewer reads the plan and the decision half; the Execution Agent reads the plan" fails easily** (C06). A scan route that gets the review history is no longer blind, and a busy Author puts the whole record into the Execution Agent context. Both rules name an action, and both depend on a person who does the check once. No mechanism catches the failure. When material goes missing or extra, add a dispatch template. Do not merge the two products.
- **The level depends on the cost of a wrong action** (C04, C13). The tests are lists now: four for Light, five classes for Deep. A combination of tests still goes wrong. Watch one failure: "a Light level is a reason to do less". If a shared interface gets a Light level, change those tests. Do not replace them with a more abstract principle, and do not return to "three routes always".
- **The boundary between partial delivery and an exit without convergence** (C10) can split a plan that is "a little wrong everywhere" into a partial delivery. When that happens, tighten the rule: each of the three end questions for the ready part has a direct answer. If one has none, exit the whole plan without convergence.
- **Tier B "change one component" overlaps "local repair" of the Adversarial route** (C04). The overlap is not a problem. When the two routes agree, merge the two problems.
- **One limit of ten rounds lets a Light level use all ten** (C13). The limit is not a permission. A plan that meets the pass test should stop at once. Watch the failure "we still have rounds, so review once more". Do not change the limit when you see it. Check first whether that round has an executable action.
- **Prose about code has an accuracy ceiling** (C09, C12). A plan that restates the code keeps one class of finding alive however many rounds it runs: the plan names the wrong location, the wrong branch, or a name that does not exist. Observed 2026-11-27: rounds five to seven of a seven-round run produced mostly this class, and each finding was real, and each one was cheaper to catch in code than in prose. **Signal**: in one round, more than half of the high findings are of this class (location, branch, name, byte arithmetic). **What to do**: report it to the User as "this should move to code", and let the User decide. The Author passes it upward, once per round at most. **This is not an exit gate**: a count decides no close (C04, F10, F65). **Why not a rule**: the cheap part of this class is scriptable — a landing anchor, a name mark, the source column — and what is left is the residue that no wording removes.

## Field Sample: 2026-11-27

One live task ran the loop seven rounds and reached v12 (a Feishu bridge plugin: peer bots wake each other, with a hop counter against a loop). What it confirms, and where it shows a class being breached:

- **Confirms C02.** Each round found three to six high problems, each checked against the code and each holding.
- **Confirms C12.** The mechanism budget held for all seven versions: one `Map` and one field.
- **Confirms C04.** The two gates were used daily, and "high, medium, and low are a summary only; they do not decide a continuation or a close" was the sentence that mattered most. Do not touch it: a count that decides is F10.
- **Breaches C03 and C07.** The three original routes did not sit in the plan session's sub-agent tree and could not be reused, so rounds two to seven each had two brand-new agents doing a full scan. No reviewer then read the position of a closed item. "Fix once, break once" is the product of that gap: v8 dropped v7's `+1`, v11's landing position did not match, v12 moved an order. This is F62 and F63.
- **Confirms C03, second reading.** An audit of the same loop found that "review only the diff each round" plus "a high-problem majority turns to implementation" is exactly the configuration F40 deleted. See "One trade, two rules".

**What the live task did not show.** The rounds never failed to find problems; they failed to keep a found repair. The cost of the loop rose because every round paid for two new faces, and the regression check had no owner. That is a defect of one assumption — that the agent of an earlier round still answers — and not a defect of the full scan. Repair the assumption first. The scan is what makes the four families visible, and three of the four are invisible to a diff.

## Rejected Change Proposals: 2026-11-27

The five proposals of the live task. Two arrived as a correction to a rule: the relation sentence of a landing anchor (C09, F60), and the source of the state and the input in an acceptance row (C09, F61). Two arrived as the reason and the branch of an existing rule: reuse as a safety duty (C07, F62), and the closed-position list of a round where no route can be reused (C03, F63). The three rejections follow, with the failure each one brings back.

| Proposal | Why not | Which deleted configuration it revives |
|---|---|---|
| **Review only the diff** (a change list and an invariant list; a new face checks the change only; the full scan runs in round one only). | A reader of the diff sees no cross-section contradiction and no regression in a line it did not touch. Both families were present in the live task. | "A diff re-review after the budget". See "One trade, two rules". |
| **Stop at a class count** (more than half of the highs are landing-point or compatibility items: stop and turn the rest into a list with bring-back conditions). | A count decides the close, and a landing-point error is Question 1 of the gate, not a blind spot. | The same one, and "a pass gate written as zero high, zero medium on each route". |
| **`supersedes` and `superseded_by` on each decision point.** | A fourth home for a rejected candidate, and a scan route cannot use it. | None. It adds a structure that one rule already carries. |

## Unmerged (one sample)

**Empty.** All seventy recorded failures found a class. Two entries carry no failure at all, and they sit here rather than in a class: the full format of the start instructions (a rule added in the second pass, with no case recorded — SKILL.md section 1, plan item 3), and the overlap between Tier B and the Adversarial local repair (a known overlap, not a problem — see the residual risks).

The two nearest misses are C10 and C12. Each holds exactly one other sample, and in each pair the second sample shares the **cause**, not the symptom. If a later reading finds that either second sample does not share the cause, that class collapses to one sample and it moves into this section. A single sample is not abstracted here: to abstract one accident is to tell a concrete story as a vague sentence, and the vague sentence loses the check.

A future failure that fits no class goes here with its one line, not into the nearest class.

## Appendix: Class Index

| Class | Cause in one line | Cases | Read this rule first |
|---|---|---|---|
| C01 | One fact, several authoritative copies | 9 | The change surface's three lists, with no offset |
| C02 | The producer certifies its own work | 2 | The Author's own check is not sufficient |
| C03 | One state, more than one answer | 7 | The Author makes every close |
| C04 | A cheaper proxy takes the judge's seat | 9 | The counts are a summary only |
| C05 | Cost separates from value, so the review is skipped | 8 | One full scan route each round |
| C06 | A boundary that lives only in a sentence decays | 4 | The dispatch message decides the independence |
| C07 | A repair or a text operation silently removes a test | 5 | Is the completion test of each rule still there? |
| C08 | The rule text does not fix the reader's action | 4 | Five strength words, one form each |
| C09 | The basis is not observable inside the material | 9 | Run it now, or write one falsifiable condition |
| C10 | A two-valued decision on a partly good result | 2 | Partial delivery, or exit the whole plan |
| C11 | Content with no named reader has no owner | 4 | Which reader owns this line? |
| C12 | A new finding has no cheap destination | 2 | The routing table |
| C13 | A relaxation is read as a permission | 3 | The level selects the number of routes only |
| C14 | A deletion loses the failure it guarded | 2 | One line per deletion, naming the carrier |
