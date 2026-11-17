
import numpy as np

from legal_move_search import generate_legal_chromosome
from random_search import evaluate_chromosome
from hill_climbing import mutate_chromosome


def hybrid_search(num_iterations=100, num_commands=100, num_mutations=10):
    chromosome, attempts = generate_legal_chromosome(
        num_commands=num_commands
    )

    if (len(chromosome) - 1) // 2 != num_commands:
        raise RuntimeError("Could not generate enough legal movements")

    best_chromosome = chromosome.copy()
    best_fitness = evaluate_chromosome(best_chromosome)

    print(f"Initial fitness: {best_fitness:.6f}")
    print(f"Initial generation attempts: {attempts}")

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            best_chromosome,
            num_mutations=num_mutations
        )

        candidate_fitness = evaluate_chromosome(candidate)

        if candidate_fitness < best_fitness:
            best_chromosome = candidate.copy()
            best_fitness = candidate_fitness

            print(
                f"Iteration {iteration + 1}: "
                f"Improved to {best_fitness:.6f}"
            )

    return best_chromosome, best_fitness


if __name__ == "__main__":
    from random_search import evaluate_cube_placement

    np.random.seed(42)

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    placement = evaluate_cube_placement(chromosome)

    print("\n--- Hybrid Search Results ---")
    print("Best fitness:", fitness)
    print("Correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])
