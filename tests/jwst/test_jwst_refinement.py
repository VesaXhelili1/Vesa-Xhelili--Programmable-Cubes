
import sys
from pathlib import Path

import numpy as np
import pytest

JWST_SOURCE = Path(__file__).resolve().parents[2] / "src" / "jwst"
sys.path.insert(0, str(JWST_SOURCE))

import jwst_refinement_search as refinement


def test_mutation_preserves_chromosome_structure():
    chromosome = np.array([
        10, 0,
        20, 1,
        30, 2,
        -1,
    ])

    rng = np.random.default_rng(42)

    mutated = refinement.mutate_chromosome(
        chromosome, mutation_count=2, rng=rng
    )

    assert len(mutated) == len(chromosome)
    assert mutated[-1] == -1
    assert np.array_equal(
        chromosome,
        [10, 0, 20, 1, 30, 2, -1]
    )

    assert np.all((mutated[:-1:2] >= 0))
    assert np.all((mutated[:-1:2] < 643))
    assert np.all((mutated[1:-1:2] >= 0))
    assert np.all((mutated[1:-1:2] < 6))

    changed = sum(
        not np.array_equal(
            mutated[i:i+2],
            chromosome[i:i+2]
        )
        for i in range(0, len(chromosome)-1, 2)
    )

    assert changed == 2


def test_invalid_mutation_count():
    chromosome = np.array([10, 0, 20, 1, -1])
    rng = np.random.default_rng(42)

    with pytest.raises(ValueError):
        refinement.mutate_chromosome(chromosome, 0, rng)

    with pytest.raises(ValueError):
        refinement.mutate_chromosome(chromosome, 3, rng)


def test_refinement_saves_results_without_esa_simulator(
    tmp_path, monkeypatch
):
    baseline = np.array([
        10, 0,
        20, 1,
        30, 2,
        -1,
    ])

    baseline_path = tmp_path / "baseline.npy"
    output_dir = tmp_path / "output"

    np.save(baseline_path, baseline)

    evaluations = []

    def fake_fitness(chromosome):
        evaluations.append(chromosome.copy())
        return float(np.sum(chromosome[:-1]))

    monkeypatch.setattr(
        refinement, "evaluate_jwst", fake_fitness
    )

    results = refinement.run_refinement(
        baseline_path=baseline_path,
        output_dir=output_dir,
        mutation_sizes=(1, 2),
        evaluations=3,
    )

    assert len(results) == 2
    assert all(r["evaluations"] == 3 for r in results)
    assert all(len(r["fitness_history"]) == 4 for r in results)

    best_path = output_dir / "best_refined_jwst.npy"
    assert best_path.exists()
    assert (output_dir / "refinement_results.json").exists()

    best = np.load(best_path)
    assert fake_fitness(best) <= fake_fitness(baseline)


def test_existing_worse_checkpoint_is_replaced(
    tmp_path, monkeypatch
):
    baseline = np.array([10, 0, 20, 1, -1])
    worse = np.array([50, 0, 60, 1, -1])

    baseline_path = tmp_path / "baseline.npy"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    np.save(baseline_path, baseline)
    np.save(output_dir / "best_refined_jwst.npy", worse)

    monkeypatch.setattr(
        refinement,
        "evaluate_jwst",
        lambda chromosome: float(
            np.sum(chromosome[:-1])
        ),
    )

    refinement.run_refinement(
        baseline_path=baseline_path,
        output_dir=output_dir,
        mutation_sizes=(1,),
        evaluations=1,
    )

    saved = np.load(
        output_dir / "best_refined_jwst.npy"
    )

    assert float(np.sum(saved[:-1])) <= float(
        np.sum(baseline[:-1])
    )
