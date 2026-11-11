# 🧭 SDLC Framework

The **Specification-Driven SDLC Framework** (`sdlc-framework/`) is a reusable, AI-enabled operating system that governs the lifecycle of software work — from idea to specification approval, planning, implementation, review, and commit — while enforcing human control at all critical decision points.

## 🏛️ Core Principles (Protected Invariants)

Enforced via [policies/protected_policy_reference.md](policies/protected_policy_reference.md) (non-overridable):

1. **Specification Before Implementation** — no code without an approved specification.
2. **Technology Agnosticism** — specifications are independent of any tech stack.
3. **Evidence-Based Completion** — no completion is claimed without verifiable evidence.

## 🧩 Framework Components

| Component | Location | Purpose |
|---|---|---|
| Policies | `policies/` | Reusable, non-overridable governance rules. |
| Workflows | `workflows/` | High-level multi-step sequences (entry points for the user). |
| Skills | `.opencode/skills/<skill-id>/SKILL.md` | Atomic, callable procedures (e.g., `wf-bootstrap`, `wf-task-code`, `wf-review`, `wf-commit`). |
| Commands | `.opencode/commands/wf-<skill-id>.md` | OpenCode command wrappers (e.g., `@wf-bootstrap`) that delegate to the corresponding skill. |
| Schemas | `schemas/` | Structured data for framework artifacts (e.g., `work_ledger_schema.json`). |
| Documentation | `documentation/` | Usage guides, getting started, skill inventory. |
| Tools | `tools/` | Reusable programmatic utilities (worktree lifecycle, policy checks, git state analysis). |

## 🔄 End-to-End Flow

```
@wf-bootstrap <project description>
    ↓ (approved project spec + non-executable scaffold)
@wf-task-code <project> <feature description>   |   @wf-task-noncode <project> <work>
    ↓ (approved task spec + worktree + handoff with suggested skill run)
[implementer writes code in worktree]
    ↓
@wf-commit <project> <worktree> <task spec ID> [push yes/no]
```

Disambiguation: `@wf-state` discovers current state (read-only); `@wf-reconcile` evaluates specification consistency; `@wf-review` performs independent evidence-based reviews.

## 📖 Further Reading

- [documentation/sdlc-skill-usage.md](documentation/sdlc-skill-usage.md) — how to invoke every skill/command.
- [documentation/getting_started.md](documentation/getting_started.md) — first-project setup and first-feature workflow.
- [policies/protected_policy_reference.md](policies/protected_policy_reference.md) — the definitive protected invariants.
