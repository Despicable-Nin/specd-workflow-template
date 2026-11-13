---
id: USER-ID
version: 1.0
status: Draft
---

# CAP-USERID: User Identification Capability

## Description

User identification mechanism for actor identification and profile holding. Defines the structure and constraints for user identifiers across all seven service domains (IAM, ECS, AMS, FRAS, ESS, GRA-Service, LGS).

## Normative Definition

A `UserID` consists of:

- **format:** Alphanumeric string with optional prefix indicating educational level
- **uniqueness:** Must be globally unique within the operational record store
- **stability:** Identifier must not change over the lifecycle of a record
- **scope:** Applicable across all service domains for actor identification

## Status Vocabulary

Entity | Status Values
--- | ---
UserID | `Draft`, `Approved`, `Superseded`

## Relations

- **Used by:** IAM (actor identification), all seven domains (actor reference)
- **Related to:** CAP-STATUSENUMS (user status values), CAP-TIMESTAMPFORMAT (creation/modification timestamps)

## Constraints

- UserID must not be empty or null
- UserID must conform to the format defined by the owning domain
- UserID must be resolvable to a profile via IAM operations