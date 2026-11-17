
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




def evaluate_cube_placement(chromosome):
    import os
    import sys
    from pathlib import Path
    from collections import Counter

    esa_path = (
        Path(__file__).resolve().parent.parent
        / "esa-reference"
        / "Challenge 3 Programmable Cubes"
    )

    if str(esa_path) not in sys.path:
        sys.path.insert(0, str(esa_path))

    original_directory = os.getcwd()

    try:
        os.chdir(esa_path)

        from programmable_cubes_UDP import (
            programmable_cubes_UDP,
            ProgrammableCubes,
        )

        problem = programmable_cubes_UDP("ISS")

        initial_positions = np.load(
            "data/ISS/Initial_Config.npy"
        )

        cubes = ProgrammableCubes(initial_positions)
        steps_needed = cubes.apply_chromosome(chromosome,False)

        correct_cubes = 0

        for cube_type in range(problem.setup["num_cube_types"]):
            target = problem.target_cube_positions[
                problem.target_cube_types == cube_type
            ]

            final = cubes.cube_position[
                problem.initial_cube_types == cube_type
            ]

            target_positions = Counter(map(tuple, target))
            final_positions = Counter(map(tuple, final))

            correct_cubes += sum(
                min(count, final_positions[position])
                for position, count in target_positions.items()
            )

        total_cubes = len(cubes.cube_position)

        return {
            "correct_cubes": correct_cubes,
            "total_cubes": total_cubes,
            "cube_fraction": correct_cubes / total_cubes,
            "steps_needed": steps_needed,
        }

    finally:
        os.chdir(original_directory)





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
    
    np.random.seed(42)
    command_lengths = [10, 100, 500]

    for num_commands in command_lengths:
        print(f"\n--- Testing {num_commands} commands ---")

        best_solution, best_score = random_search(
            num_iterations=5,
            num_commands=num_commands
        )

        print("Best fitness:", best_score)
        print("Best chromosome length:", len(best_solution))

