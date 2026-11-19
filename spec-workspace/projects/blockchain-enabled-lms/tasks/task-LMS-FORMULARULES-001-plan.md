---
skill: wf-plan
task_id: WORK-LMS-FORMULARULES-001
task_spec: spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-FORMULARULES-001-noncode.md
task_type: noncode
repo: D:\hobby\specd-workflow-template
base_branch: main
calibration: {1: C, 2: E, 3: C, 4: A, 5: C, 6: C}
workflow: A
decision: workflow A (PLAN -> APPROVE -> IMPLEMENT); plan filled and confirmed Done by the human at 2026-11-19T14:06:42Z; Gate 3 plan approval recorded as ledger Decision WORK-201 (2026-11-19T14:40:58Z)
status: ready-for-implement
pending: 
worktree: D:/hobby/specd-worktree/lms-formularules-plan
branch: task/WORK-LMS-FORMULARULES-001-plan
---

# Plan â€” WORK-LMS-FORMULARULES-001

## Progress

| id | question | answer |
|----|----------|--------|
| calibration-1 | Plan output shape | C. Card first; layered tree only where it adds |
| calibration-2 | Understanding aid | E. Combination, but always visual-first |
| calibration-3 | Explanation budget | C. Only explain when ambiguous or risky |
| calibration-4 | Workflow path | A. PLAN -> APPROVE -> IMPLEMENT |
| calibration-5 | Implementation chrome | C. Layer by layer; one layer fully verified before next |
| calibration-6 | Teach or orient | C. Hybrid (teach only when concept is important/new/risky) |

## Pending

- none

## Decisions

- Workflow A (PLAN -> APPROVE -> IMPLEMENT). No challenge step; standard gate sequence.
- Implementation chrome C: layered-by-layer reporting, one layer verified before the next begins.
- Posture C: hybrid teach/orient; teach only the important, new, or risky concepts.
- Plan confirmed DONE by the human at 2026-11-19T14:06:42Z ("Done" at the plan-done prompt).
- Gate 3 approval recorded as ledger Decision WORK-201 (2026-11-19T14:40:58Z), plan ready-for-implement.
- **AC-9 disposition (2026-11-19): default no-flip path taken.** Human chose Keep `not-yet-specified` at the wf-implement AC-9 prompt; written rationale recorded as ledger Decision `WORK-202`; `service-contracts.yaml` ECS row untouched. Revisit only when an ECS implementation plan names a deployable component with `provides`/`requires`.
- Worktree relocated same session: initially created in-repo at `.worktrees/lms-formularules-plan` (plain reading of calibration choice 4 option B), then moved to `D:/hobby/specd-worktree/lms-formularules-plan` after the human pointed out the house precedent (sibling worktree dir; cf. `D:/hobby/specd-worktree/lms-contract-plan`). A `.gitignore` ignoring `.worktrees/` was created for the in-repo layout and then Removed when the worktree relocated out of the repo.

## Calibration

1. **Plan output shape** â€” compact card first; layered tree only where it adds something the
   card cannot. 2. **Understanding aid** â€” combination, always visual-first. 3. **Explanation
   budget** â€” only on ambiguity or risk; silence otherwise. 4. **Workflow path** â€” PLAN -> APPROVE
   -> IMPLEMENT. 5. **Implementation chrome** â€” layer by layer, one layer verified before the
   next begins. 6. **Teach or orient** â€” hybrid.

## Baseline

| Artifact | State |
|---|---|
| Parent spec `SRS-LMS-v1.0` v1.3 | `Approved` (Gate 2 `WORK-192`); attendance Workflow W-7/C-8 landed 2026-11-19 |
| Task spec `task-LMS-FORMULARULES-001-noncode.md` v1.2 | `Approved` (Gate 3, Decision `WORK-198`, 2026-11-19); calibration final (Gate 1); three review passes, terminal APPROVED WITH COMMENTS; AC-8 executed, all OK |
| Capabilities | `CAP-TIMESTAMPFORMAT` v1.1, `CAP-SCHEMAVERSIONCONSTRAINT` v1.1, `CAP-USERID` v1.1 ADOPT; `CAP-STATUSENUMS` v1.2, `CAP-CANONICAL-FORM` v1.0 DECLINE (spec Â§7) |
| `service-contracts.yaml` | `ecs` = `not-yet-specified`; the AC-9 flip decision is deferred to this plan (named-component rule: flip only with a named component + `provides`/`requires`; else written rationale; ledger Decision either way) |
| Codebase `generated-projects/blockchain-enabled-lms/` | scaffold only; zero implementation; `binding.yaml` re-pinned to root spec v1.3 |
| Git | worktree `D:/hobby/specd-worktree/lms-formularules-plan` on `task/WORK-LMS-FORMULARULES-001-plan`, based on `main` @ `ecad899`; worktree clean; main ahead of origin by 1 (push unauthorized) |
| Open questions (spec Â§10â€“11) | SRS Q-1 (WORK-179 substance; WORK-182 annotation pending); CONST tension 6 (WORK-181); retention Decision (tension 1); approval-chain by-reference decided (spec Â§13.6) |
| Preconditions for downstream coding | separate contracts outstanding: `Session`/`AttendanceRecord` and `GradeRecord` (WORK-196) |

## Plan

**Objectives (trace).** Execute the approved contract's own bookkeeping â€” nothing new is built. Traces: AC-1â€¦AC-13 gate `WORK-LMS-FORMULARULES-001`; this plan closes AC-9 (the only open deliverable), fixes the verification index, and hands the slice over cleanly.

**Approach.** PLAN â†’ APPROVE â†’ IMPLEMENT (workflow A). Worktree `D:/hobby/specd-worktree/lms-formularules-plan` on `task/WORK-LMS-FORMULARULES-001-plan` from `main` @ `ecad899` (created at plan time, per choice-4 preferences). No coding layers; implementation for this non-code task is decision application and record-keeping, executed by `wf-implement` against this file.

**Layers (non-coding split):**

1. **Configuration / Infrastructure â€” `service-contracts.yaml` (AC-9).** Current: `ecs` = `not-yet-specified`. No named ECS component exists (no code; SRS Â§6 defers topology). **Default, honest disposition: remain `not-yet-specified` with a written rationale + ledger Decision.** Flip only if the human names a component with `provides`/`requires` recorded in the manifest; never invent a runtime binding; never edit bindings without the named-component rule satisfied. **Outcome (2026-11-19): executed by `wf-implement` - default no-flip path; human chose Keep at the AC-9 prompt; ledger Decision `WORK-202`; manifest untouched.**
2. **Specification â€” nothing.** The Approved spec v1.2 is frozen; changes via change control only.
3. **Process / Documentation.** (a) Evidence index mapping AC-1â€¦AC-13 to artifacts: AC-1 frontmatter/path âœ” (exists); AC-2/AC-5 Â§13 matrix âœ” review passes (F/C-1..M-class, all resolved); AC-3 stability clause âœ”; AC-4 standalone-numeric-literal tokenizer âœ” (final pass zero hits); AC-6 ownership clause âœ”; AC-7 caps table vs `library/` âœ”; AC-8 pre-check log âœ” (review session `ses_e0db7dd7bffeyWSfzGVM7qPART`, all steps OK); AC-10â€“13 reviewer-validated âœ”; **AC-9 â†’ this layer.** (b) Handoff refresh on approval. (c) Commits only at explicit human authorization; SHAs recorded in the ledger when they happen.
4. **Others.** Worktree relocated (2026-11-19) to the house sibling dir `D:/hobby/specd-worktree/lms-formularules-plan` after initial in-repo placement; no stack, no storage, no protocol decisions.

**Files touched.** `service-contracts.yaml` (decision record; edit only on flip), this plan file, `task-LMS-FORMULARULES-001-handoff.md`, `spec-workspace/project-temp/work_ledger.yaml`, (optionally `.gitignore` in a commit). **Off-limits:** SRS, constitution, CAP artifacts, `schema/final-academic-record.md`, the codebase, the task spec body, `service-contracts.yaml` bindings beyond the `ecs` row.

**Data flow.** None â€” decision + records only.

**Verification strategy (AC â†’ evidence).** AC-1: path + frontmatter check. AC-2/AC-5: Â§13.2/Â§13.3 tables vs Â§14 matrix (reviewer). AC-3: Â§13.4 stability clause read. AC-4: word-tokenizer per the AC-4 definition (excluded classes iâ€“iii). AC-6: Â§13.1 ownership clause + SRS citations. AC-7: versions against `library/Capabilities/` frontmatter. AC-8: pre-check log from the reviewing session. AC-9: file diff or recorded rationale + ledger Decision. AC-10: registrar-reader pass (reviewer). AC-11: grep against marker list. AC-12: Â§13.8 scoping vs SRS W-3/S-3. AC-13: Â§13.9 boundary table vs Â§13.8/Â§13.10 alignment. Evidence pack = links to the review-session findings + this mapping.

**Evidence index / rationale home (F-04).** The verification index lives **inline in this file** (the table above); no separate index document is produced. The AC-9 written rationale (default no-flip path taken) is recorded as **ledger Decision `WORK-202`** - cited here and in the handoff; the manifest itself stays untouched in this branch and `git diff` on `service-contracts.yaml` is empty. The evidence pack for convergence is exactly the pointer set above; `wf-implement` cites these, never re-derives them.

**Risks.** (1) Flipping `ecs` without a named component invents runtime binding and violates AC-9 â€” forbidden. (2) Editing any Approved artifact outside change control voids its approval. (3) Push/commit without authorization â€” will not happen; each is asked at its prompt. (4) Path drift between plan/handoff â€” mitigated: relocation recorded in this file and the handoff.

**Out of scope.** Any implementation code; SRS/constitution edits; contract changes (change control only); Session/AttendanceRecord and GradeRecord contracts (`WORK-196`, separate tasks); `WORK-181`/`WORK-182`; retention Decision (constitution tension 1); pushing without explicit authorization.

## Out of scope

- Any implementation code â€” implementation-shaped slices here are decision application and records only.
- SRS, constitution, CAP artifacts edits â€” Approved artifacts change by change control only.
- The contract spec body (v1.2) â€” frozen by approval; any change is a new CR/version cycle.
- `service-contracts.yaml` bindings other than the `ecs` row; any flip without a named component.
- Session/AttendanceRecord and GradeRecord contracts (`WORK-196` â€” separate `wf-task-noncode` tasks).
- `WORK-181` (constitution v1.4) and `WORK-182` (SRS Section 11 CR) â€” other owners' change requests.
- Retention-policy Decision (constitution tension 1) â€” owed separately.
- Push of any commit â€” requires explicit human authorization at its prompt each time.
