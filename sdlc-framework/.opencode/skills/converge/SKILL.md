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
Record convergence verdict and, if applicable, new `ReviewFinding` items.

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
