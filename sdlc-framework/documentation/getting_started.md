# 🧭 Getting Started: The First Project
## 1. Introduction
Welcome to the OpenCode SDLC OS. This system requires a minimum of three components to operate: The Codebase, The Specification, and The System.

## 2. Initial Setup (Prerequisite)
Run: `opcode project-init`
*   **Expected Result:** This initializes the `project-temp/` directory and generates the initial, non-functional Work Ledger (WORK-002: Blockers).
*   **Action:** The user must wait for the system to pause and explicitly approve the initial framework specification.

## 3. Workflow Execution: Building a Feature
Follow this sequence in the console:
1. Start the flow: `opcode workflow-new-feature`
2. Discovery/Assessment: The system runs `skill-project-assess` and presents findings.
3. Specification (Manual/Draft): The user provides initial requirements $\rightarrow$ The system runs `skill-specification-create`.
4. **🛑 GATE POINT:** The system stops. The user must review the draft specification and manually approve it to proceed.
5. Planning: `opcode skill-plan-create`.
6. Execution: `opcode workflow-run-feature` (This invokes the TDD loop).

## Key Commands:
*   **Check Status:** `opcode script-session-bootstrap`
*   **Signal Completion:** `opcode skill-commit-and-pr-create`
