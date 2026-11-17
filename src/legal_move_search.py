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

