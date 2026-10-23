# Canonical Example: Deffuant-Weisbuch Opinion Dynamics

This folder contains a complete reference implementation of the classical **Deffuant-Weisbuch Bounded Confidence Model** of continuous opinion dynamics (Deffuant et al., 2000).

It demonstrates the complete 4-stage ABMforAI workflow:
1. **Elicit:** Conceptual interview record in `specification.md`.
2. **Formalize:** Full ODD protocol specification in `odd.md` and theoretical consensus in `decision-log.md`.
3. **Simulate:** Modular Python implementation in Mesa 3.x (`agents.py`, `model.py`, `experiments.py`, `metrics.py`, `experiment-config.yaml`).
4. **Verify:** Comprehensive verification test suite covering checks V1-V8 in `tests/test_model.py`.

---

## The Phenomenon

The model explores how continuous opinions (such as attitudes toward a policy, ideology, or social topic) evolve when individuals only interact with peers who hold similar viewpoints.

- Each agent $i$ possesses an opinion $x_i \in [0, 1]$.
- In each interaction between agents $i$ and $j$, they compare opinions.
- If $|x_i - x_j| < \epsilon$ (the tolerance or confidence bound), their opinions converge:
  $$x_i \leftarrow x_i + \mu (x_j - x_i)$$
  $$x_j \leftarrow x_j + \mu (x_i - x_j)$$
  where $\mu \in (0, 0.5]$ is the convergence rate.
- If $|x_i - x_j| \ge \epsilon$, no interaction occurs.

### Emergent Patterns
Depending on the tolerance threshold $\epsilon$:
- **High tolerance ($\epsilon \ge 0.3$):** Global consensus (a single shared central opinion).
- **Moderate tolerance ($\epsilon \approx 0.2$):** Bipolarization (two distinct opposing opinion clusters).
- **Low tolerance ($\epsilon \le 0.1$):** Fragmentation into multiple echo chambers.

---

## File Structure

```text
opinion-dynamics/
├── README.md               # Overview and instructions
├── specification.md        # Stage 1: Conceptual interview record
├── odd.md                  # Stage 2: Formal ODD protocol (Grimm et al. 2020)
├── decision-log.md         # Stage 2: Log of theoretical decisions and assumptions
├── TASKS.md                # Task tracking and evidence-gated completion landmarks
├── experiment-config.yaml  # Parameter definitions, named scenarios, and parameter sweeps
├── requirements.txt        # Pinned dependencies (mesa 3.5, numpy, matplotlib, pytest)
├── agents.py               # OpinionAgent class with ODD annotations
├── model.py                # OpinionModel class with DataCollector and Mesa 3 AgentSet
├── experiments.py          # Runner for multi-seed baseline, scenarios, and sweeps
├── metrics.py              # Cluster detection, variance calculation, and plots
├── verification-report.md  # Stage 4: Comprehensive model verification report
└── tests/
    ├── __init__.py
    └── test_model.py       # Mandatory verification checks (V1 to V8)
```

---

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Verification Tests
```bash
pytest tests/ -v
```

### 3. Run Experiments and Generate Plots
```bash
python experiments.py
```
This produces raw simulation metrics in `output/` and plot figures showing opinion trajectories and cluster distributions.
