# Calibration Record — task-LMS-FORMULARULES-001-noncode

`CALIBRATION-LMS-FORMULARULES-001`  |  status: **final** (Gate 1 — user confirmed "Final" 2026-11-19T13:19:31Z+)
Created: 2026-11-19T13:19:31Z  |  Skill: `wf-task-noncode`  |  Project: `blockchain-enabled-lms`
Task spec (once finalized): `task-LMS-FORMULARULES-001-noncode.md`  |  Task id: `WORK-LMS-FORMULARULES-001`

Answers recorded bindingly by the user, 2026-11-19, one at a time, no defaults assumed.

| # | Choice | Answer (verbatim decision) |
|---|--------|-----------------------------|
| 1 | Task shape | Field-level contract spec: FormulaRules. Contract defines the **structure and semantics only** — NO formula content, NO weights. Analogous to WORK-LMS-CONTRACT-001's shape. Scope: the rules container GRA-Service consumes under SRS §2.3/C-6. |
| 2 | Evidence / deliverables | Contract spec + task file only. No separate rendering document; fields/cardinality live inline in the spec. |
| 3 | Verification depth | Independent review (wf-review) PLUS a mandatory **downstream conformance pre-check**: 1–2 consumers (attendance / GradeRecord / GRA-Service) simulated on paper to catch cross-contract mismatch early. |
| 4 | Workflow path | **Worktree inside the repo** at `.worktrees/<task-slug>` (task-slug e.g. `lms-formularules-plan`), branch `task/WORK-LMS-FORMULARULES-001-plan` (or `task/task-LMS-FORMULARULES-001` — exact name finalized at `wf-plan`), base `main`. Preferences only — `wf-plan` creates the worktree from `main`/`master`, honouring this preference. |
| 5 | Implementation surface | Task spec + calibration + handoff + ledger appends **and** a decision about `service-contracts.yaml` ECS binding rows (e.g. flipping `ecs` from `not-yet-specified` to `declared`) is in-scope for this task. OFF-LIMITS: the SRS (never modified by this task), the constitution, the five CAP artifacts, the existing `final_academic_record` contract and its rendering, the codebase. |
| 6 | Orientation target | Stakeholders + implementer: plain-language executive summary (registrar / academic office audience) alongside the normative body. |

## Binding notes

- SRS is off-limits — no Section 11 CR may be smuggled into this task. Any SRS change is its own CR.
- No ECS rule content is authored by this task, ever: the contract defines the container; the weights/thresholds/aggregation stay ECS-owned.
- Deliverable is technology-agnostic (Protected Invariant II). No stack, storage, or protocol named.
- This is a **non-coding** task. Code is never written under this task; any slice that needs code spawns a separate coding task via `wf-task-code` after the contract is Approved.
- Parent-spec explicit targeting (Step 3) and Approved-status check (Step 4) follow finalization.
- Downstream: `wf-plan` (worktree creation) → task spec review (wf-review) → Gate 3 approval.
