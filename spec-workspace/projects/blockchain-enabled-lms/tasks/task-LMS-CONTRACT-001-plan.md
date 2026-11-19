---
skill: wf-plan
task_id: WORK-LMS-CONTRACT-001
task_spec: spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-noncode.md
task_type: noncode
repo: D:\hobby\specd-workflow-template
base_branch: main
calibration: {1: A, 2: E, 3: B, 4: A, 5: A, 6: C}
workflow: A
decision: 'Human confirmed the regenerated plan is done at the plan-done gate (2026-11-19). Workflow A: PLAN -> APPROVE -> IMPLEMENT. Next: independent review (Gate 2, wf-review), then human Gate 3 approval; status moves to ready-for-implement only after Gate 3 and only with a ledger Decision.'
status: in-progress
pending: ''
worktree: D:/hobby/specd-worktree/lms-contract-plan
branch: task/WORK-LMS-CONTRACT-001-plan
---

# Plan — WORK-LMS-CONTRACT-001

## Progress

| id | question | answer |
|----|----------|--------|
| calibration-1 | Plan output shape | A. Compact card: objective, approach, files touched, verification, risks |
| calibration-2 | Understanding aid | E. Combination, but always visual-first |
| calibration-3 | Agent explanations | B. Short explanation + diagram |
| calibration-4 | Workflow path | A. PLAN → APPROVE → IMPLEMENT |
| calibration-5 | Implementation chrome | A. Numbered step lines (Step 1/N, what changed), then the next slice waits |
| calibration-6 | Teach or orient | C. Hybrid (teach only when the concept is important, new, or risky) |

Calibration recorded 2026-11-16 (single turn) and reaffirmed by the human 2026-11-18
(`WORK-148`; calibration record `CALIBRATION-LMS-CONTRACT-001`). It is binding for this
regeneration and is not re-asked.

## Decisions

- Choice 1 (Plan output shape): A — Compact card.
- Choice 2 (Understanding aid): E — Combination, but always visual-first (see the flow diagram
  under Approach).
- Choice 3 (Agent explanations): B — Short explanation + diagram.
- Choice 4 (Workflow path): A — PLAN → APPROVE → IMPLEMENT.
- Choice 5 (Implementation chrome): A — Numbered step lines, then the next slice waits.
- Choice 6 (Teach or orient): C — Hybrid.

Note: the parent SRS is Approved (`WORK-176`), so the PLAN → APPROVE → IMPLEMENT path is open;
no challenge step is mandated this run.

## Calibration

Human answers (single-letter answers, recorded verbatim): `1A 2E 3B 4A 5A 6C`. Calibration record:
`tasks/task-LMS-CONTRACT-001-noncode-calibration.md` (`CALIBRATION-LMS-CONTRACT-001`, status
Confirmed — user confirmed 6/6 on 2026-11-16; reaffirmed 2026-11-18 under `WORK-148`; binding.yaml
row corrected in `WORK-176`).

## Baseline

What exists today (verified 2026-11-19):

- Parent specification `SRS_LMS_v1.0.md` — `SRS-LMS-v1.0` **v1.2, `Approved`** (Section 11 Change
  Request `WORK-171`, Gate 2 Decision `WORK-176`, commit `b6ce80c`; v1.1 at `4b3936a`; v1.0
  anchored to `167af69`).
- Task specification `tasks/task-LMS-CONTRACT-001-noncode.md` — `WORK-LMS-CONTRACT-001`
  **v1.5, `Approved`** (`WORK-156`; seventh review; editorial pass only).
- Normative rendering `schema/final-academic-record.md` — `SCHEMA-LMS-FAR-v1.0` **v1.0.0,
  `Approved`**, `rendered_from_version: 1.5` in frontmatter. Its body provenance line still cites
  "version 1.4" — a known inconsistency (the rendering is the defect class here, not the task spec).
- Capability artifacts — all five `Approved`: `CAP-CANONICAL-FORM` v1.0, `CAP-USERID` v1.1,
  `CAP-TIMESTAMPFORMAT` v1.1, `CAP-SCHEMAVERSIONCONSTRAINT` v1.1 (Decision `WORK-175`, applied at
  `7a80293`); `CAP-STATUSENUMS` v1.1 (under `WORK-176` in the same change as SRS v1.2).
- Codebase `generated-projects/blockchain-enabled-lms/` — scaffolded, `binding.yaml` determined
  (`WORK-160`); holds scaffold only, no source. This task writes **no implementation code**.
- `service-contracts.yaml` — two declared bindings (IAM/`auth-service`, LGS/`record-schema`);
  five domains not-yet-specified; `blockchain-gateway` retired (`WORK-173`).
- SRS Q-1 answered by Decision `WORK-179` (ECS mints and owns `GoverningRuleSetID`); SRS Q-2 still
  open (the contract keeps both identifiers opaque). Retention posture: retain-all (`WORK-180`).
  Constitution tensions 1 and 6 resolved **in substance** by `WORK-180`/`WORK-179`; the document
  strike is `WORK-181` (proposed, not started). The SRS annotations are `WORK-182` (proposed, not
  started).
- This plan file previously carried a stale body (v1.2-era) and a materially false frontmatter
  (`status: complete`, "ready-for-implement", a fictitious `WORK-028` approval Decision). It is
  replaced by this regeneration. The worktree was missing; recreated from `main` (`9022742`) as
  `task/WORK-LMS-CONTRACT-001-plan`.

Honest scope note: **the deliverables of this task are largely finished and `Approved`.** The
remaining work is *verification and bookkeeping*, not authoring. `wf-implement` must not expand
this into designing the services.

## Plan

### Objectives (traced to acceptance criteria AC-1…AC-9, task spec §5)

1. Prove the normative rendering conforms to the authoritative contract v1.5 — field coverage,
   encapsulated objects, canonical field list order, presence rules, and exclusions (evidence for
   **AC-6**, **AC-8**, **AC-9**; single encoding slot already designated, **AC-5**).
2. Fix the rendering's stale attribution lines — a rendering-class defect; the task spec wins
   (project `AGENTS.md` §3). **Three lines, attribution-only, zero requirement change:** (i) the
   body provenance `1.4` → `1.5` (rendering line 17); (ii) the §9 heading reference `(v1.4)` →
   `(v1.5)` — the acceptance criteria mirror task spec §5, and the task spec is at v1.5; (iii) the
   §8 sentence "This contract is at `1.0.0` and **has never been approved**" — false; the rendering
   is `Approved` (frontmatter). Any other divergence found is **recorded as a finding, not silently
   fixed**.
3. Re-point the collection `binding.yaml` rows this run creates/changes: the plan row (this file,
   regenerated from v1.5 — `wf-plan`, 2026-11-19) and the handoff row (recreated by this run,
   status `Open`, disposable). Nothing else moves.
4. Produce the verification evidence pack the independent reviewer and `wf-converge` will read:
   a field-by-field conformance table rendering↔spec, the encoding/timestamp spot checks (**AC-7**),
   and the status-vocabulary reference (`CAP-STATUSENUMS` now Approved; the spec cites §9.1).
5. Hand off clean: handoff file updated to reflect reality, ledger records approval, and `wf-converge`
   can evaluate every AC without re-deriving anything.

```
 task spec v1.5 (Approved, authoritative)
        │  renders
        ▼
 schema/final-academic-record.md ──fix provenance line──▶ 1.5
        │ field-by-field conformance
        ▼
 evidence pack (field table · digest list order · presence rules)
        │
        ▼
 binding.yaml rows (plan, handoff) · handoff file · ledger
        │
        ▼
 wf-review ──▶ human Gate 3 ──▶ wf-implement (this file is its source of truth)
```

### Implementation layers (non-coding task)

1. **Specification** — read `schema/final-academic-record.md` fully; perform the field-by-field
   conformance check against the task spec §4.2 / §4.4 / §4.5 / §4.6 (every field, type,
   cardinality, nullability, order of the 13-field canonical list, exclusion record, R-1/R-3/R-4
   encoding, R-2 not encoded). Fix exactly three attribution-only lines (objective 2): line 17
   provenance; §9 `(v1.4)` → `(v1.5)`; §8 "has never been approved" sentence. Any other
   divergence found is **recorded as a finding, not silently fixed**.
2. **Configuration / Infrastructure** — `binding.yaml`: plan row pre-Gate-3 text is as landed in
   this change ("exists ... in-progress pending wf-review and Gate 3 approval"); at Gate 3 with the
   human's Decision, flip the row's status to `ready-for-implement` and cite the Gate 3 Decision
   id. Handoff row stays `Open (recreated by wf-plan 2026-11-19)` for the life of the task; it is
   deleted, not archived, when the handoff is disposed (`Done`). No other rows. No
   `service-contracts.yaml` change. No codebase change.
3. **Process / Documentation** — evidence pack written into the handoff (AC-1…AC-9, each mapped to
   the named evidence); `wf-implement` records what was checked and the outcome; deviations
   become findings for `wf-review`.
4. **Others** — none. No implementation code, no schema redesign, no service work.

### Files touched

- `schema/final-academic-record.md` — the three attribution-only lines (line 17 provenance
  `1.4` → `1.5`; §9 `(v1.4)` → `(v1.5)`; §8 "has never been approved" sentence) — nothing else.
- `binding.yaml` — plan row and handoff row only.
- `tasks/task-LMS-CONTRACT-001-handoff.md` — recreated by this run; updated by `wf-implement`.
- `tasks/task-LMS-CONTRACT-001-plan.md` — this file (the deliverable).
- `spec-workspace/project-temp/work_ledger.yaml` — by skills, not by hand.

**Off-limits:** the task specification (`../task-LMS-CONTRACT-001-noncode.md`, Approved — no
content edit, including the "SRS Q-1 remains open" wording made stale by `WORK-179`); the SRS
(Approved — changes only via Section 11 CR, `WORK-182`); the constitution (changes only via
amendment, `WORK-181`); all capability artifacts (Approved); any codebase file.

### Verification strategy

Every item above is document-level evidence; `wf-converge` re-verifies.

| AC | Proof | Evidence |
|---|---|---|
| AC-1 | Spec §4 principle 1, R-2, §4.2 row, §4.3; expected grep of the rendering: no `Superseded` state field, no change-classification field | §4.2 field table row; R-2; no `Superseded` state; no change-classification field. |
| AC-2 | Spec §4 principle 2 (ECS supplier, GRA-Service recorder; now also `WORK-179`, which does not alter the contract) | §4.2 `GoverningRuleSetID` row; §2.7 step 1 citation. |
| AC-3 | Rendering + digest-ready declaration; depends on the attribution-line fix landing **before** `wf-converge` runs | §4.1 statement; §4.5 13-entry list equals §4.2's 13 fields; `rendered_from_version: 1.5`. |
| AC-4 | `CAP-SCHEMAVERSIONCONSTRAINT` | §4.2 `schema_version` row; §4 principle 3; distinction from canonical-form version stated. |
| AC-5 | Single encoding designated; expected grep of the rendering for a competing format name returns no match | §4 principle 4; §4.7; search rendering for any second encoding name returns none — record the grep output in the evidence pack. |
| AC-6 | Field coverage complete, no null, rendering adds nothing | Appendix A check; rendering tables vs §4.2/§4.4.1/§4.4.2 row-by-row (27 rows). |
| AC-7 | Timestamps inventory | Appendix B check; three timestamp fields, all `YYYY-MM-DDTHH:MM:SSZ`; zero epoch fields. |
| AC-8 | Canonical field list ordered, no exclusions | §4.5 order vs §4.2 digest column; §4.6 exclusion record with per-category reasons. |
| AC-9 | Finalization fields mandatory and listed | §4.2 `finalized_at`/`authorized_by` rows; positions 11-12 of §4.5; presence rule R-4. |

`wf-review` (this plan) is Gate 2; `ready-for-implement` follows human approval (Gate 3). The
*contract* is already Approved — the gate here approves the **plan**, not the contract.

### Risks

- Rendering drifts beyond the one-line fix → becomes review findings, not silent edits (project
  `AGENTS.md` §3: rendering defects are fixed against the spec).
- `binding.yaml` re-drifts on the next `wf-implement`/`wf-commit` change → each row touched must be
  re-checked in the same change.
- Scope confusion — treating this task as "implement the LMS" → it is contract bookkeeping only;
  code for the system is a separate coding task via `wf-task-code`.
- False economy — skipping the independent review because "the artifacts are already Approved" →
  the *plan* is a new artifact and needs its own gate.
- Post-Gate-3 discovery of rendering divergence (e.g. a further stale line or a semantic drift)
  **after** `wf-converge` runs → stop the task; do not improvise a fix; return to Gate 2/Gate 3
  with the finding; `wf-implement` performs only fence-to-gate-authorized edits. Owner: human +
  `wf-converge`.
- Sequencing divergence — implementing from a stale plan because the implementation worktree holds
  the pre-regeneration file → the regenerated plan/`binding.yaml`/handoff must land on the task
  branch/worktree (verified by `git -C <worktree> show HEAD:tasks/task-LMS-CONTRACT-001-plan.md`
  showing the regenerated body) **before** `wf-implement` begins; the handoff names this
  verification explicitly. Owner: `wf-commit` flow at Gate 3 time.

## Out of scope

- Any implementation code; any service design; ECS rule content or rule-set identifier *format*
  (Q-1 answered by `WORK-179` = ECS mints the value; the format/representation question stays a
  parent concern, `SRS Q-2` for `parent_transaction_id` is untouched).
- Editing the Approved task specification, SRS, or constitution — stale wordings go through their
  own channels (`WORK-181`, `WORK-182`).
- Changing normative contract content, the canonical field list, or the rendering's semantics.
- Closing the handoff or merging anything — `wf-commit` owns commit/push; this run only records.
- Deleting the worktree — it stays for `wf-implement`.
