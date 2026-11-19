
import json
from pathlib import Path
from zipfile import ZipFile

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "enterprise"

# Corrected Enterprise V3 experiment files.
OPTIMIZATION_SUMMARY = (
    RESULTS_DIR / "enterprise_v3_final_summary.json"
)

REFINEMENT_SUMMARY = (
    RESULTS_DIR / "enterprise_v3_refinement_summary.json"
)

REFINEMENT_ARCHIVE = (
    RESULTS_DIR / "enterprise-v3-refinement-final.zip"
)

ALGORITHMS = ("random", "hill", "hybrid")
SEEDS = (10, 20, 30)
MUTATION_SIZES = (1, 3, 10)


def load_results():
    for file in (
        OPTIMIZATION_SUMMARY,
        REFINEMENT_SUMMARY,
        REFINEMENT_ARCHIVE,
    ):
        assert file.exists(), f"Missing required file: {file}"

    with OPTIMIZATION_SUMMARY.open() as file:
        optimization = json.load(file)

    with REFINEMENT_SUMMARY.open() as file:
        refinement = json.load(file)

    assert (
        optimization["fitness_direction"]
        == "official_ESA_minimize"
    )

    assert (
        refinement["fitness_direction"]
        == "official_ESA_minimize"
    )

    histories = {}

    with ZipFile(REFINEMENT_ARCHIVE) as archive:
        for size in MUTATION_SIZES:
            filename = (
                f"mutation_{size}/refinement_results.json"
            )

            with archive.open(filename) as file:
                data = json.load(file)

            histories[size] = (
                data["experiments"][0]["fitness_history"]
            )

    return optimization, refinement, histories


def plot_algorithm_comparison(optimization):
    runs = optimization["results"]

    plt.figure(figsize=(10, 6))

    for algorithm in ALGORITHMS:
        fitness_values = []

        for seed in SEEDS:
            matching = [
                run for run in runs
                if run["algorithm"] == algorithm
                and run["seed"] == seed
            ]

            assert len(matching) == 1

            fitness_values.append(
                matching[0]["fitness"]
            )

        plt.plot(
            SEEDS,
            fitness_values,
            marker="o",
            label=algorithm.title(),
        )

    plt.title(
        "Enterprise V3: Corrected Algorithm Comparison"
    )
    plt.xlabel("Random Seed")
    plt.ylabel("Official ESA Fitness (Lower Is Better)")
    plt.xticks(SEEDS)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output = (
        RESULTS_DIR / "enterprise_fitness_comparison.png"
    )

    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def plot_mutation_comparison(refinement):
    experiments = refinement["experiments"]

    values = []

    for size in MUTATION_SIZES:
        matching = [
            item for item in experiments
            if item["mutation_size"] == size
        ]

        assert len(matching) == 1
        values.append(matching[0]["fitness"])

    plt.figure(figsize=(9, 6))

    plt.bar(
        [str(size) for size in MUTATION_SIZES],
        values,
    )

    plt.title(
        "Enterprise V3: Corrected Mutation Comparison"
    )
    plt.xlabel("Number of Mutated Commands")
    plt.ylabel("Official ESA Fitness (Lower Is Better)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    output = (
        RESULTS_DIR / "enterprise_mutation_comparison.png"
    )

    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def plot_refinement_convergence(histories):
    plt.figure(figsize=(10, 6))

    for size in MUTATION_SIZES:
        history = np.asarray(
            histories[size],
            dtype=float,
        )

        evaluations = np.arange(
            1,
            len(history) + 1,
        )

        plt.plot(
            evaluations,
            history,
            label=f"{size}-command mutations",
        )

    plt.title(
        "Enterprise V3: Corrected Refinement Convergence"
    )
    plt.xlabel("Fitness Evaluation")
    plt.ylabel("Best Official ESA Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output = (
        RESULTS_DIR / "enterprise_refinement_convergence.png"
    )

    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def main():
    optimization, refinement, histories = load_results()

    assert len(optimization["results"]) == 9
    assert len(refinement["experiments"]) == 3

    assert np.isclose(
        optimization["best_fitness"],
        -0.009539123630673031,
        atol=1e-10,
        rtol=0,
    )

    assert np.isclose(
        refinement["best_fitness"],
        -0.013940532081377245,
        atol=1e-10,
        rtol=0,
    )

    print("--- Enterprise V3 Experiment Analysis ---")

    plot_algorithm_comparison(optimization)
    plot_mutation_comparison(refinement)
    plot_refinement_convergence(histories)

    print("\n--- Corrected Enterprise Results ---")
    print(
        "Best algorithm:",
        optimization["best_algorithm"],
    )
    print(
        "Best seed:",
        optimization["best_seed"],
    )
    print(
        "Optimization fitness:",
        optimization["best_fitness"],
    )
    print(
        "Best mutation size:",
        refinement["best_mutation_size"],
    )
    print(
        "Final refined fitness:",
        refinement["best_fitness"],
    )

    print("Graphs generated: 3")
    print("ENTERPRISE V3 ANALYSIS: PASSED")


if __name__ == "__main__":
    main()
