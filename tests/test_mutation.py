
import io
from contextlib import redirect_stdout
import sys
from pathlib import Path

# Make the src folder available for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


import numpy as np

from random_search import generate_chromosome, evaluate_chromosome
from hill_climbing import mutate_chromosome, hill_climbing

np.random.seed(42)

original = generate_chromosome(
    num_cubes=148,
    num_commands=100
)
original_backup = original.copy()

for num_mutations in [1, 3, 5, 10]:
    mutated = mutate_chromosome(
        original,
        num_mutations=num_mutations
    )

    assert len(mutated) == len(original)
    assert mutated[-1] == -1
    assert np.all((mutated[:-1:2] >= 0) & (mutated[:-1:2] < 148))
    assert np.all((mutated[1:-1:2] >= 0) & (mutated[1:-1:2] < 6))
    assert np.array_equal(original, original_backup)
    assert not np.array_equal(mutated, original)

    print(f"{num_mutations} mutations: PASSED")

print("\nAll mutation validation tests passed!")

# Validate Hill Climbing fitness
np.random.seed(42)

initial_chromosome = generate_chromosome(
    num_cubes=148,
    num_commands=100
)

initial_fitness = evaluate_chromosome(initial_chromosome)

# Reset the seed to reproduce the same starting chromosome
np.random.seed(42)

with redirect_stdout(io.StringIO()):
    best_chromosome, best_fitness = hill_climbing(
        num_iterations=99,
        num_commands=100,
        num_mutations=10
    )

assert best_fitness <= initial_fitness

assert np.isclose(
    evaluate_chromosome(best_chromosome),
    best_fitness
)

print("Hill Climbing fitness validation: PASSED")

