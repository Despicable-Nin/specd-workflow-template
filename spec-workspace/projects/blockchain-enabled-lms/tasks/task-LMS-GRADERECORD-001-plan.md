---
skill: wf-plan
task_id: WORK-LMS-GRADERECORD-001
task_spec: spec-workspace/projects/blockchain-enabled-lms/tasks/task-LMS-GRADERECORD-001-noncode.md
task_type: noncode
repo: D:/hobby/specd-worktree/lms-graderecord-plan
base_branch: main
calibration: {1: C, 2: E, 3: D, 4: C, 5: A, 6: B}
workflow: C
decision: Gate 3 decision recorded 2026-11-19T18:54:42Z at the human's question prompt ("Approve as-is"): plan approved as drafted; Gate 2 review recorded as WORK-206 (verdict APPROVED WITH COMMENTS, no blocking findings); findings F-1..F-9 dispositioned as accept-as-is (NOT folded); status ready-for-implement (Decision WORK-207)
status: ready-for-implement
status: in-progress
pending: 
worktree: D:/hobby/specd-worktree/lms-graderecord-plan
branch: task/WORK-LMS-GRADERECORD-001-plan
---

# Plan — WORK-LMS-GRADERECORD-001

## Progress

| id | question | answer |
|----|----------|--------|
| calibration-1 | Plan output shape | C. Card first; layered tree only where it adds something the card cannot |
| calibration-2 | Understanding aid | E. Combination, but always visual-first |
| calibration-3 | Explanation budget | D. Explain everything, but collapsed and structured |
| calibration-4 | Workflow path | C. PLAN -> I REVIEW -> REVISE -> APPROVE -> IMPLEMENT |
| calibration-5 | Implementation chrome | A. Numbered step lines (Step 1/5, what changed), then the next slice waits |
| calibration-6 | Teach or orient | B. Orient me ("here's what exists and what we're changing") |

## Calibration

1. **Plan output shape** — compact card first; layered tree only where it adds something the
   card cannot. 2. **Understanding aid** — combination, always visual-first. 3. **Explanation
   budget** — explain everything, but collapsed and structured. 4. **Workflow path** — PLAN ->
   I REVIEW -> REVISE -> APPROVE -> IMPLEMENT. 5. **Implementation chrome** — numbered step lines,
   slice waits after each. 6. **Orientation target** — orient; presume the reader needs the
   map, not the lectures.

## Pending

- none

## Decisions

- Workflow C (PLAN -> I REVIEW -> REVISE -> APPROVE -> IMPLEMENT). The human reviews the plan; revise loop before approval; no challenge step.
- Implementation chrome A: numbered step lines; each slice waits.
- Posture B: orient — this file states the map; it is not a lecture.
- Explanation budget D: everything explained, but collapsed and structured.
- Plan output C: card first; layered tree only where the card cannot carry something.
- Worktree REUSED (created 2026-11-19 at the commit prompt, based on `main` @ `c68389d`; branch `task/WORK-LMS-GRADERECORD-001-plan`; now at `747bde0`; one worktree per task rule satisfied; never a second).
- Delegated Gate 2 review of the plan (2026-11-19, session `ses_e0c99b327ffea9IfBhaeJNB48n`, read-only): verdict **APPROVED WITH COMMENTS**, no blocking findings; F-1..F-9 recorded as ledger item `WORK-206` (`proposed`). Human disposed at the Gate 3 question prompt (2026-11-19): **approve as-is** — findings not folded into the plan content; F-1 (three→four re-checks), F-2 (stale tree-clean claim), F-3 (handoff status tokens), F-4 (commit-before-implement), F-5, F-6, F-7, F-8 (ledger drift drift noted), F-9 stand recorded in `WORK-206` only.
- Gate 3 plan-approval Decision recorded as ledger item `WORK-207`; plan `status: ready-for-implement`. F-4's source-of-truth-at-a-SHA precondition is satisfied by the commit carrying this file (and this note).

## Baseline

| Exists | State |
|---|---|
| Task spec `task-LMS-GRADERECORD-001-noncode.md` | **v1.3, Approved** (Gate 3, Decision `WORK-204`, 2026-11-19T18:15:32Z); four independent Gate 2 passes (pass 4 APPROVED WITH COMMENTS; F-01..F-13, F-201..F-208, F-301..F-303 applied and re-verified); 15 acceptance criteria (AC-1..AC-15); §13 contract; Appendix A FAR alignment; Sections 10/11 open questions and inherited caveats |
| Parent `SRS-LMS-v1.0` v1.3 | `Approved` (Gate 2 `WORK-192`; W-7/C-8 attendance landed 2026-11-19) |
| Calibration `CALIBRATION-LMS-GRADERECORD-001` | Gate 1 final; records registrar-first orientation, contract-spec-only shape, review + pre-check-walk verification, sibling-worktree preference (honoured), surface limited to `tasks/` + ledger, schema/ not off-limits but unused |
| Handoff `task-LMS-GRADERECORD-001-handoff.md` | Committed (state: `Approved`; action items; suggested run: this plan); F-10 placement resolved (artifacts in this worktree, committed on this branch) |
| Sibling contracts | `WORK-LMS-CONTRACT-001` (student-period record) Approved v1.5; `SCHEMA-LMS-FAR-v1.0` Approved v1.0.0; `WORK-LMS-FORMULARULES-001` (FormulaRules) Approved v1.2 and **converged/committed/pushed** — the records-only implement pattern this task mirrors |
| `service-contracts.yaml` | **Off-limits** (frozen by calibration choice 5); ECS row remains `not-yet-specified` (`WORK-202`); LGS row `declared`; GRA-Service `not-yet-specified` — no binding work is authorized for this task |
| Codebase `generated-projects/blockchain-enabled-lms/` | Scaffold only (`AGENTS.md` + `binding.yaml` re-pinned to v1.3); zero source; nothing here is authorized to change |
| Git | This worktree on `task/WORK-LMS-GRADERECORD-001-plan` @ `747bde0` (e69901e + SHA-record); upstream `origin/task/WORK-LMS-GRADERECORD-001-plan`; **0 ahead / 0 behind**; tree clean; `main` untouched at `c68389d` |
| Open questions | `WORK-196` remains for the Session/AttendanceRecord contract (this task closes its GradeRecord third only); `change_status` vocabulary owed to change control (Section 11 C-1); SRS Q-2 formats (C-2); Q-OWN-2 granularity accepted at Gate 3; retention Decision (tension 1) still owed |
| Preconditions | None for this plan. Downstream coding slices remain gated on `WORK-196` (Session/AttendanceRecord) |

**Orientation:** this task is records-only end to end — its approval was the gate; nothing remains to be built. The remaining work is verification and record-keeping executed by `wf-implement` against this plan, then `wf-converge`, then disposal of the handoff by `wf-commit`.

## Plan

**Objectives (trace to the task's acceptance criteria).** This task's only remaining deliverable is a clean, verified handoff of an already-approved artifact. The plan closes the records-only loop for `WORK-LMS-GRADERECORD-001`: re-verify the mechanical criteria on the committed file, cite the review evidence for the rest, refresh records, and dispose of the handoff after convergence. Nothing new is designed or built; Approved v1.3 is frozen. Traces: AC-1..AC-15 (all fifteen live or die with this slice).

**Orientation diagram.**

```
SRS v1.3 (Approved, WORK-192)
        │
        ▼
GradeRecord contract v1.3 (Approved — Gate 3 WORK-204)   ← this task
        │
        ▼
this plan (records-only verification) ──▶ wf-implement ──▶ wf-converge ──▶ wf-commit
        │                                    │                  │                │
        └─ evidence index inline             ├─ AC-4 re-scan    ├─ AC-1..15      └─ handoff deleted
                                             ├─ AC-10 re-grep   ├─ verdict       └─ commit/push at prompt
                                             └─ AC-7 re-check   └─ ledger
```

**Approach.** Workflow C: PLAN → (you) REVIEW → REVISE → APPROVE → IMPLEMENT. No challenge step. Implementation for this non-code task is decision application and record-keeping. No code is authorized. The plan file is the source of truth for `wf-implement`.

**Layers (non-coding split):**

1. **Configuration / Infrastructure — NONE.** `service-contracts.yaml` is off-limits for this task (calibration choice 5). No binding decision is open: ECS stays `not-yet-specified` (`WORK-202`), LGS `declared`, GRA-Service `not-yet-specified` — no flip, no rationale owed here. No `schema/` rendering is produced (calibration choice 2/5; available surface, unused).
2. **Specification — nothing.** The contract v1.3 is Approved and frozen; any change is an SRS §11 Change Request.
3. **Process / Documentation.** (a) Evidence index — inline in this file (below; no separate index document). (b) Handoff refresh at plan approval and at convergence. (c) Re-verify the mechanical ACs on the committed file at implement time. (d) Commits only at explicit human authorization; SHAs recorded in the ledger.
4. **Others.** No new files beyond this plan, the handoff refresh, and ledger items. No worktree changes (reused).

**Files touched.** `task-LMS-GRADERECORD-001-plan.md` (this file), `task-LMS-GRADERECORD-001-handoff.md` (refresh), `work_ledger.yaml` (new items only). **Off-limits:** SRS, constitution, CAP artifacts, `schema/final-academic-record.md`, FAR task spec, FormulaRules contract and its artifacts, `service-contracts.yaml`, the codebase, the contract spec body (v1.3 frozen).

**Data flow.** None — records and verification only.

**Verification strategy (AC → evidence).**

| AC | Evidence | When |
|----|----------|------|
| AC-1 | Path + frontmatter: `status: Approved`, `task_type: noncode`, v1.3 | implement re-check |
| AC-2 | Field-by-field §13.2/13.3 (type, card, null, semantics; identity opacity/stability) | Gate 2 passes (pass 3/4 verified in-text) |
| AC-3 | §13.4 stability/immutability/determinism clause; rule set identifier sufficient to reproduce | Gate 2 passes |
| AC-4 | Word-tokenizer re-scan on the committed v1.3; exclusions (i)–(iii); zero applicable hits (the §13.2 `weight`-row ordinal `12` is class (iii)) | implement re-check |
| AC-5 | §14 matrix; 20/20 fields cite anchors; no field cites nothing | Gate 2 passes (pass 4) |
| AC-6 | §13.1 ownership clause (GRA-Service sole writer; store home; never proof-committed) + SRS citations | Gate 2 passes |
| AC-7 | §7 adoption table vs `library/Capabilities/` frontmatter: TIMESTAMPFORMAT 1.1 ADOPT, SCHEMAVERSIONCONSTRAINT 1.1 ADOPT, USERID 1.1 ADOPT, STATUSENUMS 1.2 ADOPT, CANONICAL-FORM 1.0 DECLINE | implement re-check (versions still match) |
| AC-8 | Pre-check log from the review session (pass 4): Walk A A1–A5 OK; Walk B B1, B2, B4, B5 OK; B3 AMBIGUOUS — pre-dispositioned Section 11 C-1 (not a failure). AC-8's rule (any unlogged MISSING/AMBIGUOUS, or an uncarried pre-disposition, blocks Gate 3) is satisfied — B3's pre-disposition is carried | cite at converge |
| AC-9 | §0 registrar-readable (reviewer read-through, pass 4 N-clean) | cite at converge |
| AC-10 | Marker grep re-run on v1.3 (languages/DBMS/vendors/frameworks/protocols incl. json/http/grpc/websocket/sql); zero true hits (only the `service-contracts.yaml` filename and AC-10's own criterion text match) | implement re-check |
| AC-11 | §13.8 refusal clause; scoped to malformed/unknown/unsupported/predecessor-unknown; historical identifiers resolve (reproduction) | Gate 2 passes |
| AC-12 | §13.9 exhaustive over §13.2: 6/6 opacities; 2/2 enums; 2/2 UserIDs; iff-Finalized pair; iff-successor pair; terminal/no-write; linkage; formula application; W-flows — each exactly once (pass-4 re-walk) | cite at converge |
| AC-13 | `status` = Proposed/Finalized only; CAP-STATUSENUMS v1.2 + SRS §2.9; direct-`Finalized` appeal successor; no `Superseded` state (pass-4 verified) | cite at converge |
| AC-14 | Sections 10/11 register: every caveat/question has owner + disposition; carried explicitly; none silently resolved (pass-4 verified) | cite at converge |
| AC-15 | Appendix A vs `schema/final-academic-record.md`: 20/20 fields mapped incl. `schema_version`; type-identical where mapped; record-local markings honest (pass-4 verified) | cite at converge |

**Evidence pack** = the pointer set above (pass-4 session `ses_e0cbb1527ffeW7RRPph0CQYj6u` + implement-time re-checks). `wf-converge` maps each AC to it; never re-derives beyond the three implement-time checks.

**Risks.** (1) Any "fix" to the Approved contract during execution — forbidden; remedy is SRS §11 CR. (2) Commit/push without explicit authorization — will not happen; asked at the prompt each time. (3) Re-deriving evidence that the reviews already validated — mitigated: only AC-1/AC-4/AC-7/AC-10 re-run; the rest are cited. (4) Handoff deleted prematurely — no: deletion only by `wf-commit` after `wf-converge` returns CONVERGED. (5) Divergence between plan/handoff/ledger — mitigated: each records the other by id.

## Out of scope

- Implementation code — none exists or is authorized; `wf-task-code` territory, separate tasks.
- `service-contracts.yaml` — off-limits; no ECS/GRA-Service binding flip (`WORK-202` pattern; named-component rule unsatisfied).
- Edits to SRS, constitution, capabilities, FAR contract/rendering, FormulaRules contract, Session/AttendanceRecord or GradeRecord spec bodies — Approved/frozen or other owners' tasks (`WORK-196`, `WORK-181`, `WORK-182`).
- `schema/` rendering for GradeRecord — deliverable set excludes it (calibration choices 2/5).
- `change_status` vocabulary, `transaction_id`/`parent_transaction_id` formats — change-control items (Section 11 C-1/C-2); not decided here.
- Session/AttendanceRecord contract, retention Decision (constitution tension 1), LGS-name-collision note (F-13) — other tasks.
- Push or merge — explicit authorization at the prompt; PR creation not requested and not done.
