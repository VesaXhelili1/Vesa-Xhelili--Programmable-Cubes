
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "jwst"))

from jwst_random_search import generate_chromosome
from jwst_hill_climbing import mutate_chromosome, hill_climbing
from jwst_legal_move_search import generate_legal_chromosome
from jwst_hybrid_search import hybrid_search
from analyze_movements import analyze_movements
from jwst_fitness import evaluate_jwst


def test_jwst_chromosome_format():
    chromosome = generate_chromosome(num_commands=20)

    assert chromosome.shape == (41,)
    assert chromosome[-1] == -1

    assert np.all(
        (chromosome[0:-1:2] >= 0)
        & (chromosome[0:-1:2] < 643)
    )

    assert np.all(
        (chromosome[1:-1:2] >= 0)
        & (chromosome[1:-1:2] < 6)
    )


def test_jwst_mutation():
    np.random.seed(42)

    original = generate_chromosome(num_commands=20)
    mutated = mutate_chromosome(original, num_mutations=2)

    assert len(original) == len(mutated)
    assert mutated[-1] == -1
    assert np.array_equal(original[-1:], mutated[-1:])


def test_jwst_legal_generation():
    np.random.seed(42)

    chromosome, attempts = generate_legal_chromosome(
        num_commands=20
    )

    successful, rejected = analyze_movements(chromosome)

    assert successful == 20
    assert rejected == 0
    assert attempts >= 20


def test_jwst_hill_climbing():
    np.random.seed(42)

    chromosome, fitness = hill_climbing(
        num_iterations=5,
        num_commands=20,
        num_mutations=2
    )

    assert len(chromosome) == 41
    assert np.isclose(
        fitness,
        evaluate_jwst(chromosome)
    )


def test_jwst_hybrid_search():
    np.random.seed(42)

    chromosome, fitness = hybrid_search(
        num_iterations=5,
        num_commands=20,
        num_mutations=2
    )

    assert len(chromosome) == 41
    assert np.isclose(
        fitness,
        evaluate_jwst(chromosome)
    )
