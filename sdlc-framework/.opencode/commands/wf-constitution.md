---
name: wf-constitution
skill: wf-constitution
description: Establish or update the project constitution — durable engineering principles that steer specifications, planning, implementation, and review. Cannot weaken protected framework invariants.
---

# @wf-constitution

Invoke the [wf-constitution skill](../skills/constitution/SKILL.md) to establish or update the project constitution.

## Usage

```
@wf-constitution <project name/path> [principles]
```

## What it does

1. Gathers engineering principles (quality, testing, security, performance, process)
2. Drafts the constitution
3. Routes to independent review (wf-review)
4. Requires explicit human approval
5. Records the approved constitution

## Never

- Weakens protected framework invariants
- Writes executable content
- Silently overwrites an existing constitution

## Related commands

`@wf-bootstrap` `@wf-plan` `@wf-task-code` `@wf-task-noncode` `@wf-review` `@wf-converge`
