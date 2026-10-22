# ABMforAI: Scientific Agent-Based Modeling with AI Assistants

Guidelines, templates, and agent skills designed to assist researchers in building rigorous, reproducible computational simulations in Python without undocumented theoretical assumptions.

---

## Overview

Agent-Based Modeling is a powerful methodology for studying emergent phenomena in social, ecological, biological, and economic systems. However, domain researchers often face a steep programming barrier when implementing simulations, while generic AI assistants tend to silently invent decision rules, interaction equations, and behavioral parameters without domain grounding.

This project bridges that gap:
- **Theory Ownership:** The researcher owns all theoretical and behavioral decisions. The AI provides software craftsmanship.
- **Zero Undocumented Assumptions:** The AI is strictly prohibited from inventing behavioral rules. Any missing detail pauses execution and is logged for human review.
- **Scientific Protocol:** Every model is grounded in the standardized **ODD (Overview, Design Concepts, Details)** protocol ([Grimm et al., 2020](https://doi.org/10.18564/jasss.4259)).
- **Reproducibility by Design:** Explicit random seed control, parameter sweeps via configuration files, and automated invariance testing.

---

## The 4-Stage Operational Workflow

The methodology follows a gated progression:

```
[1. Elicit] --------> [2. Formalize] ------> [3. Simulate] ------> [4. Verify]
Diagnostic Interview    ODD Protocol &        Modular Python/Mesa     Sanity Checks &
(Domain Discovery)      Decision Log          Implementation          Experiments
```

1. **Elicit (Diagnostic Interview):** The agent interviews the researcher along 12 foundational dimensions (entities, topology, decision rules, temporal scales, output metrics) without writing code.
2. **Formalize (ODD Protocol):** The model specification is formalized into `odd.md` and `decision-log.md`. Any theoretical ambiguity is flagged as `[DECISION NEEDED]`.
3. **Simulate (Modular Python Implementation):** The approved ODD is implemented as modular Python code (Mesa 3.x by default) with explicit inline ODD references for all behavioral methods.
4. **Verify (Integrity & Experimentation):** Automated tests verify seed determinism, state invariants, boundary behaviors, and documentation-code correspondence.

---

## Repository Structure

```text
ABMforAI/
├── README.md               # Project overview and usage guide
├── LICENSE                 # MIT Open Source License
├── .gitignore              # Ignored cache, virtualenvs, and data outputs
├── AGENTS.md               # Universal instructions for AI coding assistants
├── PLAN-IN-STEPS.md        # Phased roadmap of the methodology
├── .agents/
│   ├── rules/              # IDE workspace rules (Always On & On Demand)
│   │   ├── human-review.md
│   │   ├── no-undocumented-assumptions.md
│   │   ├── task-management.md
│   │   ├── reproducibility.md
│   │   └── code-organization.md
│   └── skills/
│       └── abm-modeler/    # Self-contained skill package
│           ├── SKILL.md
│           ├── references/ # Stage runbooks and canonical ODD references
│           └── resources/  # Templates (ODD, spec, config, decision log)
└── examples/
    └── opinion-dynamics/   # Canonical reference model (Fase 3)
```

---

## How to Use

### 1. In this Repository
When working inside this repository, AI coding assistants (such as Antigravity, Cursor, Claude Code, or Copilot) automatically discover the rules in `.agents/rules/` and the skill in `.agents/skills/abm-modeler/`.

To begin designing a model, prompt your agent:
```text
I want to build an agent-based model to study [describe your phenomenon]. 
Guide me through the ABM design process.
```

### 2. Exporting to Another Project
The `abm-modeler` skill is completely self-contained. To use it in an external project:
1. Copy `.agents/skills/abm-modeler/` to your target project's `.agents/skills/` directory.
2. Copy `AGENTS.md` to your target project's root.
3. Start interacting with your AI assistant using the Elicit-Formalize-Simulate-Verify workflow.

---

## Citation & Academic Context

This repository is developed as a software artifact and methodological proposal to support AI-assisted construction of scientific agent-based models.

If you use these guidelines or skills in your research, please cite:
```bibtex
@software{abmforai2026,
  title = {ABMforAI: Rigorous AI-Assisted Agent-Based Modeling},
  author = {FIB and Contributors},
  year = {2026},
  url = {https://github.com/your-username/ABMforAI}
}
```

---

## License

MIT License. Open for scientific and educational use.
