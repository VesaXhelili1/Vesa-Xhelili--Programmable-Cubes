
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from random_search import (
    generate_chromosome,
    evaluate_cube_placement,
)

np.random.seed(42)

chromosome = generate_chromosome(
    num_cubes=148,
    num_commands=100
)

result = evaluate_cube_placement(chromosome)

print("\n--- Movement Success Test ---")
print("Commands attempted:", result["steps_needed"])
print("Successful moves:", result["successful_moves"])
print("Rejected moves:", result["rejected_moves"])
print("Success rate:", f'{result["success_rate"]:.2%}')
print("Correct cubes:", result["correct_cubes"])

assert (
    result["successful_moves"] + result["rejected_moves"]
    == result["steps_needed"]
)

assert 0 <= result["success_rate"] <= 1

print("\nMovement counter validation: PASSED")


from random_search import try_legal_move

print("\n--- Legal Move Function Test ---")

class FakeCubes:
    def apply_single_update_step(self, cube_id, move, verbose=False):
        return 1 if move == 0 else 0

fake_cubes = FakeCubes()

assert try_legal_move(fake_cubes, 0, 0) is True
assert try_legal_move(fake_cubes, 0, 1) is False

print("Legal move function: PASSED")