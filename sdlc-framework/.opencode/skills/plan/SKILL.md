---
name: wf-plan
id: wf-plan
version: 2.0.0
description: Create an implementation/technical plan from an approved task specification, using the plan-fix calibration pattern - six consumption choices asked one at a time, recorded bindingly in a single run file, no defaults assumed. Always creates the task worktree from the main/master base branch and the task handoff file. The plan file is the source of truth for wf-implement, for coding and non-coding tasks alike.
category: planning
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-plan

## Purpose

Create an implementation/technical plan from an approved task specification, tracing planned work
back to the approved task acceptance criteria and the approved parent project specification.

The plan file this skill produces is the **single source of truth for `wf-implement`** — the same
way a `plan-fix` run file is the RAG for `implement-fix`. It serves coding and non-coding tasks
alike. `wf-implement` reads the plan file and follows it; it does not re-derive intent from the
task spec.

## Rule 0 — AGENTS.md binds this skill, always

This skill is bound by the nearest applicable `AGENTS.md` — the repository root `AGENTS.md`, plus
the `AGENTS.md` of any ancestor directory of every path this skill reads or writes. **Read them
before the first action.**

* **Silence is not permission.** A step in this skill that says nothing about a location, a name,
  or a placement rule does not authorise improvising one. The `AGENTS.md` still governs.
* **Conflict.** Protected Invariants > explicit user instruction > `AGENTS.md` > this skill. Where
  this skill and an `AGENTS.md` disagree, follow the `AGENTS.md`, state the conflict, and record
  it in the work ledger. Do not silently pick a side.
* **Hard stop.** If an `AGENTS.md` rule cannot be satisfied — the canonical folder is missing, a
  required `binding.yaml` is absent, the target path is ambiguous — stop, name the violated rule,
  and record a `Blocker` in the work ledger under the Gate Failure Protocol. Never improvise a
  location.
* **Handoff.** Before acting, look for the task's handoff file at its canonical location and read it if it exists - it is the task's running state (purpose, status, action items, next step). A handoff file is **disposable**: when its status becomes `Done` it is deleted, not archived, and the durable history stays in the work ledger. A handoff belongs inside the directory of the work it describes.
* **Code authority.** this skill writes a plan only. It never writes implementation code. It
  creates a worktree and a handoff file, but the worktree it creates stays empty of
  implementation.

## Invocation Conditions

Invoke when:

- An approved task specification exists (via `wf-task-code` / `wf-task-noncode`) and planning is
  required before implementation.

Do not invoke when:

- No task specification is approved (use `wf-task-code` / `wf-task-noncode` first).
- A plan already exists and is `ready-for-implement` — do not re-plan an approved plan.

## Preconditions

- Approved task specification at
  `spec-workspace/projects/<project-name>/tasks/task-<task-id>-<type>.md` with `status: Approved`.
- Approved parent project specification.
- A clean git working tree, or explicit acknowledgement that uncommitted work will be carried.

## Required Context

- Approved task spec ID and content.
- Approved project specification.
- The task's existing handoff file, if any — read it before planning.
- Existing implementation (read-only).

## Inputs

| Input | Description | Default |
|---|---|---|
| Task spec ID | Approved task to plan for | Required |
| Project name | Project the task belongs to | Task spec's `project` |
| Scope | Planning scope | Task scope |
| Base branch | Branch the worktree is created from | `main`, else `master` |

## Outputs

| Output | Location | Description |
|---|---|---|
| Plan run file | `spec-workspace/projects/<project-name>/tasks/task-<task-id>-plan.md` | The calibration record and the plan. One file, both roles. |
| Worktree | Per calibration, based on the base branch | Isolated working directory for the task |
| Branch | Named from the task ID | e.g. `task/WORK-LMS-CONTRACT-001-plan` |
| Task handoff file | `spec-workspace/projects/<project-name>/tasks/task-<task-id>-handoff.md` | Created or updated with purpose, status, action items, and the suggested next run |
| Review findings | Work ledger (`ReviewFinding` items) + reviewer output | Evidence-based findings from `wf-review` |
| Approved plan | Same plan file, `status: ready-for-implement` | Human approval recorded in the ledger |

## Agent Responsibilities

- Calibrate the plan's shape with the human before drafting it. **No defaults are assumed.**
- Derive the plan strictly from the approved task spec and parent spec.
- Create the worktree and the handoff file **before** the plan is drafted.
- Submit the plan to independent review (`wf-review`, type `architecture` / `implementation`).
- Enforce the approval gate before implementation.
- Never write implementation code.

---

## The calibration pattern

This skill uses the `plan-fix` pattern. The mechanics are load-bearing:

* **One run file, created before anything is asked.** It is created or resumed *before* the first
  question, and it is the only file this skill writes during calibration.
* **The file is the memory.** On every later turn, read the file first. A reply answers the
  `pending` question. Never guess which question they mean.
* **Record the open question before waiting.** Set `pending`, add the Progress row with an empty
  answer, then wait.
* **Record the answer before asking the next.** Write the answer, clear `pending`, then set the
  next `pending`.
* **Every question is a choice list**, asked one at a time via the `question` tool. Never stack
  questions. Never ask an open question with no options. The last option is always exactly
  `Other.. type your thoughts`.
* **All six calibration questions are asked in one consolidated turn**, before the baseline
  write-up.
* **Status stays `in-progress`** until the human says the plan is done. Only then is the plan
  filled, `decision` set, and `status` moved to `ready-for-implement`.

### The six calibration choices

Asked together, in one turn, each with `Other.. type your thoughts` last.

1. **Plan output shape** — how the plan should be presented.
   * A. Compact card: objective, approach, files touched, verification, risks
   * B. Layered tree: the implementation layers, with steps under each
   * C. Card first; layered tree only where it adds something the card does not
   * D. Other.. type your thoughts

2. **When you need to understand something** — the understanding aid.
   * A. Diagram
   * B. Short bullets
   * C. Code or artifact excerpt
   * D. Diff
   * E. Combination, but always visual-first
   * F. Other.. type your thoughts

3. **Agent explanations** — the explanation budget.
   * A. 3–5 bullets maximum
   * B. Short explanation + diagram
   * C. Only explain when something is ambiguous or risky
   * D. Explain everything, but collapsed and structured
   * E. Other.. type your thoughts

4. **Workflow path** — how the plan reaches implementation.
   * A. PLAN → APPROVE → IMPLEMENT
   * B. PLAN → I THINK → AI CHALLENGES ME → REVISED PLAN → APPROVE → IMPLEMENT
   * C. PLAN → I REVIEW → REVISE → APPROVE → IMPLEMENT
   * D. Other.. type your thoughts

5. **Implementation chrome** — how implementation should be reported back.
   * A. Numbered step lines (`Step 1/5`, what changed), then the next slice waits
   * B. `Implementing...` for the slice, then one concise final visual summary. Stop.
   * C. Layer by layer — one layer fully verified before the next begins
   * D. Other.. type your thoughts

6. **Teach or orient** — the posture of the explanation.
   * A. Teach me ("here's why this approach works")
   * B. Orient me ("here's what exists and what we're changing")
   * C. Hybrid (teach only when the concept is important, new, or risky)
   * D. Other.. type your thoughts

The human may answer all six in one string (`AAAAAA`, `1A 2D 3B 4C 5A 6B`, `[A,A,A,A,A,A]`).
Record all of them, then proceed.

---

## The plan run file

One file, created or resumed before the first question, at
`spec-workspace/projects/<project-name>/tasks/task-<task-id>-plan.md`. It carries both the
calibration record and the plan. **Do not create a second file.** `wf-implement` reads this same
file.

```markdown
---
skill: wf-plan
task_id: <WORK-XXX>
task_spec: spec-workspace/projects/<project-name>/tasks/task-<task-id>-<type>.md
task_type: <coding | noncode>
repo: <absolute git toplevel>
base_branch: <main | master>
calibration: {1: <letter or empty>, 2: <>, 3: <>, 4: <>, 5: <>, 6: <>}
workflow: <A|B|C or empty>
decision: <empty until chosen>
status: in-progress
pending: <question id or empty>
worktree: <path or empty>
branch: <name or empty>
---

# Plan — <task id>

## Progress

| id | question | answer |
|----|----------|--------|
| calibration-1 | Plan output shape | |

## Pending

- id: calibration-1
- prompt: Plan output shape
- options: A. ... / Other.. type your thoughts

## Decisions

<the chosen path and why; unknowns still open; in-scope paths; out of scope>

## Calibration

<the six answers, with the human's own wording where they supplied one>

## Baseline

<what exists today: relevant files, modules, contracts, and the state of the task spec>

## Plan

<empty until the human says the plan is done>

## Out of scope

<explicitly excluded, with the reason>
```

`status` takes exactly two values in this skill: `in-progress` and `ready-for-implement`.

---

## Step-by-Step Procedure

### Step 1 — Load approved inputs

Read the approved task spec and the approved parent project specification; record their IDs and
versions. Read the task's existing handoff file if one exists.

### Step 2 — Create or resume the plan run file

Create `tasks/task-<task-id>-plan.md` with the frontmatter and skeleton above, `status:
in-progress`, and `pending: calibration-1`. If the file already exists, **resume it**: read its
`pending` field and continue from there. Never overwrite a different run.

### Step 3 — Calibration (six questions, one turn)

Present all six calibration questions together as a single consolidated prompt, each with
`Other.. type your thoughts` last. Use the `question` tool where available. Record all six
answers in the file's `calibration` map and the Progress table. Clear `pending`.

### Step 4 — Baseline

Read-only survey of what exists: relevant source files, modules, contracts, existing
specifications, and the state of the task's acceptance criteria. Present the baseline in the
calibrated shape (choice 1). **Do not invent paths** — every path cited must exist.

### Step 5 — Create the worktree and branch

Create the task worktree **from the base branch** (`main`, else `master`) — this happens before
the plan is drafted, not after.

1. Resolve the base branch: use `main` if it exists, otherwise `master`. Record it in the file's
   `base_branch`.
2. Create the branch from the base branch: `git worktree add <path> -b <branch> <base-branch>`.
   Use `-b` — creating the branch in the same step avoids Git's `invalid reference` failure when
   the branch name is already checked out elsewhere.
3. Verify the worktree is linked and clean: `git worktree list`, `git -C <path> status`.
4. Record `worktree` and `branch` in the plan file.
5. **One worktree per task.** If a worktree already exists for this task ID, reuse it and say so;
   never create a second.

### Step 6 — Create or update the handoff file

Create (or update) `tasks/task-<task-id>-handoff.md`. It must satisfy the handoff contract in the
root `AGENTS.md` Section 5: **purpose**, **status**, and **action items** — each action item stating
what to do, which artifact it touches, how it is verified, and which skill owns it — plus
preconditions unmet, open questions, the suggested skill run with exact parameters, and a
phase-contributions table.

The handoff lives inside the directory of the work it describes, and it is **disposable**: once its
status becomes `Done`, `wf-commit` deletes it. Do not rely on it as a permanent record — put
anything that must survive in the work ledger.

### Step 7 — Draft the plan

Draft the plan into the run file's `## Plan` section, in the calibrated shape (choices 1, 2, 3, 6).
It must contain:

* **Objectives** — traced to the task's acceptance criteria.
* **Approach** — the chosen path and why (choice 4 may require a challenge step first).
* **Implementation layers**, divided as:
  * coding task: **UI**, **API / Services**, **Repository**, **Others**
  * non-coding task: **Specification**, **Configuration / Infrastructure**, **Process / Documentation**, **Others**
* **Files touched** — every path, and which are off-limits.
* **Data flow** — where it applies.
* **Verification strategy** — how each acceptance criterion is checked, and what evidence proves it.
* **Risks** — what breaks if this is wrong.

`## Out of scope` lists everything excluded, with the reason.

**Leave `## Plan` empty and `status` as `in-progress` until the human confirms.** Propose the plan
in chat first; do not treat the chat copy as the artifact.

### Step 8 — Present the plan and stop

Present the full plan in chat. Then ask exactly one selection:

`Is this plan done?`

| Option | Action |
|--------|--------|
| Done | Fill `## Plan` from the proposal they approved. Set `decision` and `status: ready-for-implement`. Clear `plan-done`. Then ask Step 10. |
| STOP | Record the answer. Clear `pending`. Stop. Leave `status: in-progress`. |
| Other.. type your thoughts | Revise the proposal from their text. Update the file. Ask `plan-done` again. Do **not** set `ready-for-implement`. |

### Step 9 — Independent review

Submit the plan to `wf-review` (type `architecture` or `implementation`). The reviewer must
challenge assumptions, missing requirements, defects, regression risks, and unnecessary
complexity — and must not simply agree. Record each actionable finding as a `ReviewFinding` work
ledger item with status `proposed`.

If the review returns blocking findings: the plan stays `in-progress`, the findings are recorded,
and the plan is revised with the human. **Do not advance to `ready-for-implement`.**

### Step 10 — Approval gate and handoff

Once the review is clear, present the plan and the findings to the human. On approval:

1. Record the approval as a `Decision` work ledger item — the plan's ID, version, approver,
   timestamp, and path.
2. Set the plan file's `status: ready-for-implement` and record `decision`.
3. Update the handoff file: status, the new action items, and the suggested next run.

Then steer to `wf-implement` with the plan file path, the task spec path, the worktree path, and
the branch. **Do not start implementation in this skill.** Ask whether to run `wf-implement`; the
plan file is the deliverable, and implementation is the next step, not a requirement.

---

## Decision Rules

| Rule | Statement |
|---|---|
| Calibration is binding | The six answers are recorded and followed. Do not re-ask, do not assume, do not substitute a default. |
| Traceability | Every plan element traces to an approved task acceptance criterion. |
| No scope creep | The plan must not add unapproved scope. |
| Worktree first | The worktree is created from the base branch before the plan is drafted. |
| Plan is the RAG | `wf-implement` follows this file. It does not re-derive intent from the task spec. |
| Approved before implement | Implementation begins only after plan approval. |
| One worktree per task | Never two. Reuse or escalate. |
| One handoff per task | The handoff file is created here and appended to by every later skill. |

## Delegation Strategy

- Independent review: delegated to `wf-review`.
- Implementation: delegated to `wf-implement`, on this plan file.

## Approval Gates

| Gate | What | Who |
|---|---|---|
| Gate 1 | Calibration confirmed | Human |
| Gate 2 | Draft plan review | Reviewer agent / `wf-review` |
| Gate 3 | Plan approval | Human |

## Safety Boundaries

- No implementation before plan approval.
- No unapproved scope in the plan.
- Never discard uncommitted work — if the tree is dirty, stop and report it.
- Never force-push.

## Error Handling

| Situation | Handling |
|---|---|
| Plan approval denied | Stop; plan stays `in-progress`; record a `Blocker`. |
| Review returns blocking findings | Plan stays `in-progress`; record `ReviewFinding` items; revise with the human. |
| Worktree already exists for this task | Reuse it; report the reuse; never create a second. |
| Branch already exists | Ask the user: new name, reuse, or abort. |
| Base branch is neither `main` nor `master` | Stop and ask which branch to base on. Record the answer. |
| Worktree creation fails | Record a `Blocker` in the work ledger. Do not proceed to planning. |
| The run file is missing but a plan was already approved | Stop. Do not re-plan an approved plan. |

## Validation

- Plan run file exists at the canonical path, with all six calibration answers recorded bindingly.
- Worktree exists, is linked, is clean, and is based on `main`/`master`.
- Branch and worktree paths recorded in the plan file.
- Handoff file exists and satisfies the handoff contract in the root `AGENTS.md`.
- Plan traces every element to an approved task acceptance criterion.
- Plan is divided into layers.
- Review findings recorded as `ReviewFinding` ledger items.
- Approval Decision recorded in the work ledger.
- `status: ready-for-implement` only after explicit human approval.
- No implementation code was written by this skill.
- No protected invariant was violated.

## Handoff Requirements

- Plan file path and version.
- Worktree path and branch.
- Handoff file path, with status and action items.
- Next recommended action: `wf-implement` with the plan file, task spec, worktree, and branch.

## Related Skills

- **wf-task-code / wf-task-noncode** — produce the approved task spec and the calibration record.
- **wf-review** — reviews the draft plan; its findings gate `ready-for-implement`.
- **wf-implement** — consumes this plan file as its source of truth.
- **wf-converge** — verifies the implementation against the task acceptance criteria.
- **wf-commit** — commits the work produced in the worktree.
