---
id: SCHEMA-LMS-FAR-v1.0
version: 1.0.0
status: Draft
title: final_academic_record - Canonical Data Contract
project: Blockchain-Enabled LMS
rendered_from: ../tasks/task-LMS-CONTRACT-001-noncode.md
rendered_from_id: WORK-LMS-CONTRACT-001
rendered_from_version: 1.1
created: 2026-11-13T02:00:00Z
updated: 2026-11-13T02:00:00Z
---

# `final_academic_record` - Canonical Data Contract

> **Provenance and authority.** The authoritative definition of this contract is
> `tasks/task-LMS-CONTRACT-001-noncode.md` (task ID `WORK-LMS-CONTRACT-001`, version 1.1).
> This file is its **normative rendering**. Where this file and the task specification
> disagree, **the task specification wins** and this file is the defect. This file must not
> introduce requirements the task specification does not authorize.

## 1. Scope

**In scope** (per task specification Section 2):

- Mandatory fields, data types, and nullability for the core academic record.
- Structured encapsulation for service-specific payloads (e.g. `EnrollmentDetail`, `GradeAssessment`).
- Schema versioning rules, including backwards/forward compatibility procedures.
- The mandatory validation rules that must be applied by the Educational Context Service (ECS).
- Linkage of all changes to the originating transaction record.

**Out of scope** (per task specification Section 3): implementation of any microservice logic or
data transformation, and database migration scripts. This contract defines the target structure
only.

## 2. The three non-negotiable principles

These are quoted from task specification Section 4 and are the load-bearing constraints of this
contract.

1. **Immutability & Auditability.** All changes (including appeals/amendments) must create an
   appended, versioned audit record. That record **must** include a unique `parent_transaction_id`
   linking it back to the original record being amended, and a clear status flag documenting the
   nature of the change (e.g. `APPEAL_FIX`).
2. **Governed State.** The payload must reserve and utilize the `GoverningRuleSetID` field, which
   **must be populated by the ECS**, acting as the definitive proof of the validation rules used
   when the record was final.
3. **Contract Integrity.** The payload must contain a top-level, mandatory field
   `schema_version: [MAJOR.MINOR.PATCH]` to guarantee consistency across evolving services.

## 3. Record envelope

The generic record envelope established for the LMS system of record. `final_academic_record` is
one of its record types (Section 4).

```json
{
  "type": "object",
  "properties": {
    "recordId": {"type": "string", "description": "Unique immutable ID (UUIDv4)."},
    "ownerId": {"type": "string", "description": "ID of the user/system that created the record."},
    "createdAt": {"type": "integer", "description": "Unix timestamp (milliseconds) of creation."},
    "updatedAt": {"type": "integer", "description": "Unix timestamp (milliseconds) of last update."},
    "recordType": {"type": "string", "enum": ["USER", "COURSE", "ENROLLMENT", "FINAL_ACADEMIC_RECORD", "CUSTOM"], "description": "Categorization of the record."},
    "schema_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$", "description": "Mandatory contract version, MAJOR.MINOR.PATCH. Enforced by the LGS validator."},
    "GoverningRuleSetID": {"type": "string", "description": "Identity of the ECS rule set applied when the record was final. Populated by the ECS. Mandatory on a finalized academic record."},
    "payload": {"type": "object", "description": "The dynamic, record-specific data payload."}
  },
  "required": ["recordId", "ownerId", "createdAt", "recordType", "schema_version", "payload"]
}
```

**Change from the pre-reconciliation draft:** `schema_version` was added to `required`, in direct
fulfilment of task specification Section 4 principle 3 and acceptance criterion 4. The previous
`required` list omitted it, which contradicted the task specification.

## 4. `final_academic_record` payload

Type: `FINAL_ACADEMIC_RECORD`. Contains the student's full academic history for a specific academic
period (task specification Section 4).

### 4.1 Mandated by the task specification

| Field | Type | Nullable | Notes |
|---|---|---|---|
| `schema_version` | string `[MAJOR.MINOR.PATCH]` | No | Top-level; also envelope-level. |
| `GoverningRuleSetID` | string | No | Populated by the ECS. |
| `parent_transaction_id` | string | **Conditionally required** | Required on every appended audit record (appeal/amendment). Absent on the original record. Links to the original transaction record. |
| `change_status` | string | No on audit records | Nature of the change, e.g. `APPEAL_FIX`. |
| `academic_period` | string | No | The academic period this history covers. |
| `educational_level` | string | No | Governs which ECS ruleset applies. |
| `academic_history` | array | No | The student's achievements for the period. |
| `cumulative_weighted_gpa` | number | Conditional | College-level achievement. Value is produced by the version-specific formula linked by `GoverningRuleSetID`. |
| `total_credits` | number | Conditional | College-level achievement. |

### 4.2 Defined during task execution (WORK-028 resolution)

The following items have been defined and resolved per WORK-028 (approval Decision for WORK-LMS-CONTRACT-001 v1.1):

### 4.2.1 `academic_history` entry field set, data types, and nullability

Each entry in the `academic_history` array represents one assessed outcome for the student's academic period. The full field set is:

| Field | Type | Nullable | Notes |
|---|---|---|---|
| `assessment_id` | string | No | Unique ID for the assessment |
| `assessment_type` | string | No | e.g., `exam`, `project`, `practical` |
| `grade_raw` | number | No | The raw score/grade before finalization |
| `grade_final` | string | Conditional | Final grade letter or `null` if not yet finalized |
| `weight` | number | Yes | Weighting factor for GPA calculation; `null` for primary school |
| `max_score` | number | No | The maximum possible score for the assessment |
| `achievement_level` | string | Yes | e.g., `Distinction`, `Merit`, `Pass`; `null` for primary school |

**Minimum progression metrics for Primary School basic achievement:**
- `assessment_id`: UUIDv4 format, globally unique
- `assessment_type`: one of [`exam`, `project`, `participation`]
- `grade_raw`: integer between 0 and `max_score`
- `weight`: `null` (primary school has no weighting)
- `max_score`: positive integer, typically 100
- `achievement_level`: one of [`Pass`, `Merit`] for primary school

### 4.2.2 Structured contents of `EnrollmentDetail` encapsulated payload

The `EnrollmentDetail` payload encapsulates enrollment-specific data for service-specific payloads. It is structured as:

```json
{
  "enrollment_id": {"type": "string", "description": "UUIDv4 enrollment identity"},
  "course_id": {"type": "string", "description": "Course identification code"},
  "section_id": {"type": "string", "description": "Section identifier"},
  "student_id": {"type": "string", "description": "Link to user profile via IAM"},
  "enrollment_status": {"type": "string", "enum": ["Enrolled", "Completed", "Dropped", "Withdrawn"]},
  "enrollment_date": {"type": "integer", "description": "Unix timestamp (milliseconds) of enrollment"},
  "credits_earned": {"type": "number", "description": "Credits applied toward the academic period"},
  "grade_assessment": {"type": "string", "description": "Raw grade assessment before finalization"}
}
```

### 4.2.3 Structured contents of `GradeAssessment` encapsulated payload

The `GradeAssessment` payload encapsulates grade-specific data for service-specific payloads. It is structured as:

```json
{
  "assessment_record_id": {"type": "string", "description": "UUIDv4 assessment identity"},
  "student_id": {"type": "string", "description": "Link to user profile via IAM"},
  "section_id": {"type": "string", "description": "Section identification code"},
  "assessment_type": {"type": "string", "description": "e.g., `exam`, `project`, `practical`"},
  "raw_score": {"type": "number", "description": "The score before finalization"},
  "computed_grade": {"type": "string", "description": "Computed final grade"},
  "governing_rule_set_id": {"type": "string", "description": "Identifier from ECS per SRS 3.1"},
  "submission_timestamp": {"type": "integer", "description": "Unix timestamp (milliseconds) of submission"}
}
```

### 4.2.4 `AppealRecord` object shape beyond mandatory `parent_transaction_id` linkage

The `AppealRecord` object appended during the grade appeal/correction workflow is:

```json
{
  "parent_transaction_id": {"type": "string", "description": "UUIDv4 linking to the original record's recordId"},
  "change_status": {"type": "string", "enum": ["APPEAL_FIX", "GRADE_UP", "GRADE_DOWN", "REVIEW_REQUIRED"], "description": "Nature of the appeal change"},
  "appeal_id": {"type": "string", "description": "UUIDv4 identity of this appeal record"},
  "appeal_initiated_at": {"type": "integer", "description": "Unix timestamp (milliseconds) when appeal was initiated"},
  "appeal_authority": {"type": "string", "description": "ECS-supplied approval chain authority, per SRS 3.1"},
  "delta_computed_grade": {"type": "string", "description": "Proposed grade change delta, if applicable"},
  "supporting_rationale": {"type": "string", "description": "Free-text rationale for the appeal"},
  "status": {"type": "string", "enum": ["UnderReview", "Approved", "Rejected"], "description": "Current appeal status"}
}
```

### 4.2.5 Exact enumeration of `change_status` values

The `change_status` field on audit records uses the following enumeration:

| Value | Meaning |
|---|---|
| `APPEAL_FIX` | An appeal-approved correction to a finalized grade |
| `GRADE_UP` | A grade increase approved outside the appeal chain |
| `GRADE_DOWN` | A grade decrease approved outside the appeal chain |
| `REVIEW_REQUIRED` | A change that requires additional review before approval |

### 4.2.6 Concrete `GoverningRuleSetID` identifier format and its owning authority

The `GoverningRuleSetID` field format and authority are defined as follows:

- **Owning authority**: ECS (Educational Context Service), per SRS Section 3.1 — "ECS must be the supreme authority that dictates how any given domain (AMS, ESS, GRA) must behave"
- **Identifier format**: `ECS-<level>-<period>-<cycle>`, where:
  - `<level>` is the educational level key (e.g., `primary`, `secondary`, `college`)
  - `<period>` is the academic period identifier (e.g., `Fall2026`, `Spring2027`)
  - `<cycle>` is the cycle type key (e.g., `standard`, `accelerated`)
- **Example**: `ECS-college-Fall2026-standard`
- **Resolution**: ECS is the sole authority; GRA-Service does not determine or override the governing rule set
- **Citation**: SRS Section 3.1, Section 3.2, Section 3.3, and the ECS consumers section (AMS, ESS, FRAS, GRA-Service must consult ECS before any critical state change)

## 5. Audit linkage

Every appeal or amendment creates a **new, appended, versioned** record. It never alters the
original's content. The new record carries:

- `parent_transaction_id` - the `recordId` / transaction identity of the record being amended.
- `change_status` - the nature of the change.

Per the parent specification (SRS Section 2.9), a finalized record's state is terminal and is
never written to. A correction appends a successor that links back through `parent_transaction_id`;
supersession is expressed by that link alone, because recording a `Superseded` state would write to
a finalized record and change the digest computed over it.

The complete, approved state of the student's academic history is held in the operational
record store, which is the system of record (SRS Section 3.6); the Ledger Service (LGS) commits an
immutable proof over it (SRS Sections 2.7 and 3.6).

## 6. Versioning and compatibility

- `schema_version` is `MAJOR.MINOR.PATCH`.
- `MAJOR` - incompatible change; consumers must reject the payload.
- `MINOR` - backward-compatible addition; consumers may accept.
- `PATCH` - backward-compatible clarification.

**Rejection rule.** A payload whose `schema_version` is unsupported must be **rejected in a
controlled manner by the LGS validator**, not silently coerced or partially applied. This is
acceptance criterion 5 and requires an integration test at implementation time.

**Governance of the ruleset.** The formula that produces `cumulative_weighted_gpa` is selected by
the ECS for the current `EducationalLevel` and `AcademicPeriod` (SRS Sections 2.3 and 5). The
version-specific formula is identified by `GoverningRuleSetID`.

## 7. Acceptance criteria

Each criterion is independently verifiable, and maps to the task specification Section 5. Items marked "RESOLVED (WORK-028)" have been defined in Sections 4.2.1-4.2.6.

| # | Criterion | Verification |
|---|---|---|
| 1 | Basic Achievement (Primary School) fields populate correctly with minimum progression metrics. | Minimum progression metric values are defined and asserted for a primary-school sample (see Section 4.2.1). |
| 2 | Advanced Achievement (College) stores cumulative weighted GPA and total credits, calculated with the version-specific formula linked by `GoverningRuleSetID`. | GPA and credits asserted against a formula identified by the recorded `GoverningRuleSetID` (see Section 4.2.6 for identifier format; GPA formula is version-specific and ECS-governed). |
| 3 | The Grade Appeal/Correction workflow appends a full `AppealRecord` containing a mandatory `parent_transaction_id` matching the original record's ID. | Append produces a new record; original is unmodified; `parent_transaction_id` matches (see Section 4.2.4 for AppealRecord shape). |
| 4 | Schema validation enforces the presence and correct format of the top-level `schema_version` string. | Validator rejects a payload with a missing or malformed `schema_version` (enforced per envelope Section 2, pattern `^[0-9]+\\.[0-9]+\\.[0-9]+$`). |
| 5 | Submitting a record with an unsupported `schema_version` results in a controlled rejection by the LGS validator. | Integration test: unsupported version is rejected, not coerced (enforced by LGS validator per Section 6 rejection rule). |

## 8. Open questions

All carried-forward open questions have been resolved per WORK-028 (approval Decision for WORK-LMS-CONTRACT-001 v1.1):

1. **Official source/authority for populating the `GoverningRuleSetID` field**: RESOLVED — ECS per SRS 3.1 (see Section 4.2.6). No further action needed.
2. **Data format/standard for `parent_transaction_id`** across all participating services: RESOLVED — UUIDv4 format (see Sections 4.2.1, 4.2.4). No further action needed.

## 9. Change history

| Date | Change | Source |
|---|---|---|
| 2026-11-13 | Rendered from `WORK-LMS-CONTRACT-001` v1.1. Added `schema_version` to the required set; added `GoverningRuleSetID`; added the `FINAL_ACADEMIC_RECORD` record type; recorded the `parent_transaction_id` / `change_status` audit-linkage rules; removed the claim to be the single source of truth (the task specification holds that authority). | Reconciliation, decision D-2 |
| 2026-11-13 | Defined previously "To be defined" items: `academic_history` entry field set with minimum progression metrics for Primary School; `EnrollmentDetail` and `GradeAssessment` encapsulated payload structures; `AppealRecord` object shape beyond mandatory `parent_transaction_id` linkage; `change_status` enumeration; concrete `GoverningRuleSetID` identifier format with ECS as owning authority per SRS 3.1. | wf-implement, decision D-3 |
| 2026-11-13 | Resolved open questions: GoverningRuleSetID authority = ECS per SRS 3.1; `parent_transaction_id` format = UUIDv4. | wf-implement, decision D-3 |
