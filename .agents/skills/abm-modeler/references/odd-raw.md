# Canonical ODD Protocol Reference (Grimm et al., 2006, 2010, 2020)

## Primary Sources and Official Links

- **ODD 2020 (Second Update - Open Access):**
  Grimm, V., Railsback, S. F., Vincenot, C. E., Berger, U., Gallagher, C., DeAngelis, D. L., Edmonds, B., Ge, J., Giske, J., Groeneveld, J., Johnston, A. S. A., Milles, A., Nabe-Nielsen, J., Polhill, J. G., Radchuk, V., Rohwäder, M.-S., Stillman, R. A., Thiele, J. C., & Ayllón, D. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism." *Journal of Artificial Societies and Social Simulation*, 23(2), 7.
  - HTML (Full Text): <https://www.jasss.org/23/2/7.html>
  - PDF: <https://www.jasss.org/23/2/7/7.pdf>
  - Permanent DOI: <https://doi.org/10.18564/jasss.4259>

- **ODD 2010 (First Update):**
  Grimm, V., Berger, U., DeAngelis, D. L., Polhill, J. G., Giske, J., & Railsback, S. F. (2010). "The ODD protocol: A review and first update." *Ecological Modelling*, 221(23), 2760-2768.
  - DOI: <https://doi.org/10.1016/j.ecolmodel.2010.08.019>
  - ScienceDirect: <https://www.sciencedirect.com/science/article/pii/S030438001000416X>

- **ODD 2006 (Foundational Paper):**
  Grimm, V., Berger, U., Bastiansen, F., Eliassen, S., Ginot, V., Giske, J., Goss-Custard, J., Grand, T., Heinz, S. K., Huse, G., Huth, A., Jepsen, J. U., Jørgensen, C., Mooij, W. M., Müller, B., Pe'er, G., Piou, C., Railsback, S. F., Robbins, A. M., Robbins, M. M., Rossmanith, E., Rüger, N., Strand, E., Souissi, S., Stillman, R. A., Vabø, R., Visser, U., & DeAngelis, D. L. (2006). "A standard protocol for describing individual-based and agent-based models." *Ecological Modelling*, 198(1-2), 115-126.
  - DOI: <https://doi.org/10.1016/j.ecolmodel.2006.04.023>
  - ScienceDirect: <https://www.sciencedirect.com/science/article/pii/S030438000600185X>

- **ODD+D (Human Decision-Making Extension):**
  Müller, B., Bohn, F., Dreßler, G., Groeneveld, J., Klassert, C., Liang, R., Schlüter, M., Schwarz, N., & Weise, H. (2013). "Describing Human Decisions in Agent-Based Models - ODD + D, an Extension of the ODD Protocol." *Environmental Modelling & Software*, 48, 37-48.
  - DOI: <https://doi.org/10.1016/j.envsoft.2013.06.003>
  - ScienceDirect: <https://www.sciencedirect.com/science/article/pii/S136481521300146X>

---

## Instruction for AI Assistant

This document contains the canonical definitions and guiding questions for each element of the ODD protocol.

If you are uncertain about how to classify a modeling construct, or if the researcher indicates that you structured an ODD section incorrectly:
1. Halt code or document generation.
2. Inform the researcher of the potential discrepancy.
3. With the researcher's permission, consult the corresponding section below to align with canonical ODD standards.

---

## The Seven Elements of ODD

An ODD description consists of seven numbered elements grouped into three conceptual categories: Overview (1-3), Design Concepts (4), and Details (5-7).

```
I. Overview
   1. Purpose and patterns
   2. Entities, state variables, and scales
   3. Process overview and scheduling

II. Design Concepts
   4. Design concepts (4.1 to 4.11)

III. Details
   5. Initialization
   6. Input data
   7. Submodels
```

---

### 1. Purpose and Patterns

- **Guiding Questions:**
  - What is the purpose of the model? What scientific or practical problem does it address?
  - For whom was the model designed?
  - What real-world patterns (empirical dynamics, stylized facts) are used to evaluate whether the model is useful and structurally realistic?
- **Standard Requirement:** Be concise. Do not describe the entire mechanism here; describe what question the model was built to answer and what criteria determine its fitness for purpose.

---

### 2. Entities, State Variables, and Scales

- **Guiding Questions:**
  - What types of entities are in the model?
    - Agents (individual decision-makers).
    - Spatial units (cells, patches, network nodes).
    - Collectives (groups, organizations, herds).
    - Environment (global abiotic or institutional conditions).
  - For each entity type, what state variables characterize it?
    - State variables are attributes that vary among entities of the same type or vary over time.
    - Each variable must specify its name, data type, physical or dimensionless unit, and valid numerical range.
  - What are the temporal and spatial scales?
    - What does one simulation time step (tick) represent in physical time?
    - How many time steps does a simulation run last?
    - What is the spatial resolution (size of a grid cell) and spatial extent (total area / boundary)?

---

### 3. Process Overview and Scheduling

- **Guiding Questions:**
  - Who does what, in what order, and when are state variables updated?
  - What are the distinct processes occurring during one time step?
  - How is time stepped (discrete time steps, event-driven)?
  - How are agents activated?
    - Random sequential (shuffled every step).
    - Fixed order.
    - Asynchronous vs. Synchronous (two-phase: compute updates based on pre-step states, then apply all updates simultaneously).
- **Standard Requirement:** Provide an overview only. The detailed mathematical equations or decision algorithms for each process belong in **7. Submodels**.

---

### 4. Design Concepts

The protocol evaluates 11 foundational concepts. If a concept does not apply, write "Not applicable" with a brief justification.

- **4.1. Basic Principles:** Which general theories, hypotheses, or empirical paradigms (e.g., Deffuant bounded confidence, Schelling segregation, optimal foraging) underlie the model's design?
- **4.2. Emergence:** What system-level phenomena emerge from individual agent interactions without being explicitly programmed at the macro level?
- **4.3. Adaptation:** What rules or heuristics do agents use to adapt their behavior in response to changes in their internal state or environment?
- **4.4. Objectives:** Do agents have explicit fitness measures, utility functions, or objective criteria they seek to maximize?
- **4.5. Learning:** Do agents change the adaptive traits or rules themselves over time based on accumulated experience?
- **4.6. Prediction:** Do agents anticipate future conditions or state transitions to make current decisions? What internal model of the world do they use?
- **4.7. Sensing:** What internal and environmental state variables can agents perceive? What are the sensory limits, range, or error?
- **4.8. Interaction:** How do agents interact? Are interactions direct (one-to-one, local neighborhood, network edges) or indirect (mediated by environment/stigmergy)?
- **4.9. Stochasticity:** Which processes explicitly incorporate pseudorandom numbers, and for what purpose (initial attribute distributions, tie-breaking, behavioural noise)?
- **4.10. Collectives:** Do agents form distinct social structures, teams, or groups that act as higher-level entities with their own state variables?
- **4.11. Observation:** What metrics, summary statistics, or individual trajectories are recorded from the simulation to address the purpose defined in Section 1?

---

### 5. Initialization

- **Guiding Questions:**
  - What is the exact state of the model world at time $t = 0$?
  - How many entities of each type are created?
  - How are their initial state variables assigned (homogeneous constants, random draws from specified distributions, or loaded from empirical data)?
  - Is initialization deterministic (identical across runs) or stochastic (varying between runs)?

---

### 6. Input Data

- **Guiding Questions:**
  - Does the model depend on external data driving environmental or exogenous dynamics over time (e.g., historical weather time series, economic shocks, spatial GIS layers)?
  - If no external data are consumed during the run, state explicitly: "The model is self-contained and does not use external input data."

---

### 7. Submodels

- **Guiding Questions:**
  - For each process listed in **Section 3**, provide an exhaustive, unambiguous algorithmic and mathematical description.
  - Could an independent researcher reimplement the submodel identically from this text without viewing the source code?
  - Every equation must define its symbols, units, default parameter values, and valid ranges.
  - What are the edge-case handling rules (e.g., zero denominators, empty neighbor sets, ties, boundary hits)?
  - Cross-reference the exact function and file where the submodel is implemented (e.g., `Implemented in: agents.py -> revise_opinion()`).
