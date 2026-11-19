
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

import enterprise_hybrid_search as hybrid


def fake_legal_generator(num_commands, rng):
    chromosome = np.array([
        10, 0,
        20, 1,
        30, 2,
        -1,
    ])
    return chromosome, 12


def test_hybrid_search_with_fake_fitness(monkeypatch):
    evaluated = []

    def fake_fitness(chromosome):
        evaluated.append(chromosome.copy())
        return float(np.sum(chromosome[:-1]))

    monkeypatch.setattr(
        hybrid,
        "generate_legal_chromosome",
        fake_legal_generator,
    )

    monkeypatch.setattr(
        hybrid,
        "evaluate_enterprise",
        fake_fitness,
    )

    best, fitness = hybrid.hybrid_search(
        num_iterations=5,
        num_commands=3,
        num_mutations=1,
        seed=42,
    )

    assert len(evaluated) == 5
    assert len(best) == 7
    assert best[-1] == -1

    initial_fitness = float(
        np.sum(evaluated[0][:-1])
    )

    assert fitness <= initial_fitness
    assert fitness == fake_fitness(best)


def test_hybrid_search_is_reproducible(monkeypatch):
    monkeypatch.setattr(
        hybrid,
        "generate_legal_chromosome",
        fake_legal_generator,
    )

    monkeypatch.setattr(
        hybrid,
        "evaluate_enterprise",
        lambda chromosome: float(
            np.sum(chromosome[:-1])
        ),
    )

    first, first_fitness = hybrid.hybrid_search(
        num_iterations=5,
        num_commands=3,
        num_mutations=1,
        seed=42,
    )

    second, second_fitness = hybrid.hybrid_search(
        num_iterations=5,
        num_commands=3,
        num_mutations=1,
        seed=42,
    )

    assert np.array_equal(first, second)
    assert first_fitness == second_fitness


def test_invalid_iteration_count():
    with pytest.raises(ValueError):
        hybrid.hybrid_search(num_iterations=0)


def test_invalid_mutation_count():
    with pytest.raises(ValueError):
        hybrid.hybrid_search(
            num_commands=3,
            num_mutations=4,
        )
