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
| `SRS_LMS_v1.0.md` | Parent specification — objectives, stakeholders, capabilities and workflows, domain boundaries, quality expectations, composition and topology decisions. `spec_id: SRS-LMS-v1.0`, version 1.0, `status: Draft`. |
| `schema/final-academic-record.md` | Normative rendering of the `final_academic_record` contract. `status: Draft`. |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification `WORK-LMS-CONTRACT-001`. `status: Draft`. |
| `tasks/task-LMS-CONTRACT-001-plan.md` | The implementation plan for that task. **Does not exist yet** — created by `wf-plan`. |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | The one handoff for that task. Disposable: deleted once its status is `Done`. |
| `binding.yaml` | Pointer from this collection to the codebase. |
| `spec-workspace/library/Capabilities/CAP-CANONICAL-FORM.md` | The capability the specification's proof guarantee depends on. |
| `service-contracts.yaml` | Runtime service-to-service dependency manifest. |

## 3. Authority

**The task specification is authoritative for the `final_academic_record` contract.**
`schema/final-academic-record.md` is its normative rendering. Where the two disagree, the task
specification wins and the rendering is the defect. The rendering must not introduce requirements
the task specification does not authorize.

## 4. Status — read this before starting anything

**Nothing in this collection is `Approved`.** The parent specification is `Draft`, and that gates
everything beneath it: a task specification may not be `Approved` ahead of its parent.

| Blocker | Detail |
|---|---|
| `WORK-016`, `WORK-032`, `WORK-039` | The parent SRS has no approval Decision. It was rewritten on 2026-11-13 to conform to the `wf-bootstrap` specification contract — all 14 blocking review findings against it were addressed (`WORK-040`…`WORK-053`). It is awaiting independent re-review, then explicit approval. |
| `WORK-009` | The task spec carries no approval Decision in the work ledger. It was once marked `Approved` with no body; the body was restored and the status corrected to `Draft`. |
| `WORK-020` | The task depends on four capabilities (`UserID`, `TimestampFormat`, `StatusEnums`, `SchemaVersionConstraint`) that have **no defining artifact**. The SRS now defines the status vocabulary normatively for this project (Section 9) as an interim measure; the shared capability artifacts are still owed. |
| `WORK-130` | The canonical-form rules that `CAP-CANONICAL-FORM` defines have no owning domain. SRS Question Q-5. |
| `WORK-062`, `WORK-064`…`WORK-069` | Seven blocking findings remain on the task specification. They cannot be closed until the parent is `Approved`. |

**The correct next action is `@wf-review` against `SRS_LMS_v1.0.md` — the parent, not the task.**
The order is: review and approve the parent → then close the task spec's blocking findings →
then review and approve the task. Not `@wf-task-code`, and not implementation.

## 5. Domain rules that bind any work here

* **ECS is the rule authority.** The Educational Context Service determines which rules apply for
  a given `EducationalLevel` and `AcademicPeriod`, and its rules must be consulted on every
  critical state change (SRS Sections 3.2 and 3.3). A task must not author ECS rule content — it
  defines the schema field and its cardinality, and cites the SRS section that owns the rules.
* **The operational record store is the system of record**; the Ledger Service commits an
  immutable proof over it (SRS Sections 2.7 and 3.6). This is *not* the framework's "System of
  Record" — see `spec-workspace/SDLC-SOR-v1.0.md`.
* **Audit linkage is non-negotiable.** Every appeal or amendment appends a new versioned record
  carrying a mandatory `parent_transaction_id`; originals are never mutated (SRS Section 2.4 and
  the state transitions in Section 2.9).

## 6. Code for this project

The codebase does not exist yet, and its location is undecided (`WORK-017`). Until that is settled:

* **No implementation code is written into this collection.** This tree holds specifications only.
* Code for this project is raised as a **separate coding task** via `wf-task-code`, targeting
  `generated-projects/blockchain-enabled-lms/`, and implemented by `wf-implement` only.
* This project's `binding.yaml` currently lives here rather than in a codebase directory. It must
  be mirrored into the codebase directory once one exists.
