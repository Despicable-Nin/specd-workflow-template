# generated-projects/AGENTS.md

# Codebase Workspace Steward

*(This file governs where implementation code is created and what must exist for it to be
traceable. It is subordinate to the root `AGENTS.md` and inherits its Rule 0.)*

## Rule 0 applies here

Every skill touching this tree is bound by the root `AGENTS.md` Rule 0, including the
code-generation guardrail in root Section 4.

## 1. Purpose

Each subdirectory of this tree is a **project codebase** — the physical realization of a
specification collection. This tree holds **how** it is built. It never holds **what** is intended;
that lives in `spec-workspace/`.

| Tree | Holds | Never holds |
|---|---|---|
| `spec-workspace/` | Specifications, contracts, decisions | Implementation code |
| `generated-projects/` | Codebases, scaffolds, implementation | Specifications |

A specification is never copied into a codebase, and code is never copied into a specification.

## 2. Structure

```
generated-projects/
├── README.md
└── <project-name>/          # name MUST match spec-workspace/projects/<project-name>/
    ├── AGENTS.md            # project context and rules for the codebase
    ├── binding.yaml         # REQUIRED - references the spec collection id + version
    └── ...                  # the implementation
```

## 3. Rules

1. **One codebase per project**, named identically to its specification collection:
   `generated-projects/<project-name>/` binds to `spec-workspace/projects/<project-name>/`.
2. **`binding.yaml` is mandatory** in every codebase directory and must reference the stable id and
   version of the specification collection it implements. A codebase without a valid `binding.yaml`
   is untraceable and must not be built.
3. **`binding.yaml` carries only that pointer.** Runtime service dependencies belong in
   `service-contracts.yaml` inside the specification collection.
4. **`wf-bootstrap` creates a non-executable scaffold** here — directory, `AGENTS.md`,
   `binding.yaml`. Never source files.
5. **Implementation code is written only by `wf-implement`**, inside a task worktree, against an
   approved task specification. No other skill writes source files here.
6. A specification written into this tree is **misfiled** and must be moved back to the collection
   it belongs to.

## 4. Current contents

| Directory | State |
|---|---|
| `scaffold-project/` | Minimal placeholder scaffold — `AGENTS.md`, `.gitkeep`. No `binding.yaml`; it has no specification collection to bind to. |

## 5. Known gaps

* The **Blockchain-Enabled LMS** codebase does not exist. Its `binding.yaml` currently lives at
  `spec-workspace/projects/blockchain-enabled-lms/binding.yaml` because the codebase directory is
  undetermined — `WORK-017`, `WORK-030`.
* Candidate codebase locations exist in the repository (`lms-platform/`, `src/identity/`) and
  neither is an approved decision. Do not build in either until that is settled.
