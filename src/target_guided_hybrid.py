
import numpy as np

from legal_move_search import (
    generate_legal_chromosome,
    initialize_cubes,
)
from hill_climbing import mutate_chromosome
from random_search import (
    evaluate_chromosome,
    evaluate_cube_placement,
)
from target_heuristic import calculate_target_distance


def evaluate_solution(chromosome):
    fitness = evaluate_chromosome(chromosome)

    cubes = initialize_cubes()
    cubes.apply_chromosome(chromosome, False)

    distance = calculate_target_distance(
        cubes.cube_position
    )

    return fitness, distance


def target_guided_hybrid(
    num_iterations=99,
    num_commands=100,
    num_mutations=10,
):
    chromosome, attempts = generate_legal_chromosome(
        num_commands=num_commands
    )

    if (len(chromosome) - 1) // 2 != num_commands:
        raise RuntimeError("Could not generate enough legal moves")

    best_chromosome = chromosome.copy()
    best_fitness, best_distance = evaluate_solution(
        best_chromosome
    )

    print("Initial fitness:", best_fitness)
    print("Initial target distance:", best_distance)

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            best_chromosome,
            num_mutations=num_mutations
        )

        candidate_fitness, candidate_distance = (
            evaluate_solution(candidate)
        )

        # ESA fitness is the primary objective.
        # Target distance breaks ties in fitness.
        if (
            candidate_fitness < best_fitness
            or (
                np.isclose(
                    candidate_fitness,
                    best_fitness,
                    rtol=0,
                    atol=1e-12
                )
                and candidate_distance < best_distance
            )
        ):
            best_chromosome = candidate.copy()
            best_fitness = candidate_fitness
            best_distance = candidate_distance

            print(
                f"Iteration {iteration + 1}: "
                f"fitness={best_fitness:.6f}, "
                f"distance={best_distance}"
            )

    return best_chromosome, best_fitness, best_distance


if __name__ == "__main__":
    np.random.seed(42)

    chromosome, fitness, distance = target_guided_hybrid(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    placement = evaluate_cube_placement(chromosome)

    print("\n--- Target-Guided Hybrid Results ---")
    print("Best fitness:", fitness)
    print("Target distance:", distance)
    print("Correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])

    assert len(chromosome) == 201
    assert chromosome[-1] == -1
    assert np.isclose(fitness, evaluate_chromosome(chromosome))

    print("Target-Guided Hybrid: PASSED")
