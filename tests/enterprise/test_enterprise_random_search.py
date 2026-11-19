
import sys
from pathlib import Path

import numpy as np
import pytest

SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "enterprise"
)

sys.path.insert(0, str(SOURCE))

import enterprise_random_search as random_module


def test_chromosome_structure():
    chromosome = random_module.generate_chromosome(
        num_commands=10,
        rng=np.random.default_rng(42),
    )

    assert len(chromosome) == 21
    assert chromosome[-1] == -1

    assert np.all(chromosome[:-1:2] >= 0)
    assert np.all(chromosome[:-1:2] < 1472)

    assert np.all(chromosome[1:-1:2] >= 0)
    assert np.all(chromosome[1:-1:2] < 6)


def test_reproducible_generation():
    first = random_module.generate_chromosome(
        10, np.random.default_rng(42)
    )

    second = random_module.generate_chromosome(
        10, np.random.default_rng(42)
    )

    assert np.array_equal(first, second)


def test_invalid_command_count():
    with pytest.raises(ValueError):
        random_module.generate_chromosome(0)

    with pytest.raises(ValueError):
        random_module.generate_chromosome(100001)


def test_random_search_with_fake_fitness(monkeypatch):
    calls = []

    def fake_fitness(chromosome):
        calls.append(chromosome.copy())
        return float(np.sum(chromosome[:-1]))

    monkeypatch.setattr(
        random_module,
        "evaluate_enterprise",
        fake_fitness,
    )

    best, fitness = random_module.random_search(
        num_iterations=5,
        num_commands=3,
        seed=42,
    )

    assert len(calls) == 5
    assert len(best) == 7

    assert fitness == min(
        float(np.sum(chromosome[:-1]))
        for chromosome in calls
    )
