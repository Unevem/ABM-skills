"""Automated Verification Suite (V1 to V8) for Deffuant Opinion Dynamics.

Conforms to Stage 4 Verification requirements in references/stage-4-verify.md.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

# Add parent directory to sys.path to allow importing model, agents, metrics
sys.path.insert(0, str(Path(__file__).parent.parent))

from model import OpinionModel
import metrics


def test_v1_model_runs() -> None:
    """V1: The model initializes and runs N steps with default configuration without raising."""
    model = OpinionModel(population_size=50, epsilon=0.2, mu=0.5, seed=42)
    for _ in range(50):
        model.step()
    assert model.steps == 50


def test_v2_seed_determinism() -> None:
    """V2: Two runs with the same seed and parameters produce identical DataCollector output."""
    model_a = OpinionModel(population_size=30, epsilon=0.2, mu=0.5, seed=123)
    model_b = OpinionModel(population_size=30, epsilon=0.2, mu=0.5, seed=123)

    for _ in range(30):
        model_a.step()
        model_b.step()

    df_a = model_a.datacollector.get_model_vars_dataframe()
    df_b = model_b.datacollector.get_model_vars_dataframe()

    pd.testing.assert_frame_equal(df_a, df_b)

    agent_df_a = model_a.datacollector.get_agent_vars_dataframe()
    agent_df_b = model_b.datacollector.get_agent_vars_dataframe()

    pd.testing.assert_frame_equal(agent_df_a, agent_df_b)


def test_v3_seed_sensitivity() -> None:
    """V3: Two different seeds produce different outputs (confirms seed is used)."""
    model_1 = OpinionModel(population_size=30, epsilon=0.2, mu=0.5, seed=10)
    model_2 = OpinionModel(population_size=30, epsilon=0.2, mu=0.5, seed=20)

    for _ in range(20):
        model_1.step()
        model_2.step()

    df_1 = model_1.datacollector.get_model_vars_dataframe()
    df_2 = model_2.datacollector.get_model_vars_dataframe()

    # The trajectories should diverge for different seeds
    assert not df_1.equals(df_2)


def test_v4_state_invariants() -> None:
    """V4: After every step, every state variable stays within its ODD 2 range [0.0, 1.0]."""
    model = OpinionModel(population_size=40, epsilon=0.3, mu=0.5, seed=99)
    for _ in range(30):
        model.step()
        for agent in model.agents:
            assert 0.0 <= agent.opinion <= 1.0, f"Opinion {agent.opinion} escaped [0.0, 1.0]"


def test_v5_population_conservation() -> None:
    """V5: The agent count stays strictly constant across all steps."""
    initial_n = 50
    model = OpinionModel(population_size=initial_n, epsilon=0.2, mu=0.5, seed=77)
    assert len(model.agents) == initial_n

    for _ in range(30):
        model.step()
        assert len(model.agents) == initial_n


def test_v6_parameters_wired() -> None:
    """V6: Each parameter reaches the model and changing it affects behavior."""
    # Changing epsilon from narrow to wide must lead to fewer clusters
    model_narrow = OpinionModel(population_size=60, epsilon=0.05, mu=0.5, seed=42)
    model_wide = OpinionModel(population_size=60, epsilon=0.5, mu=0.5, seed=42)

    for _ in range(200):
        model_narrow.step()
        model_wide.step()

    opinions_narrow = [a.opinion for a in model_narrow.agents]
    opinions_wide = [a.opinion for a in model_wide.agents]

    clusters_narrow = metrics.count_clusters(opinions_narrow, epsilon=0.05)
    clusters_wide = metrics.count_clusters(opinions_wide, epsilon=0.5)

    assert clusters_narrow > clusters_wide
    assert clusters_wide == 1  # Epsilon 0.5 reaches global consensus


def test_v7_outputs_collected() -> None:
    """V7: Every metric in the ODD output table appears in collected data with expected rows."""
    steps = 25
    n_agents = 20
    model = OpinionModel(population_size=n_agents, epsilon=0.2, mu=0.5, seed=5)

    for _ in range(steps):
        model.step()

    model_df = model.datacollector.get_model_vars_dataframe()
    agent_df = model.datacollector.get_agent_vars_dataframe()

    # ODD Annex A.2 metrics
    assert "mean_opinion" in model_df.columns
    assert "opinion_variance" in model_df.columns
    assert "opinion" in agent_df.columns

    # Step 0 plus steps 1..25 = 26 data points
    assert len(model_df) == steps + 1
    assert len(agent_df) == (steps + 1) * n_agents


def test_v8_edge_cases() -> None:
    """V8: Edge cases (single agent, invalid parameter boundaries)."""
    # 1. Single agent population: no crash, stays intact
    single_agent_model = OpinionModel(population_size=1, epsilon=0.2, mu=0.5, seed=42)
    initial_op = single_agent_model.agents.to_list()[0].opinion
    single_agent_model.step()
    assert single_agent_model.agents.to_list()[0].opinion == initial_op

    # 2. Invalid parameter values raise ValueError
    with pytest.raises(ValueError):
        OpinionModel(population_size=0)

    with pytest.raises(ValueError):
        OpinionModel(epsilon=-0.1)

    with pytest.raises(ValueError):
        OpinionModel(epsilon=1.5)

    with pytest.raises(ValueError):
        OpinionModel(mu=0.0)

    with pytest.raises(ValueError):
        OpinionModel(mu=0.9)  # mu cannot exceed 0.5 in Deffuant formulation
