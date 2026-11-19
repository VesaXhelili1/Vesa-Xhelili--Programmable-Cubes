
import json
from pathlib import Path
from zipfile import ZipFile

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results" / "enterprise"

V2_ARCHIVE = RESULTS_DIR / "enterprise-checkpoint-v4.zip"
REFINEMENT_ARCHIVE = (
    RESULTS_DIR / "enterprise-refinement-final.zip"
)

ALGORITHMS = ("random", "hill", "hybrid")
SEEDS = (10, 20, 30)
MUTATIONS = (1, 3, 10)


def read_json(archive, filename):
    with archive.open(filename) as file:
        return json.load(file)


def load_results():
    assert V2_ARCHIVE.exists(), "Enterprise V4 ZIP missing"
    assert REFINEMENT_ARCHIVE.exists(), "Refinement ZIP missing"

    with ZipFile(V2_ARCHIVE) as archive:
        summary = read_json(
            archive, "enterprise_v2_summary.json"
        )

    with ZipFile(REFINEMENT_ARCHIVE) as archive:
        refinement = read_json(
            archive, "enterprise_refinement_summary.json"
        )

        histories = {}

        for mutation_size in MUTATIONS:
            data = read_json(
                archive,
                f"mutation_{mutation_size}/refinement_results.json",
            )

            histories[mutation_size] = (
                data["experiments"][0]["fitness_history"]
            )

    return summary, refinement, histories


def plot_algorithm_comparison(summary):
    runs = summary["results"]

    plt.figure(figsize=(10, 6))

    for algorithm in ALGORITHMS:
        fitness_values = []

        for seed in SEEDS:
            matching = [
                run for run in runs
                if run["algorithm"] == algorithm
                and run["seed"] == seed
            ]

            assert len(matching) == 1, (
                f"Missing run: {algorithm}, seed {seed}"
            )

            fitness_values.append(matching[0]["fitness"])

        plt.plot(
            SEEDS,
            fitness_values,
            marker="o",
            label=algorithm.title(),
        )

    plt.title("Enterprise: Algorithm Fitness Comparison")
    plt.xlabel("Random Seed")
    plt.ylabel("Best ESA Fitness (Lower Is Better)")
    plt.xticks(SEEDS)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = RESULTS_DIR / "enterprise_fitness_comparison.png"
    plt.savefig(path, dpi=200)
    plt.close()

    print("Created:", path.name)


def plot_mutation_comparison(refinement):
    experiments = refinement["experiments"]

    fitness_values = []

    for mutation_size in MUTATIONS:
        matching = [
            experiment for experiment in experiments
            if experiment["mutation_size"] == mutation_size
        ]

        assert len(matching) == 1
        fitness_values.append(matching[0]["fitness"])

    plt.figure(figsize=(9, 6))

    plt.bar(
        [str(size) for size in MUTATIONS],
        fitness_values,
    )

    plt.title("Enterprise: Mutation Size Comparison")
    plt.xlabel("Number of Mutated Commands")
    plt.ylabel("Best ESA Fitness (Lower Is Better)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    path = RESULTS_DIR / "enterprise_mutation_comparison.png"
    plt.savefig(path, dpi=200)
    plt.close()

    print("Created:", path.name)


def plot_refinement_convergence(histories):
    plt.figure(figsize=(10, 6))

    for mutation_size in MUTATIONS:
        history = np.asarray(
            histories[mutation_size], dtype=float
        )

        evaluations = np.arange(1, len(history) + 1)

        plt.plot(
            evaluations,
            history,
            label=f"{mutation_size}-command mutations",
        )

    plt.title("Enterprise: Refinement Convergence")
    plt.xlabel("Fitness Evaluation")
    plt.ylabel("Best ESA Fitness (Lower Is Better)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    path = RESULTS_DIR / "enterprise_refinement_convergence.png"
    plt.savefig(path, dpi=200)
    plt.close()

    print("Created:", path.name)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    summary, refinement, histories = load_results()

    assert len(summary["results"]) == 9
    assert len(refinement["experiments"]) == 3

    print("--- Enterprise Experiment Analysis ---")

    plot_algorithm_comparison(summary)
    plot_mutation_comparison(refinement)
    plot_refinement_convergence(histories)

    print("\n--- Final Results ---")
    print("Best algorithm:", summary["best_algorithm"])
    print("Optimization fitness:", summary["best_fitness"])
    print("Refined fitness:", refinement["best_fitness"])
    print("Graphs generated: 3")
    print("ENTERPRISE ANALYSIS: PASSED")


if __name__ == "__main__":
    main()
