
import argparse
import json
import time
from pathlib import Path

import numpy as np

from enterprise_fitness import evaluate_enterprise
from enterprise_random_search import random_search
from enterprise_hill_climbing import hill_climbing
from enterprise_hybrid_search import hybrid_search


ALGORITHMS = {
    "random": random_search,
    "hill": hill_climbing,
    "hybrid": hybrid_search,
}


def run_experiments(
    seeds,
    evaluations,
    commands,
    mutations,
    output_dir,
):
    if evaluations < 1:
        raise ValueError("Evaluations must be positive")

    if not 1 <= mutations <= commands:
        raise ValueError("Invalid mutation count")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    best_path = output_dir / "best_enterprise_chromosome.npy"
    results_path = output_dir / "enterprise_experiment_results.json"

    best_fitness = float("inf")

    if best_path.exists():
        existing = np.load(best_path, allow_pickle=False)
        best_fitness = float(evaluate_enterprise(existing))
        print("Previous best fitness:", best_fitness)

    results = []

    for name, algorithm in ALGORITHMS.items():
        for seed in seeds:
            print(
                f"\n--- {name.upper()} | Seed {seed} ---",
                flush=True,
            )

            start = time.perf_counter()

            if name == "random":
                chromosome, fitness = algorithm(
                    num_iterations=evaluations,
                    num_commands=commands,
                    seed=seed,
                )
            else:
                chromosome, fitness = algorithm(
                    num_iterations=evaluations,
                    num_commands=commands,
                    num_mutations=mutations,
                    seed=seed,
                )

            elapsed = time.perf_counter() - start
            fitness = float(fitness)

            result = {
                "algorithm": name,
                "seed": seed,
                "evaluations": evaluations,
                "commands": commands,
                "mutations": mutations if name != "random" else None,
                "fitness": fitness,
                "time_seconds": elapsed,
            }

            results.append(result)

            if fitness < best_fitness:
                verified = float(
                    evaluate_enterprise(chromosome)
                )

                assert np.isclose(
                    verified,
                    fitness,
                    atol=1e-10,
                    rtol=0,
                )

                np.save(best_path, chromosome)
                best_fitness = verified

                print(
                    "NEW GLOBAL BEST:",
                    best_fitness,
                    flush=True,
                )

            # Preserve statistics after every completed run.
            results_path.write_text(
                json.dumps(
                    {
                        "best_fitness": best_fitness,
                        "completed_runs": results,
                    },
                    indent=2,
                )
            )

            print(
                f"Completed in {elapsed:.2f}s",
                flush=True,
            )

    if not best_path.exists():
        raise RuntimeError("No best chromosome was saved")

    verified = float(
        evaluate_enterprise(
            np.load(best_path, allow_pickle=False)
        )
    )

    assert np.isclose(
        verified,
        best_fitness,
        atol=1e-10,
        rtol=0,
    )

    print("\n--- Enterprise Experiment Summary ---")
    print("Best fitness:", verified)
    print("Completed runs:", len(results))
    print("Fitness evaluations requested:",
          len(results) * evaluations)
    print("Verification: PASSED")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[10, 20, 30],
    )
    parser.add_argument(
        "--evaluations",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--commands",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--mutations",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--output-dir",
        default="results/enterprise",
    )

    args = parser.parse_args()

    run_experiments(
        seeds=args.seeds,
        evaluations=args.evaluations,
        commands=args.commands,
        mutations=args.mutations,
        output_dir=args.output_dir,
    )
