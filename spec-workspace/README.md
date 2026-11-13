# Specification Workspace

The decoupled, technology-agnostic knowledge layer. This directory holds **what** is intended;
`generated-projects/` holds **how** it is built. The two are linked by `binding.yaml` files and by
the work ledger - never by duplication.

## Structure

| Path | Purpose |
|---|---|
| `library/` | Reusable, technology-agnostic artifacts. May not reference implementation details. |
| `library/Engineering/` | Cross-cutting engineering practices and constraints. |
| `library/Capabilities/` | Reusable capability specifications (e.g. `UserID`, `TimestampFormat`). |
| `projects/<project-name>/` | The complete specification collection for one project. |
| `projects/<project-name>/SRS_LMS_v1.0.md` | The parent specification (root of the collection). |
| `projects/<project-name>/schema/` | Normative renderings of data contracts. |
| `projects/<project-name>/tasks/` | Task specifications and their handoff files. |
| `projects/<project-name>/binding.yaml` | Pointer from this specification collection to the codebase. |
| `projects/<project-name>/service-contracts.yaml` | Runtime service-to-service dependency manifest. |
| `tasks/` | Framework-level handoffs (not project-scoped). |
| `project-temp/work_ledger.yaml` | The persistent work ledger - the local source of truth for all work. |
| `SDLC-SOR-v1.0.md` | The framework's own system-of-record definition. |

## Naming conventions

* Project directories: lowercase, hyphenated - `blockchain-enabled-lms`.
* Task specification: `tasks/task-<task-id>-noncode.md` or `tasks/task-<task-id>-coding.md`.
* Task handoff: `tasks/task-<task-id>-handoff.md` - **one** per task, not one per skill.
  Contributing skills append their phase contribution to it while its status is not `Done`.
* Calibration record: `tasks/task-<task-id>-noncode-calibration.md` (required by the
  `wf-task-noncode` File Emission Guardrail).

## Specification lifecycle

`Draft -> In_Review -> Approved -> Superseded`

`wf-bootstrap` creates project specifications. `wf-review` is the independent gate before any
`Approved` status is granted, and the approval evidence must be recorded in the work ledger.
`wf-task-code` and `wf-task-noncode` create task specifications, each subject to `wf-review`.

**Current status:** no specification is `Approved`. The LMS parent spec (`SRS-LMS-v1.0`) and the
`WORK-LMS-CONTRACT-001` task spec are both `Draft` - see ledger `WORK-009` and `WORK-016`.

## Data integrity (binding)

Each project's codebase directory must contain a `binding.yaml` referencing the stable ID and
version of the specification collection here. `binding.yaml` carries **only** that pointer;
runtime service bindings belong in `service-contracts.yaml`.

The LMS project's `binding.yaml` currently lives at
`spec-workspace/projects/blockchain-enabled-lms/binding.yaml` because the codebase directory is
not yet determined. It must be mirrored into the codebase directory once one exists.
