---
task_id: WORK-LMS-CONTRACT-001
version: 1.1
status: Draft
project: blockchain-enabled-lms
parent_spec: ../SRS_LMS_v1.0.md
parent_spec_id: SRS-LMS-v1.0
task_type: noncode
open_questions:
  - question: Official authority for GoverningRuleSetID field (ECS/GRA-Service) — Resolved: ECS per SRS 3.1
    severity: low
  - question: Data format/standard for parent_transaction_id across all participating services — Resolved: UUIDv4
    severity: low
created: 2026-11-11T12:00:00Z
updated: 2026-11-13T01:50:00Z
---
# Task: Define Canonical final_academic_record Data Contract (v1.1)

*> **Provenance.** The body below was restored from git blob `58f2453` on 2026-11-13; the working-tree copy had been reduced to frontmatter only. `status` remains `Draft` until a `wf-review` approval Decision is recorded in the work ledger (see WORK-009).

## 📜 1. Task Summary and Description
This task's objective is to define the standardized, canonical data contract (schema) for the `final_academic_record` payload. This schema serves as the definitive, auditable data input for the Ledger Service (LGS). It is the single source of truth governing the structure of all academic achievements committed to the blockchain.

## 🧱 2. In-Scope Activities (Revised)
*   Defining all mandatory fields, data types, and nullability for the core academic record.
*   Defining structured encapsulation for service-specific payloads (e.g., `EnrollmentDetail`, `GradeAssessment`).
*   Establishing rules for versioning the schema, including backwards/forward compatibility procedures.
*   Defining the schema field `GoverningRuleSetID`: its type (string), cardinality (1..1), and format citation (SRS Section 3.1: ECS must be the supreme authority governing validation rules for any given domain). Explicitly excluding the authoring of ECS rule content — the SRS Section 3.2 and 3.3 own the ECS rule-definition domain.
*   Mandating the linkage of all changes to the originating transaction record via `parent_transaction_id`.

## ❌ 3. Out-of-Scope Activities
*   Implementation of any microservice logic or data transformation (This task only defines the target structure).
*   Writing database migration scripts.

## ⚙️ 4. Expected Behavior (Revised)
The final payload must be a JSON/YAML object containing the student's full academic history for a specific academic period. Critically, it must satisfy three non-negotiable principles:
1.  **Immutability & Auditability:** All changes (including appeals/amendments) must create an appended, versioned audit record. This record *must* include: a unique `parent_transaction_id` that links it back to the original record being amended, and a clear status flag documenting the nature of the change (e.g., `APPEAL_FIX`).
2.  **Governed State:** The payload must reserve and utilize the `GoverningRuleSetID` field, which must be populated by the ECS, acting as the definitive proof of the validation rules used when the record was final.
3.  **Contract Integrity:** The payload must contain a top-level, mandatory field: `schema_version: [MAJOR.MINOR.PATCH]` to guarantee consistency across evolving services.

## 🎯 5. Acceptance Criteria (Measurable Tests - Revised)
The contract is accepted only when the schema satisfies the following advanced criteria:
*   [ ] Basic Achievement (Primary School) fields populate correctly with minimum progression metrics.
*   [ ] Advanced Achievement (College) calculates and stores cumulative weighted GPA and total credits using the version-specific formula linked by `GoverningRuleSetID`.
*   [ ] Grade Appeal/Correction workflow successfully appends a full `AppealRecord` object. Critically, the appeal MUST contain a mandatory `parent_transaction_id` matching the original record's ID.
*   [ ] Schema validation must successfully enforce the presence and correct formatting of the top-level `schema_version` string.
*   [ ] The contract requires integration tests confirming that attempting to submit a record with an unsupported `schema_version` results in a controlled rejection by the LGS validator.

## 🔗 6. Dependencies and Sources
*   **Parent Specification:** `SRS_LMS_v1.0.md` (Section 2).
*   **Required Tools:** ECS, GRA-Service, LGS.
*   **Adopted Capabilities:** Standard `UserID`, `TimestampFormat` (ISO 8601), `StatusEnums`, `SchemaVersionConstraint`.

## 🔕 7. Validation Requirements
The contract must be rigorously tested via a formal validation pipeline that validates the payload against the defined rules, ensuring all fields, version markers, and parental links are accounted for before LGS commitment.

---

*This document is ready for independent review.*