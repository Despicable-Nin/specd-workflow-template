# Handoff: final_academic_record Schema Definition (v1.1)

**Task ID:** WORK-LMS-CONTRACT-001
**Parent Spec:** SRS_LMS_v1.0.md
**Task Status:** Approved / Worktree Active
**Worktree Path:** d://hobby/specd-worktree/final-record-schema
**Branch Name:** feat/final-record-schema
**Base Branch:** main
**Worktree Commit:** e062913

## 📐 Task Scope Summary
**Goal:** Define the canonical data contract (schema) for the `final_academic_record` payload for the Blockchain-Enabled LMS.
**In-Scope:** Defining mandatory fields, data types, versioning, audit linkage (`parent_transaction_id`), ECS governance (`GoverningRuleSetID`), and schema versioning.
**Out-of-Scope:** Writing any implementation code, data transformation scripts, or migration scripts (Task Type: noncode).

## ✅ Acceptance Criteria Summary
The contract is considered complete when:
1.  Basic and advanced academic achievements are correctly mapped across service domains.
2.  Appeal workflows are formalized with mandatory audit linkage (`parent_transaction_id`).
3.  The schema enforces mandatory versioning (`schema_version`) and ECS rule citation (`GoverningRuleSetID`).

## ⚙️ Suggested Skill Run (MANDATORY NEXT STEP)
The task specification is approved and the worktree is active. The next logical step is to implement the data contract as code within this isolated environment.

*   **Suggested Skill:** `wf-task-code`
*   **Parameters:**
    *   Project Name: Blockchain-Enabled LMS
    *   Task Spec ID: WORK-LMS-CONTRACT-001
    *   Worktree Path: d://hobby/specd-worktree/final-record-schema
    *   Branch: feat/final-record-schema
    *   Push Flag: No (awaiting human confirmation before push)
*   **Rationale:** The contract is defined; now it must be translated into language-specific, testable code artifacts within the dedicated worktree.

## ❓ Unresolved Open Questions Carried Forward
1.  Official source/authority for populating the `GoverningRuleSetID` field.
2.  Confirmation of the data format for `parent_transaction_id` across all participating services.
