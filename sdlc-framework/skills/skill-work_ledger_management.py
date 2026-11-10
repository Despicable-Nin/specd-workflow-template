# sdlc-framework/skills/skill-work_ledger_management.py

# Skill ID: [project-reconcile]
# Purpose: To ingest, validate, and update the centralized Work Ledger, establishing the single source of truth for project status.
# When to use: At the start of every substantial session (mandatory for [project-assess], [project-resume]).
# Inputs: None (Reads from the dedicated WorkLedger file in the current project context).
# Procedure:
# 1. Load the WorkLedger structure from the designated file path.
# 2. Traverse the repository context (Git status, open issues, TODOs, Project state).
# 3. Compare physical/external state against recorded ledger items.
# 4. Identify: NEW Discoveries, STATUS CHANGES, or FAILED/MISSING items.
# 5. Output the delta of changes and return the updated ledger structure.
# Decision Points:
# - Conflict Resolution: New discoveries are recorded as 'WORK-xxxx' (Proposed Status) and must be flagged for human review.
# - Data Cleansing: The skill MUST NOT auto-close items; items must be explicitly resolved/superseded.
# Approval Requirements: None (Read/Write access to the ledger file).
# Expected Outputs: A complete, updated Work Ledger object.
# Validation: Verify the history log includes the current session ID, a summary of changes, and the timestamp.