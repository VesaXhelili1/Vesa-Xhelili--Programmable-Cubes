
import time
import numpy as np

from jwst_hybrid_search import hybrid_search
from analyze_movements import analyze_movements


COMMAND_COUNTS = [100, 300, 1000]
SEEDS = [10, 20, 30]
EVALUATIONS = 10

results = []

print("--- JWST Scaling Benchmark ---")

for num_commands in COMMAND_COUNTS:
    print(f"\n--- Commands: {num_commands} ---")

    for seed in SEEDS:
        np.random.seed(seed)

        start = time.perf_counter()

        chromosome, fitness = hybrid_search(
            num_iterations=EVALUATIONS - 1,
            num_commands=num_commands,
            num_mutations=10,
        )

        elapsed = time.perf_counter() - start

        successful, rejected = analyze_movements(
            chromosome
        )

        results.append({
            "commands": num_commands,
            "seed": seed,
            "fitness": float(fitness),
            "time": elapsed,
            "successful": successful,
            "rejected": rejected,
        })

        print(
            f"Seed {seed}: "
            f"fitness={fitness:.6f}, "
            f"time={elapsed:.3f}s, "
            f"successful={successful}, "
            f"rejected={rejected}"
        )


print("\n--- JWST Scaling Summary ---")

for num_commands in COMMAND_COUNTS:
    runs = [
        result
        for result in results
        if result["commands"] == num_commands
    ]

    print(f"\nCommands: {num_commands}")
    print(
        "Average fitness:",
        np.mean([r["fitness"] for r in runs])
    )
    print(
        "Best fitness:",
        min(r["fitness"] for r in runs)
    )
    print(
        "Average execution time:",
        f'{np.mean([r["time"] for r in runs]):.3f}s'
    )
    print(
        "Average successful moves:",
        np.mean([r["successful"] for r in runs])
    )


