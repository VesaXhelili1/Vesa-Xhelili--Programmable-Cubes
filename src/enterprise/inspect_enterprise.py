
import json
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]

ESA_DIR = (
    ROOT
    / "esa-reference"
    / "Challenge 3 Programmable Cubes"
)

DATA_DIR = ESA_DIR / "data" / "Enterprise"
PROBLEM_PATH = ESA_DIR / "problems" / "Enterprise.json"


def inspect_enterprise():
    print("\n--- ENTERPRISE SCENARIO ---")

    with PROBLEM_PATH.open("r") as file:
        problem = json.load(file)

    print("\nProblem settings:")
    print(json.dumps(problem, indent=2))

    filenames = [
        "Initial_Config.npy",
        "Initial_Cube_Types.npy",
        "Target_Config.npy",
        "Target_Cube_Types.npy",
    ]

    arrays = {}

    for filename in filenames:
        path = DATA_DIR / filename

        if not path.exists():
            raise FileNotFoundError(path)

        arrays[filename] = np.load(path, allow_pickle=False)

    initial = arrays["Initial_Config.npy"]
    initial_types = arrays["Initial_Cube_Types.npy"]
    target = arrays["Target_Config.npy"]
    target_types = arrays["Target_Cube_Types.npy"]

    print("\n--- Configuration Shapes ---")
    print("Initial configuration:", initial.shape)
    print("Target configuration:", target.shape)
    print("Initial cube types:", initial_types.shape)
    print("Target cube types:", target_types.shape)

    print("\n--- Cube Information ---")
    print("Initial cubes:", len(initial_types))
    print("Target cubes:", len(target_types))

    print(
        "Initial type distribution:",
        dict(sorted(Counter(initial_types.flatten().tolist()).items()))
    )

    print(
        "Target type distribution:",
        dict(sorted(Counter(target_types.flatten().tolist()).items()))
    )

    print("\n--- Validation ---")
    print("Cube count matches:", len(initial_types) == len(target_types))
    print("Configuration shapes match:", initial.shape == target.shape)

    print("\nEnterprise inspection: PASSED")


if __name__ == "__main__":
    inspect_enterprise()
