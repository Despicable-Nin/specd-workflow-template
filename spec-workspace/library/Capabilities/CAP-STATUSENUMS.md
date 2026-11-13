---
id: STATUS-ENUMS
version: 1.0
status: Draft
---

# CAP-STATUSENUMS: Status Enumeration Capability

## Description

Normative status vocabulary for the Blockchain-Enabled LMS. Defines the valid status values for academic period records, grade records, appeal records, enrollment records, and level-completion records.

## Normative Definition

The following status values are standardized for this project. These are defined inline in SRS_LMS_v1.0.md Section 9.1 and are also provided by this capability artifact for independent verification.

### Academic Period Statuses

Entity | Status Values
--- | ---
Academic period | `Draft`, `Active`, `Closed`

### Grade Record Statuses

Entity | Status Values
--- | ---
Grade record | `Proposed`, `Finalized`

### Appeal Record Statuses

Entity | Status Values
--- | ---
Appeal record | `UnderReview`, `Approved`, `Rejected`

### Student-Period Record Statuses

Entity | Status Values
--- | ---
Student-period record | `Finalized`

### Enrollment Statuses

Entity | Status Values
--- | ---
Enrollment | `Requested`, `Enrolled`, `Completed`, `Refused`, `Withdrawn`

### Level-Completion Record Statuses

Entity | Status Values
--- | ---
Level-completion record | `InProgress`, `Completed`

## Status Transition Rules

| From | Event | To |
|---|---|---|
| — | Period defined | `Draft` |
| `Draft` | Period opened for enrollment and assessment | `Active` |
| `Active` | Period closed | `Closed` |
| — | Assessment results submitted and a grade computed | `Proposed` |
| `Proposed` | Approved and recorded | `Finalized` |
| — | Appeal raised against a finalized grade | `UnderReview` |
| `UnderReview` | The last authority in the approval chain rejects the appeal | `Rejected` |
| `UnderReview` | The last authority in the approval chain approves the appeal | `Approved` |
| — | Student begins study at a level | `InProgress` |
| `InProgress` | All requirements for the level are met | `Completed` |

## Status Vocabulary Table (Normative)

| Entity | Valid Status Values |
|---|---|
| Academic period | `Draft`, `Active`, `Closed` |
| Grade record | `Proposed`, `Finalized` |
| Appeal record | `UnderReview`, `Approved`, `Rejected` |
| Student-period record | `Finalized` |
| Enrollment | `Requested`, `Enrolled`, `Completed`, `Refused`, `Withdrawn` |
| Level-completion record | `InProgress`, `Completed` |

## Constraints

- Status values must be drawn from the normative table above
- Status transitions must follow the table in Section "Status Transition Rules"
- The ECS (Educational Context Service) is the supreme authority that dictates how any given domain must behave
- No field of a finalized grade record is ever written. A correction appends a new record and expresses the relationship by linkage; it does not amend what it corrects
- A finalized record's state is terminal and is never written to; supersession is expressed only by a successor carrying `parent_transaction_id`