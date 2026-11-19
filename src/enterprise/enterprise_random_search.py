
import numpy as np

from enterprise_fitness import evaluate_enterprise


NUM_CUBES = 1472
NUM_MOVES = 6
MAX_COMMANDS = 100000


def generate_chromosome(num_commands=100, rng=None):
    """Generate a random Enterprise movement sequence."""

    if not 1 <= num_commands <= MAX_COMMANDS:
        raise ValueError("Invalid number of commands")

    if rng is None:
        rng = np.random.default_rng()

    chromosome = np.empty(
        2 * num_commands + 1,
        dtype=np.int64,
    )

    chromosome[0:-1:2] = rng.integers(
        0, NUM_CUBES, size=num_commands
    )

    chromosome[1:-1:2] = rng.integers(
        0, NUM_MOVES, size=num_commands
    )

    chromosome[-1] = -1

    return chromosome


def random_search(
    num_iterations=100,
    num_commands=100,
    seed=42,
):
    """Evaluate random chromosomes and retain the best."""

    if num_iterations < 1:
        raise ValueError("Iterations must be positive")

    rng = np.random.default_rng(seed)

    best_chromosome = None
    best_fitness = float("inf")

    for iteration in range(num_iterations):
        chromosome = generate_chromosome(
            num_commands=num_commands,
            rng=rng,
        )

        fitness = float(evaluate_enterprise(chromosome))

        if fitness < best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome.copy()

            print(
                f"Iteration {iteration + 1}: "
                f"Best fitness = {best_fitness:.9f}"
            )

    return best_chromosome, best_fitness
