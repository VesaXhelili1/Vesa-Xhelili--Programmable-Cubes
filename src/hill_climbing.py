
import numpy as np


from random_search import generate_chromosome, evaluate_chromosome




def mutate_chromosome(chromosome, num_mutations=1):
    mutated = chromosome.copy()

    num_commands = (len(mutated) - 1) // 2

    for _ in range(num_mutations):
        command_index = np.random.randint(0, num_commands)

        cube_index = command_index * 2
        movement_index = cube_index + 1

        mutation_type = np.random.choice(["cube", "movement"])

        if mutation_type == "cube":
            old_cube = mutated[cube_index]

            new_cube = np.random.randint(0, 147)
            if new_cube >= old_cube:
                new_cube += 1

            mutated[cube_index] = new_cube

        else:
            old_movement = mutated[movement_index]

            new_movement = np.random.randint(0, 5)
            if new_movement >= old_movement:
                new_movement += 1

            mutated[movement_index] = new_movement

    return mutated







def hill_climbing(
    num_iterations=100,
    num_commands=100,
    num_mutations=1
):
    current_chromosome = generate_chromosome(
        num_cubes=148,
        num_commands=num_commands
    )

    current_fitness = evaluate_chromosome(current_chromosome)

    print(f"Initial fitness: {current_fitness:.6f}")

    for iteration in range(num_iterations):
        candidate = mutate_chromosome(
            current_chromosome,
            num_mutations=num_mutations
        )

        candidate_fitness = evaluate_chromosome(candidate)


        if candidate_fitness < current_fitness:
            current_chromosome = candidate
            current_fitness = candidate_fitness
            print(
                f"Iteration {iteration + 1}: "
                f"Improved to {current_fitness:.6f}"
            )
        else:
            print(f"Iteration {iteration + 1}: No improvement")

    return current_chromosome, current_fitness








if __name__ == "__main__":
    np.random.seed(42)

    
    best_solution, best_fitness = hill_climbing(
    num_iterations=99,
    num_commands=100,
    num_mutations=10
    )


    print("\n--- Hill Climbing Results ---")
    print("Best fitness:", best_fitness)
    print("Chromosome length:", len(best_solution))


