# Stage 4: Verify

Goal: show that the implementation does what the ODD says, consistently and
reproducibly, then run the planned experiments.

> **Always tell the researcher:** passing these checks means the code matches
> its specification (*verification*). It does **not** mean the model is a
> correct description of reality (*validation*). Validation against empirical
> patterns or data is a scientific task the researcher owns.

---

## Mandatory Checks

Implement these in `tests/test_model.py` with `pytest`. Each check is written
from the ODD, not from the code.

| # | Check | How |
|---|---|---|
| V1 | **Runs** | The model initializes and runs N steps with the default configuration without raising |
| V2 | **Seed determinism** | Two runs with the same seed and parameters produce identical `DataCollector` output (compare the DataFrames exactly) |
| V3 | **Seed sensitivity** | For a stochastic model, two different seeds produce different output (confirms the seed is actually used) |
| V4 | **State invariants** | After every step, every state variable stays within its ODD 2 range |
| V5 | **Population** | The agent count stays constant, or changes only through the birth/death rules of ODD 7 |
| V6 | **Parameters wired** | Each parameter in `experiment-config.yaml` reaches the model (changing it changes the stored attribute; where cheap, check it changes behavior) |
| V7 | **Outputs collected** | Every metric in the ODD output table appears in the collected data with the expected number of rows |
| V8 | **Edge cases** | The edge cases listed in the ODD submodels (empty neighborhood, single agent, parameter at the boundary of its range) behave as the ODD specifies |

Add domain checks where the ODD implies them. Examples: mass or wealth
conservation; a known analytical result for a special case (e.g., with
`epsilon = 1`, a bounded-confidence model converges to the mean).

### Running

```bash
pip install -r requirements.txt
pytest tests/ -v
```

**Pass criterion:** every test passes. A failing test is never "fixed" by
loosening the test. Find out whether the code or the ODD is wrong. If the ODD
is wrong, go back to Stage 2 with the researcher.

---

## Documentation-Code Correspondence

Check it manually, item by item, and record the result in the verification
report:

1. Every ODD 7.x submodel has an **Implemented in:** reference, and the
   referenced function exists.
2. Every behavioral method in `agents.py` and `model.py` cites an ODD
   section that exists.
3. The order of calls in `Model.step()` matches ODD 3 exactly.
4. The parameter defaults in the code, `experiment-config.yaml`, and the ODD
   parameter table are identical.
5. No `[DECISION NEEDED]` appears anywhere in the code.
6. Every `[ASSUMPTION]` in the code has a decision-log entry.

Useful searches:

```bash
grep -rn "DECISION NEEDED" .
grep -rn "ASSUMPTION" .
grep -rn "ODD " agents.py model.py
```

---

## Experiments

1. Run the scenarios defined in `experiment-config.yaml` using several seeds
   per configuration (the number of replications is a researcher decision;
   suggest enough to see the variance between runs).
2. Save raw output (CSV or Parquet) with the parameters and seed of every
   run.
3. Produce the plots and tables for the metrics in the ODD output table.
4. Report the results neutrally: what was observed and how much it varied
   across seeds. Leave the interpretation to the researcher.

---

## Verification Report

Write `verification-report.md` containing:

- the date, code version (commit hash if available), and package versions;
- the result of each check V1-V8 plus the domain checks;
- the correspondence check, item by item;
- the open `[ASSUMPTION]` items, as candidates for sensitivity analysis;
- the verification-vs-validation statement above.

---

## Exit Criteria

- All mandatory checks pass.
- The correspondence check shows no mismatches.
- `verification-report.md` exists.
- The researcher has reviewed the report and the experiment results.
