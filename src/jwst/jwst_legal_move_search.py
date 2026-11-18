
import numpy as np

from analyze_movements import initialize_jwst
from jwst_random_search import NUM_CUBES
from jwst_fitness import evaluate_jwst


def generate_legal_chromosome(
    num_commands=100,
    max_attempts_per_command=100,
):
    cubes = initialize_jwst()

    chromosome = []
    successful = 0
    attempts = 0

    max_attempts = (
        num_commands * max_attempts_per_command
    )

    while (
        successful < num_commands
        and attempts < max_attempts
    ):
        cube_id = np.random.randint(0, NUM_CUBES)
        movement = np.random.randint(0, 6)

        attempts += 1

        result = cubes.apply_single_update_step(
            cube_id, movement
        )

        if result == 1:
            chromosome.extend([cube_id, movement])
            successful += 1

    if successful != num_commands:
        raise RuntimeError(
            "Unable to generate requested legal movements"
        )

    chromosome.append(-1)

    return np.array(chromosome, dtype=int), attempts


if __name__ == "__main__":
    np.random.seed(42)

    print("--- JWST Legal-Move Search ---")

    chromosome, attempts = generate_legal_chromosome(
        num_commands=100
    )

    fitness = evaluate_jwst(chromosome)

    print("Requested commands:", 100)
    print("Generated legal commands:", (len(chromosome) - 1) // 2)
    print("Movement attempts:", attempts)
    print("Generation acceptance rate:", f"{100 / attempts:.1%}")
    print("ESA fitness:", fitness)

    assert len(chromosome) == 201
    assert chromosome[-1] == -1
    assert np.isfinite(fitness)

    print("JWST Legal-Move Search: PASSED")
