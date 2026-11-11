---
name: wf-implement
skill: wf-implement
description: Implement an approved task specification in its dedicated task worktree using the Red -> Green -> Refactor TDD loop, within the approved plan scope, and against the approved task acceptance criteria.
---

# @wf-implement

Invoke the [wf-implement skill](../skills/implement/SKILL.md) to implement an approved task specification in its dedicated task worktree.

## Usage

```
@wf-implement <project name/path> <task spec ID> <worktree path/branch>
```

## What it does

1. Loads the approved task spec + approved plan
2. Runs the Red -> Green -> Refactor TDD loop in the task worktree
3. Verifies against task verification requirements

## Never

- Implements outside approved task/plan scope
- Weakens protected invariants

## Related commands

`@wf-plan` `@wf-task-code` `@wf-task-noncode` `@wf-implement` `@wf-converge` `@wf-commit`
