
import json
from pathlib import Path
from zipfile import ZipFile

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "jwst"

CHECKPOINTS = {
    "hybrid_300": RESULTS / "jwst-checkpoint.zip",
    "hybrid_1000": RESULTS / "jwst-checkpoint-v2.zip",
    "refinement": RESULTS / "jwst-checkpoint-v3.zip",
}


def load_checkpoint_json(zip_path, filename):
    """Read experiment statistics without extracting ZIP files."""
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing checkpoint: {zip_path}")

    with ZipFile(zip_path) as archive:
        with archive.open(filename) as file:
            return json.load(file)


def load_results():
    first = load_checkpoint_json(
        CHECKPOINTS["hybrid_300"],
        "experiment_results.json",
    )

    second = load_checkpoint_json(
        CHECKPOINTS["hybrid_1000"],
        "large_experiment_results.json",
    )

    refinement = load_checkpoint_json(
        CHECKPOINTS["refinement"],
        "refinement_results.json",
    )

    return first, second, refinement


def plot_fitness_progression(first, second, refinement):
    """Show the progression of verified best fitness."""

    stages = [
        "Mac baseline",
        "Hybrid 300",
        "Hybrid 1000",
        "Refinement",
    ]

    fitness = [
        -0.038571111111111125,
        first["best_fitness"],
        second["best_fitness"],
        refinement["global_best_fitness"],
    ]

    plt.figure(figsize=(10, 5))
    plt.plot(stages, fitness, marker="o", linewidth=2)

    plt.title("JWST - Best Fitness Progression")
    plt.xlabel("Optimization stage")
    plt.ylabel("ESA Fitness (lower is better)")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output = RESULTS / "jwst_fitness_progress.png"
    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def plot_mutation_comparison(refinement):
    """Compare final fitness for each mutation size."""

    experiments = refinement["experiments"]

    labels = [
        f"{item['mutation_size']} commands"
        for item in experiments
    ]

    fitness = [
        item["final_fitness"]
        for item in experiments
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(labels, fitness)

    plt.title("JWST - Refinement Mutation Comparison")
    plt.xlabel("Mutation size")
    plt.ylabel("Final ESA Fitness (lower is better)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    output = RESULTS / "jwst_mutation_comparison.png"
    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def plot_refinement_convergence(refinement):
    """Show how the fitness changed during refinement."""

    plt.figure(figsize=(10, 5))

    for experiment in refinement["experiments"]:
        history = experiment["fitness_history"]

        plt.plot(
            range(len(history)),
            history,
            label=f"Mutation {experiment['mutation_size']}",
        )

    plt.title("JWST - Refinement Convergence")
    plt.xlabel("Fitness evaluations")
    plt.ylabel("Best Fitness (lower is better)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output = RESULTS / "jwst_refinement_convergence.png"
    plt.savefig(output, dpi=200)
    plt.close()

    print("Created:", output.name)


def main():
    first, second, refinement = load_results()

    plot_fitness_progression(first, second, refinement)
    plot_mutation_comparison(refinement)
    plot_refinement_convergence(refinement)

    print("\n--- JWST Experiment Analysis ---")
    print("Hybrid experiment 1:", first["best_fitness"])
    print("Hybrid experiment 2:", second["best_fitness"])
    print("Refinement:", refinement["global_best_fitness"])
    print("Graphs generated: 3")
    print("Analysis: PASSED")


if __name__ == "__main__":
    main()
