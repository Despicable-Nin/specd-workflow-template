---
name: wf-task-noncode
id: wf-task-noncode
version: 1.3.0
description: Create an implementation-ready specification for a non-coding task (documentation, configuration, infrastructure, process, data migration setup). Follows the plan-fix calibration pattern: six choices asked one at a time, answers recorded bindingly, no defaults assumed, finalized only on explicit confirmation. Worktree creation parameters are decided during calibration (choice 4). Requires explicit project-spec targeting (never assumed). No code-level test scenarios (not applicable to non-coding work); measurable acceptance criteria are still required. Produces a task specification, a dedicated per-task worktree and branch, and a task handoff file that includes a suggested skill run.
category: task-specification
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-task-noncode

## Purpose
Create an implementation-ready specification for a **non-coding task** (documentation, configuration, infrastructure, process, data migration setup, etc.). Follows the `/plan-fix` calibration pattern: interactive choices asked one at a time, answers recorded bindingly, no defaults assumed, finalized only when you confirm. Worktree creation parameters (worktree needed, branch naming, worktree location) are decided during calibration choice 4. Produces a task specification with no code-level test scenarios but with measurable acceptance criteria, the worktree plan that `wf-plan` acts on, and a task handoff file that includes a **suggested skill run**.

This skill is for non-coding work only. For coding work (features, bug fixes, refactors, test additions), use wf-task-code instead.

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
* **Code authority.** this skill produces a **specification or a non-code artifact** only. It must **never** write implementation code — that is the defining constraint of a non-coding task. If the work turns out to require code, **stop**: raise a separate coding task via `wf-task-code` targeting `generated-projects/<project-name>/`, record the link in the work ledger and the handoff, and keep this task's deliverable a specification. Code never goes into `spec-workspace/`.

## Invocation Conditions
Invoke when:
- An approved project specification exists (wf-bootstrap produced it)
- User wants to implement a non-coding task
- No task specification exists yet for this work unit

Do not invoke when:
- No approved project specification exists (use wf-bootstrap first)
- The work is coding (use wf-task-code)

## Preconditions
- Approved project specification at `spec-workspace/projects/<project-name>/specification.md` with `status: Approved`
- Work ledger accessible
- Git repository accessible

## Required Context
- Project name or path
- Natural-language description of the non-coding work

## Inputs
| Input | Description | Source |
|-------|-------------|--------|
| Project name / path | Target project | User |
| Work description | Description of the non-coding work | User |
| Calibration answers | Six plan-fix-style choices, recorded bindingly one at a time | User (interactive) |
| Target project spec ID | Explicitly selected by user from presented options | User (interactive) |

## Outputs
| Output | Location | Description |
|--------|----------|-------------|
| Calibration run file | `spec-workspace/projects/<project-name>/tasks/task-<nnn>-noncode-calibration.md` | Binding record of the six calibration choices, including worktree plan from choice 4 |
| Draft task spec | `spec-workspace/projects/<project-name>/tasks/task-<nnn>-noncode.md` | `status: Draft` |
| Approved task spec | Same file, `status: Approved` | Approval evidence recorded in work ledger |
| Worktree plan | Calibration run file, choice 4 | Branch naming and placement **preferences** only. The worktree itself is created by `wf-plan`, from the `main`/`master` base branch. |
| Task handoff file | `spec-workspace/projects/<project-name>/tasks/task-<nnn>-handoff.md` | One per task, not per skill; contributing skills append while status != Done; includes detailed handoff + suggested skill run |
| Planned task summary | Console output + work ledger | Concise summary of the planned task: scope, acceptance criteria, worktree branch/path, suggested skill run |
| Work ledger items | Task created, calibrated, reviewed, approved, worktree-associated | NEW items only; existing items never modified or closed |

## Agent Responsibilities
- **Plan-fix calibration**: Ask six consumption choices one at a time (analogous to plan-fix's scan shape, visual aid, explanation budget, workflow, implementation chrome, teach or orient), adapted for non-coding work. Do not assume defaults. Wait for each answer before proceeding.
- Record each answer in the calibration run file; each answer binds subsequent steps.
- **Calibration choice 4 (workflow path)**: Capture worktree/branch *preferences* - whether a worktree is needed, branch naming preference, worktree placement preference. `wf-plan` creates the worktree from `main`/`master` and honours these preferences.
- Present the full calibration plan for finalization. Proceed to drafting only when you explicitly confirm the plan is done.
- **Explicit project-spec targeting**: Present all approved project specifications with ID/title/status/last-updated. User must select one. Never assume.
- Identify reusable capabilities from `spec-workspace/library/`
- Examine existing implementation (read-only only)
- Define scope, exclusions, expected behavior, acceptance criteria (non-code deliverables)
- Submit draft for independent review (wf-review)
- Obtain explicit human approval before worktree creation or implementation
- **Do not create a worktree or branch.** Hand the worktree plan to `wf-plan`, which creates both from the `main`/`master` base branch.
- Record the worktree plan (choice 4 preferences) in the work ledger and handoff file for `wf-plan` to act on
- **Generate a detailed task handoff file that includes a suggested skill run** (which skill to run next, with parameters); this is the task's single common handoff file; contributing skills append while its status is not Done
- **Present a summary of the planned task to the user** (scope, acceptance criteria, worktree branch/path, suggested skill run)
- Never write implementation code during this skill
- Never modify the approved project specification
- Never discard uncommitted work
- Never force-push by default

## File Emission Guardrail (artifact persistence)

Artifact-producing steps in this skill MUST persist files to the canonical paths below before any downstream step (draft review, approval, worktree association, handoff consumption) proceeds.

| Artifact | Canonical path | Requirement |
|----------|----------------|-------------|
| Task spec | `spec-workspace/projects/<project-name>/tasks/task-<nnn}-noncode.md` | Written as `status: Draft`; later changed to `Approved` only via explicit approval |
| Calibration run | `spec-workspace/projects/<project-name>/tasks/task-<nnn}-noncode-calibration.md` | All six answers recorded bindingly, incl. worktree plan from choice 4 |
| Task handoff | `spec-workspace/projects/<project-name>/tasks/task-<nnn}-handoff.md` | Common per-task handoff file — one per task, not per skill; contributing skills append while status != Done; must contain detailed handoff + suggested skill run with exact parameters |

Rules:
- Presenting artifact content in chat or returning it inline is NOT sufficient; the file must exist on disk at the canonical path.
- Create parent directories as needed; never write artifacts to ad-hoc locations.
- After writing, verify the file exists at the canonical path and contains the expected frontmatter before continuing.
- On write failure, missing file, or path mismatch: HARD STOP. Do not proceed to review/approval/next steps. Notify the user; record a `Blocker` in the work ledger (Gate Failure Protocol).

## Step-by-Step Procedure

### Step 1 — Plan-fix calibration (six choices, one at a time)
Ask each choice, wait for the answer, record it bindingly in the calibration run file. No defaults. Choices:

1. **Task shape**: What kind of non-coding work is this (documentation, configuration, infrastructure, process, data migration setup)? What is the estimated scope and blast radius?
2. **Evidence/deliverables**: What concrete deliverables must this task produce (documents, config files, infra provisioning, process records, sign-offs)?
3. **Verification depth**: How must the deliverable be verified (review sign-off, config validation, infra smoke test, stakeholder demo, compliance check)?
4. **Workflow path**: Does this require an isolated worktree (yes/no)? If yes: what branch naming preference? What worktree placement preference? This decision **is** the worktree plan — no separate worktree step later.
5. **Implementation surface**: Which existing docs, configs, infra definitions, or processes will this touch? Which are off-limits?
6. **Orientation target**: Who must understand this task spec (implementer, reviewer, stakeholder, future maintainer)?

### Step 2 — Finalize calibration plan
Present all six recorded answers to the user, including the worktree plan from choice 4. Ask: "Is this calibration plan final, or do you want to revise any choice?" Only proceed to Step 3 when you explicitly confirm the plan is final.

### Step 3 — Explicit project-spec targeting
List all approved project specifications for the project, each with: spec ID, title, status, last-updated timestamp. Ask the user to select which spec this task implements. Record the selected `parent_spec` ID.

### Step 4 — Verify selected spec is Approved
Confirm the selected spec has `status: Approved`. If not, error: direct the user to get the project specification approved first (this skill cannot proceed without an approved parent spec).

### Step 5 — Identify reusable capabilities
Scan `spec-workspace/library/` for capabilities applicable to this task. Record adopted capabilities and their versions in the task spec.

### Step 6 — Examine existing implementation (read-only)
Inspect `generated-projects/<project-name>/` for existing docs, configs, infra definitions, or processes relevant to this task. Identify dependencies and boundaries already established. Do not modify anything.

### Step 7 — Define scope and exclusions
State what is in-scope and what is explicitly out-of-scope for this non-coding task, informed by calibration choices 1, 5, and 6.

### Step 8 — Establish expected behavior
Describe expected behavior in technology-agnostic terms. Reference the sections of the approved project specification this task implements.

### Step 9 — Define measurable acceptance criteria
Create measurable, testable criteria that determine when the task is complete. Focus on non-code deliverables (documents published, config applied, infra provisioned, process documented, sign-off obtained). Each criterion must be independently verifiable. No vague criteria.

### Step 10 — Omitted: code-level test scenarios
Code-level test scenarios (the Gherkin-style Given/When/Then scenarios required by `wf-task-code`)
are not applicable to non-coding work, and this step is intentionally skipped for this skill.

This does **not** mean the task specification has no verifiable criteria. Step 9's measurable
acceptance criteria are required and must be independently verifiable. Where a non-code deliverable
is itself a contract, schema, or document that mandates a future integration test — for example, a
data contract that must state how an unsupported `schema_version` is rejected by a downstream
validator — that requirement belongs in the acceptance criteria as part of the *deliverable*, not
as an implementation task. See ledger `WORK-021`.

### Step 11 — Establish verification requirements
Specify how the deliverable will be verified (review sign-off, config validation, infra smoke test, stakeholder demo, compliance check) and what evidence is required for completion.

### Step 12 — Draft task specification
Create `spec-workspace/projects/<project-name>/tasks/task-<nnn>-noncode.md` with YAML frontmatter:

```yaml
---
task_id: WORK-<nnn>-TASK-NONCODE
version: 1.0
status: Draft
project: <project-name>
parent_spec: WORK-<nnn>-SPEC
task_type: noncode
calibration_file: task-<nnn>-noncode-calibration.md
created: <ISO-8601 timestamp>
updated: <ISO-8601 timestamp>
---
```

Body (technology-agnostic):
- Task summary and description
- In-scope and out-of-scope
- Expected behavior
- Acceptance criteria (measurable, non-code deliverables)
- Verification requirements
- Dependencies (other task specs, capabilities)
- Reusable capabilities adopted (with versions)
- Consistency note: how this task aligns with the approved project specification

### Step 13 — Independent review
Submit the draft task specification to wf-review (or a dedicated reviewer agent). The reviewer must challenge assumptions, missing requirements, defects, unnecessary complexity, and whether the non-coding deliverable actually satisfies the project specification. Every finding needs: evidence, severity, affected location, reasoning, and recommended resolution. The reviewer must not simply agree.

### Step 14 — Approval gate (Gate 3)
Present the draft + review findings to the human. Obtain explicit approval:
- On approval: change task spec frontmatter `status` to `Approved`; record approval as a Work Ledger `Decision` item with evidence (spec ID, version, approver, timestamp, file path)
- On rejection or blocking findings: return to Step 12; address findings; re-draft and re-submit for review

### Step 15 — Hand the worktree plan to `wf-plan` (no worktree is created here)
**Gate 4**: the worktree is **not** created by this skill. `wf-plan` creates it, always from the
repository's `main`/`master` base branch, and creates or updates the task handoff file at the same
time.

1. **Validate specification identity and approval**: Confirm the task spec exists with `status: Approved`.
2. **Inspect Git state (read-only)**: List branches (`git branch -a`), existing linked worktrees (`git worktree list`), current branch, and uncommitted changes (`git status`).
3. **Check for uncommitted work**: If uncommitted changes exist, warn the user. Ask whether to stash, commit, or abort. Never discard uncommitted work.
4. **Record the worktree plan**: Carry calibration choice 4 (branch naming preference, worktree placement preference) into the calibration run file and into the handoff as *preferences* for `wf-plan` to honour. The worktree itself does not exist yet.
5. **Do not create a branch or worktree here.** If a worktree already exists for this task spec ID, note it in the handoff so `wf-plan` reuses it rather than creating a second.

### Step 16 — Task handoff file (HARD RULE: detailed handoff + suggested skill run)
Create `spec-workspace/projects/<project-name>/tasks/task-<nnn>-handoff.md` containing **only this task's information** and MUST include:

**Detailed handoff:**
- Approved task ID and spec location
- Parent project spec ID
- Calibration run file location
- Worktree plan from calibration choice 4 - branch naming and placement **preferences**. The worktree does not exist yet; `wf-plan` creates it from `main`/`master`.
- **Purpose**, **status**, and **action items** - the three elements the root `AGENTS.md` handoff contract requires of every handoff file
- Task scope summary (in-scope, out-of-scope)
- Acceptance criteria summary
- Verification requirements summary
- Any unresolved open questions

**Suggested skill run (MANDATORY):**
- Which skill to run next - `wf-plan`. It creates the task worktree from `main`/`master`, calibrates the plan, and produces the plan file that `wf-implement` follows.
- Exact parameters to pass (project name/path, task spec ID, plan file path)
- Rationale for why this skill is the logical next step

### Step 17 — Record work ledger entries
Create new `WORK-XXX` items:
- Task created (type: Task, status: done)
- Task calibrated (type: Decision, status: done)
- Task approved (type: Decision, status: done, with approval evidence)
- Worktree plan recorded for `wf-plan` to execute (type: Task, status: done)
- Never modify or close existing items

### Step 18 — Present planned task summary
Present a concise summary of the planned task to the user:
- Task ID and type (noncode)
- Parent project spec ID
- Scope summary (in-scope, out-of-scope)
- Acceptance criteria summary (non-code deliverables)
- Worktree plan from calibration choice 4 - branch naming and placement **preferences**. The worktree does not exist yet; `wf-plan` creates it from `main`/`master`.
- **Purpose**, **status**, and **action items** - the three elements the root `AGENTS.md` handoff contract requires of every handoff file
- Suggested skill run (which skill, exact parameters, rationale)
- Any unresolved open questions

This summary is the user's confirmation that the task is fully planned and ready for implementation.

## Decision Rules
| Rule | Statement |
|------|-----------|
| Plan-fix calibration | Six choices asked one at a time; answers recorded bindingly; no defaults assumed |
| Calibration finalization | No drafting until user explicitly confirms the calibration plan is final |
| Worktree in calibration | Choice 4 captures branch/placement **preferences**; `wf-plan` creates the worktree from `main`/`master` |
| Git worktree creation | When creating a worktree for a new task branch, use `git worktree add <path> -b <new-branch> <base-branch>`; never attempt to check out an already-active branch into a new worktree |
| Explicit spec targeting | User selects project spec from presented options; never assumed |
| Non-coding only | This skill is for non-coding tasks; code-level test scenarios are not applicable, but measurable acceptance criteria are required |
| One worktree per task | `wf-plan` creates exactly one worktree per task, from `main`/`master`. Never two; reuse or escalate. |
| Approved spec only | Never create implementation worktrees for unsigned-off specifications |
| No uncommitted work discard | Check for uncommitted changes; warn user before proceeding |
| One handoff per task | One common handoff file per task (not per skill); handoff contains only this task's information |
| HARD RULE: handoff includes suggested skill run | Every task handoff file must include a detailed handoff AND a suggested skill run with parameters |
| Human owns approval | Explicit approval required before worktree creation and implementation |

## Delegation Strategy
- Independent review: Delegated to wf-review or a dedicated reviewer agent
- Commit and push: Delegated to wf-commit after implementation

## Approval Gates
| Gate | What | Who |
|------|------|-----|
| Gate 1 | Calibration plan finalization (includes worktree plan) | User |
| Gate 2 | Independent review of draft task spec | Reviewer agent / wf-review |
| Gate 3 | Explicit task specification approval | Human |
| Gate 4 | Worktree creation authorization | Human |

## Safety Boundaries
- No implementation code written during this skill
- Technology-agnostic task specification (no language, framework, database, etc.)
- Never modify the approved project specification
- One worktree per task; never share worktrees across tasks
- Never discard uncommitted work
- Never force-push by default

## Error Handling
| Situation | Handling |
|-----------|----------|
| No approved project specification | Error; direct user to wf-bootstrap first |
| No specifications to select | Error; project needs bootstrapping before task specification |
| Calibration plan not finalized | Pause; do not proceed to drafting |
| Approval denied | Return to drafting; address review findings; re-submit |
| Blocking review findings | Address before re-submission for review |
| Uncommitted changes present | Warn user; ask to stash, commit, or abort; never discard |
| Branch already exists | Ask user: new name, reuse existing, or abort |
| Worktree already exists for this task | Warn; do not duplicate; ask whether to reuse or abort |
| Worktree creation fails | Record as Blocker in work ledger. If failure is `invalid reference`, verify whether the base branch is already checked out in the primary worktree; if so, use the `-b` flag pattern (`git worktree add <path> -b <new-branch> <base-branch>`) rather than attempting to check out an existing branch name into a new worktree. |
| Artifact write missing/fails | HARD STOP; do not proceed to review/approval/next steps; notify user; record `Blocker` in work ledger (Gate Failure Protocol) |

## Validation
- Calibration run file exists with all six answers recorded bindingly, including worktree plan from choice 4
- Task spec file exists at `spec-workspace/projects/<project-name>/tasks/task-<nnn}-noncode.md` before submission to review
- Task spec exists with `status: Approved` and `task_type: noncode`
- Parent spec ID references an Approved project specification
- No code-level test scenarios present (not applicable to non-coding); measurable acceptance criteria ARE present and independently verifiable
- Worktree plan from calibration choice 4 recorded in the calibration run file and handed to `wf-plan`
- Task handoff file exists at `spec-workspace/projects/<project-name>/tasks/task-<nnn}-handoff.md` containing only this task's information, with detailed handoff AND suggested skill run, before handing off to `wf-plan`
- No existing work ledger items were modified or closed
- No uncommitted work was discarded
- No protected invariant was violated (approved parent spec, technology-agnostic task spec, evidence-based acceptance criteria)

## Handoff Requirements
- Approved task ID and spec location
- Parent project spec ID
- Calibration run file location
- Branch name and worktree path
- Base branch
- Next recommended action
- Suggested skill run with exact parameters
- Any unresolved open questions carried forward

## Related Skills
- **wf-bootstrap** — creates the approved project specification
- **wf-task-code** — companion skill for coding tasks
- **wf-review** — review gate for the draft task spec
- **wf-commit** — commits task spec and implementation from the worktree (suggested skill run in handoff)
