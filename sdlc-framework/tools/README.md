# Tools Directory

This folder contains specialized, reusable programmatic utilities that support the workflow. Tools
should encapsulate complex, repeatable operations that cannot be achieved purely through a single
agent call or simple skill.

## Key Tools

> **Status: planned — not implemented.** None of the utilities below exist on disk. This directory
> currently contains this README only. Tracked as ledger `WORK-022`.
>
> The utilities were previously listed here without qualification, which read as a claim that they
> existed. Under Protected Invariant III (Evidence-Based Completion) every functional claim needs
> verifiable evidence; each entry below is therefore explicitly marked with its real state.

| Utility | Responsibility | State |
|---|---|---|
| `worktree_manager.tool` | Lifecycle of parallel worktrees (create, list, switch, safe removal). | **Not implemented** |
| `policy_checker.tool` | Programmatically verifies adherence to protected policies before critical state changes. | **Not implemented** |
| `git_state_analyzer.tool` | Gathers deep, canonical diff and history data at a specific point in time. | **Not implemented** |

Until these are implemented, the equivalent operations are performed directly by the skills using
ordinary Git commands. `wf-commit` is the primary consumer of worktree lifecycle operations.
