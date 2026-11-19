# ESA Programmable Cubes — DAA Project

## Project Overview

This project investigates optimization algorithms for the European Space Agency (ESA) SpOC-3 Programmable Cubes challenge.

It was developed as part of the **Design and Analysis of Algorithms (DAA)** course.

The objective is to find sequences of movement commands that transform an initial configuration of programmable cubes toward a target configuration while improving the official ESA fitness score.

Three scenarios were investigated:

| Scenario   | Number of Cubes | Cube Types | Maximum Commands |
| ---------- | --------------: | ---------: | ---------------: |
| ISS        |             148 |          3 |           10,000 |
| JWST       |             643 |          6 |           30,000 |
| Enterprise |           1,472 |         10 |          100,000 |

All reported solutions are evaluated using ESA's official fitness function, where **lower fitness values indicate better results**.

The project focuses on implementing, analyzing, and experimentally comparing optimization algorithms rather than claiming complete assembly of every target configuration.

## Algorithms Implemented

The project implements and evaluates several optimization approaches:

1. Random Search
2. Hill Climbing
3. Legal-Move Search
4. Hybrid Search
5. Target-Guided Hybrid Search
6. Assignment-Guided Hybrid Search
7. Legal-Aware Hybrid Search
8. Mutation-Based Refinement

Additional experiments investigate optimization budgets, legal-movement initialization, mutation sizes, suffix mutations, and middle-chromosome mutations.

Not every algorithm variant was tested in every scenario. The ISS experiments include additional guided and legal-aware approaches, while JWST and Enterprise focus on baseline algorithms, Hybrid Search, and refinement.

## Technologies

- Python 3.12
- NumPy
- Numba
- SciPy
- Matplotlib
- PyGMO
- pytest
- Visual Studio Code
- Kaggle CPU

Python implementations were developed and tested in VS Code.

Computationally intensive optimization experiments were executed on Kaggle using the official ESA simulator.

## Project Structure

The main project directories are organized as follows:

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
│   ├── visualize_iss.py
│   ├── jwst/
│   │   ├── jwst_fitness.py
│   │   ├── jwst_random_search.py
│   │   ├── jwst_hill_climbing.py
│   │   ├── jwst_hybrid_search.py
│   │   └── ...
│   └── enterprise/
│       ├── enterprise_fitness.py
│       ├── enterprise_random_search.py
│       ├── enterprise_hill_climbing.py
│       ├── enterprise_legal_move_search.py
│       ├── enterprise_hybrid_search.py
│       ├── enterprise_refinement_search.py
│       ├── enterprise_experiments.py
│       └── enterprise_experiment_analysis.py
├── tests/
│   └── ...
├── docs/
│   ├── complexity-analysis.md
│   ├── iss-experiment-results.md
│   ├── jwst-experiment-results.md
│   └── enterprise-experiment-results.md
├── notebooks/
│   └── ...
├── results/
│   ├── jwst/
│   ├── enterprise/
│   ├── best_iss_chromosome.npy
│   ├── best_iss_mutation.npy
│   └── ...
├── esa-reference/
│   └── Challenge 3 Programmable Cubes/
└── README.md
```

The directory tree shows the main components rather than every generated file or experiment script.

## Environment Setup

A Python 3.12 environment is recommended.

Using Conda:

```bash
conda create -n programmable-cubes python=3.12
conda activate programmable-cubes
conda install numpy numba scipy matplotlib pygmo pytest
```

The project also requires the official ESA Programmable Cubes reference implementation and scenario data.

The expected location is:

```text
esa-reference/Challenge 3 Programmable Cubes/
```

ESA reference files are maintained separately from the project's own algorithm implementations.

## Running the Project

Activate the Python environment from the repository root:

```bash
conda activate programmable-cubes
```

### ISS Optimization

Run the main Hybrid Search experiment:

```bash
python src/optimize_iss.py
```

Compare legal-aware suffix mutation sizes:

```bash
python src/compare_mutation_sizes.py
```

Visualize the best saved ISS solution:

```bash
python src/visualize_iss.py
```

### JWST Optimization

JWST algorithms and experiment scripts are available in:

```text
src/jwst/
```

The computationally intensive JWST experiments were executed on Kaggle.

### Enterprise Optimization

Enterprise algorithms and experiment scripts are available in:

```text
src/enterprise/
```

The main experiment runner is:

```text
src/enterprise/enterprise_experiments.py
```

The Enterprise analysis script can be executed locally using previously saved results:

```bash
python src/enterprise/enterprise_experiment_analysis.py
```

This generates the Enterprise comparison and convergence graphs without rerunning the ESA optimization experiments.

### Automated Tests

Run the complete test suite:

```bash
python -m pytest tests/ -q
```

The project includes automated tests for chromosome generation, mutation, legal-movement logic, optimization algorithms, refinement, and selected saved-solution checks.

Tests based on mocked simulator behavior verify implementation logic; official fitness scores were separately validated using ESA's real simulator.

## Best Experimental Results

The following table summarizes the strongest verified fitness values obtained during the reported experiments.

| Scenario   | Best ESA Fitness | Commands |
| ---------- | ---------------: | -------: |
| ISS        |    -0.1009994121 |      100 |
| JWST       |    -0.0605711111 |      300 |
| Enterprise |    -0.0151087637 |      100 |

These values represent the best solutions found during the experiments.

They do not imply that every cube reached its target position. Fitness values from different scenarios should not be treated as directly comparable measures of assembly completeness.

---

## ISS Scenario — Optimization Results

The ISS scenario contains **148 cubes across three cube types**.

### Baseline Algorithm Comparison

A five-seed comparison was performed using 100 fitness evaluations.

| Algorithm     | Average Fitness | Average Correct Cubes |
| ------------- | --------------: | --------------------: |
| Random Search |       -0.020047 |                  24.8 |
| Hill Climbing |       -0.034333 |                  26.6 |
| Hybrid Search |       -0.050206 |                  28.6 |

Hybrid Search achieved the strongest average performance among the three baseline approaches.

Increasing the Hybrid Search evaluation budget from 100 to 300 improved its average fitness from -0.050206 to -0.067666.

Further improvements were obtained through legal-aware suffix mutation experiments.

### Best Verified ISS Solution

| Metric                     |               Result |
| -------------------------- | -------------------: |
| Best ESA fitness           | -0.10099941211052317 |
| Correctly positioned cubes |             35 / 148 |
| Successful movements       |                   61 |
| Rejected movements         |                   39 |
| Total movement commands    |                  100 |

Best saved chromosome:

`results/best_iss_mutation.npy`

Visualization:

`results/iss_best_configuration.png`

The complete target configuration was not achieved.

Detailed analysis is available in [ISS Experiment Results](docs/iss-experiment-results.md).

---

## JWST Scenario — Optimization Results

The JWST scenario contains **643 cubes across six cube types**.

The implemented approaches include Random Search, Hill Climbing, Legal-Move Search, Hybrid Search, and Checkpoint-Based Refinement.

### Optimization Progress

| Optimization Stage                |  Best Fitness |
| --------------------------------- | ------------: |
| Initial local optimization        |     -0.038571 |
| Hybrid Search — 900 evaluations   |     -0.046571 |
| Hybrid Search — 3,000 evaluations |     -0.056571 |
| Checkpoint-Based Refinement       | **-0.060571** |

**Best verified JWST fitness: -0.06057111111111108**

The final refinement experiments tested different mutation sizes and preserved the strongest chromosome.

The reported result was verified using the official ESA simulator.

### JWST Experimental Evidence

Generated visualizations:

- `results/jwst/jwst_fitness_progress.png`
- `results/jwst/jwst_mutation_comparison.png`
- `results/jwst/jwst_refinement_convergence.png`

The JWST implementation is located in `src/jwst/`.

See [JWST Experiment Results](docs/jwst-experiment-results.md) for detailed methodology and analysis.

The complete target configuration was not achieved.

---

## Enterprise Scenario — Optimization Results

The Enterprise scenario contains **1,472 cubes across ten cube types**, making it the largest of the three investigated scenarios.

The optimization experiments used 100-command chromosomes.

### Initial Experiment — Enterprise V1

Three algorithms were compared across seeds 10, 20, and 30, using 20 evaluations per run.

| Algorithm     |     Mean Fitness |     Best Fitness |
| ------------- | ---------------: | ---------------: |
| Random Search |     -0.004251956 |     -0.005425665 |
| Hill Climbing |     -0.002491393 |     -0.003665102 |
| Hybrid Search | **-0.005132238** | **-0.005425665** |

Hybrid Search achieved the best mean fitness in the initial experiment.

### Extended Experiment — Enterprise V2

The evaluation budget was increased to 100 evaluations per run, with 100 commands per chromosome.

| Algorithm     |          Seed 10 |          Seed 20 |          Seed 30 |
| ------------- | ---------------: | ---------------: | ---------------: |
| Random Search |     -0.005425665 |     -0.003665102 |     -0.004545383 |
| Hill Climbing |     -0.010707355 |     -0.006305947 |     -0.008066510 |
| Hybrid Search | **-0.012467919** | **-0.009827074** | **-0.008066510** |

The extended comparison consisted of nine runs and 900 requested fitness evaluations.

Hybrid Search achieved the best result for Seeds 10 and 20 and tied with Hill Climbing for Seed 30.

**Best optimization fitness: -0.012467918622848122**

### Refinement Experiments

The best Hybrid Search chromosome was selected as the baseline for mutation-based refinement.

Three mutation sizes were tested, each with 100 evaluations.

| Mutation Size |     Best Fitness | Improvements |
| ------------- | ---------------: | -----------: |
| 1 command     |     -0.013348200 |            1 |
| 3 commands    | **-0.015108764** |            3 |
| 10 commands   | **-0.015108764** |            3 |

The 3-command and 10-command strategies reached the same best fitness.

Mutation size 3 was selected as the representative best solution, while both resulting chromosomes were preserved.

### Best Verified Enterprise Solution

| Metric                    |                     Result |
| ------------------------- | -------------------------: |
| Best ESA fitness          |      -0.015108763693270667 |
| Movement commands         |                        100 |
| Optimization method       | Hybrid Search + Refinement |
| Selected mutation size    |                          3 |
| Official ESA verification |                     Passed |

### Enterprise Experimental Evidence

Generated visualizations:

- `results/enterprise/enterprise_fitness_comparison.png`
- `results/enterprise/enterprise_mutation_comparison.png`
- `results/enterprise/enterprise_refinement_convergence.png`

The `results/enterprise/` folder also contains checkpoint archives, experiment statistics, and best chromosomes.

Detailed methodology, results, visualizations, and limitations are documented in [Enterprise Experiment Results](docs/enterprise-experiment-results.md).

---

## Complexity Analysis

The project analyzes the theoretical time and auxiliary space complexity of its search and refinement algorithms.

The analysis considers:

- Number of cubes
- Movement-command sequence length
- Number of fitness evaluations
- Mutation size
- Legal-movement generation attempts
- ESA simulator evaluation cost

The simulator's internal evaluation cost is treated separately from the Python search logic where necessary.

See [Algorithm Complexity Analysis](docs/complexity-analysis.md).

## Results and Reproducibility

The `results/` directory contains experimental evidence, including:

- Saved chromosomes (`.npy`)
- Recorded statistics (`.json`)
- Fitness comparison graphs (`.png`)
- Kaggle checkpoint archives (`.zip`)

The `notebooks/` directory contains notebook-based experiment work.

The project follows a workflow in which algorithm source code is maintained in VS Code, computationally intensive fitness evaluations are executed on Kaggle, and results are transferred back into the repository for analysis.

Random seeds, evaluation budgets, and mutation settings are recorded to support reproducibility.

## Limitations

The experiments have several limitations:

- None of the reported best solutions demonstrates complete assembly of its respective target configuration.
- The comparison experiments use a limited number of random seeds.
- Evaluation budgets and command lengths were substantially below the maximum permitted commands.
- Optimization methods may become trapped in local optima.
- Hybrid Search performs additional legal-movement generation work beyond counted fitness evaluations.
- Larger experiments could provide stronger statistical evidence and potentially better solutions.

The project reports the best solutions found under the tested settings rather than claiming globally optimal configurations.

## Conclusion

This project demonstrates the implementation, testing, and experimental evaluation of optimization algorithms for ESA's SpOC-3 Programmable Cubes challenge.

Three scenarios—ISS, JWST, and Enterprise—were investigated using random search, local optimization, legal-movement strategies, hybrid approaches, and mutation-based refinement.

Hybrid Search produced strong results across the tested scenarios, and refinement strategies further improved the best solutions.

The project provides a reproducible experimental framework for studying optimization techniques, algorithm complexity, movement constraints, and the impact of computational budgets on solution quality.
