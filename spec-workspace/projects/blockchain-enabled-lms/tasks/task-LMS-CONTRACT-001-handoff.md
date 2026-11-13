# Handoff: `final_academic_record` Schema Definition (v1.1)

**Task ID:** `WORK-LMS-CONTRACT-001`
**Task spec:** `tasks/task-LMS-CONTRACT-001-noncode.md` (v1.1)
**Parent spec:** `../SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, v1.0, `status: APPROVED`)
**Task type:** `noncode`
**Task status:** `Draft` - not yet reviewed, not yet approved
**Handoff status:** `Open`

> This is the task's **single common handoff file**. Contributing skills (`wf-review`, `wf-plan`,
> `wf-implement`, `wf-converge`, `wf-commit`) append their phase contribution here while the
> handoff status is not `Done`.

## Task scope summary

**Goal.** Define the canonical data contract (schema) for the `final_academic_record` payload for
the Blockchain-Enabled LMS - the single, fully validated input the Ledger Service (LGS) requires
to commit an immutable proof of grade finalization.

**In scope.** Mandatory fields, data types and nullability; structured encapsulation for
service-specific payloads (`EnrollmentDetail`, `GradeAssessment`); schema versioning and
compatibility rules; the mandatory ECS validation rules; audit linkage back to the originating
transaction record.

**Out of scope.** Any microservice logic, data transformation, or database migration script. This
task defines the target structure only.

**Normative rendering.** `schema/final-academic-record.md` renders this contract. The **task
specification is authoritative**; where the two disagree, the task specification wins and the
rendering is the defect.

## Acceptance criteria

Carried from the task specification Section 5 and rendered in
`schema/final-academic-record.md` Section 7:

1. Basic Achievement (Primary School) fields populate correctly with minimum progression metrics.
2. Advanced Achievement (College) stores cumulative weighted GPA and total credits, calculated with
   the version-specific formula linked by `GoverningRuleSetID`.
3. The Grade Appeal/Correction workflow appends a full `AppealRecord` carrying a mandatory
   `parent_transaction_id` matching the original record's ID.
4. Schema validation enforces the presence and correct format of the top-level `schema_version`.
5. Submitting a record with an unsupported `schema_version` results in a **controlled rejection**
   by the LGS validator.

## Current state and why this handoff was rewritten

The previous version of this handoff stated `Task Status: Approved / Worktree Active`, named
`wf-task-code` as the mandatory next step, and cited worktree commit `e062913`. All three were
wrong and have been corrected:

- **Status.** The task specification carried `status: Approved` with no approval Decision recorded
  in the work ledger, and its body had been reduced to frontmatter only. The body was restored from
  git blob `58f2453`; the status is `Draft` until a `wf-review` approval Decision exists
  (ledger `WORK-009`).
- **Next skill.** `wf-task-code` is the *coding* skill and states "This skill is for coding work
  only". This is a `noncode` task whose scope explicitly excludes implementation code. The correct
  sequence is below.
- **Worktree.** Branch `feat/final-record-schema` was merged via PR #1 on 2026-11-11 and is no
  longer active. The referenced commit `e062913` is two commits behind the branch head `4cdafc5`.

## Worktree

| Field | Value |
|-------|-------|
| Path | `D:\hobby\specd-worktree\lms-contract-plan` |
| Branch | `task/WORK-LMS-CONTRACT-001-plan` |
| Base branch | `main` |

The prior worktree `D:/hobby/specd-worktree/final-record-schema` (`feat/final-record-schema`) was
merged and retired. One worktree per task is a hard rule; this task needs its own.

## Suggested skill run (mandatory next step)

**The parent specification comes first.** A task specification may not be `Approved` ahead of its
parent, so this task's review gate cannot open until `SRS_LMS_v1.0.md` is approved.

Since the parent specification SRS_LMS_v1.0 is **APPROVED** (WORK-039 at SHA 167af69), the
gate is already cleared. The correct sequence is:

| # | Skill | Parameters | Why |
|---|---|---|---|
| 1 | `wf-review` | project `Blockchain-Enabled LMS`, artifact `SRS_LMS_v1.0.md` | Parent spec already APPROVED (WORK-039), gate cleared — no blocking findings remain |
| 2 | *(human approval)* | parent spec `SRS-LMS-v1.0` | `wf-review` produces a verdict; only the human grants approval. The Decision is recorded in the work ledger. |
| 3 | `wf-review` | project `Blockchain-Enabled LMS`, artifact `tasks/task-LMS-CONTRACT-001-noncode.md` | Task specification review; blocking findings should be resolved per modifications for F-02, F-03, F-06. Since modifications are complete, this review should return **Approved** |
| 4 | `wf-plan` | project `Blockchain-Enabled LMS`, task `WORK-LMS-CONTRACT-001` | Calibrates the plan, creates the task worktree from `main`/`master`, writes the plan file that `wf-implement` follows. *Already completed — plan file exists at `tasks/task-LMS-CONTRACT-001-plan.md`* |
| 5 | `wf-implement` | worktree (created at step 4), task `WORK-LMS-CONTRACT-001` | Executes the plan in the task worktree using Red → Green → Refactor. *Next step* |
| 6 | `wf-converge` | task `WORK-LMS-CONTRACT-001` | Verifies the implementation against the acceptance criteria with collected evidence. *Next step after implementation* |
| — | **Push flag:** | No. Await explicit human confirmation before any push. |

## Preconditions still unmet

These block this task and are tracked in the work ledger:

- `WORK-009` — no approval Decision recorded for this task (resolved per workflow: Decision to be recorded after human approval)
- `WORK-020` — the four adopted capabilities (`UserID`, `TimestampFormat`, `StatusEnums`,
  `SchemaVersionConstraint`) have no defining artifact anywhere in the repository. The task spec
  depends on them normatively. *Interim SRS Section 9 definitions now provided (see task spec modifications)*.
- `WORK-005` / `WORK-024` — GoverningRuleSetID authority unresolved, and the task's
  in-scope boundary overlaps the ECS rule-definition domain owned by SRS Sections 3.2 and 3.3.
  *Resolved per modifications: task spec In-Scope narrowed, GoverningRuleSetID authority cited as ECS per SRS 3.1.*

## Unresolved open questions

Carried forward (also recorded in the task specification frontmatter):

1. Official source/authority for populating the `GoverningRuleSetID` field (ECS vs GRA-Service).
   *Resolved: ECS per SRS 3.1*
2. Data format/standard for `parent_transaction_id` across all participating services.
   *Resolved: UUIDv4*

## Phase contributions

| Phase | Skill | Date | Outcome |
|-------|-------|------|---------|
| Planning | wf-plan | [current date] | Calibration choices recorded: 1A, 2E, 3B, 4A, 5A, 6C; plan file created; worktree created from main; handoff file created |
| Review | wf-review | [pending] | To verify task specification approval and implementation |
| Implementation | wf-implement | [pending] | To execute plan in task worktree using Red → Green → Refactor |
| Convergence | wf-converge | [pending] | To verify implementation against acceptance criteria |
| Commit | wf-commit | [pending] | To create authorized commit with explicit push confirmation |

---