
import numpy as np

from enterprise_fitness import evaluate_enterprise
from enterprise_random_search import (
    generate_chromosome,
    NUM_CUBES,
    NUM_MOVES,
)


def mutate_chromosome(chromosome, num_mutations=2, rng=None):
    """Change selected movement commands in a chromosome."""

    if rng is None:
        rng = np.random.default_rng()

    candidate = chromosome.copy()
    num_commands = (len(candidate) - 1) // 2

    if not 1 <= num_mutations <= num_commands:
        raise ValueError("Invalid number of mutations")

    positions = rng.choice(
        num_commands,
        size=num_mutations,
        replace=False,
    )

    for position in positions:
        index = 2 * position

        if rng.random() < 0.5:
            old = int(candidate[index])
            new = int(rng.integers(0, NUM_CUBES - 1))

            if new >= old:
                new += 1

            candidate[index] = new
        else:
            old = int(candidate[index + 1])
            new = int(rng.integers(0, NUM_MOVES - 1))

            if new >= old:
                new += 1

            candidate[index + 1] = new

    return candidate


def hill_climbing(
    num_iterations=100,
    num_commands=100,
    num_mutations=2,
    seed=42,
):
    """Improve a random chromosome through greedy mutations."""

    if num_iterations < 1:
        raise ValueError("Iterations must be positive")

    rng = np.random.default_rng(seed)

    current = generate_chromosome(num_commands, rng)
    current_fitness = float(evaluate_enterprise(current))

    best = current.copy()
    best_fitness = current_fitness

    print("Initial fitness:", best_fitness)

    for iteration in range(1, num_iterations):
        candidate = mutate_chromosome(
            current,
            num_mutations,
            rng,
        )

        fitness = float(evaluate_enterprise(candidate))

        if fitness < current_fitness:
            current = candidate.copy()
            current_fitness = fitness

            best = current.copy()
            best_fitness = fitness

            print(
                f"Iteration {iteration}: "
                f"Improved to {best_fitness:.9f}"
            )

    return best, best_fitness
