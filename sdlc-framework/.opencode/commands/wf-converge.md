---
name: wf-converge
skill: wf-converge
description: Run the convergence loop — verify implemented work against approved task acceptance criteria and produce a final convergence verdict.
---

# @wf-converge

Invoke the [wf-converge skill](../skills/converge/SKILL.md) to run the convergence loop.

## Usage

```
@wf-converge <project name/path> <task spec ID>
```

## What it does

1. Gathers implementation evidence (tests, build, review)
2. Evaluates against approved task acceptance criteria
3. Issues a convergence verdict (`Converged` / `Not Converged`)

## Never

- Declares convergence without evidence
- Commits before convergence verdict

## Related commands

`@wf-implement` `@wf-task-code` `@wf-task-noncode` `@wf-review` `@wf-commit` `@wf-converge`
