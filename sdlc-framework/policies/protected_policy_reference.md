# 📁 sdlc-framework/policies/protected_policy_reference.md

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