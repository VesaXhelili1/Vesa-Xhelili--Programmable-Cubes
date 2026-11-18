
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

ESA = ROOT / "esa-reference" / "Challenge 3 Programmable Cubes"
DATA = ESA / "data" / "JWST"
PROBLEM = ESA / "problems" / "JWST.json"

print("--- JWST Problem Inspection ---")

if not DATA.exists() or not PROBLEM.exists():
    raise FileNotFoundError(
        "JWST reference files were not found."
    )

with open(PROBLEM) as file:
    problem = json.load(file)

print("Problem configuration keys:", list(problem.keys()))

files = [
    "Initial_Config.npy",
    "Initial_Cube_Types.npy",
    "Target_Config.npy",
    "Target_Cube_Types.npy",
]

for filename in files:
    array = np.load(DATA / filename)

    print(f"\n{filename}")
    print("Shape:", array.shape)
    print("Data type:", array.dtype)

    if "Types" in filename:
        unique, counts = np.unique(
            array,
            return_counts=True
        )
        print("Cube type counts:", dict(zip(
            unique.tolist(),
            counts.tolist()
        )))

print("\nJWST inspection: COMPLETED")
