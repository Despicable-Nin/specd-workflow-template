# Handoff: `final_academic_record` Schema Definition (v1.1)

**Task ID:** `WORK-LMS-CONTRACT-001`
**Task spec:** `tasks/task-LMS-CONTRACT-001-noncode.md` (v1.1)
**Parent spec:** `../SRS_LMS_v1.0.md` (`SRS-LMS-v1.0`, v1.0, `status: Draft`)
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
|---|---|
| Path | *to be created* |
| Branch | *to be created* per the `wf-task-noncode` calibration (choice 4) |
| Base branch | `main` |

The prior worktree `D:/hobby/specd-worktree/final-record-schema` (`feat/final-record-schema`) was
merged and retired. One worktree per task is a hard rule; this task needs its own.

## Suggested skill run (mandatory next step)

**The parent specification comes first.** A task specification may not be `Approved` ahead of its
parent, so this task's review gate cannot open until `SRS_LMS_v1.0.md` is approved.

| # | Skill | Parameters | Why |
|---|---|---|---|
| 1 | `wf-review` | project `Blockchain-Enabled LMS`, artifact `SRS_LMS_v1.0.md` | The parent spec was rewritten on 2026-11-13 to close 14 blocking findings. It needs a fresh independent verdict before it can be approved. |
| 2 | *(human approval)* | parent spec `SRS-LMS-v1.0` | `wf-review` produces a verdict; only the human grants approval. The Decision is recorded in the work ledger. |
| 3 | `wf-review` | project `Blockchain-Enabled LMS`, artifact `tasks/task-LMS-CONTRACT-001-noncode.md` | Seven blocking findings remain on this task spec (`WORK-062`, `WORK-064`…`WORK-069`) and can only be closed once the parent is approved. |
| 4 | `wf-plan` | project `Blockchain-Enabled LMS`, task `WORK-LMS-CONTRACT-001` | Calibrates the plan, creates the task worktree from `main`/`master`, writes the plan file that `wf-implement` follows. |
| 5 | `wf-implement` | worktree (created at step 4), task `WORK-LMS-CONTRACT-001` | Executes the plan in the task worktree using Red -> Green -> Refactor. |
| 6 | `wf-converge` | task `WORK-LMS-CONTRACT-001` | Verifies the implementation against the acceptance criteria with collected evidence. |

**Push flag:** No. Await explicit human confirmation before any push.

## Preconditions still unmet

These block this task and are tracked in the work ledger:

- `WORK-009` - no approval Decision recorded for this task.
- `WORK-062` - the parent specification is not `Approved`. **This blocks everything below.**
- `WORK-020` - the four adopted capabilities (`UserID`, `TimestampFormat`, `StatusEnums`,
  `SchemaVersionConstraint`) have no defining artifact anywhere in the repository. The task spec
  depends on them normatively.
- `WORK-005` / `WORK-024` - the `GoverningRuleSetID` authority is unresolved, and the task's
  in-scope boundary overlaps the ECS rule-definition domain owned by SRS Sections 3.2 and 3.3.

## Unresolved open questions

Carried forward (also recorded in the task specification frontmatter):

1. Official source/authority for populating the `GoverningRuleSetID` field (ECS vs GRA-Service).
2. Data format/standard for `parent_transaction_id` across all participating services.

## Phase contributions

| Phase | Skill | Date | Outcome |
|---|---|---|---|
| Reconciliation | `wf-reconcile` | 2026-11-13 | Task spec body restored; status corrected to `Draft`; handoff rewritten; contract consolidated under `schema/final-academic-record.md`; project collection relocated to the canonical root. |
| Review | `wf-review` | 2026-11-13 | Two independent review sessions. Both returned NOT APPROVABLE - 22 blocking findings on the parent spec, 8 on this task spec. Recorded as `WORK-039`…`WORK-078`. |
| Remediation | `wf-reconcile` | 2026-11-13 | Parent specification rewritten to the `wf-bootstrap` contract; all 14 of its blocking findings closed (`WORK-040`…`WORK-053`). This task spec's seven remaining blocking findings stay open until the parent is approved. |
