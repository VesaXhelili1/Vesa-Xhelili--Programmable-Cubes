
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

import enterprise_legal_move_search as legal


class FakeCubes:
    def __init__(self):
        self.attempts = 0

    def apply_single_update_step(self, cube_id, movement):
        self.attempts += 1

        # Accept every second movement.
        return 1 if self.attempts % 2 == 0 else 0


def test_legal_chromosome_structure(monkeypatch):
    monkeypatch.setattr(
        legal, "initialize_enterprise", FakeCubes
    )

    chromosome, attempts = legal.generate_legal_chromosome(
        num_commands=5,
        rng=np.random.default_rng(42),
    )

    assert len(chromosome) == 11
    assert chromosome[-1] == -1
    assert attempts == 10

    assert np.all(chromosome[:-1:2] >= 0)
    assert np.all(chromosome[:-1:2] < 1472)

    assert np.all(chromosome[1:-1:2] >= 0)
    assert np.all(chromosome[1:-1:2] < 6)


def test_legal_generation_is_reproducible(monkeypatch):
    monkeypatch.setattr(
        legal, "initialize_enterprise", FakeCubes
    )

    first, first_attempts = legal.generate_legal_chromosome(
        5,
        rng=np.random.default_rng(42),
    )

    second, second_attempts = legal.generate_legal_chromosome(
        5,
        rng=np.random.default_rng(42),
    )

    assert np.array_equal(first, second)
    assert first_attempts == second_attempts


def test_invalid_parameters():
    with pytest.raises(ValueError):
        legal.generate_legal_chromosome(0)

    with pytest.raises(ValueError):
        legal.generate_legal_chromosome(100001)

    with pytest.raises(ValueError):
        legal.generate_legal_chromosome(
            5, max_attempts_per_command=0
        )


def test_failed_generation(monkeypatch):
    class AlwaysReject:
        def apply_single_update_step(self, cube_id, movement):
            return 0

    monkeypatch.setattr(
        legal,
        "initialize_enterprise",
        AlwaysReject,
    )

    with pytest.raises(RuntimeError):
        legal.generate_legal_chromosome(
            num_commands=3,
            max_attempts_per_command=2,
            rng=np.random.default_rng(42),
        )


def test_analyze_movements(monkeypatch):
    monkeypatch.setattr(
        legal, "initialize_enterprise", FakeCubes
    )

    chromosome = np.array([
        10, 0,
        20, 1,
        30, 2,
        40, 3,
        -1,
    ])

    successful, rejected = legal.analyze_movements(
        chromosome
    )

    assert successful == 2
    assert rejected == 2
