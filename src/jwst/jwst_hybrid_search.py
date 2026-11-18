
import numpy as np

from jwst_legal_move_search import generate_legal_chromosome
from jwst_hill_climbing import mutate_chromosome
from jwst_fitness import evaluate_jwst
from analyze_movements import analyze_movements


def hybrid_search(
    num_iterations=99,
    num_commands=100,
    num_mutations=10,
):
    chromosome, attempts = generate_legal_chromosome(
        num_commands=num_commands
    )

    best = chromosome.copy()
    best_fitness = evaluate_jwst(best)

    print("Initial fitness:", best_fitness)
    print("Initial generation attempts:", attempts)

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            best,
            num_mutations=num_mutations
        )

        candidate_fitness = evaluate_jwst(candidate)

        if candidate_fitness < best_fitness:
            best = candidate.copy()
            best_fitness = candidate_fitness

            print(
                f"Iteration {iteration + 1}: "
                f"Improved to {best_fitness:.8f}"
            )

    return best, best_fitness


if __name__ == "__main__":
    np.random.seed(42)

    print("--- JWST Hybrid Search ---")

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10,
    )

    successful, rejected = analyze_movements(chromosome)

    print("\n--- Hybrid Search Results ---")
    print("Best fitness:", fitness)
    print("Commands:", (len(chromosome) - 1) // 2)
    print("Successful moves:", successful)
    print("Rejected moves:", rejected)

    assert len(chromosome) == 201
    assert chromosome[-1] == -1
    assert np.isfinite(fitness)
    assert np.isclose(
        fitness,
        evaluate_jwst(chromosome)
    )

    print("JWST Hybrid Search: PASSED")
