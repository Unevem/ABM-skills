# ODD Protocol Specification: [Model Name]

Based on the canonical ODD Protocol (Grimm et al., 2020).

<!-- INSTRUCTION FOR AI ASSISTANT:
1. Every element 1 through 7 must be explicitly addressed.
2. If theoretical details are unknown, mark them as [DECISION NEEDED] and halt dependent implementation.
3. Every provisional value accepted by the researcher must be tagged as [ASSUMPTION] and reference an entry in decision-log.md.
4. If you are in doubt regarding canonical ODD conventions, or if the researcher indicates that an element was structured incorrectly:
   - First notify the researcher of the potential discrepancy.
   - Upon confirmation, consult the canonical reference in `references/odd-raw.md` or the open-access publication at <https://www.jasss.org/23/2/7.html>.
-->

---

## 1. Purpose and Patterns

<!--
What is the purpose of the model? What specific scientific question does it address?
Who is the intended audience?
What real-world patterns (stylized facts) will be used to assess whether the model is useful and structurally realistic?
-->
[Describe the purpose, research question, target audience, and reference patterns.]

---

## 2. Entities, State Variables, and Scales

<!--
What entities (agents, spatial units/cells, environment, institutions) exist?
For each entity, list every state variable with: Name, Type, Unit, Range, and whether it is Static or Dynamic.
What does one simulation time step represent in the real world?
What is the total duration of a simulation run?
What is the spatial extent and resolution (if applicable)?
-->

### Entity Types and Attributes
| Entity Type | State Variable | Type | Unit | Range | Static/Dynamic | Description |
|---|---|---|---|---|---|---|
| Agent | `id` | int | - | [0, N-1] | Static | Unique agent identifier |
| Agent | [variable] | [float/int/etc] | [unit] | [min, max] | [Dynamic/Static] | [Description] |
| Environment | [variable] | [type] | [unit] | [range] | [Dynamic/Static] | [Description] |

### Temporal and Spatial Scales
- **Time Step (dt):** 1 step = [unit of physical time, or abstract interaction round]
- **Run Length:** [number of steps, or convergence termination condition]
- **Spatial Extent & Topology:** [dimensions, e.g., 50x50 discrete grid, continuous space [0, 1]^2, network, or non-spatial / well-mixed]

---

## 3. Process Overview and Scheduling

<!--
What processes happen in what order during one time step?
Who executes each process?
Are updates synchronous (two-phase: compute then apply) or sequential (immediate update)?
In what order are agents activated (random shuffle, fixed order, priority)?
-->
1. **[Process 1 Name]:** Executed by [Agents/Model]. [Synchronous / Sequential]. Activation order: [Random shuffle / Fixed]. Detailed in Section 7.1.
2. **[Process 2 Name]:** Executed by [Agents/Model]. Detailed in Section 7.2.
3. **Observation & Data Collection:** Executed by Model DataCollector at the end of each step.

---

## 4. Design Concepts

<!--
Address all 11 design concepts. If a concept is not applicable, state "Not applicable" followed by a one-line explanation of why.
-->

### 4.1. Basic Principles
<!-- Which underlying theoretical paradigms, hypotheses, or foundational models (e.g., Deffuant bounded confidence, Schelling segregation, evolutionary game theory) are used? -->
[Describe foundational theories and empirical background.]

### 4.2. Emergence
<!-- What macro-level system results emerge from agent-level interactions rather than being hardcoded? -->
[Describe expected emergent macro-behaviors, such as consensus, clustering, polarization, price stability, or spatial patterns.]

### 4.3. Adaptation
<!-- Do agents change their rules or decisions based on changes in their state or the environment? If so, how? -->
[Describe adaptive heuristics, response thresholds, or state transitions.]

### 4.4. Objectives
<!-- Do agents pursue explicit goals (e.g., utility maximization, survival, payoff)? How do they measure success? -->
[Describe agent objectives or utility functions, or state "Not applicable" if purely reactive.]

### 4.5. Learning
<!-- Do agents change the way they adapt based on past experience (e.g., reinforcement learning, Bayesian update)? -->
[Describe learning mechanisms, or state "Not applicable".]

### 4.6. Prediction
<!-- Do agents forecast future conditions to make decisions? What model of the world do they use? -->
[Describe prediction mechanisms, or state "Not applicable".]

### 4.7. Sensing
<!-- What internal and external variables do agents perceive? Is sensing local, global, or erroneous? -->
[Describe what information agents perceive and any sensory limits or noise.]

### 4.8. Interaction
<!-- How do agents interact with each other (direct 1-on-1, broadcast, spatial neighbors, network edges, or indirect via environmental signals)? -->
[Describe interaction topologies and protocols.]

### 4.9. Stochasticity
<!-- Which processes use pseudorandomness and for what purpose (initialization, tie-breaking, asynchronous interaction, noise)? -->
[List all random processes and their probability distributions.]

### 4.10. Collectives
<!-- Do agents form distinct groups, organizations, or coalitions that have their own state or actions? -->
[Describe emergent or predefined groups, or state "Not applicable".]

### 4.11. Observation
<!-- What metrics are collected from the simulation to address the research question? -->
[List macro and micro metrics, collection frequencies, and summary statistics.]

---

## 5. Initialization

<!--
What is the exact state of the model at step 0?
How many agents exist?
Are initial state variables homogeneous, drawn from random distributions, or loaded from empirical data?
Does initialization vary between runs (stochastic) or is it identical?
-->
[Specify step 0 conditions, population sizes, attribute assignments, and spatial placement.]

---

## 6. Input Data

<!--
Does the model use external data files, empirical time series, or GIS rasters during simulation runs?
-->
[Specify input files and formats, or state "None (model is self-contained)".]

---

## 7. Submodels

<!--
Provide an exhaustive mathematical and algorithmic description of each process listed in Section 3.
Include exact equations, parameter symbols, default values, ranges, tie-breaking rules, and edge-case behaviors.
-->

### 7.1. [Process 1 Name]
- **Purpose:** [Brief purpose]
- **Executed by:** [Agent type / Model]
- **Algorithm / Equation:**
  ```text
  [Provide exact mathematical formulas or unambiguous pseudocode]
  ```
- **Parameters Used:**
  - `param_name`: [Symbol], Default = [Value], Range = [min, max], Unit = [unit]
- **Edge Cases & Tie Breaking:**
  - What happens if neighborhood is empty? [Rule]
  - What happens on exact numerical ties? [Rule]
  - What happens if variable exceeds boundaries? [Boundary rule: clip / wrap / error]
- **Implemented in:** `agents.py -> [FunctionName]` <!-- Filled during Stage 3 -->

### 7.2. [Process 2 Name]
- **Purpose:** [Brief purpose]
- **Executed by:** [Agent type / Model]
- **Algorithm / Equation:**
  ```text
  [Formulas / pseudocode]
  ```
- **Parameters Used:**
  - [List parameters]
- **Edge Cases & Tie Breaking:** [Specify rules]
- **Implemented in:** `model.py -> [FunctionName]` <!-- Filled during Stage 3 -->

---

## Annex: Parameter and Output Tables

### A.1. Parameter Table
| Symbol | Parameter Name | Default Value | Allowed Range | Unit | Source / Literature |
|---|---|---|---|---|---|
| `N` | `population_size` | 100 | [10, 10000] | agents | Researcher |
| `eps` | `tolerance` | 0.2 | [0.01, 1.0] | dimensionless | [ASSUMPTION] (decision-log #1) |

### A.2. Output Table
| Metric Name | Aggregation Level | Formula / Method | Frequency |
|---|---|---|---|
| `mean_opinion` | Global aggregate | Average opinion across active agents | Every step |
| `cluster_count` | Global aggregate | Number of opinion clusters (distance > eps) | Final step |

---

## Canonical Reference

- Canonical guidelines for all 7 elements: [references/odd-raw.md](../references/odd-raw.md).
- Primary publication (Open Access): Grimm et al. (2020), *Journal of Artificial Societies and Social Simulation*, 23(2), 7.
  - Full Text (HTML): <https://www.jasss.org/23/2/7.html>
  - Full Article (PDF): <https://www.jasss.org/23/2/7/7.pdf>
  - Permanent DOI: <https://doi.org/10.18564/jasss.4259>
