# Stage 3: Simulate

Goal: implement the approved ODD as modular Python, one atomic task from
`TASKS.md` at a time.

Default stack: **Mesa 3.x**. Plain Python (optionally with NumPy or NetworkX)
is fine when Mesa adds no value; the same layout and rules apply.

Before writing Mesa code, check the installed version
(`python -c "import mesa; print(mesa.__version__)"`). Mesa's API changes
between minor versions. If something below does not match the installed
version, follow the installed version's documentation and record the
difference in the decision log as a technical decision.

---

## Project Layout

```text
<model-name>/
├── README.md               # What the model is, how to run it
├── model-specification.md  # Stage 1 output
├── odd.md                  # Stage 2 output
├── decision-log.md
├── TASKS.md
├── experiment-config.yaml  # All parameters with defaults; scenarios
├── requirements.txt        # Pinned major versions, e.g. mesa>=3.0,<4
├── agents.py               # Agent classes: state + individual behavior
├── model.py                # Model: init, space, scheduling, data collection
├── experiments.py          # Single runs, scenarios, parameter sweeps
├── metrics.py              # Output metrics and plots
└── tests/
    ├── __init__.py
    └── test_model.py       # Stage 4 checks
```

### Responsibilities

| File | Contains | Does not contain |
|---|---|---|
| `agents.py` | State variables (ODD 2), behavioral methods (ODD 7.x) | Scheduling, global loops, file I/O, plotting |
| `model.py` | Parameters, initialization (ODD 5), space, `step()` order (ODD 3), `DataCollector` | Behavioral rules belonging to agents, plotting |
| `experiments.py` | Loading the config, running scenarios and sweeps, saving raw output | Model logic |
| `metrics.py` | Metric functions, plots, summary tables | Model logic |

---

## Mesa 3.x Conventions

```python
import mesa


class OpinionAgent(mesa.Agent):
    """ODD 2 - Entity: individual holding an opinion."""

    def __init__(self, model: "OpinionModel", opinion: float) -> None:
        super().__init__(model)          # unique_id is assigned automatically
        self.opinion = opinion           # ODD 2: float in [0, 1], dynamic

    def step(self) -> None:
        """ODD 3 - Process 1: pick a partner and revise opinion."""
        partner = self.model.random.choice(self.model.agents.to_list())
        self.revise(partner)

    def revise(self, partner: "OpinionAgent") -> None:
        """ODD 7.1 - Submodel: Opinion Revision."""
        ...


class OpinionModel(mesa.Model):
    """ODD 1-3 - Model controller."""

    def __init__(self, n_agents: int = 100, epsilon: float = 0.2,
                 mu: float = 0.5, seed: int | None = None) -> None:
        super().__init__(seed=seed)      # seeds self.random and self.rng
        self.epsilon = epsilon           # ODD 7.1, parameter epsilon
        self.mu = mu                     # ODD 7.1, parameter mu

        # ODD 5 - Initialization
        for _ in range(n_agents):
            OpinionAgent(self, opinion=self.random.random())  # auto-registered

        self.datacollector = mesa.DataCollector(
            model_reporters={...},       # ODD annex - output table
            agent_reporters={"opinion": "opinion"},
        )
        self.datacollector.collect(self)

    def step(self) -> None:
        """ODD 3 - Process overview and scheduling."""
        self.agents.shuffle_do("step")   # random sequential activation
        self.datacollector.collect(self)
```

The values and rules in this example are illustrative only. Real models take
them from the ODD.

### Key points
- **No schedulers.** Mesa 3 removed `RandomActivation` and the other
  schedulers. Express the ODD 3 schedule with `AgentSet` operations:
  - random sequential: `self.agents.shuffle_do("step")`
  - fixed order: `self.agents.do("step")`
  - synchronous (all agents read the old state, then all update): two phases,
    e.g. `self.agents.do("compute")` then `self.agents.do("apply")`
  - per type: `self.agents_by_type[AgentType].shuffle_do("step")`
  - Which one to use is a theoretical decision (ODD 3). Never pick it
    yourself.
- **Agents register themselves** on creation. Remove one with
  `agent.remove()`.
- **Steps are counted automatically** in `self.steps`. Do not keep your own
  counter.
- **Randomness:** use only `self.random` (Python `Random`) or `self.rng`
  (NumPy `Generator`) on the model (`self.model.random` from an agent).
  Both are seeded by `super().__init__(seed=seed)`.
- **Indexing:** `model.agents` is a set. Use `.to_list()` when you need
  indexing, and remember that iteration order can depend on insertion
  order.
- **Space:** for new grid and network models, prefer the cell-space API
  (`mesa.discrete_space`) if the installed version provides it; the legacy
  `mesa.space` classes still exist. Neighborhood type, torus, and capacity
  per cell are ODD decisions.
- **Visualization** (Solara-based in Mesa 3) is optional and lives outside
  `model.py`.

---

## Coding Rules

1. **One task at a time.** Move it to `In Progress` in `TASKS.md`, implement
   it, test it, and report.
2. **ODD annotations.** Every class and behavioral method has a docstring
   starting with its ODD reference. Non-obvious lines carry an inline
   `# ODD x.y` comment. See [guardrails.md](guardrails.md) §4.
3. **Fill in the reverse link.** After implementing a submodel, set its
   **Implemented in:** field in `odd.md`.
4. **Parameters.** Every parameter is an `__init__` argument with the ODD
   default, and appears in `experiment-config.yaml`. Behavior never depends
   on a literal inside a method.
5. **Type hints and docstrings** on all public functions. The researcher must
   be able to read the code.
6. **No silent fixes.** If the ODD turns out to be ambiguous or impossible
   to implement as written, stop and go back to Stage 2. Do not "make it
   work".
7. **Readability over cleverness.** Prefer explicit loops to dense
   vectorization unless performance requires it. If you optimize, log it as a
   technical decision and keep a test showing the behavior is unchanged.

---

## Exit Criteria

- Every ODD 7.x submodel has an annotated implementation, and its
  **Implemented in:** field is filled.
- `python experiments.py` (or the documented command) runs with the default
  configuration without errors.
- All implementation tasks in `TASKS.md` are `Completed`, with evidence.
- The researcher has reviewed the behavioral code (`agents.py` and
  `Model.step()`).

Then move to Stage 4.
