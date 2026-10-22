"""Agent definitions for Deffuant opinion dynamics.

Conforms to ODD Protocol:
- Entity & State Variables: ODD Section 2
- Process: ODD Section 3
- Submodel: ODD Section 7.1 (Opinion Revision)
"""

from typing import TYPE_CHECKING
import mesa

if TYPE_CHECKING:
    from model import OpinionModel


class OpinionAgent(mesa.Agent):
    """An agent possessing a continuous opinion in [0.0, 1.0].
    
    ODD: Section 2 - Entities, State Variables, and Scales
    """

    def __init__(self, model: "OpinionModel", opinion: float) -> None:
        """Initialize the opinion agent.
        
        Args:
            model: The parent OpinionModel instance.
            opinion: Initial continuous opinion value in [0.0, 1.0].
        """
        # In Mesa 3.x, unique_id is managed automatically
        super().__init__(model)
        
        # ODD: Section 2 - State variable: opinion (float in [0.0, 1.0], dynamic)
        self.opinion: float = float(opinion)

    def step(self) -> None:
        """Execute one agent step in the Monte Carlo sweep.
        
        ODD: Section 3 - Process Overview and Scheduling
        """
        # In a well-mixed population of size >= 2, choose an interaction partner j != self
        agent_list = self.model.agents.to_list()
        if len(agent_list) < 2:
            return

        # Draw a random peer from the global pool using the model's seeded RNG
        partner = self.model.random.choice(agent_list)
        while partner is self and len(agent_list) > 1:
            partner = self.model.random.choice(agent_list)

        self.interact(partner)

    def interact(self, partner: "OpinionAgent") -> None:
        """Bilateral opinion revision under bounded confidence.
        
        ODD: Section 7.1 - Submodel: Opinion Revision
        Reference: Deffuant et al. (2000), Eq. 1 & 2
        """
        distance = abs(self.opinion - partner.opinion)

        # ODD: Section 7.1 - Rule: interact if and only if |x_i - x_j| < epsilon
        if distance < self.model.epsilon:
            # ODD: Section 7.1 - Symmetric convergence with rate mu
            diff = partner.opinion - self.opinion
            self.opinion += self.model.mu * diff
            partner.opinion -= self.model.mu * diff

            # ODD: Section 7.1 - Invariant preservation on [0.0, 1.0]
            self.opinion = max(0.0, min(1.0, self.opinion))
            partner.opinion = max(0.0, min(1.0, partner.opinion))
