---
id: SCHEMA-LMS-FAR-v1.0
version: 1.0.0
status: Approved
title: final_academic_record - Canonical Data Contract
project: blockchain-enabled-lms
rendered_from: ../tasks/task-LMS-CONTRACT-001-noncode.md
rendered_from_id: WORK-LMS-CONTRACT-001
rendered_from_version: 1.5
created: 2026-11-13T02:00:00Z
updated: 2026-11-16T09:26:06Z
---

# `final_academic_record` — Canonical Data Contract

> **Provenance and authority.** The authoritative definition of this contract is
> `tasks/task-LMS-CONTRACT-001-noncode.md` (task ID `WORK-LMS-CONTRACT-001`, **version 1.4**).
> This file is its **normative rendering**. Where this file and the task specification disagree,
> **the task specification wins** and this file is the defect. This file must not introduce a
> requirement the task specification does not authorise (project `AGENTS.md` §3).

## 1. Scope

**In scope** — mirrors task specification §2:

- Every field of the record, with its data type, cardinality and nullability.
- The two encapsulated objects — the `academic_history` entry and `EnrollmentDetail` — and their
  field sets.
- The ordered canonical field list, and the record that no field is excluded from it.
- The finalization-time and authorizing-authority fields that SRS §2.8 requires inside the digest.
- The record's state field, drawn from the SRS §9.1 vocabulary.
- The `schema_version` rule and the compatibility meaning of a MAJOR, MINOR and PATCH change.
- `GoverningRuleSetID` — type, cardinality, and ECS as supplier.
- `parent_transaction_id` linkage on every superseding record.
- Exactly one record encoding.

**Out of scope** — mirrors task specification §3. Notably: implementation of any kind; ECS rule
content, including value domains for academic judgement; the canonical-form reduction rules, field
ordering rule and digest algorithm, which `CAP-CANONICAL-FORM` owns; the canonical-form version and
digest algorithm identifier, which the proof commits and the verification surface publishes
(SRS §2.8, §3.7) and which are **not** fields of this record; resolution of the parent's open
questions Q-1 and Q-2; runtime validation; any API, user-interface, transport or persistence
definition; and every other record type — `GradeRecord`, `Enrollment`,
`LevelCompletionRecord` and `GradeAppealRecord` are separately owned and separately specified.

## 2. The record is the canonical payload

**There is no envelope.** The record is one flat object, and that object is the canonical payload.

Three SRS statements force this. SRS §2.8:222 reduces *"the canonical payload"* to its canonical
form and computes the digest over it. SRS §3.7:437-440 has the verification surface return *"the
canonical **payload**"* together with the canonical-form version, the digest algorithm identifier
and the canonical field list. SRS §4.2 S-2:484 requires the digest to *"recompute from the canonical
payload published on the verification surface."*

A digested field that is not published cannot be verified; a published field that is not digested is
unprotected. The digested set and the published set must therefore be the same set. A wrapper object
would break that identity in one direction or the other, so this contract declares none.

**Identity.** SRS §2.8:218-219 defines the proof unit as the payload *"for **one student, for one
academic period**"*. Identity is `student_id` together with `academic_period`; a superseding record
for the same student and period is distinguished by its `parent_transaction_id` and by its content.
No record identifier is declared: SRS §2.8:222-224 commits the transaction identity alongside the
digest, and SRS Q-2 leaves that identity's representation open.

## 3. The complete schema

The block below is **one complete schema document**. Every `$ref` resolves within it. It is a
**structural** rendering: it encodes field names, types, enumerations, required-ness and closed
field sets. Presence rules R-1, R-3 and R-4 are encoded — as a single-value enumeration, a minimum
array length, and required-ness respectively. **R-2 is the only presence rule not encoded**, because
it is a condition on when a record may be created rather than on its shape; it is checked when the
record is assembled (GRA-Service, SRS §2.7 step 2) and at the proof commit boundary (LGS, SRS §2.7
step 4).

```json
{
  "title": "final_academic_record",
  "description": "The canonical payload for one student and one academic period. There is no envelope: every field below is digested and published.",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Mandatory contract version, MAJOR.MINOR.PATCH, per CAP-SCHEMAVERSIONCONSTRAINT. This is the record type's version, not the canonical-form version."
    },
    "student_id": {
      "type": "string",
      "description": "CAP-USERID of the student this record attests for. Part of the record's identity."
    },
    "academic_period": {
      "type": "string",
      "description": "Opaque, ECS-owned academic period identity (SRS 3.4). Part of the record's identity. No internal format is declared."
    },
    "educational_level": {
      "type": "string",
      "enum": ["Primary School", "Secondary School", "College"],
      "description": "The educational level the governing rules were selected for. The three values are those SRS 1.3 places in scope; the rules for each level are ECS content (SRS 3.1)."
    },
    "record_state": {
      "type": "string",
      "enum": ["Finalized"],
      "description": "The SRS 9.1 student-period state. Finalized is the only value; there is no Open state and no Superseded state (SRS 2.9)."
    },
    "GoverningRuleSetID": {
      "type": "string",
      "description": "Opaque rule set identifier supplied by ECS and recorded by GRA-Service (SRS 2.7 step 1). No internal format is declared (SRS Q-1 is open)."
    },
    "parent_transaction_id": {
      "type": "string",
      "description": "The transaction identity under which the superseded student-period record's proof was committed. Absent on an original record; present exactly when this record supersedes one (presence rule R-2)."
    },
    "academic_history": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/definitions/AcademicHistoryEntry"},
      "description": "At least one finalized assessed outcome (presence rule R-3)."
    },
    "cumulative_weighted_gpa": {
      "type": "number",
      "description": "Present when the governing rule set computes it. Whether an educational level uses it is ECS rule content (SRS 3.1); this contract declares no level condition."
    },
    "total_credits": {
      "type": "number",
      "description": "Present when the governing rule set computes it. Whether an educational level uses it is ECS rule content (SRS 3.1); this contract declares no level condition."
    },
    "finalized_at": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
      "description": "ISO 8601 UTC timestamp of finalization, per CAP-TIMESTAMPFORMAT. Inside the digest (SRS 2.8)."
    },
    "authorized_by": {
      "type": "string",
      "description": "CAP-USERID of the authority that authorized finalization. Inside the digest (SRS 2.8, SRS 5 Traceability of authority)."
    },
    "canonical_field_list": {
      "type": "array",
      "minItems": 13,
      "maxItems": 13,
      "items": {"type": "string"},
      "description": "The ordered declaration in Section 5. Its value must equal that list; a mismatch is a rejection."
    }
  },
  "required": [
    "schema_version",
    "student_id",
    "academic_period",
    "educational_level",
    "record_state",
    "GoverningRuleSetID",
    "academic_history",
    "finalized_at",
    "authorized_by",
    "canonical_field_list"
  ],
  "definitions": {
    "AcademicHistoryEntry": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "assessment_id": {
          "type": "string",
          "description": "Opaque identifier, unique within the operational record store."
        },
        "assessment_type": {
          "type": "string",
          "description": "The kind of assessment. The set of kinds is ECS rule content (SRS 3.1); not constrained here."
        },
        "section_id": {
          "type": "string",
          "description": "Opaque identifier of the section in which the assessment was taken. Declared on the entry so that an entry without enrollment_detail still identifies its section."
        },
        "grade_raw": {
          "type": "number",
          "description": "The score before finalization."
        },
        "grade_final": {
          "type": "string",
          "description": "The finalized grade. Mandatory: the record is assembled only from finalized grades (SRS 2.7 step 2, 2.9)."
        },
        "max_score": {
          "type": "number",
          "description": "The maximum attainable score."
        },
        "weight": {
          "type": "number",
          "description": "The weighting applied in the aggregate. Absent where the level does not use weighting."
        },
        "achievement_level": {
          "type": "string",
          "description": "The band awarded. The set of bands is ECS rule content (SRS 3.1); not constrained here."
        },
        "submission_timestamp": {
          "type": "string",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
          "description": "ISO 8601 UTC timestamp of submission, per CAP-TIMESTAMPFORMAT."
        },
        "enrollment_detail": {"$ref": "#/definitions/EnrollmentDetail"}
      },
      "required": [
        "assessment_id",
        "assessment_type",
        "section_id",
        "grade_raw",
        "grade_final",
        "max_score",
        "submission_timestamp"
      ]
    },
    "EnrollmentDetail": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "enrollment_id": {
          "type": "string",
          "description": "Opaque identifier."
        },
        "course_id": {
          "type": "string",
          "description": "Opaque identifier."
        },
        "enrollment_date": {
          "type": "string",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
          "description": "ISO 8601 UTC timestamp of enrollment, per CAP-TIMESTAMPFORMAT."
        },
        "credits_earned": {
          "type": "number",
          "description": "Credits applied toward the academic period."
        }
      },
      "required": ["enrollment_id", "course_id", "enrollment_date"]
    }
  }
}
```

`student_id` and `authorized_by` are typed by `CAP-USERID`. The schema does not restate that
capability's format constraints — alphanumeric, globally unique, stable — which are enforced by the
capability rather than by this structural rendering.

Three things this schema deliberately does **not** contain, each for a stated reason:

* **An envelope.** There is none (§2). `additionalProperties: false` at every level means a payload
  carrying any field not declared here — including a storage identifier or a creation stamp — fails
  validation rather than passing unverified.
* **`GradeAssessment`.** It was removed in v1.4. Its `assessment_record_id` duplicated the entry's
  `assessment_id` and its `computed_grade` duplicated `grade_final`; its `section_id` and
  `submission_timestamp` are now declared on the entry, and its `governing_rule_set_id` duplicated
  the record-level `GoverningRuleSetID`.
* **`appeal_record`, `appeal_id` and `change_status`.** `GradeAppealRecord` is a GRA-Service-owned
  operational record (SRS §3.1:359), not a member of the student-period record. The change flag
  belongs to the appended grade record (SRS §2.4 step 5), and supersession of a student-period
  record is expressed only by `parent_transaction_id` (SRS §2.9:318-321).

## 4. Presence rules

Normative, from task specification §4.3.

| Rule | Statement | Authority |
|---|---|---|
| R-1 | `record_state` is `Finalized` and no other value. There is no `Open` state and no `Superseded` state. | SRS §2.9, §9.1 |
| R-2 | `parent_transaction_id` is present exactly when this record supersedes an earlier student-period record for the same student and period, and absent on an original record. | SRS §2.9 |
| R-3 | `academic_history` carries at least one entry. | SRS §2.7 |
| R-4 | `finalized_at` and `authorized_by` are present on every record, including a superseding one. | SRS §2.8, §5 |

R-1, R-3 and R-4 are encoded in §3: R-1 as a single-value enumeration, R-3 as a minimum array
length, and R-4 as required-ness. **R-2 is the only presence rule not encoded**, because it is a
condition on when a record may be created rather than on its shape. R-2 is checked when the record
is assembled (GRA-Service, SRS §2.7 step 2) and at the proof commit boundary (LGS, SRS §2.7 step 4).

**No presence rule is declared for `cumulative_weighted_gpa` or `total_credits`.** SRS §1.3
describes College's emphasis as *"Credit accumulation, weighted grade-point average"*, but an
emphasis is not a presence rule. Both are optional; their use is ECS rule content (SRS §3.1).

**Cardinality and nullability are separate declarations.** Cardinality states whether a field is
present; nullability states whether a present field may carry null. **No field in this contract
permits null.** A field that does not apply is absent, never null.

## 5. Canonical field list

The digest covers exactly these fields, **in this order**. `CAP-CANONICAL-FORM` property 3 makes the
declared order the canonical order and applies it recursively to nested structures; the field orders
declared in §3 are the nested orders.

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

This satisfies every element SRS §2.8 requires the digest to cover: identity (2, 3), content
(4, 5, 7–10), the rule set identifier (6), the time of finalization (11), and the authorizing
authority (12). Field 13 is the declaration itself, which SRS §8.1 places inside the digest.
Field 1 is the contract version that `CAP-SCHEMAVERSIONCONSTRAINT` requires to be a mandatory
top-level field; SRS §2.8 does not name it as a digest element, but a declared field of the record
is inside the digest by declaration.

**The list contains its own name.** This is intentional and not circular: the value of
`canonical_field_list` is a finite array of field names, and that array is one of the values the
digest covers. A verifier reads the list from the payload, checks that it equals the list declared
here, and reduces accordingly. Altering the array would change the digest, so the declaration is
tamper-evident rather than merely asserted. The schema fixes the array at 13 items, so it cannot be
shortened or extended.

## 6. Exclusions from the canonical form

`CAP-CANONICAL-FORM` property 2 requires an exclusion to be **recorded**, not implied. This record
type declares **no exclusion**: every field it declares is in the canonical field list, and it has
no field that is not in the list.

The five categories property 2 excludes by default are recorded as considered and absent:

| Default-excluded category | Applies? | Reason |
|---|---|---|
| Session identifiers | No | The record type declares no session field. |
| Last-read / access markers | No | The record type declares no access marker. |
| Transport and envelope metadata | No | The record type declares no envelope and no transport field (§2). |
| Storage and physical locators | No | The record type declares no storage locator. |
| Cache and materialization state | No | The record type declares no materialization field. |

`finalized_at` is **not** excluded. `CAP-CANONICAL-FORM` property 2 states the distinction:
*"A field that records when a record was finalized is not volatile — it is a property of the record
— and is included."*

## 7. Encoding

The record is encoded as JSON. No second encoding is named anywhere in this contract.

The **canonical form's** encoding is not this contract's to state. `CAP-CANONICAL-FORM` property 4
records it as the UTF-8 encoding of a canonical JSON text: declared fields only, in declared order,
no insignificant whitespace, no duplicate member names, shortest numeric form. The two statements
are consistent — the record is JSON, its reduction is canonical JSON — but they are separate
obligations with separate owners.

Timestamps are strings in ISO 8601 extended form `YYYY-MM-DDTHH:MM:SSZ`, per `CAP-TIMESTAMPFORMAT`,
constrained in §3 by the exact pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`. A general
date-time format is deliberately not used: it admits fractional seconds and numeric offsets that
this contract excludes.

**Timestamp inventory** (evidence for AC-7):

| # | Field | Declared by | Type | Format |
|---|---|---|---|---|
| 1 | `finalized_at` | Record | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |
| 2 | `submission_timestamp` | `academic_history` entry | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |
| 3 | `enrollment_date` | `EnrollmentDetail` | string | ISO 8601 `YYYY-MM-DDTHH:MM:SSZ` |

Identifiers declared "opaque" carry no internal format constraint: `academic_period`,
`parent_transaction_id`, `GoverningRuleSetID`, `assessment_id`, `section_id`, `enrollment_id`,
`course_id`. SRS Q-1 and Q-2 remain open and govern the two identifiers they name.

## 8. Versioning and compatibility

`schema_version` is the **record type's** version, formatted `MAJOR.MINOR.PATCH`.
`CAP-SCHEMAVERSIONCONSTRAINT` fixes the format, the mandatory top-level presence and the controlled
rejection; it defines no per-segment semantics, so the three compatibility meanings below are
**this contract's own decision**:

- `MAJOR` — incompatible change; consumers must reject the payload.
- `MINOR` — backward-compatible addition; consumers may accept.
- `PATCH` — backward-compatible clarification with no structural effect.

**Rejection rule.** A payload whose `schema_version` is unsupported is **rejected**, not silently
coerced or partially applied. This is a validation obligation on the consuming surfaces, stated as a
rule; it is not a test this task constructs (task specification §3 item 7, §7).

`schema_version` is **not** the canonical-form version. `CAP-CANONICAL-FORM` property 5 defines the
canonical-form version as distinct, and SRS §2.8 has the proof commit it together with the digest
algorithm identifier. Neither is a field of this record.

This contract is at `1.0.0` and has never been approved, so no compatibility obligation exists yet.
The first approved version establishes the baseline.

## 9. Acceptance criteria

Each criterion mirrors the task specification §5 (v1.4) and is verified by document review. The task
specification is authoritative; this table restates it and must not diverge.

| ID | Criterion | Checked against | Evidence |
|---|---|---|---|
| **AC-1** | `parent_transaction_id` is declared on every superseding record, the superseded record's fields are never rewritten, and supersession is expressed only by that link — no `Superseded` state and no second change-classification field. | SRS §2.9, §5 | Section 3 property row (correctly absent from `required` per R-2); presence rule R-2; Section 10. |
| **AC-2** | `GoverningRuleSetID` is string, 1..1, mandatory on every finalized student-period record, attributed to ECS as supplier and GRA-Service as recorder, and sufficient to reproduce the computation. | SRS §2.7 step 1, §3.1, §4.2 S-6, §5 | Section 3 property row and `required` list. |
| **AC-3** | Every field the digest covers is a field of the record, and the record is the unit the verification surface publishes — so a verifier holding the published record holds every digested field. | SRS §2.8, §3.7, §4.2 S-2 | Section 2; Section 5, whose 13 entries are exactly the 13 fields of Section 3; Section 6. |
| **AC-4** | `schema_version` is mandatory and top-level, `MAJOR.MINOR.PATCH`, with MAJOR/MINOR/PATCH meaning stated, an unsupported value rejected rather than coerced, and the field distinguished from the canonical-form version. | `CAP-SCHEMAVERSIONCONSTRAINT` (format, presence, rejection); SRS §2.8 property 5 (distinction only) | Section 3 property row and `required` list; Section 8. |
| **AC-5** | Exactly one record encoding is designated, no second alternative is named, and the canonical form's encoding is attributed to `CAP-CANONICAL-FORM`. | SRS §2.8 property 4; `CAP-CANONICAL-FORM` property 4 | Section 7; a full-text search for a competing format name returns nothing. |
| **AC-6** | Every field declares a type, cardinality and nullability; no field permits null; no field appears here that the task specification does not declare. | Task specification §4 and Appendix A; project `AGENTS.md` §3 | The `required` lists and enumerations in Section 3; the coverage table in the task specification Appendix A. |
| **AC-7** | Every timestamp is an ISO 8601 string `YYYY-MM-DDTHH:MM:SSZ`; no numeric epoch representation appears. | `CAP-TIMESTAMPFORMAT` | The timestamp inventory in Section 7 and the `pattern` constraints in Section 3. |
| **AC-8** | An ordered canonical field list is declared, no field is excluded, the five default-excluded categories are recorded as absent, and the declared order is stated to be the canonical order. | SRS §2.8, §8.1; `CAP-CANONICAL-FORM` properties 1, 2, 3 | Sections 5 and 6. |
| **AC-9** | An explicit finalization-time field and an explicit authorizing-authority field are declared, both mandatory, and both named in the canonical field list. | SRS §2.8, §8.1, §5 | Section 3 rows and `required` list; positions 11 and 12 of Section 5; presence rule R-4. |

## 10. Audit linkage

An appeal approved **after** period close appends a **new** student-period record; an appeal
approved **before** period close needs no successor, because the student-period record does not yet
exist and the corrected grade is simply part of the aggregate assembled at close (SRS §2.7). A
successor never alters the original's content. It carries `parent_transaction_id` — the transaction
identity under which the superseded record's proof was committed.

Per the parent specification (SRS §2.9), a finalized record's state is terminal and is never
written. A correction appends a successor linked by `parent_transaction_id`; supersession is
expressed by that link alone, because recording a `Superseded` state would write to a finalized
record and change the digest computed over it. The change flag lives on the appended **grade**
record (SRS §2.4 step 5) and the appeal record is GRA-Service-owned (SRS §3.1); neither is a member
of this record.

`parent_transaction_id` names one concept at every level — *the record this one supersedes* — and
resolves within that record type. On a student-period record it points at the superseded
student-period record; on a grade record it points at the superseded grade record (SRS §2.9).

The complete, approved state of a student's academic history is held in the operational record store
(SRS §3.6); the Ledger Service commits an immutable proof over the finalized student-period record
(SRS §2.7 step 4, §2.8).

## 11. Change history

| Date | Change | Source |
|---|---|---|
| 2026-11-13 | Rendered from `WORK-LMS-CONTRACT-001` v1.1. Added `schema_version` to the required set; added `GoverningRuleSetID`; added the `FINAL_ACADEMIC_RECORD` record type; recorded the `parent_transaction_id` / `change_status` audit-linkage rules; removed the claim to be the single source of truth. | Reconciliation, decision D-2 |
| 2026-11-13 | Defined previously "to be defined" items: `academic_history` entry field set; `EnrollmentDetail` and `GradeAssessment` structures; `AppealRecord` shape; `change_status` enumeration; `GoverningRuleSetID` identifier format. | Earlier pass — superseded, see 2026-11-16 below |
| 2026-11-16 | Re-rendered from v1.2. Acceptance criteria replaced with AC-1…AC-7. `change_status` clarified as a change classification distinct from record state. `enrollment_status` corrected to the SRS §9.1 vocabulary. All five timestamp fields converted to ISO 8601 strings. | Authoring pass |
| 2026-11-16 | Re-rendered from v1.3. Sections 5 and 6 added: the ordered canonical field list and the recorded exclusions. `finalized_at`, `authorized_by`, `record_state`, `student_id`, `canonical_field_list` and `appeal_record` added. All four object field sets mirrored the task specification. Invented identifier formats and invented academic policy removed. | First modelling pass |
| 2026-11-16 | **Re-rendered from v1.4 — the correction pass.** The **envelope is gone**: the record is one flat object, so every digested field is published and every published field is digested. `recordId`, `recordType`, `ownerId`, `createdAt` and `updatedAt` removed with it, and the exclusion table now records that no field is excluded. `GradeAssessment` deleted: `assessment_record_id` duplicated `assessment_id`, `computed_grade` duplicated `grade_final`, `governing_rule_set_id` duplicated `GoverningRuleSetID`; `section_id` and `submission_timestamp` moved onto the entry. `enrollment_status` and `section_id` removed from `EnrollmentDetail`. `appeal_record`, `appeal_id` and `change_status` removed: the appeal is a GRA-Service-owned record and the change flag belongs to the appended grade record. Presence rule R-5 removed as invented policy. `educational_level` given its three-value SRS §1.3 domain. `canonical_field_list` fixed at 13 items. One complete schema with resolving `$ref` values, `additionalProperties: false` at every level, and exact timestamp patterns replacing the general date-time format. | Correction pass, sixth review findings `C-01`, `C-02`, `W-01`…`W-14`, `I-01`…`I-03` |
| 2026-11-16 | **Re-rendered from v1.5 — editorial corrections only; no requirement changed.** Section 10 now distinguishes a pre-close appeal, which needs no successor (SRS §2.7), from a post-close one, and attributes the change flag to SRS §2.4 step 5 and the appeal record to §3.1 (`V14-W1`). Section 4 and AC-9 state that R-4 is encoded as required-ness and R-2 is the only unencoded presence rule, checked at GRA-Service assembly and the LGS commit (`V14-W2`, `V14-W5`). AC-1 no longer cites SRS §4.2 S-1, a grade-record criterion, and its evidence no longer points at a `required` list the field is correctly absent from (`V14-W3`, `V14-W6`). Section 8 attributes only format, presence and rejection to `CAP-SCHEMAVERSIONCONSTRAINT`, and states the three compatibility meanings as this contract's decision (`V14-W4`). `EnrollmentRecord` renamed to the SRS name `Enrollment` (`V14-I1`). Identifier-format enforcement delegated explicitly to `CAP-USERID` (`V14-I2`). The canonical-list mapping accounts for position 1 (`V14-I3`). AC-3 restores the verifier clause (`V14-I5`). |
