---
id: CAP-USERID
version: 1.1
status: In_Review
title: User Identification Capability
created: 2026-11-13T00:00:00Z
updated: 2026-11-18T06:55:06Z
---

# CAP-USERID: User Identification Capability

## Description

Actor identification for the consuming service domains. Defines the structure and constraints
for the identifiers that records carry for actors and authorities, across all domains that adopt
this capability.

## Normative Definition

A `UserID` consists of:

- **opaque:** an opaque, non-empty string. This capability constrains no internal format;
  any internal structure (prefixes, checksums, encodings) is a decision of the adopting
  project, not capability policy.
- **uniqueness:** globally unique within the operational record store.
- **stability:** the identifier must not change over the lifecycle of a record.
- **scope:** applicable across all consuming domains for actor identification.

## Relations

- **Used by:** all consuming domains (actor reference)
- **Related to:** CAP-TIMESTAMPFORMAT (creation/modification timestamps)

## Constraints

- `UserID` must not be empty or null.
- `UserID` must be resolvable to a profile via the adopting project's identity operations.
