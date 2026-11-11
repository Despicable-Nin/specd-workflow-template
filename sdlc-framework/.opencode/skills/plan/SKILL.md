---
name: wf-plan
id: wf-plan
version: 1.0.0
description: Create an implementation/technical plan from an approved task specification (and its approved parent project specification). Produces a plan artifact, independent review, and human approval before implementation begins.
category: planning
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-plan

## Purpose
Create an implementation/technical plan from an approved task specification, tracing planned work back to the approved task acceptance criteria and the approved parent project specification.

## Invocation Conditions
Invoke when:
- An approved task specification exists (via `wf-task-code` / `wf-task-noncode`) and planning is required before implementation.

Do not invoke when:
- No task specification is approved (use `wf-task-code` / `wf-task-noncode` first).

## Preconditions
- Approved task specification at `spec-workspace/projects/<project-name>/tasks/task-<nnn>-<type>.md` with `status: Approved`.
- Approved parent project specification.

## Required Context
- Approved task spec ID and content.
- Approved project specification.
- Existing implementation (read-only).

## Inputs
| Input | Description | Default |
|---|---|---|
| Task spec ID | Approved task to plan for | Required |
| Scope | Planning scope | Task scope |

## Outputs
| Output | Location | Description |
|---|---|---|
| Implementation plan | `spec-workspace/projects/<project-name>/plans/task-<nnn>-plan.md` | Technical/implementation plan |
| Review findings | Work ledger + reviewer output | Evidence-based findings |
| Approved plan | Same file, approved | Human approval recorded |

## Agent Responsibilities
- Derive the plan strictly from the approved task spec and parent spec.
- Define architecture, components, data flow, and verification approach.
- Submit to independent review (`wf-review`, type `architecture` / `implementation`).
- Enforce the approval gate before implementation.

## Step-by-Step Procedure
### Step 1 — Load approved inputs
Read the approved task spec and approved parent project specification; record their IDs.

### Step 2 — Derive the plan
Draft the plan: objectives, approach, components, boundaries, data flow, risks, and verification strategy. Trace each plan element to task acceptance criteria.

### Step 3 — Independent review
Submit to `wf-review`. The reviewer must challenge assumptions, missing requirements, defects, regression risks, unnecessary complexity.

### Step 4 — Approval gate
Present plan + findings to the human. On approval: record as approved plan. On rejection/blocking findings: return to drafting.

### Step 5 — Handoff
Hand off to `wf-implement` with the approved plan and task spec.

## Decision Rules
| Rule | Statement |
|---|---|
| Traceability | Every plan element must trace to an approved task acceptance criterion. |
| No scope creep | The plan must not add unapproved scope. |
| Approved before implement | Implementation begins only after plan approval. |

## Delegation Strategy
- Independent review: delegated to `wf-review`.

## Approval Gates
| Gate | What | Who |
|---|---|---|
| Gate 1 | Draft plan review | Reviewer agent / `wf-review` |
| Gate 2 | Plan approval | Human |

## Safety Boundaries
- No implementation before plan approval.
- No unapproved scope in the plan.

## Error Handling
| Situation | Handling |
|---|---|
| Plan approval denied | Stop; plan stays `Draft`; record Blocker. |

## Validation
- Plan exists, approved, traces to approved task spec.
- No protected invariant violated.

## Handoff Requirements
- Approved plan path/version.
- Next recommended action: `wf-implement` with approved task spec + plan.

## Related Skills
- **wf-task-code / wf-task-noncode** — produce the approved task spec.
- **wf-implement** — consumes the approved plan.
- **wf-review** — reviews the draft plan.
