# Protected Policy Reference

The single source of truth for non-negotiable system policies.

## I. Primary Protected Invariants (Non-Overridable)
1. Specification Before Implementation: Implementation implies active approval of a specification.
2. Technology Agnosticism: All abstract specifications must be independent of technology stack.
3. Evidence-Based Completion: No completion is claimed without verifiable evidence (PR refs, build logs, test outputs, hashes).

## II. Policy Enforcement Mechanism
Policies are enforced via runtime checks embedded in the Orchestrator agent calls and the core tools. Any attempt to violate a protected invariant must result in a hard gate failure and clear notification to the user referencing the specific violated invariant and the policy section.

## III. Policy Overrides (Limited):
Project-specific policies (in project-a/AGENTS.md) may override *default* workflow behaviors (e.g., changing a default code standard) but can *never* weaken a Protected Invariant.

## IV. Approval Hierarchy:
Material decision must be logged as a **Decision** in the Work Ledger and require explicit authorization from a designated human or system trust boundary.

## V. Gate Failure Protocol
When any gate (Bootstrap, Task, Commit, Review) is failed or about to be bypassed due to a Protected Invariant:

1. **Hard stop**: The workflow halts immediately; no artifact on the violating path is produced or executed.
2. **Citation**: The failure message must reference the violated invariant (e.g., `Specification Before Implementation`) and this policy section.
3. **Ledger**: A `Blocker` work item is recorded in the Work Ledger referencing the violated invariant, gate, and context.
4. **Notification**: The human is notified clearly and explicitly; the failure is never silently retried or overridden.
5. **No override**: Policy overrides (Section III) may not be applied to Protected Invariants; only explicit human authorization recorded as a `Decision` may supersede a workflow default.