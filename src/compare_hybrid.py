
import time
import numpy as np

from hill_climbing import hill_climbing
from hybrid_search import hybrid_search
from random_search import evaluate_cube_placement


seeds = [10, 20, 30, 40, 50]

results = {
    "hill": [],
    "hybrid": [],
}

for seed in seeds:
    print(f"\n--- Seed {seed} ---")

    np.random.seed(seed)
    start = time.perf_counter()

    hill_chromosome, hill_fitness = hill_climbing(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    hill_time = time.perf_counter() - start

    np.random.seed(seed)
    start = time.perf_counter()

    hybrid_chromosome, hybrid_fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    hybrid_time = time.perf_counter() - start

    for name, chromosome, fitness, elapsed in [
        ("hill", hill_chromosome, hill_fitness, hill_time),
        ("hybrid", hybrid_chromosome, hybrid_fitness, hybrid_time),
    ]:
        placement = evaluate_cube_placement(chromosome)

        results[name].append({
            "fitness": fitness,
            "correct_cubes": placement["correct_cubes"],
            "success_rate": placement["success_rate"],
            "time": elapsed,
        })

        print(
            f"{name}: fitness={fitness:.6f}, "
            f"correct cubes={placement['correct_cubes']}, "
            f"success rate={placement['success_rate']:.1%}, "
            f"time={elapsed:.3f}s"
        )


print("\n--- Final Comparison ---")

for name, runs in results.items():
    print(f"\n{name}")
    print("Average fitness:", np.mean([r["fitness"] for r in runs]))
    print("Average correct cubes:", np.mean([r["correct_cubes"] for r in runs]))
    print("Average success rate:", f'{np.mean([r["success_rate"] for r in runs]):.1%}')
    print("Average time:", f'{np.mean([r["time"] for r in runs]):.3f}s')
