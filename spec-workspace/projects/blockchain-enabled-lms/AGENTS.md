# Blockchain-Enabled LMS — Project AGENTS.md

*(Project-local context and rules for the Blockchain-Enabled LMS specification collection. It is
subordinate to the root `AGENTS.md` and to `spec-workspace/AGENTS.md`, and inherits their Rule 0.)*

## 1. What this collection is

The complete specification collection for a blockchain-enabled Learning Management System: a system
of record for student academic achievements across Primary, Secondary, and College education,
with immutable blockchain proofs of grade finalization.

The parent specification is `SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, v1.2).

## 2. Contents

| Path | Role |
|---|---|
| `SRS_LMS_v1.0.md` | Parent specification — objectives, stakeholders, capabilities and workflows, domain boundaries, quality expectations, composition and topology decisions. `spec_id: SRS-LMS-v1.0`, version 1.2, `status: Approved` (`WORK-039`; v1.2 refreshed Sections 8.1 and 9 per Section 11 Change Request `WORK-171`, Gate 2 Decision `WORK-176`, commit `b6ce80c`). |
| `schema/final-academic-record.md` | Normative rendering of the `final_academic_record` contract. `status: Approved` (v1.0.0; rendering of task spec v1.5). |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification `WORK-LMS-CONTRACT-001`. `status: Approved` (v1.5, `WORK-156`; seventh review; `parent_transaction_id` format opaque, no UUIDv4 mandate). |
| `tasks/task-LMS-CONTRACT-001-plan.md` | The implementation plan for that task. Exists but **stale** — written against task spec v1.2; regenerate from v1.5 via `wf-plan` before any `wf-implement` (known defect; frontmatter overstates readiness). |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | The one handoff for that task. **MISSING as of 2026-11-18** (verified); `binding.yaml` records it as `missing` (previously listed as `In Progress`) — disposition `WORK-170`. Recreated through the `wf-plan`/`wf-implement` flow; disposable: deleted once its status is `Done`. |
| `binding.yaml` | Pointer from this collection to the codebase. |
| `spec-workspace/library/Capabilities/CAP-*.md` | All five capability artifacts (`CAP-CANONICAL-FORM` v1.0, `CAP-USERID` v1.1, `CAP-TIMESTAMPFORMAT` v1.1, `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 — Decision `WORK-175`; `CAP-STATUSENUMS` v1.1 — Decision `WORK-176`). `status: Approved` (2026-11-18). |
| `service-contracts.yaml` | Runtime service-to-service dependency manifest. |

## 3. Authority

**The task specification is authoritative for the `final_academic_record` contract.**
`schema/final-academic-record.md` is its normative rendering. Where the two disagree, the task
specification wins and the rendering is the defect. The rendering must not introduce requirements
the task specification does not authorize.

## 4. Status — read this before starting anything

**Every approval-gated artifact in this collection is `Approved` as of 2026-11-18.** (The plan
below is stale and the handoff below is missing — neither is an approval artifact; the
calibration record is `Confirmed`, not `Approved`.) The parent gates children, and the
children are now cleared:

| Artifact | Status | Evidence |
|---|---|---|
| Parent SRS `SRS-LMS-v1.0` | v1.2, `Approved` | Gate 2 Decision `WORK-176`; Change Request `WORK-171`; applied at `b6ce80c` |
| Schema rendering `SCHEMA-LMS-FAR-v1.0` | v1.0.0, `Approved` | rendering of task spec v1.5 |
| Task spec `WORK-LMS-CONTRACT-001` | v1.5, `Approved` | Decision `WORK-156` |
| Five capability artifacts | all `Approved` (2026-11-18) | Decision `WORK-175` (applied at `7a80293`); `CAP-STATUSENUMS` under `WORK-176` |
| Project constitution | `CONST-LMS-v1.3`, `Approved` | Gate 2 Decision `WORK-178`; commit `b33e6a6` |
| Collection binding | `codebase_dir` determined | Decision `WORK-160` (`generated-projects/blockchain-enabled-lms/`) |

**Still open — not blockers to new specs, but to the first implementation slice:**

| Item | Detail |
|---|---|
| Stale plan | `tasks/task-LMS-CONTRACT-001-plan.md` was written against task spec v1.2 and must be regenerated from v1.5 via `wf-plan` before any `wf-implement` (known defect; its frontmatter overstates readiness). |
| Missing handoff | `tasks/task-LMS-CONTRACT-001-handoff.md` does not exist; `binding.yaml` records it as `missing` (previously listed as `In Progress`; disposition `WORK-170`). Recreated through the `wf-plan`/`wf-implement` flow. |
| SRS Q-1 | Authoritative source of the rule-set identifier value (bears on P-3, P-4). Open. |
| SRS Q-2 | Agreed data format for `parent_transaction_id` (the contract v1.5 dodged it with an opaque type). Open. |
| Retention policy | Constitution tension 1: P-5/P-6 monotonic retention vs any future hard-deletion/minimisation requirement — an explicit retention-policy Decision is owed before any lifecycle/deletion feature. |
| SRS Q-3 (residual) | The exploratory `lms-platform/` and `src/identity/` directories were removed 2026-11-17 (Decision `WORK-160`); the question is answered in substance. Annotate via Section 11 if formal closure is wanted. |

**The correct next action is `@wf-plan` against `WORK-LMS-CONTRACT-001` (v1.5), not `@wf-review` of
the parent** — the parent is `Approved`. Then implementation slices are raised via
`@wf-task-code` targeting `generated-projects/blockchain-enabled-lms/`; code is written only by
`wf-implement`.

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

The codebase is **decided and scaffolded**: `generated-projects/blockchain-enabled-lms/`
(`WORK-017` / `WORK-035`, Decision `WORK-160`, 2026-11-17). Its `binding.yaml` carries the
`SPEC-LMS-v1.0` v1.0 pointer; the collection `binding.yaml` mirrors this (`codebase_dir`
determined). It holds a scaffold only — no source directories yet.

* **No implementation code is written into this collection.** This tree holds specifications only.
* Code for this project is raised as a **separate coding task** via `wf-task-code`, targeting
  `generated-projects/blockchain-enabled-lms/`, and implemented by `wf-implement` only.
* The first coding task's plan decides the source layout and toolchain.
