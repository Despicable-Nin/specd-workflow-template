# Handoff — WORK-LMS-GRADERECORD-001 (GradeRecord contract)

`status: In Progress` — Gate 2 plan review done (APPROVED WITH COMMENTS, `WORK-206`); Gate 3 plan approval recorded 2026-11-19 (Decision `WORK-207`); plan `status: ready-for-implement`. `wf-implement` is next (records-only). Worktree: `D:/hobby/specd-worktree/lms-graderecord-plan` on branch `task/WORK-LMS-GRADERECORD-001-plan` (base `main` @ `c68389d`; reused — one worktree per task). Commit of plan + this refresh + ledger at the human's prompt.

## 1. Purpose

Deliver the field-level, technology-agnostic contract for the GRA-Service-owned **`GradeRecord`** record — one record per assessed outcome for one student in one assessment. The immutable, append-only artifact behind the student-period aggregate's `academic_history`. Interests: determinism under the governing rule set, attribution, append-only corrections via `parent_transaction_id`, terminal `Finalized` state. **Never formula content; never proof-committed (proofs are over the student-period record); attendance never embedded.**

Implements: `SRS-LMS-v1.0` **v1.3** (§1.3; §2.2 W-1; §2.3 W-2; §2.4 W-3; §2.9; §3.1 GRA-Service; §3.5; §3.6; §3.7; §4.2 S-1/S-3/S-6; §5; §9.1/CAP-STATUSENUMS; §10). Implements the `WORK-196` gap partially (this contract only; Session/AttendanceRecord remains).

**Explicitly not covered:** `GradeAppealRecord`, `ReviewLog`, `LevelCompletionRecord`, `StudentPeriodRecord` field semantics; formula content; the `change_status` vocabulary (deferred: change control); formats of `transaction_id`/`parent_transaction_id`; retention policy; the Session/AttendanceRecord contract; `CAP-STATUSENUMS` restatement; `service-contracts.yaml`.

## 2. Status

`In Progress` — spec **v1.3** Approved (Gate 3, Decision `WORK-204`; four independent Gate 2 spec passes). Plan run file `task-LMS-GRADERECORD-001-plan.md` reviewed 2026-11-19 (verdict APPROVED WITH COMMENTS; `WORK-206`, findings F-1..F-9 not folded — human disposed **approve as-is**) and approved at Gate 3 (Decision `WORK-207`); `status: ready-for-implement`. Work is records-only: nothing remains to be designed or built. Contributing skills: `wf-task-noncode`, `wf-plan`, `wf-review`; next: `wf-implement` (Step 1..5), then `wf-converge`, then `wf-commit` (handoff disposed there).

**Artifact placement (F-10) — RESOLVED 2026-11-19 at the commit prompt:** the artifacts were untracked on `task/WORK-LMS-FORMULARULES-001-plan` at Gate 3; the human chose to create the designated task worktree/branch (`D:/hobby/specd-worktree/lms-graderecord-plan`, `task/WORK-LMS-GRADERECORD-001-plan`, off `main`) and carry them there. They are committed on that branch; the FormulaRules worktree/branch is clean and untouched.

## 3. Action items

1. **DONE** — `wf-review` ran (verdict APPROVED WITH COMMENTS; `WORK-206`); human disposed **approve as-is**; Gate 3 plan approval recorded (`WORK-207`); plan `status: ready-for-implement`.
2. **`wf-implement`** — records-only per the plan (calibration 5A chrome: numbered step lines, slice waits): re-run **AC-1 / AC-4 / AC-7 / AC-10** on the committed v1.3; cite the other eleven ACs to the pass-3/4 evidence; refresh records; hand off to `wf-converge`. No code is authorized.
3. **`wf-converge`** — verify AC-1..AC-15 against the plan's inline index; then **`wf-commit`** disposes of this handoff (deleted, not archived) and commits at the prompt.
4. **Commits** — `e69901e`/`747bde0` DONE 2026-11-19. Plan + this refresh + ledger committed at the human's prompt (this commit); pushes only with explicit authorization.
5. **`WORK-196`** — remains open for the Session/AttendanceRecord contract (the last gap before any coding slice).
6. **Change requests (owed, not started)** — `SRS §11 CR`/`CAP-STATUSENUMS` v1.3 for the `change_status` vocabulary (Section 11 C-1); SRS Q-2 resolutions (C-2); `WORK-181`/`WORK-182`; retention-policy Decision (constitution tension 1); F-13 (LGS `TransactionID` name-collision note) carried to the LGS task spec.

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

**`wf-implement`** — parameters:

- Project: `blockchain-enabled-lms`
- Plan: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-plan.md` (`status: ready-for-implement`; Gate 3 `WORK-207`)
- Task spec: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-noncode.md` (Approved v1.3; `WORK-204`)
- Worktree: `D:/hobby/specd-worktree/lms-graderecord-plan`; branch `task/WORK-LMS-GRADERECORD-001-plan`
- Rationale: the plan is the source of truth; this records-only slice re-checks AC-1/AC-4/AC-7/AC-10 on the committed file and cites the rest; `wf-converge` then verifies AC-1..AC-15; `wf-commit` disposes of this handoff (deletes it) and commits at the prompt.

## 7. Phase contributions

| Skill | When | Produced |
|---|---|---|
| `wf-task-noncode` | 2026-11-19 | Six-choice calibration (Gate 1 final; bindings recorded); scan of SRS v1.3 + sibling contracts + FAR rendering + capabilities; spec v1.0 drafted; v1.1 after Gate 2 pass 1 (F-01..F-13); v1.2 after pass 2 (F-201..F-208); v1.3 after pass 3 (F-301..F-303 + N-1); pass 4 APPROVED WITH COMMENTS; Gate 3 approval `WORK-204`; handoff (this file); ledger `WORK-204`, `WORK-205` |
| `wf-plan` | 2026-11-19 | Plan run file `task-LMS-GRADERECORD-001-plan.md` drafted (calibration 1C 2E 3D 4C 5A 6B; workflow C); worktree REUSED (created at the commit prompt from `main` @ `c68389d`; branch `task/WORK-LMS-GRADERECORD-001-plan`); Plan drafted and confirmed Done by the human; handoff refreshed; baseline table; evidence index inline |
| `wf-review` | 2026-11-19 | Gate 2 review of the plan (session `ses_e0c99b327ffea9IfBhaeJNB48n`, read-only): verdict APPROVED WITH COMMENTS; findings F-1..F-9 recorded as ledger item `WORK-206` (`proposed`; none auto-closed); human disposed approve-as-is at the Gate 3 prompt |
| `wf-plan` (Gate 3) | 2026-11-19 | Plan approval Decision `WORK-207` recorded; plan `status: ready-for-implement`; this file refreshed; plan/handoff/ledger committed on this branch at the human's prompt |
