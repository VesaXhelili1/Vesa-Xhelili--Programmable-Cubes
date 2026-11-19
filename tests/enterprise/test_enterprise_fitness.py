
import sys
from pathlib import Path

import numpy as np

SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "enterprise"
)

sys.path.insert(0, str(SOURCE))

import enterprise_fitness as fitness_module


def test_enterprise_preserves_official_fitness(monkeypatch):
    """The wrapper must not reverse ESA's fitness sign."""

    class FakeProblem:
        def fitness(self, chromosome):
            return np.array([-0.25])

    monkeypatch.setattr(
        fitness_module,
        "programmable_cubes_UDP",
        lambda scenario: FakeProblem(),
    )

    chromosome = np.array([0, 0, -1], dtype=int)

    result = fitness_module.evaluate_enterprise(chromosome)

    assert result == -0.25
