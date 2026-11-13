---
spec_id: SRS-LMS-v1.0
id: SRS-LMS-v1.0
collection_id: SPEC-LMS-v1.0
version: 1.0
status: Approved
title: Software Requirements Specification - Blockchain-Enabled LMS
project: blockchain-enabled-lms
created: 2026-11-11T12:00:00Z
updated: 2026-11-13T05:00:00Z
---

# Software Requirements Specification - Blockchain-Enabled LMS

> **Terminology note.** "System of Record" has two distinct uses in this repository. In this
> document it always means the **operational record store** that holds the authoritative academic
> state (Sections 3.6 and 3.7). The framework's own use of the phrase — for the specification artifact layer
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
| **Integrity** | A finalized grade record is immutable in every field. A correction is *appended*, never substituted. |
| **Verifiability** | A third party can confirm that a final academic record existed, was authorized, and has not been altered, using only a published verification surface. |
| **Traceability** | Any record can be traced back to the assessment and the rule set that produced it. |
| **Longevity** | A record remains provable independently of the lifetime of any single service, because both the proof sequence and the canonical payload are archived. |
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
| **Academic administrators** (Dean, Principal, Chair, Head of Year) | Control over level transitions, and the authority to approve corrections. |
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
| C-4 | Allocate instructional resources to scheduled sections, and own instructor load. | FRAS |
| C-5 | Instantiate learning: sections, enrollments, scheduling. | ESS |
| C-6 | Compute the final grade from assessments under the governing formula, and own the appeal and review history. | GRA-Service |
| C-7 | Assemble the finalized academic record for a student-period, and commit its proof. | LGS |

### 2.2 Workflow W-1 — Academic period gatekeeping

**Trigger.** Any creation or update of a student academic record — an enrollment, a grade
submission, a section allocation, or a course or program definition that takes effect in a period.

**Participants.** AMS, ESS, FRAS, GRA-Service.

**Flow.**

1. The creating domain requests the governing context for the target educational level and academic
   period from ECS.
2. ECS resolves the academic period's current status.
3. If the status is not `Active`, ECS refuses the request and the creating domain must not proceed.
4. If the status is `Active`, ECS returns the governing rule set identifier, which the creating
   domain records against the record it is about to create.

**Rule.** No record that takes effect in an academic period may be created or modified in a period
whose status is not `Active` — **except** the period-close assembly and finalization of the
student-period record, which Workflow W-6 governs.

### 2.3 Workflow W-2 — Grade submission

**Trigger.** An instructor submits assessed results for an enrolled student in a section.
**Participants.** GRA-Service, ECS.
**Flow.**

1. The submission names the enrolled student, the section, the assessment, and the raw scores.
2. GRA-Service requests the governing grading formula from ECS for the student's educational level
   and the academic period in force.
3. GRA-Service applies the formula and produces a proposed final grade, recorded with the rule set
   identifier returned in step 2.
4. The grade is approved and recorded in the operational record store with status `Finalized`, and
   the approving authority is recorded against it.

**Rule.** A finalized grade must carry the rule set identifier under which it was computed.

**No proof is committed here.** A proof is committed over a *student-period record*, not over an
individual grade (Section 2.8).

### 2.4 Workflow W-3 — Appeal and correction

**Trigger.** A correction is required to a grade that has already been finalized.
**Participants.** GRA-Service, ECS, IAM, the approval chain, LGS.
**Flow.**

1. A `GradeAppealRecord` is raised against the finalized grade, referencing it by its transaction
   identity, with status `UnderReview`.
2. GRA-Service computes the proposed grade delta under the rule set identified in the original
   record.
3. The appeal passes through the approval chain that ECS supplies for the student's educational
   level. Each step is recorded.
4. On rejection, the appeal moves to `Rejected` and no further record is created.
5. On approval, the appeal moves to `Approved` and a **new, versioned grade record** is appended
   that references the original via `parent_transaction_id` and carries the status flag of the
   change. **No field of the original grade record is written.**
6. A **new** student-period record is assembled for that student and period, and is created
   directly in state `Finalized` (Section 2.9). The prior student-period record is not written to.
7. LGS commits a **new proof** over the new student-period record, appended to that student's
   sequence after the prior proof (Section 2.8).

**Rule (append-only).** A correction never overwrites the grade record it corrects. The operational
record store holds both, linked by `parent_transaction_id`.

> **Decision recorded.** The append-only model is adopted. The alternative — amending the original
> grade record in place — is explicitly rejected, because it destroys the evidence that a finalized
> record existed in the form it was finalized.

**Approval chain by level.** ECS supplies the chain required for the student's educational level.
The customary chains are: instructor → head of year → principal for primary and secondary;
instructor → chair → dean for college. A level with no chair has no chair step — the chain is
determined by the rule set, not assumed.

### 2.5 Workflow W-4 — Level transition

**Trigger.** A student's `LevelCompletionRecord` for a level reaches `Completed`.
**Participants.** GRA-Service, AMS, ECS, IAM, ESS.
**Flow.**

1. GRA-Service validates that the student meets the credit and pass milestones for the level, as
   defined by AMS and ECS.
2. An IAM-secured role at dean or principal authority manually approves the transition.
3. ESS updates the student's level to the next expected level — as determined by the rule set ECS
   supplies for the level just completed — and signals the transition.
4. The transition is recorded as a new versioned record linked to the prior one.

**The `LevelCompletionRecord`.** A student has one level-completion record per educational level. It
records the requirements met toward completing that level, and it is distinct from a section
enrollment: a section enrollment covers one course in one section, while a level-completion record
covers the whole level. It becomes `Completed` when all requirements for the level are met.

### 2.6 Workflow W-5 — College enrollment

**Trigger.** A student requests enrollment in a course or program at college level.
**Participants.** ESS, AMS, ECS.
**Flow.**

1. AMS validates the request against the prerequisite map for the student's program.
2. AMS confirms the student holds an active major program definition.
3. ECS supplies the capacity constraints in force for the academic period — the maximum credits
   a student may carry in the period, and the maximum students a section may hold.
4. ESS enrolls the student only if every constraint is satisfied, and records the outcome against
   the governing rule set. Where a constraint is not satisfied, the request moves to `Refused`.

**Capacity enforcement.** ESS is the single owner of enforcing capacity constraints, and it does so
at the point of enrollment (Section 3.3). No other domain re-derives or re-enforces them.

### 2.7 Workflow W-6 — Period close and record finalization

**Trigger.** An academic period moves to `Closed`.
**Participants.** GRA-Service, ECS, LGS.
**Flow.**

1. GRA-Service requests the governing rule set from ECS for the student's educational level and the
   period, and records the rule set identifier against the record. The rule set identifier is a
   **mandatory attribute** of a finalized student-period record.
2. For each student with finalized grades in the period, GRA-Service assembles the
   **student-period record**: the canonical `final_academic_record` payload defined by
   `WORK-LMS-CONTRACT-001`.
3. The student-period record is marked `Finalized`, and its status is recorded.
4. LGS commits a proof over the student-period record (Section 2.8).

**Rule.** A student-period record is finalized at period close, or when an approved appeal amends
an already-finalized aggregate, and only then is it proven. A grade finalized earlier in the period
is auditable in the operational record store immediately, but it is not itself proven — the proof
attests the period aggregate.

**Appeal and period close.** An appeal may be raised at any time. If it is approved **before** period
close, the student-period record does not yet exist, so no successor is needed — the corrected grade
is simply part of the aggregate assembled at close. If it is approved **after** period close, the
student-period record already exists in state `Finalized`, and W-3 step 6 creates a **new**
student-period record that supersedes it by linkage. Either way the prior record is never written.

### 2.8 Proof of finalization — the proof unit

**One proof unit, stated precisely:**

* **What is proved.** The finalized **student-period record** — the canonical `final_academic_record`
  payload for **one student, for one academic period**, as defined by `WORK-LMS-CONTRACT-001`.
* **Granularity.** One proof per finalized student-period record. A grade finalized mid-period does
  **not** produce a proof; the proof is committed at period close (Section 2.7).
* **How the proof is formed.** The canonical payload is reduced to its **canonical form** and a
  digest is computed over it. The proof commits that digest together with the transaction identity,
  the **canonical-form version** the reduction was performed under, the **digest algorithm identifier**
  used, and a linkage to the preceding proof in the sequence. Committing the version and the
  algorithm identifier is what makes the versioning guarantee below exercisable: a verifier learns
  which reduction rules and which algorithm to apply, and a change to either requires a new version
  rather than silently invalidating existing proofs.
* **What the digest covers.** The canonical form is **exactly the canonical field list declared by
  the record type** — for the student-period record: its identity, its content, the rule set
  identifier under which it was computed, the time of finalization, and the authorizing authority.
  The field list is **declared explicitly**, not derived from a general test, so two parties reducing
  the same record cannot disagree about which fields belong. Session identifiers, last-read markers,
  transport metadata and storage locators are excluded by the declaration, because including them
  would make the digest irreproducible. **The authority attestation and the time of finalization are
  inside the digest**, so they are tamper-evident, not merely committed alongside it. This places a
  requirement on the record type: the canonical payload must carry an explicit finalization-time
  field and an explicit authorizing-authority field (see Section 8.1).
* **How a verifier re-derives it.** A verifier obtains the canonical **payload** from the
  verification surface (Section 4.1), together with the canonical-form version, the digest algorithm
  identifier, and the canonical field list. It performs the reduction itself, computes the digest,
  and compares it with the committed digest. The surface does **not** publish the reduced bytes: if it
  did, the verifier would be trusting the publisher's reduction rather than re-deriving it, and the
  exclusion rules would go unverified.
* **The sequence.** One proof sequence per **student**: every proof ever committed for that student,
  in order, each linked to its predecessor. The linkage is **tamper-evident** — each element commits
  to its predecessor's value, so altering or removing one breaks every later link. The first element
  of a student's sequence is that student's **genesis proof**. A verifier is given the student's
  sequence from its genesis proof and walks it, which establishes that **no proof in that student's
  sequence was removed or reordered**; it does not by itself attest to proofs of other students.

**Rule.** The proof commits evidence of a record's existence and content. It is **not** the record,
and it does not replace the operational record store.

**Canonical form — required properties.** The canonical form is defined by the
`CAP-CANONICAL-FORM` capability artifact (`spec-workspace/library/Capabilities/canonical-form.md`),
which owns the detailed rules. It must satisfy, at minimum:

1. **Declared field set** — the fields included are exactly those the record type's canonical field
   list declares. The declaration, not a general test, is the authority.
2. **Volatile fields excluded by declaration** — a field whose value varies between otherwise
   identical records is excluded, and the exclusion is recorded in the record type's canonical field
   list rather than implied. A field may be both a property of the record and excluded; the
   declaration decides, not the property.
3. **Defined ordering** — fields are ordered by a stated rule, so the reduction is deterministic.
4. **Defined encoding** — one stated encoding is used, recorded in the capability artifact. Until it is
   recorded there, **no proof may be committed**.
5. **Versioned** — the canonical form carries its own version, and the proof commits that version, so
   a change to the rules does not silently invalidate proofs committed under the earlier version.

### 2.9 State transitions

#### Academic period

| From | Event | To |
|---|---|---|
| — | Period defined | `Draft` |
| `Draft` | Period opened for enrollment and assessment | `Active` |
| `Active` | Period closed | `Closed` |

`Closed` is terminal. A record may not be created or modified in a period that is not `Active`
(Workflow W-1).

#### Grade record

| From | Event | To |
|---|---|---|
| — | Assessment results submitted and a grade computed | `Proposed` |
| `Proposed` | Approved and recorded | `Finalized` |
| — | An appeal is approved against a finalized grade — a new grade record is appended, linked by `parent_transaction_id` | `Finalized` |

`Finalized` is **terminal**. No field of a finalized grade record is ever written. A correction does
not move a grade record to another state — it appends a new one (Workflow W-3).

#### Appeal record

| From | Event | To |
|---|---|---|
| — | Appeal raised against a finalized grade | `UnderReview` |
| `UnderReview` | The last authority in the ECS-supplied approval chain rejects the appeal | `Rejected` |
| `UnderReview` | The last authority in the ECS-supplied approval chain approves the appeal | `Approved` |

`Rejected` and `Approved` are terminal. On `Approved`, a successor grade record is appended
(Workflow W-3); the appealed grade record is unchanged.

#### Student-period record

| From | Event | To |
|---|---|---|
| — | Period closes and the record is assembled | `Finalized` |
| — | An approved appeal amends an already-finalized aggregate — a new record is created | `Finalized` |

`Finalized` is **terminal**. A later student-period record for the same student and period — for
example after an approved appeal — does not alter this one. It carries `parent_transaction_id`
pointing at the record it supersedes. There is no `Open` state: a student-period record is created
only when it is final, and it carries the rule set identifier that governed the period.

**Rule.** A finalized student-period record is never altered, and it never leaves the `Finalized`
state. Supersession is expressed **only** by a successor that links to it. There is no
`Superseded` state, because recording one would write to a finalized record and change the digest
computed over it.

#### Enrollment

| From | Event | To |
|---|---|---|
| — | Enrollment requested | `Requested` |
| `Requested` | Prerequisites and capacity constraints satisfied | `Enrolled` |
| `Requested` | A constraint is not satisfied | `Refused` |
| `Enrolled` | All requirements of the enrolled course are met | `Completed` |
| `Enrolled` | Withdrawn by the student or an administrator | `Withdrawn` |

`Refused` and `Withdrawn` are distinct terminal states: a refusal records that the system declined
the request, a withdrawal records that the student or an administrator ended it. A refused request
may be submitted again.

#### Level-completion record

| From | Event | To |
|---|---|---|
| — | Student begins study at a level | `InProgress` |
| `InProgress` | All requirements for the level are met | `Completed` |

`Completed` is terminal and triggers Workflow W-4.

---

## 3. Logical architecture boundaries and responsibilities

### 3.1 The seven service domains

| Domain | Responsibility | Operations it exposes | Operational record it owns |
|---|---|---|---|
| **IAM** | Identify and authorize actors; hold the user profile. | Authenticate an actor and return an access assertion; return the profile of an authenticated actor; resolve the authorities held by an actor. | `User`, `UserGroup`, `Scope`, `Authority` |
| **ECS** | **The rule authority.** Determine the rules in force for an educational level and academic period. | Given an educational level and academic period, return the governing rule set identifier and the rules it contains; given a period, return its current status; return the approval chain required for a level; return the capacity constraints in force for a level and period. | `EducationalLevel`, `AcademicPeriod`, `CycleType`, `FormulaRules` |
| **AMS** | Define what is taught: subjects, course definitions, degree structures, prerequisite maps. | Define a course, validated against the prerequisite map; define a program of study; return the prerequisites of a course. | `CourseCatalog`, `ProgramMap` |
| **FRAS** | Allocate instructional resources to scheduled sections; own instructor load. | Assign an instructor to a section, validated against instructor load; return an instructor's load record. | `Faculty`, `Assignment`, `LoadRecord` |
| **ESS** | Instantiate learning: sections, enrollments, scheduling; enforce capacity constraints at enrollment. | Enroll a student in a section, validated against prerequisites (AMS) and capacity (ECS); return a student's enrollment instance. | `Section`, `Enrollment` |
| **GRA-Service** | Compute the final grade under the governing formula; own grade, appeal, review and level-completion records. | Submit an assessment result and receive the computed final grade; raise an appeal against a finalized grade; record an approval step; assemble a student-period record. | `GradeRecord`, `GradeAppealRecord`, `ReviewLog`, `LevelCompletionRecord`, `StudentPeriodRecord` |
| **LGS** | Commit the immutable proof of a finalized student-period record; maintain the proof sequence. | Commit a proof over a finalized student-period record; return a student's proof sequence for verification. | `BlockHash`, `TransactionID` |

### 3.2 The closed set of ECS consumers

The following domains **must** consult ECS before any critical state change, and no other domain is
required to:

`AMS`, `ESS`, `FRAS`, `GRA-Service`

Each is shown consulting ECS in a workflow: AMS, ESS and FRAS in W-1 (Section 2.2), GRA-Service in
W-2 (Section 2.3). **LGS is not a consumer** — it commits a proof over an already-finalized record
and does not vary by educational level or academic period. ECS is the authority and is not a
consumer of itself. IAM is not a consumer — it authorizes actors and does not vary by level or
period.

### 3.3 Capacity and load ownership

**Three distinct constraints, each with exactly one owner. No constraint has two enforcers.**

| Constraint | Defined by | Enforced by | When |
|---|---|---|---|
| **Section capacity** — maximum students a section may hold | ECS | **ESS** | At enrollment |
| **Credit capacity** — maximum credits a student may carry in a period | ECS | **ESS** | At enrollment |
| **Instructor load** — maximum teaching load and availability of an instructor | FRAS | **FRAS** | At section allocation |

ECS *defines* the capacity constraints because they are level- and period-dependent, exactly like
every other rule. ESS *enforces* them because it is the domain that acts on them, and it does so
once, at enrollment. FRAS owns instructor load outright — it is a property of the instructor, not a
rule derived from a level or period, so neither ECS nor ESS is involved.

The instructor-load rule is not derived from ECS, though ECS is still consulted at the period
gate when a section is allocated (Section 3.2).

**No other domain re-derives or re-enforces a capacity constraint.**

### 3.4 Academic period ownership

`AcademicPeriod` is owned **solely by ECS**. ECS owns its identity, its status, its cycle type,
and the rule set applicable within it.

ESS does not own `AcademicPeriod`. ESS owns the **enrollment instances bound to** a period — the
sections scheduled inside it and the students enrolled in them — and references the period by its
ECS-owned identity.

### 3.5 The audit trail has a stated home

The operational record store holds the complete, authoritative academic history: finalized grade
records, appeal records, approval-chain review logs, student-period records, level-completion
records, and their linkage. GRA-Service does **not** hold this state transiently — its own working
state is transient, but every artifact it produces is committed to the operational record store as
it is produced.

### 3.6 The operational record store is the record of truth

The operational record store is the authoritative, complete, approved state of a student's academic
history. It is always able to answer, for any student and period, the full set of grades, appeals,
status flags and records — including those that a later appeal superseded, which remain present and
linked.

LGS commits proof over that state. LGS does not hold it, and does not replace it.

### 3.7 The operational record store is a component, not a domain

The operational record store is a **named durable component** of the system, and it is deliberately
not one of the seven service domains. It is the component that holds the authoritative state and
that publishes the canonical payload for verification.

**Responsibility.** Hold the authoritative, complete academic history. Publish the canonical
**payload** — not the reduced bytes — for verification, together with the canonical-form version, the
digest algorithm identifier, and the canonical field list. Retain superseded records with their
linkage.

**Operations it exposes.** Exactly two, and they are the only way anything outside the system reads
authoritative academic state:

1. **Read a student's period history** — returns the records for one student and period, including
   superseded ones and their linkage.
2. **Publish the canonical payload for verification** — returns the canonical **payload** of a
   finalized student-period record, together with the canonical-form version, the digest algorithm
   identifier, and the canonical field list, so that a verifier performs the reduction itself and
   recomputes the digest. The reduced bytes are never published.

**Ownership.** Each domain owns the records it produces *within* the store, and no domain owns
another domain's records. The store itself is a shared durable component; it has no domain
ownership of its own, because its contents are owned domain by domain and its behaviour is defined
by the two operations above.

**Why it is not a domain.** It has no rules of its own to enforce and no independent decision to
make. Treating it as a domain would give it an identity to own, which it does not have.

**Longevity.** The store is replicated and archived. Because the proof sequence and the canonical
payload are both archived, the loss of any single service — including the store itself — does not
destroy provability: a verifier can recompute the digest from an archived copy of the canonical
payload and check it against the archived proof sequence.

---

## 4. Non-goals and success criteria

### 4.1 Non-goals

The following are explicitly **out of scope** for this specification:

* **Implementation.** No language, framework, storage engine, deployment platform, or hosting
  arrangement is specified or implied. Those are chosen when the implementation plan is created.
* **Delivery model.** How the seven domains and the operational record store are deployed, scaled,
  or networked is not specified.
* **Field-level academic record contracts.** Defined by `WORK-LMS-CONTRACT-001`, not here.
* **Financial, payroll, and human-resources functions.** Only the instructional allocation that
  academic scheduling requires is in scope.
* **Learning content authoring.** Course content is referenced by identity, not modelled.
* **Third-party integration protocols.** Consumers outside the seven domains are not specified.
  **This is not the same as excluding third-party verification.** Section 2.8 requires two read-only
  surfaces: the **canonical payload** surface, owned by the operational record store (Section 3.7),
  and the **proof sequence** surface, owned by the Ledger Service (Section 3.1). What is excluded is a
  *protocol* by which other systems integrate with the seven domains.
* **Historical migration of existing records.** The system governs records it creates.
* **Correction of records finalized before this system existed.**

### 4.2 Success criteria

| # | Criterion | How it is judged |
|---|---|---|
| S-1 | A finalized grade record cannot be altered without leaving a linked, appended successor. | Audit of the operational record store shows original and successor both present, linked by `parent_transaction_id`, with the original's fields unchanged. |
| S-2 | Any finalized student-period record can be verified by a party with no access to the originating services. | The digest recomputes from the canonical payload published on the verification surface. |
| S-3 | Every finalized grade states the rule set it was computed under. | Every finalized grade carries a rule set identifier that resolves to a known rule set. |
| S-4 | No record that takes effect in an academic period is created in a period that is not active, except the period-close finalization of the student-period record. | No enrollment, grade submission, section allocation, course definition, or student-period record exists whose period was not `Active` at creation — other than a student-period record finalized at period close under W-6. |
| S-5 | A level transition is never automatic. | Every level transition records an explicit approval by a dean or principal authority. |
| S-6 | Rules in force are consistent across every domain that depends on them. | ECS is the sole source of the rule set for a level and period, and every dependent domain records the identifier it used. |
| S-7 | A proof is committed for every finalized student-period record, and only for those. | The set of committed proofs corresponds exactly to the set of finalized student-period records. |

---

## 5. Quality expectations

| Attribute | Expectation |
|---|---|
| **Immutability** | No field of a finalized grade record, and no field of a finalized student-period record, is ever written. A correction appends a new record and expresses the relationship by linkage; it does not amend what it corrects. |
| **Verifiability** | The proof of a finalized student-period record must be independently recomputable from the canonical payload published on the verification surface, by a party with no privileged access. |
| **Auditability** | Every state change to an academic record — creation, appeal, approval step, level transition — must be attributable to an actor and an authorization, and retained. |
| **Determinism** | Given the same rule set and the same assessed inputs, the computed grade must be identical. The rule set identifier must therefore be sufficient to reproduce a computation. |
| **Completeness** | The operational record store must be able to reconstruct a student's complete academic history at any point in time, including superseded records. |
| **Traceability of authority** | Every record that depends on a rule set must name it; every record that depends on an approval must name the approving authority; and both are inside the digested canonical form. |
| **Refusal over ambiguity** | When a rule set cannot be resolved, a governing context cannot be established, or an approval is absent, the operation must be refused rather than completed under an assumption. |
| **Latency** | The system must not make correctness contingent on timing. No workflow may race an academic period's status or an approval. |

---

## 6. Architecture composition decision

**Decision.** The system is composed of **seven independently-owned service domains, one rule
authority (ECS), one proof authority (LGS), and one shared durable component (the operational
record store)**, connected by explicit operation contracts rather than by shared state.

**Rationale.**

* A single rule authority is the only arrangement that makes the determinism and traceability
  expectations in Section 5 achievable. If two domains could each decide the applicable rules, the
  same computation could legitimately produce different answers.
* Separating the proof authority from the record authority keeps the record store complete and
  queryable (Section 3.6), instead of making the proof sequence the primary store.
* Treating the operational record store as a component rather than a domain keeps the seven service
  domains a closed set of decision-makers, while still giving the component that holds the
  authoritative state a name, a boundary, and exactly two operations (Section 3.7).
* Explicit operation contracts, rather than shared state, keep the boundaries in Section 3
  enforceable: a domain that needs another's data must call that domain's operation.

**Consequence.** Domain boundaries are contracts, not deployment boundaries. The seven domains and
the operational record store may be deployed together or separately; that choice is not made here.

---

## 7. Repository topology decision

**Decision.** The specification collection is rooted at
`spec-workspace/projects/blockchain-enabled-lms/`, and the codebase — when created — is rooted at
`generated-projects/blockchain-enabled-lms/`, bound to the collection by `binding.yaml`. This path
is fixed by the root `AGENTS.md`; it is not an open question.

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

**Consequence.** A codebase directory exists only after its `binding.yaml` is written. Until then
the collection's `binding.yaml` declares the identifier and version but has no binding target.

**Open.** Whether the exploratory `lms-platform/` and `src/identity/` directories are folded into
the codebase directory, or removed, is undecided — `WORK-017`, `WORK-035`.

---

## 8. Related artifacts

### 8.1 Artifacts in this collection

| Artifact | State | Relationship to this specification |
|---|---|---|
| `schema/final-academic-record.md` | exists, `Draft` | Normative rendering of the `final_academic_record` payload — the payload a proof is computed over (Section 2.8). Authoritative source: `tasks/task-LMS-CONTRACT-001-noncode.md`. **Open requirement:** the payload must carry an explicit finalization-time field and an explicit authorizing-authority field, and must declare its canonical field list, because Section 2.8 places all three inside the digest. |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | exists, `Draft` | Task specification that defines the field-level data contract for the finalized student-period record. |
| `tasks/task-LMS-CONTRACT-001-plan.md` | **not yet created** | The implementation plan for that task, produced by `wf-plan`. Its canonical path is listed in Section 7; the file does not exist yet. |
| `tasks/task-LMS-CONTRACT-001-noncode-calibration.md` | **not yet created** | The calibration record for that task, required by the root `AGENTS.md`. It does not exist yet. |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | exists, `Open` | The running handoff for that task. Disposable: deleted once its status is `Done`. |
| `binding.yaml` | exists | Declares this collection's identifier and version. Its codebase binding target is not yet determined. |
| `service-contracts.yaml` | exists | Runtime dependency manifest. It declares all seven domains: three have a runtime binding specified, and four are marked `not-yet-specified`. It also declares one service with `domain: unresolved` — a gateway whose place in the domain model is undecided. This manifest is a **runtime artifact**, not a source of authority; where it disagrees with Section 3, this document governs. |
| `AGENTS.md` (project) | exists | Project-local rules that bind any work in this collection. |

### 8.2 Section-anchor map

Child artifacts cite this specification by section. The anchors are stable:

| Concern | Section |
|---|---|
| Objectives and stakeholders | §1.2, §1.4 |
| Capabilities | §2.1 |
| Academic period gatekeeping | §2.2 |
| Grade submission | §2.3 |
| Appeal and correction; audit linkage | §2.4 |
| Level transition | §2.5 |
| College enrollment | §2.6 |
| Period close and record finalization | §2.7 |
| Proof unit; canonical form | §2.8 |
| State transitions and status vocabulary | §2.9, §9 |
| Domain responsibilities and operations | §3.1 |
| ECS consumers | §3.2 |
| Capacity and load ownership | §3.3 |
| Academic period ownership | §3.4 |
| Audit trail home | §3.5 |
| Operational record store | §3.6, §3.7 |
| Non-goals; success criteria | §4.1, §4.2 |
| Quality expectations | §5 |
| Composition decision | §6 |
| Repository topology | §7 |
| Glossary | §10 |

---

## 9. Open questions

| # | Question | Owner | Blocks |
|---|---|---|---|
| Q-1 | Which domain is the authoritative source for the value of the rule set identifier that a finalized record carries? | ECS / GRA-Service domain owners | `WORK-LMS-CONTRACT-001` (the `GoverningRuleSetID` field) |
| Q-2 | What is the agreed data format for `parent_transaction_id` across the domains that produce and consume it? | Domain owners | `WORK-LMS-CONTRACT-001` (the `parent_transaction_id` field) |
| Q-3 | Should the exploratory `lms-platform/` and `src/identity/` directories be folded into the codebase directory, or removed? | Architecture owner | `WORK-017`, `WORK-035` |
| Q-4 | Which capability artifacts define the shared `UserID`, `TimestampFormat`, `StatusEnums`, and `SchemaVersionConstraint` vocabularies that the **child task specification** adopts normatively? This specification defines its own status vocabulary inline (Section 9 below) and does not use those four. | Architecture owner | `WORK-020`, `WORK-LMS-CONTRACT-001` |
| Q-5 | Which domain owns the canonical form rules that `CAP-CANONICAL-FORM` defines — ECS as the rule authority, or LGS as the proof authority? | Architecture owner | `WORK-130` |
| Q-6 | Which domain does the `blockchain-gateway` service belong to, or is it outside the seven-domain model? | Architecture owner | `WORK-037` |

### 9.1 Status vocabulary used by this specification

| Entity | Status values |
|---|---|
| Academic period | `Draft`, `Active`, `Closed` |
| Grade record | `Proposed`, `Finalized` |
| Appeal record | `UnderReview`, `Approved`, `Rejected` |
| Student-period record | `Finalized` |
| Enrollment | `Requested`, `Enrolled`, `Completed`, `Refused`, `Withdrawn` |
| Level-completion record | `InProgress`, `Completed` |

These are normative for this project. The shared `StatusEnums` capability artifact does not yet
exist (Q-4); until it does, this table is the authority.

---

## 10. Glossary

| Term | Meaning in this document |
|---|---|
| **Grade record** | The immutable record of one assessed outcome for one student in one assessment. Terminal once `Finalized`. |
| **Student-period record** | The aggregate of a student's finalized grades for one academic period. This is what a proof is computed over. |
| **Level-completion record** | A student's record of requirements met toward completing one educational level. Distinct from a section enrollment. |
| **Proof** | A committed, independently recomputable digest over the canonical form of a finalized student-period record, together with its position in that student's proof sequence. Evidence *of* a record, never the record itself. |
| **Canonical form** | The deterministic reduction of a record to the exact bytes a digest is computed over. Defined by `CAP-CANONICAL-FORM`. |
| **Canonical field list** | The explicit declaration of which fields a record type contributes to its canonical form. The declaration, not a general test, decides membership. |
| **Genesis proof** | The first proof in a student's proof sequence. |
| **Approval chain** | The ordered sequence of authorities that must approve a change for a given educational level, supplied by ECS. |
| **Operational record store** | The authoritative, complete state of academic history. The record of truth for this system. |
| **Rule set** | The complete set of rules in force for an educational level and academic period. Identified by an identifier that a finalized grade carries. |
| **Academic period** | A named span of time with a status and a cycle type. Owned solely by ECS. |
| **Level transition** | A student's progression from one educational level to the next. Distinct from academic promotion or graduation. |
| **Superseded** | The relationship a later student-period record has to an earlier one, expressed by the successor's `parent_transaction_id`. **Not a state.** A superseded record is still `Finalized`, with its content and its digest unchanged. |
| **Appended successor** | A new record created to correct a finalized one, linked to it by `parent_transaction_id`. |

---

## 11. Change control

**This requirement applies from the first approved version onward.** Pre-approval drafting — up to
and including the version that first earns approval — is governed by the review-and-approval
process itself, not by this section. The 2026-11-13 rewrites were pre-approval drafting: they
addressed the blocking findings of the independent reviews recorded as `WORK-039` and `WORK-079`,
and they therefore did not increment the version.

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
