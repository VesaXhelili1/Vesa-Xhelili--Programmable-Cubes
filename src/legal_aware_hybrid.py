
import numpy as np

from legal_move_search import initialize_cubes
from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
    try_legal_move,
)


def mutate_legal_suffix(
    chromosome,
    num_commands=100,
    min_replace=5,
    max_replace=20,
):
    # Keep a random number of existing commands.
    replace_count = np.random.randint(
    min_replace,
    max_replace + 1
)

    prefix_length = num_commands - replace_count

    prefix = chromosome[:prefix_length * 2].tolist()

    # Replay the unchanged commands.
    cubes = initialize_cubes()

    if prefix:
        cubes.apply_chromosome(
            np.array(prefix + [-1], dtype=int),
            False,
        )

    new_commands = prefix.copy()

    remaining = num_commands - prefix_length
    successful = 0
    attempts = 0
    max_attempts = remaining * 100

    # Generate movements that are legal in the
    # current cube configuration.
    while successful < remaining and attempts < max_attempts:
        cube_id = np.random.randint(0, 148)
        move = np.random.randint(0, 6)

        attempts += 1

        if try_legal_move(cubes, cube_id, move):
            new_commands.extend([cube_id, move])
            successful += 1

    if successful != remaining:
        return None

    new_commands.append(-1)

    return np.array(new_commands, dtype=int)


def legal_aware_hybrid(
    initial_chromosome,
    num_iterations=299,
    min_replace=5,
    max_replace=20,
):
    best_chromosome = initial_chromosome.copy()
    best_fitness = evaluate_chromosome(best_chromosome)

    print("Initial fitness:", best_fitness)

    for iteration in range(num_iterations):
        candidate = mutate_legal_suffix(
    best_chromosome,
    min_replace=min_replace,
    max_replace=max_replace,
)

        if candidate is None:
            continue

        candidate_fitness = evaluate_chromosome(candidate)

        if candidate_fitness < best_fitness:
            best_chromosome = candidate.copy()
            best_fitness = candidate_fitness

            print(
                f"Iteration {iteration + 1}: "
                f"Improved fitness to {best_fitness:.6f}"
            )

    return best_chromosome, best_fitness


if __name__ == "__main__":
    from pathlib import Path

    np.random.seed(42)

    results_dir = (
        Path(__file__).resolve().parent.parent / "results"
    )

    original = np.load(
        results_dir / "best_iss_chromosome.npy"
    )

    original_fitness = evaluate_chromosome(original)
    original_placement = evaluate_cube_placement(original)

    chromosome, fitness = legal_aware_hybrid(
    initial_chromosome=original,
    num_iterations=999,
)

    placement = evaluate_cube_placement(chromosome)

    assert len(chromosome) == 201
    assert chromosome[-1] == -1
    assert np.isclose(
        fitness,
        evaluate_chromosome(chromosome),
    )

    print("\n--- Legal-Aware Hybrid Comparison ---")
    print("Original fitness:", original_fitness)
    print("New fitness:", fitness)
    print(
        "Original correct cubes:",
        original_placement["correct_cubes"],
    )
    print("New correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])

    if fitness < original_fitness:
        np.save(
            results_dir / "best_iss_legal_aware.npy",
            chromosome,
        )
        print("Improved chromosome saved!")
    else:
        print("No ESA fitness improvement found.")

    print("Legal-aware validation: PASSED")
