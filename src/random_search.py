
import numpy as np

import os
import sys
from pathlib import Path



def generate_chromosome(num_cubes=148, num_commands=6000):
    chromosome = []

    for _ in range(num_commands):
        cube_id = np.random.randint(0, num_cubes)
        movement = np.random.randint(0, 6)

        chromosome.extend([cube_id, movement])

    chromosome.append(-1)

    return np.array(chromosome)



def evaluate_chromosome(chromosome):
    project_root = Path(__file__).resolve().parent.parent
    esa_path = project_root / "esa-reference" / "Challenge 3 Programmable Cubes"

    # Make ESA's simulator available to Python
    if str(esa_path) not in sys.path:
        sys.path.insert(0, str(esa_path))

    from programmable_cubes_UDP import programmable_cubes_UDP

    # ESA loads scenario files using relative paths
    original_directory = os.getcwd()

    try:
        os.chdir(esa_path)
        simulator = programmable_cubes_UDP("ISS")
        fitness = simulator.fitness(chromosome)[0]
    finally:
        os.chdir(original_directory)

    return fitness



def random_search(num_iterations=5, num_commands=100):
    best_chromosome = None
    best_fitness = float("inf")

    for iteration in range(num_iterations):
        chromosome = generate_chromosome(
            num_cubes=148,
            num_commands=num_commands
        )

        fitness = evaluate_chromosome(chromosome)

        print(f"Iteration {iteration + 1}: Fitness = {fitness:.6f}")

        if fitness < best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome.copy()

    return best_chromosome, best_fitness




if __name__ == "__main__":
    best_solution, best_score = random_search(
        num_iterations=5,
        num_commands=100
    )

    print("\n--- Random Search Results ---")
    print("Best fitness:", best_score)
    print("Best chromosome length:", len(best_solution))


