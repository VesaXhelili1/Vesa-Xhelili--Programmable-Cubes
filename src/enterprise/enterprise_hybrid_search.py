
import numpy as np

from enterprise_fitness import evaluate_enterprise
from enterprise_hill_climbing import mutate_chromosome
from enterprise_legal_move_search import generate_legal_chromosome


def hybrid_search(
    num_iterations=100,
    num_commands=100,
    num_mutations=10,
    seed=42,
):
    """
    Combine legal movement generation with Hill Climbing.

    Lower ESA fitness is better.
    """

    if num_iterations < 1:
        raise ValueError("Iterations must be positive")

    if not 1 <= num_mutations <= num_commands:
        raise ValueError("Invalid mutation count")

    rng = np.random.default_rng(seed)

    # Generate an initial chromosome containing legal moves.
    current, attempts = generate_legal_chromosome(
        num_commands=num_commands,
        rng=rng,
    )

    current_fitness = float(evaluate_enterprise(current))

    best = current.copy()
    best_fitness = current_fitness

    print("Initial fitness:", best_fitness)
    print("Initial generation attempts:", attempts)

    # Iteratively improve the initial solution.
    for iteration in range(1, num_iterations):
        candidate = mutate_chromosome(
            current,
            num_mutations=num_mutations,
            rng=rng,
        )

        candidate_fitness = float(
            evaluate_enterprise(candidate)
        )

        if candidate_fitness < current_fitness:
            current = candidate.copy()
            current_fitness = candidate_fitness

            best = current.copy()
            best_fitness = current_fitness

            print(
                f"Iteration {iteration}: "
                f"Improved to {best_fitness:.9f}"
            )

    return best, best_fitness
