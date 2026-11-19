
import sys
from pathlib import Path

import numpy as np

from enterprise_random_search import (
    NUM_CUBES,
    NUM_MOVES,
    MAX_COMMANDS,
)


ROOT = Path(__file__).resolve().parents[2]
ESA_DIR = (
    ROOT / "esa-reference" /
    "Challenge 3 Programmable Cubes"
)

sys.path.insert(0, str(ESA_DIR))

from programmable_cubes_UDP import ProgrammableCubes


def initialize_enterprise():
    """Initialize Enterprise cubes from ESA's configuration."""

    positions = np.load(
        ESA_DIR / "data" / "Enterprise" / "Initial_Config.npy",
        allow_pickle=False,
    )

    return ProgrammableCubes(positions)


def generate_legal_chromosome(
    num_commands=100,
    max_attempts_per_command=100,
    rng=None,
):
    """
    Generate a sequence containing accepted movements only.

    The simulator updates its state after each legal movement.
    """

    if not 1 <= num_commands <= MAX_COMMANDS:
        raise ValueError("Invalid command count")

    if max_attempts_per_command < 1:
        raise ValueError("Attempt limit must be positive")

    if rng is None:
        rng = np.random.default_rng()

    cubes = initialize_enterprise()

    chromosome = []
    attempts = 0

    max_attempts = (
        num_commands * max_attempts_per_command
    )

    while (
        len(chromosome) // 2 < num_commands
        and attempts < max_attempts
    ):
        cube_id = int(rng.integers(0, NUM_CUBES))
        movement = int(rng.integers(0, NUM_MOVES))

        attempts += 1

        accepted = cubes.apply_single_update_step(
            cube_id,
            movement,
        )

        if accepted == 1:
            chromosome.extend([cube_id, movement])

    if len(chromosome) // 2 != num_commands:
        raise RuntimeError(
            "Unable to generate the requested number "
            "of legal movements"
        )

    chromosome.append(-1)

    return np.array(chromosome, dtype=np.int64), attempts


def analyze_movements(chromosome):
    """Count accepted and rejected movements."""

    cubes = initialize_enterprise()

    successful = 0
    rejected = 0

    num_commands = (len(chromosome) - 1) // 2

    for index in range(num_commands):
        cube_id = int(chromosome[index * 2])
        movement = int(chromosome[index * 2 + 1])

        accepted = cubes.apply_single_update_step(
            cube_id,
            movement,
        )

        if accepted == 1:
            successful += 1
        else:
            rejected += 1

    return successful, rejected
