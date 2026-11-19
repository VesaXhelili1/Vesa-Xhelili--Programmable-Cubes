
import argparse
import json
import time
from pathlib import Path

import numpy as np

from jwst_hybrid_search import hybrid_search
from jwst_fitness import evaluate_jwst
from analyze_movements import analyze_movements


ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "jwst"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_experiment(command_counts, evaluations, seeds):
    all_results = []
    best_overall = None

    for num_commands in command_counts:
        print(f"\n--- Commands: {num_commands} ---")

        for seed in seeds:
            np.random.seed(seed)

            start = time.perf_counter()

            chromosome, fitness = hybrid_search(
                num_iterations=evaluations - 1,
                num_commands=num_commands,
                num_mutations=10,
            )

            elapsed = time.perf_counter() - start

            successful, rejected = analyze_movements(
                chromosome
            )

            result = {
                "seed": seed,
                "commands": num_commands,
                "evaluations": evaluations,
                "fitness": float(fitness),
                "successful_moves": successful,
                "rejected_moves": rejected,
                "time_seconds": elapsed,
            }

            all_results.append(result)

            print(
                f"Seed {seed}: "
                f"fitness={fitness:.6f}, "
                f"successful={successful}, "
                f"time={elapsed:.3f}s"
            )

            if (
                best_overall is None
                or fitness < best_overall["fitness"]
            ):
                best_overall = result.copy()

                np.save(
                    RESULTS_DIR / "best_jwst_chromosome.npy",
                    chromosome,
                )

                print("New best JWST chromosome saved!")

    saved = np.load(
        RESULTS_DIR / "best_jwst_chromosome.npy"
    )

    verified_fitness = evaluate_jwst(saved)

    assert np.isclose(
        verified_fitness,
        best_overall["fitness"],
    )

    output = {
        "best_solution": best_overall,
        "all_results": all_results,
    }

    with open(
        RESULTS_DIR / "jwst_optimization_results.json",
        "w",
    ) as file:
        json.dump(output, file, indent=4)

    print("\n--- JWST Optimization Summary ---")

    for num_commands in command_counts:
        runs = [
            r for r in all_results
            if r["commands"] == num_commands
        ]

        print(f"\nCommands: {num_commands}")
        print(
            "Average fitness:",
            np.mean([r["fitness"] for r in runs])
        )
        print(
            "Average time:",
            f'{np.mean([r["time_seconds"] for r in runs]):.3f}s'
        )

    print("\n--- Best JWST Solution ---")
    print("Seed:", best_overall["seed"])
    print("Commands:", best_overall["commands"])
    print("Evaluations:", best_overall["evaluations"])
    print("Fitness:", best_overall["fitness"])
    print("Successful moves:", best_overall["successful_moves"])
    print("Rejected moves:", best_overall["rejected_moves"])
    print("Verification: PASSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--commands",
        type=int,
        nargs="+",
        default=[100, 300],
    )
    parser.add_argument(
        "--evaluations",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[10, 20, 30, 40, 50],
    )

    args = parser.parse_args()

    run_experiment(
        args.commands,
        args.evaluations,
        args.seeds,
    )
