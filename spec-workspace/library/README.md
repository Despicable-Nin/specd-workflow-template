# Library

Reusable, technology-agnostic artifacts. A library artifact may **not** reference implementation
details, frameworks, or products - it states a capability or a constraint, and the technology is
chosen later.

| Subtree | Purpose |
|---|---|
| `Engineering/` | Cross-cutting engineering practices, standards, and constraints. |
| `Capabilities/` | Reusable capability specifications - the normative definitions of shared concepts. |

## Why Capabilities exist

Task specifications reference capabilities by name in their "Dependencies and Sources" section and
treat them as normative. If a capability has no artifact, the task that depends on it cannot be
independently verified - there is nothing to check the task against.

The first live project exposed this gap, and the gap is now closed: `WORK-LMS-CONTRACT-001`
depends on four capabilities, and all five (those four plus `CAP-CANONICAL-FORM`, on which the
proof guarantee depends) have defining artifacts under `Capabilities/`:

| Capability | Referenced as | Status |
|---|---|---|
| `CAP-USERID` | Standard user identity | Exists (`In_Review`) |
| `CAP-TIMESTAMPFORMAT` | ISO 8601 | Exists (`In_Review`) |
| `CAP-STATUSENUMS` | Shared status enumerations | Exists (`In_Review`) |
| `CAP-SCHEMAVERSIONCONSTRAINT` | `MAJOR.MINOR.PATCH` version constraint | Exists (`In_Review`) |
| `CAP-CANONICAL-FORM` | Canonical form and digest constraint | Exists (`In_Review`) |

## Status

**Populated.** Each capability carries a stable ID, a version, and a `status` from the
`Draft -> In_Review -> Approved -> Superseded` lifecycle. Approval requires independent review
and a recorded ledger Decision per artifact before it is marked `Approved`; promotion evidence
lives in the work ledger. `CAP-STATUSENUMS` promotion is additionally gated on the SRS Section 11
Change Request that reduces `SRS_LMS_v1.0.md` Section 9.1 to a normative reference to the
capability.

See ledger `WORK-020` (authoring).
