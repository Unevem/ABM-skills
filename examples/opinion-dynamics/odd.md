# ODD Protocol Specification: Deffuant-Weisbuch Opinion Dynamics

Conforms to the ODD Protocol (Grimm et al., 2020) and references canonical literature:
Deffuant, G., Neau, D., Amblard, F., & Weisbuch, G. (2000). "Mixing beliefs among interacting agents." *Advances in Complex Systems*, 3(01n04), 87-98.

---

## 1. Purpose and Patterns

The purpose of the model is to investigate the conditions under which continuous individual opinions in a population converge to global consensus, stabilize into polarized opposing factions, or fragment into multiple disjoint opinion clusters.

The model is designed as a foundational theoretical benchmark in social simulation and computational sociology.

### Stylized Facts to Reproduce
1. **Consensus Regime:** For high tolerance ($\epsilon \ge 0.3$), all agents converge to a single intermediate opinion cluster centered near 0.5.
2. **Polarization Regime:** For intermediate tolerance ($\epsilon \approx 0.2$), two distinct symmetrical extremist or moderate clusters emerge and stabilize.
3. **Fragmentation Regime:** For narrow tolerance ($\epsilon \le 0.1$), the population fragments into multiple non-interacting clusters.

---

## 2. Entities, State Variables, and Scales

### Entity Types and Attributes
| Entity Type | State Variable | Type | Unit | Range | Static/Dynamic | Description |
|---|---|---|---|---|---|---|
| `OpinionAgent` | `id` | int | - | [0, N-1] | Static | Unique identifier auto-assigned by Mesa |
| `OpinionAgent` | `opinion` | float | - | [0.0, 1.0] | Dynamic | Continuous attitude/opinion |

### Temporal and Spatial Scales
- **Time Step (dt):** 1 tick = 1 Monte Carlo sweep. During one step, each of the $N$ agents attempts one bilateral interaction on average.
- **Run Length:** Default $T = 1000$ steps (sufficient for asymptotic convergence under default parameters).
- **Spatial Extent & Topology:** Non-spatial, well-mixed global interaction pool. There is no physical geometry or distance metric; every agent is potentially connected to every other agent.

---

## 3. Process Overview and Scheduling

During each time step $t$, the simulation executes the following sequence:

1. **Agent Activation (Random Sequential):**
   - The set of active agents is randomly shuffled via `self.agents.shuffle_do("step")`.
   - Each agent selects an interaction partner $j \ne i$ at random from the population and executes the Opinion Revision submodel (Section 7.1).
   - Updates are sequential: changes to an agent's opinion take effect immediately and are observable by subsequent interactions within the same step.
2. **Observation & Data Collection:**
   - At the conclusion of step $t$, the `mesa.DataCollector` collects model-level statistics (mean opinion, opinion variance) and agent-level opinions.

---

## 4. Design Concepts

### 4.1. Basic Principles
The model implements the Bounded Confidence hypothesis (Deffuant et al., 2000): individuals only influence one another if their current beliefs are sufficiently close (within confidence bound $\epsilon$).

### 4.2. Emergence
Opinion clusters (number of factions, cluster positions, and cluster variances) emerge strictly from bottom-up bilateral pairwise compromises, without any top-down coordination, leadership, or external broadcast signals.

### 4.3. Adaptation
Agents adapt their opinion $x_i$ upon interacting with an eligible peer $j$ by shifting toward $x_j$. The adaptation is conditional on the threshold criterion $|x_i - x_j| < \epsilon$.

### 4.4. Objectives
Not applicable. Agents are behavioral and heuristic; they do not optimize an explicit objective or utility function.

### 4.5. Learning
Not applicable. Agents do not modify their adaptation rule over time.

### 4.6. Prediction
Not applicable. Agents do not forecast future opinion distributions.

### 4.7. Sensing
Agents sense the exact opinion $x_j$ of their chosen interaction partner with perfect accuracy (no sensory noise or misperception).

### 4.8. Interaction
Interactions are direct, bilateral, and symmetric. If agent $i$ and partner $j$ agree to interact, both adjust their opinions simultaneously toward each other.

### 4.9. Stochasticity
Pseudorandomness is used for:
1. Drawing initial opinions: $x_i(0) \sim \text{Uniform}(0.0, 1.0)$.
2. Shuffling agent activation order at each step.
3. Randomly choosing interaction partner $j \ne i$.
All stochastic processes use the dedicated generator seeded by `super().__init__(seed=seed)`.

### 4.10. Collectives
Collectives (opinion clusters) emerge dynamically as groups of agents with nearly identical opinions, but they have no formal organizational structure or collective agency.

### 4.11. Observation
- Aggregate metrics: `mean_opinion` ($\bar{x}$) and `opinion_variance` ($\sigma^2$) computed at every step.
- Micro metrics: Individual opinion trajectory $x_i(t)$ recorded for all agents.
- Post-simulation metrics: Final cluster count calculated by group clustering with threshold $\epsilon$.

---

## 5. Initialization

At time $t = 0$:
1. $N$ agents are instantiated and added to the model.
2. For each agent $i \in \{0, \dots, N-1\}$, initial opinion is drawn independently:
   $$x_i(0) \sim \text{Uniform}(0.0, 1.0)$$
3. The initial state is logged via `DataCollector.collect(self)`.

---

## 6. Input Data

The model is completely self-contained and does not consume external input datasets or time series.

---

## 7. Submodels

### 7.1. Opinion Revision
- **Purpose:** Execute bilateral compromise between agent $i$ and selected partner $j$.
- **Executed by:** `OpinionAgent.step()` calling `OpinionAgent.interact(partner)`.
- **Algorithm:**
  1. Agent $i$ chooses partner $j$ uniformly at random from $\{k \in \text{Agents} \mid k \ne i\}$.
  2. Compute opinion distance $\Delta = |x_i - x_j|$.
  3. If $\Delta < \epsilon$:
     $$x_i \leftarrow x_i + \mu (x_j - x_i)$$
     $$x_j \leftarrow x_j + \mu (x_i - x_j)$$
  4. Enforce invariant boundary:
     $$x_i \leftarrow \min(\max(x_i, 0.0), 1.0)$$
     $$x_j \leftarrow \min(\max(x_j, 0.0), 1.0)$$
- **Parameters Used:**
  - $\epsilon$ (`epsilon`): Confidence bound threshold. Default = 0.2, Range = $(0.0, 1.0]$.
  - $\mu$ (`mu`): Convergence rate parameter. Default = 0.5, Range = $(0.0, 0.5]$.
- **Edge Cases & Tie Breaking:**
  - If $N < 2$, no interaction can take place.
  - If $|x_i - x_j| = \epsilon$, no update occurs (strict inequality).
- **Implemented in:** `agents.py -> OpinionAgent.interact()`

---

## Annex: Parameter and Output Tables

### A.1. Parameter Table
| Symbol | Parameter Name | Default Value | Allowed Range | Unit | Source / Literature |
|---|---|---|---|---|---|
| $N$ | `population_size` | 100 | [10, 10000] | agents | Deffuant et al. (2000) |
| $\epsilon$ | `epsilon` | 0.2 | [0.01, 1.0] | dimensionless | Deffuant et al. (2000) |
| $\mu$ | `mu` | 0.5 | [0.01, 0.5] | dimensionless | Deffuant et al. (2000) |
| $T$ | `max_steps` | 1000 | [10, 50000] | steps | Standard convergence horizon |

### A.2. Output Table
| Metric Name | Aggregation Level | Formula / Definition | Frequency |
|---|---|---|---|
| `mean_opinion` | Global aggregate | $\frac{1}{N} \sum_{i=0}^{N-1} x_i$ | Every step |
| `opinion_variance` | Global aggregate | $\frac{1}{N} \sum_{i=0}^{N-1} (x_i - \bar{x})^2$ | Every step |
| `opinion` | Individual micro | Current opinion value $x_i$ | Every step |
| `cluster_count` | Summary metric | Number of distinct clusters with pairwise distance $> \epsilon$ | Final step |

---

## Canonical Reference

- Canonical guidelines for all 7 elements: [references/odd-raw.md](../../.agents/skills/abm-modeler/references/odd-raw.md).
- Primary open-access source: Grimm et al. (2020), *Journal of Artificial Societies and Social Simulation*, 23(2), 7. <https://www.jasss.org/23/2/7.html>.
