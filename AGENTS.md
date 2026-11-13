# Root Workspace AGENTS.md

# The Specification Kit — Operating Contract

*(This file is the entry point for any agent or skill working in this repository. It is not a
summary; it is a binding contract. Read it before acting.)*

---

## Rule 0 — AGENTS.md binds every skill, always

**This is Rule 0. It outranks every other rule in this file and every step list inside any skill.**

1. **Always read before acting.** Every skill MUST read this file and the nearest ancestor
   `AGENTS.md` of every path it will read or write, *before* its first action. If a skill's own
   procedure is silent about a location, naming, or placement rule, **this file still governs it**.
   Silence in a skill is not permission to improvise.
2. **Applies to every skill, every phase, every agent.** No skill is exempt because it is
   "read-only", because it is a helper, or because it was invoked directly rather than through
   `@wf-`. `wf-state` and `wf-reconcile` still obey where files live. `wf-commit` still obeys
   naming. `wf-implement` still obeys the code guardrail.
3. **Conflict resolution.** Where a skill's instructions and an applicable `AGENTS.md` disagree:
   * **Protected Invariants win over everything** (`sdlc-framework/policies/protected_policy_reference.md`).
   * An **explicit user instruction** wins over `AGENTS.md`.
   * Otherwise **`AGENTS.md` wins over the skill.** A skill must not "do it its own way".
   * The skill states the conflict, follows `AGENTS.md`, and records the conflict in the work
     ledger. It does not silently pick a side.
4. **Hard stop, never silent deviation.** If an `AGENTS.md` rule cannot be satisfied — the
   canonical folder does not exist, a required `binding.yaml` is missing, a target path is
   ambiguous — the skill **stops**, names the violated rule, and records a `Blocker` in the work
   ledger citing this rule. This is the Gate Failure Protocol. It does not improvise a location.
5. **`AGENTS.md` is read-only during a skill run** unless the task is explicitly a documentation
   task whose scope covers this file, and that has been approved.

---

## 1. The kit has exactly two trees

| Tree | Holds | Never holds |
|---|---|---|
| `spec-workspace/` | **What** is intended — specifications, contracts, decisions. Technology-agnostic. | Implementation code. |
| `generated-projects/` | **How** it is built — codebases, scaffolds, implementation. | Specifications. |

The two are connected by `binding.yaml` and by the work ledger — **never by duplication**. A
specification is never copied into a codebase, and code is never copied into a specification.

---

## 2. Where to create specification folders

All specification artifacts live under `spec-workspace/`. Nothing else in the repository may hold a
specification.

```
spec-workspace/
├── README.md                        # contract of this tree
├── SDLC-SOR-v1.0.md                 # the framework's own system-of-record definition
├── library/                         # reusable, technology-agnostic artifacts
│   ├── Engineering/                 # cross-cutting practices and constraints
│   └── Capabilities/                # reusable capability specifications
├── projects/
│   └── <project-name>/              # ONE collection per project. lowercase, hyphenated.
│       ├── AGENTS.md                # project-local context and rules
│       ├── specification.md         # parent specification (root of the collection)
│       ├── binding.yaml             # pointer: spec collection ID + version
│       ├── service-contracts.yaml   # runtime service-to-service dependency manifest
│       ├── schema/                  # normative renderings of data contracts
│       └── tasks/
│           ├── task-<task-id>-noncode.md   # task specification
│           ├── task-<task-id>-coding.md    # task specification
│           ├── task-<task-id>-handoff.md   # ONE handoff per task (not one per skill)
│           └── task-<task-id>-noncode-calibration.md  # the six recorded calibration answers
├── <project-name>/work_ledger.yaml  # project-scoped ledger (optional; project-temp is the default)
├── tasks/                           # framework-level handoffs (not project-scoped)
└── project-temp/work_ledger.yaml    # THE work ledger - the local source of truth for all work
```

**Rules for specification folders:**

* A project collection is created by `wf-bootstrap` and lives at
  `spec-workspace/projects/<project-name>/`. `<project-name>` is lowercase and hyphenated
  (`blockchain-enabled-lms`).
* The parent specification is written by `wf-bootstrap` to
  `spec-workspace/projects/<project-name>/specification.md`. A project may give its root spec a
  domain-specific filename — `SRS_LMS_v1.0.md` in the LMS project — provided three things agree:
  the file's `id` in frontmatter, the reference in `binding.yaml`, and the `parent_spec` reference
  in every dependent task spec. A filename change alone is not enough.
* Task artifacts are created by `wf-task-code` / `wf-task-noncode` at the canonical paths in the
  table above. A skill **must not** write a specification to an ad-hoc location.
* Capability artifacts are created under `spec-workspace/library/Capabilities/`.
* `spec-workspace/project-temp/work_ledger.yaml` is the single work ledger. Every skill that
  creates or discovers work records it there with a new `WORK-XXX` id. A project may additionally
  keep its own ledger at `spec-workspace/<project-name>/work_ledger.yaml`.

---

## 3. Where to create the codebase

```
generated-projects/
├── README.md                        # contract of this tree
└── <project-name>/                  # ONE codebase per project. Same name as the spec collection.
    ├── AGENTS.md                    # project context and rules for the codebase
    ├── binding.yaml                 # REQUIRED: references the spec collection ID + version
    ├── .opencode/skills/            # project-local copies of the canonical framework skills
    └── ...                          # the implementation
```

**Rules for codebases:**

* The codebase directory name **must** match the specification collection name exactly:
  `generated-projects/<project-name>/` binds to `spec-workspace/projects/<project-name>/`.
* `binding.yaml` is **mandatory** in every codebase directory and **must** reference the stable
  id and version of the specification collection it implements. A codebase without a valid
  `binding.yaml` is untraceable and must not be built.
* `binding.yaml` carries **only** that pointer. Runtime service bindings go in
  `service-contracts.yaml`.
* `wf-bootstrap` creates a **non-executable scaffold** here — directory, `AGENTS.md`, and
  `binding.yaml`. Never source files.

---

## 4. WHEN code may be generated — the guardrail

**Implementation code is produced in exactly one place, by exactly one skill: inside a task
worktree, by `wf-implement`, against an approved task specification.**

| Skill | May it write implementation code? |
|---|---|
| `wf-implement` | **YES** — the only skill that may. Requires an approved task spec and a task worktree. |
| `wf-task-code` | **NO.** Produces a *specification* that says what to build. It never builds it. |
| `wf-task-noncode` | **NO — NEVER.** A non-coding task produces a specification or a document/artifact. It does not produce code. |
| `wf-bootstrap` | **NO.** Non-executable scaffold only. |
| `wf-plan` | **NO.** A plan is not code. |
| `wf-review`, `wf-state`, `wf-reconcile` | **NO.** Read-only by definition. |
| `wf-converge`, `wf-commit`, `wf-constitution` | **NO.** Verdict, record, and governance principles only. |

**The escalation rule (this is what "wf-task-noncode ONLY" protects).** If work begun through
`wf-task-noncode` turns out to require implementation code:

1. The code does **not** go into `spec-workspace/`. The specification kit never holds code.
2. The noncode task does **not** silently acquire a code deliverable.
3. **Stop**, and raise a **separate coding task** through `wf-task-code` against the codebase
   directory in `generated-projects/<project-name>/`.
4. The noncode task's deliverable remains a specification or artifact, and the link between the
   two tasks is recorded in the work ledger and in the handoff.

**The mirror rule.** Code that implements a specification lands in the codebase, never in
`spec-workspace/`. A specification that is written into `generated-projects/` is misfiled and must
be moved back to the collection it belongs to.

---

## 5. Artifact placement and handoff files

### 5.1 Placement

| Artifact | Lives in | Created by |
|---|---|---|
| Parent specification | `spec-workspace/projects/<p>/` | `wf-bootstrap` |
| Capability specification | `spec-workspace/library/Capabilities/` | `wf-bootstrap` / a capability task |
| Task specification | `spec-workspace/projects/<p>/tasks/` | `wf-task-code` / `wf-task-noncode` |
| Task calibration record | `spec-workspace/projects/<p>/tasks/` | `wf-task-code` / `wf-task-noncode` |
| Task plan (one per task) | `spec-workspace/projects/<p>/tasks/` | `wf-plan` |
| Task handoff (one per task) | `spec-workspace/projects/<p>/tasks/` | `wf-task-code` / `wf-task-noncode`, refreshed by `wf-plan`, appended by every later skill |
| Data contract rendering | `spec-workspace/projects/<p>/schema/` | a noncode task |
| `binding.yaml` | `generated-projects/<p>/` | `wf-bootstrap` |
| Project scaffold | `generated-projects/<p>/` | `wf-bootstrap` |
| Implementation | `generated-projects/<p>/` | `wf-implement` (in a worktree) |
| Work ledger entry | `spec-workspace/project-temp/work_ledger.yaml` | every skill that creates or discovers work |

### 5.2 The handoff file — location

**A handoff file always lives inside the directory of the work it describes.** There is no
central handoff folder, and a handoff is never parked in a sibling project's directory or at the
repository root.

| Handoff describes | Lives at |
|---|---|
| A project task | `spec-workspace/projects/<project-name>/tasks/task-<task-id>-handoff.md` |
| Framework-level work | `spec-workspace/tasks/task-<task-id>-handoff.md` |

### 5.3 The handoff file — always look for it

**Every skill looks for the task's handoff file before it acts, and reads it if it exists.** It is
the task's running state: what the task is for, where it stands, what is outstanding, and what
runs next. A skill that starts work on a task without reading its handoff has not started properly.

If no handoff file exists and the skill is producing one, it creates it at the canonical location
above.

### 5.4 The handoff file — required content

Every handoff file must contain, in this order:

1. **Purpose** — what this task is for, what it delivers, what it explicitly does **not** cover,
   and which specification it implements.
2. **Status** — `Open` | `In Progress` | `Blocked` | `Done`; plus which skills have contributed
   and what each one produced.
3. **Action items** — numbered. Each item states **what** to do, **which artifact or file** it
   touches, **how it is verified**, and **which skill owns it**.
4. **Preconditions unmet** — the blockers that must clear before the next skill may run.
5. **Open questions** — unresolved decisions, each with its owner.
6. **Suggested skill run** — the exact next skill with exact parameters, and why it is next.
7. **Phase contributions** — a table of every skill that appended to the file.

### 5.5 The handoff file — disposable

**A handoff file is a working note, not a record of record. It is disposable.**

* **When the handoff's status becomes `Done`, the file is disposed of — deleted, not archived.**
  It leaves no trace in the tree.
* Disposal happens in the same change that sets the status to `Done` — in practice, by `wf-commit`
  once `wf-converge` has confirmed convergence.
* **Durable history lives in the work ledger and in the specifications, never in a handoff.** If
  something must survive the task, it goes into the ledger or a spec before the handoff is
  deleted.
* Never delete a handoff that is `Open`, `In Progress`, or `Blocked`. A blocked handoff is the
  most useful file in the tree — it is the first thing the next session reads.

---

## 6. Specification lifecycle

`Draft -> In_Review -> Approved -> Superseded`

* `wf-bootstrap` creates project specifications. `wf-review` is the **independent gate** before any
  `Approved` status is granted.
* `wf-task-code` and `wf-task-noncode` create task specifications, each subject to `wf-review`.
* **`Approved` requires evidence in the work ledger.** A status field alone is not approval. An
  artifact marked `Approved` with no approval Decision recorded in the ledger is a defect — see
  `WORK-009`.
* `wf-task-noncode` produces task specifications that are **specifications only**. The word
  "non-code" describes the *deliverable*, not a lesser kind of specification.

---

## 7. Protected Invariants

Non-negotiable, defined in
[sdlc-framework/policies/protected_policy_reference.md](sdlc-framework/policies/protected_policy_reference.md):

1. **Specification Before Implementation** — no code without an approved specification.
2. **Technology Agnosticism** — specifications are independent of any tech stack.
3. **Evidence-Based Completion** — no completion is claimed without verifiable evidence.

An `AGENTS.md` rule may be overridden by explicit human authorization recorded as a `Decision` in
the work ledger. It may **never** weaken a protected invariant.

---

## 8. Which skill for which scenario

The eleven SDLC skills live in `sdlc-framework/.opencode/skills/<skill-id>/SKILL.md` and are
exposed as `@wf-` commands in `sdlc-framework/.opencode/commands/`. Each carries **Rule 0** in its
own `SKILL.md`.

### 8.1 Routing table — start here

| You want to… | Run | Gate / precondition |
|---|---|---|
| Start a **brand-new** project from a description | `@wf-bootstrap` | No project spec may exist yet. Produces the spec **and** a non-executable scaffold. |
| Set the project's **durable engineering principles** | `@wf-constitution` | Run once, early, or when principles change. |
| Know **what is actually true right now** | `@wf-state` | Read-only. Never changes a spec. |
| Find **specifications that disagree, duplicate, or dangle** | `@wf-reconcile` | Read-only. Produces a plan; never edits a spec. |
| Get **code** written | `@wf-task-code` → `@wf-plan` → `@wf-implement` | Parent spec must be `Approved`. `wf-implement` is the only skill that writes code. |
| Get a **document, config, infra, or process** written | `@wf-task-noncode` | Parent spec must be `Approved`. **Never** produces code. |
| Get an artifact **independently checked** | `@wf-review` | **Mandatory before any `Approved` status.** |
| Get an **implementation plan** from an approved spec | `@wf-plan` | Task spec must already be `Approved`. |
| Know whether the **implementation met the criteria** | `@wf-converge` | Needs implementation + test evidence. |
| Get the work **committed and pushed** | `@wf-commit` | The only skill that creates commits. |

### 8.2 The happy path

```
@wf-bootstrap <project>
    ↓ approved project spec + non-executable scaffold
@wf-task-code | @wf-task-noncode <project> <work>
    ↓ task spec Draft → @wf-review → Approved + calibration record + handoff
@wf-plan <project> <task id>
    ↓ six-choice calibration → worktree created from main/master → plan file → @wf-review → Approved
@wf-implement <project> <worktree> <task id>
    ↓ Red → Green → Refactor, following the plan file
@wf-converge <project> <task id>
    ↓ acceptance criteria verified against evidence
@wf-commit <project> <worktree> <task id> [push yes/no]
    ↓ handoff marked Done and disposed of
```

**The worktree and the plan are created by `wf-plan`, not by the task skill.** The task skill
records the worktree *preferences* (calibration choice 4); `wf-plan` creates the branch and the
worktree from `main`/`master`, and creates or refreshes the handoff file.

### 8.3 Skill cards

**`@wf-bootstrap`** — *good for:* creating a project from a natural-language description, once.
*Not for:* adding a feature to a project that already exists. *Calibration:* free-form project
description and an optional project name. It drafts the spec, asks for approval, and only then
generates the scaffold — so it **has its own approval gate** before any scaffold is written.
Outputs `spec-workspace/projects/<p>/specification.md`, the scaffold in
`generated-projects/<p>/` with `AGENTS.md` and `binding.yaml`, project-local skill copies, and
ledger entries.

**`@wf-constitution`** — *good for:* the durable, versioned set of engineering principles
(quality, testing, security, performance, process) that steer specifications, plans, and reviews.
Run once, early, or when the principles change. *Not for:* product requirements. *Calibration:*
candidate principles (required), scope (`project` | `domain` | `system`, default `project`),
version (default `1.0`).

**`@wf-state`** — *good for:* discovering the actual current state — session resume, handoff, or
before planning. *Not for:* changing anything, or judging whether specs agree with each other.
*Calibration:* project name/path (defaults to the working context), scope filter
(`full` | `specs` | `git` | `work-items` | `handoffs`, default `full`). Its only permitted write is
appending new `proposed` ledger items.

**`@wf-reconcile`** — *good for:* duplicates, conflicts, overlaps, fragmentation, outdated specs,
and missing relationships between specs. *Not for:* authoring, fixing, or superseding a spec.
*Calibration:* project name/path, scope (`all` or specific spec IDs). Outputs a reconciliation
report and a plan; each recommended action becomes a `proposed` ledger item.

**`@wf-task-code`** — *good for:* work that will produce **implementation code** — feature, bug fix,
refactor, test addition. *Not for:* documents, config, infra, or process. *Calibration:* the **six
plan-fix choices** (below), asked one at a time, **no defaults**. Then explicit parent-spec
targeting — the selected spec must be `Approved` — and a capability scan of
`spec-workspace/library/`. Its File Emission Guardrail requires the task spec, calibration record,
and handoff to exist at their canonical paths before review proceeds. **It creates no branch and no
worktree** — choice 4 records the preferences and `wf-plan` acts on them.

**`@wf-task-noncode`** — *good for:* work that produces a **document, configuration, infrastructure,
process, or data-migration setup** — and *only* that. *Not for:* anything needing code. If the work
turns out to need code, **stop** and raise a separate `@wf-task-code` task (root Section 4).
*Calibration:* the same **six plan-fix choices**, reworded for non-code work (below). It carries a
distinct rule: **no code-level test scenarios; measurable acceptance criteria are still required.**

**`@wf-plan`** — *good for:* turning an approved task specification into an implementation/technical
plan. It is the bridge between "what to build" and "how it will be built", tracing planned work
back to both the task acceptance criteria and the approved parent spec. *Not for:* writing the task
spec, or writing code. *Calibration:* the **six plan-fix-style consumption choices** — plan output
shape, understanding aid, explanation budget, workflow path, implementation chrome, teach or
orient — asked together in one turn, recorded bindingly in a single run file, no defaults assumed.
It **always creates the task worktree from the `main`/`master` base branch**, and creates or
refreshes the task handoff file, before the plan is drafted. The plan file it writes is the
**source of truth for `wf-implement`**, for coding and non-coding tasks alike — `wf-implement`
follows that file rather than re-deriving intent from the task spec.

**`@wf-review`** — *good for:* an independent, evidence-based gate on a project spec, task spec,
architecture decision, implementation, or pull request. **This is the mandatory gate before any
artifact may claim `Approved`.** *Not for:* authoring or repairing the thing being reviewed.
*Calibration:* review type (`spec` | `architecture` | `implementation` | `pull-request`), artifact
reference (file path, branch, or PR), review scope (full, or focused on an area such as security or
performance). Every finding carries evidence, severity, affected location, and a recommended
resolution.

**`@wf-implement`** — *good for:* writing the code for an approved task spec under an approved
plan. **The only skill permitted to write implementation code.** It runs Red → Green → Refactor
and writes only within the approved scope, into `generated-projects/<p>/` — never into
`spec-workspace/`. *Not for:* changing the spec, or code outside the approved scope. *Calibration:*
task spec ID (required), plan reference (required), worktree path and branch.

**`@wf-converge`** — *good for:* deciding whether the implemented work actually met the approved
acceptance criteria, using collected evidence — test output, build logs, review verdicts. *Not
for:* fixing the gaps; it loops back to `@wf-implement`. *Calibration:* task spec ID (required);
each criterion is mapped to its evidence, and unmet criteria produce a `Not Converged` verdict.

**`@wf-commit`** — *good for:* creating the authorized commit for work finished in a task
worktree, and optionally pushing it. **The only skill that creates commits.** It verifies
approved-spec linkage, inspects the complete diff, validates the intended scope, checks tests and
review findings, excludes unrelated files and secrets, and never force-pushes by default.
*Calibration:* project name/path, worktree path or branch, task spec ID linked to that worktree,
and a push flag (`yes`/`no`).

### 8.4 The calibration model

`@wf-task-code` and `@wf-task-noncode` share one calibration pattern: **six choices, asked one at
a time, with no defaults assumed.** Each answer is recorded bindingly in the task's calibration
file, and the plan is only finalized when the human confirms it.

| # | `@wf-task-code` | `@wf-task-noncode` |
|---|---|---|
| 1 | **Task shape** — feature, bug fix, refactor, test addition? Scope and blast radius? | **Task shape** — documentation, configuration, infrastructure, process, data migration? Scope and blast radius? |
| 2 | **Evidence/artifacts** — what must be produced beyond code? | **Evidence/deliverables** — what concrete deliverables? |
| 3 | **Verification depth** — unit tests, integration tests, manual review, demo? | **Verification depth** — review sign-off, config validation, infra smoke test, demo, compliance check? |
| 4 | **Workflow path** — isolated worktree? Branch naming? Worktree placement? | same |
| 5 | **Implementation surface** — which modules/interfaces, and which are off-limits? | which docs, configs, infra definitions, or processes — and which are off-limits? |
| 6 | **Orientation target** — who must understand this spec? | same |

**Choice 4 is the worktree plan.** There is no separate worktree step afterwards — the branch name
and the worktree path are decided there and honoured by every later skill.

### 8.5 Common mis-routings

| Symptom | Right skill | Why the obvious one is wrong |
|---|---|---|
| "I need this feature built." | `@wf-task-code` | `@wf-task-noncode` would produce a specification, never code. |
| "I need this document written." | `@wf-task-noncode` | `@wf-task-code` would demand code-level test scenarios that a document cannot have. |
| "The spec says `Approved`." | `@wf-review` | A status field is not approval — the evidence lives in the ledger. |
| "The files are in the wrong place." | `@wf-reconcile` | `@wf-state` reports the state but never judges consistency. |
| "The code is wrong." | `@wf-converge` | `@wf-implement` fixes; `@wf-converge` decides whether it is done. |
| "Commit my work." | `@wf-commit` | No other skill may create a commit. |
| "Set up a worktree for this task." | `@wf-plan` | The task skill records the *preferences*; only `wf-plan` creates the branch and worktree, and only from `main`/`master`. |
| "Where did this task stand?" | Read the **handoff file** | It is the task's running state — purpose, status, action items. It is disposable, so the ledger holds the durable history. |

Usage reference:
[sdlc-framework/documentation/sdlc-skill-usage.md](sdlc-framework/documentation/sdlc-skill-usage.md)

---

## 9. Global model routing defaults

* **Planner:** `qwen3.8-q4_K_M`
* **Reviewer:** `ornith:latest`
* **Discovery:** `gemma4:latest`

---

## 10. Tool integration

Custom tools are limited to what OpenCode provides or what is defined in
[sdlc-framework/tools/](sdlc-framework/tools/). That directory is currently a **placeholder** — the
utilities it names are not implemented (`WORK-022`). Do not assume a tool exists; verify first.

---

## 11. Instruction precedence

1. Protected Framework Invariants (highest — cannot be weakened by anything below)
2. Explicit User Instructions (highest override, except over protected invariants)
3. **Rule 0 — this file and the nearest applicable `AGENTS.md`**
4. [sdlc-framework/AGENTS.md](sdlc-framework/AGENTS.md)
5. Global Defaults (lowest)

---

## 12. Recommended initial action

`@wf-state` to discover the actual current state, then `@wf-reconcile` if specifications disagree.
`@wf-bootstrap` to begin a new project from scratch.
