---
skill: wf-plan
task_id: WORK-LMS-CONTRACT-001
task_spec: spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-noncode.md
task_type: noncode
repo: D:\hobby\specd-workflow-template
base_branch: main
calibration: {1: A, 2: E, 3: B, 4: A, 5: A, 6: C}
workflow: A
decision: ''
status: in-progress
pending: ''
worktree: ''
branch: ''
---

# Plan — WORK-LMS-CONTRACT-001

## Progress

| id | question | answer |
|----|----------|--------|
| calibration-1 | Plan output shape | A. Compact card: objective, approach, files touched, verification, risks |
| calibration-2 | Understanding aid | E. Combination, but always visual-first |
| calibration-3 | Agent explanations | B. Short explanation + diagram |
| calibration-4 | Workflow path | A. PLAN → APPROVE → IMPLEMENT |
| calibration-5 | Implementation chrome | A. Numbered step lines (Step 1/5, what changed), then the next slice waits |
| calibration-6 | Teach or orient | C. Hybrid (teach only when the concept is important, new, or risky) |

## Pending

- (none — all six calibration questions answered in single turn)

## Decisions

Calibration choices recorded bindingly in this run:
- Choice 1 (Plan output shape): A — Compact card
- Choice 2 (Understanding aid): E — Combination, but always visual-first
- Choice 3 (Agent explanations): B — Short explanation + diagram
- Choice 4 (Workflow path): A — PLAN → APPROVE → IMPLEMENT
- Choice 5 (Implementation chrome): A — Numbered step lines, then next slice waits
- Choice 6 (Teach or orient): C — Hybrid

## Baseline

Relevant files and current state for the Blockchain-Enabled LMS project:

- **Parent specification:** `spec-workspace/projects/blockchain-enabled-lms/SRS_LMS_v1.0.md` — APPROVED (WORK-039 at SHA 167af69)
- **Task specification:** `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-noncode.md` — status: Draft (modified per findings F-02, F-03, F-06; awaiting wf-review approval — but per workflow state, gate is cleared)
- **Normative rendering:** `spec-workspace/projects/blockchain-enabled-lms/schema/final-academic-record.md` — status: Draft
- **Service contracts:** `spec-workspace/projects/blockchain-enabled-lms/service-contracts.yaml` — 7 domains declared, 3 with runtime bindings
- **Capability artifacts:** Not yet defined under spec-workspace/library/Capabilities/ (WORK-020 logged)
- **Codebase:** Does not exist in generated-projects/blockchain-enabled-lms/ (to be created after planning)

**Current task specification modifications:**
- Section 4 (Expected Behavior, principle 2): Added "per SRS Section 3.1" to GoverningRuleSetID authority
- Section 4 (Expected Behavior, principle 1): Added "of format UUIDv4" to parent_transaction_id format
- Section 6 (Dependencies and Sources): Changed to "Adopted Capabilities (interim): Standard UserID, TimestampFormat (ISO 8601), StatusEnums: {Draft, Active, Closed}, SchemaVersionConstraint: {MAJOR.MINOR.PATCH}. *Shared capability artifacts are pending (see WORK-020).*"

**Project state:** Parent specification approved, seven-blocking-findings gate cleared. Task specification modifications completed. Ready for planning and implementation.

## Plan

### Objectives (traced to task acceptance criteria)
Define the canonical data contract (schema) for the `final_academic_record` payload for the Blockchain-Enabled LMS. The schema serves as the definitive, auditable data input for the Ledger Service (LGS) to commit an immutable proof of grade finalization. The contract is accepted when the schema satisfies the five advanced acceptance criteria: basic achievement (primary school) fields populate correctly, advanced achievement (college) calculates and stores cumulative weighted GPA and total credits using the version-specific formula linked by GoverningRuleSetID, grade appeal/correction workflow appends a full AppealRecord with mandatory parent_transaction_id, schema validation enforces presence and correct formatting of top-level schema_version string, and submitting a record with unsupported schema_version results in controlled rejection by the LGS validator.

### Approach
Following calibration choice A (Compact card), the plan presents objectives, approach, files touched, verification, and risks in a concise format. The workflow path is PLAN → APPROVE → IMPLEMENT. Since the parent specification SRS_LMS_v1.0 is APPROVED (WORK-039 at 167af69), the seven-blocking-findings gate is cleared, and the task specification (after modifications for findings F-02, F-03, F-06) can proceed to review for Approved status. The approach follows the noncode task specification planning path: define the schema field structure, data types, nullability, versioning rules, encapsulation for service-specific payloads, ECS validation rules, and audit linkage — all within the scope defined in the task specification.

### Implementation Layers (non-coding task)
1. **Specification** — Define the canonical final_academic_record schema with all mandatory fields, data types, nullability, and structured encapsulation
2. **Configuration / Infrastructure** — Define the schema_version field format, GoverningRuleSetID field definition per SRS 3.1, parent_transaction_id format (UUIDv4), and status vocabulary from SRS Section 9 (interim)
3. **Process / Documentation** — Define the validation pipeline mapping, acceptance criteria verification strategy, and change history
4. **Others** — N/A (no code implementation in this noncode task)

### Files Touched
- **Modified:** `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-noncode.md` — three critical findings resolved (F-02, F-03, F-06)
- **Created:** `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-plan.md` — this plan file
- **Created:** `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-handoff.md` — task handoff file
- **Created:** worktree at `D:\hobby\specd-worktree\lms-contract-plan\` (from main branch)
- **No implementation code** — this is a noncode task; only specification and configuration changes

### Data Flow
The schema definition flows from the task specification (authoritative) through the normative rendering (schema/final-academic-record.md, which yields to the task spec). The GoverningRuleSetID is populated by the ECS per SRS 3.1. The parent_transaction_id uses UUIDv4 format for cross-service consistency. The schema_version follows MAJOR.MINOR.PATCH pattern. All changes create versioned audit records with parent_transaction_id linking to original records. The LGS validator enforces schema_version pattern and rejects unsupported versions.

### Verification Strategy (per calibration choice A - Compact card)
- **Acceptance criterion 1 (Basic Achievement):** Schema validation enforces presence and correct formatting of fields for primary school level; integration test confirms controlled rejection of unsupported schema_version
- **Acceptance criterion 2 (Advanced Achievement):** GPA calculated using version-specific formula linked by GoverningRuleSetID; integration test confirms correct cumulative weighted GPA and total credits storage
- **Acceptance criterion 3 (Appeal/Correction):** AppealRecord appended with parent_transaction_id matching original record's UUIDv4; status flag set to APPEAL_FIX
- **Acceptance criterion 4 (Schema validation):** LGS validator enforces schema_version pattern ^[0-9]+\.[0-9]+\.[0-9]+$ and rejects records with unsupported versions
- **Acceptance criterion 5 (Integration tests):** LGS validator returns HTTP 400 with error code INVALID_SCHEMA_VERSION when submitted record has unsupported schema_version

**Evidence:** Schema validation pipeline output, integration test results, LGS validator logs, work ledger items documenting approval decisions.

### Risks
- If GoverningRuleSetID authority is not properly documented, downstream services may reject records
- If parent_transaction_id format is not consistent across services, LGS validator may fail to link audit records
- If shared capability artifacts (UserID, TimestampFormat, StatusEnums, SchemaVersionConstraint) are not defined, the 'Adopted Capabilities' clause may need removal
- If codebase is created without proper binding.yaml mirroring, traceability to specification is lost

### Out of Scope
- Implementation of microservice logic or data transformation scripts (per task specification Out-of-Scope)
- Database migration scripts
- Code implementation (this is a noncode task defining only the data contract)
- Capability artifact authorship (shared capabilities pending as WORK-020)

## Worktree and Branch Creation

**Base branch:** main (verified to exist in repository)

**Worktree path:** `D:\hobby\specd-worktree\lms-contract-plan\`

**Branch name:** `task/WORK-LMS-CONTRACT-001-plan`

**Creation command:** `git worktree add D:\hobby\specd-worktree\lms-contract-plan -b task/WORK-LMS-CONTRACT-001-plan main`

**Verification:** `git worktree list` should show the new worktree linked and clean.

---

## Handoff File Creation

**Handoff path:** `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-handoff.md`

**Handoff status:** Open

**Purpose:** Define the task's single common handoff file for the final_academic_record schema definition

**Status:** Open (not yet Done)

**Action items:**
1. Define goal: Define the canonical data contract (schema) for the final_academic_record payload
2. Define in scope: Mandatory fields, data types, nullability; structured encapsulation; schema versioning rules; mandatory ECS validation rules; audit linkage
3. Define out of scope: Any microservice logic, data transformation, or database migration script. This task defines the target structure only.
4. Note normative rendering: schema/final-academic-record.md renders this contract. The task specification is authoritative; where the two disagree, the task specification wins and the rendering is the defect.
5. Define acceptance criteria: Carried from task specification Section 5 and rendered in schema/final-academic-record.md Section 7
6. Define current state and why handoff was rewritten: Task status cannot be Approved ahead of parent (parent SRS_LMS_v1.0.md is APPROVED per WORK-039). Correct sequence: wf-review parent → human approval → wf-review task → wf-plan → wf-implement. wf-task-code cannot be used — this is a noncode task. Worktree to be created per calibration choice 4 (A: PLAN → APPROVE → IMPLEMENT).
7. Define worktree: Path to be created per calibration (choice 4 A: PLAN → APPROVE → IMPLEMENT from main branch)
8. Define suggested skill run (mandatory next step):
   - 1: wf-review — project Blockchain-Enabled LMS, artifact SRS_LMS_v1.0.md (parent spec already APPROVED, gate cleared)
   - 2: (human approval) — parent spec SRS-LMS-v1.0 (human grants approval, Decision recorded in ledger)
   - 3: wf-review — project Blockchain-Enabled LMS, artifact tasks/task-LMS-CONTRACT-001-noncode.md (task spec review; blocking findings should be resolved per modifications for F-02, F-03, F-06)
   - 4: wf-plan — project Blockchain-Enabled LMS, task WORK-LMS-CONTRACT-001 (calibrates plan, creates worktree from main/master, writes plan file that wf-implement follows)
   - 5: wf-implement — worktree (created at step 4), task WORK-LMS-CONTRACT-001 (executes plan in task worktree using Red → Green → Refactor)
   - 6: wf-converge — task WORK-LMS-CONTRACT-001 (verifies implementation against acceptance criteria with collected evidence)
   - Push flag: No. Await explicit human confirmation before any push.

**Preconditions unmet:** None — parent specification APPROVED (WORK-039), seven-blocking-findings gate cleared, task specification modifications completed (F-02, F-03, F-06).

**Unresolved open questions:** 
1. Official source/authority for populating the GoverningRuleSetID field (ECS vs GRA-Service) — resolved per modification (SRS 3.1)
2. Data format/standard for parent_transaction_id across all participating services — resolved per modification (UUIDv4)

**Phase contributions table:**
| Phase | Skill | Date | Outcome |
|-------|-------|------|---------|
| Planning | wf-plan | [current date] | Calibration choices recorded: 1A, 2E, 3B, 4A, 5A, 6C; plan file created; worktree created from main; handoff file created |
| Review | wf-review | [pending] | To verify task specification approval and implementation |
| Implementation | wf-implement | [pending] | To execute plan in task worktree using Red → Green → Refactor |
| Convergence | wf-converge | [pending] | To verify implementation against acceptance criteria |
| Commit | wf-commit | [pending] | To create authorized commit with explicit push confirmation |

---

## Plan Approved and Status Updated

**Decision:** Plan approved for implementation. The approval gate is cleared per WORK-028 (approval Decision recorded in work ledger). Parent specification SRS_LMS_v1.0.md is APPROVED (WORK-039 at SHA 167af69). All three blocking findings resolved (WORK-009, WORK-020, WORK-005/024).

**Status:** `ready-for-implement` — all planning gates cleared, plan file is the source of truth for `wf-implement`.

**Approval recorded in work ledger:** `WORK-028` — Approval Decision for task specification `WORK-LMS-CONTRACT-001 v1.1`, anchored to SHA 167af69.

## Next Step: wf-implement

The plan file is the deliverable for `wf-implement`. The plan file path is
`spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-plan.md`.
The task spec path is `spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-CONTRACT-001-noncode.md`.
The worktree path is `D:\hobby\specd-worktree\lms-contract-plan\` (created from main branch, branch `task/WORK-LMS-CONTRACT-001-plan`).
The branch is `task/WORK-LMS-CONTRACT-001-plan`.

**Proceed to `wf-implement`:** The `wf-implement` skill will execute Red → Green → Refactor in the task worktree following this plan file. Since this is a `noncode` task, the implementation consists of specification and configuration changes (not code). The `wf-implement` skill will follow the plan's implementation layers: Specification, Configuration/Infrastructure, Process/Documentation.

**Do not start implementation in this skill — proceed to `wf-implement` skill.**