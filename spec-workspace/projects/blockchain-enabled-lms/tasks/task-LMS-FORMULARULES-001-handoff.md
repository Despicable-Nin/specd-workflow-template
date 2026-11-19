# Handoff — WORK-LMS-FORMULARULES-001 (FormulaRules contract)

`status: In Progress` — Gate 3 approved; ready for `wf-plan`.

## 1. Purpose

Deliver the field-level, technology-agnostic contract for the ECS-owned **`FormulaRules`** record —
the grade-formula rule book the LMS consumes to compute final grades. Defines **structure only**
(envelope, identity, versioning, supersession, validation boundaries); **never** formula content
(weights, thresholds, aggregation policy). Implements: `SRS-LMS-v1.0` v1.3 (capability C-2; §2.3
W-2 formula-ownership note; §3.1 ECS; §3.2; §4.2 S-3/S-6; §5; §6).

**Explicitly not covered:** the formula content itself (ECS-owned); any implementation; the
`Session`/`AttendanceRecord` and `GradeRecord` contracts; the constitution; the SRS.

## 2. Status

`In Progress` — Gate 3 approved 2026-11-19 (Decision `WORK-198`); task spec **Approved v1.2**
at `tasks/task-LMS-FORMULARULES-001-noncode.md`. Independent review: three passes, terminal
verdict APPROVED WITH COMMENTS (AC-8 executed, all OK). This task and its handoff are governed by
the root `AGENTS.md` and `spec-workspace/AGENTS.md`; Rule 0 applies.

Contributing skills so far: `wf-task-noncode` (calibration, draft, review loop, Gate 3, handoff).
Next: `wf-plan`.

## 3. Action items

1. **`wf-plan`** — create the task worktree **from `main`**. Preferences (calibration choice 4):
   **in-repo** worktree under `.worktrees/<task-slug>`, branch `task/WORK-LMS-FORMULARULES-001-plan`
   (exact slug finalized at `wf-plan`), base `main`. Artifact: plan file at
   `tasks/task-LMS-FORMULARULES-001-plan.md` — the source of truth for `wf-implement`. **This skill
   creates no worktree; the handoff preferences only.**
2. **Decide `service-contracts.yaml` ECS binding** (spec AC-9, in-scope per calibration): flip
   `ecs` to `declared` only with (a) a named component and (b) `provides`/`requires` recorded in the
   manifest — otherwise keep `not-yet-specified` with a written rationale; either way record a
   ledger Decision. Do not invent a runtime binding.
3. If the disposition is commit-worthy (expected): commit the contract artifacts
   (`task-LMS-FORMULARULES-001-noncode.md`, calibration, handoff, ledger) under authorization at
   the prompt. No push without explicit authorization.
4. Record commit SHA(s) in the ledger history of this task's items at commit time.

## 4. Preconditions unmet

None for `wf-plan`. For downstream coding slices (separate tasks): the `Session`/`AttendanceRecord`
contract and the `GradeRecord` contract must exist and be Approved first (ledger `WORK-196`,
partially discharged by this task).

## 5. Open questions

1. SRS Q-1 (rule-set identifier source) — open in the SRS text; resolved in substance by `WORK-179`
   (ECS mints/owns `GoverningRuleSetID`); formal annotation pending `WORK-182` (proposed). The
   contract carries the caveat (§11 of the spec).
2. Constitution tension 6 (SRS Q-1, open as of CONST-LMS-v1.3) — constitution v1.4 pending
   (`WORK-181`, proposed).
3. Retention of superseded rule sets — constitution tension 1; Decision owed separately.
4. Rule-set lifecycle states — declined in this contract (no lifecycle); revisit only via review or
   Section 11 CR.
5. Approval chain embedding — **decided in-spec**: by reference, never embedded (§13.6). Revisit
   only via review.

## 6. Suggested skill run

**`wf-plan`** — exact parameters:

- Project: `blockchain-enabled-lms`
- Task id: `WORK-LMS-FORMULARULES-001`
- Task spec: `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-FORMULARULES-001-noncode.md` v1.2 (`Approved`)
- Worktree preferences: in-repo `.worktrees/<task-slug>`, branch `task/WORK-LMS-FORMULARULES-001-plan`, base `main`
- Parent spec: `SRS-LMS-v1.0` v1.3

Why next: the task is approved; `wf-plan` always creates the worktree from `main`/`master`,
calibrates the plan (six choices recorded bindingly), and produces the plan file — the source of
truth for `wf-implement`. The deliverable here is the contract (no code), so the plan sequences
review/approval bookkeeping, not implementation.

## 7. Phase contributions

| Skill | When | Produced |
|---|---|---|
| `wf-task-noncode` | 2026-11-19 | Calibration run file; task spec v1.0 → v1.2 (Approved); Gate 1 (calibration final), Gate 3 (approval, Decision `WORK-198`); this handoff; ledger entries |
