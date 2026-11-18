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
| `CAP-USERID` | Standard user identity | **Approved** (2026-11-18) |
| `CAP-TIMESTAMPFORMAT` | ISO 8601 | **Approved** (2026-11-18) |
| `CAP-STATUSENUMS` | Shared status enumerations | **Approved** (2026-11-18) |
| `CAP-SCHEMAVERSIONCONSTRAINT` | `MAJOR.MINOR.PATCH` version constraint | **Approved** (2026-11-18) |
| `CAP-CANONICAL-FORM` | Canonical form and digest constraint | **Approved** (2026-11-18) |

## Status

**Populated; five of five Approved.** Each capability carries a stable ID, a version, and a
`status` from the `Draft -> In_Review -> Approved -> Superseded` lifecycle. Approval required
independent review and a recorded ledger Decision per artifact; the four promotions are recorded
in ledger `WORK-175` and the `CAP-STATUSENUMS` promotion in `WORK-176`. `SRS_LMS_v1.0.md`
Section 9.1 now carries a normative reference to `CAP-STATUSENUMS` (SRS v1.2, 2026-11-18); the
values are identical, and the capability governs the status vocabulary.

See ledger `WORK-020` (authoring).
