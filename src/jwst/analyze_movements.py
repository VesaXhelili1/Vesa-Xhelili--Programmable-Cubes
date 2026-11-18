
import sys
from pathlib import Path

import numpy as np

from jwst_random_search import generate_chromosome, NUM_CUBES
from jwst_fitness import evaluate_jwst


ROOT = Path(__file__).resolve().parents[2]
ESA_DIR = ROOT / "esa-reference" / "Challenge 3 Programmable Cubes"

sys.path.insert(0, str(ESA_DIR))

from programmable_cubes_UDP import ProgrammableCubes


def initialize_jwst():
    initial_positions = np.load(
        ESA_DIR / "data" / "JWST" / "Initial_Config.npy"
    )

    return ProgrammableCubes(initial_positions)


def analyze_movements(chromosome):
    cubes = initialize_jwst()

    commands = (len(chromosome) - 1) // 2

    successful = 0
    rejected = 0

    for i in range(commands):
        cube_id = int(chromosome[2 * i])
        movement = int(chromosome[2 * i + 1])

        result = cubes.apply_single_update_step(
            cube_id, movement
        )

        if result == 1:
            successful += 1
        else:
            rejected += 1

    return successful, rejected


if __name__ == "__main__":
    np.random.seed(42)

    print("--- JWST Movement Analysis ---")

    chromosome = generate_chromosome(
        num_commands=100
    )

    successful, rejected = analyze_movements(chromosome)

    print("Total commands:", 100)
    print("Successful movements:", successful)
    print("Rejected movements:", rejected)
    print("Movement success rate:", f"{successful / 100:.1%}")

    fitness = evaluate_jwst(chromosome)

    print("ESA fitness:", fitness)

    assert successful + rejected == 100

    print("JWST movement analysis: PASSED")
