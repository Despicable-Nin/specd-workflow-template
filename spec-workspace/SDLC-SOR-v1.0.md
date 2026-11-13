# 📜 SDLC SYSTEM OF RECORD (Framework Container)

**Document ID:** `FW-SOR-v1.0`
**Target Scope:** Foundational SDLC Operating System (The Framework Container)
**Completion Date:** Nov 11, 2026
**Reconciled:** Nov 13, 2026

> **Terminology.** "System of Record" is used here for the *specification artifact layer*
> (this repository's `spec-workspace/` and `generated-projects/`). It is **not** the same concept
> as the "System of Record" that `SRS_LMS_v1.0.md` Section 4.3 assigns to the LMS operational
> database. Two distinct scopes, one phrase - disambiguated here so the collision is not
> re-raised (ledger `WORK-026`).

---

## 1. Overview and Purpose

This document records the history, design, and physical implementation of the core **System of
Record (SOR)** infrastructure. It defines the rules, policies, and structural placeholders
necessary for *all* subsequent development within this system.

**State:** **COMMITTED.** Merged into `main` via PR #1 (head commit `4cdafc5`, merged
2026-11-11T09:05:53Z, merge commit `13d7b86`).

> **Prior claim corrected.** This document previously read *"COMPLETED AND COMMITTED (WORK-004)"*.
> `WORK-004` is a work-ledger item for an unrelated decision (a task-spec status contradiction) and
> was never this document's identifier. The `WORK-004-SCHEMA` identifier has been retired in favour
> of `FW-SOR-v1.0` to remove the collision (ledger `WORK-012`).

## 2. Core Principles & Directives

The entire OS is built upon these non-negotiable, protected invariants, logged in
`sdlc-framework/policies/protected_policy_reference.md`.

1. **Specification Before Implementation:** No code or task can proceed without an explicitly
   `Approved` Specification.
2. **Technology Agnosticism:** All `spec-workspace` files MUST remain language-agnostic.
3. **Evidence-Based Completion:** Every functional claim must point to verifiable evidence (PR SHAs,
   work ledger IDs, test passes).

## 3. Architecture Components & Skills

The system is composed of **11 atomic, callable skills**, each wired to a matching `@wf-` command
wrapper in `sdlc-framework/.opencode/commands/`:

| Skill | Command | Role |
|---|---|---|
| `wf-bootstrap` | `@wf-bootstrap` | Creates the project container and initial blueprint. |
| `wf-constitution` | `@wf-constitution` | Establishes the durable engineering principles that steer specifications. |
| `wf-state` | `@wf-state` | The read-only observer - discovers the actual current state. |
| `wf-reconcile` | `@wf-reconcile` | The consistency engine - detects conflicts, duplicates, fragmentation. |
| `wf-task-code` | `@wf-task-code` | Generates an implementation-ready specification for **coding** work. |
| `wf-task-noncode` | `@wf-task-noncode` | Generates an implementation-ready specification for **non-coding** work. |
| `wf-plan` | `@wf-plan` | Produces the implementation/technical plan from an approved task specification. |
| `wf-review` | `@wf-review` | The independent, evidence-based review gate. |
| `wf-implement` | `@wf-implement` | Executes the plan in the task worktree (Red -> Green -> Refactor). |
| `wf-converge` | `@wf-converge` | Verifies the implementation against the acceptance criteria. |
| `wf-commit` | `@wf-commit` | The authorized recorder of change. |

> **Prior claim corrected.** This document previously read *"7 atomic, callable skills"* and
> enumerated 6. Eleven skills and eleven command wrappers ship today (ledger `WORK-019`).

## 🔴 Physical Manifestation (The Scaffold)

Two distinct physical trees exist. The earlier version of this document conflated them and
described a scaffold that was never built.

### 3.1 `generated-projects/scaffold-project/` - the minimal scaffold

This directory is the placeholder for a project codebase and contains exactly:

* `AGENTS.md` - the scaffold's system-context note.
* `.gitkeep` - marks the directory as intentionally populated.

It does **not** contain `binding.yaml`, `policies/`, `skills/`, or `documentation/`. The earlier
manifest listing those four was never realised on disk (ledger `WORK-011`).

### 3.2 `sdlc-framework/` - where the framework components actually live

| Component | Location | Present |
|---|---|---|
| Policies | `sdlc-framework/policies/` | Yes - `protected_policy_reference.md` |
| Skills | `sdlc-framework/.opencode/skills/<id>/SKILL.md` | Yes - 11 skills |
| Commands | `sdlc-framework/.opencode/commands/wf-<id>.md` | Yes - 11 wrappers |
| Schemas | `sdlc-framework/schemas/` | Yes - `work_ledger_schema.json` |
| Documentation | `sdlc-framework/documentation/` | Yes |
| Tools | `sdlc-framework/tools/` | **README only** - the three utilities it names are not implemented (ledger `WORK-022`) |
| Workflows | `sdlc-framework/workflows/` | **README only** - the four blueprints it names are not implemented (ledger `WORK-022`) |

## 4. Specification Layer

The `spec-workspace/` tree follows the contract in `spec-workspace/AGENTS.md`:

* `spec-workspace/library/` - reusable, technology-agnostic artifacts. Capability specifications
  are still outstanding (`WORK-020`).
* `spec-workspace/projects/<project-name>/` - the complete specification collection for each
  project. The first live project, **Blockchain-Enabled LMS**, lives at
  `spec-workspace/projects/blockchain-enabled-lms/`.
* `spec-workspace/SDLC-SOR-v1.0.md` - this document.
* `spec-workspace/project-temp/work_ledger.yaml` - the persistent work ledger.

---

## 📈 Conclusion

The framework's policies, skills, commands, schemas, and documentation are complete and committed.
The minimal project scaffold exists and is tracked.

**What is not yet complete:** the `tools/` and `workflows/` utilities are named but unimplemented
(`WORK-022`); the `library/` capability specifications are absent (`WORK-020`); and no approved
project specification exists yet - the LMS parent spec remains `Draft` (`WORK-016`).

**The OS is stable. It is ready to carry its first live project specification through the review
gate.**
