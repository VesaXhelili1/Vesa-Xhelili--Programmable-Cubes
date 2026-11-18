
import numpy as np

from jwst_fitness import evaluate_jwst
from jwst_random_search import (
    generate_chromosome,
    NUM_CUBES,
    MAX_COMMANDS,
)


def mutate_chromosome(chromosome, num_mutations=2):
    candidate = chromosome.copy()

    num_commands = (len(candidate) - 1) // 2

    if not 1 <= num_mutations <= num_commands:
        raise ValueError("Invalid number of mutations")

    positions = np.random.choice(
        num_commands,
        size=num_mutations,
        replace=False,
    )

    for position in positions:
        if np.random.rand() < 0.5:
            candidate[2 * position] = np.random.randint(
                0, NUM_CUBES
            )
        else:
            candidate[2 * position + 1] = np.random.randint(
                0, 6
            )

    return candidate


def hill_climbing(
    num_iterations=99,
    num_commands=20,
    num_mutations=2,
):
    if not 1 <= num_commands <= MAX_COMMANDS:
        raise ValueError("Invalid number of commands")

    best = generate_chromosome(num_commands)
    best_fitness = evaluate_jwst(best)

    print("Initial fitness:", best_fitness)

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            best,
            num_mutations=num_mutations,
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

    print("--- JWST Hill Climbing ---")

    chromosome, fitness = hill_climbing(
        num_iterations=99,
        num_commands=20,
        num_mutations=2,
    )

    print("\n--- Results ---")
    print("Best fitness:", fitness)
    print("Commands:", (len(chromosome) - 1) // 2)
    print("Chromosome length:", len(chromosome))

    assert len(chromosome) == 41
    assert chromosome[-1] == -1
    assert np.isfinite(fitness)
    assert np.isclose(fitness, evaluate_jwst(chromosome))

    print("JWST Hill Climbing: PASSED")
