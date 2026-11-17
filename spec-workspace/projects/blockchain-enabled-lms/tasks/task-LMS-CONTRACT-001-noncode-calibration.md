---
id: CALIBRATION-LMS-CONTRACT-001
task_id: WORK-LMS-CONTRACT-001
task_type: noncode
project: blockchain-enabled-lms
record_type: calibration
status: Confirmed — user confirmed 6/6 calibration choices per seventh review bounded confirmation (CONFIRMATION: complete, session ses_e1c6c7735ffeqXQQMMMtpeM23un); approval Decision WORK-156 recorded 2026-11-16; 11/11 editorial corrections verified applied, no requirement changed.
created: 2026-11-16T08:04:22Z
updated: 2026-11-16T09:26:06Z
supersedes: none
---

# Calibration record — `WORK-LMS-CONTRACT-001`

## Provenance — read this first

**This record is retrospective.** Root `AGENTS.md` §8.4 requires the six calibration choices to be
asked one at a time, with no defaults assumed, and recorded bindingly *before* the artifact is
authored. That did not happen for this task: the specification was authored across several passes
and the calibration record was never created. `WORK-148` records the gap.

Two consequences, both stated plainly:

1. **The answers below are not claims about what was asked.** They record what the artifact
   actually implements, so that the choices are visible and reviewable rather than implicit.
2. **The values `1A/2E/3B/4A/5A/6C` in `task-LMS-CONTRACT-001-plan.md` are `wf-plan`'s
   consumption choices, not these answers.** They were never this record. Treating them as this
   record is what allowed `WORK-068` to be closed against unrelated text.

`status: Draft` until the user confirms or amends each choice. Confirmation belongs with the
approval Decision that closes `WORK-009`.

## The six choices

### 1. Task shape — what kind of non-code task is this?

**Implemented: documentation / specification.** A technology-agnostic data contract, plus its
normative rendering. No configuration, infrastructure, process or migration deliverable.

**Scope and blast radius.** Two normative artifacts — `tasks/task-LMS-CONTRACT-001-noncode.md` and
`schema/final-academic-record.md` — plus this calibration record, the handoff, and this task's
entries in `binding.yaml`. Downstream, the contract is consumed by the surfaces that assemble,
validate and prove the record, and by every service that reads a finalized student-period record —
so the
blast radius of a *wrong* contract is the whole record store. That is why the review bar is
document-level rigour rather than implementation testing.

**If amended:** a different shape would mean this is not the right skill, and the task should be
re-raised.

### 2. Evidence and deliverables — what concrete artifacts must exist?

**Implemented:**

| Deliverable | Path |
|---|---|
| Task specification | `tasks/task-LMS-CONTRACT-001-noncode.md` (v1.5) |
| Normative rendering — one complete schema | `schema/final-academic-record.md` |
| Field coverage table, with type, cardinality and nullability | Task specification Appendix A (27 fields) |
| Timestamp inventory | Task specification Appendix B (3 fields); mirrored in rendering §7 |
| Canonical field list and exclusion record | Task specification §4.5, §4.6; rendering §5, §6 |
| Calibration record | `tasks/task-LMS-CONTRACT-001-noncode-calibration.md` |

**If amended:** additional evidence artifacts would be added to §7 of the task specification.

### 3. Verification depth — how is correctness established?

**Implemented: independent document review.** No pipeline, no test harness, no demo. This is forced
by the task type: the deliverable is a specification, and building a validator would be
implementation, which §3 item 7 excludes. The reviewer checks each acceptance criterion against the
section it names, using the evidence the criterion identifies.

The rendering is a **structural** schema: it encodes field names, types, enumerations, required-ness
and closed field sets. Presence rules R-1, R-3 and R-4 are encoded; **R-2 is the only one not
encoded**, because it is a condition on when a record may be created rather than on its shape. The
task specification §7 names GRA-Service assembly and the LGS commit boundary as R-2's check points.

**If amended:** a deeper level — for example executing the schema against sample payloads — would
require a separate coding task under `wf-task-code`, not an extension of this one.

### 4. Workflow path — worktree, branch, placement

**Implemented:** isolated worktree at `D:/hobby/specd-worktree/lms-contract-plan`, branch
`task/WORK-LMS-CONTRACT-001-plan`, created from `main` by `wf-plan`. Recorded in the plan
frontmatter.

**Open issue.** `WORK-133`: `main` carries the task specification as `Approved` while the plan
branch carries it as `Draft`. One state must become authoritative before approval. That is a git
decision, not an edit, and it is the user's.

**Stale plan.** `I-02`: the plan file was written against v1.2 and still describes UUIDv4 identifiers
and an integration-test requirement that v1.4 removed. It is marked `stale` and must be regenerated
by `wf-plan` from v1.4 before any `wf-implement` run.

**If amended:** a different branch or placement is recorded here and honoured by `wf-commit`.

### 5. Implementation surface — what may this task touch, and what is off-limits?

**In bounds:**

- `tasks/task-LMS-CONTRACT-001-noncode.md`
- `schema/final-academic-record.md`
- `tasks/task-LMS-CONTRACT-001-noncode-calibration.md`
- `tasks/task-LMS-CONTRACT-001-handoff.md`
- This task's entries in `binding.yaml` — version, status and the calibration record

**Off-limits:**

- Any implementation code, anywhere. This tree holds specifications only (`spec-workspace/AGENTS.md` §1).
- ECS rule content — value domains for academic judgement (SRS §3.1).
- The canonical-form reduction rules, ordering rule and digest algorithm (`CAP-CANONICAL-FORM`).
- The canonical-form version and digest algorithm identifier — proof-level, not payload fields.
- Parent open questions Q-1 and Q-2 — a child cannot close a parent question.
- `AGENTS.md` files at any level. Rule 0 makes them read-only during a skill run without an
  approved documentation task covering them. `WORK-134` tracks the staleness this leaves behind.
- The parent SRS, except for editorial corrections already recorded (`WORK-140`, `WORK-138`).

### 6. Orientation target — who must understand this specification?

**Implemented:** two audiences, in this order.

1. **The implementer of the record-assembly and proof-commit validation surfaces**, who must be
   able to write a validator
   from this document alone — hence the explicit `required` lists, enumerations, cardinalities,
   nullability, closed field sets and the single complete schema.
2. **An independent verifier of a committed proof**, who must be able to re-derive the digest from
   the published payload plus the canonical field list, without access to the originating services
   (SRS §4.2 S-2). That requirement is why the record has no envelope: the published unit is the
   digested unit.

The document is therefore written as a normative contract, not as a narrative.

## Binding effect

Once confirmed, these six choices bind `wf-implement`, `wf-converge` and `wf-commit` for this task.
Any deviation is recorded here before it is acted on.
