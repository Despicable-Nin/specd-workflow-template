---
id: TIMESTAMP-FORMAT
version: 1.0
status: Draft
---

# CAP-TIMESTAMPFORMAT: Timestamp Format Capability

## Description

ISO 8601 format for temporal assertions and finalization timestamps. Defines the structure and constraints for timestamp values across all seven service domains.

## Normative Definition

A timestamp must conform to the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) extended format:

- **Date:** `YYYY-MM-DD` (e.g., `2026-11-13`)
- **Time:** `HH:MM:SS` (24-hour format, e.g., `14:30:00`)
- **Combined:** `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2026-11-13T14:30:00Z`)
- **Timezone:** UTC (`Z`) is the default; other timezone offsets are permitted but must be explicitly declared

## Status Vocabulary

Entity | Status Values
--- | ---
TimestampFormat | `Draft`, `Approved`, `Superseded`

## Relations

- **Used by:** All seven domains (creation/modification timestamps, finalization timestamps)
- **Related to:** CAP-USERID (user creation timestamps), CAP-STATUSENUMS (status change timestamps), CAP-SCHEMAVERSIONCONSTRAINT (schema version timestamps)

## Constraints

- Timestamp must not be empty or null
- Timestamp must conform to ISO 8601 extended format
- Timestamps must be stored in UTC in the operational record store
- Timezone information must be explicitly declared when not UTC