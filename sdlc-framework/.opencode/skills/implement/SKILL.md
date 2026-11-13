---
name: wf-implement
id: wf-implement
version: 1.0.0
description: Implement an approved task specification in its dedicated task worktree using the Red -> Green -> Refactor TDD loop, within the approved plan scope, and against the approved task acceptance criteria.
category: implementation
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-implement

## Purpose
Implement an approved task specification in the task worktree using the Red -> Green -> Refactor TDD loop, writing only within the approved plan/task scope.

## Rule 0 — AGENTS.md binds this skill, always

This skill is bound by the nearest applicable `AGENTS.md` — the repository root `AGENTS.md`, plus
the `AGENTS.md` of any ancestor directory of every path this skill reads or writes. **Read them
before the first action.**

* **Silence is not permission.** A step in this skill that says nothing about a location, a name,
  or a placement rule does not authorise improvising one. The `AGENTS.md` still governs.
* **Conflict.** Protected Invariants > explicit user instruction > `AGENTS.md` > this skill. Where
  this skill and an `AGENTS.md` disagree, follow the `AGENTS.md`, state the conflict, and record
  it in the work ledger. Do not silently pick a side.
* **Hard stop.** If an `AGENTS.md` rule cannot be satisfied — the canonical folder is missing, a
  required `binding.yaml` is absent, the target path is ambiguous — stop, name the violated rule,
  and record a `Blocker` in the work ledger under the Gate Failure Protocol. Never improvise a
  location.
* **Handoff.** Before acting, look for the task's handoff file at its canonical location and read it if it exists - it is the task's running state (purpose, status, action items, next step). A handoff file is **disposable**: when its status becomes `Done` it is deleted, not archived, and the durable history stays in the work ledger. A handoff belongs inside the directory of the work it describes.
* **Code authority.** this skill is the **only** skill permitted to write implementation code. It does so inside the task worktree, against an **approved** task specification, targeting the codebase directory `generated-projects/<project-name>/` — never inside `spec-workspace/`.

## Invocation Conditions
Invoke when:
- An approved task specification AND an approved implementation plan exist, with a dedicated task worktree.

Do not invoke when:
- Task spec or plan is not approved.
- No task worktree exists.

## Preconditions
- Approved task spec (`status: Approved`, `task_type: code` **or** `noncode`).
- Approved plan for the task — the plan run file at
  `spec-workspace/projects/<project-name>/tasks/task-<task-id>-plan.md`, `status: ready-for-implement`.
- Dedicated task worktree checked out on the task branch.

## Required Context
- Approved task spec + approved plan.
- Worktree path / branch.
- The task's handoff file — read it before acting.

## Inputs
| Input | Description | Default |
|---|---|---|
| Task spec ID | Approved task to implement | Required |
| Plan ref | Approved plan for the task | Required |
| Handoff ref | The task's handoff file | Derived from the plan |

## Outputs
| Output | Location | Description |
|---|---|---|
| Implementation | Task worktree | Code changes within approved scope |
| Test evidence | Task worktree / CI | Red -> Green -> Refactor evidence |
| Handoff contribution | Task handoff file | This phase's contribution, appended |
| Work ledger update | Work ledger | Task implementation progress |

## Agent Responsibilities
- **Treat the plan file as the RAG.** Its `## Decisions`, `## Plan`, `## Out of scope`, and recorded
  calibration answers are binding. Do not re-derive intent from the task spec, and do not act on
  anything the plan does not authorise.
- Implement strictly within approved task scope/plan.
- TDD: Red (failing test) -> Green (minimal pass) -> Refactor (clean).
- Report progress in the plan's calibrated chrome (calibration choice 5).
- Run verification per task verification requirements.
- Never weaken protected invariants or add unapproved scope.

## Step-by-Step Procedure
### Step 1 — Load approved context
Read the approved task spec, the approved plan run file, and the task handoff file; confirm the
worktree association. From the plan file, take: the chosen path and why (`## Decisions`), the
implementation layers (`## Plan`), the excluded scope (`## Out of scope`), and the reporting
chrome (calibration choice 5). The plan wins over the task spec wherever they differ.

### Step 2 — Red
Write/adjust the failing test for the next acceptance criterion; run it and confirm failure.

### Step 3 — Green
Implement minimal code to pass; run tests; confirm green.

### Step 4 — Refactor
Refactor within approved scope; re-run tests.

### Step 5 — Verify
Run full task verification (tests, review sign-off per task verification requirements).

### Step 6 — Handoff
Append this phase's contribution (implementation + TDD evidence) to the task handoff file (the task's single common per-task handoff), then hand off to `wf-converge` (and later `wf-commit` after convergence).

## Decision Rules
| Rule | Statement |
|---|---|
| Plan is the source of truth | The approved plan file governs. Where it and the task spec differ, the plan wins. |
| Out of scope is binding | Anything in the plan's `## Out of scope` is off-limits, whatever else might suggest it. |
| Approved scope only | Implement within approved task scope/plan. |
| TDD mandatory | Red -> Green -> Refactor required. |
| No force-push | Never force-push. |

## Delegation Strategy
- Convergence: delegated to `wf-converge`.
- Commit: delegated to `wf-commit` after convergence.

## Approval Gates
- Implementation requires approved task spec + approved plan (Gates 3 and 2 of task/plan phases).

## Safety Boundaries
- No unapproved scope.
- No secrets; no force-push; no discard of uncommitted work.

## Error Handling
| Situation | Handling |
|---|---|
| Tests fail persistently | Record Blocker; do not claim convergence. |

## Validation
- Implementation exists within approved scope.
- TDD loop evidence present.
- No protected invariant violated.

## Handoff Requirements
- Implementation state + test evidence.
- Next recommended action: `wf-converge`.

## Related Skills
- **wf-plan** — approved plan being implemented.
- **wf-converge** — convergence/verification loop.
- **wf-task-code / wf-task-noncode** — produced the approved task spec.
- **wf-commit** — after convergence.
