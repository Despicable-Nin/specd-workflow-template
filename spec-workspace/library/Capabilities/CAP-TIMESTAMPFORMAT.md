---
id: CAP-TIMESTAMPFORMAT
version: 1.1
status: Approved
title: Timestamp Format Capability
created: 2026-11-13T00:00:00Z
updated: 2026-11-18T07:22:17Z
---

# CAP-TIMESTAMPFORMAT: Timestamp Format Capability

## Description

ISO 8601 format for temporal assertions: creation, modification and finalization timestamps
recorded by the consuming domains.

## Normative Definition

A timestamp conforms to the ISO 8601 extended format:

- **Date:** `YYYY-MM-DD` (e.g., `2026-11-13`)
- **Time:** `HH:MM:SS` (24-hour format, e.g., `14:30:00`)
- **Combined:** `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2026-11-13T14:30:00Z`) - the only permitted form;
  the UTC designator `Z` is mandatory.
- **Timezone:** UTC. All timestamps are UTC. No other offset is permitted.

## Relations

- **Used by:** all consuming domains (creation/modification timestamps, finalization timestamps)
- **Related to:** CAP-USERID (user creation timestamps), CAP-STATUSENUMS (status change timestamps)

## Constraints

- A timestamp must not be empty or null.
- A timestamp must conform to `YYYY-MM-DDTHH:MM:SSZ` exactly.
- Timestamps are stored in UTC in the operational record store.
