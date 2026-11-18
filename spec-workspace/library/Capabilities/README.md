# Capabilities

Reusable capability specifications - the normative definitions of concepts shared across
projects.

A capability specification answers: what does this concept mean, what are its fields and
invariants, and what may a consumer rely on. It does not say how it is implemented.

## Required shape

Every capability artifact follows the same contract as any other specification:

* YAML frontmatter with a stable `id`, a `version`, a `status`, and a `created` / `updated` pair.
* `status` drawn from `Draft -> In_Review -> Approved -> Superseded`.
* Evidence of review recorded in the work ledger before it is marked `Approved`.

## Referencing a capability

A task specification names a capability in its "Dependencies and Sources" section and may rely on
it normatively. The reference must resolve to an artifact in this directory - a bare name with no
artifact is a missing relationship, not an implicit convention.

## Status

**Populated; five of five Approved (2026-11-18).** All five capabilities are `Approved`:
`CAP-CANONICAL-FORM` (v1.0; `WORK-175`), `CAP-USERID` (v1.1; `WORK-175`),
`CAP-TIMESTAMPFORMAT` (v1.1; `WORK-175`), `CAP-SCHEMAVERSIONCONSTRAINT` (v1.1; `WORK-175`), and
`CAP-STATUSENUMS` (v1.1; `WORK-176` - promoted at the same Gate-approved change that retired the
`SRS_LMS_v1.0.md` Section 9.1 interim table, now a normative reference to this capability).
Approvals were recorded as ledger Decisions per the framework approval hierarchy. See
`spec-workspace/library/README.md` and ledger `WORK-020` (authoring), `WORK-175`/`WORK-176`
(promotions).
