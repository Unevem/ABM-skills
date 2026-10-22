---
description: Guidelines for explicit random seed control, stochasticity, and invariance testing in simulation models.
trigger: model_decision
---

# Rule: Reproducibility & Stochasticity

## Objective
Ensure that any scientific model built using these guidelines can be reproduced exactly across machines, runs, and platforms.

## Guidelines for Stochastic Models

1. **Explicit Random Seeds:**
   - Every model class must accept a `seed` argument (integer or `None`).
   - Use dedicated random number generators (RNG) attached to the model instance (e.g., `self.random` in Mesa or an explicit `numpy.random.Generator`), rather than relying on global `random.random()` or global `np.random`.
   - Running the simulation with the same seed, parameters, and step count **must produce identical trajectories and metric outputs**.

2. **No Magic Numbers:**
   - Hardcoded constants in the middle of functions are prohibited.
   - All parameters must be declared as configurable attributes of the model, passed via `__init__`, or loaded from an external experiment configuration file (`experiment-config.yaml`).

3. **Invariance and Sanity Testing:**
   - Every model must be accompanied by automated sanity tests (in `tests/`):
     - **Deterministic Seed Test:** Running `model(seed=42)` twice yields bit-for-bit identical aggregate metric logs.
     - **Conservation Laws:** Total population, energy, or mass checks across steps (if applicable to the domain).
     - **Domain Boundaries:** Ensuring bounded state variables (e.g., probability, opinion $\in [0, 1]$) never escape their mathematical definitions.
