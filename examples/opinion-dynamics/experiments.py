"""Experiment execution and scenario runner for opinion dynamics.

Executes baseline runs, predefined scenarios, and parameter sweeps according
to experiment-config.yaml and ODD specifications.
"""

from pathlib import Path
import yaml
from model import OpinionModel
import metrics


def run_single_simulation(
    population_size: int = 100,
    epsilon: float = 0.2,
    mu: float = 0.5,
    max_steps: int = 1000,
    seed: int | None = 42,
) -> tuple[OpinionModel, dict]:
    """Execute a single model run and return the model instance and summary statistics."""
    model = OpinionModel(
        population_size=population_size,
        epsilon=epsilon,
        mu=mu,
        seed=seed,
    )

    for _ in range(max_steps):
        model.step()

    final_opinions = [a.opinion for a in model.agents]
    clusters = metrics.identify_clusters(final_opinions, epsilon=epsilon)

    summary = {
        "seed": seed,
        "population_size": population_size,
        "epsilon": epsilon,
        "mu": mu,
        "steps_run": model.steps,
        "final_mean": sum(final_opinions) / len(final_opinions),
        "cluster_count": len(clusters),
        "cluster_sizes": [len(c) for c in clusters],
    }

    return model, summary


def main() -> None:
    """Load configuration and run baseline experiments and scenario comparisons."""
    config_path = Path(__file__).parent / "experiment-config.yaml"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True, parents=True)

    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

    # 1. Run Baseline Simulation
    print("Running Baseline Simulation (Deffuant Bounded Confidence)...")
    baseline_params = config.get("model_parameters", {})
    pop_size = baseline_params.get("population_size", {}).get("default", 100)
    eps = baseline_params.get("epsilon", {}).get("default", 0.2)
    mu_val = baseline_params.get("mu", {}).get("default", 0.5)
    max_steps = config.get("run_controls", {}).get("max_steps", 1000)
    seed = config.get("run_controls", {}).get("seeds", [42])[0]

    model, summary = run_single_simulation(
        population_size=pop_size,
        epsilon=eps,
        mu=mu_val,
        max_steps=max_steps,
        seed=seed,
    )

    print(f"Baseline finished in {summary['steps_run']} steps.")
    print(f"Clusters formed: {summary['cluster_count']} | Cluster sizes: {summary['cluster_sizes']}")

    # Export Data
    model_df = model.datacollector.get_model_vars_dataframe()
    agent_df = model.datacollector.get_agent_vars_dataframe()

    model_df.to_csv(output_dir / "baseline_model_vars.csv")
    agent_df.to_csv(output_dir / "baseline_agent_vars.csv")

    # Generate Plots
    metrics.plot_opinion_trajectories(
        agent_df,
        title=f"Baseline Opinion Trajectories (eps={eps}, mu={mu_val})",
        save_path=str(output_dir / "baseline_trajectories.png"),
    )
    final_opinions = [a.opinion for a in model.agents]
    metrics.plot_final_distribution(
        final_opinions,
        title=f"Final Opinion Distribution (eps={eps}, mu={mu_val})",
        save_path=str(output_dir / "baseline_distribution.png"),
    )
    print(f"Results and plots saved to: {output_dir}")

    # 2. Run Theoretical Scenarios
    scenarios = config.get("scenarios", {})
    if scenarios:
        print("\nRunning Defined Theoretical Scenarios:")
        for sc_name, sc_data in scenarios.items():
            sc_params = sc_data.get("parameters", {})
            _, sc_summary = run_single_simulation(
                population_size=sc_params.get("population_size", pop_size),
                epsilon=sc_params.get("epsilon", eps),
                mu=sc_params.get("mu", mu_val),
                max_steps=sc_params.get("max_steps", max_steps),
                seed=seed,
            )
            print(f"  - {sc_name} (eps={sc_params.get('epsilon')}): {sc_summary['cluster_count']} clusters -> {sc_data.get('description')}")


if __name__ == "__main__":
    main()
