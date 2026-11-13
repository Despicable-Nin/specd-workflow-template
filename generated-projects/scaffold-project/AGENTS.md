# Scaffold Project — AGENTS.md

This directory represents the **physical scaffold** for the Foundational "System-of-Record"
architecture.

The scaffold is the minimal, necessary physical structure of the SDLC Operating System. It is a
**placeholder codebase**, not a project.

## Status

* **Scaffold:** `Done` — merged into `main` via PR #1 (head `4cdafc5`, merge commit `13d7b86`,
  2026-11-11).
* **Not a project collection.** It has no specification collection to bind to, so it has **no
  `binding.yaml`** — and per `generated-projects/AGENTS.md` a codebase without a valid
  `binding.yaml` must not be built upon. When a real project arrives, `wf-bootstrap` creates
  `generated-projects/<project-name>/` with a proper `binding.yaml`.

## Contents

| File | Purpose |
|---|---|
| `AGENTS.md` | This file — the scaffold's context note. |
| `.gitkeep` | Marks the directory as intentionally populated. |

The earlier manifest in `spec-workspace/SDLC-SOR-v1.0.md` claimed this scaffold also contained
`binding.yaml`, `policies/`, `skills/`, and `documentation/`. It does not. The real framework
component tree is `sdlc-framework/` (`WORK-011`).

## Rule 0 applies here

This directory is governed by the root `AGENTS.md` Rule 0 and by
`generated-projects/AGENTS.md`. In particular, **implementation code is written here only by
`wf-implement`**, inside a task worktree, against an approved task specification.
