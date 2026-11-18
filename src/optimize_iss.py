
import json
from pathlib import Path

import numpy as np

from hybrid_search import hybrid_search
from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
)


SEEDS = [10, 20, 30, 40, 50]
BUDGETS = [100, 300]

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

best_overall = None
all_results = []

for budget in BUDGETS:
    print(f"\n--- Budget: {budget} evaluations ---")

    for seed in SEEDS:
        np.random.seed(seed)

        chromosome, fitness = hybrid_search(
            num_iterations=budget - 1,
            num_commands=100,
            num_mutations=10,
        )

        placement = evaluate_cube_placement(chromosome)

        result = {
            "seed": seed,
            "evaluations": budget,
            "fitness": float(fitness),
            "correct_cubes": int(placement["correct_cubes"]),
            "successful_moves": int(
                placement["successful_moves"]
            ),
            "rejected_moves": int(
                placement["rejected_moves"]
            ),
        }

        all_results.append(result)

        print(
            f"Seed {seed}: "
            f"fitness={fitness:.6f}, "
            f"correct cubes={result['correct_cubes']}"
        )

        if (
            best_overall is None
            or fitness < best_overall["fitness"]
        ):
            best_overall = result.copy()

            np.save(
                RESULTS_DIR / "best_iss_chromosome.npy",
                chromosome
            )

            print("New best solution saved!")


print("\n--- Budget Comparison ---")

for budget in BUDGETS:
    runs = [
        result
        for result in all_results
        if result["evaluations"] == budget
    ]

    print(f"\nBudget: {budget}")
    print(
        "Average fitness:",
        np.mean([r["fitness"] for r in runs])
    )
    print(
        "Average correct cubes:",
        np.mean([r["correct_cubes"] for r in runs])
    )


saved_chromosome = np.load(
    RESULTS_DIR / "best_iss_chromosome.npy"
)

verified_fitness = evaluate_chromosome(
    saved_chromosome
)

assert np.isclose(
    verified_fitness,
    best_overall["fitness"],
)

with open(
    RESULTS_DIR / "iss_optimization_results.json",
    "w",
) as file:
    json.dump(
        {
            "best_solution": best_overall,
            "all_results": all_results,
        },
        file,
        indent=4,
    )


print("\n--- Best ISS Solution ---")
print("Seed:", best_overall["seed"])
print("Evaluations:", best_overall["evaluations"])
print("Best fitness:", best_overall["fitness"])
print("Correct cubes:", best_overall["correct_cubes"])
print("Successful moves:", best_overall["successful_moves"])
print("Rejected moves:", best_overall["rejected_moves"])
print("Saved chromosome: results/best_iss_chromosome.npy")
print("Saved results: results/iss_optimization_results.json")
print("Fitness verification: PASSED")
