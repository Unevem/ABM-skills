---
name: abm-reviewer
description: >-
  Use this skill to conduct an adversarial, multi-stage audit of an Agent-Based
  Model (ABM) before stage transitions, human sign-offs, or git commits.
  Verifies ODD protocol completeness, decision log honesty, parameter range
  alignment across documentation, YAML config, code and tests, absence of config
  drift (seeds and sweeps), absence of phantom completed tasks, and empirical
  fidelity against confirmation bias.
---

# ABM Reviewer & Audit Skill

This skill acts as an adversarial, methodological reviewer for Agent-Based Models (ABM). Its primary purpose is to catch the known failure modes of AI assistants (silent assumptions, config drift, range discrepancies, fabricated consensus, and phantom task completion) **before** changes are committed to Git or submitted to the researcher.

---

## When to Run This Skill

1. **Pre-Commit Gate:** Mandatory check before executing any `git commit`.
2. **Stage Transition Gate:** Before closing any stage (Elicit -> Formalize -> Simulate -> Verify).
3. **Audit Request:** When the researcher asks for a sanity check or review of an existing model.
4. **Pre-Grill-Me Prep:** Before presenting results to the researcher, to ensure all claims are backed by verifiable evidence.

---

## The 6-Dimension Review Protocol

When executing this skill, walk through every dimension systematically. Do not skip checks.

```
[1. Decision Log]  --> [2. Formalization / ODD] --> [3. Code & ODD Traceability]
        |                        |                             |
[4. Config Alignment] --> [5. Test & Invariants] --> [6. Tasks & Landmarks]
```

---

### Dimension 1: Decision Log & Theoretical Honesty
- [ ] **No Fabricated Consensus:** Check every entry marked `Decided by: researcher`. Was this question actually asked to the researcher in the conversation history? If not, flag immediately as a critical defect.
- [ ] **Honest Attribution:** If the researcher agreed with an agent proposal, does the rationale explicitly state `"Researcher accepted agent recommendation: <literature basis>"`?
- [ ] **Technical Decisions Logged:** Are library additions, refactorings, or API deprecation adaptations logged as `Decided by: agent (technical)`?
- [ ] **No Dangling Tags:** Ensure no `[DECISION NEEDED]` remains in files intended for simulation. Ensure every `[ASSUMPTION]` in documentation or code cites a matching `#ID` in `decision-log.md`.

### Dimension 2: Specification & ODD Consistency
- [ ] **ODD Completeness:** Are all canonical sections 1 to 7 present?
- [ ] **Submodel Mapping:** Does every submodel in ODD Section 7 have an explicit **Implemented in:** field pointing to a real Python function/method?
- [ ] **Boundary & Edge Conditions:** Are boundary conditions, initial states, and scheduling mechanisms fully specified without ambiguity?

### Dimension 3: Code Architecture & ODD Grounding
- [ ] **In-Code ODD Annotations:** Does every agent class, behavioral method (`interact`, `step`), and schedule loop contain an explicit `# ODD Section X.Y` citation?
- [ ] **Reproducibility & Randomness:**
  - Is random seed control explicit in the model constructor?
  - For Mesa 3.5+, is `super().__init__(rng=seed)` used to prevent deprecation warnings?
  - Are all random draws derived strictly from `self.random` or `self.rng`? (Zero use of global `random` or `np.random`).
- [ ] **No Hardcoded Magic Numbers:** Are behavioral thresholds, rates, or constants exposed as configurable parameters in `__init__` and `experiment-config.yaml`?
- [ ] **Modular Separation:**
  - `agents.py`: state variables and behavioral rules only.
  - `model.py`: initialization, space, scheduling, and DataCollector only.
  - `metrics.py`: metric functions, clustering, and plots only.
  - `experiments.py`: experiment runner only.

### Dimension 4: Configuration & Parameter Range Alignment
- [ ] **Cross-Layer Range Uniformity:** Compare parameter ranges across all 4 layers:
  1. ODD Parameter Table (Annex A.1)
  2. `experiment-config.yaml` schema (`range: [min, max]`)
  3. `Model.__init__` argument validation (`if param < min: raise ValueError`)
  4. Test assertions (especially edge cases in V8)
  *Defect Trigger:* If ODD says $N \in [10, 10000]$ but code allows $N=1$, flag range drift.
- [ ] **Config Consumption (No Config Drift):**
  - Are **all** seeds in `run_controls.seeds` actually executed by `experiments.py`?
  - Are defined scenarios iterated over?
  - Is `parameter_sweep` executed or explicitly reported as deferred?
  - Do exported CSVs include columns identifying the `seed` and scenario parameters?

### Dimension 5: Empirical Integrity & Invariant Verification
- [ ] **Full Test Suite Passing:** Run pytest (`pytest tests/ -v`) in the active virtual environment. Verify 0 failures and 0 unexpected warnings.
- [ ] **True Invariant Verification:** Does test V4 test natural mathematical bounds rather than masking bugs with artificial `np.clip` or `min/max`?
- [ ] **No Narrative Confirmation Bias:**
  - Compare the actual numbers from simulation runs against the textual claims.
  - If a scenario text says "two polarized clusters" but the cluster algorithm outputs 3 clusters (e.g., sizes 414, 5, 581), flag the discrepancy!
  - Never alter or suppress empirical data to match theoretical expectations.

### Dimension 6: Tasks, Landmarks, and Human Governance
- [ ] **No Phantom Completion:** Check every item marked `[x]` in `TASKS.md` and `PLAN-IN-STEPS.md`. Does the artifact file, test output, or report actually exist on disk?
- [ ] **Evidence-Gated Landmarks:** Was each completed item accompanied by concrete evidence and signed off by the researcher?
- [ ] **Decisions Needed Section:** Does `## Decisions Needed` list all unresolved questions, along with the specific tasks they block?

---

## Output Format: The Review Audit Report

When concluding the review, output a structured report in the researcher's language:

```markdown
### ABM Review Audit Report
**Target:** <Directory or Component reviewed>
**Trigger:** <Pre-commit / Stage Gate / Manual Audit>

#### 1. Compliance Summary
- Decision Log Honesty: [PASS / FAIL]
- ODD & Specification Completeness: [PASS / FAIL]
- Code Grounding & Reproducibility: [PASS / FAIL]
- Parameter & Config Range Alignment: [PASS / FAIL]
- Empirical Integrity & Test Verification: [PASS / FAIL]
- Task Contract & No-Phantom Verification: [PASS / FAIL]

#### 2. Discovered Discrepancies & Drift
- [List any drift, range mismatches, or unexecuted config items]

#### 3. Empirical Anomalies vs. Theoretical Narratives
- [List any difference between simulation outputs and scenario descriptions]

#### 4. Required Fixes Before Commit / Sign-Off
1. [Actionable fix 1]
2. [Actionable fix 2]

#### 5. Verdict
- [READY TO COMMIT / BLOCKED PENDING CORRECTIONS]
```
