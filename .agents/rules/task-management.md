---
description: Task lifecycle and state tracking rules for maintaining TASKS.md.
trigger: always_on
---

# Rule: Task Management & State Tracking

## Objective
Maintain a transparent, living record of project progress so that both the researcher and AI agents maintain context across sessions.

---

## The `TASKS.md` Contract

Every model directory must maintain a `TASKS.md` file organized strictly into four sections:

```markdown
# Tasks

## In Progress
- [ ] Currently active task (at most 1-2 items simultaneously)

## Pending
- [ ] Tasks queued for subsequent implementation

## Decisions Needed
- [ ] Questions requiring theoretical or domain guidance from the researcher

## Completed
- [x] Finished tasks with verifiable output
```

---

## Agent Operational Rules

1. **Check Before Acting:**
   - At the beginning of each turn, read `TASKS.md` to ground context.
2. **Move Atomic Tasks:**
   - Move an item from `Pending` to `In Progress` before generating code.
   - The AI is **strictly forbidden from unilaterally moving tasks to `Completed`**. Work must first be proven with verifiable evidence, followed by an interactive review gate.
3. **Escalate Blockers:**
   - If an unstated assumption or design choice arises, immediately append it to `Decisions Needed` and halt further dependent implementation.
4. **No Phantom Tasks:**
   - Never mark an item as `Completed` without proving that the corresponding file, test, or documentation section actually exists, is complete, and passes verification.
5. **Evidence-Gated Completion (Grill-Me Protocol):**
   - Finish each atomic task with a checkpoint report and empirical evidence.
   - The agent must demonstrate concrete proof of success to the researcher (e.g., test execution output, file validation, metrics table).
   - The agent triggers an interactive review gate (or invites a `/grill-me` alignment round), prompting the researcher to audit and validate the implementation.
   - Only upon explicit researcher confirmation does the task transition to `Completed`, formatted with its approved landmark: `(evidence: <files/command>; approved by researcher <date>)`.
6. **CLI-Mediated Task Governance:**
   - The AI is **strictly forbidden from directly editing `TASKS.md` with file tools** (`write_to_file`, `replace_file_content`).
   - All task operations must be executed exclusively via terminal commands using `python tools/tasks.py`:
     - Create: `python tools/tasks.py init [--path <TASKS.md>]`
     - Add/Queue: `python tools/tasks.py add "task description" [--section Pending|In Progress|Decisions Needed]`
     - Complete: `python tools/tasks.py complete "task text" --evidence <file_path>`
   - This ensures the AI cannot modify tasks without explicit human command approval, and programmatically prevents phantom tasks by verifying file existence on disk.
