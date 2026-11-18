
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ESA_DIR = ROOT / "esa-reference" / "Challenge 3 Programmable Cubes"

sys.path.insert(0, str(ESA_DIR))

from programmable_cubes_UDP import programmable_cubes_UDP


def evaluate_jwst(chromosome):
    original_directory = Path.cwd()

    try:
        os.chdir(ESA_DIR)

        problem = programmable_cubes_UDP("JWST")
        fitness = problem.fitness(chromosome)[0]

        return float(fitness)

    finally:
        os.chdir(original_directory)


if __name__ == "__main__":
    print("--- JWST Fitness Test ---")

    # One movement command followed by the
    # required chromosome termination marker.
    chromosome = np.array([0, 0, -1], dtype=int)

    print("Chromosome:", chromosome)
    print("Commands:", (len(chromosome) - 1) // 2)

    fitness = evaluate_jwst(chromosome)

    print("JWST fitness:", fitness)

    assert np.isfinite(fitness)

    print("JWST fitness evaluation: PASSED")
