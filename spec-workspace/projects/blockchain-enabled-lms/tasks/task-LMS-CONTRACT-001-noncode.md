---
task_id: WORK-LMS-CONTRACT-001
version: 1.5
status: Approved
project: blockchain-enabled-lms
parent_spec: ../SRS_LMS_v1.0.md
parent_spec_id: SRS-LMS-v1.0
task_type: noncode
open_questions: []
inherited_open_questions: [Q-1, Q-2]
created: 2026-11-11T12:00:00Z
updated: 2026-11-16T09:26:06Z
---

# Task: Define the Canonical `final_academic_record` Data Contract (v1.5)

> **Provenance.** v1.0 was authored 2026-11-11. The body was restored from git blob `58f2453` on
> 2026-11-13 after the working-tree copy had been reduced to frontmatter only. v1.2 rewrote the
> acceptance criteria and the validation section. v1.3 was the first modelling pass. **v1.4 is the
> correction pass that answers all nineteen findings of the sixth independent review.** It removes
> three things the parent specification never declares — a record envelope, an embedded appeal
> object, and a change-classification field — and promotes the two facts the appeal object carried
> that the record does need. **v1.5 applies the eleven editorial corrections raised by the seventh
> review; no requirement changed.** `status` remains `Draft` until an approval Decision is recorded
> in the work ledger (see `WORK-009`).

## 1. Task Summary and Description

The parent specification delegates field-level academic record contracts to this task. SRS §4.1
lists them under Non-goals with the delegation stated explicitly: *"Field-level academic record
contracts. Defined by `WORK-LMS-CONTRACT-001`, not here."*

This task defines the canonical structure of the `final_academic_record` — the **student-period
record** for one student and one academic period (SRS §2.8), and the payload over which the Ledger
Service (LGS) commits its proof. It is the single authoritative declaration of the record's fields,
types, cardinalities, nullability, and canonical field list.

**The record is the canonical payload.** This contract declares no envelope, no wrapper, and no
storage metadata. SRS §2.8 reduces *the canonical payload* to its canonical form, and SRS §3.7
publishes *the canonical payload* for verification; the two must therefore be the same object, or a
verifier cannot recompute the digest from what it is given. §4.1 states this in full.

It defines **structure only**. It defines no computation, no ECS rule content, and no runtime
behaviour.

## 2. In-Scope Activities

* Declaring every field of the record with its data type, cardinality and nullability.
* Declaring the two encapsulated objects — the `academic_history` entry and `EnrollmentDetail` —
  with their own field sets, so that no field exists only in the rendering.
* Declaring the **canonical field list** — the ordered list of fields the digest covers — and
  recording that no field of this record type is excluded from it, with the reason. SRS §2.8 and
  §8.1 place this on the record type; `CAP-CANONICAL-FORM` confirms the declaration belongs to the
  record type's own specification.
* Declaring the record's **finalization-time** and **authorizing-authority** fields, which SRS §2.8
  requires to be inside the digest.
* Declaring the record's **state** field, drawn from the SRS §9.1 vocabulary.
* Establishing the versioning rule for the schema, including the compatibility meaning of a MAJOR,
  MINOR and PATCH change.
* Declaring `GoverningRuleSetID` — type, cardinality, and the citation of SRS §3.1, §4.2 S-6 and
  §2.7 step 1 for ECS authority. Authoring ECS rule content is excluded.
* Declaring `parent_transaction_id` linkage on every superseding record, per SRS §2.9:306-321 and
  §5 (Immutability).
* Designating exactly one payload encoding.
* Updating this task's entries in `binding.yaml` — version, status and the calibration record — so
  the collection index matches the artifacts it indexes.

## 3. Out-of-Scope Activities

1. Implementation of any microservice logic or data transformation. This task defines the target
   structure; nothing here is built.
2. Writing database migration scripts.
3. Authoring ECS rule content — including **value domains for academic judgement**. Which
   assessment types exist, which achievement levels a school level uses, what counts as a passing
   score, and which levels use a weighted grade-point average are rule content (SRS §3.1), not
   structure. This contract declares the *field* that carries such a value and does not constrain
   the value.
4. Defining the canonical-form reduction rules, the field ordering rule, or the digest algorithm.
   `CAP-CANONICAL-FORM` owns them under SRS §2.8. This contract declares **which** fields are
   reduced, not **how** they are reduced.
5. The **canonical-form version** and the **digest algorithm identifier**. SRS §2.8:222-228 places
   both in the proof, and SRS §3.7:437-440 has the verification surface publish them alongside the
   payload. They are not fields of this record.
6. Resolving the parent's open questions **Q-1** (authoritative source of the rule set identifier's
   value) and **Q-2** (`parent_transaction_id` data format). A child specification cannot close a
   parent question. This contract therefore treats both identifiers as opaque and declares no
   internal format for either.
7. Runtime validation. The surfaces that enforce this contract at run time are implementation
   concerns specified by the implementation plan, not by this contract.
8. Any API, user-interface, transport, or persistence-mechanism definition.
9. **Every other record type.** This contract defines the student-period record only. It does not
   define `GradeRecord`, `Enrollment`, `LevelCompletionRecord`, or `GradeAppealRecord`, each
   of which is owned by a service domain and has its own field-level contract under the same SRS
   §4.1 delegation. In particular, `GradeAppealRecord` is a **GRA-Service-owned operational
   record** (SRS §3.1:359) and is not a member of the student-period record. The student-period
   record carries no appeal object, no appeal identifier, and no change-classification field:
   SRS §2.4 step 5 attaches the change flag to the appended *grade* record, and SRS §2.9:318-321
   states that supersession of a student-period record is expressed **only** by a successor that
   links to it.

## 4. Expected Behavior

The contract must satisfy five properties, each anchored to the approved parent specification.

1. **Immutability and append-only correction** — SRS §5 (Immutability), §2.9:306-321.
   A finalized record is never written. Every amendment appends a new record carrying a mandatory
   `parent_transaction_id`. The superseded record's fields remain byte-identical and both records
   remain retrievable (SRS §3.6). Supersession is expressed by that link and by nothing else: there
   is no `Superseded` state, because recording one would write to a finalized record and change the
   digest computed over it (SRS §2.9:318-321).
   `parent_transaction_id` names the same concept at every level of the model — *the record this one
   supersedes* — and resolves within that record type. On a student-period record it points at the
   superseded student-period record; on a grade record it points at the superseded grade record
   (SRS §2.9). It is the **transaction identity** under which the superseded record's proof was
   committed (SRS §2.8:222-224); its data format is SRS Q-2 and is not declared here.

2. **Governed state** — SRS §3.1:355, §2.7:194-196, §4.2 S-6, §5 (Determinism, Traceability of
   authority).
   `GoverningRuleSetID` is mandatory, of type string, cardinality 1..1, on every finalized
   student-period record. ECS supplies the rule set and GRA-Service records its identifier against
   the record (SRS §2.7 step 1). Its value must be sufficient to reproduce the computation (SRS §5
   Determinism). This contract names the identifier and does not constrain its internal form; SRS
   Q-1 remains open in the parent and governs if it resolves differently.

3. **Contract integrity and versioning** — `CAP-SCHEMAVERSIONCONSTRAINT` for the format, the
   mandatory top-level presence and the controlled rejection. The three compatibility meanings below
   are **this contract's own decision**: the capability fixes the format and the rejection rule and
   defines no per-segment semantics.
   `schema_version` is a mandatory top-level field, formatted `MAJOR.MINOR.PATCH`. A MAJOR change is
   incompatible with prior versions; a MINOR change is a backward-compatible addition; a PATCH
   change is a clarification with no structural effect. A payload whose `schema_version` is
   unsupported is rejected, never coerced.
   This field is the **record type's** version. It is not the canonical-form version, which
   `CAP-CANONICAL-FORM` property 5 defines as distinct and which the proof commits (see §3 item 5).
   SRS §2.8 property 5 is cited for that distinction only: it versions the canonical form, not the
   record type.

4. **Single encoding** — SRS §2.8 property 4, which requires that *one stated encoding* is used.
   The designated encoding for this record is **JSON**. This contract names no alternative.
   The **canonical form's** encoding is not this contract's to state: `CAP-CANONICAL-FORM`
   property 4 records it as the UTF-8 encoding of a canonical JSON text, declared fields only, in
   declared order. The two statements are consistent — the record is JSON, and its reduction is
   canonical JSON — but they are separate obligations with separate owners.

5. **Digest-ready declaration** — SRS §2.8:229-244, §8.1:577, §5 (Traceability of authority).
   The contract declares, explicitly and in order, the fields the digest covers. The declaration
   includes the record's identity, its content, the rule set identifier, the **time of
   finalization**, the **authorizing authority**, and the declaration itself. It also records that
   no field of this record type is excluded, with the reason. SRS §2.8:236-238 states the
   requirement directly: *"the canonical payload must carry an explicit finalization-time field and
   an explicit authorizing-authority field"*, and SRS §8.1 adds that it *"must declare its
   canonical field list, because Section 2.8 places all three inside the digest."*

### 4.1 The record is the canonical payload

**There is no envelope.** The record type declares one flat object, and that object is the canonical
payload. Three SRS statements force this:

* SRS §2.8:222 — *"The canonical payload is reduced to its canonical form and a digest is computed
  over it."* The digest is computed over the payload.
* SRS §3.7:437-440 — the verification surface *"returns the canonical **payload** of a finalized
  student-period record, together with the canonical-form version, the digest algorithm identifier,
  and the canonical field list, so that a verifier performs the reduction itself and recomputes the
  digest."* The payload is what a verifier receives.
* SRS §4.2 S-2:484 — *"The digest recomputes from the canonical payload published on the
  verification surface."*

A field that is digested but not published is unverifiable, and a field that is published but not
digested is unprotected. The only arrangement that satisfies all three statements is that the set of
digested fields and the set of published fields are **the same set**. Declaring a wrapper object
with fields outside the digest would put storage metadata on the verification surface, which
`CAP-CANONICAL-FORM` property 2 excludes by default, or would digest fields the surface never
publishes. Neither is acceptable. This contract therefore declares no envelope, and every field in
§4.2 is both digested and published.

**Identity.** SRS §2.8:218-219 defines the proof unit as *"the canonical `final_academic_record`
payload for **one student, for one academic period**"*. The record's identity is therefore
`student_id` together with `academic_period`. A superseding record for the same student and period
is distinguished by its `parent_transaction_id` and by its content. **No record identifier is
declared**, because the parent declares none: SRS §2.8:222-224 has the proof commit *the transaction
identity* alongside the digest, and SRS Q-2 leaves the representation of that identity open. Adding
an identifier field would be a field the parent never asks for, and excluding it from the digest
would leave a digested-but-unpublished gap.

### 4.2 Field set

| Field | Type | Cardinality | Nullable | In digest |
|---|---|---|---|---|
| `schema_version` | string, `MAJOR.MINOR.PATCH` (`CAP-SCHEMAVERSIONCONSTRAINT`) | 1..1 | No | Yes |
| `student_id` | string, `CAP-USERID` | 1..1 | No | Yes |
| `academic_period` | string, opaque — the ECS-owned period identity (SRS §3.4) | 1..1 | No | Yes |
| `educational_level` | string, enum `Primary School`, `Secondary School`, `College` (SRS §1.3) | 1..1 | No | Yes |
| `record_state` | string, enum `Finalized` (SRS §9.1) | 1..1 | No | Yes |
| `GoverningRuleSetID` | string, opaque — supplied by ECS (SRS §2.7 step 1) | 1..1 | No | Yes |
| `parent_transaction_id` | string, opaque — the transaction identity of the superseded record | 0..1 | No | Yes |
| `academic_history` | array of `academic_history` entry objects (§4.4.1) | 1..N | No | Yes |
| `cumulative_weighted_gpa` | number | 0..1 | No | Yes |
| `total_credits` | number | 0..1 | No | Yes |
| `finalized_at` | string, ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` (`CAP-TIMESTAMPFORMAT`) | 1..1 | No | Yes |
| `authorized_by` | string, `CAP-USERID` — the authority that authorized finalization | 1..1 | No | Yes |
| `canonical_field_list` | array of string — the ordered declaration in §4.5 | 13..13 | No | Yes |

**Cardinality and nullability are separate declarations.** Cardinality states whether the field is
present. Nullability states whether a present field may carry a null value. No field in this
contract permits null: a field that does not apply is **absent**, never null. The minimum
cardinality is therefore `0` in every case where a field may be absent, and the nullability is `No`
throughout.

**`educational_level`.** The three values are those SRS §1.3 places in scope. The contract declares
the field's domain from that table and declares nothing about the rules that apply at each level;
those are ECS content (SRS §3.1:355).

### 4.3 Presence rules

These follow from the SRS and are normative.

| Rule | Statement | Authority |
|---|---|---|
| R-1 | `record_state` is `Finalized` and no other value. A student-period record is created only when it is final; there is no `Open` state and no `Superseded` state. | SRS §2.9:306-321, §9.1 |
| R-2 | `parent_transaction_id` is present exactly when this record supersedes an earlier student-period record for the same student and period, and absent on an original record. | SRS §2.9:306-321 |
| R-3 | `academic_history` carries at least one entry. A record is assembled only for students with finalized grades in the period. | SRS §2.7:197-200 |
| R-4 | `finalized_at` and `authorized_by` are present on every record, including a superseding one. | SRS §2.8:229-238, §5 |

**No presence rule is declared for `cumulative_weighted_gpa` or `total_credits`.** SRS §1.3:53
describes College's emphasis as *"Credit accumulation, weighted grade-point average"*, but an
emphasis is not a presence rule. Conditioning these fields on `educational_level` would be invented
policy. Both are declared `0..1`; whether a level uses them is ECS rule content (SRS §3.1:355).

**No presence rule is declared for `parent_transaction_id` beyond R-2.** SRS §2.9:318-321 states
that supersession *"is expressed **only** by a successor that links to it"*. The contract therefore
declares no change-classification field and no appeal reference: adding one would give supersession
a second expression the parent does not authorise.

### 4.4 Encapsulated objects

Each object below is declared here in full. No object's field set is left to the rendering.

#### 4.4.1 `academic_history` entry

One finalized assessed outcome for the student within the period. It carries the fields common to
every outcome; the enrollment-specific detail is carried by the optional `EnrollmentDetail` object
in §4.4.2, so no fact is represented twice.

| Field | Type | Cardinality | Nullable |
|---|---|---|---|
| `assessment_id` | string, opaque — unique within the operational record store | 1..1 | No |
| `assessment_type` | string — the kind of assessment; the set of kinds is ECS rule content (SRS §3.1) | 1..1 | No |
| `section_id` | string, opaque — the section in which the assessment was taken | 1..1 | No |
| `grade_raw` | number — the score before finalization | 1..1 | No |
| `grade_final` | string — the finalized grade | 1..1 | No |
| `max_score` | number — the maximum attainable score | 1..1 | No |
| `weight` | number — the weighting applied in the aggregate | 0..1 | No |
| `achievement_level` | string — the band awarded; the set of bands is ECS rule content (SRS §3.1) | 0..1 | No |
| `submission_timestamp` | string, ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` (`CAP-TIMESTAMPFORMAT`) | 1..1 | No |
| `enrollment_detail` | `EnrollmentDetail` object (§4.4.2) | 0..1 | No |

`grade_final` is mandatory. A student-period record is assembled only from students with finalized
grades (SRS §2.7 step 2) and is created only when final (SRS §2.9), so a proposed grade cannot
appear in it.

`section_id` is declared **on the entry**, not inside the optional object. Every assessed outcome is
taken in a section, so an entry that carried no optional object would otherwise record an outcome
with no section. SRS §2.5:167-170 confirms a section enrollment covers one course in one section.

`weight` and `achievement_level` are absent where the educational level does not use them; they are
not null. Which levels use them is ECS rule content, so this contract does not enumerate levels.

#### 4.4.2 `EnrollmentDetail`

The enrollment-specific detail of an outcome. It carries only what the entry does not already
carry; `student_id` is record-level, and `section_id`, `assessment_id` and `submission_timestamp`
are entry-level and are not repeated here.

| Field | Type | Cardinality | Nullable |
|---|---|---|---|
| `enrollment_id` | string, opaque | 1..1 | No |
| `course_id` | string, opaque | 1..1 | No |
| `enrollment_date` | string, ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` (`CAP-TIMESTAMPFORMAT`) | 1..1 | No |
| `credits_earned` | number — credits applied toward the period | 0..1 | No |

**`enrollment_status` is not declared here.** Enrollment state is a property of the enrollment
record, which ESS owns (SRS §3.1); SRS §9.1 defines its vocabulary for that record type. Freezing a
transient enrollment state into an immutable digested record would also assert that the state cannot
change after finalization, which the SRS does not say. The entry records what the student achieved,
not the current state of the enrollment that produced it.

#### 4.4.3 Record types this contract does not define

| Record type | Owner | Why it is not a member of this record |
|---|---|---|
| `GradeAppealRecord` | GRA-Service (SRS §3.1:359) | It is its own operational record, raised against a finalized grade and referencing it by transaction identity (SRS §2.4 step 1). It has its own status vocabulary (SRS §9.1) and its own field-level contract. |
| `GradeRecord` | GRA-Service | It is the record an appeal corrects and the record that carries the change flag (SRS §2.4 step 5). Its fields are a separate contract. |
| `Enrollment` | ESS | It carries the enrollment state this contract deliberately does not copy (§4.4.2). |
| `LevelCompletionRecord` | GRA-Service | It covers a whole level, not one period, and is distinct from a section enrollment (SRS §2.5:167-170). |

### 4.5 Canonical field list

The digest covers exactly the fields below, **in this order**. `CAP-CANONICAL-FORM` property 3
makes the declared order the canonical order, and applies it recursively to nested structures; the
entry and `EnrollmentDetail` field orders declared in §4.4 are the nested orders.

| # | Field |
|---|---|
| 1 | `schema_version` |
| 2 | `student_id` |
| 3 | `academic_period` |
| 4 | `educational_level` |
| 5 | `record_state` |
| 6 | `GoverningRuleSetID` |
| 7 | `parent_transaction_id` |
| 8 | `academic_history` |
| 9 | `cumulative_weighted_gpa` |
| 10 | `total_credits` |
| 11 | `finalized_at` |
| 12 | `authorized_by` |
| 13 | `canonical_field_list` |

This satisfies each element SRS §2.8:229-238 requires the digest to cover: identity (2 and 3),
content (4, 5, 7–10), the rule set identifier (6), the time of finalization (11), and the
authorizing authority (12). Field 13 is the declaration itself, which SRS §8.1 places inside the
digest. Field 1 is the contract version that `CAP-SCHEMAVERSIONCONSTRAINT` requires to be a
mandatory top-level field; SRS §2.8 does not name it as a digest element, but a declared field of
the record is inside the digest by declaration.

**The list contains its own name.** This is intentional and not circular: the value of
`canonical_field_list` is a finite array of field names, and that array is one of the values the
digest covers. A verifier reads the list from the payload, checks that it equals the list declared
here, and reduces accordingly. If a party altered the array, the digest would change, so the
declaration is tamper-evident rather than merely asserted. The array's cardinality is fixed at
`13..13` (§4.2), so it cannot be shortened or extended without failing validation.

### 4.6 Exclusions from the canonical form

`CAP-CANONICAL-FORM` property 2 requires an exclusion to be **recorded**, not implied. This record
type declares **no exclusion**: every field it declares is in the canonical field list, and the
record has no field that is not in the list.

The five categories property 2 excludes by default are recorded here as considered and absent:

| Default-excluded category | Applies to this record type? | Reason |
|---|---|---|
| Session identifiers | No | The record type declares no session field. |
| Last-read / access markers | No | The record type declares no access marker. |
| Transport and envelope metadata | No | The record type declares no envelope and no transport field (§4.1). |
| Storage and physical locators | No | The record type declares no storage locator. |
| Cache and materialization state | No | The record type declares no materialization field. |

`finalized_at` is **not** excluded. `CAP-CANONICAL-FORM` property 2 states the distinction
explicitly: *"A field that records when a record was finalized is not volatile — it is a property
of the record — and is included."* The record's content includes the finalization event.

### 4.7 Encoding

The record is encoded as JSON. No second encoding is named anywhere in this contract.

Timestamps are strings in ISO 8601 extended form `YYYY-MM-DDTHH:MM:SSZ`, per `CAP-TIMESTAMPFORMAT`.
No numeric epoch representation is used anywhere in the record. The rendering constrains each
timestamp with the exact pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$` rather than a general
date-time format, because the general form admits fractional seconds and numeric offsets that this
contract excludes.

Identifiers declared "opaque" — `academic_period`, `parent_transaction_id`, `GoverningRuleSetID`,
`assessment_id`, `section_id`, `enrollment_id`, `course_id` — carry no internal format constraint.
Each must be unique where uniqueness is stated, and stable for the life of the record. SRS Q-1 and
Q-2 remain open and govern the two identifiers they name.

## 5. Acceptance Criteria

This task produces a specification and a normative rendering, not running code. Every criterion
below is verified by document review, and every criterion names the evidence that proves it. None
requires a pipeline, a test harness, or a deployed service.

| ID | Criterion | Checked against | Evidence that proves it |
|---|---|---|---|
| **AC-1** | The contract declares `parent_transaction_id` on every superseding record, states that the superseded record's fields are never rewritten, and states that supersession is expressed only by that link — with no `Superseded` state and no second change-classification field. | SRS §2.9:306-321, §5 (Immutability) | The §4.2 field-table row; presence rule R-2; the §4 principle 1 statement; the §4.3 statement that no change-classification field is declared. |
| **AC-2** | `GoverningRuleSetID` is declared string, 1..1, mandatory on every finalized student-period record, attributed to ECS as supplier and GRA-Service as recorder, and stated to be sufficient to reproduce the computation. | SRS §2.7:194-196, §3.1:355, §4.2 S-6, §5 (Determinism) | The §4.2 field-table row; the §4 principle 2 authority statement. |
| **AC-3** | Every field the digest covers is a field of the record, and the record is the unit the verification surface publishes — so a verifier holding the published record holds every digested field. | SRS §2.8:222-244, §3.7:427-440, §4.2 S-2 | The §4.1 statement and its three citations; the §4.5 list, whose 13 entries are exactly the 13 fields of §4.2; the §4.6 record that no field is excluded. |
| **AC-4** | `schema_version` is declared mandatory and top-level, formatted `MAJOR.MINOR.PATCH`, the compatibility meaning of a MAJOR, MINOR and PATCH change is stated, an unsupported value is stated to be rejected rather than coerced, and the field is distinguished from the canonical-form version. | `CAP-SCHEMAVERSIONCONSTRAINT` (format, presence, rejection); SRS §2.8 property 5 (for the distinction only) | The §4.2 field-table row; the §4 principle 3 statement, including the distinction from `CAP-CANONICAL-FORM` property 5. |
| **AC-5** | Exactly one record encoding is designated, the contract names no second alternative anywhere in its text, and the canonical form's encoding is attributed to `CAP-CANONICAL-FORM` rather than claimed here. | SRS §2.8 property 4; `CAP-CANONICAL-FORM` property 4 | The §4 principle 4 statement and the §4.7 encoding statement; a full-text search of this document for a competing format name returning no result. |
| **AC-6** | Every field in the record — top-level and each of the two encapsulated objects — declares a type, a cardinality and a nullability; no field permits null; and no field appears in the normative rendering that is absent from this specification. | This specification §4; project `AGENTS.md` §3 | Appendix A, the field coverage table, with one row per field and `Type`, `Cardinality` and `Nullable` columns; plus the field tables in §4.2, §4.4.1 and §4.4.2. |
| **AC-7** | Every timestamp in the record is declared as an ISO 8601 string `YYYY-MM-DDTHH:MM:SSZ`; no numeric epoch representation appears. | `CAP-TIMESTAMPFORMAT` | Appendix B, the timestamp inventory, listing every timestamp field with its declared type; plus the §4.7 statement. |
| **AC-8** | The contract declares an ordered canonical field list, records that no field is excluded and that the five default-excluded categories are absent, and states that the declared order is the canonical order. | SRS §2.8:229-238, §8.1; `CAP-CANONICAL-FORM` properties 1, 2, 3 | The §4.5 ordered table; the §4.6 exclusion record with its per-category reasons. |
| **AC-9** | The contract declares an explicit finalization-time field and an explicit authorizing-authority field, both mandatory, and both named in the canonical field list. | SRS §2.8:235-238, §8.1:577, §5 (Traceability of authority) | The §4.2 rows for `finalized_at` and `authorized_by`; positions 11 and 12 of the §4.5 list; presence rule R-4. |

**Verification method.** Independent document review against the sections named in the "Checked
against" column, using the evidence each criterion identifies. The reviewer records a pass or fail
per criterion. A criterion that cannot be evaluated from the named evidence is a defect in the
criterion, not a pass.

## 6. Dependencies and Sources

**Parent specification** — `SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, `status: Approved`, Decision
`WORK-039`). Sections relied on: §1.3 (educational levels), §2.4 (Workflow W-3), §2.5 (level
transition and section enrollment), §2.7 (Workflow W-6), §2.8 (proof unit, canonical form), §2.9
(state transitions), §3.1 (ECS authority and record ownership), §3.4 (academic period ownership),
§3.6–§3.7 (the operational record store), §4.1 (the delegation), §4.2 (S-2, S-6), §5 (quality
expectations), §8.1 (artifacts), §9.1 (status vocabulary).

**Participating service domains** (each defined in SRS §3.1):

| Domain | Participation |
|---|---|
| ECS | Supplies the rule set; owns `AcademicPeriod` identity and status. |
| GRA-Service | Assembles the record and records the rule set identifier (SRS §2.7 step 1). |
| LGS | Commits the proof over the finalized record (SRS §2.7 step 4). |

The table lists the domains that **author** the record. Identities the record references are owned
elsewhere: ESS owns `Section` and `Enrollment` (SRS §3.1:358), and AMS owns the course catalog
(SRS §3.1:356).

**Adopted capability artifacts** — all under `spec-workspace/library/Capabilities/`:
`CAP-USERID` (identifier properties), `CAP-TIMESTAMPFORMAT` (timestamp form),
`CAP-STATUSENUMS` (status vocabulary), `CAP-SCHEMAVERSIONCONSTRAINT` (`schema_version`),
`CAP-CANONICAL-FORM` (canonical form properties 1–5).

## 7. Validation Requirements

Validation for this task is **document-level**, and the method, evidence and reviewer are those
stated in §5: an independent reviewer checks each acceptance criterion against the section it
names, using the evidence the criterion identifies.

Two evidence artifacts are **produced by this task** and are part of its deliverable, not left for
the reviewer to construct:

* **Appendix A — Field coverage table.** One row per field in the record, with its type, cardinality
  and nullability, and the object that declares it. This is the evidence for AC-6.
* **Appendix B — Timestamp inventory.** Every timestamp field with its declared type. This is the
  evidence for AC-7.

**The schema is structural.** The rendering in `schema/final-academic-record.md` encodes field
names, types, enumerations, required-ness and closed field sets. Presence rules R-1, R-3 and R-4
are encoded: R-1 as a single-value enumeration, R-3 as a minimum array length, and R-4 as
required-ness. **R-2 is the only presence rule not encoded**, because it is a condition on when a
record may be created rather than on its shape. R-2 is checked when the record is assembled
(GRA-Service, SRS §2.7 step 2) and at the proof commit boundary (LGS, SRS §2.7 step 4).

No validation pipeline is constructed by this task, and none may be required by it — building one
is implementation, which §3 item 7 excludes.

## 8. Consistency

The authoritative definition of this contract is this document. Its normative rendering is
`schema/final-academic-record.md` (`SCHEMA-LMS-FAR-v1.0`, `rendered_from_version: 1.5`). The
rendering restates this specification and must not introduce a requirement this specification does
not authorise; where the two disagree, this specification wins and the rendering is the defect
(project `AGENTS.md` §3).

## 9. Resolved Questions

| Question | Resolution | Authority |
|---|---|---|
| Official authority for `GoverningRuleSetID` | ECS supplies the rule set; GRA-Service records its identifier against the record. The identifier is opaque to this contract. SRS Q-1 remains open in the parent and governs if it resolves differently. | SRS §2.7 step 1, §3.1, §4.2 S-6 |
| Format of `parent_transaction_id` | Opaque. Its only normative requirement is that it identifies the transaction under which the superseded record's proof was committed. SRS Q-2 remains open in the parent and governs the representation. | SRS §2.8:222-224, §2.9, §5 (Immutability) |
| Whether the record has an envelope | No. The digest is computed over the canonical payload (SRS §2.8:222) and the verification surface publishes the canonical payload (SRS §3.7:437-440), so the record is the payload. | SRS §2.8, §3.7, §4.2 S-2 |
| Whether the record carries an appeal object or a change classification | No. `GradeAppealRecord` is GRA-Service-owned (SRS §3.1:359); the change flag belongs to the appended grade record (SRS §2.4 step 5); supersession of a student-period record is expressed only by `parent_transaction_id` (SRS §2.9:318-321). | SRS §2.4, §2.9, §3.1 |
| Whether GPA and credits are conditional on the College level | No. SRS §1.3 states an emphasis, not a presence rule. Both are optional and their use is ECS rule content. | SRS §1.3, §3.1 |

## 10. Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-11 | Initial task specification. |
| 1.1 | 2026-11-13 | Body restored from blob `58f2453`; ECS rule-authoring boundary added (`WORK-066`); capability citations added. |
| 1.2 | 2026-11-16 | Acceptance criteria replaced with evidence-bearing criteria; §7 rewritten as document-level verification; out-of-scope completed; SRS citations added; single encoding designated; consistency note added; resolved questions moved out of frontmatter. Corrected anchors previously asserted in the ledger: success criteria are SRS §4.2, not §5; Workflow W-3 is §2.4, not §2.3. |
| 1.3 | 2026-11-16 | First modelling pass. Declared the canonical field list and the exclusions; added `finalized_at`, `authorized_by`, `record_state`, `student_id`, `canonical_field_list` and `appeal_record`; promoted the four objects' field sets into this document; separated cardinality from nullability; removed invented identifier formats and invented academic policy; added Appendices A and B. |
| 1.4 | 2026-11-16 | **Correction pass answering all nineteen findings of the sixth independent review.** Removed the record **envelope** (`recordId`, `recordType`, `ownerId`, `createdAt`, `updatedAt`): the SRS declares no envelope, the digest is computed over the canonical payload and the verification surface publishes the canonical payload, so a digested envelope field is unpublished and an excluded envelope field is unprotected (`C-01`, `W-01`). The record is now one flat object and the canonical list is exactly its 13 fields. Removed the embedded `GradeAppealRecord` object and the `change_status` field: the appeal is a GRA-Service-owned record and the change flag belongs to the appended grade record (`W-03`, `W-14`); supersession is expressed only by `parent_transaction_id` (`W-09`). Deleted `GradeAssessment`, whose `assessment_record_id` and `computed_grade` duplicated the entry's `assessment_id` and `grade_final`, and promoted `section_id` and `submission_timestamp` onto the entry (`C-02`, `W-10`). Removed `enrollment_status` from `EnrollmentDetail` and `section_id` with it. Removed presence rule R-5: SRS §1.3 states an emphasis, not a presence rule, so conditioning GPA and credits on the College level was invented policy (`W-04`). Declared `educational_level`'s three-value domain from SRS §1.3. Fixed `canonical_field_list` to `13..13` (`W-02`). Re-anchored four citations from SRS §3.2/§3.3 to §3.1 (`W-11`); dropped §4.2 S-3 from AC-2 (`W-12`); repointed AC-4's evidence to §4.2 and `CAP-SCHEMAVERSIONCONSTRAINT` (`W-05`); added type, cardinality and nullability columns to Appendix A (`W-06`); rendered one complete schema whose `$ref` values resolve (`W-07`); replaced `format: date-time` with an exact pattern (`W-08`); stated that the schema is structural and named where presence rules are validated (`W-09`); added `binding.yaml` to the in-scope list (`W-13`); recorded inherited questions Q-1 and Q-2 (`I-03`). |
| 1.5 | 2026-11-16 | **Editorial corrections answering the seventh review's six warnings and five infos; no requirement changed.** AC-1 and §4 principle 1 no longer cite SRS §4.2 S-1, which is a grade-record criterion (`V14-W3`); the append-only authority is §2.9:306-321 and §5. The three MAJOR/MINOR/PATCH meanings are stated as this contract's own decision, with `CAP-SCHEMAVERSIONCONSTRAINT` cited for format, presence and rejection only (`V14-W4`). R-2 is now stated to be the only presence rule the schema does not encode — R-4 is encoded as required-ness — and R-2's check points are GRA-Service assembly and the LGS commit boundary, not ECS (`V14-W2`, `V14-W5`). `EnrollmentRecord` renamed to the SRS name `Enrollment` (`V14-I1`). The canonical-list mapping accounts for position 1 (`V14-I3`). The dependency table now states that ESS and AMS own the referenced identities (`V14-I4`). |

---

## Appendix A — Field coverage table

Every field in the record, with its declared type, cardinality, nullability, and the object that
declares it. This table is the evidence for AC-6.

| # | Field | Declared by | Type | Cardinality | Nullable | Section |
|---|---|---|---|---|---|---|
| 1 | `schema_version` | Record | string `MAJOR.MINOR.PATCH` | 1..1 | No | §4.2 |
| 2 | `student_id` | Record | string (`CAP-USERID`) | 1..1 | No | §4.2 |
| 3 | `academic_period` | Record | string, opaque | 1..1 | No | §4.2 |
| 4 | `educational_level` | Record | string, enum of 3 | 1..1 | No | §4.2 |
| 5 | `record_state` | Record | string, enum `Finalized` | 1..1 | No | §4.2 |
| 6 | `GoverningRuleSetID` | Record | string, opaque | 1..1 | No | §4.2 |
| 7 | `parent_transaction_id` | Record | string, opaque | 0..1 | No | §4.2 |
| 8 | `academic_history` | Record | array of entry | 1..N | No | §4.2 |
| 9 | `cumulative_weighted_gpa` | Record | number | 0..1 | No | §4.2 |
| 10 | `total_credits` | Record | number | 0..1 | No | §4.2 |
| 11 | `finalized_at` | Record | string, ISO 8601 | 1..1 | No | §4.2 |
| 12 | `authorized_by` | Record | string (`CAP-USERID`) | 1..1 | No | §4.2 |
| 13 | `canonical_field_list` | Record | array of string | 13..13 | No | §4.2 |
| 14 | `assessment_id` | `academic_history` entry | string, opaque | 1..1 | No | §4.4.1 |
| 15 | `assessment_type` | `academic_history` entry | string | 1..1 | No | §4.4.1 |
| 16 | `section_id` | `academic_history` entry | string, opaque | 1..1 | No | §4.4.1 |
| 17 | `grade_raw` | `academic_history` entry | number | 1..1 | No | §4.4.1 |
| 18 | `grade_final` | `academic_history` entry | string | 1..1 | No | §4.4.1 |
| 19 | `max_score` | `academic_history` entry | number | 1..1 | No | §4.4.1 |
| 20 | `weight` | `academic_history` entry | number | 0..1 | No | §4.4.1 |
| 21 | `achievement_level` | `academic_history` entry | string | 0..1 | No | §4.4.1 |
| 22 | `submission_timestamp` | `academic_history` entry | string, ISO 8601 | 1..1 | No | §4.4.1 |
| 23 | `enrollment_detail` | `academic_history` entry | `EnrollmentDetail` object | 0..1 | No | §4.4.1 |
| 24 | `enrollment_id` | `EnrollmentDetail` | string, opaque | 1..1 | No | §4.4.2 |
| 25 | `course_id` | `EnrollmentDetail` | string, opaque | 1..1 | No | §4.4.2 |
| 26 | `enrollment_date` | `EnrollmentDetail` | string, ISO 8601 | 1..1 | No | §4.4.2 |
| 27 | `credits_earned` | `EnrollmentDetail` | number | 0..1 | No | §4.4.2 |

Twenty-seven fields: thirteen on the record, ten on the `academic_history` entry, four on
`EnrollmentDetail`. No field name appears twice, and no field permits null.

## Appendix B — Timestamp inventory

Every timestamp field in the record, with its declared type. This table is the evidence for AC-7.

| # | Field | Declared by | Type | Format |
|---|---|---|---|---|
| 1 | `finalized_at` | Record | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |
| 2 | `submission_timestamp` | `academic_history` entry | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |
| 3 | `enrollment_date` | `EnrollmentDetail` | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |

Three timestamp fields. Every one is a string in ISO 8601 extended form with a UTC designator. No
field is declared as a number, and no epoch-based representation appears in this contract.

---

*This document is ready for independent review.*
