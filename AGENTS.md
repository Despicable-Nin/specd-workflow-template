# Root Workspace AGENTS.md

# Global Engineering Operating System Policies and Defaults
*(This file defines the global configurable defaults and must be kept minimal, only referencing the framework components.)*

## 1. Protected Invariants & Architecture:
This space enforces global constraints (e.g., Specification Before Implementation, Technology Agnosticism). All policies are managed via the
[sdlc-framework/policies/protected_policy_reference.md] artifact.

## 2. Global Model Routing Defaults:
*   **Planner:** qwen3.8-q4_K_M
*   **Reviewer:** ornith:latest
*   **Discovery:** gemma4:latest

## 3. Tool Integration Overview:
Custom tools are limited to what OpenCode provides or what is defined in the [sdlc-framework/tools/].

## 4. SDLC Skills & Commands:
The eleven SDLC skills live in `sdlc-framework/.opencode/skills/<skill-id>/SKILL.md` and are exposed as `@wf-` commands in `sdlc-framework/.opencode/commands/`:
- `wf-bootstrap` — project foundation from a natural-language description
- `wf-state` — read-only project state discovery
- `wf-reconcile` — specification consistency evaluation
- `wf-task-code` — coding task specification with test scenarios
- `wf-task-noncode` — non-coding task specification (docs, config, infra)
- `wf-review` — independent evidence-based review
- `wf-commit` — authorized commits and remote synchronization
- `wf-constitution` — project constitution (governance principles)
- `wf-plan` — implementation/technical plan from approved task spec
- `wf-implement` — Red -> Green -> Refactor implementation
- `wf-converge` — convergence verdict and loop completion

Usage documentation: [sdlc-framework/documentation/sdlc-skill-usage.md](sdlc-framework/documentation/sdlc-skill-usage.md)

## 5. Instruction Precedence Policy:
1. Protected Framework Invariants (Highest)
2. Explicit User Instructions (Highest override)
3. [project-specific AGENTS.md]
4. [sdlc-framework/AGENTS.md]
5. Global Defaults (Lowest)

## 6. Recommended Initial Action:
Run: `@wf-bootstrap` to begin building a new project from scratch.