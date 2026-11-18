# Blockchain-Enabled LMS — Codebase AGENTS.md

*(Project context and rules for the codebase. Subordinate to the root `AGENTS.md` and to
`generated-projects/AGENTS.md`; inherits their Rule 0.)*

## 1. What this directory is

The physical realization of the specification collection
`spec-workspace/projects/blockchain-enabled-lms/`. It holds **how** the system is built —
implementation code, and nothing else. It never holds **what** is intended; specifications,
contracts, and decisions live in the specification collection and are never copied here.

Status: **scaffold only.** No implementation code exists here yet. The directory and its
`binding.yaml` were created on 2026-11-17 under ledger items WORK-017 / WORK-035 (Decision
WORK-160). The first coding task — raised via `wf-task-code`, targeting this directory — decides
the source layout; do not improvise one.

## 2. Binding

`binding.yaml` in this directory points at the specification collection this codebase implements:
collection `SPEC-LMS-v1.0` v1.0, root spec `SRS-LMS-v1.0` v1.1 (`Approved`, `WORK-039`; v1.1 amends Section 9 Q-5 per Decision `WORK-167`),
project constitution `CONST-LMS-v1.0` v1.0 (`Approved`, `WORK-159`). This directory is invalid
without that pointer. `generated-projects/AGENTS.md` governs this tree.

## 3. Rules that bind any work here

* **Implementation code is written only by `wf-implement`**, inside a task worktree, against an
  approved task specification. No other skill writes source files here.
* **No code without an approved spec** (Protected Invariant I). Every task here cites its task
  specification, its plan, and its worktree.
* **The constitution binds this codebase.** `spec-workspace/projects/blockchain-enabled-lms/
  constitution.md` (CONST-LMS-v1.0 v1.0, Approved) is the durable engineering principles for this
  project — specification before implementation (P-11), evidence-based completion (P-9), explicit
  operation contracts over shared state (P-12), one normative contract per subject (P-14).
* **Domain boundaries are contracts.** The seven service domains (IAM, ECS, AMS, FRAS, ESS,
  GRA-Service, LGS — SRS Section 3.1) are closed decision-makers; the operational record store is a
  shared durable component with exactly two operations (SRS Sections 3.6–3.7). A domain that needs
  another's data calls that domain's operation. There is no shared state and no bypass read.
* **ECS is the rule authority; LGS is the proof authority; record authority is neither.** Do not
  author rule content in any other domain (SRS Sections 3.2, 3.3).
* **Finalized records are never mutated.** Corrections append new linked records
  (`parent_transaction_id`); see SRS Section 2.4 and the constitution.
* **Traceability:** every record that depends on a rule set names it; every approval names the
  approver; both are inside the digested canonical form (constitution P-4).
* **Technology choices belong here, not in specifications.** The specs are technology-agnostic by
  contract; this codebase may choose, but only through planning and implementation, recorded here.

## 4. Contents

| File | Purpose |
|---|---|
| `AGENTS.md` | This file. |
| `binding.yaml` | Pointer to the specification collection — mandatory. |

No source directories yet. The first implementation plan creates them.

## 5. Open items that bind future work here

* The first coding task decides the source layout and the build/test toolchain (via
  `wf-task-code` → `wf-plan` → `wf-implement`).
* `service-contracts.yaml` in the collection declares runtime bindings (IAM/LGS declared; other
  domains not-yet-specified; `blockchain-gateway` `domain: unresolved` — SRS Q-6, ledger
  `WORK-037`). None of this blocks the first task; it constrains it.
* The canonical-form contract (`WORK-LMS-CONTRACT-001` v1.5, Approved) and `CAP-CANONICAL-FORM`
  define the digest; implementation must not re-derive them.
