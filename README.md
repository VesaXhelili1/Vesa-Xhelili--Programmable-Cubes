# ESA Programmable Cubes — DAA Project

## Project Overview

This project explores optimization algorithms for the ESA
SpOC-3 Programmable Cubes challenge.

It was developed as part of the Design and Analysis of
Algorithms (DAA) course.

The current implementation focuses on the ISS problem,
which contains 148 programmable cubes of three types.

The objective is to find sequences of movements that
transform the initial cube configuration toward ESA's
target configuration.

## Algorithms Implemented

The project implements and evaluates:

1. Random Search
2. Hill Climbing
3. Legal-Move Search
4. Hybrid Search
5. Target-Guided Hybrid Search
6. Assignment-Guided Hybrid Search
7. Legal-Aware Hybrid Search

Additional experiments investigate optimization budgets,
suffix mutation sizes, and middle-chromosome mutations.

All solutions are evaluated using ESA's official fitness
function, where lower values indicate better results.

## Technologies

- Python 3.12
- NumPy
- Numba
- SciPy
- Matplotlib
- PyGMO
- pytest

## Project Structure

```text
.
├── src/
│   ├── random_search.py
│   ├── hill_climbing.py
│   ├── legal_move_search.py
│   ├── hybrid_search.py
│   ├── target_heuristic.py
│   ├── target_guided_hybrid.py
│   ├── assignment_guided_hybrid.py
│   ├── legal_aware_hybrid.py
│   ├── middle_mutation_search.py
│   ├── optimize_iss.py
│   ├── compare_mutation_sizes.py
│   └── visualize_iss.py
├── tests/
├── docs/
│   ├── complexity-analysis.md
│   └── iss-experiment-results.md
├── results/
│   ├── best_iss_chromosome.npy
│   ├── best_iss_legal_aware.npy
│   ├── best_iss_mutation.npy
│   ├── iss_optimization_results.json
│   └── *.png
└── README.md
```

Additional comparison scripts are available in `src/`.

## Environment Setup

A Python 3.12 environment is recommended.

For example, using Conda:

```bash
conda create -n programmable-cubes python=3.12
conda activate programmable-cubes
conda install numpy numba scipy matplotlib pygmo pytest
```

The project also requires the official ESA Programmable
Cubes reference implementation and ISS data files.

Place the official reference implementation in the
directory expected by the source code:

`esa-reference/Challenge 3 Programmable Cubes/`

The ESA reference files are maintained separately
from this project's algorithm implementations.

## Running the Project

From the repository root, activate the Python environment.

Run the main Hybrid Search optimization experiment:

```bash
python src/optimize_iss.py
```

Compare legal-aware suffix mutation sizes:

```bash
python src/compare_mutation_sizes.py
```

Visualize the best saved solution:

```bash
python src/visualize_iss.py
```

Run all automated tests:

```bash
python -m pytest tests/ -v
```

## Experimental Results

Five-seed baseline comparison with 100 fitness evaluations:

| Algorithm     | Average Fitness | Average Correct Cubes |
| ------------- | --------------: | --------------------: |
| Random Search |       -0.020047 |                  24.8 |
| Hill Climbing |       -0.034333 |                  26.6 |
| Hybrid Search |       -0.050206 |                  28.6 |

Hybrid Search achieved the strongest average performance
among these three baseline approaches.

Increasing the Hybrid Search evaluation budget from
100 to 300 improved its average fitness from
-0.050206 to -0.067666.

Further improvements were obtained through legal-aware
suffix mutation experiments.

## Best Verified ISS Solution

The best saved solution achieved:

- Correctly positioned cubes: 35 / 148
- ESA fitness: -0.10099941211052317
- Successful movements: 61
- Rejected movements: 39
- Total movement commands: 100

The chromosome is saved at:

`results/best_iss_mutation.npy`

The visualization is saved at:

`results/iss_best_configuration.png`

## Testing

The project currently contains 14 automated tests.

Tests cover:

- Chromosome validity
- Random Search and Hill Climbing
- Movement success and legality
- Hybrid Search
- Target-distance calculations
- Saved ISS solution verification
- Deterministic solution replay

Latest test result: 14 passed.

## Complexity Analysis

The time and space complexity of the algorithms
is discussed in:

`docs/complexity-analysis.md`

Detailed experimental comparisons are available in:

`docs/iss-experiment-results.md`

## Limitations

The complete ISS target configuration has not been reached.

The best saved solution correctly positions 35 of the
148 cubes.

Some commands are rejected by the simulator, and the
search algorithms may become trapped in local optima.

The experimental results are based on limited random
seeds and evaluation budgets.

## Conclusion

The project demonstrates the implementation, evaluation,
and comparison of optimization algorithms for a
constrained movement problem.

Hybrid Search performed better than the tested
Random Search and Hill Climbing baselines.

Legal-aware suffix mutations further improved the
best obtained ISS solution.

The project provides a reproducible experimental
framework for studying optimization techniques,
algorithm complexity, and movement constraints.

---

## JWST Scenario — Optimization

The JWST scenario of ESA's SpOC-3 Programmable Cubes
challenge contains 643 cubes across six cube types.

### Implemented Algorithms

- Random Search
- Hill Climbing
- Legal Move Search
- Hybrid Search
- Checkpoint-Based Refinement Search

All algorithms use ESA's official fitness evaluator.

### Experimental Methodology

Algorithms were developed in Python using VS Code.
Computationally expensive experiments were executed
on Kaggle using CPU resources.

The project includes reproducible experiment scripts,
automated tests, saved chromosomes, and statistics.

### Best JWST Results

| Optimization Stage                | Best Fitness |
| --------------------------------- | -----------: |
| Initial local optimization        |    -0.038571 |
| Hybrid Search — 900 evaluations   |    -0.046571 |
| Hybrid Search — 3,000 evaluations |    -0.056571 |
| Checkpoint-Based Refinement       |    -0.060571 |

**Best verified fitness:** -0.06057111111111108

Lower fitness values are better.

These results demonstrate improvements in heuristic
optimization, not a globally optimal solution.

### Experimental Evidence

Generated visualizations:

- `results/jwst/jwst_fitness_progress.png`
- `results/jwst/jwst_mutation_comparison.png`
- `results/jwst/jwst_refinement_convergence.png`

Detailed experimental analysis:

- `docs/jwst-experiment-results.md`
- `docs/complexity-analysis.md`

### Automated Tests

The project passed 25 automated tests.

To execute the test suite:

```bash
python -m pytest tests/ -q
```

Computationally expensive optimization experiments
should be executed on Kaggle rather than locally.

### Implementation

JWST Python algorithms are located in `src/jwst/`.

The full ESA target configuration has not yet been
achieved.
