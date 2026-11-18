
import json
from pathlib import Path

import numpy as np

from jwst_fitness import evaluate_jwst


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = (
    ROOT
    / "esa-reference"
    / "Challenge 3 Programmable Cubes"
    / "problems"
    / "JWST.json"
)

with open(CONFIG_PATH) as file:
    CONFIG = json.load(file)

NUM_CUBES = CONFIG["num_cubes"]
MAX_COMMANDS = CONFIG["max_cmds"]


def generate_chromosome(num_commands=20):
    if not 1 <= num_commands <= MAX_COMMANDS:
        raise ValueError("Invalid number of commands")

    cube_ids = np.random.randint(
        0, NUM_CUBES, size=num_commands
    )

    movements = np.random.randint(
        0, 6, size=num_commands
    )

    chromosome = np.empty(
        2 * num_commands + 1,
        dtype=int
    )

    chromosome[0:-1:2] = cube_ids
    chromosome[1:-1:2] = movements
    chromosome[-1] = -1

    return chromosome


def random_search(num_iterations=10, num_commands=20):
    if num_iterations < 1:
        raise ValueError("Iterations must be positive")

    best_chromosome = None
    best_fitness = float("inf")

    for iteration in range(num_iterations):
        chromosome = generate_chromosome(num_commands)

        fitness = evaluate_jwst(chromosome)

        if fitness < best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome.copy()

            print(
                f"Iteration {iteration + 1}: "
                f"Best fitness = {best_fitness:.8f}"
            )

    return best_chromosome, best_fitness


if __name__ == "__main__":
    np.random.seed(42)

    print("--- JWST Random Search ---")

    chromosome, fitness = random_search(
        num_iterations=10,
        num_commands=20
    )

    print("\n--- Results ---")
    print("Number of cubes:", NUM_CUBES)
    print("Commands:", (len(chromosome) - 1) // 2)
    print("Best fitness:", fitness)
    print("Chromosome length:", len(chromosome))

    assert len(chromosome) == 41
    assert chromosome[-1] == -1
    assert np.isfinite(fitness)

    print("JWST Random Search: PASSED")
