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
   - Once implementation and sanity checks pass, move it to `Completed`.
3. **Escalate Blockers:**
   - If an unstated assumption or design choice arises, immediately append it to `Decisions Needed` and halt further dependent implementation.
4. **No Phantom Tasks:**
   - Never remove or mark an item as `Completed` without verifying that the corresponding file, test, or documentation section actually exists and is complete.
