# Generated Projects

Each subdirectory here is a **project codebase** - the physical realization of a specification
collection. It is deliberately kept separate from `spec-workspace/`, which holds only *what* is
intended, never *how* it is built.

## Contract

| Rule | Detail |
|---|---|
| One directory per project | Named after the project, lowercase and hyphenated (e.g. `blockchain-enabled-lms`). |
| `binding.yaml` required | Must reference the stable ID and version of the project's specification collection in `spec-workspace/projects/<project-name>/`. This is what makes a codebase traceable to its definition (`spec-workspace/AGENTS.md` Section 4). |
| Non-executable scaffold at creation | `wf-bootstrap` creates a scaffold only - never implementation code. Code appears via `wf-implement`, inside a task worktree, against an approved task specification. |
| `AGENTS.md` | Declares the project context and the rules that apply inside the codebase. |

## Current contents

| Directory | Contents | State |
|---|---|---|
| `scaffold-project/` | `AGENTS.md`, `.gitkeep` | Minimal placeholder scaffold created by the framework bootstrap phase. No `binding.yaml` yet - it has no specification collection to bind to. |

## Not yet created

The **Blockchain-Enabled LMS** codebase does not exist yet. Its specification collection is at
`spec-workspace/projects/blockchain-enabled-lms/`, and its `binding.yaml` currently lives there
because the codebase directory is undetermined. Two candidate locations exist in the repository -
`lms-platform/` (four empty directories) and `src/identity/` - and neither is an approved
decision. Tracked as ledger `WORK-017` and `WORK-030`.
