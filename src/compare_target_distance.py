
import numpy as np

from hybrid_search import hybrid_search
from legal_move_search import initialize_cubes
from target_heuristic import (
    calculate_target_distance,
    calculate_assignment_distance,
)
from random_search import evaluate_cube_placement


seeds = [10, 20, 30, 40, 50]

results = []

for seed in seeds:
    print(f"\n--- Seed {seed} ---")

    np.random.seed(seed)

    chromosome, fitness = hybrid_search(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

    cubes = initialize_cubes()
    cubes.apply_chromosome(chromosome, False)

    distance = calculate_target_distance(
        cubes.cube_position
    )
    assignment_distance = calculate_assignment_distance(
        cubes.cube_position
    )

    placement = evaluate_cube_placement(chromosome)

    results.append({
        "seed": seed,
        "fitness": fitness,
        "distance": distance,
        "assignment_distance": assignment_distance,
        "correct_cubes": placement["correct_cubes"],
    })

    print(
        f"Fitness: {fitness:.6f}, "
        f"Distance: {distance}, "
        f"Correct cubes: {placement['correct_cubes']}"
    )


print("\n--- Target Distance Summary ---")

for result in results:
    print(
        f"Seed {result['seed']}: "
        f"fitness={result['fitness']:.6f}, "
        f"distance={result['distance']}, "
        f"cubes={result['correct_cubes']}"
    )

print("\nAverage distance:", np.mean([r["distance"] for r in results]))
print("Average fitness:", np.mean([r["fitness"] for r in results]))
print(
    "Average correct cubes:",
    np.mean([r["correct_cubes"] for r in results])
)


print("\n--- Assignment Distance Summary ---")

for result in results:
    print(
        f"Seed {result['seed']}: "
        f"assignment={result['assignment_distance']}, "
        f"fitness={result['fitness']:.6f}, "
        f"correct cubes={result['correct_cubes']}"
    )

average_assignment = np.mean(
    [r["assignment_distance"] for r in results]
)

print("\nInitial assignment distance: 478")
print("Average final assignment distance:", average_assignment)
print("Average assignment improvement:", 478 - average_assignment)

