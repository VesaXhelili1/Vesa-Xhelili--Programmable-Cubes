
import time

import numpy as np

from jwst_random_search import random_search
from jwst_hill_climbing import hill_climbing


SEEDS = [10, 20, 30, 40, 50]
EVALUATIONS = 100
COMMANDS = 20

results = {
    "random": [],
    "hill": [],
}

for seed in SEEDS:
    print(f"\n--- Seed {seed} ---")

    np.random.seed(seed)
    start = time.perf_counter()

    _, random_fitness = random_search(
        num_iterations=EVALUATIONS,
        num_commands=COMMANDS,
    )

    random_time = time.perf_counter() - start

    np.random.seed(seed)
    start = time.perf_counter()

    _, hill_fitness = hill_climbing(
        num_iterations=EVALUATIONS - 1,
        num_commands=COMMANDS,
        num_mutations=2,
    )

    hill_time = time.perf_counter() - start

    results["random"].append({
        "fitness": random_fitness,
        "time": random_time,
    })

    results["hill"].append({
        "fitness": hill_fitness,
        "time": hill_time,
    })

print("\n--- JWST Algorithm Comparison ---")

for name, runs in results.items():
    print(f"\n{name}")
    print(
        "Average fitness:",
        np.mean([r["fitness"] for r in runs])
    )
    print(
        "Best fitness:",
        min(r["fitness"] for r in runs)
    )
    print(
        "Average time:",
        f'{np.mean([r["time"] for r in runs]):.3f}s'
    )
