# Stage 1: Elicit

Goal: understand the researcher's idea well enough to write a
`model-specification.md` that contains no hidden guesses.

**No code is written in this stage.**

---

## Interview Method

1. **Start broad.** Ask the researcher to describe the phenomenon in their
   own words, with no jargon required. If they already have text (a paper
   draft, notes, a figure), ask for it and use it as a pre-filled draft.
2. **One question at a time.** Never send a block of ten questions.
3. **Offer options.** Each question has 2-4 concrete options, each with a
   short plain-language consequence and a recommended option. The researcher
   can always answer freely instead.
4. **Translate.** The researcher speaks the language of their field; you
   write the specification. Confirm translations: "When you say *contagion*,
   do you mean agents copy a behavior after one contact, or only after
   repeated exposure?"
5. **Push for the minimum.** Ask "Is this needed to answer your research
   question?" for every entity and mechanism. A simpler model the researcher
   fully understands beats a complex one they cannot defend.
6. **Record as you go.** Update `model-specification.md` after each answer
   and show the researcher the change.

---

## Interview Dimensions

Cover all of these. The order is a guideline; follow the conversation, but
check every dimension before you exit.

### A. Purpose and question
- What phenomenon or pattern does the model explain or explore?
- What specific question should the simulation answer?
- Who is the audience (theory building, policy exploration, teaching)?
- What patterns from the real world should the model be able to reproduce
  (stylized facts)?

### B. Entities
- What kinds of agents exist? Are there several types?
- Are there non-agent entities (patches or cells, resources, institutions,
  the global environment)?
- Are agents identical or heterogeneous? In which attributes?

### C. State variables
- What attributes does each agent have? For each: type, unit, allowed range.
- Which attributes change over time, and which are fixed?
- Does the environment have its own state?

### D. Space and topology
- Does space matter for the phenomenon?
- If yes: discrete grid, continuous space, or a network? Which neighborhood
  or network structure? What happens at the edges?
- If no: who can interact with whom (anyone with anyone, groups)?

### E. Time and scales
- What does one simulation step represent in real time (a day, an
  interaction, a generation)?
- How long does a run last (a fixed number of steps, or until a condition
  is met)?
- What is the spatial extent, if any?

### F. Behavior and decisions
- What does an agent do in one step?
- What information does it use (sensing): its own state, its neighbors,
  global information?
- How does it decide: a fixed rule, a threshold, optimization, imitation,
  learning, chance?
- Do agents adapt or learn from past experience? Do they predict the future?

### G. Interaction
- Do agents interact directly (one-to-one, group) or indirectly (through
  the environment)?
- What exactly changes when two agents interact?

### H. Scheduling
- In what order do agents act? Does the order matter?
- Do all agents update at once (synchronous) or one by one (sequential)?
- Are there several sub-steps per step (e.g., move, then interact, then
  update)?

### I. Stochasticity
- Which processes are random, and with what distribution?
- Which processes are deterministic?

### J. Initialization and input
- How is the population created at the start? Same for every run?
- Does the model use external data (empirical distributions, maps, time
  series)?

### K. Population dynamics
- Can agents be born, die, enter, or leave? If yes, under which rules?

### L. Outputs
- Which metrics answer the research question (averages, distributions,
  clusters, time to consensus)?
- At which resolution (every step, end of the run, per agent, aggregate)?
- Which experiments or scenarios does the researcher want to compare?

---

## Handling Answers

| Researcher says | Agent does |
|---|---|
| A clear answer | Write it into the specification |
| "I don't know" / "Whatever is standard" | Present literature-standard options with consequences; if they pick one, log it as `[ASSUMPTION]` |
| "Doesn't matter" | Check: "Would changing this change your results?" If it might, it matters; offer to make it a parameter for sensitivity analysis |
| Nothing (the topic was skipped) | Tag it `[DECISION NEEDED]` |

---

## Exit Criteria

- Every dimension A-L is answered or explicitly tagged `[DECISION NEEDED]`.
- Every `[ASSUMPTION]` has a decision-log entry.
- The researcher has read `model-specification.md` and confirmed that it
  matches their idea.
- `TASKS.md` exists and lists the open `[DECISION NEEDED]` items.

Then move to Stage 2.
