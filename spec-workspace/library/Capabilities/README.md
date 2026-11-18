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

**Populated; promotions underway.** All five capabilities exist: `CAP-CANONICAL-FORM` (v1.0),
`CAP-USERID` (v1.1), `CAP-TIMESTAMPFORMAT` (v1.1), `CAP-STATUSENUMS` (v1.1),
`CAP-SCHEMAVERSIONCONSTRAINT` (v1.1). Each artifact follows the required shape above. Promotion
to `Approved` requires independent review plus a recorded ledger Decision per artifact, per the
framework approval hierarchy. `CAP-STATUSENUMS` promotion is additionally gated on the SRS
Section 11 Change Request that reduces `SRS_LMS_v1.0.md` Section 9.1 to a normative reference to
this artifact. See `spec-workspace/library/README.md` and ledger `WORK-020` (authoring).
