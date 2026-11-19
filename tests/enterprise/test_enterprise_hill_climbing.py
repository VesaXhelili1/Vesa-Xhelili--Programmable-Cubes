
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

import enterprise_hill_climbing as hill


def test_mutation_preserves_structure():
    chromosome = np.array([
        10, 0,
        20, 1,
        30, 2,
        -1,
    ])

    rng = np.random.default_rng(42)

    candidate = hill.mutate_chromosome(
        chromosome,
        num_mutations=2,
        rng=rng,
    )

    assert len(candidate) == len(chromosome)
    assert candidate[-1] == -1

    assert np.array_equal(
        chromosome,
        [10, 0, 20, 1, 30, 2, -1],
    )

    assert np.all(candidate[:-1:2] >= 0)
    assert np.all(candidate[:-1:2] < 1472)

    assert np.all(candidate[1:-1:2] >= 0)
    assert np.all(candidate[1:-1:2] < 6)

    changed_commands = sum(
        not np.array_equal(
            candidate[i:i + 2],
            chromosome[i:i + 2],
        )
        for i in range(0, len(chromosome) - 1, 2)
    )

    assert changed_commands == 2


def test_mutation_is_reproducible():
    chromosome = np.array([
        10, 0,
        20, 1,
        30, 2,
        -1,
    ])

    first = hill.mutate_chromosome(
        chromosome,
        2,
        np.random.default_rng(42),
    )

    second = hill.mutate_chromosome(
        chromosome,
        2,
        np.random.default_rng(42),
    )

    assert np.array_equal(first, second)


def test_invalid_mutation_count():
    chromosome = np.array([10, 0, 20, 1, -1])
    rng = np.random.default_rng(42)

    with pytest.raises(ValueError):
        hill.mutate_chromosome(chromosome, 0, rng)

    with pytest.raises(ValueError):
        hill.mutate_chromosome(chromosome, 3, rng)


def test_hill_climbing_with_fake_fitness(monkeypatch):
    evaluated = []

    def fake_fitness(chromosome):
        evaluated.append(chromosome.copy())
        return float(np.sum(chromosome[:-1]))

    monkeypatch.setattr(
        hill,
        "evaluate_enterprise",
        fake_fitness,
    )

    best, fitness = hill.hill_climbing(
        num_iterations=5,
        num_commands=3,
        num_mutations=1,
        seed=42,
    )

    assert len(evaluated) == 5
    assert len(best) == 7
    assert fitness <= fake_fitness(evaluated[0])
    assert fitness == fake_fitness(best)
