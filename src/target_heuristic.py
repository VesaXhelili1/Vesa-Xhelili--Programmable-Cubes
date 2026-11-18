
import os
import sys
from pathlib import Path

import numpy as np


def load_target_configuration():
    project_root = Path(__file__).resolve().parent.parent

    esa_path = (
        project_root
        / "esa-reference"
        / "Challenge 3 Programmable Cubes"
    )

    original_directory = os.getcwd()

    try:
        os.chdir(esa_path)

        target_positions = np.load(
            "data/ISS/Target_Config.npy"
        )

        target_types = np.load(
            "data/ISS/Target_Cube_Types.npy"
        )

        initial_types = np.load(
            "data/ISS/Initial_Cube_Types.npy"
        )

    finally:
        os.chdir(original_directory)

    return target_positions, target_types, initial_types


def calculate_target_distance(cube_positions):
    target_positions, target_types, initial_types = (
        load_target_configuration()
    )

    total_distance = 0

    for cube_id, position in enumerate(cube_positions):
        cube_type = initial_types[cube_id]

        matching_targets = target_positions[
            target_types == cube_type
        ]

        distances = np.sum(
            np.abs(matching_targets - position),
            axis=1
        )

        total_distance += np.min(distances)

    return int(total_distance)


def calculate_assignment_distance(cube_positions):
    from scipy.optimize import linear_sum_assignment

    target_positions, target_types, initial_types = (
        load_target_configuration()
    )

    total_distance = 0

    for cube_type in np.unique(initial_types):
        current = cube_positions[
            initial_types == cube_type
        ]

        targets = target_positions[
            target_types == cube_type
        ]

        if len(current) != len(targets):
            raise ValueError(
                "Mismatch between current and target cube counts"
            )

        cost_matrix = np.sum(
            np.abs(current[:, None, :] - targets[None, :, :]),
            axis=2
        )

        row_indices, col_indices = linear_sum_assignment(
            cost_matrix
        )

        total_distance += cost_matrix[
            row_indices,
            col_indices
        ].sum()

    return int(total_distance)


if __name__ == "__main__":
    from legal_move_search import initialize_cubes

    cubes = initialize_cubes()

    distance = calculate_target_distance(
        cubes.cube_position
    )

    print("--- Target Distance Test ---")
    print("Initial target distance:", distance)

    assert distance >= 0
    print("Target distance calculation: PASSED")




    from hybrid_search import hybrid_search
    from random_search import evaluate_cube_placement

    print("\n--- Hybrid Search Target Distance Test ---")

    np.random.seed(42)

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    final_cubes = initialize_cubes()
    final_cubes.apply_chromosome(chromosome, False)

    final_distance = calculate_target_distance(
        final_cubes.cube_position
    )

    placement = evaluate_cube_placement(chromosome)

    print("\n--- Distance Comparison ---")
    print("Initial distance:", distance)
    print("Hybrid final distance:", final_distance)
    print("Distance improvement:", distance - final_distance)
    print("Correct cubes:", placement["correct_cubes"])
    print("ESA fitness:", fitness)

    print("\n--- Assignment Distance Test ---")

    cubes = initialize_cubes()

    nearest_distance = calculate_target_distance(
        cubes.cube_position
    )

    assignment_distance = calculate_assignment_distance(
        cubes.cube_position
    )

    print("Nearest-target distance:", nearest_distance)
    print("Assignment distance:", assignment_distance)

    assert assignment_distance >= nearest_distance

    print("Assignment distance calculation: PASSED")


    print("\n--- Hybrid Assignment Distance Comparison ---")

    np.random.seed(42)

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    final_cubes = initialize_cubes()
    final_cubes.apply_chromosome(chromosome, False)

    initial_assignment = calculate_assignment_distance(
        cubes.cube_position
    )

    final_assignment = calculate_assignment_distance(
        final_cubes.cube_position
    )

    print("Initial assignment distance:", initial_assignment)
    print("Final assignment distance:", final_assignment)
    print("Assignment distance improvement:", initial_assignment - final_assignment)
    print("ESA fitness:", fitness)

