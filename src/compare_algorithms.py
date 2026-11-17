import matplotlib.pyplot as plt
import time
import numpy as np

from random_search import random_search
from hill_climbing import hill_climbing



# Complexity analysis
#
# n = number of commands in a chromosome
# k = number of fitness evaluations
# F(n) = time required by ESA's fitness evaluator
#
# Random Search:
# Time:  O(k * (n + F(n)))
# Space: O(n)
#
# Hill Climbing:
# Time:  O(n + k * (n + F(n)))
# Space: O(n)
#
# These bounds describe the search algorithms.
# They exclude the internal memory used by ESA's simulator.



if __name__ == "__main__":
    num_commands = 100
    num_evaluations = 100
    seeds = [10, 20, 30, 40, 50]

    random_results = []
    hill_results = []
    improved_hill_results = []

    for seed in seeds:
        print(f"\n--- Testing seed {seed} ---")

        # Random Search
        np.random.seed(seed)

        start_time = time.perf_counter()
        _, random_fitness = random_search(
            num_iterations=num_evaluations,
            num_commands=num_commands
        )
        random_time = time.perf_counter() - start_time

        # Hill Climbing
        np.random.seed(seed)

        start_time = time.perf_counter()
        _, hill_fitness = hill_climbing(
            num_iterations=num_evaluations - 1,
            num_commands=num_commands
        )
        hill_time = time.perf_counter() - start_time


        # Improved Hill Climbing (10 mutations)
        np.random.seed(seed)

        start_time = time.perf_counter()
        _, improved_hill_fitness = hill_climbing(
            num_iterations=num_evaluations - 1,
            num_commands=num_commands,
            num_mutations=10
        )
        improved_hill_time = time.perf_counter() - start_time


        random_results.append((random_fitness, random_time))
        hill_results.append((hill_fitness, hill_time))

        improved_hill_results.append(
            (improved_hill_fitness, improved_hill_time)
        )

        print(f"\nSeed {seed} results:")
        print(f"Random Search: {random_fitness:.6f}, {random_time:.2f}s")
        print(f"Hill Climbing: {hill_fitness:.6f}, {hill_time:.2f}s")

        print(
            f"Improved Hill Climbing: "
            f"{improved_hill_fitness:.6f}, "
            f"{improved_hill_time:.2f}s"
        )

    # Calculate averages
    random_avg_fitness = np.mean([r[0] for r in random_results])
    random_avg_time = np.mean([r[1] for r in random_results])

    hill_avg_fitness = np.mean([r[0] for r in hill_results])
    hill_avg_time = np.mean([r[1] for r in hill_results])


    improved_hill_avg_fitness = np.mean(
        [r[0] for r in improved_hill_results]
    )
    improved_hill_avg_time = np.mean(
        [r[1] for r in improved_hill_results]
    )

   
    print("\n--- Average Results (5 runs) ---")
    print(f"Commands per chromosome: {num_commands}")
    print(f"Fitness evaluations per algorithm: {num_evaluations}")

    print(f"\nRandom Search fitness: {random_avg_fitness:.6f}")
    print(f"Random Search time: {random_avg_time:.2f}s")

    print(f"\nHill Climbing fitness: {hill_avg_fitness:.6f}")
    print(f"Hill Climbing time: {hill_avg_time:.2f}s")


    print(f"\nImproved Hill Climbing fitness: {improved_hill_avg_fitness:.6f}")
    print(f"Improved Hill Climbing time: {improved_hill_avg_time:.2f}s")



    # Compare average fitness
    algorithms = [
    "Random Search",
    "Hill Climbing (1)",
    "Hill Climbing (10)"
]
    average_fitness = [
    random_avg_fitness,
    hill_avg_fitness,
    improved_hill_avg_fitness
]

    plt.figure(figsize=(8, 5))

    plt.bar(algorithms, average_fitness)

    plt.title("Average Fitness Comparison")
    plt.ylabel("Average Fitness (lower is better)")

    plt.axhline(0, color="gray", linewidth=0.8)
    plt.tight_layout()
    plt.show()

    # Compare average execution time
    average_times = [
    random_avg_time,
    hill_avg_time,
    improved_hill_avg_time
]

    plt.figure(figsize=(8, 5))

    plt.bar(algorithms, average_times)

    plt.title("Average Execution Time Comparison")
    plt.ylabel("Execution Time (seconds)")

    plt.tight_layout()
    plt.show()




