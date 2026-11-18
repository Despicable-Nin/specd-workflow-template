---
id: CAP-SCHEMAVERSIONCONSTRAINT
version: 1.1
status: In_Review
title: Schema Version Constraint Capability
created: 2026-11-13T00:00:00Z
updated: 2026-11-18T06:55:06Z
---

# CAP-SCHEMAVERSIONCONSTRAINT: Schema Version Constraint Capability

## Description

Constraint on the `schema_version` field of a record type that declares one. Defines the
format, presence, and the rejection rule for missing, malformed or unsupported values. It
defines no per-segment semantics: the meanings of MAJOR, MINOR and PATCH are the record
type's own contract decision, not this capability's.

## Normative Definition

A record type that declares a `schema_version` field conforms to:

- **Format:** `MAJOR.MINOR.PATCH`, where MAJOR, MINOR and PATCH are non-negative integers
  (e.g., `1.0.0`, `2.3.1`).
- **Presence:** the field is mandatory and top-level.
- **Rejection:** a record whose `schema_version` is missing, malformed, or unsupported by the
  consuming surface is rejected, never coerced. What counts as supported is defined by the
  consuming surface.

## Relations

- **Consumed by:** any record type whose contract adopts this constraint. The LMS
  `final_academic_record` contract (`WORK-LMS-CONTRACT-001`) is the reference adopter.

## Constraints

- `schema_version` is non-negotiable: a record type that adopts this constraint requires a
  mandatory top-level string field `schema_version` matching `MAJOR.MINOR.PATCH`.
- Records submitted without `schema_version` are rejected.
- Records submitted with a `schema_version` that does not match `MAJOR.MINOR.PATCH`, or that
  is not supported by the consuming surface, are rejected.
- This capability fixes the format, presence, and rejection rule only. It defines no
  per-segment semantics and gates no governance process.
