# Guardrails

These rules apply in every stage of the workflow. They are bundled inside the
skill so that it works in any project. When the host repository also defines
`.agents/rules/`, both sets apply, and the stricter rule wins.

---

## 1. Ownership of Decisions

The researcher owns theory. The agent owns software craftsmanship.

**Theoretical decisions (always the researcher's):**

| Category | Examples |
|---|---|
| Decision architecture | Threshold rule, utility maximization, imitation, reinforcement learning, stochastic transition |
| Functional forms | Update equations, payoff matrices, influence or similarity functions, probability distributions |
| Parameter values and ranges | Population size, rates, thresholds, initial distributions |
| Topology and space | Well-mixed, grid (Moore or Von Neumann neighborhood), continuous space, network type |
| Scheduling | Synchronous, random sequential, fixed order, priority-based, event-driven |
| Boundary conditions | Toroidal, reflective, absorbing, finite or infinite |
| Initialization | Homogeneous or heterogeneous agents, empirical or synthetic initial states |
| Validity invariants | Allowed ranges of state variables, conservation laws |
| Outputs | Which metrics answer the research question |

**Technical decisions (the agent may make these, and must document them in
the decision log):**
file layout, variable naming, data structures, plotting style, test
organization, and performance optimizations that do not change model behavior.

**If unsure which category a choice belongs to, treat it as theoretical.**

---

## 2. Tag Vocabulary

Exactly two tags exist. Use them verbatim, so they can be found with grep and
checked by validators.

### `[DECISION NEEDED]`

A gap the researcher has not resolved yet. It **blocks** all dependent work.

- Format: `[DECISION NEEDED] <question>`. Example:
  `[DECISION NEEDED] Are agent updates synchronous or random sequential?`
- Allowed in: `model-specification.md`, `odd.md`, `TASKS.md`.
- **Never allowed in code.** If code would need it, that code must not be
  written yet.

### `[ASSUMPTION]`

A provisional choice that the researcher **has accepted**, but that is not
yet grounded in data or literature, or that is marked for later sensitivity
analysis.

- Format: `[ASSUMPTION] <statement> (decision-log #N)`. Example:
  `[ASSUMPTION] Initial opinions are uniform on [0, 1] (decision-log #4)`
- Allowed in: documentation and code comments.
- Every `[ASSUMPTION]` must have a matching entry in `decision-log.md`.

A choice that is neither stated by the researcher nor accepted by them is not
an assumption. It is a `[DECISION NEEDED]`.

---

## 3. Halt Protocol

When a theoretical gap appears:

1. Stop work that depends on the gap. Unrelated work may continue.
2. Tag the gap `[DECISION NEEDED]` in the relevant document.
3. Add it to `TASKS.md` under `## Decisions Needed`.
4. Ask the researcher one structured question:
   - what must be decided, and why it matters for the research question;
   - 2-4 options, each with its theoretical consequence in plain language;
   - a recommended option, citing standard literature when possible;
   - an explicit statement that you will wait for their choice.
5. After the answer: record it in `decision-log.md`, replace the tag in the
   documents with the resolved content (or with `[ASSUMPTION]` if it is
   provisional), and move the item out of `## Decisions Needed`.

---

## 4. Traceability

Every behavioral element in the code points back to its definition.

```python
class OpinionAgent(mesa.Agent):
    def interact(self, partner: "OpinionAgent") -> None:
        """ODD 7.1 - Submodel: Opinion Revision."""
        # ODD 7.1, Eq. 1: update only if |x_i - x_j| < epsilon
        if abs(self.opinion - partner.opinion) < self.model.epsilon:
            # ODD 7.1, Eq. 2: symmetric convergence with rate mu
            self.opinion += self.model.mu * (partner.opinion - self.opinion)
```

- Use the format `ODD <section number>` (and the equation or rule label if one
  exists). ODD sections are numbered as in `odd.md`.
- Code comments carry `[ASSUMPTION] ... (decision-log #N)` wherever an
  assumption is implemented.
- In reverse, every ODD submodel must name the function that implements it.

---

## 5. Decision Log

`decision-log.md` is an append-only table. Each entry records:

| Field | Content |
|---|---|
| `#` | Sequential ID, never reused |
| Date | ISO date |
| Stage | Elicit / Formalize / Simulate / Verify |
| Topic | Short name (e.g., "Scheduling") |
| Decision | The chosen alternative |
| Alternatives considered | The options that were presented |
| Rationale | The researcher's justification or literature reference |
| Decided by | `researcher` or `agent (technical)` |
| Status | `confirmed` or `assumption` |

When a decision changes, add a new entry that references the old one. Never
edit or delete old entries.

---

## 6. TASKS.md Contract

The project root contains a `TASKS.md` with exactly these four sections, in
this order:

```markdown
# Tasks

## In Progress
- [ ] (at most 1-2 items)

## Pending
- [ ] ...

## Decisions Needed
- [ ] [DECISION NEEDED] ... (blocks: <task names>)

## Completed
- [x] ... (evidence: <file, test, or section>)
```

Rules:

1. Read it at the start of every session.
2. Move a task to `In Progress` before working on it.
3. Move it to `Completed` only after its output exists and has been checked.
   Cite the evidence.
4. Each item in `Decisions Needed` lists the tasks it blocks.
5. Never delete tasks silently. Abandoned tasks move to `Completed` with the
   reason.

---

## 7. Reproducibility

- The model takes a `seed` and passes it to `super().__init__(seed=seed)`.
- All randomness uses the model's generators (`self.random` or `self.rng`).
  Never use the global `random` or `np.random` modules.
- Every parameter is an argument of the model's `__init__` and appears in
  `experiment-config.yaml`. No literals that affect behavior appear inside
  methods.
- Same seed + same parameters + same code = identical output. This is tested
  (see Stage 4).

---

## 8. Scope Discipline

- Implement only what the ODD specifies. No "helpful" extra mechanisms.
- Do not modify files unrelated to the current task.
- After each task, tell the researcher which files were created or changed
  and why.
