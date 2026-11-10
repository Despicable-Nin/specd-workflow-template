# spec-workspace/AGENTS.md

# Specification Workspace Steward
*(This file manages the discovery, storage, and retrieval of all knowledge, decoupled from code implementation.)*

## 1. Purpose (System Functionality)
This workspace manages all reusable and project-specific specifications, ensuring they are technology-agnostic records of intent.

## 2. Directory Structure & Purpose:
*   **[library/]:** Contains general, reusable, technology-agnostic artifacts. Cannot reference implementation details.
    *   Engineering/
    *   Capabilities/
    *   ...
*   **[projects/]:** Contains the unique, complete specification collection for each project.
    *   `project-a/`: Complete spec for Project A (Intake, Constitution, etc.)
    *   `project-b/`: Complete spec for Project B

## 3. Key Process (Specification Lifecycle):
The system must enforce the state machine: `Draft -> In_Review -> Approved -> Superseded`. The `wf-bootstrap` skill creates project specifications, and `wf-review` acts as the independent review gate before approval. Task specifications are created by `wf-task-code` and `wf-task-noncode`, each subject to `wf-review` approval before implementation.

## 4. Data Integrity (Binding):
The `binding.yaml` file in a project's codebase directory must reference the stable ID and version of the specification collection residing here. This ensures the codebase is traceable to its required definition.