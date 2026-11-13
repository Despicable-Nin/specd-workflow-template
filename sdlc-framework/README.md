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
| Workflows | `workflows/` | High-level multi-step sequences (entry points for the user). **Placeholder** — the four blueprints it names are not yet implemented (ledger `WORK-022`). |
| Skills | `.opencode/skills/<skill-id>/SKILL.md` | Atomic, callable procedures. **11 shipped**: `wf-bootstrap`, `wf-constitution`, `wf-state`, `wf-reconcile`, `wf-task-code`, `wf-task-noncode`, `wf-plan`, `wf-review`, `wf-implement`, `wf-converge`, `wf-commit`. |
| Commands | `.opencode/commands/wf-<skill-id>.md` | OpenCode command wrappers (e.g., `@wf-bootstrap`) that delegate to the corresponding skill. **11 wrappers**, one per skill. |
| Schemas | `schemas/` | Structured data for framework artifacts (e.g., `work_ledger_schema.json`). |
| Documentation | `documentation/` | Usage guides, getting started, skill inventory. |
| Tools | `tools/` | Reusable programmatic utilities. **Placeholder** — the three utilities it names are not yet implemented (ledger `WORK-022`). |

## 🔄 End-to-End Flow

```
@wf-bootstrap <project description>
    ↓ (approved project spec + non-executable scaffold)
@wf-state <project>                          # optional: read-only state discovery
@wf-reconcile <project>                      # optional: specification consistency check
    ↓
@wf-task-code <project> <feature description>   |   @wf-task-noncode <project> <work>
    ↓ (task spec Draft -> @wf-review -> Approved + worktree + handoff with suggested skill run)
@wf-plan <project> <task spec ID>
    ↓ (implementation plan + independent review + human approval)
@wf-implement <project> <worktree> <task spec ID>
    ↓ (Red -> Green -> Refactor in the task worktree)
@wf-converge <project> <task spec ID>
    ↓ (acceptance criteria verified against evidence)
@wf-commit <project> <worktree> <task spec ID> [push yes/no]
```

`@wf-constitution` is invoked once per project, before or alongside `@wf-bootstrap`, to establish the
durable engineering principles that steer every later specification.

Disambiguation: `@wf-state` discovers current state (read-only); `@wf-reconcile` evaluates specification consistency; `@wf-review` performs independent evidence-based reviews; `@wf-plan` turns an approved task specification into an implementation plan; `@wf-converge` verifies the result against the acceptance criteria.

## 📖 Further Reading

- [documentation/sdlc-skill-usage.md](documentation/sdlc-skill-usage.md) — how to invoke every skill/command.
- [documentation/getting_started.md](documentation/getting_started.md) — first-project setup and first-feature workflow.
- [policies/protected_policy_reference.md](policies/protected_policy_reference.md) — the definitive protected invariants.
