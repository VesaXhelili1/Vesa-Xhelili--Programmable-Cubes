import os
import sys
from pathlib import Path

import numpy as np

from random_search import (
    try_legal_move,
    evaluate_cube_placement,
    evaluate_chromosome,
)



def initialize_cubes():
    project_root = Path(__file__).resolve().parent.parent

    esa_path = (
        project_root
        / "esa-reference"
        / "Challenge 3 Programmable Cubes"
    )

    if str(esa_path) not in sys.path:
        sys.path.insert(0, str(esa_path))

    from programmable_cubes_UDP import ProgrammableCubes

    original_directory = os.getcwd()

    try:
        os.chdir(esa_path)

        initial_positions = np.load(
            "data/ISS/Initial_Config.npy"
        )

        cubes = ProgrammableCubes(initial_positions)

    finally:
        os.chdir(original_directory)

    return cubes





def generate_legal_chromosome(num_commands=100):
    cubes = initialize_cubes()
    num_cubes = len(cubes.cube_position)

    chromosome = []
    successful_moves = 0
    attempts = 0
    max_attempts = num_commands * 100

    while successful_moves < num_commands and attempts < max_attempts:
        cube_id = np.random.randint(0, num_cubes)
        move = np.random.randint(0, 6)

        attempts += 1

        if try_legal_move(cubes, cube_id, move):
            chromosome.extend([cube_id, move])
            successful_moves += 1

    chromosome.append(-1)

    assert successful_moves <= num_commands

    return np.array(chromosome), attempts


def legal_move_search(num_iterations=30, num_commands=100):
    best_chromosome = None
    best_fitness = float("inf")

    for iteration in range(num_iterations):
        chromosome, attempts = generate_legal_chromosome(
            num_commands=num_commands
        )

        commands_generated = (len(chromosome) - 1) // 2

        if commands_generated != num_commands:
            print(f"Iteration {iteration + 1}: Incomplete chromosome")
            continue

        fitness = evaluate_chromosome(chromosome)

        if fitness < best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome.copy()

            print(
                f"Iteration {iteration + 1}: "
                f"Improved fitness to {best_fitness:.6f}"
            )

    return best_chromosome, best_fitness



if __name__ == "__main__":
    cubes = initialize_cubes()

    print("--- ESA Cube Initialization Test ---")
    print("Total cubes:", len(cubes.cube_position))
    print("Cube positions shape:", cubes.cube_position.shape)
    print("Neighbour lists:", len(cubes.cube_neighbours))
    print("Surroundings lists:", len(cubes.cube_surroundings))


    print("\n--- Legal Chromosome Generation Test ---")

    np.random.seed(42)

    chromosome, attempts = generate_legal_chromosome(
        num_commands=100
    )

    print("Commands generated:", (len(chromosome) - 1) // 2)
    print("Attempts needed:", attempts)
    print("Chromosome ends with -1:", chromosome[-1] == -1)


    print("\n--- Legal Movement Replay Test ---")

    result = evaluate_cube_placement(chromosome)

    print("Commands attempted:", result["steps_needed"])
    print("Successful moves:", result["successful_moves"])
    print("Rejected moves:", result["rejected_moves"])
    print("Correct cubes:", result["correct_cubes"])

    assert result["rejected_moves"] == 0
    assert result["successful_moves"] == 100

    print("Legal movement replay: PASSED")

    fitness = evaluate_chromosome(chromosome)
    print("Legal chromosome fitness:", fitness)



    print("\n--- Improved Legal-Move Search Test ---")

    np.random.seed(42)

    best_chromosome, best_fitness = legal_move_search(
        num_iterations=30,
        num_commands=100
    )

    assert best_chromosome is not None

    placement = evaluate_cube_placement(best_chromosome)

    print("\n--- Best Solution ---")
    print("Best fitness:", best_fitness)
    print("Correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])

    assert placement["successful_moves"] == 100
    assert placement["rejected_moves"] == 0

    print("Improved Legal-Move Search: PASSED")



    print("\n--- Target Configuration Inspection ---")

    project_root = Path(__file__).resolve().parent.parent
    esa_path = project_root / "esa-reference" / "Challenge 3 Programmable Cubes"

    original_directory = os.getcwd()

    try:
        os.chdir(esa_path)

        target_positions = np.load("data/ISS/Target_Config.npy")
        target_types = np.load("data/ISS/Target_Cube_Types.npy")
        initial_types = np.load("data/ISS/Initial_Cube_Types.npy")

    finally:
        os.chdir(original_directory)

    print("Target positions shape:", target_positions.shape)
    print("Target types shape:", target_types.shape)
    print("Initial types shape:", initial_types.shape)
    print("Unique target cube types:", np.unique(target_types))
    print("Unique initial cube types:", np.unique(initial_types))

