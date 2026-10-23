"""Experiment execution and scenario runner for opinion dynamics.

Executes baseline runs across multiple seeds, predefined scenarios,
and parameter sweeps according to experiment-config.yaml and ODD specifications.
"""

from pathlib import Path
import pandas as pd
import yaml
from model import OpinionModel
import metrics


def run_single_simulation(
    population_size: int = 1000,
    epsilon: float = 0.2,
    mu: float = 0.5,
    max_steps: int = 500,
    seed: int | None = 42,
    collect_agent_vars: bool = True,
) -> tuple[OpinionModel, dict]:
    """Execute a single model run and return the model instance and summary statistics."""
    model = OpinionModel(
        population_size=population_size,
        epsilon=epsilon,
        mu=mu,
        seed=seed,
        collect_agent_vars=collect_agent_vars,
    )

    for _ in range(max_steps):
        model.step()

    final_opinions = [a.opinion for a in model.agents]
    clusters = metrics.identify_clusters(final_opinions, epsilon=epsilon)
    mean_val = sum(final_opinions) / len(final_opinions)
    var_val = sum((x - mean_val) ** 2 for x in final_opinions) / len(final_opinions)

    summary = {
        "seed": seed,
        "population_size": population_size,
        "epsilon": epsilon,
        "mu": mu,
        "max_steps": max_steps,
        "steps_run": model.steps,
        "final_mean": mean_val,
        "final_variance": var_val,
        "cluster_count": len(clusters),
        "cluster_sizes": [len(c) for c in clusters],
    }

    return model, summary


def main() -> None:
    """Load configuration and run baseline experiments, scenarios, and parameter sweeps."""
    config_path = Path(__file__).parent / "experiment-config.yaml"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True, parents=True)

    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

    baseline_params = config.get("model_parameters", {})
    pop_size = baseline_params.get("population_size", {}).get("default", 1000)
    eps = baseline_params.get("epsilon", {}).get("default", 0.2)
    mu_val = baseline_params.get("mu", {}).get("default", 0.5)
    max_steps = config.get("run_controls", {}).get("max_steps", 500)
    seeds = config.get("run_controls", {}).get("seeds", [42, 123, 999])

    # -------------------------------------------------------------
    # 1. Run Baseline Simulations across all configured seeds
    # -------------------------------------------------------------
    print(f"1. Running Baseline Simulation across seeds {seeds} (N={pop_size}, eps={eps}, mu={mu_val}, T={max_steps})...")
    baseline_summaries = []

    for idx, s in enumerate(seeds):
        # Full agent collection for primary seed to generate trajectory plots
        collect_agents = (idx == 0)
        model, summary = run_single_simulation(
            population_size=pop_size,
            epsilon=eps,
            mu=mu_val,
            max_steps=max_steps,
            seed=s,
            collect_agent_vars=collect_agents,
        )
        summary["run_type"] = "baseline"
        baseline_summaries.append(summary)

        print(f"   - Seed {s}: {summary['cluster_count']} clusters formed | Sizes: {summary['cluster_sizes']}")

        if idx == 0:
            # Export data and plots for primary seed with metadata columns
            model_df = model.datacollector.get_model_vars_dataframe().copy()
            agent_df = model.datacollector.get_agent_vars_dataframe().copy()

            model_df["seed"] = s
            model_df["scenario"] = "baseline"
            model_df["population_size"] = pop_size
            model_df["epsilon"] = eps
            model_df["mu"] = mu_val

            agent_df["seed"] = s
            agent_df["scenario"] = "baseline"

            model_df.to_csv(output_dir / "baseline_model_vars.csv")
            agent_df.to_csv(output_dir / "baseline_agent_vars.csv")

            metrics.plot_opinion_trajectories(
                agent_df,
                title=f"Baseline Opinion Trajectories (Seed {s}, N={pop_size}, eps={eps}, mu={mu_val})",
                save_path=str(output_dir / "baseline_trajectories.png"),
            )
            final_opinions = [a.opinion for a in model.agents]
            metrics.plot_final_distribution(
                final_opinions,
                title=f"Final Opinion Distribution (Seed {s}, N={pop_size}, eps={eps}, mu={mu_val})",
                save_path=str(output_dir / "baseline_distribution.png"),
            )

    # -------------------------------------------------------------
    # 2. Run Theoretical Scenarios across configured seeds
    # -------------------------------------------------------------
    scenarios = config.get("scenarios", {})
    scenario_rows = []

    if scenarios:
        print("\n2. Running Defined Theoretical Scenarios across seeds:")
        for sc_name, sc_data in scenarios.items():
            sc_params = sc_data.get("parameters", {})
            sc_pop = sc_params.get("population_size", pop_size)
            sc_eps = sc_params.get("epsilon", eps)
            sc_mu = sc_params.get("mu", mu_val)
            sc_t = sc_params.get("max_steps", max_steps)

            for s in seeds:
                _, sc_summary = run_single_simulation(
                    population_size=sc_pop,
                    epsilon=sc_eps,
                    mu=sc_mu,
                    max_steps=sc_t,
                    seed=s,
                    collect_agent_vars=False,
                )
                sc_summary["scenario"] = sc_name
                sc_summary["description"] = sc_data.get("description", "")
                scenario_rows.append(sc_summary)
                print(f"   - {sc_name} (seed={s}, eps={sc_eps}): {sc_summary['cluster_count']} clusters -> sizes: {sc_summary['cluster_sizes']}")

        scenarios_df = pd.DataFrame(scenario_rows)
        scenarios_df.to_csv(output_dir / "scenarios_summary.csv", index=False)
        print(f"   -> Scenarios summary saved to: {output_dir / 'scenarios_summary.csv'}")

    # -------------------------------------------------------------
    # 3. Execute Parameter Sweep Grid (Full Verification)
    # -------------------------------------------------------------
    sweep_cfg = config.get("parameter_sweep", {})
    if sweep_cfg:
        grid = sweep_cfg.get("grid", {})
        fixed = sweep_cfg.get("fixed_parameters", {})
        reps = sweep_cfg.get("iterations_per_config", 3)
        base_seed = sweep_cfg.get("base_seed", 1000)

        eps_values = grid.get("epsilon", [0.1, 0.2, 0.3, 0.4, 0.5])
        fixed_pop = fixed.get("population_size", 1000)
        fixed_mu = fixed.get("mu", 0.5)
        fixed_t = fixed.get("max_steps", 500)

        print(f"\n3. Executing Parameter Sweep Grid ({len(eps_values)} values x {reps} replications = {len(eps_values)*reps} runs)...")
        sweep_rows = []
        run_id = 0

        for cur_eps in eps_values:
            for rep in range(reps):
                run_id += 1
                cur_seed = base_seed + run_id
                _, sw_summary = run_single_simulation(
                    population_size=fixed_pop,
                    epsilon=cur_eps,
                    mu=fixed_mu,
                    max_steps=fixed_t,
                    seed=cur_seed,
                    collect_agent_vars=False,
                )
                sw_summary["run_id"] = run_id
                sw_summary["replication"] = rep + 1
                sweep_rows.append(sw_summary)

        sweep_df = pd.DataFrame(sweep_rows)
        sweep_df.to_csv(output_dir / "parameter_sweep_results.csv", index=False)
        print(f"   -> Parameter sweep results saved to: {output_dir / 'parameter_sweep_results.csv'}")

        # Aggregate sweep summary table
        agg_summary = sweep_df.groupby("epsilon")["cluster_count"].agg(["mean", "std", "min", "max"]).reset_index()
        print("\nParameter Sweep Aggregate Results (Cluster Count by Epsilon):")
        print(agg_summary.to_string(index=False))

    print(f"\nAll experiments successfully completed. Outputs written to: {output_dir}")


if __name__ == "__main__":
    main()
