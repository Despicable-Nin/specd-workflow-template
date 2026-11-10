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

## 4. Instruction Precedence Policy:
1. Protected Framework Invariants (Highest)
2. Explicit User Instructions (Highest override)
3. [project-specific AGENTS.md]
4. [sdlc-framework/AGENTS.md]
5. Global Defaults (Lowest)

## 5. Recommended Initial Action:
Run: `opcode project-init` to begin building a new project from scratch.