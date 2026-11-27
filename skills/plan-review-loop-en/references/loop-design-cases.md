# Design Cases: The Record Behind Each Failure Class

**This file is not a runtime instruction, and it is not the design notes.** It is the lookup table behind [Design Notes](loop-design.md): every recorded failure, one line each, grouped by the class that explains it, then the anchor ledger and the pass log.

Read it in three cases only: you look up the case behind a rule; you decide whether a rule that carries only an inference is a deletion candidate; you ask who keeps the aim of a deleted rule. Do not read it on a round of the loop, and do not read it to understand the classes. The classes, their causes, their rules, and their identification test are in the design notes. This file holds no rule.

A case is marked **†** when its rule is new and had no case at the time of writing. **✗** marks a proposal that would bring a deleted failure back. **⋄** marks a near miss seen while the 2026-11-27 change was written; the rule closed it in the same change, and the design notes record it first.

## C01 · One fact, more than one authoritative copy

- **F03** The "three capacity items" of `user-profile-repo` v1.0 sat in three places, each changing on its own, and a rule count showed nothing → report new positions and deleted-or-merged rules as two separate lists, with no offset between the counts.
- **F25b** A changed decision left the sentences that cite it in the plan with no owner → the test "the two products agree" in gate 3.
- **F28** The code samples of the failure-mode table, the field rules of the Revision Table, and the three acceptance-assertion rules sat in the main file as a second copy of checklist sections A, C, and D → the main file keeps one test and one pointer.
- **F30** The three context-isolation rules had two owners, and the two copies differed → one owner, in the protocol section that held the fuller text.
- **F45** "When no rule can be deleted, add only" pointed the same way as "do not answer a new finding with a new rule" → the second copy is deleted; "the round has no executable action" carries both.
- **F51** An implementation deviation made a number in the plan out of date in the record → the two products are cross-checked at delivery; move the content back, and do not keep a copy in each place.
- **F66 ✗** A proposal to add `supersedes` and `superseded_by` to each decision point: a fourth home for a rejected candidate, while the table column, the Choice List, and the record already hold three → rejected; prefix the stable number with the version (`v11-D3`) and add one line to the dispute table, "a decided item changes only with new evidence".
- **F67 ⋄** A new column arrived in the acceptance table, and the sentence that enumerates the acceptance rules still named the old set, so the pointer was short by one member → the enumeration gained the new member in the same change. A list that enumerates the members of a set is a copy of that set: when a member arrives, the list gains it, or the pointer lies.
- **F70 ⋄** This file carried the main file's line count and character count as a hand-maintained figure ("329 lines and about 13,000 characters", then "397 and 43,000"), and every change of the main file owed it an update that nobody collected → the figure is deleted; the residual risk now says "measure it now: do not trust a number written here". A fact that one command produces is measured, not copied.

## C02 · The producer certifies its own work

- **F02** Of eight implementation deviations, two real problems came from the reviewer — the Choice List written twice, and the round archive that contradicted itself — and the Author's own check found neither → do not let the Author enumerate the consistency conclusions.
- **F19** Six tables each round, four of them the Author's own proof, while the real risk was the Author approving its own work → one Closure Table and one Revision Table.

## C03 · One state, more than one answer

- **F11** A disagreement about feasibility was answered with "use the higher severity" → the severity rule is limited to one problem with two severities; feasibility goes to the dispute table.
- **F21** The close test and the pass test had different sources, so one state had two answers → a reviewer reports problems and the two gate values, and gives no close decision.
- **F40** A diff re-review after the budget overlapped two other rules, so one state had three answers and the reader took the cheapest → deleted, because "one full scan route each round" already carries the cost side and a second exit is not needed.
- **F44** "Freeze for a run after two rounds with no high or medium problem resolved" contradicted "true means continue" at the same state, and its closing action "write a blind spot" is forbidden in section 1 → "the round has no executable action" carries it.
- **F49 ✗** A proposed exit that skips the review ("a single-point change that one command verifies goes straight to work"): one more exit makes "I do not want a review today" the default → not adopted. Judge it again only if the skill starts automatically.
- **F63** Every round paid for a new face, and no reviewer read the position of a closed item, because the three original routes did not sit in the plan session's sub-agent tree and could not be reused; rounds two to seven each carried two brand-new agents doing a full scan → the closed-position list, and a written "no regression protection" when it cannot be built. Observed on 2026-11-27: the position regression of closed items had no owner in any round.
- **F64 ✗** A proposal to review only the diff: it revives the deleted exit of F40 and breaks the pair that "One trade, two rules" records in the design notes → rejected; see C07 for the damage that a diff reader cannot see.

## C04 · A cheaper proxy takes the judge's seat

- **F10** "Most routes judged it low" hid a real problem, and the cheapest close became the default → no pass by a vote count; the counts are a summary only.
- **F17** One switch, "add a route or not", for three sizes of change → three tiers, A, B, C, each with its own trigger and cost.
- **F18** Six process lists became the pass test, and "the tables exist" took the place of "the work can start" → the pass test is two groups: the plan is ready to start, and the record is auditable.
- **F39** A fixed three routes ("use three routes even for a simple plan") removed the judgment instead of recording it → three levels, selected by the cost of a wrong action. A Light level is not its return: it needs all four criteria, each with evidence.
- **F41** An "area that does not grow" gate on the rule count, the parameter count, and the acceptance item count invited merge and rewording to avoid it, and one ignored rule was the result → deleted; the content test carries it, because "rule" has no countable definition.
- **F42** "Two points met in round 3 adds route four" read whether the plan passes, not the nature of the problem, so it forced a new approach on a plan that had the right direction and needed precision → select the tier by the size of the change.
- **F43** A pass gate written as "zero high, zero medium on each route": a count is a finish line and a forbidden target at the same time, so the usual result was a lower severity → the Closure Table carries it, and the count became a summary.
- **F47** A score, a weight, a vote count: the Author improves the number, the reviewer improves the number, and nobody owns the question "can this plan be implemented" → never adopted; the substantive question decides.
- **F65 ✗** A proposal to stop at a class count ("more than half of the highs are landing-point or compatibility items: stop and turn the rest into a list") → rejected: a count decides the close, and a landing-point error is Question 1 of the gate, not a blind spot.

## C05 · The cost of the review separates from the value, and the person skips the review

- **F13** Every route re-read everything, so the cost separated from the value, and "was the full check really done" was not observable → one full scan route each round, and every other route checks the Closure Table only. See "One trade, two rules" in the design notes.
- **F14** A three-line change started a table and two routes, and the cost was high enough that people avoided the review → three levels, with the four Light criteria written down.
- **F20** A low problem got a full check per item: full cost for noise that decides nothing → a low problem needs no item-by-item check.
- **F29** The six archive rules, the Evidence templates, and the Choice List groups sat on the round path, though the Author uses them only when it writes a file or the record → moved into the protocol sections that name the trigger.
- **F31** The round arithmetic of the Alternative route sat in the main file, though the Author uses it only when it starts an alternative → moved to alternative-review.md "Rounds and Route Accounting".
- **F32** The four values of "the round has no executable action" sat in the main file, though the Author uses them only at the stop decision → moved to the protocol section "Delivery Check", then brought back when the fifth pass showed every branch reads it.
- **F38** A block that every round reads sat in its own file, and two tests replaced "how often is it read": does every branch read it, and is it a test or a format → two blocks came back: the five file-location rules, and the four values of an executable action.
- **F50** The main file stopped being one page, and a split brings a new risk: nobody reads a pointer → do not split for a word count; add the trigger when someone reports a pointer they did not follow.

## C06 · A boundary that lives only in a sentence decays

- **F12** A new agent was called a blind review, and the independent review became a second echo → the dispatch message defines the blindness, and it holds no reason of the Author.
- **F25a** The rules said what to give a reviewer, and nothing about the implementer → context isolation at implementation dispatch, with the delete-list and its one-sentence test.
- **F52** The isolation rules name an action and depend on a person who does the check once; no mechanism catches it (a scan route that gets the review history is no longer blind, and a busy Author pastes the whole record) → the boundary is carried by a dispatch artifact and by a line in the record, not by a sentence.
- **F69 ⋄** The closed-position list was required, and the rule did not say what the list must not hold, so the channel that leaks history into a blind route opened by itself → the list holds no history, no conclusion, no problem ID, and no wording of the original problem. A boundary that names only what the artifact must carry leaves the other direction open.

## C07 · A repair or a text operation silently removes a completion test

- **F33** During a compression pass, "no vote count, no higher severity" went missing from the "two routes disagree" row → **the position must not move**, because `multi-route-review.md` and this design file both point to that row; a read-only re-review found the loss, and the line was restored.
- **F34** In the first version of the Split pass, two tests went missing while sentences were shortened: "no vote count, no higher severity", and "handle each new high or medium problem" → a move down gets an independent line-by-line read against the backup.
- **F36** Nine forms of strength carried two levels, and two heavy sentences held two requirements each at a clause boundary → the five strength words, one form each; a clause boundary carries no second requirement.
- **F37** A wording pass produced four kinds of damage — a prohibition became neutral guidance, a clause of a list went missing, a conjunction became a disjunction, an exception test became an example — each found by a read-only re-review, never by the Author's own check → the four kinds are a check list for any wording pass.
- **F62** Three versions of one plan broke an earlier repair: v8 dropped the `+1` that v7 had put in, v11 landed on a position that did not match the decision, and v12 moved an order. The Closure Table still said resolved, and the repair read only the passage it changed → reuse is a safety duty, not only a saving. Observed on 2026-11-27, seven rounds, v12.

## C08 · The rule text does not fix the reader's action

- **F04** "Count it against the round limit" gave no number, so the person at that step invented one and nobody checked it: the main file cited the limit in four places and gave no digit → ten rounds, written as a digit, for all levels, and the count is not reset.
- **F27** Four invented terms explained each other — released item, trigger item, dead state, judged item — and a rule gave no action → disclosed item, must change, uncleared, one test; each term names an action.
- **F35** Nine forms expressed two levels of strength, and no script could read them → five forms, one per word, and a script reads the five.
- **F46** Route names A, B, and C stayed after Tier A, B, and C arrived, so "route C" and "Tier C" read as one thing → route names are words.

## C09 · The basis of a judgment is not observable inside the material under review

- **F06** "It looks supported" took the place of support, and a passage supported a conclusion that the full text rejected → an anchor and a falsifiable condition for a Core Precondition.
- **F07** The Author read the source and inferred "the script runs this way", and the run took another branch → an executable precondition runs in an isolated directory.
- **F09** The Author forwarded "fixed" and pointed to no rule → the Closure Table carries a position evidence, and no position counts as open.
- **F16** A fact that one command could show became a question for the User; the User could not answer, and the same wrong conclusion returned → run a to-verify fact by default, and park it on the unverified list only when no command can show it.
- **F48** Question 2 of the gate needed four versions before anyone saw that it asked "what did the User say", which is not in the text under review. Question 1 never had the problem, because its operands sit in the text → test one: do all the operands of a test sit inside the text under review?
- **F60 †** A name that exists was accepted as the landing point while the decision sat one call away: "change `onInbound`" passes a search for `onInbound`, and the decision sits in `route` → the landing anchor's second part, the sentence that names the deciding symbol.
- **F61 †** A fixture wrote the state that the entry point writes: the assertion passed and the entry point itself never ran → the second column of the acceptance table, with a producer named for a production path.
- **F68 ⋄** The rule required a producer for a claimed production path, and it did not say which class a cell falls into when no producer can be written, so the claim stayed assertable and out of reach of a search → a cell that names neither counts as hand-made. A rule that names the good case and not the empty case leaves the empty case to the reader.

## C10 · A two-valued decision is applied to a result that is partly good

- **F15** A plan that was 80 percent ready was returned whole, and the User got no usable part → partial delivery, with the ready part's start instructions complete.
- **F54** The boundary between partial delivery and an exit without convergence could split a plan that is "a little wrong everywhere" into a partial delivery → each of the three end questions for the ready part needs a direct answer, or the whole plan exits.

## C11 · Content with no named reader has no owner

- **F05** The decision history filled the context of the Execution Agent, and the goal named the User as the reader of a product that the Execution Agent must read → two products by reader, each with its own test.
- **F22** The old third end question, "why did we decide this", is the question of an auditor; inside the execution product it forced the plan to hold history, which fights "the plan becomes shorter" → the three end questions use the execution view.
- **F23** The Decision Table's anchors, properties, and rejection conditions used too much of the Execution Agent context → the table moved into the record, and the plan keeps `Decision N` only.
- **F26** The required fields had no reader, so the record grew into a file nobody reads → the record names its reader section by section.

## C12 · A new finding has no cheap destination, so every answer is more text

- **F01** Every new finding became a new paragraph: the plan of this skill grew from 11,784 bytes to 29,768 bytes, and 17 versions only added text → the routing table gives every finding a destination that is not a new rule.
- **F08** The Author could not say "I do not know this", so the deletions never stopped → the Blind Spot List, with its name and its return condition, and the clause that a blind spot is not a new rule.

## C13 · A relaxation, or a leftover budget, is read as a permission

- **F24** A Light level was exempt from the Decision Table; after the table moved into the record, the exemption saved plan space only, and it hid the case "a Light level cannot say why we decided this" → no exemption, for any level.
- **F53** The four Light tests were read as "a Light level is a reason to do less" → the tests are a list with evidence per criterion, and a shared interface moves the level up.
- **F56** One limit of ten rounds let a Light level use all ten, and the failure "we still have rounds, so review once more" followed → the limit is not a permission; check whether the round has an executable action first.

## C14 · A deletion loses the failure that the deleted rule guarded

- **F57** A deleted rule whose aim nobody recorded came back as a mechanism in the next pass → maintenance item 5: one line here per deletion, naming who keeps the aim.
- **F58** Fifteen rules carry only an inference: no recorded failure stands behind them, so nobody can tell whether they defend anything → the inference mark, and the rule that such a rule is a deletion candidate rather than a reason to keep it.

## Anchor Ledger

Seven rules have a real anchor. Fifteen carry an inference only, and each one is a **deletion candidate, not a reason to keep it**. Three of the fifteen are new and have no case yet — F60, F61, and the channel rule of checklist C5: give each one chance. Read the class before you delete one.

| Rule | Class | Anchor |
|---|---|---|
| The routing table for a new finding | C12 | This skill's own plan: 11,784 to 29,768 bytes, 17 versions, additions only |
| The Author does not enumerate the consistency conclusions | C02 | Two of eight implementation deviations came from the reviewer; the Author's own check found neither |
| The change surface reports new positions and deleted or merged rules, with no offset between the counts | C01 | The three capacity items of `user-profile-repo` v1.0 sat in three places |
| A fixed budget of ten rounds, the same for all levels | C08 | The main file cited the limit in four places and gave no digit; the User set ten rounds on the spot |
| Two products by reader | C11 | The User said on 2026-11-24 that the earlier goal named the User as the reader |
| Reuse as a safety duty: the position of a closed item | C07 | 2026-11-27, seven rounds, v12: v8 dropped v7's `+1`, v11 landed on the wrong position, v12 moved an order, and the Closure Table said resolved each time |
| The closed-position list of a round with no reusable route | C03 | 2026-11-27: the three original routes sat outside the plan session's sub-agent tree, rounds two to seven had no reusable route, and the regression check of closed items had no owner in any round |

Inference only. One line per rule, so that a rule can be retired on its own:

- An anchor and a falsifiable condition for a Core Precondition — C09, F06.
- An isolated run of an executable precondition — C09, F07.
- The Blind Spot List, and the rule that a blind spot is not a new rule — C02 and C12, F08.
- The Closure Table with a position evidence — C09, F09.
- No pass by vote count or average score — C04, F10.
- A minimum check when two routes disagree — C03, F11.
- The dispatch message defines the blindness — C06, F12.
- One full scan route each round — C05, F13.
- Three levels, with the four Light criteria written down — C05 and C13, F14.
- Partial delivery — C10, F15.
- Run a to-verify fact by default instead of parking it on a list — C09, F16.
- Three tiers for an alternative solution — C04, F17.
- The relation sentence of a landing anchor — C09, F60. New, no case yet.
- The source of a state or an input in an acceptance row — C09, F61. New, no case yet.
- The channel that an assertion reads and the channel under test — C09, no ID yet. New, no case yet.

The three rules marked "new, no case yet" arrived with the 2026-11-27 change. Give each one chance. The channel rule has no case and no ID: give it an ID on the day a failure arrives, and until then do not delete it for having no anchor — it has not had its chance.

## Pass Log

Each pass kept its lesson. The lesson is a rule now; the class holds it.

| Pass | What it did | What it taught |
|---|---|---|
| 2026-11-24, first | The pass test from six lists to two groups by reader; six tables to two; the Decision Table into the record; the terms rewired | An artifact of the process is not the outcome (C04); a product with no named reader grows or rots (C11) |
| 2026-11-24, second | Added three rules only: context isolation, the two-products cross-check, the full format of the start instructions. It changed no round rule, no level rule, no gate, and no tier | A rule can be complete for the reviewer and silent for the implementer (C06) |
| 2026-11-24, third: move the details down, change no test | Deleted no test and added no mechanism; moved the sections that serve one test only into `references/`; deleted the repeated copies | **A pointer silently removes a test.** Only an independent read-only review that compares each line with the backup found the two lost tests (C07) |
| 2026-11-24, fourth: wording only | Five strength words, one form each; heavy sentences split at the clause boundary; then the six reference files took the same treatment | Four kinds of damage follow a wording pass, and none of them is visible to the Author's own read (C07) |
| 2026-11-24, fifth: two blocks came back | Two tests replaced "how often is it read": does every branch read it, and is it a test or a format | Placement follows consumption, not frequency (C05) |
| 2026-11-27: the live task | One plan, seven rounds, twelve versions, three to six high problems each round, each one holding against the code. Five changes proposed: four adopted, three rejected | Reuse is a safety duty, not a saving (C07); a diff reads no cross-text contradiction (C07); a count decides no close (C04) |

**The lesson of the eight passes on 2026-11-22 and 2026-11-23** is more useful than the number of attempts: to judge whether a test can be used, first check whether all its operands sit inside the text under review. See F48.
