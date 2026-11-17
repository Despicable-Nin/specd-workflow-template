# Reconciliation Report — Blockchain-Enabled LMS

**Project:** blockchain-enabled-lms  
**Date:** 2026-11-17  
**Scope:** All specifications in `spec-workspace/projects/blockchain-enabled-lms/`

---

## Step 1 — Collect specifications

Gathered the following specification files:

| File | Spec ID | Version | Status (per frontmatter) | Status (per AGENTS.md) | Notes |
|------|---------|---------|--------------------------|------------------------|-------|
| `SRS_LMS_v1.0.md` | SRS-LMS-v1.0 | 1.0 | `Approved` | `Draft` (blocked by WORK-016, WORK-032, WORK-039) | Frontmatter says Approved per WORK-039, but project AGENTS.md says nothing is Approved |
| `schema/final-academic-record.md` | SCHEMA-LMS-FAR-v1.0 | 1.0.0 | `Approved` | N/A | Normative rendering; authoritative source: task spec |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | WORK-LMS-CONTRACT-001 | 1.5 | `Approved` | `Draft` (no approval Decision in ledger per WORK-009) | Task spec claims Approved but has no ledger Decision |
| `tasks/task-LMS-CONTRACT-001-handoff.md` | HANDOFF-LMS-CONTRACT-001 | Open | `Open` | Running handoff; disposable | Status: Open |
| `binding.yaml` | — | — | — | Pointers and references | Lists many specs as Approved; codebase_dir: null |
| `service-contracts.yaml` | — | — | — | Runtime manifest | 7 domains; 1 declared, 5 not-yet-specified, 1 unresolved |

---

## Step 2 — Detect duplicate specifications

No two specifications have *identical* scope and objectives. However, the following share the same business capability (final_academic_record contract):

- `schema/final-academic-record.md` — normative rendering
- `tasks/task-LMS-CONTRACT-001-noncode.md` — task specification

**Relationship:** Per project AGENTS.md §3: "Where the two disagree, the task specification wins and the rendering is the defect." This is not a duplicate but an authoritative/rendering relationship.

---

## Step 3 — Detect conflicting specifications

### Conflict 1: SRS frontmatter vs. project AGENTS.md approval status

| Spec | Frontmatter Status | AGENTS.md Status | Evidence |
|------|-------------------|------------------|----------|
| `SRS_LMS_v1.0.md` | `Approved` (line 6) | `Draft` (blocked) | Frontmatter was changed on 2026-11-13 per WORK-039, but the work ledger approval Decision is not properly recorded; project AGENTS.md explicitly states "Nothing in this collection is Approved" and lists WORK-016, WORK-032, WORK-039 as blockers |
| `tasks/task-LMS-CONTRACT-001-noncode.md` | `Approved` (line 4) | `Draft` (no ledger Decision) | Frontmatter says `status: Approved` but project AGENTS.md says "The task spec carries no approval Decision in the work ledger. It was once marked Approved with no body; the body was restored and the status corrected to Draft." |

**Severity:** **Critical** — Conflicts between two "Approved" designations (if we count the frontmatter) and the actual governance state. The SRS and task both claim Approved but neither has a valid approval Decision in the work ledger.

### Conflict 2: Task spec references missing capabilities

The task specification `WORK-LMS-CONTRACT-001` adopts normatively the capability artifacts under `spec-workspace/library/Capabilities/`:
- `CAP-USERID` ✓ (cited)
- `CAP-TIMESTAMPFORMAT` ✓ (cited)
- `CAP-STATUSENUMS` ✓ (cited, but artifact missing — WORK-020)
- `CAP-SCHEMAVERSIONCONSTRAINT` ✓ (cited)
- `CAP-CANONICAL-FORM` ✓ (cited, but artifact missing — WORK-020)

**Evidence:** The task spec's "Dependencies and Sources" section (line 411-414) lists all five capability artifacts. Two of them (CAP-STATUSENUMS, CAP-CANONICAL-FORM) have no defining artifact per the work ledger (WORK-020).

**Severity:** **Critical** — The task claims normative adoption of capabilities that don't exist, creating an impossible dependency.

---

## Step 4 — Detect overlapping requirements

### Overlap 1: Task spec vs. schema rendering

| Artifact | Scope | Relationship |
|----------|-------|-------------|
| `tasks/task-LMS-CONTRACT-001-noncode.md` | Defines the canonical field set, types, cardinalities, nullability, digest fields, encoding, and acceptance criteria for `final_academic_record` | **Authoritative** per project AGENTS.md §3 |
| `schema/final-academic-record.md` | Normative rendering that restates the task spec; must not introduce requirements the task does not authorize | **Defective if it disagrees** — rendering is the defect |

**Evidence of overlap:** Both declare the same 13 fields in the canonical field list, the same encoding (JSON), and the same digest-ready declaration. The schema is a rendering of the task spec, not an independent specification.

**Legitimacy:** This is a **legitimate overlap** — the schema exists to provide a developer-friendly rendering, and the task spec explicitly governs where they disagree. No action needed beyond ensuring the schema stays in sync.

### Overlap 2: SWS capabilities vs. task spec adoption

The SRS §9.1 defines a status vocabulary table (Primary School, Secondary School, College, etc.), and the task spec §9.1 references the same table. The task spec also declares that "The shared `StatusEnums` capability artifact does not yet exist (Q-4); until it does, this table is the authority."

**Legitimacy:** **Legitimate** — the task spec explicitly acknowledges the capability is missing and falls back to the inline table. This is documented as Q-4 and WORK-020.

---

## Step 5 — Identify fragmented specifications

### Fragmentation 1: Task specification version history

The task specification has undergone five version revisions (1.0 through 1.5) in a single day (2026-11-16):

| Version | Date | Primary Change |
|---------|------|----------------|
| 1.0 | 2026-11-11 | Initial task specification |
| 1.1 | 2026-11-13 | Body restored from git blob; ECS rule-authoring boundary added (WORK-066); capability citations added |
| 1.2 | 2026-11-16 | Acceptance criteria replaced with evidence-bearing criteria; §7 rewritten as document-level verification |
| 1.3 | 2026-11-16 | First modelling pass; declared canonical field list and exclusions; added finalized_at, authorized_by, record_state, student_id, canonical_field_list and appeal_record |
| 1.4 | 2026-11-16 | **Correction pass answering all nineteen findings of the sixth independent review.** Removed record envelope, embedded GradeAppealRecord, change_status field, GradeAssessment, enrollment_status, and presence rule R-5. Declared educational_level's three-value domain. Fixed canonical_field_list to 13..13. |
| 1.5 | 2026-11-16 | **Editorial corrections answering the seventh review's six warnings and five infos; no requirement changed.** |

**Assessment:** This is **intentional evolution**, not problematic fragmentation. Each version addresses specific review findings. However, the rapid successive revisions (1.0 → 1.5 in one day) suggest the specification was still settling. The current state (v1.5) is the de facto authority.

### Fragmentation 2: Capability artifacts scattered

Five capability artifacts are referenced across the project:
- `CAP-USERID` — exists (implied by citations)
- `CAP-TIMESTAMPFORMAT` — exists (implied by citations)
- `CAP-STATUSENUMS` — **missing** (WORK-020)
- `CAP-SCHEMAVERSIONCONSTRAINT` — exists (implied by citations)
- `CAP-CANONICAL-FORM` — **missing** (WORK-020)

**Assessment:** The two missing capabilities represent **fragmentation** — the specification depends on them but they are not defined in the tree. This is a candidate for consolidation (create the missing artifacts).

---

## Step 6 — Find outdated or superseded specifications

### Outdated artifact: `tasks/task-LMS-CONTRACT-001-plan.md`

Per `binding.yaml` (line 39-43):
```
- path: tasks/task-LMS-CONTRACT-001-plan.md
  id: PLAN-LMS-CONTRACT-001
  version: 1.0
  status: stale - regenerate from task spec v1.5
  role: Implementation plan - written against v1.2; superseded by v1.5. Not a source of truth until regenerated.
```

**Assessment:** The plan file is **stale** and should be regenerated against the current task spec v1.5. It is referenced in the binding but marked as not being a source of truth.

### Outdated: binding.yaml plan reference

Per binding.yaml line 42: `status: stale - regenerate from task spec v1.5`

**Assessment:** The plan file needs regeneration. This is a candidate for the `wf-plan` skill to regenerate.

---

## Step 7 — Identify missing relationships

### Missing relationship 1: binding.yaml → codebase

Per binding.yaml line 62-65:
```
codebase_dir: null
codebase_dir_status: undetermined
```
**Decision needed:** The codebase directory for this project is not yet determined. Per SRS Section 7 and Question Q-3 (WORK-017, WORK-035), the codebase must be at `generated-projects/blockchain-enabled-lms/` once created, and binding.yaml must be mirrored there.

### Missing relationship 2: task spec → capability artifacts

The task spec `WORK-LMS-CONTRACT-001` references five capability artifacts, but two (CAP-STATUSENUMS, CAP-CANONICAL-FORM) have no defining artifact in `spec-workspace/library/Capabilities/`.

**Evidence:** WORK-020 records this gap. The SRS §9.1 status vocabulary is used as an interim measure.

### Missing relationship 3: work ledger ↔ specification status

- WORK-009: "The task spec carries no approval Decision in the work ledger. It was once marked Approved with no body; the body was restored and the status corrected to Draft."
- WORK-016, WORK-032, WORK-039: Blocking findings on the parent SRS. The SRS frontmatter claims Approved per WORK-039, but the project AGENTS.md says nothing is Approved.
- WORK-130: "The canonical-form rules that CAP-CANONICAL-FORM defines have no owning domain. SRS Question Q-5."

### Missing relationship 4: service-contracts.yaml ↔ domain model

The service-contracts.yaml declares `blockchain-gateway` with `domain: unresolved` and notes "Requires a human decision - see SRS Question Q-6 and ledger WORK-037." No domain in the SRS seven-domain model includes a gateway, yet the service exists in the repository (two candidate directories: `lms-platform/blockchain-proxy`, `lms-platform/web-api-gateway`).

---

## Step 8 — Evaluate architecture and requirement drift

### Drift 1: SRS status vs. governance state

- **What SRS says:** `status: Approved` in frontmatter, with approval anchored to revision SHA `167af69` (2026-11-13 rewrite).
- **What the work ledger says:** WORK-009, WORK-016, WORK-032, WORK-039 blockages; project AGENTS.md says "Nothing in this collection is Approved."
- **Drift direction:** The frontmatter was updated to Approved without the corresponding work ledger Decision, or vice versa. The project AGENTS.md is the authoritative source for this project's governance state.

### Drift 2: Task spec approval vs. work ledger

- **What task spec says:** `status: Approved` (frontmatter line 4)
- **What the project AGENTS.md says:** "The task spec carries no approval Decision in the work ledger. It was once marked Approved with no body; the body was restored and the status corrected to Draft."
- **Drift:** Frontmatter and ledger are out of sync. The AGENTS.md is correct — the task is not Approved until a Decision item is recorded in the work ledger.

### Drift 3: Capability dependency vs. availability

- **What task spec assumes:** All five capability artifacts (CAP-USERID, CAP-TIMESTAMPFORMAT, CAP-STATUSENUMS, CAP-SCHEMAVERSIONCONSTRAINT, CAP-CANONICAL-FORM) are available normatively.
- **Reality:** CAP-STATUSENUMS and CAP-CANONICAL-FORM have no defining artifact (WORK-020).
- **Result:** The task spec has a broken normative dependency.

---

## Step 9 — Produce reconciliation plan

| # | Finding | Category | Recommendation | Rationale | Human Approval Required |
|---|---------|----------|----------------|-----------|------------------------|
| 1 | SRS frontmatter `Approved` vs. AGENTS.md `Draft` with blockers | Conflict (critical) | **Revise frontmatter**: Change `status: Approved` to `status: Draft` until WORK-009, WORK-016, WORK-032, WORK-039 are resolved. Or: **Record approval Decision in work ledger** if the 2026-11-13 rewrite was genuinely reviewed. | The project AGENTS.md is the authoritative governance source for this collection. The frontmatter change on 2026-11-13 was pre-approval drafting per the change control section (SRS §11). | **Yes** — critical conflict between two "Approved" designations |
| 2 | Task spec `Approved` vs. no ledger Decision | Conflict (critical) | **Record approval Decision** in work ledger as a new `WORK-XXX` item, or **correct status to Draft**. Per project AGENTS.md §4: "The task spec carries no approval Decision in the work ledger. It was once marked Approved with no body; the body was restored and the status corrected to Draft." | The AGENTS.md explicitly documents what happened; restoring the status to Draft is the documented path. | **Yes** — critical; human must decide: record Decision or revert status |
| 3 | CAP-STATUSENUMS and CAP-CANONICAL-FORM missing (WORK-020) | Outdated/fragmentation | **Create capability artifacts** under `spec-workspace/library/Capabilities/`. These are reusable, technology-agnostic artifacts required by the task spec. | Without these, the task spec's normative dependencies are broken. Creating them enables the task to move forward. | **Yes** — the agent recommends; the human decides and executes |
| 4 | Stale plan file `tasks/task-LMS-CONTRACT-001-plan.md` | Outdated | **Regenerate plan** via `wf-plan` against task spec v1.5. Per binding.yaml: "status: stale - regenerate from task spec v1.5. Not a source of truth until regenerated." | The plan was written against v1.2 and is superseded by v1.5. Regenerating ensures it's the source of truth for any implementation. | **Yes** — the human must approve the regeneration |
| 5 | Codebase directory undetermined (WORK-017) | Missing relationship | **Decide codebase location** and mirror binding.yaml. Per SRS Section 7 and Q-3: codebase at `generated-projects/blockchain-enabled-lms/`, binding.yaml mirrored there. | Without a codebase, no implementation can proceed. This blocks wf-task-code and wf-implement. | **Yes** — architectural decision; human must decide |
| 6 | blockchain-gateway domain unresolved (service-contracts.yaml) | Missing relationship | **Human decision on Q-6**: Which domain does blockchain-gateway belong to, or is it outside the seven-domain model? Per service-contracts.yaml note: "Requires a human decision - see SRS Question Q-6 and ledger WORK-037." | This is an architectural decision that affects the domain model and runtime bindings. | **Yes** — the human must decide |
| 7 | Schema rendering may diverge from task spec | Overlap (legitimate) | **Monitor for drift**: Ensure schema/final-academic-record.md stays in sync with task spec. Per project AGENTS.md §3: "Where the two disagree, the task specification wins and the rendering is the defect." | The overlap is legitimate as long as the task spec governs. Add a check to the review process. | **No** — overlap is legitimate; document as such |
| 8 | Task spec v1.5 inherits open questions Q-1, Q-2 | Missing relationship | **Address parent questions Q-1, Q-2** through independent parent review. The task spec states: "A child specification cannot close a parent question." | Q-1 (authoritative source for GoverningRuleSetID) and Q-2 (parent_transaction_id format) are parent-owned. The task spec correctly treats them as opaque. | **Yes** — but this flows from #1 and #2 (parent SRS review) |
| 9 | Handoff file open since creation | Status | **Progress handoff**: The handoff is `Open`. Per its content, advance it by recording decisions and actions. | The handoff is the task's running state; keeping it current is required for workflow continuity. | **Yes** — the human should review and update if needed |

---

## Step 10 — Record in work ledger

New `WORK-XXX` items recommended (the agent recommends; the human decides and executes):

| WORK-ID | Type | Status | Source | Description |
|---------|------|--------|--------|-------------|
| WORK-NEW-1 | Decision | proposed | SRS-LMS-v1.0 / WORK-009,WORK-016,WORK-032,WORK-039 | Resolve SRS frontmatter `Approved` vs. AGENTS.md `Draft` status. Options: (a) record approval Decision for the 2026-11-13 rewrite, or (b) change frontmatter to `Draft` and address blocking findings. |
| WORK-NEW-2 | Decision | proposed | WORK-LMS-CONTRACT-001 | Record approval Decision in work ledger for task spec, or correct status to Draft per project AGENTS.md §4. |
| WORK-NEW-3 | Task | proposed | CAP-STATUSENUMS, CAP-CANONICAL-FORM | Create missing capability artifacts under `spec-workspace/library/Capabilities/`. |
| WORK-NEW-4 | Decision | proposed | PLAN-LMS-CONTRACT-001 | Regenerate task plan via `wf-plan` against task spec v1.5. |
| WORK-NEW-5 | Decision | proposed | SPEC-LMS-v1.0 / codebase_dir | Decide codebase directory location and mirror binding.yaml. |
| WORK-NEW-6 | Decision | proposed | blockchain-gateway / Q-6 | Decide domain for blockchain-gateway service, or confirm it is outside the seven-domain model. |

---

## Step 11 — Present report and handoff

### Critical findings highlighted

1. **SRS Approved status conflict (WORK-039 vs. AGENTS.md blockers):** The SRS frontmatter claims Approved but the project AGENTS.md explicitly states nothing is Approved, with four blocking work ledger items (WORK-016, WORK-032, WORK-039, and implicitly WORK-009). This is a **critical** conflict because both the SRS and the task spec derive their authority from this parent's approval status.

2. **Task spec Approved status conflict (WORK-009):** The task specification claims `status: Approved` but has no approval Decision in the work ledger. The project AGENTS.md documents exactly what happened: the status was once marked Approved with no body, the body was restored, and the status was corrected to Draft. The task remains Draft until a Decision is recorded.

3. **Missing capability artifacts (WORK-020):** Two of five normative capability artifacts (CAP-STATUSENUMS, CAP-CANONICAL-FORM) have no defining definition. The task spec depends on them but they don't exist.

### Recommended next steps (human decisions required)

1. **First:** Run `@wf-review` against `SRS_LMS_v1.0.md` — the parent specification must be reviewed and approved (or confirmed as Draft) before anything downstream can be approved.

2. **Second:** After the parent is resolved, record the approval Decision for the task spec (or keep it Draft) and close the blocking findings.

3. **Third:** Create the missing capability artifacts (CAP-STATUSENUMS, CAP-CANONICAL-FORM).

4. **Fourth:** Regenerate the task plan via `wf-plan` against the approved task spec.

5. **Fifth:** Decide the codebase directory location (WORK-017) and mirror binding.yaml.

6. **Sixth:** Resolve the blockchain-gateway domain question (Q-6 / WORK-037).

### Handoff requirements

- Reconciliation report summary presented above
- Critical findings (SRS status conflict, task spec status conflict, missing capabilities) highlighted
- Recommended actions with rationale (above)
- **Next step:** Human decisions on each recommendation, starting with `@wf-review` against `SRS_LMS_v1.0.md`