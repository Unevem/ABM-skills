---
name: abm-modeler
description: >-
  Use this skill when a user wants to design, document, implement, verify, or
  extend an agent-based model (ABM) or agent-based simulation, especially in
  Python/Mesa, or when they describe a phenomenon (social, biological,
  ecological, economic) they want to simulate with interacting agents. Also use
  it to write or review an ODD protocol, or to audit an existing ABM for
  undocumented assumptions and reproducibility. Guides the agent through a
  gated Elicit -> Formalize -> Simulate -> Verify workflow in which the
  researcher owns every theoretical decision.
---

# ABM Modeler

This skill turns a researcher's informal description of a phenomenon into an
agent-based model that is specified (ODD protocol), implemented (Python, Mesa
3.x by default), and verified (reproducibility and invariant tests). Every
theoretical decision stays with the researcher.

The intended user knows the phenomenon well but may have little programming
experience. The agent provides the software craftsmanship. The researcher
provides the theory. The agent must never quietly fill theoretical gaps with
its own choices.

This skill is self-contained. Everything it needs is inside this folder, so
copying `abm-modeler/` into another project is enough to use it.

---

## Non-Negotiable Guardrails

Read [references/guardrails.md](references/guardrails.md) before starting any
stage. It defines the rules summarized here, along with the tag vocabulary and
the `TASKS.md` contract. If the host repository also has `.agents/rules/`, those
rules apply too; where they conflict, the stricter rule wins.

1. **No invented theory.** Never create decision rules, utility functions,
   interaction formulas, parameter values, topologies, schedules, or boundary
   conditions that the researcher has not stated or approved.
2. **Halt on gaps.** When a theoretical detail is missing, stop all work that
   depends on it. Tag the gap `[DECISION NEEDED]` in the documentation, add it
   to `TASKS.md` under `## Decisions Needed`, and ask the researcher a
   structured multiple-choice question. Independent work may continue.
3. **Trace everything.** Every agent behavior, state variable, schedule step,
   and parameter in code must cite the ODD section that defines it.
4. **Researcher sign-off.** No stage is complete until the researcher has
   explicitly reviewed and approved its output.
5. **Reproducibility.** Every source of randomness flows from a single explicit
   seed. Every parameter can be configured. No magic numbers.

---

## Workflow

```
1. ELICIT --> 2. FORMALIZE --> 3. SIMULATE --> 4. VERIFY
(interview)   (ODD + log)      (Python/Mesa)   (tests + runs)
     ^              |                |              |
     +--------------+----------------+--------------+
         any new gap sends the work back to the stage that owns it
```

The stages are **gated**. Do not start a stage until the exit criteria of the
previous one are met and the researcher has confirmed it. If a later stage
uncovers a gap (for example, while coding you notice the tie-breaking rule was
never specified), go back to the stage that owns that decision. Do not patch
the gap locally.

Work on one stage at a time. Load only the reference file for the current
stage.

### Stage 1: Elicit (diagnostic interview)

**Reference:** [references/stage-1-elicit.md](references/stage-1-elicit.md)

- **Goal:** understand the phenomenon, the research question, and the
  minimum set of entities, behaviors, and outputs needed to answer it.
- **Method:** a Socratic interview, one question at a time. Each question
  includes a recommended option and a plain-language explanation of what each
  option implies theoretically.
- **Output:** a filled `model-specification.md` (the conceptual bridge
  between natural language and ODD).
- **Exit criteria:** every interview dimension in the reference is answered
  or explicitly tagged `[DECISION NEEDED]`, and the researcher confirms that
  the specification matches their idea.
- **Forbidden:** writing any Python code.

### Stage 2: Formalize (ODD protocol and decision log)

**Reference:** [references/stage-2-formalize.md](references/stage-2-formalize.md)

- **Goal:** translate the specification into a complete ODD protocol
  (Grimm et al. 2020), in which every element is defined precisely enough
  to implement without guessing.
- **Output:** `odd.md`, `decision-log.md`, and an initial `TASKS.md` with the
  implementation broken into atomic tasks.
- **Exit criteria:** no `[DECISION NEEDED]` tags remain in any section that
  Stage 3 will implement. Every `[ASSUMPTION]` is listed in the decision log.
  The researcher approves the ODD.
- **Forbidden:** writing model code. Choosing values or rules on the
  researcher's behalf.

### Stage 3: Simulate (modular implementation)

**Reference:** [references/stage-3-simulate.md](references/stage-3-simulate.md)

- **Goal:** implement the approved ODD as clean, modular Python, one atomic
  task from `TASKS.md` at a time.
- **Output:** `agents.py`, `model.py`, `experiments.py`, `metrics.py`,
  `experiment-config.yaml`, `requirements.txt`, and tests.
- **Exit criteria:** every ODD submodel has a matching, ODD-annotated
  implementation. The model runs end to end with the default configuration.
  The researcher has reviewed the behavioral code.
- **Forbidden:** implementing anything not in the ODD. "Improving" the model
  beyond its specification.

### Stage 4: Verify (integrity and experimentation)

**Reference:** [references/stage-4-verify.md](references/stage-4-verify.md)

- **Goal:** show that the implementation is internally consistent and
  matches its documentation, then run the planned experiments.
- **Output:** a passing test suite, a verification report, and experiment
  outputs.
- **Exit criteria:** all mandatory checks pass, and the documentation-code
  correspondence check finds no mismatches. The researcher has reviewed the
  results.
- **Limitation (always state it to the researcher):** verification shows
  that the code does what the ODD says. It does **not** show that the model
  represents reality. Validation against empirical data is a separate
  scientific task owned by the researcher.

---

## Entry Points

Not every request starts at Stage 1. Identify the situation first:

| Situation | Start at |
|---|---|
| New idea, no documents | Stage 1 |
| Researcher already has a written description or paper | Stage 1, using the text as a pre-filled draft; ask only about the gaps |
| An ODD exists but there is no code | Stage 2 (audit the ODD for gaps), then Stage 3 |
| Code exists but there is no ODD | Stage 2, reverse-documenting the code; every behavior found in the code becomes `[ASSUMPTION]` until the researcher confirms it |
| Model exists and the researcher wants a change | The stage that owns the change (usually Stage 2), then cascade |
| Researcher wants only an audit | Stage 4 checks, plus the documentation-code correspondence check |

---

## Session Start Checklist

At the start of every session on an ABM project:

1. Read `TASKS.md`, `odd.md` (or `model-specification.md`), and
   `decision-log.md` if they exist.
2. Determine the current stage from `TASKS.md` and the exit criteria above.
3. Report to the researcher, in their language: the current stage, the open
   `[DECISION NEEDED]` items, and the next atomic task.
4. Load the reference file for the current stage.

## Communication

- Write all artifacts (ODD, decision log, code, comments) in English.
- Talk to the researcher in their preferred language. Explain ABM and
  programming terms in plain words the first time they come up.
- When asking a question, always: state what must be decided, give 2-4
  options, explain the theoretical consequence of each, mark one as
  recommended (citing the literature when possible), and wait for an explicit
  answer.
