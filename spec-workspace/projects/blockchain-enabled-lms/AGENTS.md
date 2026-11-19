# Blockchain-Enabled LMS — Project AGENTS.md

*(Project-local context and rules for the Blockchain-Enabled LMS specification collection. It is
subordinate to the root `AGENTS.md` and to `spec-workspace/AGENTS.md`, and inherits their Rule 0.)*

## 1. What this collection is

The complete specification collection for a blockchain-enabled Learning Management System: a system
of record for student academic achievements across Primary, Secondary, and College education,
with immutable blockchain proofs of grade finalization.

The parent specification is `SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, v1.3).

## 2. Contents

| Path | Role |
|---|---|
| `SRS_LMS_v1.0.md` | Parent specification — objectives, stakeholders, capabilities and workflows, domain boundaries, quality expectations, composition and topology decisions. `spec_id: SRS-LMS-v1.0`, version 1.3, `status: Approved` (`WORK-039`; v1.2 refreshed Sections 8.1 and 9 per Section 11 Change Request `WORK-171`, Gate 2 Decision `WORK-176`, commit `b6ce80c`; v1.3 added attendance Workflow W-7 / capability C-8 and the W-2 formula-ownership annotation per Change Request `WORK-191`, Gate 2 Decision `WORK-192`, 2026-11-19). |
| `schema/final-academic-record.md` | Normative rendering of the `final_academic_record` contract. `status: Approved` (v1.0.0; rendering of task spec v1.5). |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification `WORK-LMS-CONTRACT-001`. `status: Approved` (v1.5, `WORK-156`; seventh review; `parent_transaction_id` format opaque, no UUIDv4 mandate). |
| `tasks/task-LMS-CONTRACT-001-plan.md` | The implementation plan for that task. Regenerated from task spec v1.5 (wf-plan, 2026-11-19); validated at Gate 2 (both passes) and approved at **Gate 3** (Decision `WORK-189`); `ready-for-implement`; the source of truth for `wf-implement`. |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | The one handoff for that task. **Deleted 2026-11-19** (task converged `CONVERGED`; `Done`; disposed by `wf-commit` — disposable by contract). Not present in the tree. |
| `binding.yaml` | Pointer from this collection to the codebase. |
| `spec-workspace/library/Capabilities/CAP-*.md` | All five capability artifacts (`CAP-CANONICAL-FORM` v1.0, `CAP-USERID` v1.1, `CAP-TIMESTAMPFORMAT` v1.1, `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 — Decision `WORK-175`; `CAP-STATUSENUMS` v1.2 - v1.1 at `WORK-176`; v1.2 (attendance outcome domain, `Recorded`) atomic with SRS v1.3, Decision `WORK-192`). `status: Approved` (2026-11-18; v1.2 2026-11-19). |
| `service-contracts.yaml` | Runtime service-to-service dependency manifest. |

## 3. Authority

**The task specification is authoritative for the `final_academic_record` contract.**
`schema/final-academic-record.md` is its normative rendering. Where the two disagree, the task
specification wins and the rendering is the defect. The rendering must not introduce requirements
the task specification does not authorize.

## 4. Status — read this before starting anything

**Every approval-gated artifact in this collection is `Approved` as of 2026-11-19 (SRS v1.3 applied 2026-11-19, Decision `WORK-192`).** The plan was
regenerated from task spec v1.5 and approved at Gate 3 (Decision `WORK-189`, 2026-11-19); the task
reached convergence `CONVERGED` on 2026-11-19 (`WORK-190`) and the disposable handoff was deleted by
`wf-commit` in the same change. The parent gates children, and the children are now cleared:

| Artifact | Status | Evidence |
|---|---|---|
| Parent SRS `SRS-LMS-v1.0` | v1.3, `Approved` | Gate 2 Decision `WORK-192`; Change Request `WORK-191`; applied 2026-11-19 (atomic with `CAP-STATUSENUMS` v1.2); v1.2 anchored to `WORK-176` / `b6ce80c` |
| Schema rendering `SCHEMA-LMS-FAR-v1.0` | v1.0.0, `Approved` | rendering of task spec v1.5 |
| Task spec `WORK-LMS-CONTRACT-001` | v1.5, `Approved` | Decision `WORK-156` |
| Five capability artifacts | all `Approved` (2026-11-18) | Decision `WORK-175` (applied at `7a80293`); `CAP-STATUSENUMS` under `WORK-176` (v1.1) and `WORK-192` (v1.2, atomic with SRS v1.3) |
| Project constitution | `CONST-LMS-v1.3`, `Approved` | Gate 2 Decision `WORK-178`; commit `b33e6a6` |
| Collection binding | `codebase_dir` determined | Decision `WORK-160` (`generated-projects/blockchain-enabled-lms/`) |

**Still open — not blockers to new specs, but to the first implementation slice:**

| Item | Detail |
|---|---|
| Plan | `tasks/task-LMS-CONTRACT-001-plan.md` — regenerated 2026-11-19 (wf-plan), Gate 2 pass 2 `APPROVED WITH COMMENTS`, Gate 3 approved (Decision `WORK-189`); `ready-for-implement`. | ✅ done |
| Handoff | Recreated 2026-11-19 by `wf-plan`; driven to `Done`; **deleted by `wf-commit` 2026-11-19**. | ✅ done |
| SRS Q-1 | **Resolved in substance 2026-11-19 (Decision `WORK-179`): ECS mints and owns `GoverningRuleSetID`; GRA-Service records it (SRS §2.7).** Formal SRS annotation pending `WORK-182` (proposed). |
| SRS Q-2 | Agreed data format for `parent_transaction_id` (the contract v1.5 dodged it with an opaque type). Open. |
| Retention policy | Constitution tension 1: P-5/P-6 monotonic retention vs any future hard-deletion/minimisation requirement — an explicit retention-policy Decision is owed before any lifecycle/deletion feature. |
| SRS Q-3 (residual) | The exploratory `lms-platform/` and `src/identity/` directories were removed 2026-11-17 (Decision `WORK-160`); the question is answered in substance. Annotate via Section 11 if formal closure is wanted. |

**This task is complete:** `WORK-LMS-CONTRACT-001` converged `CONVERGED` on 2026-11-19 (`WORK-190`);
the disposable handoff was deleted by `wf-commit` in the same change. Implementation slices for the
system itself are raised via `@wf-task-code` targeting `generated-projects/blockchain-enabled-lms/`
and are written only by `wf-implement`. The contract's open follow-ons: `WORK-181` (constitution
v1.4 - strike tensions 1 and 6) and `WORK-182` (SRS Section 11 CR - Q-1/Q-3 annotations, Section 8.1
handoff row).

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
