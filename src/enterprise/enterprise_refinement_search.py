
import argparse
import json
import time
from pathlib import Path

import numpy as np

from enterprise_fitness import evaluate_enterprise
from enterprise_hill_climbing import mutate_chromosome
from enterprise_random_search import MAX_COMMANDS


def run_refinement(
    baseline_path,
    output_dir,
    mutation_sizes=(1, 3, 10),
    evaluations=300,
    seed=42,
):
    """Refine a saved Enterprise solution.

    Each mutation strategy starts from the same baseline.
    Lower ESA fitness is better.
    """

    if evaluations < 1:
        raise ValueError("Evaluations must be positive")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = np.load(
        baseline_path, allow_pickle=False
    ).copy()

    if (
        baseline.ndim != 1
        or len(baseline) < 3
        or len(baseline) % 2 != 1
        or baseline[-1] != -1
    ):
        raise ValueError("Invalid chromosome structure")

    num_commands = (len(baseline) - 1) // 2

    if num_commands > MAX_COMMANDS:
        raise ValueError("Command limit exceeded")

    if (
        np.any(baseline[:-1:2] < 0)
        or np.any(baseline[:-1:2] >= 1472)
        or np.any(baseline[1:-1:2] < 0)
        or np.any(baseline[1:-1:2] >= 6)
    ):
        raise ValueError("Invalid movement command")

    if any(
        not 1 <= size <= num_commands
        for size in mutation_sizes
    ):
        raise ValueError("Invalid mutation size")

    baseline_fitness = float(
        evaluate_enterprise(baseline)
    )

    best_path = output_dir / "best_refined_enterprise.npy"
    results_path = output_dir / "refinement_results.json"

    global_best = baseline.copy()
    global_fitness = baseline_fitness

    # Preserve a previously saved better solution.
    if best_path.exists():
        previous = np.load(
            best_path, allow_pickle=False
        )
        previous_fitness = float(
            evaluate_enterprise(previous)
        )

        if previous_fitness < global_fitness:
            global_best = previous.copy()
            global_fitness = previous_fitness

    # Always save the best verified starting solution.
    np.save(best_path, global_best)

    results = []

    print("Baseline fitness:", baseline_fitness)

    for size in mutation_sizes:
        rng = np.random.default_rng(seed + size)

        current = baseline.copy()
        current_fitness = baseline_fitness

        improvements = 0
        history = [current_fitness]
        start = time.perf_counter()

        print(f"\n--- Mutation size {size} ---", flush=True)

        for iteration in range(evaluations):
            candidate = mutate_chromosome(
                current,
                num_mutations=size,
                rng=rng,
            )

            fitness = float(
                evaluate_enterprise(candidate)
            )

            if fitness < current_fitness:
                current = candidate.copy()
                current_fitness = fitness
                improvements += 1

                if fitness < global_fitness:
                    global_best = candidate.copy()
                    global_fitness = fitness

                    np.save(best_path, global_best)

                    print(
                        f"Evaluation {iteration + 1}: "
                        f"new best {fitness:.9f}",
                        flush=True,
                    )

            history.append(current_fitness)

        results.append({
            "mutation_size": size,
            "evaluations": evaluations,
            "seed": seed + size,
            "starting_fitness": baseline_fitness,
            "final_fitness": current_fitness,
            "improvements": improvements,
            "time_seconds": time.perf_counter() - start,
            "fitness_history": history,
        })

        # Save the statistics after each strategy.
        results_path.write_text(
            json.dumps({
                "baseline_fitness": baseline_fitness,
                "global_best_fitness": global_fitness,
                "experiments": results,
            }, indent=2)
        )

    verified = float(
        evaluate_enterprise(
            np.load(best_path, allow_pickle=False)
        )
    )

    assert np.isclose(
        verified, global_fitness,
        atol=1e-10, rtol=0
    )

    print("\n--- Enterprise Refinement Summary ---")
    print("Baseline fitness:", baseline_fitness)
    print("Best fitness:", verified)
    print("Evaluations:",
          len(mutation_sizes) * evaluations)
    print("Verification: PASSED")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--baseline", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--mutation-sizes",
        type=int,
        nargs="+",
        default=[1, 3, 10],
    )
    parser.add_argument(
        "--evaluations", type=int, default=300
    )
    parser.add_argument(
        "--seed", type=int, default=42
    )

    args = parser.parse_args()

    run_refinement(
        baseline_path=args.baseline,
        output_dir=args.output_dir,
        mutation_sizes=args.mutation_sizes,
        evaluations=args.evaluations,
        seed=args.seed,
    )
