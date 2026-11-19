
import os
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]

ESA_DIR = (
    ROOT
    / "esa-reference"
    / "Challenge 3 Programmable Cubes"
)

sys.path.insert(0, str(ESA_DIR))

from programmable_cubes_UDP import programmable_cubes_UDP


def evaluate_enterprise(chromosome):
    """
    Evaluate an Enterprise chromosome using ESA's official
    simulator. Lower fitness values are better.

    The original working directory is restored afterward.
    """
    chromosome = np.asarray(chromosome, dtype=int)

    previous_directory = Path.cwd()

    try:
        os.chdir(ESA_DIR)

        problem = programmable_cubes_UDP("Enterprise")

        official_fitness = problem.fitness(chromosome)[0]

        return float(official_fitness)

    finally:
        os.chdir(previous_directory)


if __name__ == "__main__":
    print("Enterprise fitness wrapper ready.")
    print("Heavy fitness evaluations will run on Kaggle.")
