---
task_id: WORK-LMS-GRADERECORD-001
version: 1.3
status: Approved
project: blockchain-enabled-lms
parent_spec: SRS-LMS-v1.0
parent_spec_version: 1.3
task_type: noncode
calibration_file: task-LMS-GRADERECORD-001-noncode-calibration.md
created: 2026-11-19T16:22:00Z
updated: 2026-11-19T18:15:32Z
---

# Task Specification — `GradeRecord`, the GRA-Service assessment-outcome contract

`WORK-LMS-GRADERECORD-001` · non-coding task · parent: `SRS-LMS-v1.0` **v1.3** (`Approved`, Gate 2 `WORK-192`) · calibration: `CALIBRATION-LMS-GRADERECORD-001` (Gate 1 final, 2026-11-19)

> **Draft (v1.3).** Gate 2 pass 3 (verdict CHANGES REQUIRED; F-301–F-303; everything else in v1.2 verified resolved: F-201, F-202, F-205–F-208; regression steps pass; exactly one AMBIGUOUS — B3, Section 11 C-1) dispositioned in this revision: §13.9 assigns opacity for `assessment_id` and `parent_transaction_id` (F-301/F-302), restoring exhaustiveness over §13.2 (each §13.2 constraint exactly once — re-walked in-session: every opaque assignment now present, count of assignments per constraint = 1); AC-4 exclusion (i) names workflow step ordinals (N-1). No other changes; F-204's exhaustiveness claim is borne out by this text.
> **Draft (v1.2).** Gate 2 pass 2 (verdict CHANGES REQUIRED; F-201–F-208) dispositioned in this revision: F-05/F-07 carry-through defects fixed — `achievement_level` re-anchored to SRS §2.3/§3.1 (the glossary citation was unsupported) and the stray `GC` token replaced with the SRS §2.9 terminal anchor; §13.9 gains the `Finalized`-terminal/no-write row and presence-subsumption notes on the `GoverningRuleSetID` and `assessment_id`/`section_id` rows, making it exhaustive over §13.2; Appendix A `section_id` now points at the real FAR entry field (`EnrollmentDetail` holds no `section_id`); the §14 `educational_level` anchor cites §1.3/§2.2/§3.1 (§3.4 was the academic-period-ownership section); the §16 "SRS §11 Change Request" phrase is readable again (one corrupted glyph restored). This note supersedes the v1.1 note, which overstated compliance (F-204): pass 1 (F-01–F-13) was dispositioned in v1.1; pass 2 confirmed the load-bearing dispositions (F-01, F-02, F-03, F-04, F-06, F-08, F-09, F-11, F-12) and found the carry-throughs above; pass 2 also confirmed the walks produce exactly one AMBIGUOUS (B3, Section 11 C-1) — no other MISSING/AMBIGUOUS. F-205..F-208 applied; F-10 (artifact placement) dispositions with the human at Gate 3; F-13 informational, carried to the LGS task.
> **Draft (v1.1).** Independent Gate 2 review (verdict CHANGES REQUIRED; F-01–F-13) dispositioned in this revision: the `change_status` vocabulary caveat and the choice-3 proof-reference deviation now live in Section 11 (caveats C-1..C-6) and every `11-C`-style dangling marker is gone; Appendix A maps all 20 fields including `schema_version`; §13.9 is exhaustive over §13.2; AC-14 re-scoped to Sections 10 and 11; "Section 11 CR" disambiguated to "SRS §11 Change Request". B3's pre-disposition is carried consistently end-to-end (intro → Sections 10/11 → §13.2/13.8 → §15 → AC-8/AC-14). This note is retained verbatim from v1.1; the compliance claims it makes were corrected in v1.2 (pass 2).
> **Draft (v1.0).** First pass against the approved parent. Three known caveats are carried deliberately rather than resolved silently; each is recorded in Section 10 or Section 11 with an owner, and each is flagged where it applies: the `change_status` value vocabulary (SRS §2.4 step 5 names the flag, no Approved artifact enumerates its values), the glossary-vs-W-2 granularity reading (SRS §10 Glossary "Grade record" vs Workflow W-2 prose), and the `parent_transaction_id` / `transaction_id` format question (inherited SRS Q-2, open).

## 0. Plain-language summary (for registrar / academic-office readers)

This document fixes the *shape* of the immutable record of a student's assessed outcome — the
`GradeRecord`. Whenever an instructor submits results for one assessment, the grading service
records what was submitted and what was computed, with the formula rule set that produced it.
Once a grade is approved, that record never changes. If the grade must be corrected later, a new
record is appended that points back at the old one; the old one stays exactly as it was, which is
what makes the history auditable.

It does **not** say how the grade is computed, what the weights are, or what the pass mark is —
those are the Educational Context Service's content, and they are never written here. It fixes
only how a grade record is identified, structured, versioned, attributed, linked, and trusted.

If you only read one sentence: **no grade record is ever edited after approval — corrections append
a linked successor, and both remain in the record; what happens to superseded records at end of
retention is a separate, owed decision (Sections 3 and 13.7).**

## 1. Background and ownership

The LMS computes grades under a "governing formula" owned by ECS; the grade computation is
performed by **GRA-Service** (SRS §3.1; capability C-6). Grades are approved and recorded in the
operational record store, and the store is the record of truth (SRS §3.5–3.6). The SRS names
`GradeRecord` as a GRA-Service-owned operational record (§3.1) but defines no field-level contract
for it. That gap is what this task closes, at the same altitude as `WORK-LMS-CONTRACT-001` did for
the student-period record and `WORK-LMS-FORMULARULES-001` did for the rule set.

What the SRS already requires, and this contract anchors:

- the term's meaning — **one record per assessed outcome for one student in one assessment**
  (SRS §10 Glossary, "Grade record"; "Appended successor"; "Superseded");
- a **finalized grade carries the rule set identifier** under which it was computed
  (SRS §2.3 W-2 step 4 rule; success criteria S-3 and S-6, §4.2);
- **before** any critical state change ECS is consulted; a non-`Active` period refuses creation
  (SRS §2.2 W-1; §3.2 closed consumer set);
- **immutability and append-only correction** — no field of a finalized grade record is ever
  written; a correction appends a linked successor (SRS §2.3, §2.4, §2.9, §4.2 S-1; §5
  Immutability; `Finalized` terminal (SRS §2.9));
- **attributable state changes** — creation, approval, and every appeal step are attributable to an
  actor and an authorization (SRS §5 Auditability; §3.5);
- **determinism** — same rule set + same assessed inputs ⇒ identical computed grade; the rule set
  identifier is sufficient to reproduce the computation (SRS §5 Determinism);
- the grade record's **state machine** is governed by `CAP-STATUSENUMS` v1.2 and SRS §2.9:
  `Proposed` → `Finalized`; an appended appeal successor is created directly in `Finalized`; there
  is no `Superseded` state (SRS §2.9 "Grade record"; `Finalized` is terminal).

## 2. In scope

- The inline, field-level, technology-agnostic contract for the `GradeRecord` record type
  (Section 13): fields, types, cardinality, nullability, constraints, normative semantics,
  identity rules, immutability rules, and supersession linkage.
- The **state machine** obligations (Proposed → Finalized; direct-`Finalized` appeal successors),
  aligned verbatim to `CAP-STATUSENUMS` v1.2 (Section 13.4).
- The **refusal vocabulary** for this record type and its enforcement boundaries (Section 13.8).
- The **validation boundaries** — which guarantees are contract-level, which are GRA-Service
  runtime, which are ECS runtime (Section 13.9).
- The **appended successor** mechanics for corrections (Section 13.3, Section 13.7).
- A **downstream conformance pre-check** executed by the reviewer: Walk A (W-2 submission →
  approval → recording path) and Walk B (W-3 appeal → successor record → aggregate rebuild path),
  Section 15.
- An **appendix mapping** the record to the `final_academic_record`
  `academic_history` entry (Appendix A), for the assembled aggregate.

## 3. Out of scope (explicit non-goals)

- **Formula content of any kind.** No weights, thresholds, cutoffs, aggregation rules,
  attendance-component percentages, or pass/fail rules (SRS §2.3 Formula-ownership annotation).
- **`GradeAppealRecord`, `ReviewLog`, `LevelCompletionRecord`, `StudentPeriodRecord`** — separate
  records, owned by GRA-Service but not contracted here. The student-period record is contracted by
  `WORK-LMS-CONTRACT-001` (normative rendering `SCHEMA-LMS-FAR-v1.0`).
- **The `change_status` value vocabulary.** SRS §2.4 step 5 obliges the appended successor to
  carry the "status flag of the change"; no Approved artifact enumerates the values. Carried as an
  open question with an owner (Section 11) — not invented here.
- **ECS implementation, GRA-Service implementation, storage, identity, or deployment decisions.**
- **Editing the SRS, constitution, CAP artifacts, the FAR contract or its rendering, the FormulaRules
  contract, or `service-contracts.yaml`.** All frozen; this task touches none of them.
- **Coding.** Any slice requiring code spawns a separate coding task via `wf-task-code`.
- **`parent_transaction_id` / `transaction_id` format** — inherited SRS Q-2; this contract states
  opacity and defers format to its owner.
- **Retention policy** for superseded grade records — constitution tension 1; a Decision is owed
  separately.

## 4. Expected behavior (technology-agnostic)

A `GradeRecord` is created exactly when assessed results for one assessment are submitted and a
grade is computed under the governing rule set:

1. The submission names the enrolled student, the section, the assessment, and the raw scores.
   GRA-Service consults ECS for the governing rule set **before** computing, and refuses creation
   if the period is not `Active` (SRS §2.2 W-1; §3.2). A non-`Active` period refuses; no record is
   created.
2. GRA-Service applies the formula and records a proposed record with status `Proposed`, carrying
   the rule set identifier returned in step 1 (SRS §2.3 W-2 steps 2–3).
3. The grade is approved and recorded in the operational record store with status `Finalized`, and
   the approving authority is recorded against it (SRS §2.3 W-2 step 4). `Finalized` is terminal.
4. A correction after `Finalized` is expressed **only** by appending a new record linked to the
   predecessor via `parent_transaction_id`; the predecessor's fields are never written (SRS §2.4
   W-3 step 5; §2.9; §5 Immutability; S-1). An appeal-approved successor is created directly in
   `Finalized` (SRS §2.9; `CAP-STATUSENUMS` v1.2).

Guarantees this contract makes: deterministic computation under the recorded rule set (reproducible
from the rule set identifier); attributable approvals; immutable finalized records; linked
append-only corrections; refusal over ambiguity (nothing is recorded under an assumption).

## 5. Acceptance criteria (measurable; non-code deliverables)

| ID | Criterion | Check |
|---|---|---|
| AC-1 | Task spec exists at `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-noncode.md` with `status: Approved` and `task_type: noncode` before `wf-plan` runs. | Path + frontmatter inspection |
| AC-2 | Every field of `GradeRecord` (Section 13.2) defined with type, cardinality, nullability and normative semantics; identity field defined with opacity/uniqueness/stability/immutability rules (13.2 field 1; 13.4); every presence rule has an explicit condition (13.2, 13.3). | Reviewer field-by-field check |
| AC-3 | Determinism is stated as a contract guarantee: same rule set + same assessed inputs ⇒ identical `grade_final`, with a written stability/immutability clause (13.4). The rule set identifier is stated as sufficient to reproduce the computation. | Reviewer reads the clause |
| AC-4 | **No formula content.** The spec contains no numeric weights, thresholds, component percentages, pass/fail cutoffs. Check: word-tokenizer scan of the normative sections (Sections 13, 14 and 15 prose; Section 0 is glossaried plain language and excluded; Section 3 out-of-scope examples excluded by path) for **standalone numeric literals** (digit-only tokens) within 10 word-tokens of any of `weight`, `weights`, `percentage`, `threshold`, `cutoff`; zero hits required. Excluded from the digit class: (i) cross-reference tokens (`§13.5`-style section references, `P-12`, `S-3`, `AC-4`, `W-2`, `WORK-*` identifiers, dated timestamps, workflow step ordinals such as `W-2 step 4`); (ii) bare dotted section references (`13.5`-style), treated as one excluded token; (iii) table-cell digits in the §13.2 field tables that are structural metadata of the table itself — row ordinals in the leftmost cell (`1`…`20`) and cardinality cells (`0`, `1`, `0..1`, `1..n`) — between cell pipes. | Precise word-tokenizer per this definition at review |
| AC-5 | Traceability matrix (Section 14) present: every contract field cites an SRS anchor; "no field cites nothing" is the rule — §1.3, §2.2, §2.3, §2.4, §2.9, §3.1, §3.5, §3.6, §4.2 S-1/S-3/S-6, §5, §9.1-with-`CAP-STATUSENUMS`, §10 are expected anchors, not exhaustive. | Reviewer checks the matrix |
| AC-6 | Ownership clause recorded (13.1): GRA-Service solely owns and writes the record; consumers read via operational-record-store operations; no other domain writes; the record is never proof-committed (proofs are over student-period records only); attendance aggregates are never embedded. | Reviewer confirms clause + SRS citations |
| AC-7 | Capability adoption table (Section 7) present: each capability adopted/declined with rationale and version pin. | Reviewer vs `library/Capabilities/` frontmatter |
| AC-8 | **Downstream conformance pre-check** executed before Gate 3, per Section 15: Walk A (W-2 submission → approval → recording; A1–A5) and Walk B (W-3 appeal → successor record → aggregate rebuild; B1–B5), logged as `step \| input required \| field providing it \| OK/MISSING/AMBIGUOUS`; any MISSING/AMBIGUOUS not pre-dispositioned in Section 11 blocks Gate 3 until resolved. The `GradeAppealRecord` reference-by-transaction-identity path is checked inside Walk B (B2), not as a separate walk. | Pre-check log attached to review |
| AC-9 | Plain-language summary (Section 0) present and readable by a non-technical registrar audience; no jargon without gloss. | Reviewer read-through with a registrar-reader note |
| AC-10 | Technology-agnostic: no language, storage engine, framework, protocol or vendor named. Reviewer greps against a stated marker list (languages, DBMS, cloud vendors, frameworks, protocols). | Automated grep with marker list |
| AC-11 | Refusal clause present and correctly scoped (13.8): refusal applies to malformed requests, rule-set resolution failure (scoped to never-existed/unresolvable), unsupported `schema_version`, and unknown predecessor; historical (superseded) record identifiers MUST still resolve for reproduction; refusal there is a contract violation. | Reviewer confirms scope + reason codes |
| AC-12 | Validation boundary table (13.9) present and **exhaustive over §13.2's field constraints** (each constraint appears exactly once as contract-level, GRA-Service runtime, or ECS runtime), cross-checked by the reviewer. | Reviewer cross-checks exhaustiveness |
| AC-13 | State machine conformance: `status` admits exactly `Proposed` and `Finalized` (per `CAP-STATUSENUMS` v1.2 and SRS §2.9); an appended successor is created directly in `Finalized`; there is no `Superseded` state; no transition table in this contract restates or contradicts Section 2.9. | Reviewer compares tables |
| AC-14 | **Open-question and caveat register complete with owners** (Sections 10 and 11): every caveat or question in this spec names its owner and disposition; the `change_status` vocabulary (Section 11), the glossary-vs-W-2 granularity reading (Section 10, Q-OWN-2), and SRS Q-2 (Section 11) are all carried explicitly; none is silently resolved. | Reviewer cross-checks Sections 0, 2–4, 10, 11, 13 |
| AC-15 | **FAR alignment coverage** (Appendix A) present: every `GradeRecord` field is mapped to its `final_academic_record` `academic_history`-entry counterpart (or marked record-local), with type and semantics identical where mapped; no mapped pair contradicts the Approved rendering (`SCHEMA-LMS-FAR-v1.0`). | Reviewer cross-checks Appendix A vs the rendering |

## 6. Verification requirements

- Independent `wf-review` of the draft (Gate 2), findings resolved; verdict recorded as a work
  ledger item.
- Human approval at Gate 3; approval Decision recorded in the work ledger.
- The pre-check walks (Section 15) executed by the reviewer and logged; the log attaches to the
  review evidence. Rows pre-dispositioned in Section 11 are not failures; any other
  MISSING/AMBIGUOUS blocks Gate 3.
- After records exist in any later implementation, an audit of the operational record store shows
  originals and successors both present, linked, originals unchanged (SRS S-1) — verified when that
  slice runs, not here.
- Regression checks at review: AC-4 tokenizer scan (zero applicable hits) and AC-10 marker grep
  (zero hits) re-run on the final text.

## 7. Reusable capabilities adopted

| Capability | Version | Disposition | Rationale |
|---|---|---|---|
| `CAP-TIMESTAMPFORMAT` | v1.1 | **ADOPT** | `submission_timestamp` / `approved_at` are ISO 8601 extended timestamps. |
| `CAP-SCHEMAVERSIONCONSTRAINT` | v1.1 | **ADOPT** | `schema_version` on the record; rejection rule applies; per-segment semantics are this contract's own decision (13.10). |
| `CAP-USERID` | v1.1 | **ADOPT** | `student_id` / `approved_by`; format governed by this capability. Group/authority (non-person) identities are an ECS/IAM decision; the capability's opaque-string format applies unchanged. |
| `CAP-STATUSENUMS` | v1.2 | **ADOPT** | Grade record states `Proposed`, `Finalized` and the direct-`Finalized` appeal-successor transition row are governed by this capability (v1.2); this contract restates nothing. |
| `CAP-CANONICAL-FORM` | v1.0 | **DECLINE** | Grade records are never proof-committed; the proof unit is the finalized student-period record (SRS §2.8). |

## 8. Dependencies

- Parent: `SRS-LMS-v1.0` v1.3 (Approved; `WORK-192`).
- Sibling contracts: `WORK-LMS-CONTRACT-001` (student-period record; `GradeRecord` is the
  operational-record counterpart of its `academic_history` entries; alignment in Appendix A) and
  `WORK-LMS-FORMULARULES-001` (the rule set identifier this record carries; identifier semantics
  owned there).
- `WORK-LMS-ATTENDANCE-001` (or equivalent) — the Session/AttendanceRecord contract for the ESS
  side of W-7/W-2 attendance consumption; not a blocker for this contract (attendance aggregates
  are consumed but never embedded).
- `WORK-196` — remains open for the Session/AttendanceRecord contract after this task closes.
- Open: SRS Q-2 (`parent_transaction_id` format) and the `change_status` vocabulary gap — holders
  of Section 11 caveats; neither blocks authoring this contract's structure.

## 9. Consistency note (alignment with the parent spec)

This task implements no capability that does not exist, and contradicts no Approved artifact:

- Ownership matches SRS §3.1 (GRA-Service owns `GradeRecord`) and §3.5/§3.6 (audit trail home;
  operational record store is the record of truth). The record is **not** an ECS-owned rule
  authority artifact; it **consumes** ECS's identifier and is **never** proof-committed
  (§2.8 proof unit is the student-period record; §4.1 Attendance and the proof).
- State machine is `CAP-STATUSENUMS` v1.2's grade-record table, verbatim; supersession posture is
  §2.4/§2.9's append-only model; "Superseded" is a relationship, never a state (§10 Glossary).
- `GoverningRuleSetID` naming aligns with `WORK-LMS-CONTRACT-001`'s `GoverningRuleSetID` — the same
  field, the same ECS-supplier / GRA-Service-recorder relationship — rather than the FormulaRules
  contract's `rule_set_id`, which is the identifier of the rule set artifact itself.
- `CAP-STATUSENUMS` is adopted, not restated: any perceived difference between this contract and
  the capability defers to the capability (SRS §9.1).
- No requirement herein authorizes changing any Approved artifact; all changes flow through Change
  Control (SRS §11).

## 10. Open questions (with owners — recorded, not resolved here)

| ID | Question | Owner | Disposition |
|---|---|---|---|
| Q-OWN-2 | Granularity reading — glossary says one record per assessed outcome in one assessment; W-2 prose says "produces a proposed final grade". This contract follows the glossary (authoritative for term meaning); per-assessment outcomes aggregate into the student-period record (SRS §2.7; `WORK-LMS-CONTRACT-001`). | Human / wf-review adjudication | Recorded interpretation; change control if rejected. |
| Q-OWN-4 | Who may approve a grade at W-2 step 4, and whether `approved_by` is constrained by ECS approval chains. | ECS/IAM via ECS approval-chain operations; SRS §3.1 | By reference, not decided here; chain resolution for appeals is ECS runtime (13.9). |

## 11. Inherited questions and caveats (carried, with owners)

- **C-1 — `change_status` value vocabulary (inherited SRS gap; SRS §2.4 step 5).** The SRS obliges an appended successor to carry "the status flag of the change", but no Approved artifact enumerates the values. **Owner: change control** — remedy via an SRS §11 Change Request or `CAP-STATUSENUMS` v1.3. This contract types the field (descriptive string; present exactly when `parent_transaction_id` is present) and requires validators to refuse unknown values (13.8 `change_status_unsupported`). The values themselves are never invented here. Walk B row B3's AMBIGUOUS is this caveat, pre-dispositioned; it is not a failure.
- **C-2 — `parent_transaction_id` / `transaction_id` format and minter (inherited SRS Q-2, open).** Both fields are typed as opaque strings; this contract adds no format mandate. Whether the minter of the record identity is GRA-Service or the operational record store is an implementation detail, not a contract decision. **Owner: domain owners (SRS Q-2).**
- **C-3 — Calibration choice 3 deviation (recorded, not silently dropped).** The calibration required confirming that this record can carry "the finalization proof reference". That reference exists only on proof-committed records, and proofs are over the finalized student-period record — never over grade records (SRS §2.8; §13.1). Binding scope trumps a mis-instrumented check: calibration is satisfied on the other two items (`GoverningRuleSetID`, `parent_transaction_id`), and Walk B (B1–B5) covers the successor-linkage path. **Owner: this task / human at Gate 3.**
- **C-4 — Formula ownership** — weights, aggregation semantics, achievement bands, pass/fail rules, and which attendance outcomes count toward presence are **ECS content** (SRS §2.3 Formula-ownership annotation). Nothing in this contract authors, embeds, or derives any of them; the fields that carry application outcomes (`weight`, `achievement_level`) declare application, not definition.
- **C-5 — SRS Q-1** — resolved in substance (`WORK-179`): ECS mints and owns `GoverningRuleSetID`; GRA-Service records it (SRS §2.7). Format of the identifier remains opaque (Section 11, C-2).
- **C-6 — Approved artifacts** — SRS, constitution, capabilities, FAR contract and rendering, and the FormulaRules contract are frozen; this spec creates nothing outside its own task artifacts. A review finding requiring changes to any of them is an SRS §11 Change Request, not an edit here.

## 12. Risks

| # | Risk | Mitigation |
|---|---|---|
| R-1 | Weight/threshold leakage into the contract "as examples" | AC-4 tokenizer scan; exclusion path discipline; reviewer check |
| R-2 | `change_status` invented ad-hoc in code after approval | Section 11 C-1 carried; 13.2 declares the field with unknown-value refusal (13.8); vocabulary owned by change control |
| R-3 | Treated as an amendment path for finalized grades | 13.3/13.7 normative: successor append only; originals never written; S-1 audit remains meaningful |
| R-4 | Grade record confused with student-period record or with `GradeAppealRecord` | 13.1 scope; Appendix A alignment; out-of-scope §3; Walk B keeps the appeal record distinct |
| R-5 | Timestamps mixed (UTC vs local; format drift) | `CAP-TIMESTAMPFORMAT` v1.1 ADOPT; 13.2 pins ISO 8601 extended; AC-7 pins versions |
| R-6 | Contract edited outside this control cycle after approval | Frozen like its siblings; changes only via CR/version bump |
| R-7 | `transaction_id` name collides with LGS `TransactionID` in integrators' code | 13.2 semantics state explicitly: distinct store identity; LGS `TransactionID` is the proof-commit identity over student-period records; no value-sharing is declared |

## 13. The `GradeRecord` contract (normative deliverable)

### 13.1 Ownership

`GradeRecord` is **GRA-Service-owned operational configuration of grades** (SRS §3.1, §3.5).
GRA-Service is the sole writer. Consumers read through the operational record store's two
operations (SRS §3.7) or through GRA-Service operations; no other domain creates, updates, or
deletes these records. The record is an operational record: it is **never proof-committed** and
**never enters the canonical form** of a student-period record (SRS §2.8, §4.1). The audit trail
home for these records and their linkage is the operational record store (SRS §3.5). Attendance
aggregates are **never embedded** in this record (SRS §2.3 W-2 formula-ownership annotation;
attendance flows only as an ECS formula input).

### 13.2 Record fields (normative)

Conventions: a 0..1 field is **omitted** when not applicable; no field carries a null value. The
record identity field (`transaction_id`) is minted at creation; whether the minter is GRA-Service
or the operational record store is an implementation detail this contract does not decide — only
opacity, uniqueness across all time, non-reuse, stability, and immutability are required.

| # | Field | Type / format | Card. | Null? | Normative semantics |
|---|-------|---------------|-------|-------|---------------------|
| 1 | `transaction_id` | opaque non-empty string | 1 | No | The record's own identity and the value `parent_transaction_id` references in an appended successor (13.3). Globally unique across all time; never reused; immutable once minted; referenced by appeals as the grade's transaction identity (SRS §2.4 step 1). Not the LGS proof-commit `TransactionID` (SRS §3.1); no value-sharing is declared (R-7). Format is opaque by contract (SRS Q-2, inherited; Section 11, C-2). |
| 2 | `student_id` | `UserID` (CAP-USERID v1.1) | 1 | No | The student whose outcome this record attests. Attribution anchor (SRS §5 Traceability of authority). |
| 3 | `educational_level` | enum: `Primary School` \| `Secondary School` \| `College` | 1 | No | The level the outcome was computed under (SRS §1.3 literal values). |
| 4 | `academic_period` | opaque reference (ECS-owned) | 1 | No | The ECS-owned academic period identity the outcome belongs to (SRS §3.4). Not embedded copy; resolvable only via ECS period operations. |
| 5 | `section_id` | opaque reference (ESS-owned) | 1 | No | The section in which the assessment was taken. ESS-owned identity referenced, not copied. |
| 6 | `assessment_id` | opaque non-empty string | 1 | No | Identifier of the assessed outcome this record attests; unique within the operational record store. Aligns with `academic_history[].assessment_id` (Appendix A). |
| 7 | `assessment_type` | descriptive string | 1 | No | The kind of assessment. The set of kinds is ECS rule content (SRS §3.1); not constrained here. |
| 8 | `GoverningRuleSetID` | opaque string | 1 | No | The rule set identifier supplied by ECS and recorded by GRA-Service under which the grade was computed (SRS §2.2 W-1 step 4; §2.3 W-2 steps 2–4; §2.7 step 1). The rule set identifier is sufficient to reproduce the computation (SRS §5 Determinism). Mints: ECS (Q-1 substance, `WORK-179`). |
| 9 | `grade_raw` | number | 1 | No | The score before finalization semantics; raw and uninterpreted (SRS §2.3 W-2 step 1). |
| 10 | `grade_final` | string | 1 | No | The finalized grade as computed under the governing rule set. Format unconstrained (bands/letters/numbers are ECS rule content). Mandatory: a record without a computed grade is not a `GradeRecord`. |
| 11 | `max_score` | number | 1 | No | The maximum attainable score for the assessment; the scale `grade_raw` is measured against. |
| 12 | `weight` | number | 0..1 | No | The weighting applied to this outcome in the aggregate, when the governing rule set applies one. Application is recorded, not authored; presence decided by the rule set. Absent where the level does not use weighting. |
| 13 | `achievement_level` | string | 0..1 | No | The band awarded. The set of bands is ECS rule content; not constrained here. |
| 14 | `submission_timestamp` | ISO 8601 extended (CAP-TIMESTAMPFORMAT v1.1) | 1 | No | Time the results were submitted (SRS §2.3 W-2 step 1). Audit anchor; never used for in-force selection. |
| 15 | `status` | enum: `Proposed` \| `Finalized` (CAP-STATUSENUMS v1.2) | 1 | No | `Proposed` when results are submitted and a grade is computed; `Finalized` when approved and recorded (13.4). Terminal at `Finalized`. |
| 16 | `schema_version` | `MAJOR.MINOR.PATCH` (CAP-SCHEMAVERSIONCONSTRAINT v1.1) | 1 | No | Presence + format conforming to that capability; unsupported MAJOR → rejection (13.8). Per-segment semantics are this contract's own decision (13.10). |
| 17 | `parent_transaction_id` | opaque string | 0..1 | No | **Present exactly when** this record is an appended successor (13.3). Its value is the predecessor's `transaction_id` (the appeal references the grade by transaction identity, SRS §2.4 step 1/5). Absent on an original record. |
| 18 | `change_status` | descriptive string | 0..1 | No | **Present exactly when** `parent_transaction_id` is present. Carries "the status flag of the change" (SRS §2.4 step 5). The value vocabulary is an open question owned by change control (Section 11, C-1); validators MUST refuse unknown values (13.8). Semantics of *presence* are contract-level; semantics of *values* are not. |
| 19 | `approved_by` | `UserID` (CAP-USERID v1.1) | 0..1 | No | **Required iff `status` is `Finalized`.** The approving authority recorded against the grade (SRS §2.3 W-2 step 4). |
| 20 | `approved_at` | ISO 8601 extended (CAP-TIMESTAMPFORMAT v1.1) | 0..1 | No | **Required iff `status` is `Finalized`.** Must be ≥ `submission_timestamp`. Approval time marker; not used for ordering of superseded records (linkage does that). |

### 13.3 Appended successor (appeal correction) mechanics

An appended successor record (SRS §2.4 W-3 step 5; appended successors are created directly in
`Finalized`, SRS §2.9; `CAP-STATUSENUMS` v1.2):

- is a **new** record with its own `transaction_id`;
- references its predecessor via `parent_transaction_id` = the predecessor's `transaction_id`;
- carries `change_status` (value vocabulary per Section 11, C-1; unknown values refused, 13.8);
- carries `approved_by` / `approved_at` (required iff `Finalized`);
- may carry **different outcome values** (`grade_raw`, `grade_final`, `max_score`, `weight`,
  `achievement_level`) — the correction exists to change them;
- carries the **same** identity-of-outcome semantics for `student_id`, `educational_level`,
  `academic_period`, `section_id`, and `assessment_id` (the corrected outcome is the same outcome);
- is created under the rule set identified in the original record (SRS §2.4 W-3 step 2);
- never causes any field of the predecessor to be written (SRS §2.4; S-1; §5 Immutability).

A record in `status: Proposed` may be revised **before approval** (it is not yet a finalized
record); once `Finalized`, only 13.3 applies. There is no `Superseded` state anywhere (SRS §2.9;
§10 Glossary).

### 13.4 Stability, immutability and determinism

- `transaction_id` is globally unique across all time and never re-minted.
- The record is **immutable after `Finalized`**; a correction for the same outcome is a new record
  carrying `parent_transaction_id` (13.3); the original is never altered.
- Given the same rule set (`GoverningRuleSetID`) and the same assessed inputs (`grade_raw`,
  `max_score`, plus any inputs the rule set consumes — e.g. the ESS attendance aggregate under
  W-2), computation is **deterministic**: identical `grade_final` (SRS §5 Determinism). The rule
  set identifier is stated by this contract to be sufficient to reproduce the computation
  (SRS §5; §4.2 S-3, S-6).
- Historical records (including superseded ones, linked by `parent_transaction_id`) resolve for
  reproduction; refusal to resolve them is a contract violation (13.8; Section 11, C-1).
- `status` transitions are governed by `CAP-STATUSENUMS` v1.2 and SRS §2.9 verbatim; this contract
  restates nothing and invents no states.

### 13.5 The computation boundary

GRA-Service applies the formula internally; no weights, thresholds, or aggregation semantics are
declared by, embedded in, or derivable from this contract or from the record envelope. The record
stores the **application outcome** of the formula, not the formula. Validators and consumers that
are not computing the formula (e.g. store auditors) verify envelope, types, formats, enums, and
linkage only — never formula content. `weight` records the applied coefficient, never its derivation.

### 13.6 Approval authority: by reference (recorded decision)

The approving authority for a `Proposed` → `Finalized` transition is recorded as `approved_by`
(UserID). **Which roles may approve** a grade at W-2 step 4 is not decided by this contract: it is
an IAM/ECS authority question resolved through ECS operations (SRS §2.4 approval-chain operations
apply to appeals and level transitions; W-2's approval step is recorded against an actor this
contract cannot enumerate). Appeal approval chains for corrections are ECS-runtime concerns
(13.9). This is a recorded by-reference decision at the same altitude as `FormulaRules` §13.6.

### 13.7 Supersession and migration

Supersession is expressed **only** by an appended successor linked via `parent_transaction_id`
(13.3). Originals are never altered, and there is no `Superseded` state. The system governs
records it creates; historical migration of grades finalized before this system existed is a
non-goal (SRS §4.1). Retention of superseded records is constitution tension 1; a Decision is owed
separately and is not made here.

### 13.8 Refusal vocabulary (defined contract-wide; enforced at the stated boundary)

The codes below are defined here for vocabulary uniformity; the enforcing boundary of each code is
column 3, and 13.9 must remain exhaustive to match it.

| Condition | Refusal reason code | Enforced at |
|---|---|---|
| Malformed request (level/period/student/section/assessment absent or unparseable) | `grade_request_malformed` | Contract-level (any conforming validator) |
| `GoverningRuleSetID` unknown — never existed, unresolvable in **any** scope | `rule_set_not_found` | Contract-level (definition); ECS runtime (detection) |
| `schema_version` MAJOR unsupported by the validator | `schema_version_unsupported` | Contract-level |
| Appeal references an unknown grade (`parent_transaction_id` unresolvable) | `grade_record_not_found` | Contract-level (definition); GRA-Service runtime (detection) |
| `change_status` value not recognized (vocabulary open per Section 11, C-1) | `change_status_unsupported` | Contract-level |

Historical (superseded) identifiers MUST resolve for reproduction; refusing one because it is
superseded is a **contract violation**, and `grade_record_not_found` / `rule_set_not_found` never
apply to an existing predecessor.

### 13.9 Validation boundaries

Exhaustive over §13.2 field constraints (each appears exactly once):

| Guarantee | Enforced at |
|---|---|
| Required fields present; non-empty; `schema_version` format per CAP-SCHEMAVERSIONCONSTRAINT; unsupported MAJOR rejected | **Contract-level** (any conforming validator) |
| `transaction_id` opacity, uniqueness scope (all time), non-reuse, immutability | **Contract-level** (mint + post-mint checks) |
| `educational_level` within the three literal values; `status` within `Proposed`/`Finalized` | **Contract-level** |
| `GoverningRuleSetID` format-opaque and presence (presence subsumed by row 1) | **Contract-level**; its *resolution* is **ECS runtime** (13.8 `rule_set_not_found` detection) |
| `grade_raw` / `max_score` / `weight` are numbers; `weight` presence decided by the rule set | **Contract-level** |
| `grade_final` string present; `achievement_level` string present-optionally | **Contract-level** |
| Timestamp formats per CAP-TIMESTAMPFORMAT; `approved_at` ≥ `submission_timestamp` on Finalized | **Contract-level** |
| Attribution presence on `Finalized` (`approved_by`, `approved_at`); UserID format (CAP-USERID) applies to `student_id` and `approved_by` | **Contract-level** |
| `academic_period` opaque, ECS-owned reference, resolvable only via ECS period operations (its mere presence/non-emptiness is subsumed by row 1) | **Contract-level** (opaque, no format declared); **ECS runtime** (period resolution) |
| `assessment_id` opaque non-empty (subsumed by row 1) and unique in store; `section_id` non-empty opaque (subsumed by row 1) | **Contract-level** (store audit) |
| `parent_transaction_id` opaque (SRS Q-2 inherited; Section 11 C-2), present iff appended successor; `change_status` present iff `parent_transaction_id` present; unknown `change_status` refused | **Contract-level** (shape); **GRA-Service runtime** (predecessor resolution, W-3 linkage) |
| W-1 `Active` gating at creation; W-2 submission flow; W-3 approval-chain resolution for appeals; aggregate rebuild choosing successor over predecessor | **ECS runtime** (gating + chain); **GRA-Service runtime** (flow + rebuild) |
| Formula application producing `grade_final` | **GRA-Service runtime only** (formula is ECS content; application is GRA-Service) |
| Supersession linkage integrity (`parent_transaction_id` points at an existing `transaction_id`) | **GRA-Service runtime** (append-time check); **contract-level** (post-hoc audit detects violations) |
| `status` semantics — `Finalized` is terminal; no field of a `Finalized` record is ever written (§2.9; S-1) | **GRA-Service runtime** (append-only flow); **contract-level** (post-hoc audit detects writes to finalized records) |

### 13.10 `schema_version` per-segment semantics (this contract's own decision)

| Segment | Meaning | Validator behavior |
|---|---|---|
| MAJOR | Breaking change to envelope or opacity boundary (consumer-incompatible) | Unsupported MAJOR → reject (`schema_version_unsupported`) |
| MINOR | Additive envelope extensions (new optional fields); semantically inert for computation | Accept; ignore unknown fields per CAP-SCHEMAVERSIONCONSTRAINT |
| PATCH | Editorial/clarification only; no structural change | Accept |

## 14. Field-to-spec traceability matrix

| Field | SRS anchor |
|---|---|
| `transaction_id` | §2.4 (appeal references grade "by its transaction identity"), §5 Traceability of authority, §10 Glossary ("Appended successor") |
| `student_id` | §2.2 W-1 (records attributable), §3.5 (audit trail home), §5 Auditability |
| `educational_level` | §1.3 (literal values), §2.2 W-1, §3.1 |
| `academic_period` | §3.4 (ECS sole owner), §2.2 W-1 (Active gating) |
| `section_id` | §2.3 W-2 step 1 (section named in submission), §3.1 (ESS owns sections) |
| `assessment_id` | §2.3 W-2 step 1 ("the assessment"), §10 Glossary ("Grade record": one record per assessment) |
| `assessment_type` | §2.3 W-2 step 1; §3.1 (ECS rule content governs the kinds) |
| `GoverningRuleSetID` | §2.2 W-1 steps 2–4; §2.3 W-2 steps 2–4 (**MUST carry it**); §2.7 step 1; §4.2 S-3, S-6; §5 Determinism; Q-1 (`WORK-179`) |
| `grade_raw` | §2.3 W-2 step 1 (raw scores), §10 Glossary |
| `grade_final` | §2.3 W-2 steps 3–4 (computed + recorded grade), §10 Glossary, §5 Determinism |
| `max_score` | §2.3 W-2 step 1 (raw scores are measured against a scale) |
| `weight` | §2.3 Formula-ownership annotation (weights are ECS content, application recorded not authored); Appendix A parity with `academic_history[].weight` |
| `achievement_level` | §2.3 Formula-ownership annotation; §3.1 (ECS rule content governs the band set) |
| `submission_timestamp` | §2.3 W-2 step 1; §5 Auditability |
| `status` | §2.9 "Grade record"; §9.1 → `CAP-STATUSENUMS` v1.2; §2.4 W-3 step 5 (direct-`Finalized` successor) |
| `schema_version` | §2.8 property 5 (distinction from canonical-form version, by analogy); `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 |
| `parent_transaction_id` | §2.4 W-3 steps 1, 5–6; §2.9; §10 Glossary ("Appended successor"); §4.2 S-1; Q-2 inherited |
| `change_status` | §2.4 W-3 step 5 ("carries the status flag of the change"); Section 11, C-1 (vocabulary open, owner: change control) |
| `approved_by` | §2.3 W-2 step 4 (approving authority recorded), §5 Traceability of authority, §3.5 |
| `approved_at` | §2.3 W-2 step 4; §5 Auditability |

## 15. Downstream conformance pre-check (AC-8) — procedure for the reviewer

Walk A — GRA-Service W-2 path (submission → recording):

| # | Input required | Field providing it | Expected |
|---|---|---|---|
| A1 | Student, section, assessment, raw scores; period `Active`; rule set from ECS | W-1/W-2 consult; `GoverningRuleSetID` recorded | OK |
| A2 | Computed grade; record created `Proposed` | `grade_final`, `status` | OK |
| A3 | Approver recorded; record `Finalized`; terminal | `approved_by`, `approved_at`, `status` | OK |
| A4 | Grade enters period aggregate with same identity semantics | `GoverningRuleSetID`, Appendix A mapping | OK |
| A5 | Non-`Active` period ⇒ creation refused | W-1 gate; no record exists | OK |

Walk B — W-3 appeal path (appeal → successor → aggregate):

| # | Input required | Field providing it | Expected |
|---|---|---|---|
| B1 | Appeal references grade by transaction identity | `transaction_id` (original) | OK |
| B2 | Append-only: successor created directly in `Finalized`; original untouched | `status`, `parent_transaction_id` | OK |
| B3 | Successor carries the change flag | `change_status` present-iff-parent present; **value vocabulary = AMBIGUOUS per Section 11, C-1 (pre-dispositioned, owner change control)** | AMBIGUOUS — pre-dispositioned, not a failure |
| B4 | Aggregate rebuild selects successor, not original | W-3 step 6; Appendix A | OK |
| B5 | Superseded identifiers still resolve for reproduction | 13.4; 13.8 violation clause | OK |

Per AC-8: **any unlogged MISSING/AMBIGUOUS, or any pre-dispositioned row whose pre-disposition is
not carried in Section 11, blocks Gate 3.** B3 is carried in Section 11 (C-1) and is not a
failure. Results attach to the review evidence log.

## 16. Acceptance note

This contract is additive over the parent SRS: it names fields the SRS's transitions presuppose,
fixes presence rules, and binds attribution. It resolves nothing the SRS leaves to change control
(vocabulary of `change_status`, formats of identities, approval-role semantics, weighting bands)
— those carry explicit owners in Sections 10 and 11. If review or walk-through finds the parent does
not support this contract as written, the remedy is an SRS §11 Change Request, not an edit here.

## 17. Task bookkeeping

Deliverables: this specification (Draft → review → Approved), the calibration run file
`task-LMS-GRADERECORD-001-noncode-calibration.md` (final, 2026-11-19), and the task handoff
`task-LMS-GRADERECORD-001-handoff.md` (created at Gate 3; includes the suggested skill run for
`wf-plan`). No other files are produced by this task. `WORK-196` remains open for the
Session/AttendanceRecord contract.

## Appendix A — Alignment with the `final_academic_record` `academic_history` entry

Ref: normative rendering `schema/final-academic-record.md` (Approved, v1.0.0) and task spec
`WORK-LMS-CONTRACT-001` v1.5. The student-period record's aggregate entries and the operational
`GradeRecord` are the same outcome seen at two boundaries; types and semantics are identical where
mapped.

| `GradeRecord` field | counterpart | Aligned? |
|---|---|---|
| `schema_version` | record-level `schema_version` | Yes — same capability (CAP-SCHEMAVERSIONCONSTRAINT), same MAJOR.MINOR.PATCH semantics, record type's own versioning decision (13.10); record-local to each academic_history entry's parent, i.e. the aggregate as a whole carries one |
| `assessment_id` | entry `assessment_id` | Yes — same opacity, same store uniqueness |
| `assessment_type` | entry `assessment_type` | Yes — ECS-governed set, unconstrained here |
| `section_id` | entry `section_id` | Yes — ESS-owned identity, opaque |
| `grade_raw` | entry `grade_raw` | Yes — number, raw |
| `grade_final` | entry `grade_final` | Yes — string |
| `max_score` | entry `max_score` | Yes — number |
| `weight` | entry `weight` | Yes — applied coefficient, optional both sides, presence decided by the rule set both sides |
| `achievement_level` | entry `achievement_level` | Yes — ECS bands |
| `submission_timestamp` | entry `submission_timestamp` | Yes — CAP-TIMESTAMPFORMAT |
| `GoverningRuleSetID` | record-level `GoverningRuleSetID` | Yes — single record-level value in FAR; per outcome-record here; in an aggregate the entry is assembled from records each carrying it |
| `transaction_id` | — | Record-local (operational identity; not digested, never in the payload) |
| `status` | — | Record-local (`Finalized` is the only state that reaches the aggregate) |
| `parent_transaction_id` | — | Record-local (succession linkage inside the operational store; the FAR payload carries `parent_transaction_id` for student-period supersession only) |
| `change_status` | — | Record-local (Section 11, C-1) |
| `approved_by` / `approved_at` | — | Record-local (FAR digests `authorized_by` at student-period level, not per entry) |
| `student_id` | record-level `student_id` | Yes — identical type (CAP-USERID), identical semantics (record attested to this student) |
| `educational_level` | record-level `educational_level` | Yes — identical enum, identical §1.3 literal values |
| `academic_period` | record-level `academic_period` | Yes — identical semantics (ECS-owned period identity, §3.4) |
