---
capability_id: CAP-CANONICAL-FORM
version: 1.0
status: Draft
title: Canonical Form and Digest Constraint
project: blockchain-enabled-lms
adopted_by:
  - spec-workspace/projects/blockchain-enabled-lms/SRS_LMS_v1.0.md
created: 2026-11-13T03:35:00Z
updated: 2026-11-13T03:35:00Z
---

# Canonical Form and Digest Constraint (`CAP-CANONICAL-FORM`)

## Purpose

This capability defines how a record is reduced to a **canonical form** — a deterministic byte
sequence — so that a digest computed over it is reproducible by any party holding the same record.

It exists because a verifiability guarantee is only real if two parties independently compute the
same digest from the same record. Without a defined reduction, "the digest matches" is an
assertion rather than a check.

**It is a data-contract capability, not an implementation.** It specifies the *properties* the
canonical form must have and the rules that give it those properties. It does not specify an
encoding implementation, a digest algorithm, or a transport.

## Why it is needed

`SRS_LMS_v1.0.md` Section 2.8 states that a verifier "reduces it to the same fixed form, computes
the digest, and compares it with the committed digest". That guarantee is unimplementable unless
the reduction is defined. This artifact is that definition.

## The five required properties

### 1. Stable field set

The fields included in the canonical form are determined **by the record type**, and by nothing
else. The same record type always yields the same field set, on every occasion, for every party.

A field is in the canonical form if and only if its value is a property of the record itself.

### 2. Volatile fields excluded

A field whose value varies between otherwise identical records is **excluded**, and its exclusion
is stated in the record type's field list rather than left implied.

The following are excluded by default, and no record type may include them without a recorded
decision:

| Excluded | Reason |
|---|---|
| Session identifiers | Vary per session; carry no record meaning. |
| Last-read / access markers | Vary per reader. |
| Transport and envelope metadata | Vary per call: transport identifiers, received-at stamps, correlation values. |
| Storage and physical locators | Vary with replication, sharding, and rebalancing. |
| Cache and materialization state | Vary with access, not with content. |

A field that records *when a record was finalized* is **not** volatile — it is a property of the
record — and is included.

### 3. Defined ordering

The fields of the canonical form are ordered by a stated rule, so the reduction is deterministic
regardless of the order in which a party happens to read the fields.

The order is:

1. Fields in the order they are declared in the record type's field list.
2. Any nested structure follows the same rule recursively.

### 4. Defined encoding

Exactly one encoding is used to produce the canonical byte sequence, and it is stated in this
artifact. The encoding must be unambiguous — no two distinct record contents may produce the same
byte sequence, and no two parties may produce different byte sequences from the same content.

### 5. Versioned

The canonical form carries its own version, distinct from the version of the record type it
reduces.

This matters because the rules above can change. A proof committed under canonical form version
1.0 must remain verifiable after version 2.0 exists — so a verifier is told which canonical form
version applies, and the reduction used is the one that version defines. **A change to the
canonical form rules does not retroactively invalidate proofs committed under an earlier version.**

## What the digest covers

The digest is computed over the canonical byte sequence, and therefore covers every field the
canonical form includes — including, where the record type includes them:

* the record's identity,
* its content,
* the rule set identifier under which it was computed,
* the time of finalization, and
* the authorizing authority.

**The authority attestation and the time of finalization are inside the digest**, so they are
tamper-evident, not merely committed alongside it. A proof that committed them outside the digest
would assert an authority that could be altered without changing the digest.

## What this capability does not decide

* **Which domain owns these rules.** The owning domain is an open question (`SRS_LMS_v1.0.md`
  Question Q-5): ECS is the rule authority and LGS is the proof authority, and this artifact is
  used by both.
* **The digest algorithm.** That is an implementation choice, made in the implementation plan.
* **The field list of any particular record type.** That belongs to the record type's own
  specification — for the LMS, `WORK-LMS-CONTRACT-001` and its rendering.

## Adoption

| Artifact | How it is used |
|---|---|
| `spec-workspace/projects/blockchain-enabled-lms/SRS_LMS_v1.0.md` §2.8 | The proof of a finalized student-period record is a digest over the canonical form of that record. |
| `spec-workspace/projects/blockchain-enabled-lms/schema/final-academic-record.md` | Defines the record type whose canonical form is reduced and digested. |

## Open questions

1. Which domain owns the rules in this artifact — ECS as the rule authority, or LGS as the proof
   authority? (`SRS_LMS_v1.0.md` Q-5.)
2. What encoding satisfies property 4 for this project? The choice is implementation-level but must
   be recorded here once made.
3. Which fields of the `final_academic_record` payload are excluded under property 2? That
   belongs with the record type's specification, in `WORK-LMS-CONTRACT-001`.
