# Conceptual Model Specification: [Model Title]

This document records the output of the **Elicit** diagnostic interview (Stage 1). It serves as the bridge between the researcher's informal domain description and the formal scientific ODD protocol.

<!--
INSTRUCTION FOR AI ASSISTANT:
Fill this document progressively during the Stage 1 Socratic interview.
Do not skip dimensions. If the researcher cannot answer a question yet, tag it [DECISION NEEDED] and do not assume a default.
If the researcher accepts a provisional standard value, tag it [ASSUMPTION] and create a decision-log.md entry.
-->

---

## 1. Interview Diagnostic Record

### Dimension A: Purpose and Research Question
- **Real-world phenomenon:** [What pattern, system, or behavior are we studying?]
- **Core research question:** [What specific question should the simulation answer?]
- **Intended use:** [Theory building / Policy scenario testing / Empirical hypothesis exploration]
- **Stylized facts to reproduce:** [What observed empirical patterns must the model exhibit to be valid?]

### Dimension B: Entities and Actors
- **Active agents:** [Who makes decisions? E.g., consumers, firms, cells, animals, voters]
- **Agent types:** [Is there a single class of agents, or multiple distinct types?]
- **Non-agent entities:** [Are there passive entities like resource patches, obstacles, institutions, or market boards?]
- **Heterogeneity:** [Are agents identical at birth, or do they differ in traits, thresholds, or endowments?]

### Dimension C: State Variables
- **Individual agent traits:**
  - Dynamic attributes (change over time): [e.g., opinion, wealth, energy, position]
  - Static attributes (fixed): [e.g., identity, tolerance threshold, maximum speed]
- **Environment state:** [Does the global world have its own state variables, like temperature or season?]

### Dimension D: Space and Topology
- **Does space matter?** [Yes / No]
- **Spatial structure:** [Well-mixed soup / 2D discrete grid (Moore or Von Neumann) / Continuous 2D / Complex network]
- **Boundary conditions:** [Toroidal (wrap around) / Bounded walls / Absorbing]
- **Interaction radius:** [Who can reach whom? Immediate neighbors / Network neighbors / Global pool]

### Dimension E: Time and Scales
- **Time step meaning (dt):** [What does 1 tick represent in real time? E.g., 1 minute, 1 day, 1 interaction]
- **Simulation horizon:** [Fixed number of steps (e.g., 500 steps) or termination condition (e.g., convergence reached)]
- **Spatial resolution:** [Physical size of one cell or total domain, if applicable]

### Dimension F: Decision Making and Behaviors
- **Step action cycle:** [What actions does an agent take in a single time step?]
- **Perception / Sensing:** [What information does the agent see before acting?]
- **Decision mechanism:** [Deterministic threshold / Heuristic imitation / Utility maximization / Stochastic transition / Learning]
- **Memory and adaptation:** [Do agents remember past interactions, or are they memoryless?]

### Dimension G: Interactions
- **Interaction mode:** [Direct 1-on-1 bilateral exchange / Group voting / Broadcast / Indirect via environment (stigmergy)]
- **Interaction outcome:** [What state variables change for each party when an interaction occurs?]

### Dimension H: Scheduling and Process Order
- **Activation order:** [Random shuffle each step / Fixed order / Priority queue]
- **Update mode:** [Sequential (immediate effect) / Synchronous (two-phase: evaluate all, then update all)]
- **Within-step sub-phases:** [e.g., Phase 1: Move; Phase 2: Interact; Phase 3: Update state]

### Dimension I: Stochasticity
- **Where is randomness used?** [Initial attribute assignment / Partner selection / Behavioral noise / Success probabilities]
- **Distributions:** [Uniform / Normal / Power-law / Empirical distribution]

### Dimension J: Initialization
- **Initial population size:** [e.g., N = 100]
- **Initial spatial placement:** [Random uniform / Clustered / Fixed lattice]
- **Initial states:** [Homogeneous / Random uniform in range / Loaded from dataset]

### Dimension K: Population Dynamics
- **Agent entry and exit:** [Constant population / Birth and death / Influx and migration]
- **Capacity limits:** [Maximum carrying capacity of space or model]

### Dimension L: Observables and Metrics
- **Micro-level metrics:** [Individual trajectories tracked across time]
- **Macro-level metrics:** [Mean, variance, polarization index, clustering coefficient, time to consensus]
- **Reporting frequency:** [Every step / End of simulation run only]
- **Key experimental scenarios:** [What parameter variations or interventions will be tested?]

---

## 2. Mapping to ODD Protocol

This table maps the answers collected in this specification directly into the formal sections of `odd.md`:

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

- **Specification Status:** [Draft / Under Review / Approved for Stage 2 Formalization]
- **Date of Review:** [YYYY-MM-DD]
- **Open Gaps:** [List any unresolved [DECISION NEEDED] tags]
- **Confirmed by Researcher:** [Yes / No]
