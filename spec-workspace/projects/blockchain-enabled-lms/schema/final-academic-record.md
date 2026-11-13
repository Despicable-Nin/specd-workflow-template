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

### 4.2 To be defined during task execution

The task specification's acceptance criteria imply, but do not fully enumerate, the following.
They are listed as **open contract items** rather than invented here:

- The full field set, data types, and nullability of `academic_history` entries.
- The minimum progression metrics for a Primary School basic achievement.
- The structured contents of `EnrollmentDetail` and `GradeAssessment` encapsulated payloads.
- The `AppealRecord` object shape, beyond its mandatory `parent_transaction_id` linkage.
- The exact enumeration of `change_status` values.
- The concrete `GoverningRuleSetID` identifier format and its owning authority.

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
the ECS for the current `EducationalLevel` and `AcademicPeriod` (SRS Sections 3.2 and 3.3). The
version-specific formula is identified by `GoverningRuleSetID`.

## 7. Acceptance criteria

Each criterion is independently verifiable, and maps to the task specification Section 5.

| # | Criterion | Verification |
|---|---|---|
| 1 | Basic Achievement (Primary School) fields populate correctly with minimum progression metrics. | Minimum progression metric values are defined and asserted for a primary-school sample. |
| 2 | Advanced Achievement (College) stores cumulative weighted GPA and total credits, calculated with the version-specific formula linked by `GoverningRuleSetID`. | GPA and credits asserted against a formula identified by the recorded `GoverningRuleSetID`. |
| 3 | The Grade Appeal/Correction workflow appends a full `AppealRecord` containing a mandatory `parent_transaction_id` matching the original record's ID. | Append produces a new record; original is unmodified; `parent_transaction_id` matches. |
| 4 | Schema validation enforces the presence and correct format of the top-level `schema_version` string. | Validator rejects a payload with a missing or malformed `schema_version`. |
| 5 | Submitting a record with an unsupported `schema_version` results in a controlled rejection by the LGS validator. | Integration test: unsupported version is rejected, not coerced. |

## 8. Open questions

Carried forward from the task specification; unresolved (see ledger `WORK-005`).

1. **Official source/authority for populating the `GoverningRuleSetID` field** (ECS vs GRA-Service).
2. **Data format/standard for `parent_transaction_id`** across all participating services.

## 9. Change history

| Date | Change | Source |
|---|---|---|
| 2026-11-13 | Rendered from `WORK-LMS-CONTRACT-001` v1.1. Added `schema_version` to the required set; added `GoverningRuleSetID`; added the `FINAL_ACADEMIC_RECORD` record type; recorded the `parent_transaction_id` / `change_status` audit-linkage rules; removed the claim to be the single source of truth (the task specification holds that authority). | Reconciliation, decision D-2 |
