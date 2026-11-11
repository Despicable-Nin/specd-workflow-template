---
name: wf-constitution
id: wf-constitution
version: 1.0.0
description: Establish or update the project constitution — the durable set of engineering principles (quality, testing, security, performance, process) that steer specifications, planning, implementation, and review. Cannot weaken protected framework invariants.
category: governance
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-constitution

## Purpose
Establish or update the project constitution: the durable, versioned set of engineering principles that guide specification, planning, implementation, and review for a project.

## Invocation Conditions
Invoke when:
- A new project is being bootstrapped and principles must be captured alongside (or before) the specification.
- An existing project's constitution must be updated or versioned.

Do not invoke when:
- A current, approved constitution already exists and no change was requested.

## Preconditions
- Project context exists (or is being created via `wf-bootstrap`).
- Human stakeholders available for principle input.

## Required Context
- Project domain and business objectives.
- Candidate principles (quality, testing, security, performance, process).

## Inputs
| Input | Description | Default |
|---|---|---|
| Principles | Candidate engineering principles | None (required) |
| Scope | Constitution scope (project / domain / system) | Project |
| Version | Constitution version | 1.0 |

## Outputs
| Output | Location | Description |
|---|---|---|
| Project constitution | `spec-workspace/projects/<project-name>/constitution.md` | Versioned principles, `status: Draft` → approved |
| Review findings | Work ledger + reviewer output | Evidence-based findings |
| Approved constitution | Same file, approved | Human approval recorded |

## Agent Responsibilities
- Gather principles from stakeholders with explicit trade-offs.
- Draft the constitution; keep it free of executable content and free of protected-invariant weakening.
- Route to independent review (`wf-review`, type `spec`).
- Enforce the approval gate before adoption.

## Step-by-Step Procedure
### Step 1 — Gather principles
Collect candidate principles across quality, testing, security, performance, and process. Record rationale and trade-offs; no principle is adopted without rationale.

### Step 2 — Draft constitution
Write the constitution with YAML frontmatter (`constitution_id`, `version`, `status: Draft`, `project`, timestamps).

### Step 3 — Independent review
Submit to `wf-review` (spec/constitution). The reviewer must challenge assumptions and findings; every finding needs evidence, severity, location, reasoning, resolution.

### Step 4 — Approval gate
Present draft + findings to the human. On approval: set `status: Approved`, record approval as a Work Ledger `Decision`.

### Step 5 — Record and link
Link the approved constitution to the project specification and initial work ledger entries.

## Decision Rules
| Rule | Statement |
|---|---|
| Invariants are absolute | The constitution can never weaken a Protected Invariant. |
| No silent overwrite | Existing constitutions are not silently overwritten. |
| Versioned | Constitutions are versioned; supersession is explicit. |

## Delegation Strategy
- Independent review: delegated to `wf-review`.

## Approval Gates
| Gate | What | Who |
|---|---|---|
| Gate 1 | Draft constitution review | Reviewer agent / `wf-review` |
| Gate 2 | Human approval | Human |

## Safety Boundaries
- Constitution contains no executable content.
- Cannot weaken protected invariants.
- Never silently overwrite an existing constitution.

## Error Handling
| Situation | Handling |
|---|---|
| Approval denied | Stop; constitution stays `Draft`; record Blocker. |
| Blocking findings | Return to drafting; re-review; re-approve. |

## Validation
- Constitution file exists with approved status and version.
- Approval evidence recorded in Work Ledger.
- No protected invariant weakened.

## Handoff Requirements
- Approved constitution version + path.
- Next recommended action (typically `wf-plan` or task creation via `wf-task-code` / `wf-task-noncode`).

## Related Skills
- **wf-bootstrap** — creates the project specification this constitution informs.
- **wf-plan** — next phase after constitution.
- **wf-task-code / wf-task-noncode** — task creation from an approved constitution/spec.
- **wf-review** — independent review of the draft constitution.
