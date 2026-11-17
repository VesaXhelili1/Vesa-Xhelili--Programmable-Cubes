
import time

import numpy as np

from random_search import random_search, evaluate_cube_placement
from legal_move_search import generate_legal_chromosome
from random_search import evaluate_chromosome

from hill_climbing import hill_climbing


seeds = [10, 20, 30, 40, 50]

results = {
    "random": [],
    "hill": [],
    "legal": [],
}


cube_results = {
    "random": [],
    "hill": [],
    "legal": [],
}

time_results = {
    "random": [],
    "hill": [],
    "legal": [],
}
attempt_results = []


for seed in seeds:
    print(f"\n--- Seed {seed} ---")

    np.random.seed(seed)

    start = time.perf_counter()
    random_chromosome, random_fitness = random_search(
        num_iterations=100,
        num_commands=100
    )
    random_time = time.perf_counter() - start

    np.random.seed(seed)

    start = time.perf_counter()
    legal_chromosome, attempts = generate_legal_chromosome(
        num_commands=100
    )
    legal_fitness = evaluate_chromosome(legal_chromosome)
    legal_time = time.perf_counter() - start


    np.random.seed(seed)

    start = time.perf_counter()
    hill_chromosome, hill_fitness = hill_climbing(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )
    hill_time = time.perf_counter() - start


    random_placement = evaluate_cube_placement(random_chromosome)
    hill_placement = evaluate_cube_placement(hill_chromosome)
    legal_placement = evaluate_cube_placement(legal_chromosome)

    print("\nRandom Search:")
    print("Fitness:", random_fitness)
    print("Correct cubes:", random_placement["correct_cubes"])
    print("Time:", f"{random_time:.3f}s")

    results["random"].append(random_fitness)
    results["hill"].append(hill_fitness)
    results["legal"].append(legal_fitness)


    cube_results["random"].append(random_placement["correct_cubes"])
    cube_results["hill"].append(hill_placement["correct_cubes"])
    cube_results["legal"].append(legal_placement["correct_cubes"])


    time_results["random"].append(random_time)
    time_results["hill"].append(hill_time)
    time_results["legal"].append(legal_time)

    attempt_results.append(attempts)




    print("\nLegal-Move Search:")
    print("Fitness:", legal_fitness)
    print("Correct cubes:", legal_placement["correct_cubes"])
    print("Generation attempts:", attempts)
    print("Time:", f"{legal_time:.3f}s")



    print("\nHill Climbing (10 mutations):")
    print("Fitness:", hill_fitness)
    print("Correct cubes:", hill_placement["correct_cubes"])
    print("Time:", f"{hill_time:.3f}s")


print("\n--- Average Fitness Results ---")

print("Random Search:", np.mean(results["random"]))
print("Hill Climbing:", np.mean(results["hill"]))
print("Legal-Move Search:", np.mean(results["legal"]))


print("\n--- Average Correct Cubes ---")

print("Random Search:", np.mean(cube_results["random"]))
print("Hill Climbing:", np.mean(cube_results["hill"]))
print("Legal-Move Search:", np.mean(cube_results["legal"]))



print("\n--- Average Execution Times ---")

print("Random Search:", f'{np.mean(time_results["random"]):.3f}s')
print("Hill Climbing:", f'{np.mean(time_results["hill"]):.3f}s')
print("Legal-Move Search:", f'{np.mean(time_results["legal"]):.3f}s')



print("\n--- Legal-Move Generation Statistics ---")

average_attempts = np.mean(attempt_results)
acceptance_rate = (100 / average_attempts) * 100

print("Average generation attempts:", f"{average_attempts:.1f}")
print("Average acceptance rate:", f"{acceptance_rate:.2f}%")
print("Minimum attempts:", min(attempt_results))
print("Maximum attempts:", max(attempt_results))
