# Decision Log: Deffuant Opinion Dynamics

This document logs all theoretical decisions and assumptions accepted for the canonical opinion dynamics reference implementation.

---

## Log Table

| # | Date | Stage | Topic | Decision | Alternatives Considered | Rationale / Literature | Decided by | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-22 | Elicit | Model Paradigm | Deffuant-Weisbuch continuous bounded confidence | Hegselmann-Krause group averaging, discrete voter model | Canonical baseline for continuous opinion clustering (Deffuant et al., 2000) | researcher | confirmed |
| 2 | 2026-10-22 | Elicit | Topology | Non-spatial well-mixed global pool | 2D lattice grid, Barabási-Albert scale-free network | Classic mean-field formulation focused on opinion convergence mechanics | researcher | confirmed |
| 3 | 2026-10-22 | Formalize | Scheduling & Step Unit | 1 tick = 1 Monte Carlo sweep ($N$ sequential bilateral interaction attempts) | Single pair draw per tick (Gillespie), strict disjoint matching | Standard in computational physics and Mesa 3.x idiom; fast convergence | researcher | confirmed |
| 4 | 2026-10-22 | Formalize | Default Parameters | $N=100$, $\epsilon=0.2$, $\mu=0.5$ | $N=1000$, heterogeneous $\epsilon$ distribution | Standard parameters from Deffuant et al. (2000) displaying clean bipolarization | researcher | confirmed |
| 5 | 2026-10-22 | Simulate | Visualization | Static Matplotlib trajectory plots and histograms | Interactive Solara dashboard, CSV export only | Lightweight, reproducible, no heavy frontend dependencies | researcher | confirmed |
