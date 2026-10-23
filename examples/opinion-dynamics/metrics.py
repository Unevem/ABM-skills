"""Metrics calculation and visualization routines for opinion dynamics.

Conforms to ODD Protocol:
- Observation: ODD Section 4.11
- Submodel: ODD Section 7.2 (Cluster Identification)
- Outputs: ODD Annex A.2
"""

from typing import Sequence
import matplotlib.pyplot as plt
import pandas as pd


def identify_clusters(opinions: Sequence[float], epsilon: float) -> list[list[float]]:
    """Group continuous opinions into discrete clusters using 1D single-linkage gap clustering.
    
    ODD: Section 7.2 - Cluster Identification
    Agents in the same cluster have distance between consecutive sorted values < epsilon.
    
    Args:
        opinions: Collection of final opinion values.
        epsilon: Confidence bound threshold.
        
    Returns:
        List of clusters, where each cluster is a list of opinion floats.
    """
    if not opinions:
        return []

    sorted_opinions = sorted(opinions)
    clusters: list[list[float]] = [[sorted_opinions[0]]]

    for x in sorted_opinions[1:]:
        # ODD: Section 7.2 - Cluster boundary placed when gap >= epsilon
        if (x - clusters[-1][-1]) < epsilon:
            clusters[-1].append(x)
        else:
            clusters.append([x])

    return clusters


def count_clusters(opinions: Sequence[float], epsilon: float) -> int:
    """Return the total number of distinct opinion clusters.
    
    ODD: Annex A.2 - Output Table (cluster_count)
    """
    return len(identify_clusters(opinions, epsilon))


def plot_opinion_trajectories(
    agent_df: pd.DataFrame,
    title: str = "Deffuant Opinion Trajectories Over Time",
    save_path: str | None = None,
) -> None:
    """Plot individual opinion trajectories across simulation steps.
    
    Args:
        agent_df: Multi-index DataFrame from DataCollector.get_agent_vars_dataframe().
                  Index levels: (Step, AgentID), columns: ['opinion'].
        title: Plot title.
        save_path: Optional path to save the generated image file.
    """
    plt.figure(figsize=(10, 6))
    
    # Unstack so columns represent agents and index represents steps
    unstacked = agent_df["opinion"].unstack(level="AgentID")
    
    for agent_id in unstacked.columns:
        plt.plot(unstacked.index, unstacked[agent_id], alpha=0.3, linewidth=0.8)

    plt.title(title, fontsize=12)
    plt.xlabel("Simulation Step (Monte Carlo Sweeps)", fontsize=10)
    plt.ylabel("Opinion x in [0, 1]", fontsize=10)
    plt.ylim(-0.02, 1.02)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_final_distribution(
    opinions: Sequence[float],
    title: str = "Final Opinion Distribution",
    bins: int = 40,
    save_path: str | None = None,
) -> None:
    """Plot a histogram of opinions at the end of the simulation.
    
    Args:
        opinions: List or array of final agent opinions.
        title: Plot title.
        bins: Number of histogram bins.
        save_path: Optional path to save the generated image file.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(opinions, bins=bins, range=(0.0, 1.0), edgecolor="black", alpha=0.7, color="#2b5c8f")
    plt.title(title, fontsize=12)
    plt.xlabel("Opinion x", fontsize=10)
    plt.ylabel("Agent Count", fontsize=10)
    plt.xlim(0.0, 1.0)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()
