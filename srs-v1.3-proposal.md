# SRS v1.3 Proposal — Change Request WORK-191 (DRAFT 2)

**Status: PROPOSED — independent review returned CHANGES REQUIRED; all findings below are dispositioned in this draft. NOT APPLIED.**
`SRS_LMS_v1.0.md` remains `v1.2` / `Approved` until Gate 2 grants explicit human approval.
Recorded as ledger `Decision` WORK-191 (status `proposed`, 2026-11-19). Precedent: `WORK-171` → v1.2 and the atomic SRS + CAP-STATUSENUMS flip (`WORK-176`).

---

## Review disposition (independent review 2026-11-19, verdict CHANGES REQUIRED)

| Finding | Sev. | Resolution in this draft |
|---|---|---|
| F-01 — FRAS exposes no instructor-of-record operation | major | **Fixed — hunk H6b** adds the FRAS operation to §3.1. |
| F-02 — `AttendanceRecord` rule-set identifier unspecified | major | **Fixed — user decision (2026-11-19): the record carries it.** W-7 step 1/4, S-8, glossary (no §2.9 note added — H5 carries only the `Recorded` transition). |
| F-03 — `CAP-STATUSENUMS` sequencing + inline vocab + missing `Recorded` | major | **Fixed — atomic single Gate 2** (user decision): hunks C1–C3 add the attendance domain to the capability; SRS hunks strip ALL inline enumerations to capability references. |
| F-04 — v1.2 anchor `4c3a72c` false | major | **Fixed — H12 uses `b6ce80c`** (verified in git 2026-11-19). |
| F-05 — S-4 never names attendance | major | **Fixed — S-8 judge extended with refusal + identifier clauses; S-4 unchanged** (user decision); H12 names the coverage route. |
| F-06 — W-1 trigger list omits attendance | minor | **Fixed — §2.2 trigger gains "an attendance marking" (hunk H13), named modification in H12.** |
| F-07 — S-8 omits refusal paths | minor | **Fixed — H8.** |
| F-08 — "or influences" digest wording | minor | **Fixed — H7 reworded.** |
| F-09 — Determinism omits rule set | minor | **Fixed — H9.** |
| F-10 — §3.5 omits attendance records | minor | **Fixed — new hunk H9b.** |
| F-11 — `Session` vs §2.8 "session identifiers" | minor | **Fixed — H10 glossary cross-reference.** |
| F-12 — anchor map omits §2.9 | minor | **Fixed — H11.** |
| F-13 — example weights risk fossilization | minor | **Fixed — H3 marks weights "illustrative only; binds nothing"; repetition removed downstream.** |
| F-14 — glossary deferral phrasing | info | **Fixed — H10.** |
| F-15 — W-7 in §2.10; §1.3 emphasis | info | Accepted as-is (anchor stability forces the placement; §1.3 untouched — noted in H12). |

**Re-review scope if requested:** hunks H3–H13, C1–C3 — everything the disposition touched.

## Binding decisions (discovery batches, 2026-11-19) — unchanged

Per-student-per-session attendance; ESS ownership (no new domain); formula input via ECS `FormulaRules`; all three levels; CR = attendance + grade-config annotation; conceptual `Session`; outcome vocabulary governed by `CAP-STATUSENUMS`; append-only correction; instructor-of-record via FRAS; derived deterministic aggregate; never proof-committed; **rule-set identifier recorded on every AttendanceRecord**; **atomic Gate 2 for SRS v1.3 + CAP-STATUSENUMS v1.2**; **FRAS operation added in this CR**; **W-1 trigger extended; S-4 unchanged**.

---

## Frontmatter (H1)

```yaml
version: 1.2   →   1.3
updated: 2026-11-18T10:50:39Z   →   <application time>
```
`status: Approved` unchanged (Section 11 persists approval across changes; cf. v1.2).

---

## H2 — §2.1 Capabilities (new row after C-7)

```markdown
| C-8 | Record and own per-session attendance for a section, and return a student's attendance aggregate for a section and period. | ESS |
```

## H3 — §2.3 Workflow W-2 (new paragraph after the `**Rule.**` line)

```markdown
**Formula ownership.** The governing grading formula — including any attendance component inside a
composite activities block (for example: activities collectively worth some agreed share of the
final grade, quizzes and attendance among their components, and an exam worth its own agreed share —
weights are illustrative only; binds nothing) — is `FormulaRules` content owned by ECS (Section
3.1). This specification fixes that the formula is deterministic and that the governing rule set
identifier identifies it (Section 5); it does not author the formula's content, weights, or
structure. No task may author it either: tasks define the contract for the rules, never the rules.
Where the formula references attendance, GRA-Service obtains the student's attendance aggregate
from ESS by the operation defined in Section 3.1 (ESS).
```

## H13 — §2.2 Workflow W-1 (trigger enumeration extended; named modification)

Current: *"Any creation or update of a student academic record — an enrollment, a grade submission, a section allocation, or a course or program definition that takes effect in a period."*
Proposed:

```markdown
**Trigger.** Any creation or update of a student academic record — an enrollment, a grade
submission, a section allocation, an attendance marking, or a course or program definition that
takes effect in a period.
```

## H4 — New §2.10, appended after §2.9 (no existing section is renumbered)

```markdown
### 2.10 Workflow W-7 — Attendance marking

**Trigger.** A scheduled session of a section concludes, while its academic period is `Active`.

**Participants.** ESS, FRAS, ECS.

**Flow.**

1. ESS requests the governing context for the section's educational level and academic period from
   ECS. If the period's status is not `Active`, ECS refuses and no attendance record is created
   (Workflow W-1 applies to this record, as it takes effect in a period). If the status is
   `Active`, ECS returns the governing rule set identifier, which ESS records against each
   AttendanceRecord it creates for the session (Workflow W-1 step 4).
2. ESS validates the marking actor with FRAS: only the instructor of record assigned to the
   section may mark its attendance. If FRAS does not return that assignment, the marking is
   refused.
3. For each enrolled student in the session, the instructor of record records exactly one
   attendance outcome. The outcome values are governed by `CAP-STATUSENUMS` (Section 9.1); this
   specification does not restate them.
4. ESS appends one `AttendanceRecord` per (session, student), carrying the governing rule set
   identifier from step 1. A correction appends a new record linked to the record it supersedes by
   a parent reference; the original is never altered.
5. ESS exposes a student's attendance aggregate (per section, per period) as a derived value for
   consumers that need it. The aggregate is computed deterministically from the attendance records
   under the governing rule set in force; it is never stored as a second source of truth. Which
   outcomes count toward presence, and any attendance policy thresholds, are ECS rule content and
   are not defined here.

**Rule.** Attendance records are operational. They are never proof-committed and they never enter
the canonical form of a student-period record (Section 2.8, Section 4.1). Attendance may only be
referenced by the ECS governing formula as an input (Workflow W-2).
```

## H5 — §2.9 State transitions (new block after the Level-completion record block)

```markdown
#### Attendance record

| From | Event | To |
|---|---|---|
| — | Instructor of record marks a session (W-7 step 4) | `Recorded` |

There are no further transitions. A correction appends a successor linked to the record it
supersedes; the original is never altered, and there is no `Superseded` state (the supersession
posture of Section 2.4, without any commitment to a field name or format). The `Recorded` value
and the attendance outcome values are governed by `CAP-STATUSENUMS` (Section 9.1); transitions
remain governed by this section.
```

## H6 — §3.1 The seven service domains (ESS row replaced; FRAS row extended)

ESS row:
```markdown
| **ESS** | Instantiate learning: sections, enrollments, scheduling; enforce capacity constraints at enrollment; own per-session attendance. | Enroll a student in a section, validated against prerequisites (AMS) and capacity (ECS); return a student's enrollment instance; mark attendance for a scheduled session, validated against instructor-of-record assignment (FRAS) and period status (ECS); return a student's attendance aggregate for a section and period (derived, deterministic, under the governing rule set). | `Section`, `Enrollment`, `Session`, `AttendanceRecord` |
```
ESS calls FRAS for the assignment (FRAS row below); ESS does not read the assignment from elsewhere.

FRAS row:
```markdown
| **FRAS** | Allocate instructional resources to scheduled sections; own instructor load. | Assign an instructor to a section, validated against instructor load; return an instructor's load record; return the instructor of record assigned to a section. | `Faculty`, `Assignment`, `LoadRecord` |
```
Other rows unchanged. §3.2 unchanged — ESS is already in the closed ECS-consumer set.

## H7 — §4.1 Non-goals (new bullet, appended to the list)

```markdown
* **Attendance and the proof.** Attendance is not part of the proof. No attendance datum is part
  of the digested payload; attendance is never a canonical field. Attendance may influence the
  grade only as an ECS `FormulaRules` input. Attendance policy thresholds (for example, a minimum
  attendance requirement) and formula weights are ECS rule content; this specification does not
  define them.
```

## H8 — §4.2 Success criteria (new row, appended — next free number is S-8)

```markdown
| S-8 | A student's per-session attendance in an `Active` period is recordable by the section's instructor of record, and consumers can obtain the student's attendance aggregate for formula input. | For a section with a scheduled session in an `Active` period: attendance records exist per (session, student), carry the governing rule set identifier, and are marked only by the instructor of record validated via FRAS; the aggregate is derived deterministically from those records under that rule set; a non-`Active` period refuses creation; an actor FRAS does not return as instructor of record is refused; a correction appears as an appended successor with the original unchanged. |
```

## H9 — §5 Quality expectations (Determinism row extended)

```markdown
| **Determinism** | Given the same rule set and the same assessed inputs, the computed grade must be identical. The rule set identifier must therefore be sufficient to reproduce a computation. Aggregation of attendance records is likewise deterministic: the same attendance records for a (student, section, period) under the same governing rule set always yield the same aggregate. |
```

## H9b — §3.5 The audit trail has a stated home (enumeration extended, not appended around)

Current: *"The operational record store holds the complete, authoritative academic history: finalized grade records, appeal records, approval-chain review logs, student-period records, level-completion records, and their linkage."*
Proposed replacement (single sentence):

```markdown
The operational record store holds the complete, authoritative academic history: finalized grade
records, appeal records, approval-chain review logs, student-period records, level-completion
records, attendance records (ESS-owned, attributable to the marking actor, never proof-visible), and
their linkage.
```

## H10 — §10 Glossary (new terms, appended)

```markdown
| **Session** | A scheduled meeting occurrence of a section, against which attendance is recorded. Owned conceptually here; its field-level contract is defined by a task specification, not by this document. Not to be confused with the volatile capture metadata excluded from the canonical form under Section 2.8's "session identifiers" exclusion — that exclusion concerns digest capture, not the attendance Session. |
| **AttendanceRecord** | An ESS-owned operational record of one student's outcome in one session. Outcome values are governed by `CAP-STATUSENUMS` (Section 9.1); corrections append a linked successor; originals are never altered. Carries the governing rule set identifier. Never proof-committed. Field-level detail (including the parent-reference field name and format) belongs to its task-level contract. |
```

## H11 — §8.2 Section-anchor map (new row appended)

```markdown
| Attendance capability and workflow | Section 2.1, Section 2.2, Section 2.9, Section 2.10, Section 3.1 |
```
*(The existing map rows carry a mojibake byte where a section glyph once lived — pre-existing, out of scope. This row uses plain "Section n" to avoid engraving a new mojibake; the map's A-prefix style can be re-applied byte-for-byte by the applier if consistency is preferred.)*

## H12 — §12 Approval status (change record appended at application time)

```markdown
**Change record (v1.3).** 2026-11-19: Workflow W-7 (Section 2.10) and capability C-8 added —
per-session attendance recording owned by ESS (`Session`, `AttendanceRecord`), marked by the
instructor of record validated via FRAS (new FRAS operation: return the instructor of record
assigned to a section), period status enforced via ECS (W-1, whose trigger enumeration now names
attendance marking), outcome vocabulary and `Recorded` state governed by `CAP-STATUSENUMS`,
append-only correction, attendance aggregate derived deterministically for formula input and named
against the governing rule set, attendance never proof-committed nor part of the canonical form,
and `AttendanceRecord` carries the governing rule set identifier. Section 2.3 annotated: the
governing grading formula (including any attendance weight in a composite activities block;
weights illustrative, binding nothing) is ECS `FormulaRules` content; this specification does not
author it. Sections 2.2, 2.3, 2.9, 3.1, 3.5, 4.1, 4.2 (new S-8; S-4 unchanged — attendance cannot
exist outside an `Active` period and is covered there), 5, 8.2, 10 updated to match; Section 1.3
untouched (Primary-emphasis reading risk accepted); Section 9 unchanged. Fulfilled through Section
11: Change Request `WORK-191`; independent review 2026-11-19, executed in two passes — pass 1
    verdict CHANGES REQUIRED (majors F-01 to F-05, minors F-06 to F-13, informational F-14/F-15,
    all dispositioned in the draft as recorded in the work ledger); pass 2 verdict
    APPROVED WITH COMMENTS on that draft (comments N-1 to N-6, all discharged at application time;
    N-2 anchor map gains Section 2.2; N-3 disposition citation corrected; N-5 §3.5 enumeration
    extended in place; N-4 atomic-application guard executed and result recorded in the applying
    Decision's history). Atomic Gate 2 approval recorded as Decision `WORK-<id>` (<date>)
covering this SRS v1.3 change and the paired `CAP-STATUSENUMS` v1.1 → v1.2 revision (new
attendance outcome domain and AttendanceRecord transition table; capability text re-anchored to
SRS §2.9 v1.3). Version incremented to 1.3 and `updated` set to the application time, per Section
11. v1.2 remains retrievable at the commit carrying it (`b6ce80c`), anchored to approval Decision
`WORK-176`; this v1.3 revision is anchored to Decision `WORK-<id>` and to the commit carrying this
change (the commit SHA is recorded in the work ledger history at commit time). The specification
collection `SPEC-LMS-v1.0` remains version 1.0 by Decision (unchanged; root specification version is
the change signal; `root_spec.version` and the SRS `spec_files` entry in both `binding.yaml` files
move to 1.3). The id `SRS-LMS-v1.0` and the filename are unchanged. **No requirement was added,
removed or modified beyond the named additions and the named §2.2 trigger extension**; Sections
2.4–2.8 are unchanged in substance.
```

---

## H12-addendum — Paired CAP-STATUSENUMS v1.2 (atomic with v1.3; applied in the same change)

C1. **Description** gains: *"…and level-completion records. As of v1.2 it also governs the attendance outcome domain and the AttendanceRecord `Recorded` state (W-7)."*
C2. **Normative Definition** gains a second table after the status table:
```markdown
| Value domain | Values |
|---|---|
| Attendance outcome (AttendanceRecord) | `Present`, `Absent`, `Late`, `Excused` |
```
and the status table gains:
```markdown
| AttendanceRecord | `Recorded` |
```
with the identity sentence re-anchored: *"The values below are identical to the SRS Section 2.9 (v1.3) transition tables; the attendance outcome domain is defined by W-7 (Section 2.10)."*
C3. **Status Transition Rules** gains (identical to SRS §2.9 v1.3):
```markdown
### Attendance record

| From | Event | To |
|---|---|---|
| — | Instructor of record marks a session (W-7 step 4) | `Recorded` |
```
plus: *"No further transitions. A correction appends a successor linked by a parent reference; originals are never altered. There is no `Superseded` state."*
C4. Frontmatter: `version: 1.2`, `updated` at application time; **change record** notes the v1.2 addition and the atomic Gate 2 with SRS v1.3; SRS-references re-anchored to §2.9 v1.3. **Atomic-application guard (N-4):** the applier must diff the SRS §2.9 attendance transition block against the capability's AttendanceRecord transition block and record the result (byte-identical or not) in the applying Decision's history; if not identical, stop and reconcile before committing.

---

## Explicitly out of scope (unchanged artifacts)

- Field-level contracts: `Session`, `AttendanceRecord`, `FormulaRules` (grade-configuration), `GradeRecord` — each becomes a `wf-task-noncode` specification against this v1.3 parent.
- Proof, canonical form, `CAP-CANONICAL-FORM`, LGS — untouched by construction.
- Retention-policy Decision (constitution tension 1) — still owed separately; attendance retention follows the same unresolved question.
- `service-contracts.yaml` — ESS remains `not-yet-specified` at binding level; bindings are decided at implementation-plan time, not by this CR.
- Technology, deployment, directory layout — implementation-plan concerns; SRS stays agnostic.
- Q-2 (`parent_transaction_id` format) — untouched; the attendance parent reference is deliberately not named or formatted here.

## Downstream (after Gate 2)

1. Paired `CAP-STATUSENUMS` v1.2 — applied atomically in the same change (H12-addendum).
2. `wf-task-noncode`: `Session` + `AttendanceRecord` contract (attendance slice).
3. `wf-task-noncode`: `FormulaRules` / grade-configuration contract — formula content stays ECS-owned and unauthored.
4. `wf-task-noncode`: `GradeRecord` contract (existing gap, unchanged by this CR).
5. Coding slices via `@wf-task-code` targeting `generated-projects/blockchain-enabled-lms/` — only after the contracts they depend on are Approved.

**Self-check:** F-13 weights appear only in H3 and H12, both explicitly non-normative ("illustrative only; binds nothing").
