---
constitution_id: CONST-LMS-v1.3
id: CONST-LMS-v1.3
version: 1.3
status: Approved
project: blockchain-enabled-lms
scope: project
created: 2026-11-17T00:00:00Z
updated: 2026-11-18T20:27:51Z
---

# Blockchain-Enabled LMS — Project Constitution

> **Status: Approved.** v1.3 was approved by the human at Gate 2 on 2026-11-18 (Decision
> `WORK-178`), after independent review (verdict APPROVED WITH COMMENTS; findings F-01 to F-06,
> all informational; review session `ses_e1166ff8fffeISU1TbsWEM7x9g`). v1.3 re-pins three
> references that had been falsified: the Linked artifacts parent-SRS pin and the Open tensions
> item 5 "SRS Q-6 annotation PENDING" note (both falsified by the SRS v1.2 change - Gate 2
> `WORK-176`, applied at `b6ce80c`), and Open tensions item 7 (falsified by the capability
> promotions - Decision `WORK-175`, applied at `7a80293`; `CAP-STATUSENUMS` flipped under
> `WORK-176` in the same change). **No principle was added, changed or weakened.** The v1.2
> version was approved by the human at Gate 2 on 2026-11-18 (Decision
> `WORK-174`), after independent review (verdict CHANGES REQUIRED; findings F-01 to F-10; the
> human-ratified fixes and the F-03 ratification of the `WORK-156` interpretation are applied).
> v1.1 was approved at Gate 2 on 2026-11-18 (Decision `WORK-168`) and remains in git history
> (81c825f); v1.0 was approved at Gate 2 on 2026-11-17 (Decision `WORK-159`) and remains in git
> history (fcbc05a) - supersession is explicit, never silent overwrite. The v1.2 amendment changed
> no principle: it marks Open Tensions item 2 RESOLVED (interpretation of `WORK-156` - the contract
> v1.5 approval interpreted as the v1 acceptance the P-8 freeze tension required; ratified by the
> human at this Gate 2) and Open Tensions item 5 RESOLVED (Decision `WORK-173`:
> `blockchain-gateway` is outside the seven-domain model - an implementation component of LGS's
> proof-commit path). Nothing in this document weakens a Protected Invariant
> (root `AGENTS.md` Section 7). Working item: `WORK-177` (complete).

## 0. Authority and precedence

This constitution is the durable, versioned set of engineering principles for this project. It binds
specification, planning, implementation, and review for `blockchain-enabled-lms`.

Precedence: Protected Invariants > explicit user instruction > root `AGENTS.md` > this constitution
> this project's execution artifacts. Where a conflict is found, it is stated, recorded in the work
ledger, and resolved by a human Decision — never silently.

Technology choices, deployment topology, and hosting are **not** constitutional matters. They belong
to implementation planning and implementation. This document contains no executable content and
references no technology.

Principles are numbered flat (P-1…P-15) and grouped by the category they bind most strongly.
Security-relevant qualities are also binding on review even where they are listed under Quality.

## Quality

### P-1 Correctness before completeness and latency
When a rule set cannot be resolved, a governing context cannot be established, or an approval is
absent, the operation must be **refused**, never completed under an assumption. No workflow may
race an academic period's status or an approval.
*Rationale:* SRS Section 5 (Refusal over ambiguity; Latency); success criteria S-4, S-5.
*Trade-off:* more refusals and retries — refusal reasons must be legible, not silent failures.

### P-2 Immutability of finalized state
No field of a finalized grade record, and no field of a finalized student-period record, is ever
written. A correction appends a new record and expresses the relationship by linkage; it does not
amend what it corrects.
*Rationale:* SRS Section 5 (Immutability); S-1; Section 2.9 state transitions.
*Trade-off:* superseded history grows monotonically; "current" state is a read-side concern.

### P-3 Determinism and single rule authority
Given the same rule set and the same assessed inputs, the computed grade must be identical. Rules
in force are consistent across every domain that depends on them: ECS is the sole source of the
rule set for a level and period, and every dependent domain records the identifier it used.
*Rationale:* SRS Section 5 (Determinism); S-3, S-6; Section 6 composition rationale.
*Trade-off:* ECS availability and consistency become the critical path; its caching and replication
strategy is an implementation-plan concern and must not be improvised inside a domain.

### P-4 Traceability of authority
Every record that depends on a rule set must name it; every record that depends on an approval
must name the approving authority; and both are inside the digested canonical form. A level
transition is never automatic — it records explicit approval by a dean or principal authority.
*Rationale:* SRS Section 5 (Traceability of authority); S-5, S-6.
*Trade-off:* mandatory metadata on every state change; there are no "quick" writes.

### P-5 Auditability and attribution
Every state change to an academic record — creation, appeal, approval step, level transition —
must be attributable to an actor and an authorization, and retained. Appeals and amendments append
a new versioned record carrying a mandatory `parent_transaction_id`; originals are never mutated.
*Rationale:* SRS Section 5 (Auditability); Sections 2.4, 3.5; Section 2.9.
*Trade-off:* retention is monotonic; hard-deletion requests conflict with this principle and must
be resolved by an explicit retention-policy Decision, not by improvisation.

### P-6 Completeness of academic history
The operational record store must be able to reconstruct a student's complete academic history at
any point in time, including superseded records.
*Rationale:* SRS Section 5 (Completeness).
*Trade-off:* storage cost; superseded data cannot be expired casually. Tension with privacy and
retention — an explicit retention-policy Decision is owed (see Open tensions).

### P-7 The record store is a component, not a domain
The operational record store is the system of record for student academic achievements. The Ledger
Service commits an immutable proof over it — proof authority is not record authority. The store
exposes exactly two operations and remains a shared durable component, not a decision-maker.
*Rationale:* SRS Sections 3.6, 3.7, 6 (composition decision).
*Trade-off:* a constrained interface; every new query need must fit it or be added by explicit,
justified change — never by a side channel.

## Security

### P-8 Verifiability by an unprivileged third party
A finalized student-period record must be verifiable by a party with no access to the originating
services. Verification is served by **two** read-only surfaces, owned separately: the **canonical
payload** surface, owned by the operational record store (it publishes the canonical payload with
the canonical-form version, the digest algorithm identifier and the declared canonical field list —
not the reduced bytes, and no "commitments"), and the **proof sequence** surface, owned by the
Ledger Service (it serves the committed proof sequence). A proof is committed for **every** finalized
student-period record, and only for those (S-7). Provability does not depend on the lifetime of
any single service, **including the store**: both the canonical payload and the proof sequence are
archived, so loss of any one service does not destroy provability.
*Rationale:* SRS Section 5 (Verifiability); S-2, S-7; Sections 1.2, 2.8, 3.1, 3.7, 4.1.
*Trade-off:* the canonical form freezes early and changes are breaking; verification surfaces
must be designed together with the feature, never after it.

*(P-4 and P-5 are also binding security controls: attribution, authority linkage, and retention
are the authorization evidence for the appeal and correction paths. P-1 refusal-over-assumption is
the access-decision rule when authorization cannot be established.)*

## Testing

### P-9 Evidence-based completion
No completion claim without verifiable evidence: acceptance criteria mapped to artifact evidence,
review findings closed with evidence, and approval recorded as a work-ledger Decision. An
`Approved` status with no ledger Decision is a defect, not an approval.
*Rationale:* Protected Invariant III; `wf-converge`; this project's own WORK-009, WORK-136,
WORK-139 history.
*Trade-off:* ledger and review overhead on every task — accepted, non-negotiable in this project.

### P-10 Verifiability is tested, not asserted
Every acceptance criterion maps to a named artifact or executable check; canonical-form and digest
behavior is verified against vectors derived from the approved artifacts — the contract
(`WORK-LMS-CONTRACT-001`) is the field authority and `CAP-CANONICAL-FORM` is the reduction
authority (declared-field handling, ordering, encoding, volatile exclusions) — not from
re-derivation.
*Rationale:* testing consequence of P-8 and P-9; both authorities cited above govern together —
the contract for fields, `CAP-CANONICAL-FORM` for the reduction.
*Trade-off:* test vectors track the contract version; a contract change invalidates vectors and
both change together or not at all.

## Process

### P-11 Specification before implementation — always
No code without an approved specification. Code is produced only by `wf-implement`, against an
approved plan derived from an approved task specification, targeting
`generated-projects/blockchain-enabled-lms/` — never into `spec-workspace/`.
*Rationale:* Protected Invariant I; root `AGENTS.md` Section 4.
*Trade-off:* slower start; "just prototype it" is not a permitted action in this project.

### P-12 Explicit operation contracts over shared state
The seven service domains are closed decision-makers. A domain that needs another's data calls that
domain's operation; there is no shared state and no bypass read. Domain boundaries are contracts,
not deployment boundaries.
*Rationale:* SRS Section 3.1 (domain responsibilities and operations); Section 6 (composition
decision, consequence).
*Trade-off:* more interfaces to version and maintain; the shortcut is always visible and always
forbidden.

### P-13 Technology-agnostic specifications
Specification artifacts state capabilities, contracts, and requirements — never languages,
frameworks, vendors, storage engines, or hosting. Technology choices are made in implementation
planning and in implementation, and recorded there.
*Rationale:* Protected Invariant II; SRS Section 4.1 (non-goals, Implementation out of scope).
*Trade-off:* genuinely harder to write; reviews must bounce technology-laden specs.

### P-14 One normative contract per subject
Every contract has exactly one authoritative artifact. Renderings (e.g.
`schema/final-academic-record.md` of `WORK-LMS-CONTRACT-001`) must not introduce requirements the
authoritative artifact does not authorize; where they disagree, the authoritative artifact wins and
the rendering is the defect. Supersession is explicit; nothing is silently overwritten.
*Rationale:* spec-workspace `AGENTS.md` Section 4 (one filename, one contract); project
`AGENTS.md` Section 3 (the authoritative artifact wins; the rendering is the defect); root
`AGENTS.md` Section 6 (lifecycle and supersession); `CAP-CANONICAL-FORM`.
*Trade-off:* duplication is forbidden by construction — divergence is a defect to fix, not edit
around.

### P-15 Meta: this constitution
This constitution never weakens a Protected Invariant, contains no executable content, and changes
only by explicit, versioned revision with supersession marked — never silently.
*Rationale:* `wf-constitution` safety boundaries; root `AGENTS.md` Sections 6 and 7.
*Trade-off:* none. Absolute.

## Open tensions (owned; items 2, 4, 5 and 7 resolved 2026-11-18)

1. **P-5/P-6 vs privacy and retention.** Monotonic retention of superseded records and full audit
   attribution conflict with any future hard-deletion or minimisation requirement. An explicit
   retention-policy Decision is owed; this constitution does not resolve it.
2. ~~**P-8 freezes the canonical form early.** Every contract change after freezing is breaking by
   definition. Not resolved here; any v1 acceptance is a human Decision, or belongs to the first
   contract-revision agenda.~~
   **RESOLVED 2026-11-18** (interpretation of `WORK-156`, 2026-11-16, ratified at Gate 2 on
   2026-11-18 - the ratification is this amendment's own Gate 2 approval): the human approved the
   contract at v1.5, and that approval is interpreted as the v1 acceptance this tension required -
   the freeze is accepted for every proof committed under this form. Any future contract revision
   remains breaking by definition and remains a human Decision under this constitution.
3. **Latency governance.** The SRS deliberately makes no timing commitments; no performance
   principle beyond P-1 exists yet. If operational SLOs are ever required, they enter as a versioned
   revision of this constitution, not as ad hoc practice.
4. ~~**Canonical-form rule ownership (SRS Q-5; ledger WORK-130, open).** Which domain owns the
   canonical-form rules — ECS as rule authority or LGS as proof authority — is open.
   This bears on P-3, P-8 and on CAP-CANONICAL-FORM. Not resolved here.~~
   **RESOLVED 2026-11-18** (Decision `WORK-164`; SRS `v1.1` Section 9 Q-5, Decision `WORK-167`;
   `CAP-CANONICAL-FORM`). Neither domain owns the canonical-form rules: they are owned by the
   specification artifacts under spec-workspace governance. Neither ECS nor LGS may change them
   unilaterally; either may propose a revision; adoption requires a versioned revision of
   `CAP-CANONICAL-FORM`, independent review, and explicit human approval recorded as a ledger
   Decision. No runtime domain dependency is introduced. This bears on P-3, P-8 and P-14. Retained
   struck-through for traceability; not reopened.
5. ~~**`blockchain-gateway` placement (SRS Q-6; ledger WORK-037; service-contracts.yaml `domain:
   unresolved`).** Whether that gateway belongs to the seven-domain model at all is open. This
   bears on P-7 and P-12. Not resolved here.~~
   **RESOLVED 2026-11-18** (Decision `WORK-173`; closes `WORK-037`). The SRS Q-6 annotation was
   ~~PENDING - proposed Section 11 change request `WORK-171`, not yet applied; the SRS is unchanged as of this draft~~
   **applied 2026-11-18**: Section 11 Change Request `WORK-171` (Sections 8.1 and 9), Gate 2
   Decision `WORK-176`, applied at commit `b6ce80c` (SRS v1.2); this v1.3 amendment retires the
   PENDING note as stale. `blockchain-gateway` is OUTSIDE the
   seven-domain model: it is not a domain and not a service binding; the chain-client is an
   implementation component of LGS's proof-commit path, decided at implementation time by the
   LGS implementation plan. The manifest binding is superseded (`superseded_by: WORK-173`). This
   bears on P-7 and P-12 - both hold unchanged. Retained struck-through for traceability; not
   reopened.
6. **Rule-set identifier source (SRS Q-1).** The authoritative source of the rule-set identifier
   value is open. This bears on P-3 and P-4. Not resolved here.
7. ~~**Interim status vocabulary; capability artifacts exist but are unpromoted.** All five
   capability artifacts exist under `spec-workspace/library/Capabilities/` as `Draft` (created
   under ledger WORK-020, resolved 2026-11-16; promotion to Approved is a separate concern and is
   not a precondition). None is `Approved`, and `SRS Section 9.1`'s interim table still governs
   this project until the capability artifacts are promoted — at which point SRS Section 9.1
   should be revised to reference them. Not resolved here.~~
   **RESOLVED 2026-11-18** (Decision `WORK-175` - `CAP-CANONICAL-FORM` v1.0, `CAP-USERID` v1.1,
   `CAP-TIMESTAMPFORMAT` v1.1 and `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 promoted to `Approved`;
   `CAP-STATUSENUMS` v1.1 flipped `In_Review` -> `Approved` in the same change that applied
   Section 11 Change Request `WORK-171` (SRS v1.2, Gate 2 Decision `WORK-176`, commit `b6ce80c`)).
   All five capability artifacts are `Approved`; `SRS Section 9.1` no longer carries an interim
   table - it carries a normative reference to `CAP-STATUSENUMS` (the capability governs). This
   v1.3 amendment records the resolution; it does not reopen it. Retained struck-through for
   traceability; not reopened.

## Lifecycle and amendment

`Draft` → `In_Review` → `Approved` → `Superseded`. Independent review (`wf-review`) is mandatory
before `Approved`; approval is a Work Ledger Decision, not a status edit. Amendment requires the
same path and produces a new version; the old version is marked `Superseded`, never overwritten.

Clarification (v1.1): for a single-file constitution revision such as this one, supersession is
explicit through the in-file Amendment lineage block (see Linked artifacts) plus git history -
there is no separate `Superseded` file, and the old version is never overwritten in place without
the lineage record.

**Change record (v1.3, 2026-11-18).** Open tensions item 5 marked RESOLVED (the
   `PENDING` clause is struck through: the SRS Q-6 annotation was applied 2026-11-18 as part of
   Section 11 Change Request `WORK-171`, Sections 8.1 and 9, Gate 2 Decision `WORK-176`, commit
   `b6ce80c`); Open tensions item 7 marked RESOLVED (all five capability artifacts `Approved` -
   Decision `WORK-175`; `CAP-STATUSENUMS` under `WORK-176` in the same change), and the section
   heading re-anchored to items 2, 4, 5 and 7; Linked artifacts re-pinned to parent SRS v1.2;
   banner and frontmatter versioned to v1.3. **No principle was added, changed or weakened;
   P-1…P-15 and Section 0 are byte-identical to v1.2.** Amendment path per this section:
   independent review 2026-11-18 (verdict APPROVED WITH COMMENTS; findings F-01 to F-06, all
   informational; session `ses_e1166ff8fffeISU1TbsWEM7x9g`), then explicit human Gate 2 approval
   (Decision `WORK-178`). v1.2 remains in git history (`aa11a42`); never overwritten.

**Change record (v1.2, 2026-11-18).** Open tensions item 2 marked RESOLVED (`WORK-156` - the
human accepted the P-8 freeze by approving the contract at v1.5); Open tensions item 5 marked
RESOLVED (Decision `WORK-173` - `blockchain-gateway` outside the seven-domain model); banner and
frontmatter versioned to v1.2. **No principle was added, changed or weakened.** Amendment path per
this section: independent review (`wf-review`), then explicit human Gate 2 approval
(Decision `WORK-174` to be recorded at Gate 2). v1.1 remains in git history (`81c825f`); never overwritten.

**Change record (v1.1, 2026-11-18).** Open tensions item 4 marked RESOLVED (Decision `WORK-164`;
SRS `v1.1` Section 9 Q-5, Decision `WORK-167`; `CAP-CANONICAL-FORM`); Linked artifacts updated to
parent SRS `v1.1`; banner and frontmatter versioned to v1.1. **No principle was added, changed or
weakened.** Amendment path per this section: independent review (`wf-review`), then explicit human
Gate 2 approval (Decision `WORK-168`). v1.0 remains in git history (`WORK-159`); never overwritten.

## Linked artifacts

- Parent specification: `SRS_LMS_v1.0.md` (`SRS-LMS-v1.0` v1.2, Approved, `WORK-039`; v1.2
  amendment 2026-11-18 - Section 11 Change Request `WORK-171` (Sections 8.1 and 9), Gate 2
  Decision `WORK-176`, applied at `b6ce80c`; v1.1 amendment 2026-11-18 - Change Request
  `WORK-165`, Gate 2 `WORK-167`, applied at `4b3936a`; v1.0 anchored to SHA `167af69`)
- Task specification: `tasks/task-LMS-CONTRACT-001-noncode.md` (Approved v1.5, `WORK-156`)
- Collection binding: `binding.yaml`; runtime manifest: `service-contracts.yaml`
- Protected Invariants: root `AGENTS.md` Section 7; framework policy reference
- Approval: v1.0 - Gate 2, 2026-11-17, Work Ledger Decision `WORK-159`; v1.1 - Gate 2,
  2026-11-18, Work Ledger Decision `WORK-168` (status flipped Draft -> Approved in the same
  change); v1.2 - Gate 2, 2026-11-18, Work Ledger Decision `WORK-174` (status flipped Draft ->
  Approved in the same change). v1.3 - Gate 2, 2026-11-18, Work Ledger Decision `WORK-178`
  (status flipped Draft -> Approved in the same change; F-01 codebase-AGENTS.md pin cascade
  applied in the same change; review verdict and `WORK-177` transition recorded in the ledger).
- Amendment lineage: v1.0 (Approved 2026-11-17, `WORK-159`) → v1.1 (Approved 2026-11-18,
  `WORK-168`) → v1.2 (Approved 2026-11-18, `WORK-174`) → v1.3 (Approved 2026-11-18,
  `WORK-178`); v1.0, v1.1 and v1.2 retained in git history, never
  overwritten
- Work ledger: `spec-workspace/project-temp/work_ledger.yaml`
