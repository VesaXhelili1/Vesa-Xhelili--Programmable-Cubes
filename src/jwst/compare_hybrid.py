
import time

import numpy as np

from jwst_random_search import random_search
from jwst_hill_climbing import hill_climbing
from jwst_hybrid_search import hybrid_search
from analyze_movements import analyze_movements


SEEDS = [10, 20, 30, 40, 50]
EVALUATIONS = 100
COMMANDS = 100

results = {
    "random": [],
    "hill": [],
    "hybrid": [],
}

algorithms = {
    "random": lambda: random_search(
        num_iterations=EVALUATIONS,
        num_commands=COMMANDS,
    ),
    "hill": lambda: hill_climbing(
        num_iterations=EVALUATIONS - 1,
        num_commands=COMMANDS,
        num_mutations=10,
    ),
    "hybrid": lambda: hybrid_search(
        num_iterations=EVALUATIONS - 1,
        num_commands=COMMANDS,
        num_mutations=10,
    ),
}


for seed in SEEDS:
    print(f"\n--- Seed {seed} ---")

    for name, algorithm in algorithms.items():
        np.random.seed(seed)

        start = time.perf_counter()
        chromosome, fitness = algorithm()
        elapsed = time.perf_counter() - start

        successful, rejected = analyze_movements(chromosome)

        results[name].append({
            "fitness": fitness,
            "successful": successful,
            "rejected": rejected,
            "time": elapsed,
        })

        print(
            f"{name}: fitness={fitness:.6f}, "
            f"successful={successful}, "
            f"rejected={rejected}"
        )


print("\n--- JWST Hybrid Comparison ---")

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
        "Average successful movements:",
        np.mean([r["successful"] for r in runs])
    )
    print(
        "Average time:",
        f'{np.mean([r["time"] for r in runs]):.3f}s'
    )
