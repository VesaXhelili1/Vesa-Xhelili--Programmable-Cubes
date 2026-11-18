import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "jwst"))

from jwst_fitness import evaluate_jwst


def test_jwst_fitness():
    chromosome = np.array([0, 0, -1], dtype=int)

    fitness = evaluate_jwst(chromosome)

    assert np.isfinite(fitness)


def test_jwst_fitness_is_deterministic():
    chromosome = np.array([0, 0, -1], dtype=int)

    first = evaluate_jwst(chromosome)
    second = evaluate_jwst(chromosome)

    assert np.isclose(first, second, rtol=0, atol=1e-12)