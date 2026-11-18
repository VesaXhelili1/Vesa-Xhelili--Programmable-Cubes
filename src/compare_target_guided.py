
import time
import numpy as np

from hybrid_search import hybrid_search
from target_guided_hybrid import target_guided_hybrid
from random_search import evaluate_cube_placement


seeds = [10, 20, 30, 40, 50]

results = {
    "hybrid": [],
    "target_guided": [],
}

for seed in seeds:
    print(f"\n--- Seed {seed} ---")

    # Standard Hybrid Search
    np.random.seed(seed)
    start = time.perf_counter()

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    elapsed = time.perf_counter() - start
    placement = evaluate_cube_placement(chromosome)

    results["hybrid"].append({
        "fitness": fitness,
        "cubes": placement["correct_cubes"],
        "time": elapsed,
    })

    # Target-Guided Hybrid Search
    np.random.seed(seed)
    start = time.perf_counter()

    chromosome, fitness, distance = target_guided_hybrid(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    elapsed = time.perf_counter() - start
    placement = evaluate_cube_placement(chromosome)

    results["target_guided"].append({
        "fitness": fitness,
        "cubes": placement["correct_cubes"],
        "distance": distance,
        "time": elapsed,
    })


print("\n--- Final Comparison ---")

for name, runs in results.items():
    print(f"\n{name}")
    print("Average fitness:",
          np.mean([r["fitness"] for r in runs]))
    print("Average correct cubes:",
          np.mean([r["cubes"] for r in runs]))
    print("Average time:",
          f'{np.mean([r["time"] for r in runs]):.3f}s')

    if name == "target_guided":
        print("Average target distance:",
              np.mean([r["distance"] for r in runs]))
