
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from legal_move_search import initialize_cubes
from target_heuristic import (
    load_target_configuration,
    calculate_target_distance,
    calculate_assignment_distance,
)


def test_target_configuration():
    target_positions, target_types, initial_types = (
        load_target_configuration()
    )

    assert target_positions.shape == (148, 3)
    assert target_types.shape == (148,)
    assert initial_types.shape == (148,)

    assert set(np.unique(target_types)) == {0, 1, 2}
    assert set(np.unique(initial_types)) == {0, 1, 2}


def test_distance_heuristics():
    cubes = initialize_cubes()

    nearest_distance = calculate_target_distance(
        cubes.cube_position
    )

    assignment_distance = calculate_assignment_distance(
        cubes.cube_position
    )

    assert nearest_distance == 341
    assert assignment_distance == 478
    assert assignment_distance >= nearest_distance


def test_assignment_distance_with_hybrid():
    from hybrid_search import hybrid_search

    np.random.seed(42)

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    cubes = initialize_cubes()
    cubes.apply_chromosome(chromosome, False)

    final_distance = calculate_assignment_distance(
        cubes.cube_position
    )

    assert final_distance >= 0
    assert np.isfinite(fitness)
