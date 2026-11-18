---
id: CAP-STATUSENUMS
version: 1.1
status: In_Review
title: Status Enumeration Capability
created: 2026-11-13T00:00:00Z
updated: 2026-11-18T06:55:06Z
---

# CAP-STATUSENUMS: Status Enumeration Capability

## Description

Normative status vocabulary for the Blockchain-Enabled LMS: the valid status values for
academic period records, grade records, appeal records, student-period records, enrollment
records, and level-completion records. This artifact is the LMS's adopted vocabulary, filed in
the shared library; its values are project-specific. Adopting projects copy or specialize it.

## Normative Definition

The following status values are standardized for this project. The vocabulary is identical to
the interim table in `SRS_LMS_v1.0.md` Section 9.1 (v1.1), which is the interim authority until
this artifact is promoted to `Approved`; promotion requires the SRS Section 11 Change Request
that reduces Section 9.1 to a normative reference to this artifact. Until that Change Request
lands, where the two disagree, the SRS governs.

| Entity | Status values |
|---|---|
| Academic period | `Draft`, `Active`, `Closed` |
| Grade record | `Proposed`, `Finalized` |
| Appeal record | `UnderReview`, `Approved`, `Rejected` |
| Student-period record | `Finalized` |
| Enrollment | `Requested`, `Enrolled`, `Completed`, `Refused`, `Withdrawn` |
| Level-completion record | `InProgress`, `Completed` |

## Status Transition Rules

Identical to the normative tables in `SRS_LMS_v1.0.md` Section 2.9 (Approved):

### Academic period

| From | Event | To |
|---|---|---|
| — | Period defined | `Draft` |
| `Draft` | Period opened for enrollment and assessment | `Active` |
| `Active` | Period closed | `Closed` |

`Closed` is terminal. A record may not be created or modified in a period that is not `Active`
(Workflow W-1).

### Grade record

| From | Event | To |
|---|---|---|
| — | Assessment results submitted and a grade computed | `Proposed` |
| `Proposed` | Approved and recorded | `Finalized` |
| — | An appeal is approved against a finalized grade — a new grade record is appended, linked by `parent_transaction_id` | `Finalized` |

`Finalized` is **terminal**. No field of a finalized grade record is ever written. A correction
does not move a grade record to another state — it appends a new one (Workflow W-3).

### Appeal record

| From | Event | To |
|---|---|---|
| — | Appeal raised against a finalized grade | `UnderReview` |
| `UnderReview` | The last authority in the ECS-supplied approval chain rejects the appeal | `Rejected` |
| `UnderReview` | The last authority in the ECS-supplied approval chain approves the appeal | `Approved` |

`Rejected` and `Approved` are terminal. On `Approved`, a successor grade record is appended
(Workflow W-3); the appealed grade record is unchanged.

### Student-period record

| From | Event | To |
|---|---|---|
| — | Period closes and the record is assembled | `Finalized` |
| — | An approved appeal amends an already-finalized aggregate — a new record is created | `Finalized` |

`Finalized` is **terminal**. A later student-period record for the same student and period — for
example after an approved appeal — does not alter this one. It carries `parent_transaction_id`
pointing at the record it supersedes. There is no `Open` state: a student-period record is
created only when it is final, and it carries the rule set identifier that governed the period.

### Enrollment

| From | Event | To |
|---|---|---|
| — | Enrollment requested | `Requested` |
| `Requested` | Prerequisites and capacity constraints satisfied | `Enrolled` |
| `Requested` | A constraint is not satisfied | `Refused` |
| `Enrolled` | All requirements of the enrolled course are met | `Completed` |
| `Enrolled` | Withdrawn by the student or an administrator | `Withdrawn` |

`Refused` and `Withdrawn` are distinct terminal states: a refusal records that the system
declined the request, a withdrawal records that the student or an administrator ended it. A
refused request may be submitted again.

### Level-completion record

| From | Event | To |
|---|---|---|
| — | Student begins study at a level | `InProgress` |
| `InProgress` | All requirements for the level are met | `Completed` |

`Completed` is terminal and triggers Workflow W-4.

## Constraints

- Status values must be drawn from the normative table above.
- Status transitions must follow the tables above (identical to `SRS_LMS_v1.0.md` Section 2.9).
- ECS determines the rules in force for an educational level and academic period
  (SRS Section 3.1); the ECS-supplied approval chain governs appeal approval
  (SRS Sections 2.4 and 2.9).
- No field of a finalized grade record is ever written. A correction appends a new record and
  expresses the relationship by linkage; it does not amend what it corrects.
- A finalized record's state is terminal and is never written to; supersession is expressed
  only by a successor carrying `parent_transaction_id`.
