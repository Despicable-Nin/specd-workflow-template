# sdlc-framework/AGENTS.md

# SDLC Framework Core Policies and Tools
*(This file defines global operational capabilities and is a System-Level Component.)*

## 1. System Principle: Role, Skill, and Flow Separation
The Framework Agents define the *system* roles (Orchestrator, Implementer). They do not perform the work directly; they orchestrate the execution of defined Skills.

## 2. Core Components:
*   **Policies:** [policies/]: Defines reusable governance rules (e.g., `policy_specification_gate.md`).
*   **Workflows:** [workflows/]: High-level sequences (e.g., `workflow_new_feature.md`).
*   **Skills:** [.opencode/skills/]: Atomic, callable procedures (e.g., `wf-bootstrap`, `wf-task-code`, `wf-review`, `wf-commit`). Each skill has its own `SKILL.md`.
*   **Commands:** [.opencode/commands/]: OpenCode command wrappers (e.g., `@wf-bootstrap`, `@wf-review`) that delegate to the corresponding skill.
*   **Schemas:** [schemas/]: Defines the structured data for artifacts (e.g., `work_ledger_schema.json`).
*   **Documentation:** [documentation/sdlc-skill-usage.md]: Usage guide for all SDLC skills and commands.

## 3. Component Interaction:
The Orchestrator uses a Skill hook to call functions/blueprints, enforcing the correct Agent roles for the execution context.

## 4. Core Policy Enforcement:
All components must enforce the Protected Invariants defined in the system roots. The [sdlc-framework/policies/protected_policy_reference.md] is the definitive source.

## 5. Dependencies:
This framework requires the ability to manage Git Worktrees and utilize the OpenCode WorkLedger API at all times.