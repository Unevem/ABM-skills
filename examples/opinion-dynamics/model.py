"""Simulation model for Deffuant opinion dynamics.

Conforms to ODD Protocol:
- Orchestration & Scheduling: ODD Section 3
- Design Concepts: ODD Section 4
- Initialization: ODD Section 5
- Parameters & Outputs: ODD Annex A.1 & A.2
"""

import mesa
from agents import OpinionAgent


def compute_mean_opinion(model: "OpinionModel") -> float:
    """Calculate the average opinion across all active agents.
    
    ODD: Annex A.2 - Output Table
    """
    agents = model.agents.to_list()
    if not agents:
        return 0.0
    return sum(a.opinion for a in agents) / len(agents)


def compute_opinion_variance(model: "OpinionModel") -> float:
    """Calculate the variance of opinions across all active agents.
    
    ODD: Annex A.2 - Output Table
    """
    agents = model.agents.to_list()
    if not agents:
        return 0.0
    mean_val = compute_mean_opinion(model)
    return sum((a.opinion - mean_val) ** 2 for a in agents) / len(agents)


class OpinionModel(mesa.Model):
    """Deffuant bounded confidence opinion dynamics model.
    
    ODD: Section 1-3 & Section 5
    """

    def __init__(
        self,
        population_size: int = 1000,
        epsilon: float = 0.2,
        mu: float = 0.5,
        seed: int | None = None,
        collect_agent_vars: bool = True,
    ) -> None:
        """Initialize the simulation model.
        
        Args:
            population_size: Number of agents (ODD Annex A.1: population_size, default=1000).
            epsilon: Confidence bound threshold (ODD Annex A.1: epsilon, default=0.2).
            mu: Convergence rate (ODD Annex A.1: mu, default=0.5).
            seed: Explicit seed for random number generation (Reproducibility rule).
            collect_agent_vars: Whether to collect micro agent-level vars at every step (default=True).
        """
        # Seeds self.random and self.rng in Mesa 3.x
        super().__init__(rng=seed)

        # Validate domain boundaries for parameters (ODD Annex A.1)
        if not (1 <= population_size <= 10000):
            raise ValueError("population_size must be in [1, 10000]")
        if not (0.01 <= epsilon <= 1.0):
            raise ValueError("epsilon must be in [0.01, 1.0]")
        if not (0.01 <= mu <= 0.5):
            raise ValueError("mu must be in [0.01, 0.5]")

        # ODD: Annex A.1 - Parameters
        self.population_size: int = population_size
        self.epsilon: float = float(epsilon)
        self.mu: float = float(mu)
        self.collect_agent_vars: bool = collect_agent_vars

        # ODD: Section 5 - Initialization
        # Instantiate N agents with initial opinions drawn uniformly from [0.0, 1.0]
        for _ in range(self.population_size):
            initial_opinion = self.random.random()
            # Agent automatically registers into self.agents in Mesa 3.x
            OpinionAgent(self, opinion=initial_opinion)

        # ODD: Section 4.11 & Annex A.2 - Data Collection
        agent_reporters = {"opinion": lambda a: a.opinion} if self.collect_agent_vars else {}
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "mean_opinion": compute_mean_opinion,
                "opinion_variance": compute_opinion_variance,
            },
            agent_reporters=agent_reporters,
        )

        # Collect initial step 0 state
        self.datacollector.collect(self)

    def step(self) -> None:
        """Advance the simulation by one Monte Carlo sweep.
        
        ODD: Section 3 - Process Overview and Scheduling
        """
        # Random sequential activation: shuffle agents each step and call their step method
        self.agents.shuffle_do("step")

        # Collect data at conclusion of the step
        self.datacollector.collect(self)
