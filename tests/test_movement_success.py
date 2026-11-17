
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from random_search import (
    generate_chromosome,
    evaluate_cube_placement,
    try_legal_move,
)


def test_movement_success():
    np.random.seed(42)

    chromosome = generate_chromosome(
        num_cubes=148,
        num_commands=100
    )

    result = evaluate_cube_placement(chromosome)

    assert result["steps_needed"] == 100

    assert (
        result["successful_moves"] + result["rejected_moves"]
        == result["steps_needed"]
    )

    assert 0 <= result["success_rate"] <= 1

    print("Movement counter validation: PASSED")


class FakeCubes:
    def apply_single_update_step(self, cube_id, move, verbose=False):
        return 1 if move == 0 else 0


def test_legal_move_function():
    fake_cubes = FakeCubes()

    assert try_legal_move(fake_cubes, 0, 0) is True
    assert try_legal_move(fake_cubes, 0, 1) is False

    print("Legal move function: PASSED")
