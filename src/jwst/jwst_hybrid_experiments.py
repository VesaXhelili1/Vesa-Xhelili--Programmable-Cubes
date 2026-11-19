
import argparse
import json
import time
from pathlib import Path

import numpy as np

from jwst_fitness import evaluate_jwst
from jwst_hybrid_search import hybrid_search


def run_experiments(
    seeds,
    evaluations,
    commands,
    baseline_path,
    output_dir,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load an existing verified solution.
    baseline = np.load(baseline_path).copy()
    baseline_fitness = float(evaluate_jwst(baseline))

    best_path = output_dir / "best_jwst_chromosome.npy"
    results_path = output_dir / (
        f"hybrid_{commands}cmd_{evaluations}eval_results.json"
    )

    # Never replace a better existing checkpoint.
    if best_path.exists():
        saved = np.load(best_path)
        saved_fitness = float(evaluate_jwst(saved))

        if saved_fitness < baseline_fitness:
            baseline = saved.copy()
            baseline_fitness = saved_fitness

    best = baseline.copy()
    best_fitness = baseline_fitness

    print("Starting fitness:", best_fitness)

    # Save the verified starting solution.
    np.save(best_path, best)

    results = []

    for seed in seeds:
        print(f"\n--- Seed {seed} ---", flush=True)

        np.random.seed(seed)
        start = time.perf_counter()

        candidate, fitness = hybrid_search(
            num_iterations=evaluations - 1,
            num_commands=commands,
            num_mutations=10,
        )

        elapsed = time.perf_counter() - start
        fitness = float(fitness)

        results.append({
            "seed": seed,
            "fitness": fitness,
            "evaluations": evaluations,
            "commands": commands,
            "time_seconds": elapsed,
        })

        if fitness < best_fitness:
            best = candidate.copy()
            best_fitness = fitness

            np.save(best_path, best)

            print(
                "NEW BEST FITNESS:",
                best_fitness,
                flush=True,
            )

        # Save statistics after every completed seed.
        results_path.write_text(
            json.dumps(
                {
                    "starting_fitness": baseline_fitness,
                    "best_fitness": best_fitness,
                    "completed_runs": results,
                },
                indent=2,
            )
        )

        print(
            f"Completed seed {seed} in {elapsed:.2f}s",
            flush=True,
        )

    # Verify the saved result using ESA's evaluator.
    verified = float(
        evaluate_jwst(np.load(best_path))
    )

    assert np.isclose(
        verified,
        best_fitness,
        rtol=0,
        atol=1e-10,
    )

    print("\n--- JWST Hybrid Search Summary ---")
    print("Starting fitness:", baseline_fitness)
    print("Final best fitness:", verified)
    print("Completed seeds:", len(results))
    print("Total evaluations:", len(results) * evaluations)
    print("Verification: PASSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        required=True,
    )

    parser.add_argument(
        "--evaluations",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--commands",
        type=int,
        default=300,
    )

    parser.add_argument(
        "--baseline",
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
    )

    args = parser.parse_args()

    run_experiments(
        seeds=args.seeds,
        evaluations=args.evaluations,
        commands=args.commands,
        baseline_path=args.baseline,
        output_dir=args.output_dir,
    )
