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
3. **Evidence-Gated Completion (Grill-Me Protocol):** The agent is **strictly
   forbidden** from unilaterally moving tasks to `Completed`. A task moves to
   `Completed` only after:
   a) the agent demonstrates concrete empirical proof of success (real test
      outputs, generated artifacts, metric summaries);
   b) the agent presents the checkpoint to the researcher and triggers an
      interactive review gate (such as `/grill-me` or structured verification);
   c) the researcher explicitly approves the task.
4. Each item in `Decisions Needed` lists the tasks it blocks.
5. Never delete tasks silently. Abandoned tasks move to `Completed` with the
   reason.

---

## 7. Reproducibility

- The model takes a `seed` argument and passes it to the Mesa base class.
  The keyword depends on the installed version: recent Mesa 3.x releases
  use `super().__init__(rng=seed)` and deprecate `seed=`. Check the
  installed version, run the tests with warnings visible, and pin the tested
  range in `requirements.txt` (e.g. `mesa>=3.5,<4`).
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

---

## 9. Checkpoints (Never Do Everything at Once)

Work advances in small, reviewable increments separated by **checkpoints**.
A checkpoint is a landmark where the agent stops, explains what it did, and
waits for the researcher. Producing several stages, or several artifacts
that depend on each other, in a single turn is forbidden: errors made early
propagate silently into everything built on top of them.

### When a checkpoint is mandatory

1. After every question-and-answer round that produces a decision-log entry.
2. After each Stage 1-4 output document (`model-specification.md`, `odd.md`,
   `decision-log.md`, `verification-report.md`).
3. After each atomic implementation task (one file or one submodel).
4. After the test suite runs and after the experiments run.
5. Whenever the agent changes something the researcher did not ask for
   (dependency added, API adapted, file touched outside the task).

### Checkpoint report (in the researcher's language)

```text
CHECKPOINT <n> - <stage> - <task>
Done:        what was produced or changed (files, with links)
Decided by researcher:  decision-log entries created in this step (#IDs)
Decided by agent:       technical choices made in this step, and why
Not done / deviations:  anything skipped, simplified, or different from the
                        ODD, the config, or the plan
Evidence:    command run and its real output (tests, runs), or "none yet"
Next:        the single next atomic task
Waiting for: explicit approval to continue
```

Rules:

- Stop after the report. Do not start the next task in the same turn.
- The agent is **strictly forbidden from self-marking tasks as completed**.
- The "Decided by researcher" line may only list decisions the researcher
  actually answered in this conversation. If the list would be empty, say so.
- After the agent proves success and the researcher explicitly approves
  (via review, discussion, or `/grill-me`), add a landmark to the task in
  `TASKS.md` under `## Completed`:
  `(evidence: <files/command>; approved by researcher <date>)`.

---

## 10. Known Failure Modes

These errors happened in practice. Check for them before every checkpoint.

| Failure | What it looks like | Prevention |
|---|---|---|
| **Fabricated consensus** | The decision log lists decisions as `researcher` / `confirmed` that were never asked, or rationales put words in the researcher's mouth | Write a decision-log entry only right after the researcher answers. Record the exact choice. If the researcher took the recommendation, write "Researcher accepted agent recommendation" |
| **Batch execution** | Specification, ODD, decision log, code, and tests appear in one turn; the researcher sees them only at the end | Section 9: one artifact per checkpoint |
| **Phantom completion** | A task or plan item is marked done while its file does not exist | Mark done only with evidence that you just checked |
| **Autonomous completion** | The agent marks a task `[x] Completed` on its own without proving success or without an interactive review gate (`/grill-me`) | Strictly forbidden: prove success with real execution output, invite human review, and wait for explicit approval |
| **Config drift** | The config declares seeds, sweeps, or scenarios that the code silently ignores (e.g. only the first seed runs) | Correspondence check: every config key is either used or reported as a deviation |
| **Range drift** | Parameter ranges differ between the ODD table, the config, the code validation, and the tests | Compare all four in the correspondence check |
| **Narrative over evidence** | A scenario description promises an outcome ("two clusters") and the run shows something else, but the report repeats the description | Report observed results neutrally. When simulation results reveal empirical nuances (e.g. minor fringe clusters) that require updating stylized facts, apply the **Empirical Revision Tracking Pattern**: update the text, but explicitly embed an in-place `revision_note` (citing the data and decision-log #ID) rather than silently rewriting history |
| **Silent environment fixes** | A missing dependency or a deprecated API is patched without telling the researcher | Report it under "Decided by agent" and log it as a technical decision |
