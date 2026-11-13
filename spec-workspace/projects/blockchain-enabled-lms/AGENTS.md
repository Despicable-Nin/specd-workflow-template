# Blockchain-Enabled LMS — Project AGENTS.md

*(Project-local context and rules for the Blockchain-Enabled LMS specification collection. It is
subordinate to the root `AGENTS.md` and to `spec-workspace/AGENTS.md`, and inherits their Rule 0.)*

## 1. What this collection is

The complete specification collection for a blockchain-enabled Learning Management System: a system
of record for student academic achievements across Primary, Secondary, and College education,
with immutable blockchain proofs of grade finalization.

The parent specification is `SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, v1.0).

## 2. Contents

| Path | Role |
|---|---|
| `SRS_LMS_v1.0.md` | Parent specification — service domain architecture, workflows, governance. `status: Draft`. |
| `schema/final-academic-record.md` | Normative rendering of the `final_academic_record` contract. `status: Draft`. |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification `WORK-LMS-CONTRACT-001`. `status: Draft`. |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | The one handoff for that task. |
| `binding.yaml` | Pointer from this collection to the codebase. |
| `service-contracts.yaml` | Runtime service-to-service dependency manifest. |

## 3. Authority

**The task specification is authoritative for the `final_academic_record` contract.**
`schema/final-academic-record.md` is its normative rendering. Where the two disagree, the task
specification wins and the rendering is the defect. The rendering must not introduce requirements
the task specification does not authorize.

## 4. Status — read this before starting anything

**Nothing in this collection is `Approved`.**

| Blocker | Detail |
|---|---|
| `WORK-009` | The task spec carries no approval Decision in the work ledger. It was once marked `Approved` with no body; the body was restored and the status corrected to `Draft`. |
| `WORK-016` | The parent SRS has no approval Decision. It reads "*Design complete*" in prose, which is not the same as an approved status. |
| `WORK-020` | The task depends on four capabilities (`UserID`, `TimestampFormat`, `StatusEnums`, `SchemaVersionConstraint`) that have **no defining artifact** anywhere in the repository. |

The correct next action is `@wf-review` against
`tasks/task-LMS-CONTRACT-001-noncode.md` — not `@wf-task-code`, and not implementation.

## 5. Domain rules that bind any work here

* **ECS is the rule authority.** The Educational Context Service determines which rules apply for
  a given `EducationalLevel` and `AcademicPeriod`, and its rules must be consulted on every
  critical state change (SRS Sections 1.4, 4.2). A task must not author ECS rule content — it
  defines the schema field and its cardinality, and cites the SRS section that owns the rules.
* **The operational database is the system of record**; the Ledger Service hashes it and commits an
  immutable proof to the blockchain (SRS Section 4.3). This is *not* the framework's "System of
  Record" — see `spec-workspace/SDLC-SOR-v1.0.md`.
* **Audit linkage is non-negotiable.** Every appeal or amendment appends a new versioned record
  carrying a mandatory `parent_transaction_id`; originals are never mutated.

## 6. Code for this project

The codebase does not exist yet, and its location is undecided (`WORK-017`). Until that is settled:

* **No implementation code is written into this collection.** This tree holds specifications only.
* Code for this project is raised as a **separate coding task** via `wf-task-code`, targeting
  `generated-projects/blockchain-enabled-lms/`, and implemented by `wf-implement` only.
* This project's `binding.yaml` currently lives here rather than in a codebase directory. It must
  be mirrored into the codebase directory once one exists.
