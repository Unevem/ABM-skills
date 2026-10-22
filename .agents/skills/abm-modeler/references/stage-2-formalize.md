# Stage 2: Formalize

Goal: turn the approved `model-specification.md` into an ODD protocol that is
precise enough to implement **without a single guess**, plus a decision log
and an implementation task list.

Standard: ODD protocol, second update — Grimm, V., et al. (2020). "The ODD
Protocol for Describing Agent-Based and Other Simulation Models: A Second
Update to Improve Clarity, Replication, and Structural Realism." *Journal of
Artificial Societies and Social Simulation*, 23(2), 7.

**No model code is written in this stage.**

---

## ODD Structure and Numbering

Use this numbering in `odd.md`. Code comments refer to these numbers.

### Overview
1. **Purpose and patterns** — the question the model answers, and the
   patterns used to judge whether it is useful.
2. **Entities, state variables, and scales** — every entity type, every
   state variable (name, type, unit, range, static or dynamic), the meaning
   of one time step, the run length, and the spatial extent.
3. **Process overview and scheduling** — the ordered list of processes in a
   step, who executes each one, the update mode (synchronous or
   sequential), and the activation order.

### Design concepts
4. **Design concepts** — answer each one, or write "Not applicable" with a
   one-line reason:
   - 4.1 Basic principles
   - 4.2 Emergence
   - 4.3 Adaptation
   - 4.4 Objectives
   - 4.5 Learning
   - 4.6 Prediction
   - 4.7 Sensing
   - 4.8 Interaction
   - 4.9 Stochasticity
   - 4.10 Collectives
   - 4.11 Observation

### Details
5. **Initialization** — the exact initial state, how it is generated, and
   whether it varies between runs.
6. **Input data** — external time series or data files, or "None".
7. **Submodels** — one subsection per process listed in section 3
   (7.1, 7.2, ...). Each one contains:
   - the equation or algorithm, written so it can be implemented
     unambiguously (pseudocode is welcome);
   - every parameter it uses, with its symbol, meaning, default value, and
     range;
   - its edge cases (ties, empty neighborhoods, boundary values);
   - **Implemented in:** the function that implements it (filled in at
     Stage 3).

### Annex (recommended)
- **Parameter table:** symbol, name, default, range, unit, source
  (`researcher`, `literature: <ref>`, or `[ASSUMPTION]`).
- **Output table:** metric name, definition, collection frequency.

---

## Formalization Checks

Before handing the ODD to the researcher, check each of these:

1. **Implementability.** Could a programmer who has never talked to the
   researcher implement every submodel identically? If not, find the
   ambiguity and tag it `[DECISION NEEDED]`.
2. **Coverage.** Every process in section 3 has a submodel in section 7.
   Every state variable in section 2 is initialized in section 5 and used
   somewhere.
3. **Hidden choices.** Look for these common silent defaults:
   - tie-breaking (two equally good options);
   - empty neighborhoods or isolated nodes;
   - division by zero or values leaving their range;
   - whether agents see the state from before or after the current step's
     updates;
   - whether an agent can interact with itself, or with the same partner
     twice in one step;
   - the order of sub-steps within a step.
4. **Tags.** Every `[ASSUMPTION]` points to a decision-log entry. List the
   remaining `[DECISION NEEDED]` tags and which sections they block.
5. **Parameters.** Every parameter has a default and a range, and its source
   is known.

---

## Implementation Task List

Once the ODD is approved, break it into atomic tasks in `TASKS.md` under
`## Pending`. Typical order:

1. Project scaffold (files, `requirements.txt`, `experiment-config.yaml`
   with all parameters).
2. Agent class(es) with state variables (ODD 2).
3. Model initialization (ODD 5).
4. One task per submodel (ODD 7.x).
5. Scheduling in `Model.step()` (ODD 3).
6. Data collection of outputs (ODD 4.11, output table).
7. Tests (Stage 4).
8. Experiments and plots.

Each task names the ODD section it implements.

---

## Exit Criteria

- `odd.md` has all sections; none that Stage 3 will implement contains
  `[DECISION NEEDED]`.
- `decision-log.md` covers every `[ASSUMPTION]`.
- `TASKS.md` contains the implementation tasks.
- The researcher has explicitly approved the ODD.

Then move to Stage 3.
