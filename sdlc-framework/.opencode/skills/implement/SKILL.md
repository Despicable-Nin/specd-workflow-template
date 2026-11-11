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

## Invocation Conditions
Invoke when:
- An approved task specification AND an approved implementation plan exist, with a dedicated task worktree.

Do not invoke when:
- Task spec or plan is not approved.
- No task worktree exists.

## Preconditions
- Approved task spec (`status: Approved`, `task_type: code`).
- Approved plan for the task.
- Dedicated task worktree checked out on the task branch.

## Required Context
- Approved task spec + approved plan.
- Worktree path / branch.

## Inputs
| Input | Description | Default |
|---|---|---|
| Task spec ID | Approved task to implement | Required |
| Plan ref | Approved plan for the task | Required |

## Outputs
| Output | Location | Description |
|---|---|---|
| Implementation | Task worktree | Code changes within approved scope |
| Test evidence | Task worktree / CI | Red -> Green -> Refactor evidence |
| Work ledger update | Work ledger | Task implementation progress |

## Agent Responsibilities
- Implement strictly within approved task scope/plan.
- TDD: Red (failing test) -> Green (minimal pass) -> Refactor (clean).
- Run verification per task verification requirements.
- Never weaken protected invariants or add unapproved scope.

## Step-by-Step Procedure
### Step 1 — Load approved context
Read approved task spec + approved plan; confirm worktree association.

### Step 2 — Red
Write/adjust the failing test for the next acceptance criterion; run it and confirm failure.

### Step 3 — Green
Implement minimal code to pass; run tests; confirm green.

### Step 4 — Refactor
Refactor within approved scope; re-run tests.

### Step 5 — Verify
Run full task verification (tests, review sign-off per task verification requirements).

### Step 6 — Handoff
Hand off to `wf-converge` (and later `wf-commit` after convergence).

## Decision Rules
| Rule | Statement |
|---|---|
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
