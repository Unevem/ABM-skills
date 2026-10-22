---
description: Prohibits silent defaults and requires explicit tagging and traceability of all modeling assumptions back to ODD.
trigger: always_on
---

# Rule: Zero Undocumented Assumptions

## Objective
Prevent the silent introduction of hidden assumptions, default behavioral rules, or unverified mathematical formulas into scientific simulation models.

## Core Rules

1. **Explicit Tagging in Documentation (two tags only, used verbatim):**
   - `[DECISION NEEDED] <question>`: a gap the researcher has not resolved. It blocks all dependent work and is **never allowed in code**.
   - `[ASSUMPTION] <statement> (decision-log #N)`: a provisional choice the researcher has accepted but that is not yet grounded in data or literature. Allowed in docs and code comments; must have a `decision-log.md` entry.
   - A choice neither stated nor accepted by the researcher is not an assumption; it is a `[DECISION NEEDED]`.
   - Silent defaults (e.g., assuming agents have identical initial endowments without asking) are treated as bugs.

2. **In-Code Traceability (ODD-Grounded Code):**
   - Every behavioral method in `agents.py` or state transition in `model.py` must feature a comment tracing it to the corresponding ODD section or decision log entry:
     ```python
     # ODD: Section 4.3 - Submodel: Opinion Revision
     # Rule: Deffuant confidence bound |x_i - x_j| < epsilon
     if abs(self.opinion - partner.opinion) < self.model.epsilon:
         self.opinion += self.model.mu * (partner.opinion - self.opinion)
     ```

3. **Decision Log Entry:**
   - Any theoretical consensus reached during conversation with the researcher must be recorded in `decision-log.md` with:
     - Date & Step.
     - Decision topic.
     - Chosen alternative.
     - Theoretical rationale / literature basis.
