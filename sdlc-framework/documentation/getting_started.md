# 🧭 Getting Started: The First Project
## 1. Introduction
Welcome to the OpenCode SDLC OS. This system requires a minimum of three components to operate: The Codebase, The Specification, and The System.

## 2. Initial Setup (Prerequisite)
Run: `@wf-bootstrap`
*   **Expected Result:** This establishes the approved project specification and non-executable scaffold (for a new project).
*   **Action:** The user must wait for the system to pause and explicitly approve the specification.

## 3. Workflow Execution: Building a Feature
Follow this sequence:
1. Start the flow: `@wf-task-code` (coding work) or `@wf-task-noncode` (non-coding work).
2. Discovery/State: The system runs `@wf-state` and presents findings.
3. Specification (Manual/Draft): The user provides initial requirements $\rightarrow$ The system drafts the specification via `@wf-bootstrap` and reviews it independently via `@wf-review`.
4. **🛑 GATE POINT:** The system stops. The user must review the draft specification and manually approve it to proceed.
5. Planning: Task specification creation via `@wf-task-code` / `@wf-task-noncode`.
6. Execution: Implement against the approved task spec, then `@wf-commit`.

## Key Commands:
*   **Check Status:** `@wf-state`
*   **Signal Completion:** `@wf-commit`
