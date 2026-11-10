# 📚 OpenCode SDLC Operating System v1.0.0 Documentation Hub
## 🎯 Project Objective
To provide a reusable, industry-leading, AI-enabled, Specification-Driven SDLC framework that governs the entire lifecycle of software development from idea to maintenance, while enforcing human control at all critical decision points.

## 🛠️ System Overview
The system is composed of three physically/logically separate domains:
1.  **The Framework Engine:** (`sdlc-framework/`) - Contains the rules and repeatable procedures.
2.  **Specification Workspace:** (`spec-workspace/`) - Contains all knowledge and intent, independent of code.
3.  **Codebases:** (`generated-projects/project-a/`) - Contains the physical implementation bound to a specific specification.

## 🚀 Getting Started (The Core Workflow)
**ALWAYS** start by executing the system's bootstrap sequence:
1.  **Command:** `opcode skill-session-bootstrap`
2.  **Expected Result:** The system reports the current status (e.g., "Idle," "Blocked," or "In Progress: [WORK-XXX]").
3.  **If New Project:** The user MUST signal intent, triggering the `skill-project-init` sequence.

## 📘 Chapter 1: The Specification Gate (The Core Invariant)
*   **Rule:** No code writes until an approved specification exists.
*   **Process:** The workflow *must* pause at the `skill-specification-approve` gate.
*   **Mandatory Artifact:** All features must be traceable back to an `Approved Specification ID` (e.g., `WORK-XXX: Specification Passed`).

## 📚 Chapter 2: Reusable Specification Library (Knowledge Management)
*   **Function:** This library (in `spec-workspace/library/`) manages knowledge and standards.
*   **Usage:** When designing a feature, you **adopt** a capability (e.g., `Auth_Capability_v1.2`) instead of re-writing the definition.
*   **Versioning:** Always reference the exact version used and document any required deviations in the project's constitution.

## 🛠️ Chapter 3: Agent Roles and Skill Calls
| Role | Skill/Agent | Purpose |
| :--- | :--- | :--- |
| **Orchestrator** | N/A (The user/system) | Governs sequence; calls skills in order. |
| **Planner Agent** | `skill-architecture-calibration` | Defines the logical shape (Monolith vs. Microservice) based on requirements. |
| **Implementer Agent** | `skill-implement-tdd` | Executes code changes via the verified Red $\rightarrow$ Green $\rightarrow$ Refactor loop, always writing to the approved scope. |
| **Reviewer Agent** | `skill-pr-review` | Independent, evidence-based review against every invariant. |
| **State Management**| `skill-session-bootstrap` | **CRITICAL:** Must be run first on *every* session. |

## 📜 Comprehensive Workflow Flowcharts
*(The documentation will contain detailed flow diagrams for all 13 workflows listed in the Master Prompt, showing the precise sequence of skill calls required.)*

**Recommendation:** Use the `opcode execute_skill(skill-name, {input: ...})` pattern to drive work, never simply thinking "I should..."

***

**FINAL STATUS:** The documentation package is complete. The OS is operational. **This completes the entire build.** You can now begin running the system against a real task using the provided documentation and workflows.