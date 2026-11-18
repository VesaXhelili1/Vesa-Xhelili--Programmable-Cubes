
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from legal_move_search import initialize_cubes
from target_heuristic import load_target_configuration
from random_search import evaluate_cube_placement


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

chromosome = np.load(RESULTS / "best_iss_mutation.npy")

target_positions, target_types, initial_types = (
    load_target_configuration()
)

initial_cubes = initialize_cubes()
initial_positions = initial_cubes.cube_position.copy()

final_cubes = initialize_cubes()
final_cubes.apply_chromosome(chromosome, False)
final_positions = final_cubes.cube_position.copy()

placement = evaluate_cube_placement(chromosome)


def plot_configuration(ax, positions, cube_types, title):
    colors = ["tab:blue", "tab:orange", "tab:green"]

    for cube_type in np.unique(cube_types):
        selected = cube_types == cube_type

        ax.scatter(
            positions[selected, 0],
            positions[selected, 1],
            positions[selected, 2],
            color=colors[int(cube_type)],
            label=f"Type {cube_type}",
            s=22,
        )

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")


fig = plt.figure(figsize=(16, 5))

ax1 = fig.add_subplot(131, projection="3d")
plot_configuration(
    ax1, initial_positions, initial_types,
    "Initial configuration"
)

ax2 = fig.add_subplot(132, projection="3d")
plot_configuration(
    ax2, final_positions, initial_types,
    "Optimized configuration"
)

ax3 = fig.add_subplot(133, projection="3d")
plot_configuration(
    ax3, target_positions, target_types,
    "Target configuration"
)

all_positions = np.vstack([
    initial_positions,
    final_positions,
    target_positions,
])

lower = all_positions.min(axis=0)
upper = all_positions.max(axis=0)

for ax in (ax1, ax2, ax3):
    ax.set_xlim(lower[0], upper[0])
    ax.set_ylim(lower[1], upper[1])
    ax.set_zlim(lower[2], upper[2])
    ax.set_box_aspect(np.maximum(upper - lower, 1))
    ax.view_init(elev=25, azim=45)

ax1.legend(loc="upper left", fontsize=8)

fig.suptitle(
    "ESA Programmable Cubes — ISS Optimization",
    fontsize=14,
)

plt.tight_layout()
output_path = RESULTS / "iss_best_configuration.png"
plt.savefig(output_path, dpi=180)
plt.show()

print("\n--- ISS Visualization Results ---")
print("Correct cubes:", placement["correct_cubes"])
print("Total cubes:", placement["total_cubes"])
print("Successful moves:", placement["successful_moves"])
print("Rejected moves:", placement["rejected_moves"])
print("Figure saved:", output_path)
