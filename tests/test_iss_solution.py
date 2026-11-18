
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
)
from legal_move_search import initialize_cubes

BEST_SOLUTION = ROOT / "results" / "best_iss_mutation.npy"

def test_saved_chromosome_format():
    chromosome = np.load(BEST_SOLUTION)

    assert chromosome.shape == (201,)
    assert chromosome[-1] == -1
    assert np.all(
        (chromosome[0:-1:2] >= 0)
        & (chromosome[0:-1:2] < 148)
    )
    assert np.all(
        (chromosome[1:-1:2] >= 0)
        & (chromosome[1:-1:2] < 6)
    )

def test_saved_chromosome_fitness():
    chromosome = np.load(BEST_SOLUTION)

    fitness = evaluate_chromosome(chromosome)

    assert np.isfinite(fitness)
    assert np.isclose(
        fitness,
        -0.10099941211052317,
        atol=1e-10,
    )

def test_saved_chromosome_placement():
    chromosome = np.load(BEST_SOLUTION)

    placement = evaluate_cube_placement(chromosome)

    assert placement["correct_cubes"] == 35
    assert placement["total_cubes"] == 148

    assert (
        placement["successful_moves"]
        + placement["rejected_moves"]
        == 100
    )

def test_saved_chromosome_replay():
    chromosome = np.load(BEST_SOLUTION)

    first = initialize_cubes()
    second = initialize_cubes()

    first.apply_chromosome(chromosome, False)
    second.apply_chromosome(chromosome, False)

    np.testing.assert_array_equal(
        first.cube_position,
        second.cube_position,
    )