
import time

import numpy as np

from jwst_random_search import generate_chromosome
from jwst_legal_move_search import generate_legal_chromosome
from analyze_movements import analyze_movements
from jwst_fitness import evaluate_jwst


SEEDS = [10, 20, 30, 40, 50]
EVALUATIONS = 20
COMMANDS = 100

results = {
    "random": [],
    "legal": [],
}


for seed in SEEDS:
    print(f"\n--- Seed {seed} ---")

    for method in ("random", "legal"):
        np.random.seed(seed)

        start = time.perf_counter()

        best_fitness = float("inf")
        best_chromosome = None

        for _ in range(EVALUATIONS):
            if method == "random":
                chromosome = generate_chromosome(COMMANDS)
            else:
                chromosome, _ = generate_legal_chromosome(
                    num_commands=COMMANDS
                )

            fitness = evaluate_jwst(chromosome)

            if fitness < best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome.copy()

        elapsed = time.perf_counter() - start

        successful, rejected = analyze_movements(
            best_chromosome
        )

        if method == "legal":
            assert rejected == 0

        results[method].append({
            "fitness": best_fitness,
            "successful": successful,
            "rejected": rejected,
            "time": elapsed,
        })

        print(
            f"{method}: fitness={best_fitness:.6f}, "
            f"successful={successful}, "
            f"rejected={rejected}"
        )


print("\n--- JWST Legal-Move Comparison ---")

for method, runs in results.items():
    print(f"\n{method}")
    print(
        "Average fitness:",
        np.mean([r["fitness"] for r in runs])
    )
    print(
        "Average successful movements:",
        np.mean([r["successful"] for r in runs])
    )
    print(
        "Average rejected movements:",
        np.mean([r["rejected"] for r in runs])
    )
    print(
        "Average time:",
        f'{np.mean([r["time"] for r in runs]):.3f}s'
    )
