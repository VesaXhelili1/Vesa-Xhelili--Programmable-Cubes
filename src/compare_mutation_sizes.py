
from pathlib import Path

import numpy as np

from legal_aware_hybrid import legal_aware_hybrid
from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
)


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

original = np.load(
    RESULTS_DIR / "best_iss_legal_aware.npy"
)

strategies = {
    "Small (1-5)": (1, 5),
    "Medium (5-10)": (5, 10),
    "Large (10-20)": (10, 20),
}

seeds = [10, 20, 30]
results = []
best_fitness = float("inf")
best_solution = None

print("Starting fitness:", evaluate_chromosome(original))

for name, (min_replace, max_replace) in strategies.items():
    print(f"\n--- Strategy: {name} ---")

    for seed in seeds:
        np.random.seed(seed)

        chromosome, fitness = legal_aware_hybrid(
            initial_chromosome=original,
            num_iterations=299,
            min_replace=min_replace,
            max_replace=max_replace,
        )

        placement = evaluate_cube_placement(chromosome)

        if fitness < best_fitness:
            best_fitness = fitness
            best_solution = chromosome.copy()

            np.save(
                RESULTS_DIR / "best_iss_mutation.npy",
                best_solution
            )

            print(
                f"New best chromosome saved: "
                f"{best_fitness:.6f}"
            )


        results.append({
            "strategy": name,
            "seed": seed,
            "fitness": fitness,
            "correct_cubes": placement["correct_cubes"],
        })

        print(
            f"Seed {seed}: "
            f"fitness={fitness:.6f}, "
            f"correct cubes={placement['correct_cubes']}"
        )

print("\n--- Mutation Strategy Comparison ---")

for name in strategies:
    runs = [r for r in results if r["strategy"] == name]

    print(f"\n{name}")
    print(
        "Average fitness:",
        np.mean([r["fitness"] for r in runs])
    )
    print(
        "Average correct cubes:",
        np.mean([r["correct_cubes"] for r in runs])
    )
    print(
        "Best fitness:",
        min(r["fitness"] for r in runs)
    )


saved = np.load(
    RESULTS_DIR / "best_iss_mutation.npy"
)

saved_fitness = evaluate_chromosome(saved)
saved_placement = evaluate_cube_placement(saved)

assert np.isclose(saved_fitness, best_fitness)

print("\n--- Saved Best Mutation Solution ---")
print("Best fitness:", saved_fitness)
print("Correct cubes:", saved_placement["correct_cubes"])
print("Successful moves:", saved_placement["successful_moves"])
print("Rejected moves:", saved_placement["rejected_moves"])
print("Verification: PASSED")
