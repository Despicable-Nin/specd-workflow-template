---
task_id: WORK-LMS-FORMULARULES-001
version: 1.2
status: Approved
project: blockchain-enabled-lms
parent_spec: SRS-LMS-v1.0
parent_spec_version: 1.3
task_type: noncode
calibration_file: task-LMS-FORMULARULES-001-noncode-calibration.md
created: 2026-11-19T13:28:01Z
updated: 2026-11-19T13:49:10Z
---

# Task Specification — `FormulaRules`, the ECS grade-configuration contract

`WORK-LMS-FORMULARULES-001` · non-coding task · parent: `SRS-LMS-v1.0` **v1.3** (`Approved`, Gate 2 `WORK-192`) · calibration: `CALIBRATION-LMS-FORMULARULES-001` (Gate 1 final, 2026-11-19)

> **Revision note (v1.2).** Second review (verdict CHANGES REQUIRED; C-1, M-1…M-4, minors)
> dispositioned in this revision: C-1 — 13.5 no longer bans GRA-Service from interpreting the
> payload; opacity is rescoped to non-computing consumers/validators, and a normative binding
> sentence binds `attendance_aggregate` to the ESS aggregate under the ECS-versioned payload
> definition; M-1 — `educational_level` adopted verbatim from SRS §1.3; M-2 — AC-4 tokenizer defined
> (standalone numeric literals only; cross-reference tokens excluded), §3 example digit-free; M-3 — 13.8 re-titled, enforcement boundaries
> assigned per code, `rule_set_not_found` scoped to "never existed / unresolvable in any scope";
> M-4 — B4 rephrased to ECS-versioned-definition equivalence; minors (i)–(vi) applied (supersession
> chain semantics, label omission convention, CONST-LMS tension item 6 caveat added to §11, §4.2
> anchors fixed in §14, CAP-USERID cited to SRS §5 Auditability with group-authority note,
> `academic_period_ref` correctly scoped to the governed period); 13.2 conventions line added.

> **Revision note (v1.1).** Independent review 2026-11-19 (verdict CHANGES REQUIRED; F-01…F-11)
> is fully dispositioned in this revision: the inline contract landed (Section 13), refusal is
> restricted to in-force resolution with historical reproduction preserved (F-02, Section 13.8),
> the inherited SRS Q-1 caveat is carried (F-03, Section 11), the `service-contracts.yaml`
> criterion now encodes the named-component rule (F-04, AC-9), the downstream pre-check is
> executable (F-05/F-11, AC-8), citations corrected (F-07, S-3/S-6 are §4.2), open questions carry
> owners (F-08), and §0/§12 wording tightened (F-06, F-10).

## 0. Plain-language summary (for registrar / academic-office readers)

This document defines the *shape* of the school's grade formula rule book — the thing the
Educational Context Service (ECS) hands to the grading service so it can compute a student's final
grade the same way every time. It does **not** contain the rule book. The actual rules — how
components of the final grade are combined — are written and owned by ECS; this contract only
fixes how a rule book is identified, structured, versioned, attributed, and trusted. Think of it
as the format of the registrar's policy binder, not the policy inside it.

If you only read one sentence: **the formula's weights are not here and never will be; this
document makes the formula deterministic, attributable, and reproducible.**

## 1. Background and ownership

The LMS computes final grades under a "governing formula". The SRS (v1.3, §2.3 Workflow W-2 and the
Formula-ownership annotation; §3.1) assigns that formula to **ECS** — the rule authority. GRA-Service,
not ECS, performs the computation (capability C-6). The SRS requires:

- the governing rule set to be **identified by an identifier** that a finalized grade carries
  (§2.3 W-2 step 3–4; §2.2 W-1 step 4) — the success criteria that demand this are S-3 and S-6
  (SRS §4.2);
- the rules to be consultable **before** any critical state change (§3.2 closed consumer set);
- computation to be **deterministic given the same rule set** (§5 Determinism);
- **refusal over ambiguity** — when a rule set cannot be resolved, the operation is refused, not
  completed under an assumption (§5 Refusal over ambiguity; the W-1 step 3 refusal path).

Today the SRS names `FormulaRules` as an ECS-owned operational record (§3.1) but defines no
field-level contract for it. That gap is what this task closes, at the same altitude as
`WORK-LMS-CONTRACT-001` did for the finalized record.

## 2. In scope

- The inline, field-level, technology-agnostic contract for the `FormulaRules` record type
  (Section 13): envelope fields, types, cardinality, nullability, constraints, semantics, and the
  rules by which a rule-set identifier is minted and resolves.
- The contract's **relationship to the governing rule set identifier**: what it identifies, its
  stability requirements, and what consumers (GRA-Service; domains allowed by §3.2) may assume.
- **Versioning and supersession** of rule sets: how a rule set is superseded for future periods
  without altering — or denying resolution of — historical rule sets.
- **Validation boundaries**: which guarantees are contract-level and which are ECS runtime concerns
  (Section 13.9).
- A recorded decision on the **`service-contracts.yaml` ECS binding** (choice 5): whether the
  `ecs` row moves to `declared` — permitted only against the named-component rule in AC-9 — or
  stays `not-yet-specified` with a written rationale.
- A **downstream conformance pre-check** (choice 3, executable): Walk A (GRA-Service W-2) and
  Walk B (ESS→GRA-Service attendance-aggregate path).

## 3. Out of scope (explicit non-goals)

- **Formula content of any kind.** No weights, no thresholds, no aggregation rules (e.g. which
  attendance outcomes count toward presence), no pass/fail rules, no concrete component
  percentages. The SRS (v1.3) prohibits tasks from authoring ECS rule content; this task honours that.
- **ECS implementation.** Services, stores, persistence, APIs, deployment topology — none of it.
- **Editing the SRS, constitution, CAP artifacts, or the existing `final_academic_record` contract.**
- **Coding.** Any slice that requires code spawns a separate coding task via `wf-task-code`.
- **Rule-set retention policy** — constitution tension 1; a Decision is owed separately.
- **Attendance contract, `GradeRecord` contract** — separate tasks (`WORK-196` partially).
- **Defining a lifecycle state machine for rule sets** unless independent review finds one is
  required; if so, a follow-on task or Section 11 CR is raised rather than this contract inventing one.
- **A numeric totals-invariant on component weights** (e.g. a "components sum to unity" rule) —
  that is formula policy, not shape.

## 4. Expected behavior (technology-agnostic)

Given an educational level and an academic period, a consumer requests ECS; ECS returns the
governing rule-set identifier and the rules it contains. For this contract to be implementable:

1. **Resolution determinism.** The same (level, period) resolved twice, with no intervening
   rule-set change in force, yields the same identifier and the same complete rules.
2. **Identifier sufficiency.** The identifier alone is sufficient to reproduce the computation of
   a grade produced under it (SRS §5 Determinism). The contract fixes opacity, uniqueness scope and
   stability — never a formatted structure.
3. **Completeness.** The rules payload contains everything required to compute the final grade
   (including the component structure and any reference to an attendance component) and nothing it
   does not.
4. **Approval chain.** The rules reference, by opaque reference, the approval chain required for
   the level (SRS §3.1 ECS operations). The reference travels **by reference, not embedded** — a
   recorded decision (Section 13.6), not an ambiguity.
5. **Refusal, scoped.** An unknown, malformed, ambiguous, or unsupported-`schema_version`
   rule-set request MUST be refused. Superseded identifiers MUST remain resolvable for
   reproduction of historical grades (S-3; W-3 appeal recomputation under the original rule set);
   refusal applies to **in-force resolution only** — a superseded rule set is never refused as
   "unknown", and a supersession never silently substitutes the in-force set during reproduction.
6. **Attribution.** A rule set carries who authored and who approved it and when, per the
   capability adoptions recorded in Section 7 — with `CAP-USERID` mandatory. SRS §5 (Auditability)
   is the governing quality expectation: every state change attributable to an actor and an
   authorization.
7. **Time and supersession semantics.** Rule sets take effect for a period and are superseded only
   forward-looking; originals are never altered (SRS §2.4/§2.9 posture, applied to configuration);
   superseded rule sets remain resolvable for reproduction.

## 5. Acceptance criteria (measurable; non-code deliverables)

| # | Criterion | How it is verified |
|---|-----------|--------------------|
| AC-1 | Task spec exists at `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-FORMULARULES-001-noncode.md` with `status: Approved` and `task_type: noncode` before `wf-plan` runs. | Path + frontmatter inspection |
| AC-2 | Every field of `FormulaRules` (Section 13.2) defined with type, cardinality, nullability and normative semantics; the identifier field defined with opacity/uniqueness/stability rules (13.4). | Reviewer field-by-field check |
| AC-3 | Determinism is stated as a contract guarantee: identical (level, period) + unchanged in-force rule set ⇒ identical identifier and rules, with a written stability clause (13.4). | Reviewer reads the stability clause |
| AC-4 | **No formula content.** The spec contains no numeric weights, no thresholds, no component percentages, no pass/fail cutoffs. Check: word-tokenizer scan of normative sections (Section 13, Section 14 and Section 15 prose; §0 is glossaried plain language and excluded; Section 3 out-of-scope examples excluded by path) for **standalone numeric literals** (digit-only tokens) within 10 word-tokens of any of `weight`, `weights`, `percentage`, `threshold`, `cutoff`; zero hits required. Excluded from the digit class: (i) cross-reference tokens (`§13.5`-style section references, `P-12`, `S-3`, `AC-4`, `W-2`, `WORK-*` identifiers, dated timestamps); (ii) bare dotted section references (`13.5`-style), treated as one excluded token; (iii) table-cell cardinality digits in the §13.2/§13.3 field tables (`0`, `1`, `0..1`, `1..n` between cell pipes). | Precise word-tokenizer per this definition at review |
| AC-5 | Traceability matrix (Section 14) present: every contract field cites an SRS anchor; "no field cites nothing" is the rule — §2.2, §2.3, §2.9, §3.1, §3.2, §4.2, §5, §6, §9.1 are examples, not an exhaustive mandate. | Reviewer checks the matrix |
| AC-6 | Ownership clause recorded (13.1): ECS is the sole authority over rule content; consumers may read, never write; no ECS-owned contract, task, or code may author weights/thresholds. | Reviewer confirms clause + SRS citations |
| AC-7 | Capability adoption table (Section 7) present: each capability adopted/declined with rationale and version pin. | Reviewer vs `library/Capabilities/` |
| AC-8 | **Downstream conformance pre-check** (choice 3) executed before Gate 3, per Section 15: Walk A (GRA-Service W-2, A1–A4) and Walk B (ESS→GRA-Service attendance path, B1–B4), logged as `step \| input required \| field providing it \| OK/MISSING/AMBIGUOUS`; any MISSING/AMBIGUOUS blocks Gate 3 until resolved. The `GradeRecord` identifier-carry path is checked inside Walk A (A3), not as a separate walk — recorded exclusion rationale, addressing F-11. Results attach to review evidence. | Pre-check log attached to review |
| AC-9 | `service-contracts.yaml` decision recorded and applied per choice 5: row flips to `declared` **only if** a named component with `provides`/`requires` is recorded in the manifest (consistent with how the existing `declared` rows read); otherwise it stays `not-yet-specified` with a written rationale. Either way a ledger Decision is recorded; no runtime binding is invented. | Manifest diff or rationale + ledger Decision |
| AC-10 | Plain-language summary (Section 0) present and readable by a non-technical registrar audience; no jargon without gloss. | Reviewer read-through with a registrar-reader note |
| AC-11 | Technology-agnostic: no language, storage engine, framework, protocol or vendor named. Reviewer greps against a stated marker list (languages, DBMS, cloud vendors, frameworks, protocols). | Automated grep with marker list |
| AC-12 | Refusal clause present and correctly scoped (13.8): refusal applies to in-force resolution (unknown / malformed / ambiguous / unsupported `schema_version`) and carries a legible reason code; historical rule-set identifiers MUST resolve for reproduction — refusal there is a contract violation. | Reviewer confirms scope + reason codes |
| AC-13 | Validation boundary table (13.9) present: each guarantee labelled **contract-level** (any conforming validator) or **ECS runtime** (service-time); table is exhaustive over AC-2's field constraints. | Reviewer cross-checks exhaustiveness |

## 6. Verification requirements

- **Independent review** (`wf-review`) on this Draft; findings with evidence, severity, location,
  reasoning, resolution. Minimum bar: zero Critical, zero Major unresolved.
- **Downstream conformance pre-check** executed and logged (AC-8, Section 15) before Gate 3.
- **Gate 3** (explicit human approval) before the spec is `Approved`; approval recorded as a ledger
  `Decision`.
- Evidence pack: review findings, spec frontmatter, the service-contracts.yaml diff (or recorded
  rationale), ledger Decision id, pre-check log.

## 7. Reusable capabilities adopted

| Capability | Version | Disposition | Rationale |
|---|---|---|---|
| `CAP-TIMESTAMPFORMAT` | v1.1 | **ADOPT** | Effective/mint/supersession timestamps on rule sets (ISO 8601 extended). |
| `CAP-SCHEMAVERSIONCONSTRAINT` | v1.1 | **ADOPT** | `schema_version` on the record; rejection rule applies; per-segment semantics are this contract's own decision (13.10). |
| `CAP-USERID` | v1.1 | **ADOPT** | Attribution references (`minted_by` / `approved_by`) — mandatory fields; format governed by this capability. Group/authority (non-person) identities are an ECS/domain decision; the capability's opaque-string format applies unchanged. |
| `CAP-STATUSENUMS` | v1.2 | **DECLINE** | SRS grants ECS rule-authority; no lifecycle state is authorised for rule sets here. If review finds one is required: separate task or Section 11 CR. |
| `CAP-CANONICAL-FORM` | v1.0 | **DECLINE** | Rule sets are never proof-committed; no digest is computed over them (SRS §2.8). |

## 8. Dependencies

- `SRS-LMS-v1.0` **v1.3** (parent) — §2.2 W-1, §2.3 W-2 (Formula-ownership note), §2.8, §2.10,
  §3.1 (ECS `FormulaRules` ownership), §3.2 (closed ECS-consumer set), §3.5, §4.2 (S-3, S-6),
  §5 (determinism, refusal), §6 (domains are contracts, not deployment boundaries), §9.1.
- `WORK-LMS-CONTRACT-001` v1.5 + render `SCHEMA-LMS-FAR-v1.0` — authoring pattern; its
  `final_academic_record` carries the governing rule-set identifier this contract resolves.
- Constitution `CONST-LMS-v1.3` — P-3/P-4 (rule authority, attribution), P-12 (cross-domain via
  operation calls only).
- Ledger `WORK-179` / `WORK-182` — SRS Q-1 status (Section 11, inherited questions).
- Ledger `WORK-196` — this task discharges one of the three missing contracts.

## 9. Consistency note (alignment with the parent spec)

This task supports the `FormulaRules` slice of SRS capability C-2 ("Determine the rules in force")
and the ECS-owned record mandated by §3.1. It authorises no ECS behaviour beyond §3.1 and §2.3; it
defines the shape of ECS's own operational record; it never dictates how ECS resolves rules at
runtime. Where this contract and the SRS disagree, the SRS governs (contract defect). Where this
contract is silent, the SRS governs. The attendance-aggregate formula path (SRS §2.10/W-7)
consumes this contract once Approved.

## 10. Open questions (with owners — recorded, not resolved here)

1. Rule-set lifecycle states (if any) — owner: ECS domain owners; route: separate task or Section 11 CR.
2. Identifier opacity vs structured form — recommendation: opaque non-empty string (consistent with
   the v1.5 `parent_transaction_id` treatment); decision: reviewer + Gate 3.
3. Approval chain: **decided in this spec — by reference, not embedded** (13.6). Revisit only via
   review or change.
4. `service-contracts.yaml` `ecs` flip (AC-9) — owner: this task + reviewer; decision recorded per AC-9.
5. Retention of superseded rule sets — owner: project (constitution tension 1); Decision owed separately.
6. Whether attribution fields are mandatory (decided: mandatory, 13.2) — no longer open; retained for traceability of the v1.1 revision.
7. `calculation_body` opacity boundary (13.5): is any structural constraint required inside the
   opaque payload beyond the envelope? — owner: ECS/GRA-Service owners; gate: review/Gate 3.

## 11. Inherited questions (from the parent SRS — binding caveat)

- **SRS Q-1 — rule-set identifier source (open in the parent).** Resolved *in substance*
  2026-11-19 by Decision `WORK-179`: ECS mints and owns `GoverningRuleSetID`; GRA-Service records
  it. Formal SRS annotation is pending `WORK-182` (proposed). This contract treats ECS as sole
  minter. **If `WORK-182` resolves differently, this contract is a defect and is revised via the
  same change-control discipline as any approved spec.** Approval of this contract is sought under
  that caveat.
- **SRS Q-2 — `parent_transaction_id` format (open in the parent).** Not inherited by this contract;
  recorded so the dependency graph is explicit. The attendance parent reference (SRS §2.10) is
  likewise out of scope here.
- **Constitution Open tensions, item 6 — rule-set identifier source (open in the constitution as
  of CONST-LMS-v1.3).** The constitution still lists Q-1 as open; `WORK-179` resolved it in substance
  and `WORK-182` (proposed) annotates the SRS; a constitution v1.4 (`WORK-181`, proposed) is pending.
  This contract's minter clause follows `WORK-179` and carries the same caveat: if the formal
  annotations resolve differently, this contract is revised via change control.

## 12. Risks

- **Fossilization of the formula shape.** Mitigation: AC-4; reviewer watches for smuggling.
- **Over-declaration.** Mitigation: completeness scoped to grade computation inputs.
- **`service-contracts.yaml` scope creep.** Mitigation: named-component rule (AC-9).
- **Cross-contract skew.** Mitigation: AC-8 pre-check.
- **Q-1 annotation divergence.** Mitigation: Section 11 caveat.
- **Immutability drift.** Mitigation: 13.7 supersession rule — originals never mutated.

---

## 13. The `FormulaRules` contract (normative deliverable)

Status vocabulary and transitions for `AttendanceRecord` and records with lifecycle states are out
of scope here; `FormulaRules` carries no lifecycle state (supersession only, Section 13.7). The
identification of the rule set is by its identifier; consumers never re-derive it.

### 13.1 Ownership

`FormulaRules` is **ECS-owned operational configuration** (SRS §3.1). ECS is the sole authority
over its content. Consumers (domains in the §3.2 closed set; GRA-Service under §2.3) read via ECS
operation calls only (SRS §6 boundary rule; P-12). No ECS-owned contract, task, or code may author
weights, thresholds, component percentages or aggregation semantics. This contract, like
`WORK-LMS-CONTRACT-001` for the finalized record, fixes shape only.

### 13.2 Record fields (normative)

Conventions: a 0..1 field is **omitted** when not applicable; no field carries a null value.

| # | Field | Type / format | Card. | Null? | Normative semantics |
|---|-------|---------------|-------|-------|---------------------|
| 1 | `rule_set_id` | opaque non-empty string (CAP-USERID-style opacity; no internal structure) | 1 | No | The governing rule-set identifier. Minted exclusively by ECS (SRS §2.2 W-1 step 4; W-2 step 3). Globally unique across all time; never reused; immutable once minted; sufficient to reproduce the computation of any grade produced under it (SRS §5). |
| 2 | `educational_level` | enum: `Primary School` \| `Secondary School` \| `College` | 1 | No | The level this rule set governs (SRS §1.3 literal values). |
| 3 | `academic_period_ref` | opaque reference | 1 | No | Reference to the academic period the rule set governs; resolvable only via ECS period operations (SRS §3.1, §3.4). Not an embedded copy of the period record; a historical rule set references the period it governed. |
| 4 | `schema_version` | `MAJOR.MINOR.PATCH` (CAP-SCHEMAVERSIONCONSTRAINT v1.1) | 1 | No | Presence + format conforming to that capability; unsupported MAJOR ⇒ rejection (Section 13.8). Per-segment semantics are this contract's own decision (13.10). |
| 5 | `minted_by` | `UserID` (CAP-USERID v1.1) | 1 | No | Attribution of the actor who minted the rule set (audit home SRS §3.5). |
| 6 | `approved_by` | `UserID` (CAP-USERID v1.1) | 1 | No | Attribution of the approving authority for the level and period (ECS approval chain, §3.1). |
| 7 | `minted_at` | ISO 8601 extended timestamp (CAP-TIMESTAMPFORMAT v1.1) | 1 | No | Minting time; used for audit, never for in-force selection. |
| 8 | `approved_at` | ISO 8601 extended timestamp (CAP-TIMESTAMPFORMAT v1.1) | 1 | No | Approval time; must be ≥ `minted_at`. |
| 9 | `effective_from` | ISO 8601 extended timestamp (CAP-TIMESTAMPFORMAT v1.1) | 1 | No | When the rule set takes effect for its period. |
| 10 | `supersedes` | opaque non-empty string (a prior `rule_set_id`) | 0..1 | No | Forward-looking supersession link; links to the **immediate predecessor only**; originals are never altered (13.7). Absent ⇒ the rule set is the original of a sequence. |
| 11 | `components` | ordered list of component descriptors (13.3) | 1..n | No | The component structure of the governing formula. Structural envelope only; semantics and values are ECS content. |
| 12 | `approval_chain_ref` | opaque reference | 1 | No | **By reference, not embedded** (recorded decision, 13.6): resolves via ECS to the approval chain required for the level (SRS §3.1). |
| 13 | `calculation_body` | opaque structured payload (ECS-defined) | 1 | No | The ECS-owned content of the rules (weights, aggregation semantics, thresholds), delivered to consumers **as an ECS-defined, `schema_version`-gated structure**. GRA-Service applies it only as such a structure (13.5); reliance on undocumented internals or unversioned change is non-conforming. Validators and non-computing consumers enforce/check only the envelope (13.5, 13.9). |

### 13.3 Component descriptor (element of `components`)

| # | Field | Type / format | Card. | Null? | Semantics |
|---|-------|---------------|-------|-------|-----------|
| 11.1 | `component_id` | opaque non-empty string; unique within the rule set | 1 | No | Stable identity of the component; referenced by `calculation_body`. |
| 11.2 | `kind` | enum: `assessment_result` \| `attendance_aggregate` | 1 | No | Structural input type. `attendance_aggregate` marks the component that consumes the ESS attendance aggregate (SRS §2.10/W-7; GRA-Service obtains the value from ESS under W-2). Component **names and counts are ECS content**, not defined here. |
| 11.3 | `label` | descriptive string | 0..1 | No | Human-readable tag for registrar display, omitted when absent; no normative weight. |

No component descriptor carries a weight, a threshold, an aggregation function, or a cutoff. Those
live only inside `calculation_body` (13.5), ECS-owned.

### 13.4 Stability and resolution semantics

- A rule-set identifier is **globally unique across all time** and never re-minted.
- A rule set is **immutable** after minting; a correction for future periods is a new rule set
  carrying `supersedes` (13.7).
- Given (level, period) and no intervening supersession in force, resolution is **deterministic**:
  same identifier, same rules (SRS §5).
- Consumers MUST resolve rule sets exclusively via ECS operations (SRS §3.1); no caching bypasses
  resolution guarantees required for W-1 gatekeeping.

### 13.5 Opacity boundary of `calculation_body`

Opacity binds **validators and non-computing consumers** — they inspect only the envelope (field
presence, types, non-emptiness, ordering) and never interpret payload internals. Opacity does **not**
bind GRA-Service: it applies the payload as an **ECS-defined, `schema_version`-gated structure**
(13.10), exactly as SRS §2.3 W-2 step 3 requires. What is non-conforming is relying on undocumented
internals or on changes not delivered through `schema_version`; reliance on the documented, versioned
payload is the intended consumption path.

**Normative binding sentence (consumption).** An `attendance_aggregate` descriptor (13.3) binds,
under the ECS-versioned payload definition, to the ESS attendance aggregate (SRS §3.1 ESS operation;
SRS §2.10/W-7; GRA-Service obtains the value under W-2); GRA-Service consumes that aggregate
against this descriptor. The payload's weight math is not replicated or re-derived by any other
domain. Cross-version drift is impossible within a `schema_version` MAJOR and rejected across
MAJORs (13.10).

### 13.6 Approval chain: by reference (recorded decision)

`approval_chain_ref` is an opaque reference resolved through ECS on demand; the chain itself is
not embedded in the rule set. Rationale: (i) the chain is itself ECS-owned and period-specific;
embedding would duplicate and fossilize it; (ii) S-3/S-6 attribution requirements are met by the
reference plus `minted_by`/`approved_by`; (iii) §6 boundary rule favours operations over copies.
Revisit only through review.

### 13.7 Supersession and migration

- Rule sets are superseded **forward-looking only**. A superseding set carries `supersedes` →
  prior `rule_set_id` — **its immediate predecessor only**; transitive history is expressed by
  chaining (A → B → C), never by skipping (A → C is invalid). Originals are never altered.
- **Superseded rule sets remain resolvable** for reproduction of historical grades (S-3; W-3
  appeal recomputation). "Superseded" is **not** a refusal state; there is no `Superseded` status.
- At most one rule set is **in force** per (level, period); that invariant is ECS runtime to
  guarantee, stated here because S-3 and W-2 depend on it.
- Retention of superseded rule sets: constitution tension 1; Decision owed separately (Section 10.5).

### 13.8 Refusal vocabulary (defined contract-wide; enforced at the stated boundary)

The codes below are defined here for vocabulary uniformity; the enforcing boundary of each code is
column 3, and 13.9 must remain exhaustive to match it.

| Condition | Refusal reason code | Enforced at |
|---|---|---|
| Malformed request (level/period absent or unparseable) | `rule_set_request_malformed` | Contract-level (any conforming validator) |
| Identifier unknown — never existed, unresolvable in **any** scope | `rule_set_not_found` | Contract-level (definition); ECS runtime (detection) |
| `schema_version` MAJOR unsupported by the validator | `schema_version_unsupported` | Contract-level |
| More than one rule set in force for (level, period) — integrity failure | `rule_set_in_force_ambiguous` | ECS runtime |

…all four MUST produce a legible reason code (P-1; no silent fallback). **Historical identifiers**
MUST resolve for reproduction; refusing one because it is superseded is a **contract violation**,
and `rule_set_not_found` never applies to a superseded identifier that exists in scope.

### 13.9 Validation boundaries

| Guarantee | Enforced at |
|---|---|
| Required fields present; non-empty; `schema_version` format per CAP-SCHEMAVERSIONCONSTRAINT; unsupported MAJOR rejected | **Contract-level** (any conforming validator) |
| Identifier opacity, uniqueness scope (this contract), immutability after mint (this contract) | **Contract-level** (mint + post-mint immutability checks) |
| Timestamp formats per CAP-TIMESTAMPFORMAT; `approved_at` ≥ `minted_at` | **Contract-level** |
| Attribution presence and `UserID` format per CAP-USERID | **Contract-level** |
| `component_id` uniqueness within the rule set; `components` 1..n; kinds within the enum | **Contract-level** |
| In-force selection; Active-period gating; runtime refusal detection (`rule_set_not_found`, `rule_set_in_force_ambiguous`); approval-chain resolution; attendance-aggregate availability; supersession handling | **ECS runtime** |
| `calculation_body` internal semantics | **ECS runtime only** (opaque to validators; applied by GRA-Service as a versioned structure, 13.5) |

### 13.10 `schema_version` per-segment semantics (this contract's own decision)

| Segment | Meaning | Validator behavior |
|---|---|---|
| MAJOR | Breaking change to the **envelope or the opacity boundary** (consumer-incompatible) | Unsupported MAJOR ⇒ reject (`schema_version_unsupported`) — computation MAY differ only across a MAJOR bump |
| MINOR | Additive envelope extensions (new optional fields) — additions MUST be **semantically inert for computation** (no change to how any grade is computed) | Accept; ignore unknown fields per CAP-SCHEMAVERSIONCONSTRAINT |
| PATCH | Editorial/clarification only; no structural change | Accept |

## 14. Field-to-spec traceability matrix

| Field | Type of anchor | SRS anchor |
|---|---|---|
| `rule_set_id` | record-carrying identifier | §2.2 W-1 step 4, §2.3 W-2 steps 3–4, §4.2 S-3/S-6, §5 Determinism, §3.1 |
| `educational_level` | level domain | §1.3, §2.2 |
| `academic_period_ref` | period reference | §2.2, §2.9 (academic period states), §3.4 |
| `schema_version` | versioning | §3.1, §13.10, `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 |
| `minted_by` / `approved_by` / timestamps | attribution | §3.5, §5 (attribution), CAP-USERID/CAP-TIMESTAMPFORMAT |
| `effective_from` | time semantics | §2.2, §2.9 |
| `supersedes` | supersession | §2.4 (append-only posture), §2.9 (supersession analogue), §2.2 W-1 |
| `components` / `kind: attendance_aggregate` | structure + consumer link | §2.3 (W-2 attendance input), §2.10/W-7, §3.1 (ECS/ESS/GRA-Service) |
| `approval_chain_ref` | approval chain | §3.1 (ECS operations), §2.9 (approval chain governs transitions), §4.2 S-6 |
| `calculation_body` | opaque payload | §6 (boundary rule), 13.5 |
| Refusal codes (13.8) | refusal posture | §5 Refusal over ambiguity, §2.2 step 3 |
| §3 cross-domain access | operation calls | §3.2, §6 |

## 15. Downstream conformance pre-check (AC-8) — procedure for the reviewer

Prerequisite: Section 13 read. Method: two paper walks, logged as a table with columns
`step | input required | field providing it | status (OK/MISSING/AMBIGUOUS)`; any non-OK blocks Gate 3.

**Walk A — GRA-Service W-2 (grade computation consumption)**
- A1. Request (level, period) → ECS returns identifier + rules; every response element maps to a
  declared field (`rule_set_id`, `components`, `calculation_body`, …).
- A2. Computation-input completeness: component structure resolves; an `attendance_aggregate` kind,
  if present, is consumable; attribution present; nothing referenced that lacks a field.
- A3. Identifier carry: identifier recorded on the grade record at approval (W-2 step 4) and still
  present at student-period close (W-6); opacity preserved; never re-minted (S-3/S-6).
- A4. Supersession replay: resolve an intentionally superseded identifier — must return the
  historical rules, not refuse, not substitute (13.8).

**Walk B — ESS→GRA-Service (attendance aggregate formula path)**
- B1. ESS requests governing context (W-7 step 1); Active gating behaves; refusal for non-Active.
- B2. The formula's attendance component is identified via `kind: attendance_aggregate`; the
  aggregate computation itself is ECS content (out of scope) — only the carrier's shape is checked.
- B3. GRA-Service obtains the student's aggregate from ESS (SRS §2.10 step 5) and matches it to the
  attendance component — semantics align, no field is undefined.
- B4. Determinism: two resolutions of the same (level, period) under the unchanged in-force set
  yield rule payloads identical **under the ECS-versioned payload definition** (`schema_version`),
  not byte-identical bytes (no record encoding is designated by this contract).

Exclusion rationale (F-11): a separate `GradeRecord` walk is subsumed by A3/A4 (the identifier
carry and the reproduction contract). No additional walk is defined.

## 16. Acceptance note

This document is the **deliverable**; no implementation follows under this task. Coding slices
(ECS authority service; GRA-Service consumption) are separate `wf-task-code` tasks raised after
this contract is Approved and after the `Session`/`AttendanceRecord` and `GradeRecord` contracts
exist as their own tickets.

## 17. Task bookkeeping

- Task id: `WORK-LMS-FORMULARULES-001` · type: noncode · calibration: `CALIBRATION-LMS-FORMULARULES-001`
- Worktree plan (preferences, choice 4): **in-repo** worktree under `.worktrees/<task-slug>`, branch
  `task/WORK-LMS-FORMULARULES-001-plan` (exact slug finalized at `wf-plan`), base `main`. `wf-plan`
  creates the worktree; this skill does not.
- Handoff: `task-LMS-FORMULARULES-001-handoff.md` (created/finalized at Gate 3 and refreshed at
  `wf-plan`).
- This spec supports SRS capability C-2 and §3.1 `FormulaRules`; it does not create a new artifact
  authority — the SRS remains the parent and governs on any conflict.
- **Approval (Gate 3).** Approved by the user at the 2026-11-19 Gate 3 question prompt; recorded as
  ledger Decision `WORK-198`. Review trail: three passes — 2026-11-19 CHANGES REQUIRED (F-01…F-11),
  2026-11-19 CHANGES REQUIRED (C-1 critical, M-1…M-4, minors), 2026-11-19 APPROVED WITH COMMENTS
  (comments: revision-note traceability nit only). AC-8 executed by the reviewer on v1.2 text: all
  eight steps OK. v1.2 is the approved revision; `version: 1.2`, `status: Approved`, updated
  2026-11-19T13:49:10Z.
