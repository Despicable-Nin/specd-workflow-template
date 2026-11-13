---
id: CAP-CANONICAL-FORM
version: 1.0
status: Draft
title: Canonical Form and Digest Constraint
created: 2026-11-13T03:35:00Z
updated: 2026-11-13T04:25:00Z
---

# Canonical Form and Digest Constraint (`CAP-CANONICAL-FORM`)

## Purpose

This capability defines how a record is reduced to a **canonical form** — a deterministic byte
sequence — so that a digest computed over it is reproducible by any party holding the same record.

It exists because a verifiability guarantee is only real if two parties independently compute the
same digest from the same record. Without a defined reduction, "the digest matches" is an
assertion rather than a check.

**It is a data-contract capability, not an implementation.** It specifies the *properties* the
canonical form must have and the rules that give it those properties. It does not specify a digest
algorithm, a storage arrangement, or a transport.

## Why it is needed

A specification whose proof guarantee reads "a verifier reduces the record to the same fixed form
and recomputes the digest" is unimplementable unless the reduction is defined. This artifact is that
definition.

## The five required properties

### 1. Declared field set

The fields included in the canonical form are **exactly those the record type's canonical field list
declares**. The declaration, not a general test, is the authority.

This matters because a test such as "a field is included if its value is a property of the record"
collides with the exclusion rule below: an identifier field or a creation timestamp is a property of
the record, yet it also varies between otherwise identical records. Two parties applying such a test
could legitimately disagree. A declaration removes the ambiguity — there is one list, it is stated,
and both parties use it.

### 2. Volatile fields excluded by declaration

A field whose value varies between otherwise identical records is excluded, and the exclusion is
recorded in the record type's canonical field list rather than left implied.

A field may be both a property of the record and excluded. The declaration decides, not the
property. The following are excluded by default, and no record type may include them without a
recorded decision:

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

1. Fields in the order they are declared in the record type's canonical field list.
2. Any nested structure follows the same rule recursively.

### 4. Defined encoding

Exactly one encoding produces the canonical byte sequence, and it is stated here:

> The canonical byte sequence is the UTF-8 encoding of a **canonical JSON text** of the record: the
> declared fields only, in the declared order, with no insignificant whitespace, no duplicate member
> names, and the shortest form for numeric values.

It is unambiguous — no two distinct record contents produce the same byte sequence — and every party
produces the same byte sequence from the same content.

### 5. Versioned, and the version is committed

The canonical form carries its own version, distinct from the version of the record type it
reduces.

**The proof commits the canonical-form version and the digest algorithm identifier.** This is what
makes the versioning guarantee exercisable: a verifier learns which reduction rules and which
algorithm to apply, and a change to either requires a new canonical-form version rather than
silently invalidating proofs committed under the earlier one.

The verification surface publishes the canonical-form version and the algorithm identifier
alongside the payload, so a verifier never has to guess.

## What the digest covers

The digest is computed over the canonical byte sequence, and therefore covers every field the
canonical form includes — including, where the record type declares them:

* the record's identity,
* its content,
* the rule set identifier under which it was computed,
* the time of finalization, and
* the authorizing authority.

**The authority attestation and the time of finalization are inside the digest**, so they are
tamper-evident, not merely committed alongside it. A proof that committed them outside the digest
would assert an authority that could be altered without changing the digest.

## What this capability does not decide

* **The canonical field list of any particular record type.** That belongs to the record type's own
  specification, and is a prerequisite for committing any proof over that type.
* **Which domain owns these rules.** The owning domain is an open question for the adopting
  project — a rule authority and a proof authority are both candidates, and they are not the same
  party.
* **The digest algorithm.** The algorithm is chosen per adopting project, and its identifier is
  committed in every proof. Changing it requires a new canonical-form version.

## Adoption

An adopting project cites this capability from its specification and records the adoption. For
example, one project's proof guarantee depends on it directly: the student-period record there is
digested at period close, and the same project has raised the open question of which domain owns
these rules.

## Open questions

1. Which domain owns the rules in this artifact — the rule authority, the proof authority, or a
   third party?
2. Which record types, if any, require an encoding other than the default stated in property 4?
3. What is the canonical field list of each record type that is digested? Each is a prerequisite for
   committing a proof over that type.
