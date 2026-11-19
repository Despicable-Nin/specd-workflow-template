# Handoff — WORK-LMS-GRADERECORD-001 (GradeRecord contract)

`status: Approved` — Gate 3 approval recorded 2026-11-19T18:15:32Z (Decision `WORK-204`). Gate 2 converged over four independent passes (pass 4: APPROVED WITH COMMENTS, no blocking findings). Worktree does **not** exist yet; `wf-plan` creates it from `main` per calibration choice 4.

## 1. Purpose

Deliver the field-level, technology-agnostic contract for the GRA-Service-owned **`GradeRecord`** record — one record per assessed outcome for one student in one assessment. The immutable, append-only artifact behind the student-period aggregate's `academic_history`. Interests: determinism under the governing rule set, attribution, append-only corrections via `parent_transaction_id`, terminal `Finalized` state. **Never formula content; never proof-committed (proofs are over the student-period record); attendance never embedded.**

Implements: `SRS-LMS-v1.0` **v1.3** (§1.3; §2.2 W-1; §2.3 W-2; §2.4 W-3; §2.9; §3.1 GRA-Service; §3.5; §3.6; §3.7; §4.2 S-1/S-3/S-6; §5; §9.1/CAP-STATUSENUMS; §10). Implements the `WORK-196` gap partially (this contract only; Session/AttendanceRecord remains).

**Explicitly not covered:** `GradeAppealRecord`, `ReviewLog`, `LevelCompletionRecord`, `StudentPeriodRecord` field semantics; formula content; the `change_status` vocabulary (deferred: change control); formats of `transaction_id`/`parent_transaction_id`; retention policy; the Session/AttendanceRecord contract; `CAP-STATUSENUMS` restatement; `service-contracts.yaml`.

## 2. Status

`Approved` — spec **v1.3**, Gate 3 Decision `WORK-204` (2026-11-19T18:15:32Z). `task_type: noncode`; `parent_spec: SRS-LMS-v1.0` v1.3; calibration final (`CALIBRATION-LMS-GRADERECORD-001`, Gate 1 final). Review record: four delegated read-only passes — F-01..F-13, F-201..F-208, F-301..F-303 all resolved and re-verified in-text; walks clean; exactly one AMBIGUOUS (B3, Section 11 C-1, pre-dispositioned, not a failure). Contributing skills: `wf-task-noncode` (this file); next: `wf-plan`.

**Artifact placement (F-10) — RESOLVED 2026-11-19 at the commit prompt:** the artifacts were untracked on `task/WORK-LMS-FORMULARULES-001-plan` at Gate 3; the human chose to create the designated task worktree/branch (`D:/hobby/specd-worktree/lms-graderecord-plan`, `task/WORK-LMS-GRADERECORD-001-plan`, off `main`) and carry them there. They are committed on that branch; the FormulaRules worktree/branch is clean and untouched.

## 3. Action items

1. **`wf-plan`** — create the plan file for this task (creates worktree from `main`): worktree preference `D:/hobby/specd-worktree/lms-graderecord-plan`, branch `task/WORK-LMS-GRADERECORD-001-plan`, base `main` (calibration choice 4; `wf-plan` creates it, not this skill). Plan is the source of truth for `wf-implement`.
2. **`wf-implement`** (after plan approval) — records-only slice: re-run AC-4/AC-10 regressions, confirm artifacts, and hand to `wf-converge`. No code is authorized by this task.
3. **Commit** — DONE 2026-11-19: artifacts committed on `task/WORK-LMS-GRADERECORD-001-plan` in `D:/hobby/specd-worktree/lms-graderecord-plan` (commit at the commit prompt; message `[WORK-204] …`). Push to `origin` authorized by the human (`git push -u origin task/WORK-LMS-GRADERECORD-001-plan`).
4. **Handoff disposal** — when converged and committed, this handoff is marked `Done` and deleted by `wf-commit` (disposable contract).
5. **`WORK-196`** — remains open for the Session/AttendanceRecord contract (the third missing contract). Raise via `@wf-task-noncode` after this task's planning, or in parallel.
6. **Change requests (owed, not started)** — `SRS §11 CR` or `CAP-STATUSENUMS` v1.3 for the `change_status` vocabulary (Section 11 C-1); SRS Q-2 resolution (`transaction_id`/`parent_transaction_id` formats); `WORK-181`/`WORK-182`; retention-policy Decision (constitution tension 1); F-13 (LGS `TransactionID` name-collision note) carried to the LGS task spec.

## 4. Preconditions unmet

None for `wf-plan`. Downstream of this task: the `GradeRecord` contract is Approved (this task); the `Session`/`AttendanceRecord` contract is outstanding (`WORK-196`) and gates any coding slice that touches the attendance path; the FormulaRules contract is Approved; `WORK-196` must close before any `wf-task-code` slices are raised for the grading/attendance flow.

## 5. Open questions

1. `change_status` value vocabulary — **open, owner: change control** (SRS §11 CR or `CAP-STATUSENUMS` v1.3). Contract requires presence-iff-successor and refuses unknown values meanwhile (Section 11 C-1).
2. `transaction_id` / `parent_transaction_id` formats and minter — **open, owner: domain owners** (SRS Q-2; Section 11 C-2). Opaque by contract; no UUID mandate.
3. Glossary-vs-W-2 granularity reading — resolved in this task by recorded interpretation (glossary "Grade record": one record per assessed outcome in one assessment); accepted by Gate 3 approval (Q-OWN-2). Rejecting it is a change-control matter.
4. Approval authority for grades at W-2 step 4 — by reference, not decided (Q-OWN-4; ECS/IAM territory).
5. Retention of superseded records — no Decision yet (constitution tension 1); blocks any lifecycle/deletion feature.
6. N-i / N-ii (pass-4 comments) — informational; no action required; noted here for the record.

## 6. Suggested skill run

**`wf-plan`** — parameters:

- Project: `blockchain-enabled-lms`
- Task spec: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-noncode.md` (Approved v1.3; Gate 3 `WORK-204`)
- Calibration: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-noncode-calibration.md` (Gate 1 final)
- Worktree preference: `D:/hobby/specd-worktree/lms-graderecord-plan`; branch `task/WORK-LMS-GRADERECORD-001-plan`; base `main`
- Rationale: the plan file is the source of truth for `wf-implement` and creates the worktree from `main` honouring calibration choice 4. Implementation of this task is records-only (no code); convergence will verify AC-1..AC-15 (AC-4/AC-10 re-run, AC-7 capability versions, §13.9 exhaustiveness, walk logs) against the plan's inline evidence index. Commits at the prompt via `wf-commit`.

## 7. Phase contributions

| Skill | When | Produced |
|---|---|---|
| `wf-task-noncode` | 2026-11-19 | Six-choice calibration (Gate 1 final; bindings recorded); scan of SRS v1.3 + sibling contracts + FAR rendering + capabilities; spec v1.0 drafted; v1.1 after Gate 2 pass 1 (F-01..F-13); v1.2 after pass 2 (F-201..F-208); v1.3 after pass 3 (F-301..F-303 + N-1); pass 4 APPROVED WITH COMMENTS; Gate 3 approval `WORK-204`; handoff (this file); ledger `WORK-204`, `WORK-205` |
