# Decision Log: Deffuant Opinion Dynamics

This document logs all theoretical decisions, methodological agreements, and technical choices for the canonical opinion dynamics reference implementation.

<!--
RULES FOR THE DECISION LOG:
1. Append-only: Decisions must reflect actual agreements reached with the researcher.
2. If the researcher chose a recommended option during the interview, the rationale must explicitly state "Researcher accepted agent recommendation" alongside the scientific justification.
3. Every theoretical decision must be marked Decided by = "researcher".
4. Technical decisions (e.g., library choices, file layout) must be marked Decided by = "agent (technical)".
-->

---

## Log Table

| # | Date | Stage | Topic | Decision | Alternatives Considered | Rationale / Literature | Decided by | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-22 | Elicit | Model Paradigm | Deffuant-Weisbuch continuous bounded confidence | Hegselmann-Krause group averaging, discrete voter model | Researcher accepted agent recommendation: canonical baseline for continuous opinion dynamics (Deffuant et al., 2000) | researcher | confirmed |
| 2 | 2026-10-22 | Elicit | Topology | Non-spatial well-mixed global pool | 2D lattice grid, Watts-Strogatz small-world network | Researcher accepted agent recommendation: matches original Deffuant et al. (2000) mean-field formulation | researcher | confirmed |
| 3 | 2026-10-22 | Formalize | Scheduling & Step Unit | 1 tick = 1 Monte Carlo sweep (N sequential bilateral interactions via shuffle_do) | Single pair draw per tick (Gillespie), strict disjoint matching | Researcher accepted agent recommendation: standard in ABM simulation and Mesa 3.x idiom; maintains natural time scale | researcher | confirmed |
| 4 | 2026-10-22 | Formalize | Output & Visualization | Static Matplotlib trajectory plots, histogram, and CSV export | Interactive Solara dashboard, CSV export only | Researcher accepted agent recommendation: lightweight, reproducible, no heavy web dependencies | researcher | confirmed |
| 5 | 2026-10-22 | Formalize | Baseline Parameters | N = 1000, mu = 0.5, epsilon = 0.2, T = 500 sweeps | N = 100 (fast toy model), heterogeneous parameter distribution | Researcher accepted agent recommendation: matches original simulation scale of Deffuant et al. (2000) | researcher | confirmed |
| 6 | 2026-10-22 | Formalize | Invariant Preservation | Natural mathematical preservation via convex combination | Explicit min/max clipping in code | Researcher accepted agent recommendation: with mu in (0, 0.5], updates are convex combinations and never escape [0, 1]. Verified by test V4 | researcher | confirmed |
| 7 | 2026-10-22 | Formalize | Cluster Definition | 1D single-linkage gap clustering (consecutive sorted distance >= epsilon) | Radius from cluster centroid (k-means) | Researcher accepted agent recommendation: standard analytical and computational definition used in bounded confidence literature | researcher | confirmed |
| 8 | 2026-10-22 | Formalize | Termination & Scenarios | Fixed T = 500 sweeps; pure epsilon variation (0.5, 0.2, 0.1) with mu = 0.5 fixed | Dynamic stopping on zero-delta; varying mu and epsilon simultaneously | Researcher accepted agent recommendation: isolates the causal effect of epsilon and guarantees homogeneous time-series lengths | researcher | confirmed |
| 9 | 2026-10-22 | Simulate | Libraries & Config | Use PyYAML for experiment-config.yaml and pinned Mesa 3 | Hardcoded Python dictionaries | Agent technical choice: externalizes parameters cleanly per reproducibility guidelines | agent (technical) | confirmed |
| 10 | 2026-10-22 | Simulate | Dependencies: NetworkX | Include networkx>=3.0 in requirements.txt | Minimal Mesa install without networkx | Agent technical choice: Mesa 3.5.x imports mesa.discrete_space.network at package initialization, requiring networkx at runtime | agent (technical) | confirmed |
| 11 | 2026-10-22 | Simulate | Mesa 3.5 RNG Initialization | Use super().__init__(rng=seed) in OpinionModel.__init__ | Legacy super().__init__(seed=seed) | Agent technical choice: Mesa 3.5 deprecates seed= in favor of rng=; passing rng=seed avoids FutureWarning while properly initializing self.rng and self.random | agent (technical) | confirmed |
| 12 | 2026-10-22 | Verify | Empirical Revision: Bipolarization Dynamics | Update scenario description to 'two dominant polarized clusters and occasional minor fringe groups' with explicit revision notes | Artificially filter out clusters < 1% N; maintain strict 2-cluster claim despite empirical evidence | Researcher decision: multi-seed runs showed seed 123 yields 2 clusters [478, 522] while seeds 42 and 999 yield 3 clusters ([414, 5, 581] and [494, 3, 503]). Transparent empirical revision tracking prevents narrative confirmation bias per Deffuant et al. (2000) | researcher | confirmed |
