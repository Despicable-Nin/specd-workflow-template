---
name: wf-plan
skill: wf-plan
description: Create an implementation/technical plan from an approved task specification. Produces a plan artifact, independent review, and human approval before implementation begins.
---

# @wf-plan

Invoke the [wf-plan skill](../skills/plan/SKILL.md) to create an implementation/technical plan from an approved task specification.

## Usage

```
@wf-plan <project name/path> <task spec ID>
```

## What it does

1. Loads the approved task spec and approved parent project spec
2. Derives the implementation/technical plan
3. Routes to independent review (wf-review)
4. Requires explicit human approval
5. Hands off to wf-implement

## Never

- Plans outside approved task scope
- Implements before plan approval

## Related commands

`@wf-task-code` `@wf-task-noncode` `@wf-plan` `@wf-implement` `@wf-review` `@wf-converge`
