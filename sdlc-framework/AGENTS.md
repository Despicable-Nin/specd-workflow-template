# sdlc-framework/AGENTS.md

# SDLC Framework Core Policies and Tools

*(This file governs the framework itself — its skills, commands, policies, and schemas. It is
subordinate to the root `AGENTS.md` and inherits its Rule 0.)*

## Rule 0 applies here — and must be carried by every skill

Every skill in this framework is bound by the root `AGENTS.md` Rule 0. **Each `SKILL.md` in
`.opencode/skills/<skill-id>/` carries a Rule 0 block of its own**, so that the obligation survives
the skill being read in isolation, out of context, or in a different session.

A skill that cannot comply with an applicable `AGENTS.md` rule must **hard stop**, name the
violated rule, and record a `Blocker` in the work ledger under the Gate Failure Protocol. It must
not improvise a path, a name, or a shortcut.

## 1. System principle: role, skill, and flow separation

The framework agents define the *system* roles (Orchestrator, Implementer). They do not perform the
work directly; they orchestrate the execution of defined skills.

## 2. Core components

| Component | Location | State |
|---|---|---|
| Policies | `policies/` | `protected_policy_reference.md` — the definitive source of the protected invariants. |
| Skills | `.opencode/skills/<skill-id>/SKILL.md` | 11 skills, each carrying Rule 0. |
| Commands | `.opencode/commands/wf-<skill-id>.md` | 11 wrappers, one per skill. |
| Schemas | `schemas/` | `work_ledger_schema.json` — structure of the work ledger. |
| Documentation | `documentation/` | `sdlc-skill-usage.md`, `getting_started.md`, `README.md`. |
| Tools | `tools/` | **Placeholder.** The three utilities it names are not implemented — `WORK-022`. |
| Workflows | `workflows/` | **Placeholder.** The four blueprints it names are not implemented — `WORK-022`. |

## 3. Component interaction

The Orchestrator uses a skill hook to call functions/blueprints, enforcing the correct agent roles
for the execution context.

## 4. Core policy enforcement

All components enforce the protected invariants defined in the system roots.
[`policies/protected_policy_reference.md`](policies/protected_policy_reference.md) is the definitive
source.

**The code-generation guardrail is enforced here too.** The framework decides *when* code may be
written, and the answer is narrow: only `wf-implement`, inside a task worktree, against an approved
task specification. `wf-task-code` and `wf-task-noncode` produce specifications. `wf-bootstrap`
produces a non-executable scaffold. The read-only skills read. See root `AGENTS.md` Section 4.

## 5. Artifact placement within the framework

The framework is itself governed by the root `AGENTS.md`. Its components live where that contract
says they live; it does not create a third tree and does not write specifications outside
`spec-workspace/`.

## 6. Dependencies

This framework requires the ability to manage Git worktrees and to utilise the OpenCode work ledger
API at all times.

## 7. Maintaining the skills

* Every `SKILL.md` starts with YAML frontmatter (`name`, `id`, `version`, `description`,
  `category`, `status`, `framework`, `repository`) and then a **Rule 0** block.
* A skill change that alters where artifacts live **must** update the File Emission Guardrail
  table in that skill in the same change. The guardrail and this file are one contract.
* `wf-commit` is the only skill that creates commits. No other skill commits or pushes.
