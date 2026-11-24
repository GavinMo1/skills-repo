# Review Checklists: Guards, Cleanup Tables, Assertions, and Revision Records

Read this file in three cases. You dispatch a review. You check the guard patterns and the acceptance assertions of your own plan. You write the Revision Table of a round. The rules are in the [main file](../SKILL.md). This file gives checkable lists and judgeable examples.

Replace the commands, the error texts, and the field names of each example with the values of the object under review. Do not copy the constants of this project.

## A. Guards and Values: Patterns That Let a Plan Pass or Lose Data

The common point of this class: a functional test passes. The problem shows only with an illegal input or a boundary input. The reviewer must build the input. Do not wait for the Author to name a suspect.

### A1 Fail-open guard

```python
if isinstance(self.data, dict) and not v2_ok(self.data):
    raise SystemExit('version 2 is required')
```

A non-dict record makes the whole expression `False`. The version gate is skipped. This is the opposite of "the gate covers every write command". The test, in one sentence: **put this illegal input in. Does the guard refuse it or let it pass? A pass is a problem.**

Ask the Author for an explicit three-part test. Ask where the gate sits in the branch order, and which commands are exempt. For example, `init` creates the record, so the gate does not cover it.

### A2 Existence and null collapse

```python
self.data = read_json(p) if p.exists() else None
if self.data is not None:   # "file absent" and "content is null" become one state
    ...
```

Effect: the rule "refuse a null record" changes nothing in the literal implementation, because null and "absent" take the same branch. The init flow may also overwrite a record whose content is null without a message. Only the backup file keeps the old content.

Repair: put "exists" and "content" in two fields. Give each of the three tests an error message in Chinese.

```python
self.exists = self.path.exists()
self.data = read_json(self.path) if self.exists else None
# init:  if self.exists: raise 'the state list already exists'
# other: if not self.exists: raise 'initialize the state list first'
#        if not isinstance(self.data, dict): raise 'the state list must be a JSON object'
#        if not v2_ok(self.data): raise 'version 2 is required; migrate the old version first'
```

Assert four inputs: absent, `null`, `[]` (a top-level array), and an old version. For each input, require rc not 0, an error message in Chinese, and no change to the record bytes. For the top-level array, also require no traceback.

### A3 A falsy merge that loses data

```python
files = self.data.get('files') or {}      # an empty dict is also falsy
```

If the getter uses this line, the most common path (init, then register one entry) returns `rc=0 saved:true` and `files` stays `{}`. The entry is lost without a message. An acceptance run of `review` or `check` does not cover the register path.

- A missing key must raise a `ValueError`, or an equivalent with a Chinese message. It must not return an empty container.
- `or {}` may appear in a read-only filter only. The filter must not write back. Name that position in the plan text.
- Add two assertions. With a missing key, the command gives rc not 0 and the record bytes do not change. After `init` then `register`, the item count is 1.

### A4 Code position and exemption

State where an inserted guard sits: **after the "not initialized" guard and before the command dispatch. `init` is exempt.** A guard at the very front turns the clear error "initialize the state list first" into an `AttributeError` traceback. The User sees a stack, not the next action.

### A5 Asymmetry of order and rollback

The commit order and the rollback order are often not the reverse of each other. The commit uses the window "new check script with the old record": change the check first, then the state. The rollback uses "old check with the old record": restore the state first, then the check. The reverse order passes through "old check with the new state". Every command then fails, and the system stays in a middle state that no command can repair.

If the plan says "A first, then B", run both orders in a temporary directory first. Record the exit code of each command in each order. When you write the plan, write four items together: the order, the actions that the window forbids, the fixtures of the rollback acceptance, and the expected codes.

## B. Cleanup Tables and the Uncleared Scope

A cleanup table lists which states and which errors a tool command can clear, and which ones need a manual edit of the storage. Such a table often looks correct and cannot be run.

### B1 Check the message count, not the row count

- The item count of the table must equal the count of error messages that the code really produces. Copy each message from the code position that produces it. Do not list from memory. If the header says "N items", a merged row makes the reviewer count wrong. A machine check must use the message count.
- **Put a repeated message on its own row for each source position.** One message may come from several fields, for example `files.X.owner`, `files.X.contributors[0]`, and `reviews[0]`. The clearing method differs. Give a side rule. For example, a path that starts with `files.` is the author side, and a path that starts with `reviews[` is the reviewer side. Write the prefix that the real schema uses.
- **Give a copyable clear command for each row**, with its placeholders. If no tool can clear the row, write "no tool clears it: a manual edit of the record is required". "Register it again" is not a command.

| Message (as is) | Position | Tool can clear | Command or handling |
|---|---|---|---|
| missing pass record for the current content | `check --final` to `unchecked` | Yes | `state.py review --by <actor> --confirm-current` |
| entity identity unknown | `reviews[0]` | No | A manual edit of `actors` is required. Placeholder: `unknown-<source>-<date>` |

### B2 Do not enlarge the uncleared scope

- A case that a command can clear must not become "unclear" or a blind spot. Typical error: merge the missing identity of the author side with the reviewer side into one row. The author side can change with `register --actor`, and `unchecked` returns to zero.
- A real uncleared case needs three items: why no tool clears it (which command refuses, on which line), the cost, and the condition that must bring you back.
- A manual repair must use a **traceable placeholder** such as `unknown-<source>-<date>`, and the delivery note must say "not verified". Do not invent an identity or a value that looks real. No later check sees it, so the problem stays hidden for ever.

### B3 Run a mechanical action before you write it

Each item below often looks correct in a document and fails at run time. Run it on a temporary copy.

- Can you change the type or the property of a registered item? The usual result: no, except with a manual edit of the storage.
- Can a new record reuse an existing ID? The usual result: no, the command reports a conflict.
- What is the real source of an exit code? Is it "the list already exists", or the version gate? The messages differ, and a wrong assertion merges two paths into one.
- What does each command do with mixed data (new code, old data)? Which commands give rc=1 and write nothing, and which give rc=0 and write?

If a run fails, change the exit in the plan. Use the manual path that really works, or delete the exit. Do not keep a path that does not exist.

## C. Acceptance Assertions

### C1 The table must have three columns

| Recipe (the operation sequence) | Expected exit code | Expected output message set |
|---|---|---|
| (1) `init` (2) `register --kind shared` (3) `check --final` | 2 | `unchecked` holds "missing pass record for the current content" and does not hold "no registered file" |

An assertion that gives the exit code only is not acceptable. **Two different causes often give the same code.** Example: "one review is missing" and "the review conclusion needs a revision" both return rc=2. A code-only check reports a pass, and one whole path stays unchecked. Separate the two causes with the message set, the written fields, or the item count.

### C2 Check the message count, not the row count

A list check ("the cleanup table has 9 items", "5 assertions") uses the message count, not the table row count. One row may hold two messages, or two messages may be the same sentence. Either case misleads the reviewer. Write "a full count by X gives the total, and the sum of the categories equals that total" when you can. Do not give the total only.

### C3 A cited test case must exist

Before you write "covered by T1 and T3", list the full set of test cases: the ID, the script, whether it is new, and which assertion it covers. Each case below counts as not covered.

- The ID does not exist.
- The case exists but does not check this assertion.
- The text says "covered by another case" and names no case.

List the new case count and the cases in a separate script in their own line. Do not mix an existing case into "8 new cases".

### C4 A diff assertion uses content markers, not an item count

An assertion of the form "the change has exactly the four lines below" can agree with the real hunk count by chance. The count matches, the content differs, and the reviewer reports a pass. Use this form:

```
diff -U0 old new | grep -c '^@@'   # must equal 4
each hunk must hold its marker line:
  hunk1 holds <a unique symbol of the old implementation>
  hunk2 holds <a unique passage of the new call site>
  ...
one section declares a zero difference (not counted in 4)
```

Declare a zero-difference item in words: "zero difference, not counted". Without this, the reviewer counts "it was the same before" as "it was changed correctly".

### C5 Coverage self-check

- Each assertion needs at least one case that turns it from red to green. If no input turns it red, the assertion tests nothing.
- Each key path needs one regression case of the form "success, but a field did not change". Example: after a register, the item count is 1. This case catches lost data.
- The exit code of a check command needs its own assertion for each case: an empty record, a missing key, an illegal JSON file. Do not rely on "another assertion covers it".

## D. Source to Revision Table

Write one table after each review round. **One row for each finding.**

| Source | Revision | Changes the implementation action? |
|---|---|---|
| R1F-02 | The state-entry guard becomes three tests: exists, content, version. Section 4 adds an `__init__` item. V11 adds "on a `[]` record, `next` must give rc=1 and an error message". | Yes (mechanism) |
| R2F-01 | The rollback acceptance adds four fixtures and the expected codes (0, 2, 2, 1). The test script joins the replacement order. | Yes (acceptance) |
| R2F-03 | The cleanup table adds "the current content has no pass record" and merges it with an equivalent neighbor. | No (document wording) |
| R3G-09 to 12 | The record gets one Closure Table row for each item. | No (record) |

Rules for the columns:

- **Source**: the route name and the stable problem ID. If several routes report one problem, list them together (`R1F-02 / R3G-04`). Do not write "various places", "related problems", or "per the review".
- **Revision**: the section and the rule, and the new text. "Fixed" and "handled" are not revisions, and a reviewer cannot check them.
- **Changes the implementation action?**: two values only, **Yes** and **No**. Yes means the change touches a command, a state, an order, an acceptance test, or the handling of data during the implementation. No means wording, a typo, assertion precision, a record addition, or an item already in a blind spot. It also covers a change that the implementation can absorb in place. If you cannot decide, write Yes.
- The column matches the stop test "the round has no executable action" in section 4 of the main file. If every row is "No", the round stops as no action. If one row is "Yes", the round has an action.
- Do not write a status in this table. Write it in the Closure Table: resolved, partly resolved, or unresolved, with the evidence position.
