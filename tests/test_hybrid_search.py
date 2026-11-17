
import sys
import unittest
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from hybrid_search import hybrid_search
from random_search import evaluate_chromosome, evaluate_cube_placement


class TestHybridSearch(unittest.TestCase):

    def test_hybrid_search(self):
        np.random.seed(42)

        chromosome, fitness = hybrid_search(
            num_iterations=20,
            num_commands=100,
            num_mutations=10
        )

        self.assertIsNotNone(chromosome)
        self.assertEqual(len(chromosome), 201)
        self.assertEqual(chromosome[-1], -1)

        self.assertTrue(
            np.all((chromosome[:-1:2] >= 0) &
                   (chromosome[:-1:2] < 148))
        )

        self.assertTrue(
            np.all((chromosome[1:-1:2] >= 0) &
                   (chromosome[1:-1:2] < 6))
        )

        actual_fitness = evaluate_chromosome(chromosome)
        self.assertTrue(np.isclose(fitness, actual_fitness))

        placement = evaluate_cube_placement(chromosome)

        self.assertEqual(
            placement["successful_moves"] + placement["rejected_moves"],
            100
        )

        self.assertGreaterEqual(placement["correct_cubes"], 0)
        self.assertLessEqual(placement["correct_cubes"], 148)


if __name__ == "__main__":
    unittest.main()
