---
skill: wf-task-noncode
calibration_id: CALIBRATION-LMS-GRADERECORD-001
task_id: WORK-LMS-GRADERECORD-001
task_type: noncode
project: blockchain-enabled-lms
parent_spec: SRS-LMS-v1.0
parent_spec_version: 1.3
created: 2026-11-19T16:18:36Z
finalized: 2026-11-19T16:20:00Z
status: final
---

# Calibration — WORK-LMS-GRADERECORD-001 (GradeRecord contract)

Six consumption choices, asked one at a time, recorded bindingly. No defaults assumed.

| # | Choice | Answer |
|---|--------|--------|
| 1 | Task shape | **Contract spec only** — field-level, technology-agnostic specification (data contract) for the GRA-Service `GradeRecord`; FormulaRules-shaped; structure only; never formula content. Blast radius: `spec-workspace/` + work ledger; no code; SRS frozen. |
| 2 | Evidence / deliverables | **Spec + calibration + handoff** at canonical paths (`task-LMS-GRADERECORD-001-noncode.md`, this file, and the task handoff). No schema rendering is produced by this task. |
| 3 | Verification depth | **Review sign-off + downstream conformance pre-check walk** — independent `wf-review` (Gate 2) with findings resolved, human Gate 3 approval, plus an explicit downstream conformance pre-check walk (FormulaRules AC-8 analogue: walk W-2/W-3 to confirm `GradeRecord` can carry what GRA-Service must persist — `rule_set_id`, `parent_transaction_id`, and the finalization proof reference), logged as evidence. |
| 4 | Workflow path | **Isolated sibling worktree + task branch.** Preferences for `wf-plan` (which creates the worktree from `main`): worktree at `D:/hobby/specd-worktree/lms-graderecord-plan`; branch `task/WORK-LMS-GRADERECORD-001-plan`; base `main`. |
| 5 | Implementation surface | **In scope:** `spec-workspace/projects/blockchain-enabled-lms/tasks/` (new artifacts) and `spec-workspace/project-temp/work_ledger.yaml` (new items only). **Off-limits:** SRS (`SRS_LMS_v1.0.md`), constitution (`CONST-LMS-v1.3`), CAP artifacts, `schema/final-academic-record.md`, the FormulaRules contract (`task-LMS-FORMULARULES-001-noncode.md`), `service-contracts.yaml`. **Not off-limits but unused this task:** `schema/` — allowed surface, produces nothing in this task per Choice 2 (deliverable set governs). |
| 6 | Orientation target | **Registrar-first** — leads with a plain-language §0 summary for registrar / academic-office readers, then the full normative contract; written for an independent reviewer and a future maintainer. |

## Parent spec targeting (Step 3, explicit)

Selected by the human at the targeting prompt 2026-11-19: `SRS-LMS-v1.0` **v1.3** — Approved (Gate 2 Decision `WORK-192`; attendance Workflow W-7 / capability C-8). The only parent spec available in this collection. Task implements against SRS v1.3 (GRA-Service domain §3.1/§3.2; W-2/W-3; W-4 appeals; §2.7 LGS proof commitment; §5 determinism; §6 boundary rule).

## Recorded reconciliation (Choice 2 vs Choice 5)

Choice 5 marks `schema/` as *not off-limits*; Choice 2 limits this task's deliverables to spec + calibration + handoff. **Binding resolution:** this task emits no rendering; `schema/` stays read-only for this task. If a rendering is ever wanted, it is a separate task or a change request.

## Notes

- Task id `WORK-LMS-GRADERECORD-001` follows the `WORK-LMS-FORMULARULES-001` convention.
- FormulaRules is the structural template (field-level contract; ownership clause; traceability matrix; pre-check walk; caps adoption table). GradeRecord is GRA-Service-owned, NOT ECS-owned — ownership rules differ and must not be copied blindly.
- `WORK-196` (discovery `wf-state` 2026-11-19) is the gap item this task closes, and it remains open for the Session/AttendanceRecord contract.
- No worktree is created by this task; `wf-plan` creates it from `main` honouring Choice 4.
