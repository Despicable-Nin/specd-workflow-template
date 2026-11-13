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

The first live project exposed this gap. `WORK-LMS-CONTRACT-001` depends on four capabilities
that have **no defining artifact anywhere in the repository** (ledger `WORK-020`):

| Capability | Referenced as | Status |
|---|---|---|
| `UserID` | Standard user identity | **No artifact** |
| `TimestampFormat` | ISO 8601 | **No artifact** |
| `StatusEnums` | Shared status enumerations | **No artifact** |
| `SchemaVersionConstraint` | `MAJOR.MINOR.PATCH` version constraint | **No artifact** |

## Status

**Empty by design, pending authoring.** Authoring these four is a specification task, not a
reconciliation action, and the content is normative - it is deliberately not fabricated here.
Each capability, when authored, needs a stable ID, a version, a `status` from the
`Draft -> In_Review -> Approved -> Superseded` lifecycle, and a reference from the task
specification that depends on it.

See ledger `WORK-020` and `WORK-030`.
