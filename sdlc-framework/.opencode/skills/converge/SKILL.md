---
name: wf-converge
id: wf-converge
version: 1.0.0
description: Run the convergence loop: verify implemented work against approved task acceptance criteria using collected evidence (tests, build, review) and produce a final convergence verdict.
category: quality
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-converge

## Purpose
Run the convergence loop to determine whether implemented work has converged against the approved task specification, using verifiable evidence.

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
* **Code authority.** this skill writes **no implementation code**. It produces a verdict and the evidence references behind it.

## Invocation Conditions
Invoke when:
- Implementation work exists (via `wf-implement`) against an approved task spec.

Do not invoke when:
- No implementation is pending.

## Preconditions
- Approved task spec with acceptance criteria.
- Implementation evidence (tests, build, review).

## Required Context
- Task spec ID + acceptance criteria.
- Implementation evidence.

## Inputs
| Input | Description | Default |
|---|---|---|
| Task spec ID | Task to converge | Required |

## Outputs
| Output | Location | Description |
|---|---|---|
| Convergence verdict | Work ledger + report | `Converged` / `Not Converged` |
| Findings | Work ledger (`ReviewFinding`) | Blocking issues, if any |

## Agent Responsibilities
- Collect evidence: test results, build output, review findings.
- Compare evidence against approved task acceptance criteria.
- Issue a convergence verdict.
- If `Not Converged`, loop back to `wf-implement` with the remaining gaps.

## Step-by-Step Procedure
### Step 1 — Gather evidence
Collect test/build/review evidence relevant to the task.

### Step 2 — Evaluate against acceptance criteria
Map each acceptance criterion to evidence; identify unmet criteria.

### Step 3 — Verdict
- **Converged**: all acceptance criteria met with evidence; proceed to `wf-commit`.
- **Not Converged**: blocking gaps remain; loop back to `wf-implement`.

### Step 4 — Record
Record the convergence verdict into the task handoff file (the task's single common per-task handoff), and when the verdict is `Converged`, mark the task handoff status as `Done`. Also record, if applicable, new `ReviewFinding` items.

## Decision Rules
| Rule | Statement |
|---|---|
| Evidence-based | Convergence requires evidence, not assumption. |
| Loop | Not converged loops back to implementation. |

## Delegation Strategy
- Implementation: delegated to `wf-implement`.
- Commit: delegated to `wf-commit` after convergence.

## Approval Gates
- Convergence verdict is the completion gate before commit.

## Safety Boundaries
- Never declare convergence without evidence.
- Never skip review findings.

## Error Handling
| Situation | Handling |
|---|---|
| Evidence missing | Verdict `Not Converged`; do not proceed. |

## Validation
- Verdict recorded with evidence basis.
- If `Converged`: task ready for commit.

## Handoff Requirements
- Convergence verdict + rationale.
- Next recommended action: `wf-commit` (or back to `wf-implement` if not converged).

## Related Skills
- **wf-implement** — implementation being verified.
- **wf-review** — review findings feeding convergence.
- **wf-commit** — after convergence.
