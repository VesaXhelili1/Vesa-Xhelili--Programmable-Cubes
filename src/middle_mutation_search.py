
from pathlib import Path

import numpy as np

from legal_move_search import initialize_cubes
from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
    try_legal_move,
)


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def mutate_middle(chromosome):
    num_commands = (len(chromosome) - 1) // 2

    # Choose an earlier point in the command sequence.
    cut = np.random.randint(30, 81)

    prefix = chromosome[:cut * 2].tolist()

    cubes = initialize_cubes()
    cubes.apply_chromosome(
        np.array(prefix + [-1], dtype=int),
        False
    )

    new_commands = prefix.copy()
    remaining = num_commands - cut
    successful = 0
    attempts = 0
    max_attempts = remaining * 100

    while successful < remaining and attempts < max_attempts:
        cube_id = np.random.randint(0, 148)
        move = np.random.randint(0, 6)
        attempts += 1

        if try_legal_move(cubes, cube_id, move):
            new_commands.extend([cube_id, move])
            successful += 1

    if successful != remaining:
        return None

    return np.array(new_commands + [-1], dtype=int)


def middle_mutation_search(initial_chromosome, iterations=299):
    best = initial_chromosome.copy()
    best_fitness = evaluate_chromosome(best)

    print("Starting fitness:", best_fitness)

    for iteration in range(iterations):
        candidate = mutate_middle(best)

        if candidate is None:
            continue

        candidate_fitness = evaluate_chromosome(candidate)

        if candidate_fitness < best_fitness:
            best = candidate.copy()
            best_fitness = candidate_fitness

            print(
                f"Iteration {iteration + 1}: "
                f"Improved to {best_fitness:.6f}"
            )

    return best, best_fitness


if __name__ == "__main__":
    original = np.load(
        RESULTS_DIR / "best_iss_mutation.npy"
    )

    original_fitness = evaluate_chromosome(original)

    np.random.seed(42)

    best, fitness = middle_mutation_search(
        original,
        iterations=299
    )

    placement = evaluate_cube_placement(best)

    assert len(best) == 201
    assert best[-1] == -1
    assert np.isclose(fitness, evaluate_chromosome(best))

    print("\n--- Middle Mutation Results ---")
    print("Original fitness:", original_fitness)
    print("Final fitness:", fitness)
    print("Correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])

    if fitness < original_fitness:
        np.save(
            RESULTS_DIR / "best_iss_middle.npy",
            best
        )
        print("Improved chromosome saved!")
    else:
        print("No improvement found.")

    print("Verification: PASSED")
