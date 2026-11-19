# Handoff — WORK-LMS-FORMULARULES-001 (FormulaRules contract)

`status: ready-for-implement` — Gate 3 plan approval recorded 2026-11-19T14:40:58Z (Decision `WORK-201`). Plan confirmed Done by the human; Gate 2 review CHANGES REQUIRED with findings F-01..F-07, all fixed; worktree synced to `main` after the commit carrying this file.

## 1. Purpose

Deliver the field-level, technology-agnostic contract for the ECS-owned **`FormulaRules`** record — the grade-formula rule book the LMS consumes to compute final grades. Structure only; never formula content. Implements: `SRS-LMS-v1.0` v1.3 (C-2; §2.3 W-2 formula-ownership note; §3.1 ECS; §3.2; §4.2 S-3/S-6; §5; §6).

**Explicitly not covered:** formula content; implementation; `Session`/`AttendanceRecord` and `GradeRecord` contracts; constitution; SRS.

## 2. Status

`Ready for implement` — task spec **Approved v1.2** (Gate 3, Decision `WORK-198`). Plan run file `task-LMS-FORMULARULES-001-plan.md` is `ready-for-implement` (Decision `WORK-201`, 2026-11-19T14:40:58Z). Worktree: `D:/hobby/specd-worktree/lms-formularules-plan` on branch `task/WORK-LMS-FORMULARULES-001-plan` (base `main`; relocated from an initial in-repo placement). Main carries the plan/handoff/ledger commit; the worktree branch fast-forwards from `main` in the apply step.

Review trail for the plan (2026-11-19, delegated, read-only): verdict CHANGES REQUIRED; findings F-01..F-07:

- **F-01** (high) — approval evidenced only by prompt, no ledger Decision: **RESOLVED** — Gate 3 Decision `WORK-201` recorded at plan approval.
- **F-02** (high) — plan/handoff uncommitted while the worktree expected them: **RESOLVED** — committed on `main`; worktree branch fast-forwarded.
- **F-03** — handoff stale: **RESOLVED** (this refresh).
- **F-04** — evidence index / AC-9 rationale location undefined: **RESOLVED** — index inline in the plan; rationale = on-task ledger Decision cited in the plan.
- **F-05** — glued heading: **RESOLVED**. **F-06** — vestigial `.gitignore` mention: **RESOLVED**. **F-07** — path separators normalized.

Contributing skills: `wf-task-noncode` (spec loop), `wf-plan` (calibration, worktree, baseline, draft), `wf-review` (Gate 2), `wf-implement` (next).

## 3. Action items

1. **`wf-converge` / `wf-implement`** — plan is approved; the implementation slice here is records-only (AC-9 Layer 1 + evidence pack per the plan's Layer 3). Per the suggested run below; commits at your prompt.
2. **`service-contracts.yaml` ECS binding (AC-9)** — execute the plan's Layer 1: default = keep `not-yet-specified` + written rationale (recorded as an on-task ledger Decision id, cited in the plan and this file); flip only if a named component with `provides`/`requires` is supplied. Verification: manifest unchanged-or-flipped + ledger Decision.
3. **Evidence pack** — assemble per the plan's inline index (AC-1..AC-13 pointers); nothing new gets created.
4. **Handoff disposal** — when converged and committed, this handoff is marked `Done` and deleted by `wf-commit` (disposable contract).

## 4. Preconditions unmet

None for Gate 3 or `wf-converge`. For downstream coding slices (separate tasks): the `Session`/`AttendanceRecord` contract and the `GradeRecord` contract must exist and be Approved first (`WORK-196`).

## 5. Open questions

1. SRS Q-1 — resolved in substance (`WORK-179`); formal annotation pending `WORK-182` (proposed). Contract carries the caveat (spec §11).
2. CONST tension 6 — open as of CONST-LMS-v1.3; `WORK-181` (proposed).
3. Retention of superseded rule sets — constitution tension 1; Decision owed separately.
4. ECS binding flip — deferred to action item 4.
5. Approval chain — decided in-spec: by reference (spec §13.6).

## 6. Suggested skill run

**`wf-implement`** — parameters:

- Project: `blockchain-enabled-lms`
- Plan: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-FORMULARULES-001-plan.md` (`ready-for-implement`, Decision `WORK-201`)
- Task spec: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-FORMULARULES-001-noncode.md` (Approved v1.2)
- Worktree: `D:/hobby/specd-worktree/lms-formularules-plan`
- Branch: `task/WORK-LMS-FORMULARULES-001-plan`
- Rationale: the plan file is the source of truth; this slice implements Layer 1 (AC-9) + Layer 3 records (evidence pack); it is records-only, no code. `wf-converge` after it verifies AC-1..AC-13 against the plan's inline index.

## 7. Phase contributions

| Skill | When | Produced |
|---|---|---|
| `wf-task-noncode` | 2026-11-19 | Calibration; task spec v1.0→v1.2 (Approved); Gate 1 + Gate 3 (`WORK-198`); initial handoff; ledger (`WORK-198`, `WORK-199`) |
| `wf-plan` | 2026-11-19 | Plan run file (calibration 1C 2E 3C 4A 5C 6C); worktree (initially in-repo `.worktrees/`, relocated to `D:/hobby/specd-worktree/lms-formularules-plan`); branch `task/WORK-LMS-FORMULARULES-001-plan` from `main` @ `ecad899`; baseline recorded; plan drafted, human-confirmed Done; F-02..F-07 review fixes applied |
| `wf-review` | 2026-11-19 | Gate 2 review of the plan: verdict CHANGES REQUIRED; findings F-01..F-07 recorded as ledger item `WORK-200` |
| `wf-plan` (Gate 3) | 2026-11-19T14:40:58Z | Plan approval Decision `WORK-201`; `status: ready-for-implement`; this file refreshed (action items, suggested run) |
