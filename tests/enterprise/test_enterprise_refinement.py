
import json
import sys
from pathlib import Path

import numpy as np
import pytest

SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src" / "enterprise"
)
sys.path.insert(0, str(SOURCE))

import enterprise_refinement_search as refinement


def fake_fitness(chromosome):
    return float(np.sum(chromosome[:-1]))


def test_refinement_saves_results(tmp_path, monkeypatch):
    baseline = np.array([
        10, 0, 20, 1, 30, 2, -1
    ])

    baseline_path = tmp_path / "baseline.npy"
    output_dir = tmp_path / "results"
    np.save(baseline_path, baseline)

    monkeypatch.setattr(
        refinement,
        "evaluate_enterprise",
        fake_fitness,
    )

    results = refinement.run_refinement(
        baseline_path,
        output_dir,
        mutation_sizes=(1, 2),
        evaluations=3,
    )

    assert len(results) == 2
    assert all(len(r["fitness_history"]) == 4
               for r in results)

    best = np.load(
        output_dir / "best_refined_enterprise.npy"
    )

    assert fake_fitness(best) <= fake_fitness(baseline)

    with open(
        output_dir / "refinement_results.json"
    ) as file:
        data = json.load(file)

    assert len(data["experiments"]) == 2


def test_previous_better_checkpoint_preserved(
    tmp_path, monkeypatch
):
    baseline = np.array([100, 0, 200, 1, -1])
    better = np.array([1, 0, 2, 1, -1])

    baseline_path = tmp_path / "baseline.npy"
    output_dir = tmp_path / "results"
    output_dir.mkdir()

    np.save(baseline_path, baseline)
    np.save(
        output_dir / "best_refined_enterprise.npy",
        better,
    )

    monkeypatch.setattr(
        refinement, "evaluate_enterprise", fake_fitness
    )

    refinement.run_refinement(
        baseline_path,
        output_dir,
        mutation_sizes=(1,),
        evaluations=1,
    )

    saved = np.load(
        output_dir / "best_refined_enterprise.npy"
    )

    assert fake_fitness(saved) <= fake_fitness(better)


def test_previous_worse_checkpoint_replaced(
    tmp_path, monkeypatch
):
    baseline = np.array([10, 0, 20, 1, -1])
    worse = np.array([100, 0, 200, 1, -1])

    baseline_path = tmp_path / "baseline.npy"
    output_dir = tmp_path / "results"
    output_dir.mkdir()

    np.save(baseline_path, baseline)
    np.save(
        output_dir / "best_refined_enterprise.npy",
        worse,
    )

    monkeypatch.setattr(
        refinement, "evaluate_enterprise", fake_fitness
    )

    refinement.run_refinement(
        baseline_path,
        output_dir,
        mutation_sizes=(1,),
        evaluations=1,
    )

    saved = np.load(
        output_dir / "best_refined_enterprise.npy"
    )

    assert fake_fitness(saved) <= fake_fitness(baseline)


def test_invalid_evaluation_budget(tmp_path):
    with pytest.raises(ValueError):
        refinement.run_refinement(
            "unused.npy", tmp_path, evaluations=0
        )


def test_invalid_mutation_size(tmp_path, monkeypatch):
    baseline_path = tmp_path / "baseline.npy"
    np.save(
        baseline_path,
        np.array([10, 0, 20, 1, -1]),
    )

    monkeypatch.setattr(
        refinement, "evaluate_enterprise", fake_fitness
    )

    with pytest.raises(ValueError):
        refinement.run_refinement(
            baseline_path,
            tmp_path / "output",
            mutation_sizes=(3,),
            evaluations=1,
        )
