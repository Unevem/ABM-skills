# Decision Log: Modeling Consensus and Assumptions

This log tracks all theoretical agreements, provisional assumptions, and major technical design decisions throughout the modeling lifecycle.

<!--
RULES FOR UPDATING THE DECISION LOG:
1. Append-only: Never delete or overwrite previous entries. If a decision changes, add a new row referencing the previous ID (e.g., "Supercedes #2").
2. Theoretical decisions (behavior, equations, parameters, topology) must have Decided by = "researcher".
3. Technical decisions (file layout, optimization, variable naming) may have Decided by = "agent (technical)".
4. Any provisional choice accepted without complete literature/empirical grounding must be labeled Status = "assumption", and tagged in code/docs as [ASSUMPTION] (decision-log #ID).
-->

---

## Log Table

| # | Date | Stage | Topic | Decision | Alternatives Considered | Rationale / Literature | Decided by | Status |
|---|---|---|---|---|---|---|---|---|
<!-- Example row:
| 1 | 2026-10-21 | Formalize | Update Rule | Deffuant bounded confidence | Hegselmann-Krause, voter model | Standard baseline (Deffuant et al., 2000) | researcher | confirmed |
-->

---

## Field Descriptions

- **`#`**: Sequential unique identifier, cited in code comments as `[ASSUMPTION] ... (decision-log #N)`.
- **`Date`**: ISO date of the agreement (`YYYY-MM-DD`).
- **`Stage`**: Lifecycle stage (`Elicit`, `Formalize`, `Simulate`, `Verify`).
- **`Topic`**: Short descriptive topic (e.g., `Scheduling`, `Boundary Condition`, `Tolerance Value`).
- **`Decision`**: The specific choice made.
- **`Alternatives Considered`**: Other options that were presented or discussed.
- **`Rationale / Literature`**: Why this choice was selected (theoretical justification, paper citation, or hypothesis).
- **`Decided by`**: `researcher` for scientific/theoretical choices, or `agent (technical)` for implementation plumbing.
- **`Status`**: `confirmed` (grounded in theory/literature) or `assumption` (provisional choice awaiting sensitivity testing).
