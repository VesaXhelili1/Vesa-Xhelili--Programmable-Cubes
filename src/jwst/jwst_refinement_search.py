
import argparse
import json
import time
from pathlib import Path

import numpy as np

from jwst_fitness import evaluate_jwst


JWST_CUBES = 643
MOVEMENT_TYPES = 6


def mutate_chromosome(chromosome, mutation_count, rng):
    """Modify selected commands without changing chromosome length."""

    candidate = chromosome.copy()
    num_commands = (len(candidate) - 1) // 2

    if mutation_count < 1 or mutation_count > num_commands:
        raise ValueError("Invalid mutation count")

    positions = rng.choice(
        num_commands,
        size=mutation_count,
        replace=False,
    )

    for position in positions:
        index = 2 * position

        if rng.random() < 0.5:
            old_value = int(candidate[index])
            new_value = int(rng.integers(0, JWST_CUBES - 1))

            if new_value >= old_value:
                new_value += 1

            candidate[index] = new_value
        else:
            old_value = int(candidate[index + 1])
            new_value = int(rng.integers(0, MOVEMENT_TYPES - 1))

            if new_value >= old_value:
                new_value += 1

            candidate[index + 1] = new_value

    return candidate


def run_refinement(
    baseline_path,
    output_dir,
    mutation_sizes=(1, 3, 10),
    evaluations=300,
):
    """Compare mutation sizes starting from one saved solution."""

    if evaluations < 1:
        raise ValueError("Evaluations must be positive")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = np.load(baseline_path).copy()

    if len(baseline) < 3 or baseline[-1] != -1:
        raise ValueError("Invalid chromosome format")

    if (len(baseline) - 1) % 2 != 0:
        raise ValueError("Invalid chromosome length")

    baseline_fitness = float(evaluate_jwst(baseline))

    best_path = output_dir / "best_refined_jwst.npy"
    results_path = output_dir / "refinement_results.json"

    global_best = baseline.copy()
    global_fitness = baseline_fitness

    # Preserve a better result from a previous run.
    if best_path.exists():
        previous = np.load(best_path)
        previous_fitness = float(evaluate_jwst(previous))

        if previous_fitness < global_fitness:
            global_best = previous.copy()
            global_fitness = previous_fitness
    
    np.save(best_path, global_best)

    results = []

    print("Starting fitness:", baseline_fitness)

    for mutation_size in mutation_sizes:
        print(
            f"\n--- Mutation size {mutation_size} ---",
            flush=True,
        )

        rng = np.random.default_rng(100 + mutation_size)

        current = baseline.copy()
        current_fitness = baseline_fitness

        improvements = 0
        history = [current_fitness]

        start = time.perf_counter()

        for iteration in range(evaluations):
            candidate = mutate_chromosome(
                current,
                mutation_size,
                rng,
            )

            fitness = float(evaluate_jwst(candidate))

            if fitness < current_fitness:
                current = candidate.copy()
                current_fitness = fitness
                improvements += 1

                print(
                    f"Evaluation {iteration + 1}: "
                    f"Improved to {fitness:.9f}",
                    flush=True,
                )

                if fitness < global_fitness:
                    global_best = current.copy()
                    global_fitness = fitness

                    np.save(best_path, global_best)

                    print(
                        "NEW GLOBAL BEST:",
                        global_fitness,
                        flush=True,
                    )

            history.append(current_fitness)

        elapsed = time.perf_counter() - start

        results.append({
            "mutation_size": mutation_size,
            "evaluations": evaluations,
            "starting_fitness": baseline_fitness,
            "final_fitness": current_fitness,
            "improvements": improvements,
            "time_seconds": elapsed,
            "fitness_history": history,
        })

        # Save statistics after each completed strategy.
        results_path.write_text(
            json.dumps(
                {
                    "baseline_fitness": baseline_fitness,
                    "global_best_fitness": global_fitness,
                    "experiments": results,
                },
                indent=2,
            )
        )

    verified = float(evaluate_jwst(np.load(best_path)))

    assert np.isclose(
        verified,
        global_fitness,
        rtol=0,
        atol=1e-10,
    )

    print("\n--- JWST Refinement Summary ---")
    print("Original fitness:", baseline_fitness)
    print("Best refinement fitness:", verified)
    print("Total evaluations:",
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
        "--evaluations",
        type=int,
        default=300,
    )

    args = parser.parse_args()

    run_refinement(
        baseline_path=args.baseline,
        output_dir=args.output_dir,
        mutation_sizes=args.mutation_sizes,
        evaluations=args.evaluations,
    )
