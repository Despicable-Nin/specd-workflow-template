---
name: wf-review
id: wf-review
version: 1.0.0
description: Perform independent, evidence-based review of specifications, architecture, implementations, and pull requests. The reviewer must challenge assumptions — never simply agree. Every finding must have evidence, severity, affected location, reasoning, and recommended resolution.
category: review
status: active
framework: sdlc-framework
repository: sdlc-framework
---

# wf-review

## Purpose
Perform independent, evidence-based review of:
- Project specifications
- Task specifications
- Architecture decisions
- Implementations
- Pull requests

The reviewer must challenge assumptions — never simply agree with the planner or implementer. Every finding must have evidence, severity, affected location, reasoning, and recommended resolution.

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
* **Code authority.** this skill is read-only with respect to specifications and writes **no implementation code**.

## Invocation Conditions
Invoke when:
- A draft specification (project or task) is ready for review (Gate 1/Gate 2 of wf-bootstrap/wf-task-code/wf-task-noncode)
- An architecture decision needs independent validation
- An implementation or pull request needs review before merge
- User explicitly requests an independent review

## Preconditions
- The artifact to review exists (spec file, implementation, branch, PR)
- Reviewer is independent of the author/planner/implementer

## Required Context
- Type of review (spec, architecture, implementation, pull-request)
- Artifact to review (file path, branch, PR number)
- Applicable approval criteria

## Inputs
| Input | Description |
|-------|-------------|
| Review type | `spec`, `architecture`, `implementation`, `pull-request` |
| Artifact reference | File path, branch name, or PR identifier |
| Review scope | Full review or focused area (security, performance, etc.) |

## Outputs
| Output | Description |
|--------|-------------|
| Review findings report | Markdown report with findings; each: evidence, severity, location, reasoning, resolution |
| Review decision | `Approved`, `Approved with comments`, `Changes required`, `Rejected` |
| Work ledger items | New `WORK-XXX` items of type `ReviewFinding` for each finding requiring action |

## Agent Responsibilities
- Read-only inspection of the artifact
- Challenge assumptions, missing requirements, defects, security concerns, regression risks, unnecessary complexity
- The reviewer must not simply agree with the planner or implementer
- Every finding: evidence (file path/line, spec ID, commit SHA), severity (info/warning/critical), affected location, reasoning, recommended resolution
- Produce a review decision with rationale
- Record findings as Work Ledger `ReviewFinding` items (status: proposed; never auto-close existing items)
- Never implement fixes yourself
- Never modify the artifact being reviewed

## Step-by-Step Procedure

### Step 1 — Establish review context
1. Confirm review type and artifact with the user.
2. Confirm reviewer independence (not the author/planner/implementer). If the reviewer is the author, recuse and assign an independent reviewer.
3. Identify applicable approval criteria (protected framework invariants, spec consistency, quality bar).

### Step 2 — Read-only inspection
Inspect the artifact based on review type:

- **Spec review**: Read the specification file; check technology-agnosticism (no language/framework/database references), completeness, consistency with the approved project specification.
- **Architecture review**: Examine architecture decisions against requirements; check for over-engineering or under-engineering; verify architecture composition matches stated needs.
- **Implementation review**: Read code (read-only only); check against the approved specification; check for invariant violations (no spec before implementation).
- **Pull-request review**: Inspect the diff, commit messages, test coverage, and existing review comments.

### Step 3 — Identify findings
For each potential issue, document:
- **Evidence**: exact file path, line numbers, spec ID, commit SHA, or PR reference
- **Severity**: `info`, `warning`, or `critical`
- **Affected location**: where the issue exists
- **Reasoning**: why this is a problem
- **Recommended resolution**: concrete fix

Categories of findings:
- Missing requirements or acceptance criteria
- Contradictions with the approved project specification
- Technology stack references in technology-agnostic specifications
- Security concerns
- Regression risks
- Unnecessary complexity or over-engineering
- Missing test scenarios (for coding tasks)
- Invariant violations (implementation without approved specification)

### Step 4 — Compile findings report
Organize findings by severity (`critical` first, then `warning`, then `info`). Each finding fully documented with all required fields.

### Step 5 — Determine review decision
- **Approved**: no critical findings; all warnings addressed or accepted
- **Approved with comments**: minor findings only; can proceed with comments noted
- **Changes required**: critical findings must be resolved before proceeding
- **Rejected**: fundamental issues; artifact must be substantially reworked

State the decision with rationale.

### Step 6 — Record findings in work ledger
Create new `WORK-XXX` items of type `ReviewFinding`:
- Status: `proposed` (flagged for human review — never auto-resolved)
- Source: reference to the artifact reviewed
- **Do not modify or close existing items**

### Step 7 — Present report and decision
Output the findings report and review decision to the user. Handoff: if `Changes required` or `Rejected`, next action is to address findings and re-submit for review.

## Decision Rules
| Rule | Statement |
|------|-----------|
| Independence | Reviewer must not be the author/planner/implementer |
| No rubber-stamping | Reviewer must challenge, not simply agree |
| Evidence required | Every finding cites evidence (path, SHA, spec ID, PR reference) |
| Severity classification | Critical findings block progression; warnings are noted |
| No auto-resolution | Findings are `proposed`, never auto-closed |

## Delegation Strategy
- None — independent review is inherently a standalone responsibility

## Approval Gates
- The review decision is itself an approval gate for the artifact being reviewed
- If `Changes required` or `Rejected`: the author must address findings and re-submit for re-review

## Safety Boundaries
- Read-only: no modifications to the artifact being reviewed
- Never implement fixes yourself
- Never discard pending work
- Never force-push (not applicable at review stage)

## Error Handling
| Situation | Handling |
|-----------|----------|
| Artifact not found | Error; ask user to confirm path/reference |
| Reviewer is the author | Error; recuse and assign independent reviewer |
| No applicable criteria | Use protected framework invariants as default criteria |
| Binary/unreadable artifact | Report as uninspectable; continue with others |

## Validation
- Findings report contains findings organized by severity
- Every finding has evidence, severity, location, reasoning, resolution
- Review decision stated with rationale
- Work ledger contains `ReviewFinding` items for actionable findings
- No artifact files were modified

## Handoff Requirements
- Review decision and rationale
- Critical findings highlighted
- Next action (address findings and re-submit, or proceed to next gate)

## Related Skills
- **wf-bootstrap** — creates the approved project specification
- **wf-task-code** — creates coding task specs with inlined worktree
- **wf-task-noncode** — creates non-coding task specs with inlined worktree
- **wf-reconcile** — may be invoked if review finds specification conflicts
- **wf-commit** — commits task spec and implementation after review approval
