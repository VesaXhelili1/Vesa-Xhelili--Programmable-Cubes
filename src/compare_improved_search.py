
import time
import numpy as np

from random_search import (
    random_search,
    evaluate_cube_placement,
)
from hill_climbing import hill_climbing
from legal_move_search import legal_move_search


seeds = [10, 20, 30, 40, 50]

results = {
    "random": [],
    "hill": [],
    "legal": [],
}

for seed in seeds:
    print(f"\n--- Seed {seed} ---")

    np.random.seed(seed)
    start = time.perf_counter()

    random_chromosome, random_fitness = random_search(
        num_iterations=30,
        num_commands=100,
    )

    random_time = time.perf_counter() - start

    np.random.seed(seed)
    start = time.perf_counter()

    hill_chromosome, hill_fitness = hill_climbing(
        num_iterations=29,
        num_commands=100,
        num_mutations=10,
    )

    hill_time = time.perf_counter() - start

    np.random.seed(seed)
    start = time.perf_counter()

    legal_chromosome, legal_fitness = legal_move_search(
        num_iterations=30,
        num_commands=100,
    )

    legal_time = time.perf_counter() - start

    experiments = [
        ("random", random_chromosome, random_fitness, random_time),
        ("hill", hill_chromosome, hill_fitness, hill_time),
        ("legal", legal_chromosome, legal_fitness, legal_time),
    ]

    for name, chromosome, fitness, elapsed in experiments:
        if chromosome is None:
            print(f"{name}: No complete solution found")
            continue

        placement = evaluate_cube_placement(chromosome)

        results[name].append({
            "fitness": fitness,
            "correct_cubes": placement["correct_cubes"],
            "time": elapsed,
        })

        print(
            f"{name}: fitness={fitness:.6f}, "
            f"correct cubes={placement['correct_cubes']}, "
            f"time={elapsed:.3f}s"
        )


print("\n--- Final Averages ---")

for name, runs in results.items():
    if not runs:
        print(f"{name}: No completed experiments")
        continue

    print(f"\n{name}")
    print("Average fitness:", np.mean([r["fitness"] for r in runs]))
    print("Average correct cubes:", np.mean([r["correct_cubes"] for r in runs]))
    print("Average time:", f'{np.mean([r["time"] for r in runs]):.3f}s')
    print("Completed runs:", len(runs))
