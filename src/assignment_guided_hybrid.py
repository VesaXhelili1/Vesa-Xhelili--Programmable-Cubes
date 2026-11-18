
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
from target_heuristic import calculate_assignment_distance


def evaluate_assignment_solution(chromosome):
    fitness = evaluate_chromosome(chromosome)

    cubes = initialize_cubes()
    cubes.apply_chromosome(chromosome, False)

    distance = calculate_assignment_distance(
        cubes.cube_position
    )

    return fitness, distance


def assignment_guided_hybrid(
    num_iterations=99,
    num_commands=100,
    num_mutations=10,
):
    chromosome, attempts = generate_legal_chromosome(
        num_commands=num_commands
    )

    if (len(chromosome) - 1) // 2 != num_commands:
        raise RuntimeError("Could not generate enough legal movements")

    best_chromosome = chromosome.copy()
    best_fitness, best_distance = evaluate_assignment_solution(
        best_chromosome
    )

    print("Initial fitness:", best_fitness)
    print("Initial assignment distance:", best_distance)

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            best_chromosome,
            num_mutations=num_mutations
        )

        candidate_fitness, candidate_distance = (
            evaluate_assignment_solution(candidate)
        )

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
                f"assignment distance={best_distance}"
            )

    return best_chromosome, best_fitness, best_distance


if __name__ == "__main__":
    np.random.seed(42)

    chromosome, fitness, distance = assignment_guided_hybrid(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    placement = evaluate_cube_placement(chromosome)

    print("\n--- Assignment-Guided Hybrid Results ---")
    print("Best fitness:", fitness)
    print("Assignment distance:", distance)
    print("Correct cubes:", placement["correct_cubes"])
    print("Successful moves:", placement["successful_moves"])
    print("Rejected moves:", placement["rejected_moves"])

    assert len(chromosome) == 201
    assert chromosome[-1] == -1
    assert np.isclose(fitness, evaluate_chromosome(chromosome))

    print("Assignment-Guided Hybrid: PASSED")
