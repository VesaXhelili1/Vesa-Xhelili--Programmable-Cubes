# JWST Programmable Cubes — Experimental Results

## 1. Objective

The objective of this experiment is to investigate heuristic optimization algorithms for the JWST scenario of ESA's SpOC-3 Programmable Cubes challenge.

The JWST scenario contains 643 programmable cubes across six cube types. Candidate solutions are represented as chromosomes containing sequences of cube movement commands.

The official ESA simulator evaluates each chromosome through its fitness function. The optimization objective is to minimize the reported fitness value.

## 2. Implemented Algorithms

Four foundational search approaches were implemented:

- **Random Search:** Generates random candidate chromosomes and evaluates their fitness.
- **Hill Climbing:** Iteratively modifies candidate solutions and retains improvements.
- **Legal Move Search:** Constructs chromosomes using movement commands accepted by the simulator.
- **Hybrid Search:** Combines legal movement generation with iterative mutation-based optimization.

An additional **Checkpoint-Based Refinement Search** was implemented to improve an already optimized chromosome by modifying a selected number of movement commands.

## 3. Experimental Environment

Algorithms were developed in Python using VS Code.

Lightweight automated tests were executed locally. Computationally intensive experiments were executed using Kaggle's CPU environment and ESA's official Programmable Cubes simulator.

All optimized chromosomes and experimental statistics were saved for later verification and analysis.

## 4. Hybrid Search Experiments

Hybrid Search was evaluated using 300 movement commands per chromosome.

| Experiment                 | Random Seeds              | Evaluations per Seed |         Total Evaluations | Best Fitness |
| -------------------------- | ------------------------- | -------------------: | ------------------------: | -----------: |
| Initial local optimization | 30 (best-performing seed) |                  100 | Part of local experiments |    -0.038571 |
| Kaggle Hybrid Search 1     | 10, 20, 30                |                  300 |                       900 |    -0.046571 |
| Kaggle Hybrid Search 2     | 40, 50, 60                |                1,000 |                     3,000 |    -0.056571 |

The results demonstrate that increasing the evaluation budget and exploring additional random seeds produced progressively better solutions in these experiments.

The values represent observed best results. They do not establish that additional evaluations will always improve fitness.

## 5. Checkpoint-Based Refinement

The best Hybrid Search chromosome, with fitness -0.056571, was used as the starting solution for refinement.

Three mutation strategies were compared. Each strategy received 300 fitness evaluations and began from the same baseline.

| Mutation Size | Evaluations | Accepted Improvements | Final Fitness |
| ------------- | ----------: | --------------------: | ------------: |
| 1 command     |         300 |                     0 |     -0.056571 |
| 3 commands    |         300 |                     1 |     -0.058571 |
| 10 commands   |         300 |                     2 |     -0.060571 |

The best refinement result was obtained with a mutation size of 10 commands, reaching a fitness of -0.060571.

These findings are specific to the tested configuration and random-number initialization. Additional independent trials would be required to compare mutation strategies more confidently.

## 6. Fitness Progression

The best verified fitness changed across the optimization stages:

| Stage                       | Best Fitness |
| --------------------------- | -----------: |
| Local Hybrid Search         |    -0.038571 |
| Kaggle Hybrid Search 1      |    -0.046571 |
| Kaggle Hybrid Search 2      |    -0.056571 |
| Checkpoint-Based Refinement |    -0.060571 |

The final refinement score improved fitness by approximately 0.022 relative to the original local best.

Three graphs document these results:

- `results/jwst/jwst_fitness_progress.png`
- `results/jwst/jwst_mutation_comparison.png`
- `results/jwst/jwst_refinement_convergence.png`

## 7. Reproducibility and Verification

The project retains the Python implementations, automated tests, experimental parameters, checkpoint files, and generated result statistics.

The JWST refinement algorithm passed four targeted unit tests. The complete local automated test suite passed 25 tests.

The final chromosome was evaluated again using ESA's fitness evaluator, producing:

**Best verified JWST fitness: -0.06057111111111108**

The result is a verified improvement under the official evaluator, not proof of globally optimal cube placement.

## 8. Limitations

The experiments have several limitations:

- JWST's full target configuration has not been achieved.
- The optimization remains heuristic, without a global optimality guarantee.
- Results are sensitive to random initialization and evaluation budget.
- The refinement mutation-size comparison used one seeded trial per strategy.
- Computational budgets do not necessarily represent equal total simulator work across different search algorithms.

## 9. Conclusion

The experiments demonstrate that Hybrid Search can improve on simpler search approaches under the tested conditions and that checkpoint-based refinement can further improve an already optimized chromosome.

The best verified JWST fitness achieved so far is **-0.06057111111111108**.

Future work may investigate repeated refinement trials, more effective mutation operators, movement-aware neighborhood selection, and the larger Enterprise scenario.
