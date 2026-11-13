---
id: SCHEMA-VERSION-CONSTRAINT
version: 1.0
status: Draft
---

# CAP-SCHEMAVERSIONCONSTRAINT: Schema Version Constraint Capability

## Description

Schema version validation rule for the `final_academic_record` payload. Defines the required format and validation constraints for the `schema_version` field.

## Normative Definition

The `schema_version` field is a mandatory top-level field in the `final_academic_record` payload with the following constraints:

- **Format:** `MAJOR.MINOR.PATCH` (e.g., `1.0.0`, `2.3.1`)
- **Requirement:** Must be present as a top-level, mandatory field
- **Validation:** Attempting to submit a record with an unsupported `schema_version` results in a controlled rejection by the LGS validator
- **Backward compatibility:** Records with earlier `schema_version` may be accepted per domain-specific rules, but the version must be declared
- **Forward compatibility:** New `schema_version` values must be explicitly approved through the approval chain before records using them are accepted

## Status Vocabulary

Entity | Status Values
--- | ---
SchemaVersionConstraint | `Draft`, `Approved`, `Superseded`

## Relations

- **Used by:** LGS validator, all seven domains (schema version declaration)
- **Related to:** CAP-USERID (versioned records), CAP-TIMESTAMPFORMAT (version timestamps), CAP-STATUSENUMS (version-status linkage), task-LMS-CONTRACT-001-noncode.md (contract integrity principle 3)

## Validation Rules

1. The `final_academic_record` payload must contain a top-level `schema_version` string field
2. The `schema_version` string must match the pattern `MAJOR.MINOR.PATCH` where MAJOR, MINOR, and PATCH are non-negative integers
3. Attempting to submit a record with an unsupported or malformed `schema_version` results in a controlled rejection by the LGS validator
4. The `schema_version` must be declared when defining a new record type or modifying an existing one
5. Version changes must follow the approval chain: proposal → review → approval → commitment to the proof sequence

## Constraints

- The `schema_version` field is **non-negotiable**: the contract requires a top-level mandatory `schema_version: [MAJOR.MINOR.PATCH]` field (Principle 3 of Expected Behavior)
- Records submitted without a `schema_version` field are immediately rejected
- Records submitted with a `schema_version` that does not match `MAJOR.MINOR.PATCH` pattern are immediately rejected
- Version changes require explicit approval through the approval chain and are recorded in the proof sequence