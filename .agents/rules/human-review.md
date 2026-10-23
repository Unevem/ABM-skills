---
description: Mandatory criteria and triggers for halting code generation and requesting human review on theoretical ABM decisions.
trigger: always_on
---

# Rule: Human Review Gate

## Context
In scientific Agent-Based Modeling, domain validity rests entirely on the researcher's theoretical foundations. An AI assistant can structure, optimize, and write code, but it must **never** take autonomous ownership of theoretical decisions.

## Mandatory Trigger Conditions
The AI **must pause** and explicitly request human review before proceeding in the following circumstances:

1. **Choice of Decision Architecture:**
   - Whether agents use threshold rules, utility maximization, heuristic imitation, or stochastic transitions.
2. **Topology & Spatial Definition:**
   - Whether interaction is well-mixed (mean-field), bounded on a discrete grid (Moore vs. Von Neumann), continuous 2D space, or a complex network.
3. **Temporal Dynamics (Scheduling):**
   - Whether updates are synchronous, random sequential, priority-based, or continuous-time.
4. **Boundary & Edge Conditions:**
   - Periodic (toroidal), absorbing, reflective, or infinite boundaries.
5. **Emergent Invariant Definition:**
   - Determining what constitutes a valid state vs. an invalid state (e.g., can agent wealth/opinion fall below zero or exceed one?).
6. **Task Completion and Stage Transitions:**
   - Moving any task to `Completed` or concluding any workflow stage. The AI must first prove to the user that it succeeded (providing concrete execution evidence), present a structured review gate (or invite `/grill-me`), and await explicit approval.

## Protocol for Requesting Review
When one of the trigger conditions is met:
1. Append the pending decision to `TASKS.md` under `## Decisions Needed`.
2. Formulate a multiple-choice or structured question for the researcher:
   - State clearly **what** needs to be decided.
   - Explain the theoretical implications of each alternative in plain language.
   - Offer a recommended option based on standard literature if appropriate, but wait for explicit confirmation.
3. **Do not write dependent code** until the researcher responds.
