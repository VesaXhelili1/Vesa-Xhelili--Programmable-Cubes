
import sys
from pathlib import Path
import io
from contextlib import redirect_stdout

import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from random_search import (
    random_search,
    generate_chromosome,
    evaluate_chromosome,
)


def test_random_search_validation():
    np.random.seed(42)

    with redirect_stdout(io.StringIO()):
        best_chromosome, best_fitness = random_search(
            num_iterations=100,
            num_commands=100
        )

    # Check the chromosome format
    assert len(best_chromosome) == 201
    assert best_chromosome[-1] == -1

    # Check that returned fitness matches ESA's evaluator
    actual_fitness = evaluate_chromosome(best_chromosome)

    assert np.isclose(best_fitness, actual_fitness)

    print("Random Search validation: PASSED")


def test_best_solution_selection():
    np.random.seed(42)

    with redirect_stdout(io.StringIO()):
        best_chromosome, best_fitness = random_search(
            num_iterations=100,
            num_commands=100
        )

    # Independently reproduce all 100 candidates
    np.random.seed(42)

    all_fitness_values = []

    for _ in range(100):
        chromosome = generate_chromosome(
            num_cubes=148,
            num_commands=100
        )

        fitness = evaluate_chromosome(chromosome)
        all_fitness_values.append(fitness)

    expected_best = min(all_fitness_values)

    assert np.isclose(best_fitness, expected_best)

    print("Best solution selection: PASSED")
