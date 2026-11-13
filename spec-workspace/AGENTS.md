# spec-workspace/AGENTS.md

# Specification Workspace Steward

*(This file governs the storage, retrieval, and lifecycle of all knowledge, decoupled from code
implementation. It is subordinate to the root `AGENTS.md` and inherits its Rule 0.)*

## Rule 0 applies here

Every skill touching this tree — including `wf-state`, `wf-reconcile`, `wf-review`, and
`wf-commit` — is bound by the root `AGENTS.md` Rule 0. Read the root contract before acting.

## 1. Purpose

This workspace manages all reusable and project-specific specifications, ensuring they are
technology-agnostic records of intent.

**This tree never contains implementation code.** If a deliverable requires code, it belongs in
`generated-projects/<project-name>/` and is raised as a separate coding task through
`wf-task-code`. See root `AGENTS.md` Section 4, the code-generation guardrail.

## 2. Directory structure

| Path | Purpose |
|---|---|
| `library/` | General, reusable, technology-agnostic artifacts. Cannot reference implementation details. |
| `library/Engineering/` | Cross-cutting engineering practices and constraints. |
| `library/Capabilities/` | Reusable capability specifications. |
| `projects/<project-name>/` | The complete specification collection for one project. Lowercase, hyphenated. |
| `projects/<project-name>/tasks/` | Task specifications, calibration records, and the one handoff per task. |
| `projects/<project-name>/schema/` | Normative renderings of data contracts. |
| `projects/<project-name>/binding.yaml` | Pointer from this collection to its codebase. |
| `projects/<project-name>/service-contracts.yaml` | Runtime service-to-service dependency manifest. |
| `tasks/` | Framework-level handoffs, not project-scoped. |
| `project-temp/work_ledger.yaml` | The persistent work ledger — the local source of truth for all work. |
| `SDLC-SOR-v1.0.md` | The framework's own system-of-record definition. |

## 3. Key process — specification lifecycle

The system enforces the state machine: `Draft -> In_Review -> Approved -> Superseded`.

`wf-bootstrap` creates project specifications. `wf-review` is the independent review gate before
approval. Task specifications are created by `wf-task-code` and `wf-task-noncode`, each subject to
`wf-review` approval before implementation.

**`Approved` requires evidence.** The status field alone is not approval — the approval Decision
must be recorded in the work ledger. An artifact marked `Approved` with no ledger Decision is a
defect and must be reported, not honoured.

`wf-task-noncode` produces **specifications only**. "Non-code" describes the deliverable; it does
not lower the specification's rigour, and it never authorises code.

## 3a. Worktrees

**`wf-plan` creates the task worktree**, always from the repository's `main`/`master` base branch,
and creates or refreshes the task handoff file at the same time. `wf-task-code` and
`wf-task-noncode` record the worktree *preferences* in their calibration record (choice 4) and
hand them over — they never create a branch or a worktree themselves.

## 4. Data integrity (binding)

The `binding.yaml` file in a project's codebase directory must reference the stable ID and version
of the specification collection residing here. This ensures the codebase is traceable to its
required definition.

`binding.yaml` carries **only** that pointer. Runtime service dependencies belong in
`service-contracts.yaml`. One filename, one contract.

## 5. Naming

| Artifact | Pattern |
|---|---|
| Project collection | `projects/<lowercase-hyphenated-name>/` |
| Task specification | `tasks/task-<task-id>-noncode.md` or `tasks/task-<task-id>-coding.md` |
| Calibration record | `tasks/task-<task-id>-noncode-calibration.md` |
| Task plan | `tasks/task-<task-id>-plan.md` — one per task; the source of truth for `wf-implement` |
| Task handoff | `tasks/task-<task-id>-handoff.md` — one per task, not one per skill |
| Capability | `library/Capabilities/<capability-id>.md` |

### Handoff files — inside the tree, and disposable

A handoff file **always lives inside the directory of the work it describes**: a project task's
handoff is at `projects/<project-name>/tasks/`, framework-level work at `spec-workspace/tasks/`.
There is no central handoff folder.

**Handoff files are disposable.** When a handoff's status becomes `Done`, it is **deleted, not
archived**, and it leaves no trace in the tree. The durable history lives in the work ledger and in
the specifications — never in a handoff. A handoff that is `Open`, `In Progress`, or `Blocked` is
never deleted; a blocked handoff is the first thing the next session reads.

Every skill looks for the task's handoff file before acting and reads it if it exists. Its required
content — purpose, status, action items, preconditions unmet, open questions, suggested skill run,
phase contributions — is defined in the root `AGENTS.md` Section 5.

## 6. Known gaps

Recorded in the work ledger, not worked around silently:

* `library/Capabilities/` holds no capability specifications. `WORK-LMS-CONTRACT-001` depends on
  four capabilities (`UserID`, `TimestampFormat`, `StatusEnums`, `SchemaVersionConstraint`) that
  have no defining artifact — `WORK-020`.
* No specification in this tree is `Approved` — `WORK-009`, `WORK-016`.
