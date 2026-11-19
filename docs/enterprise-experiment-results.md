# Enterprise — Experiment Results

## 1. Problem Description

The Enterprise scenario is part of ESA's SpOC-3
Programmable Cubes challenge.

The objective is to optimize movement-command sequences
that transform an initial cube configuration toward a
target configuration.

### Enterprise Configuration

- Number of cubes: 1,472
- Number of cube types: 10
- Maximum permitted commands: 100,000
- Commands used in the reported experiments: 100

Each chromosome represents a sequence of cube movement
commands, followed by the termination marker -1.

Solutions are evaluated using ESA's official fitness
function. Lower fitness values indicate better results.

## 2. Implemented Algorithms

### Random Search

Random Search generates candidate chromosomes containing
random movement commands.

Each chromosome is evaluated independently, and the
algorithm retains the candidate with the lowest fitness.

### Hill Climbing

Hill Climbing starts with an initial chromosome and
repeatedly mutates selected commands.

A new candidate is accepted when its official ESA
fitness is lower than the current best value.

### Legal-Move Search

Legal-Move Search generates command sequences by
attempting movements and retaining accepted commands.

This helps construct chromosomes from movements that
are legal in the simulated cube configuration.

### Hybrid Search

Hybrid Search combines legal-movement initialization
with iterative mutation-based optimization.

It first generates a chromosome using accepted movements
and then improves that chromosome through mutations.

### Refinement Search

Refinement Search begins with a previously optimized
chromosome and explores additional mutations.

Three mutation sizes were investigated:

- 1 command
- 3 commands
- 10 commands

Each experiment starts from the same optimization baseline.

## 3. Experimental Environment

- Programming language: Python
- Development environment: Visual Studio Code
- Execution platform: Kaggle CPU
- Fitness evaluation: Official ESA simulator
- Numerical computation: NumPy
- Visualization: Matplotlib
- Automated testing: pytest

Source code was developed locally in VS Code.

Computationally intensive optimization experiments
were executed on Kaggle.

The results were saved as NumPy chromosomes, JSON
statistics, graphs, and checkpoint archives.

## 4. Fitness Evaluation Verification

During the final project audit, a sign inversion was
identified in the initial Enterprise fitness wrapper.

The original wrapper reversed the fitness value returned
by ESA's official evaluator.

This was corrected so that the wrapper directly returns
the official ESA fitness value.

The correction was verified using a direct comparison
between the wrapper and the official simulator.

An automated regression test was also added to ensure
that future changes do not reverse the fitness sign.

The corrected implementation passed all 23 Enterprise
automated tests.

The earlier Enterprise V1/V2 optimization results were
retained as historical checkpoints but excluded from
the final performance conclusions.

All results reported below use the corrected ESA fitness
direction.

## 5. Corrected Optimization Experiments — Enterprise V3

Three algorithms were evaluated:

- Random Search
- Hill Climbing
- Hybrid Search

### Experimental Settings

- Number of cubes: 1,472
- Chromosome length: 100 commands
- Seeds: 10, 20, 30
- Fitness evaluations per run: 100
- Mutation size for Hill Climbing and Hybrid Search: 10
- Number of algorithm runs: 9
- Total requested fitness evaluations: 900

Each completed result was verified using ESA's official
fitness evaluator.

### Results by Seed

| Algorithm     |      Seed 10 |      Seed 20 |      Seed 30 |
| ------------- | -----------: | -----------: | -----------: |
| Random Search | -0.003377152 | -0.004257433 | -0.003377152 |
| Hill Climbing | -0.006898279 | -0.008658842 | -0.007778560 |
| Hybrid Search | -0.007778560 | -0.009539124 | -0.007778560 |

### Mean and Best Fitness

| Algorithm     |     Mean Fitness |     Best Fitness |
| ------------- | ---------------: | ---------------: |
| Random Search |     -0.003670579 |     -0.004257433 |
| Hill Climbing |     -0.007778560 |     -0.008658842 |
| Hybrid Search | **-0.008365415** | **-0.009539124** |

Hybrid Search achieved the lowest mean fitness across
the three seeds.

It produced the best result for Seeds 10 and 20 and tied
with Hill Climbing for Seed 30.

### Best Optimization Result

- Algorithm: Hybrid Search
- Seed: 20
- Chromosome length: 100 commands
- Best official ESA fitness: -0.009539123630673031

Hybrid Search required additional movement attempts
during legal-movement initialization.

These operations are not included in the requested
fitness-evaluation count.

## 6. Corrected Refinement Experiments

The best corrected Hybrid Search chromosome was selected
as the starting point for further refinement.

### Refinement Settings

- Baseline algorithm: Hybrid Search
- Baseline seed: 20
- Baseline fitness: -0.009539123630673031
- Chromosome length: 100 commands
- Mutation sizes: 1, 3, 10 commands
- Evaluations per mutation size: 100
- Total requested refinement evaluations: 300

Each mutation-size experiment started from the same
corrected baseline chromosome.

### Refinement Results

| Mutation Size |     Best Fitness | Improvements | Runtime |
| ------------- | ---------------: | -----------: | ------: |
| 1 command     |     -0.011299687 |            2 | 11.03 s |
| 3 commands    |     -0.013060250 |            4 | 11.44 s |
| 10 commands   | **-0.013940532** |        **4** | 11.38 s |

### Refinement Analysis

The 1-command mutation experiment achieved two
improvements at evaluations 14 and 63.

The 3-command mutation experiment achieved four
improvements at evaluations 5, 11, 56, and 91.

The 10-command mutation experiment achieved four
improvements at evaluations 13, 36, 51, and 92.

Among the tested mutation sizes, the 10-command strategy
produced the lowest official ESA fitness.

## 7. Final Enterprise Result

The best verified Enterprise solution was obtained using
Hybrid Search followed by 10-command mutation refinement.

### Final Solution

- Scenario: Enterprise
- Number of cubes: 1,472
- Commands: 100
- Baseline algorithm: Hybrid Search
- Baseline seed: 20
- Selected mutation size: 10
- Final official ESA fitness: -0.013940532081377245
- Official fitness verification: Passed

The final chromosome is preserved in:

`results/enterprise/enterprise_v3_refined_best.npy`

The final corrected experiment statistics are available in:

`results/enterprise/enterprise_v3_final_summary.json`

`results/enterprise/enterprise_v3_refinement_summary.json`

These results represent the strongest solution found
during the reported experiments.

They do not demonstrate that all 1,472 cubes reached
their exact target positions.

## 8. Visualizations

Three graphs were generated from the corrected
Enterprise V3 experiment results.

### Algorithm Fitness Comparison

![Enterprise algorithm fitness comparison](../results/enterprise/enterprise_fitness_comparison.png)

### Mutation Size Comparison

![Enterprise mutation size comparison](../results/enterprise/enterprise_mutation_comparison.png)

### Refinement Convergence

![Enterprise refinement convergence](../results/enterprise/enterprise_refinement_convergence.png)

The graphs were generated using:

`src/enterprise/enterprise_experiment_analysis.py`

The analysis script uses saved experimental statistics
and does not require rerunning the optimization.

## 9. Algorithm Complexity

The project includes theoretical time and auxiliary
space complexity analysis for:

- Random Search
- Hill Climbing
- Legal-Move Generation
- Hybrid Search
- Mutation-Based Refinement

The complexity analysis considers the number of cubes,
chromosome length, mutation size, and number of fitness
evaluations.

ESA's simulator evaluation cost is represented
separately because its internal runtime depends on
the simulator implementation.

Detailed expressions and explanations are available in:

`docs/complexity-analysis.md`

## 10. Limitations

The experiments have several limitations:

- The chromosome length was limited to 100 commands.
- Three random seeds were used for algorithm comparisons.
- Each algorithm was tested with a limited evaluation budget.
- Hybrid Search performs additional legal-movement attempts
  beyond the counted fitness evaluations.
- The mutation-size comparison uses one experiment per size.
- The results do not establish global optimality.
- Complete Enterprise target assembly was not achieved.

Larger evaluation budgets, additional random seeds,
and longer chromosomes may produce better results.

## 11. Conclusion

The Enterprise experiments demonstrate the implementation
and evaluation of Random Search, Hill Climbing, Legal-Move
Search, Hybrid Search, and mutation-based refinement.

Using the corrected official ESA fitness function,
Hybrid Search achieved the best mean fitness in the
three-seed optimization comparison.

Mutation-based refinement further improved the best
Hybrid Search chromosome.

The strongest tested strategy was 10-command mutation
refinement, achieving an official ESA fitness of:

**-0.013940532081377245**

The final results are supported by saved chromosomes,
JSON statistics, graphs, automated tests, and Kaggle
experiment checkpoints.

The project provides reproducible experimental evidence
for comparing optimization strategies on the Enterprise
Programmable Cubes scenario.
