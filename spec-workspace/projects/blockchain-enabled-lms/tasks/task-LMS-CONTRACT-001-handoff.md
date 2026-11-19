# Handoff — WORK-LMS-CONTRACT-001

## Purpose

Define and maintain the single common handoff file for the task that defines the canonical
`final_academic_record` data contract — the student-period record (SRS §2.8) and the payload over
which LGS commits its proof. It tracks the task from its Approved contract through planning,
implementation and convergence to commit.

Implements: `tasks/task-LMS-CONTRACT-001-noncode.md` (`WORK-LMS-CONTRACT-001`, v1.5, `Approved`).
Parent specification: `SRS-LMS-v1.0` v1.2, `Approved` (`WORK-176`). Explicitly does **not** cover
any implementation code, any service domain, ECS rule content, or the SRS/constitution amendment
tracks (`WORK-181`, `WORK-182`).

## Status

`Open` — contract and rendering are `Approved`; the task is at the planning stage. The plan
(`tasks/task-LMS-CONTRACT-001-plan.md`) was regenerated from task spec v1.5 on 2026-11-19 and is
`in-progress` pending independent review completion and Gate 3 approval. The previous handoff file was missing
as of 2026-11-18 (verified); this file was recreated by `wf-plan` 2026-11-19.

| Skill | Date | Outcome |
|---|---|---|
| wf-task-noncode | 2026-11-11..16 | Task spec created and refined (v1.0→v1.5); six calibration choices recorded (`CALIBRATION-LMS-CONTRACT-001`) |
| wf-review | 2026-11-13..16 | Seven review passes; all findings closed in the authoritative artifact; spec `Approved` (`WORK-156`) |
| wf-plan | 2026-11-19 | Plan regenerated from v1.5 (this run); worktree `D:/hobby/specd-worktree/lms-contract-plan` created from `main` (`9022742`), branch `task/WORK-LMS-CONTRACT-001-plan` |

## Action items

1. **Verify `binding.yaml`** — the plan and handoff row re-points already exist in this change;
   `wf-implement` makes **no further** `binding.yaml` edit unless Gate 3 changes the wording (at
   Gate 3 the plan row's status flips to `ready-for-implement` citing the Gate 3 Decision). *Artifact:*
   `binding.yaml`. *Verified by:* parse + git diff shows the two rows only. *Owner:* `wf-implement`
   (verify-only).
2. **Fix the rendering's stale attribution lines** — three attribution-only edits, zero requirement
   change (rendering line 17 provenance `1.4` → `1.5`; §9 `(v1.4)` → `(v1.5)`; §8 "has never been
   approved" sentence). Rendering-class defect; the task specification (v1.5, `Approved`) wins.
   *Artifact:* `schema/final-academic-record.md`. *Verified by:* diff shows exactly those three
   line-class edits; no other change. *Owner:* `wf-implement`.
3. **Field-by-field conformance check** rendering ↔ task spec v1.5 (field tables §4.2/§4.4.1/§4.4.2;
   13-field canonical list in order; exclusion record; R-1/R-3/R-4 encoded, R-2 not encoded). Any
   divergence becomes a finding — never a silent edit. *Artifact:* verification notes in this
   handoff + the conformance table delivered by `wf-implement`. *Verified by:* independent review.
   *Owner:* `wf-implement`.
4. **Verification evidence pack** mapping AC-1…AC-9 to named evidence (per the plan's verification
   table). *Artifact:* this handoff, appended. *Verified by:* `wf-converge`. *Owner:* `wf-implement`.
5. **Plan review and approval** — submit the plan to `wf-review` (type: implementation/architecture planning artifact); on a clear verdict present it to the human for Gate 3; on approval record the
   approval Decision in the ledger and set the plan file to `status: ready-for-implement` (and flip
   the `binding.yaml` plan row to match). *Artifact:* `tasks/task-LMS-CONTRACT-001-plan.md`,
   `binding.yaml`, work ledger. *Verified by:* ledger Decision recorded; plan frontmatter
   `status: ready-for-implement`; binding row matches. *Owner:* `wf-review` → human Gate 3.

## Preconditions unmet

- None for planning. (The parent spec is `Approved`; the task spec is `Approved`.) The previous
  blocker — no codebase binding — is closed (`WORK-160`).
- Before `wf-implement` begins: the plan must reach `ready-for-implement` (Gate 2 + Gate 3).

## Open questions

1. `SRS Q-2` (`parent_transaction_id` format) — stays open, inherited by the contract as an opaque
   identifier; the parent governs if it resolves differently. Owner: domain owners (SRS §9).
2. `SRS Q-1` — answered in substance by Decision `WORK-179` (ECS mints and owns
   `GoverningRuleSetID`, 2026-11-19). Formal SRS annotation is pending `WORK-182` (proposed). The
   Approved contract's "Q-1 remains open" wording is **not** to be edited in this task. Owner: user
   + SRS Section 11 CR.
3. Retention posture — decided retain-all (`WORK-180`); constitution tension 1 remains open in the
   document until `WORK-181` (v1.4). Owner: user.

## Suggested skill run

Exact next step, in order:

1. Land this change (commit; human authorization): `spec-workspace/projects/blockchain-enabled-lms/
   tasks/task-LMS-CONTRACT-001-plan.md`, `.../tasks/task-LMS-CONTRACT-001-handoff.md`,
   `.../binding.yaml`. Verify the implementation worktree holds the regenerated plan:
   `git -C D:/hobby/specd-worktree/lms-contract-plan show HEAD:tasks/task-LMS-CONTRACT-001-plan.md`
   must show the regenerated (2026-11-19) body. Branch `task/WORK-LMS-CONTRACT-001-plan` fast-forwards
   to the landed commit. Why: without this, `wf-implement` reads the stale plan — the exact defect
   this regeneration exists to fix.
2. `@wf-review` — re-review after the Gate 2 findings are applied; artifact
   `tasks/task-LMS-CONTRACT-001-plan.md`; review type: implementation/architecture planning
   artifact. Why: expected to converge to Approved with comments; required before Gate 3.
3. (human decision) Gate 3 — approve the plan; record the approval Decision in the ledger; set the
   plan file `status: ready-for-implement` (and flip the `binding.yaml` plan row in the same change).
4. `@wf-implement` — worktree `D:/hobby/specd-worktree/lms-contract-plan`, branch
   `task/WORK-LMS-CONTRACT-001-plan`, task spec `WORK-LMS-CONTRACT-001`; source of truth is the
   regenerated plan file. Why: executes the plan; never re-derives intent.
5. `@wf-converge` — verify AC-1…AC-9 against the collected evidence (expected grep outcomes for
   AC-1/AC-5 are pre-recorded in the plan).
6. `@wf-commit` — task `WORK-LMS-CONTRACT-001`; push flag: **ask the human** (default no push
   without explicit authorization).

## Phase contributions

| Phase | Skill | Date | Outcome |
|---|---|---|---|
| Task authoring | wf-task-noncode | 2026-11-11..16 | Spec v1.0→v1.5; calibration recorded and reaffirmed |
| Review (×7) | wf-review (delegated, independent) | 2026-11-13..16 | All findings closed in-spec; spec `Approved` (`WORK-156`); contract + rendering Approved |
| Traceability fixups (SRS v1.2, capabilities, constitution v1.2/v1.3) | assorted | 2026-11-18 | Collection consistent; see `WORK-171/175/176/177/178` |
| Stale-plan regeneration | wf-plan | 2026-11-19 | Plan rewritten from v1.5; worktree recreated; handoff recreated |
| Independent review | wf-review | pending | Gate 2 on this plan |
| Approval | human Gate 3 | pending | Gate 3; Decision recorded in ledger |
| Implementation | wf-implement | pending | Binding/provenance/evidence per plan |
| Convergence | wf-converge | pending | AC-1…AC-9 verdict |
| Commit | wf-commit | pending | Commit + optional push; SHA recorded in ledger |
