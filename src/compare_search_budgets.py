
import time

import numpy as np

from random_search import random_search, evaluate_cube_placement
from hill_climbing import hill_climbing
from legal_move_search import legal_move_search


seeds = [10, 20, 30, 40, 50]
budgets = [10, 30, 100]

results = []

for budget in budgets:
    print(f"\n===== Budget: {budget} evaluations =====")

    for seed in seeds:
        algorithms = [
            ("Random Search", random_search, {
                "num_iterations": budget,
                "num_commands": 100,
            }),
            ("Hill Climbing", hill_climbing, {
                "num_iterations": budget - 1,
                "num_commands": 100,
                "num_mutations": 10,
            }),
            ("Improved Legal-Move", legal_move_search, {
                "num_iterations": budget,
                "num_commands": 100,
            }),
        ]

        for name, algorithm, parameters in algorithms:
            np.random.seed(seed)

            start = time.perf_counter()
            chromosome, fitness = algorithm(**parameters)
            elapsed = time.perf_counter() - start

            if chromosome is None:
                print(f"{name}: No complete solution")
                continue

            placement = evaluate_cube_placement(chromosome)

            results.append({
                "budget": budget,
                "seed": seed,
                "algorithm": name,
                "fitness": fitness,
                "correct_cubes": placement["correct_cubes"],
                "time": elapsed,
            })


print("\n===== Summary =====")

for budget in budgets:
    print(f"\nBudget: {budget}")

    for name in ["Random Search", "Hill Climbing", "Improved Legal-Move"]:
        subset = [
            r for r in results
            if r["budget"] == budget and r["algorithm"] == name
        ]

        if not subset:
            continue

        print(
            f"{name}: "
            f"fitness={np.mean([r['fitness'] for r in subset]):.6f}, "
            f"cubes={np.mean([r['correct_cubes'] for r in subset]):.1f}, "
            f"time={np.mean([r['time'] for r in subset]):.3f}s"
        )
