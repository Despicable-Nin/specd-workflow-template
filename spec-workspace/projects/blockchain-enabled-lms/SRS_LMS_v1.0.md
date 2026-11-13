---
spec_id: SRS-LMS-v1.0
collection_id: SPEC-LMS-v1.0
version: 1.0
status: Draft
title: Software Requirements Specification - Blockchain-Enabled LMS
project: blockchain-enabled-lms
created: 2026-11-11T12:00:00Z
updated: 2026-11-13T02:45:00Z
---

# Software Requirements Specification - Blockchain-Enabled LMS

> **Terminology note.** "System of Record" has two distinct uses in this repository. In this
> document it always means the **operational record store** that holds the authoritative academic
> state (Section 3.6). The framework's own use of the phrase — for the specification artifact layer
> under `spec-workspace/` — is a different concept entirely and is not referenced here.

---

## 1. Purpose, objectives and stakeholders

### 1.1 Purpose

This specification defines the architecture and requirements for a **Learning Management System
whose academic records are immutable, independently verifiable, and traceable to their source of
assessment**. It fixes the service-domain boundaries, the workflows those domains support, the
quality the system must meet, and the boundaries within which the system does *not* operate.

Field-level data contracts for academic records are **not** defined here. They are defined by the
task specifications derived from this document — currently `WORK-LMS-CONTRACT-001` and its
normative rendering `schema/final-academic-record.md` (Section 8).

### 1.2 Core business objectives

| Objective | Statement |
|---|---|
| **Integrity** | Every final academic record is immutable once finalized, and any later correction is *appended* rather than substituted. |
| **Verifiability** | A third party can confirm that a final academic record existed, was authorized, and has not been altered. |
| **Traceability** | Any record can be traced back to the assessment and the rule set that produced it. |
| **Longevity** | The record remains provable independent of the lifetime of any single service. |
| **Contextual correctness** | The rules applied to a student depend on the educational level and the academic period in force at the time. |

### 1.3 Educational levels in scope

| Level | Emphasis |
|---|---|
| Primary School | Pass/fail outcome, attendance, simple numerical progression. |
| Secondary School | Credit structures, electives, graduation requirements. |
| College | Credit accumulation, weighted grade-point average, prerequisite enforcement. |

### 1.4 Stakeholders

| Stakeholder | Interest |
|---|---|
| **Students** | A defensible, permanent record of their academic progress. |
| **Instructors and faculty** | The ability to record and defend an assessment, including after an appeal. |
| **Academic administrators** (Dean, Principal, Chair) | Control over promotion and promotion decisions, and the authority to approve corrections. |
| **Registrar / records office** | The authoritative, complete academic history at all times. |
| **Compliance and audit parties** | Independent evidence that records were produced under a known rule set. |
| **Learning platform operator** | Correct behaviour across levels and periods, and a defensible audit trail. |

---

## 2. Major capabilities and workflows

### 2.1 Capabilities

| # | Capability | Owning domain |
|---|---|---|
| C-1 | Identify and authorize actors, and hold the user profile. | IAM |
| C-2 | Determine the rules in force for a given educational level and academic period. | ECS |
| C-3 | Define what is taught: subjects, course definitions, degree structures, prerequisite maps. | AMS |
| C-4 | Allocate instructional resources to scheduled sections. | FRAS |
| C-5 | Instantiate learning: sections, enrollments, scheduling. | ESS |
| C-6 | Compute the final grade from assessments under the governing formula. | GRA-Service |
| C-7 | Commit an immutable, verifiable proof of grade finalization. | LGS |

### 2.2 Workflow W-1 — Academic period gatekeeping

**Trigger.** Any primary creation or update of an enrollment or a grade submission.
**Participants.** ESS, GRA-Service (and any other domain creating such records).
**Flow.**

1. The creating domain requests the governing context for the target educational level and academic
   period from ECS.
2. ECS resolves the academic period's current status.
3. If the status is not `Active`, ECS refuses the request and the creating domain must not proceed.
4. If the status is `Active`, ECS returns the governing rule set identifier, which the creating
   domain records against the record it is about to create.

**Rule.** No enrollment or grade submission may be created or modified in a period whose status is
not `Active`.

### 2.3 Workflow W-2 — Grade submission

**Trigger.** An instructor submits assessed results for an enrolled student in a section.
**Participants.** GRA-Service, ECS, LGS.
**Flow.**

1. The submission names the enrolled student, the section, the assessment, and the raw scores.
2. GRA-Service requests the governing grading formula from ECS for the student's educational level
   and the academic period in force.
3. GRA-Service applies the formula and produces a proposed final grade.
4. The proposed grade is recorded with the rule set identifier returned in step 2.
5. GRA-Service submits the finalized record to LGS for commitment as a proof (Section 2.7).

**Rule.** A finalized grade must carry the rule set identifier under which it was computed.

### 2.4 Workflow W-3 — Appeal and correction

**Trigger.** A correction is required to a grade that has already been finalized.
**Participants.** GRA-Service, IAM, the approval chain, LGS.
**Flow.**

1. A `GradeAppealRecord` is raised against the finalized grade, referencing it by its transaction
   identity.
2. GRA-Service computes the proposed grade delta under the rule set identified in the original
   record.
3. The appeal passes through a mandatory, documented approval chain: instructor, then chair, then
   dean. Each step is recorded.
4. Until the final signatory approves, the appeal carries the status `UnderReview`. **The
   original finalized record is not modified, withdrawn, or marked in any way.**
5. On approval, a **new, versioned record** is appended that references the original via
   `parent_transaction_id`, carries the status flag of the change, and states the revised grade.
   The original remains part of the history exactly as finalized.

**Rule (append-only).** A correction never overwrites the record it corrects. The operational record
store holds both, linked by `parent_transaction_id`.

> **Decision recorded.** The append-only model is adopted. The alternative — amending the original
> record in place — is explicitly rejected, because it destroys the evidence that a finalized
> record existed in the form it was finalized.

### 2.5 Workflow W-4 — Promotion between levels

**Trigger.** A student's enrollment record for a level reaches `Completed`.
**Participants.** ESS, AMS, ECS, IAM, GRA-Service.
**Flow.**

1. GRA-Service validates that the student meets the credit and pass milestones defined by AMS and
   ECS for the level being completed.
2. An IAM-secured role at dean or principal authority manually approves the transition.
3. ESS updates the student's level to the next expected level and signals the transition.
4. The transition is recorded as a new versioned record linked to the prior one.

### 2.6 Workflow W-5 — College enrollment

**Trigger.** A student requests enrollment in a course or program at college level.
**Participants.** ESS, AMS, ECS.
**Flow.**

1. AMS validates the request against the prerequisite map for the student's program.
2. AMS confirms the student holds an active major program definition.
3. ECS supplies the credit capacity constraints in force for the academic period.
4. ESS enrolls the student only if every constraint is satisfied, and records the outcome against
   the governing rule set.

### 2.7 Proof of finalization — the proof unit

**One proof unit, stated precisely:**

* **What is proved.** The finalized academic state of **one student, for one academic period**,
  captured as the canonical `final_academic_record` payload defined by `WORK-LMS-CONTRACT-001`.
* **Granularity.** One proof per finalized student-period record. A change to that record — an
  appeal outcome — produces a **new** proof, not a replacement.
* **How the proof is formed.** The canonical payload is reduced to a fixed form and a digest is
  computed over it. The proof commits that digest together with the transaction identity, the
  timestamp, the authorizing authority, and a linkage to the preceding proof in the sequence.
* **How a verifier re-derives it.** A verifier obtains the canonical payload from the operational
  record store, reduces it to the same fixed form, computes the digest, and compares it with the
  committed digest. The sequence linkage lets the verifier establish that no proof was removed or
  reordered.

**Rule.** The proof commits evidence of a record's existence and content. It is **not** the record,
and it does not replace the operational record store.

### 2.8 State transitions

#### Academic period

| From | Event | To |
|---|---|---|
| — | Period defined | `Draft` |
| `Draft` | Period opened for enrollment and assessment | `Active` |
| `Active` | Period closed | `Closed` |

`Closed` is terminal. A record may not be created or modified in a period that is not `Active`
(Workflow W-1).

#### Enrollment

| From | Event | To |
|---|---|---|
| — | Enrollment requested | `Requested` |
| `Requested` | Prerequisites, capacity and program constraints satisfied | `Enrolled` |
| `Requested` | A constraint is not satisfied | `Withdrawn` |
| `Enrolled` | All requirements met for the period | `Completed` |
| `Enrolled` | Withdrawn by the student or an administrator | `Withdrawn` |

#### Grade and appeal

| From | Event | To |
|---|---|---|
| — | Assessment results submitted and a grade computed | `Proposed` |
| `Proposed` | Approved and committed as a proof | `Finalized` |
| `Finalized` | An appeal is raised against it | `Finalized` (unchanged) with an appended appeal in `Proposed` |
| `Finalized` | An appeal is approved | The original stays `Finalized`; an appended successor record is created, and the original is additionally marked `Superseded` |
| `Finalized` | An appeal is rejected | The original stays `Finalized`; the appeal moves to `Rejected` |

**Rule.** A finalized record only ever leaves `Finalized` by being marked `Superseded` **after** a
successor has been appended. The mark records which successor supersedes it; it never alters the
superseded record's content.

---

## 3. Logical architecture boundaries and responsibilities

### 3.1 The seven service domains

| Domain | Responsibility | Operations it exposes | Operational record it owns |
|---|---|---|---|
| **IAM** | Identify and authorize actors; hold the user profile. | Authenticate an actor and return an access assertion; return the profile of an authenticated actor; resolve the authorities held by an actor. | `User`, `UserGroup`, `Scope`, `Authority` |
| **ECS** | **The rule authority.** Determine the rules in force for an educational level and academic period. | Given an educational level and academic period, return the governing rule set identifier and the rules it contains; given a period, return its current status. | `EducationalLevel`, `AcademicPeriod`, `CycleType`, `FormulaRules` |
| **AMS** | Define what is taught: subjects, course definitions, degree structures, prerequisite maps. | Define a course, validated against the prerequisite map; define a program of study; return the prerequisites of a course. | `CourseCatalog`, `ProgramMap` |
| **FRAS** | Allocate instructional resources to scheduled sections, and enforce capacity and load constraints on that allocation. | Assign an instructor to a section, validated against instructor load and section capacity; return an instructor's load record. | `Faculty`, `Assignment`, `LoadRecord` |
| **ESS** | Instantiate learning: sections, enrollments, scheduling. | Enroll a student in a section, validated against prerequisites (AMS) and capacity (FRAS); return a student's enrollment instance. | `Section`, `Enrollment` |
| **GRA-Service** | Compute the final grade under the governing formula; own the appeal and review history. | Submit an assessment result and receive the computed final grade; raise an appeal against a finalized grade; record an approval step. | `GradeRecord`, `GradeAppealRecord`, `ReviewLog` |
| **LGS** | Commit the immutable proof of grade finalization; maintain the proof sequence. | Commit a proof over a finalized `final_academic_record` payload; return the proof sequence for verification. | `BlockHash`, `TransactionID` |

### 3.2 The closed set of ECS consumers

The following domains **must** consult ECS before any critical state change, and no others are
required to:

`AMS`, `ESS`, `GRA-Service`, `FRAS`, `LGS`

ECS itself is the authority and is not a consumer of itself. IAM is not a consumer — it authorizes
actors, and does not vary by educational level or academic period.

### 3.3 Capacity and load ownership

**Ownership is split by decision, not by duplication:**

* **ECS** *defines* the capacity constraint — how many students a section may hold, derived from
  the rule set in force.
* **FRAS** *enforces* it — FRAS is the single owner of capacity-and-load validation at the point
  of instructional allocation, checking both instructor load and section capacity.
* **ESS** *consumes* the outcome — ESS enrolls against the allocation FRAS has already validated,
  and does not re-derive or re-own the constraint.

### 3.4 Academic period ownership

`AcademicPeriod` is owned **solely by ECS**. ECS owns its identity, its status, its cycle type,
and the rule set applicable within it.

ESS does not own `AcademicPeriod`. ESS owns the **enrollment instances bound to** a period — the
sections scheduled inside it and the students enrolled in them — and references the period by its
ECS-owned identity.

### 3.5 The audit trail has a stated home

The operational record store holds the complete, authoritative academic history: finalized grades,
appeal records, approval-chain review logs, and appeal status flags. GRA-Service does **not** hold
this state transiently — its own working state is transient, but every artifact it produces is
committed to the operational record store as it is produced.

### 3.6 The operational record store is the record of truth

The operational record store is the authoritative, complete, approved state of a student's academic
history. It is always able to answer, for any student and period, the full set of grades, appeals,
and status flags that have been recorded — including the records that a later appeal superseded,
which remain present and linked.

LGS commits proof over that state. LGS does not hold it, and does not replace it.

---

## 4. Non-goals and success criteria

### 4.1 Non-goals

The following are explicitly **out of scope** for this specification:

* **Implementation.** No language, framework, storage engine, deployment platform, or hosting
  arrangement is specified or implied. Those are chosen when the implementation plan is created.
* **Delivery model.** How the seven domains are deployed, scaled, or networked is not specified.
* **Field-level academic record contracts.** Defined by `WORK-LMS-CONTRACT-001`, not here.
* **Financial, payroll, and human-resources functions.** Only the instructional allocation that
  academic scheduling requires is in scope.
* **Learning content authoring.** Course content is referenced by identity, not modelled.
* **Third-party integration protocols.** Consumers outside the seven domains are not specified.
* **Historical migration of existing records.** The system governs records it creates.
* **Correction of records finalized before this system existed.**

### 4.2 Success criteria

| # | Criterion | How it is judged |
|---|---|---|
| S-1 | A finalized record cannot be altered without leaving a linked, appended successor. | Audit of the operational record store shows original and successor both present, linked by `parent_transaction_id`. |
| S-2 | Any finalized record can be verified by a party with no access to the originating services. | The proof digest recomputes from the record the store holds. |
| S-3 | Every finalized grade states the rule set it was computed under. | Every finalized grade carries a rule set identifier that resolves to a known rule set. |
| S-4 | No record is created in an academic period that is not active. | No enrollment or grade submission exists whose period was not `Active` at creation. |
| S-5 | A promotion is never automatic. | Every promotion records an explicit approval by a dean or principal authority. |
| S-6 | Rules in force are consistent across every domain that depends on them. | ECS is the sole source of the rule set for a level and period, and every dependent domain records the identifier it used. |

---

## 5. Quality expectations

| Attribute | Expectation |
|---|---|
| **Immutability** | A finalized record is never altered in place. Corrections append a linked successor. The operational record store and the proof sequence must both reflect the append. |
| **Verifiability** | The proof of a finalized record must be independently recomputable from the record the store holds, by a party with no privileged access. |
| **Auditability** | Every state change to an academic record — creation, appeal, approval step, promotion — must be attributable to an actor and an authorization, and retained. |
| **Determinism** | Given the same rule set and the same assessed inputs, the computed grade must be identical. The rule set identifier must therefore be sufficient to reproduce a computation. |
| **Completeness** | The operational record store must be able to reconstruct a student's complete academic history at any point in time, including superseded records. |
| **Traceability of authority** | Every record that depends on a rule set must name it; every record that depends on an approval must name the approving authority. |
| **Refusal over ambiguity** | When a rule set cannot be resolved, a governing context cannot be established, or an approval is absent, the operation must be refused rather than completed under an assumption. |
| **Latency** | The system must not make correctness contingent on timing. No workflow may race an academic period's status or an approval. |

---

## 6. Architecture composition decision

**Decision.** The system is composed of **seven independently-owned service domains with a single
rule authority (ECS) and a single proof authority (LGS)**, connected by explicit operation contracts
rather than by shared state.

**Rationale.**

* A single rule authority is the only arrangement that makes the determinism and traceability
  expectations in Section 5 achievable. If two domains could each decide the applicable rules, the
  same computation could legitimately produce different answers.
* Separating the proof authority from the record authority keeps the record store complete and
  queryable (Section 3.6), instead of making the proof sequence the primary store.
* Explicit operation contracts, rather than shared state, keep the boundaries in Section 3
  enforceable: a domain that needs another's data must call that domain's operation.

**Consequence.** Domain boundaries are contracts, not deployment boundaries. The seven domains may
be deployed together or separately; that choice is not made here.

---

## 7. Repository topology decision

**Decision.** The specification collection is rooted at
`spec-workspace/projects/blockchain-enabled-lms/`, and the codebase — when created — is rooted at
`generated-projects/blockchain-enabled-lms/`, bound to the collection by `binding.yaml`.

**Layout.**

```
spec-workspace/projects/blockchain-enabled-lms/
├── SRS_LMS_v1.0.md                     # this document - the parent specification
├── binding.yaml                        # pointer to the codebase, and the spec id + version
├── service-contracts.yaml              # runtime service dependency manifest
├── schema/                             # normative renderings of data contracts
│   └── final-academic-record.md
└── tasks/                              # task specifications, plans, and handoffs
    ├── task-LMS-CONTRACT-001-noncode.md
    ├── task-LMS-CONTRACT-001-plan.md
    └── task-LMS-CONTRACT-001-handoff.md

generated-projects/blockchain-enabled-lms/
├── AGENTS.md
├── binding.yaml
└── <source directories implied by the implementation plan>
```

**Rationale.** Specifications are stored separately from code and are never copied into it. The
`binding.yaml` pair is the traceability link: the collection points at the codebase, and the
codebase points back at the collection's identifier and version.

**Consequence.** A codebase directory exists only after its `binding.yaml` is written. The
collection's `binding.yaml` states the identifier and version of the specification it is bound to
(`SRS-LMS-v1.0`, version 1.0). The location of the codebase directory for this project is **not yet
decided** — see Section 9.

---

## 8. Related artifacts

| Artifact | Relationship to this specification |
|---|---|
| `schema/final-academic-record.md` | Normative rendering of the `final_academic_record` payload. Defines the payload shape referenced by Section 2.7. Authoritative source: `tasks/task-LMS-CONTRACT-001-noncode.md`. |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification that defines the field-level data contract for the finalized academic record. |
| `tasks/task-LMS-CONTRACT-001-plan.md` | The implementation plan derived from that task specification. |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | The running handoff for that task. |
| `binding.yaml` | Binds this collection's identifier and version to the codebase. |
| `service-contracts.yaml` | Runtime dependency manifest between the domains of Section 3.1. It is a **runtime artifact**, not a source of authority — where it disagrees with Section 3, this document governs. |
| `AGENTS.md` (project) | Project-local rules that bind any work in this collection. |

**Domain coverage.** This document defines seven domains (Section 3.1).
`service-contracts.yaml` currently declares three runtime bindings and records five domains as
unmapped. That manifest is **incomplete against this specification**, not contradictory to it: the
domain model here is the authority, and the manifest is to be brought into agreement. The unmapped
domains are `ECS`, `AMS`, `FRAS`, `ESS`, and `GRA-Service`.

---

## 9. Open questions

| # | Question | Owner | Blocks |
|---|---|---|---|
| Q-1 | Which domain is the authoritative source for the value of the rule set identifier that the finalized record carries? | ECS / GRA-Service domain owners | `WORK-LMS-CONTRACT-001` (the `GoverningRuleSetID` field) |
| Q-2 | What is the agreed data format for `parent_transaction_id` across the domains that produce and consume it? | Domain owners | `WORK-LMS-CONTRACT-001` (the `parent_transaction_id` field) |
| Q-3 | Where is the codebase directory for this project created? | Architecture owner | `WORK-017`, `WORK-030` |
| Q-4 | Which capability artifacts define the shared `UserID`, `TimestampFormat`, `StatusEnums`, and `SchemaVersionConstraint` vocabularies that this specification uses? | Architecture owner | `WORK-020` |

**Status vocabulary used by this specification.** The academic period status values are `Draft`,
`Active`, `Closed`. The grade and appeal status values are `Proposed`, `UnderReview`, `Finalized`,
`Superseded`. The enrollment status values are `Requested`, `Enrolled`, `Completed`, `Withdrawn`.
These are defined **here** as normative for this project; a shared capability artifact for them
does not yet exist (Q-4).

---

## 10. Glossary

| Term | Meaning in this document |
|---|---|
| **Record** | A single fact about a student's academic history — a grade, an appeal, an approval step, an enrollment. Distinct from *proof*, which is evidence about a record. |
| **Proof** | A committed, independently recomputable digest over a canonical record, together with its position in the proof sequence. Evidence *of* a record, never the record itself. |
| **Operational record store** | The authoritative, complete state of academic history. The record of truth for this system. |
| **Rule set** | The complete set of rules in force for an educational level and academic period. Identified by an identifier that a finalized record carries. |
| **Academic period** | A named span of time with a status and a cycle type. Owned solely by ECS. |
| **Finalized record** | A record that has been approved and committed. Never altered; only superseded by an appended successor. |
| **Appended successor** | A new record created to correct a finalized one, linked to it by `parent_transaction_id`. |

---

## 11. Change control

**This requirement applies from the first approved version onward.** Pre-approval drafting — up to
and including the version that first earns approval — is governed by the review-and-approval
process itself, not by this section. The 2026-11-13 rewrite was pre-approval drafting: it
addressed the blocking findings of the independent review recorded as `WORK-039`, and it therefore
did not increment the version.

Changes to an **approved** specification require:

1. A `Change Request` recorded as a `Decision` item in the work ledger, stating what changes, why,
   and which sections are affected.
2. Independent review of the change.
3. Explicit human approval.
4. A version increment and an updated `updated` timestamp.

A change is never applied by editing this document alone.

---

## 12. Approval status

**Status: `Draft`.** This specification has **not** been approved. No approval Decision is recorded
in the work ledger (`WORK-016`, `WORK-032`). It may not be used as a parent specification for an
approved task until it is.

---

*End of specification.*
