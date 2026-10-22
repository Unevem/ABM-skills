# Conceptual Model Specification: Deffuant Opinion Dynamics

This document records the output of the Stage 1 Elicit diagnostic interview for the canonical opinion dynamics simulation.

---

## 1. Interview Diagnostic Record

### Dimension A: Purpose and Research Question
- **Real-world phenomenon:** The emergence of social consensus, polarization, and echo-chamber fragmentation in continuous opinion spaces through peer-to-peer communication.
- **Core research question:** Under what confidence bound threshold $\epsilon$ does an initially uniform distribution of opinions transition from pluralistic fragmentation to bipolarization or global consensus?
- **Intended use:** Theoretical model building and replication of classical bounded confidence dynamics.
- **Stylized facts to reproduce:**
  - Plurality of clusters for small $\epsilon$ ($\epsilon \le 0.1$).
  - Bipolarized stable clusters for intermediate $\epsilon$ ($\approx 0.2$).
  - Complete central consensus for wide tolerance ($\epsilon \ge 0.3$).

### Dimension B: Entities and Actors
- **Active agents:** Individuals holding a continuous subjective opinion.
- **Agent types:** Single homogeneous agent class (`OpinionAgent`).
- **Non-agent entities:** None (pure social agent interaction).
- **Heterogeneity:** Homogeneous in behavioral rules ($\epsilon, \mu$), heterogeneous in initial opinions drawn uniformly from $[0, 1]$.

### Dimension C: State Variables
- **Individual agent traits:**
  - `opinion` (float, range: $[0.0, 1.0]$, dynamic): The continuous belief/attitude.
  - `id` (int, range: $[0, N-1]$, static): Unique identifier.
- **Environment state:** None.

### Dimension D: Space and Topology
- **Does space matter?** No.
- **Spatial structure:** Non-spatial, well-mixed global interaction pool.
- **Boundary conditions:** Not applicable (opinion boundaries bounded on $[0, 1]$).
- **Interaction radius:** Global pool; any agent can potentially interact with any other agent.

### Dimension E: Time and Scales
- **Time step meaning (dt):** 1 tick = 1 Monte Carlo sweep ($N$ random bilateral interaction attempts).
- **Simulation horizon:** Fixed duration of $T = 1000$ steps or stabilization where no further shifts occur.
- **Spatial resolution:** Not applicable.

### Dimension F: Decision Making and Behaviors
- **Step action cycle:** In each step, the agent chooses a random peer $j \ne i$. If $|x_i - x_j| < \epsilon$, both shift opinions toward each other by $\mu \cdot \Delta x$.
- **Perception / Sensing:** Perfect observation of the chosen partner's opinion $x_j$.
- **Decision mechanism:** Bounded confidence threshold rule (Deffuant et al., 2000).
- **Memory and adaptation:** Memoryless; actions depend solely on current states.

### Dimension G: Interactions
- **Interaction mode:** Bilateral, pairwise 1-on-1 direct exchange.
- **Interaction outcome:** Symmetric compromise between compatible peers:
  $$x_i \leftarrow x_i + \mu (x_j - x_i)$$
  $$x_j \leftarrow x_j + \mu (x_i - x_j)$$

### Dimension H: Scheduling and Process Order
- **Activation order:** Random sequential activation. All agents are randomly shuffled each step via `self.agents.shuffle_do("step")`.
- **Update mode:** Sequential (immediate state change upon bilateral interaction).
- **Within-step sub-phases:** Single interaction phase per agent per step.

### Dimension I: Stochasticity
- **Where is randomness used?**
  1. Initialization: Initial opinions $x_i \sim \text{Uniform}(0, 1)$.
  2. Interaction: Random selection of interaction partner $j \ne i$.
  3. Activation order: Shuffled execution order in each tick.
- **Distributions:** Uniform pseudorandom distribution seeded explicitly.

### Dimension J: Initialization
- **Initial population size:** $N = 100$ agents (default baseline).
- **Initial spatial placement:** Not applicable.
- **Initial states:** Each agent's opinion is drawn independently from $\text{Uniform}(0.0, 1.0)$.

### Dimension K: Population Dynamics
- **Agent entry and exit:** Strictly constant population ($N$ is conserved; no birth, death, or migration).
- **Capacity limits:** Fixed population.

### Dimension L: Observables and Metrics
- **Micro-level metrics:** Individual opinion trajectory $x_i(t)$.
- **Macro-level metrics:**
  - Mean opinion $\bar{x}(t)$.
  - Opinion variance $\sigma^2(t)$.
  - Final cluster count (number of groups where pairwise distances within cluster $< \epsilon$).
- **Reporting frequency:** Every step $t$.

---

## 2. Mapping to ODD Protocol

| Interview Dimension | Target Element in `odd.md` | Primary Responsibility |
|---|---|---|
| **A: Purpose & Question** | Element 1 (Purpose and Patterns) | Researcher |
| **B: Entities** | Element 2 (Entities, State Variables, Scales) | Researcher |
| **C: State Variables** | Element 2 (Entity Attributes Table) | Researcher & Agent |
| **D: Space & Topology** | Element 2 (Spatial Scales) & Element 4.8 (Interaction) | Researcher |
| **E: Time & Scales** | Element 2 (Temporal Scales) | Researcher |
| **F: Behaviors & Decisions** | Element 4 (Design Concepts) & Element 7 (Submodels) | Researcher |
| **G: Interactions** | Element 4.8 (Interaction) & Element 7 (Submodels) | Researcher |
| **H: Scheduling** | Element 3 (Process Overview and Scheduling) | Researcher |
| **I: Stochasticity** | Element 4.9 (Stochasticity) | Researcher |
| **J: Initialization** | Element 5 (Initialization) | Researcher |
| **K: Population Dynamics** | Element 2, 5 & Element 7 (Submodels) | Researcher |
| **L: Observables & Metrics** | Element 4.11 (Observation) & Annex A.2 (Output Table) | Researcher |

---

## 3. Researcher Confirmation Sign-Off

- **Specification Status:** Approved for Stage 2 Formalization
- **Date of Review:** 2026-10-22
- **Open Gaps:** None.
- **Confirmed by Researcher:** Yes
