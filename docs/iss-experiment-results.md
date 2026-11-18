# ISS Programmable Cubes — Experimental Results

## 1. Problem Overview

The ISS problem contains 148 programmable cubes
divided into three cube types.

The objective is to find a sequence of movements
that transforms the initial cube configuration
toward the target configuration.

Solutions are evaluated using ESA's official
fitness function, where lower values are better.

## 2. Algorithms Implemented

- Random Search
- Hill Climbing
- Legal-Move Search
- Hybrid Search
- Target-Guided Hybrid Search
- Assignment-Guided Hybrid Search
- Legal-Aware Hybrid Search

Additional experiments investigated:

- Different optimization budgets
- Different mutation sizes
- Middle-chromosome mutations

## 3. Baseline Algorithm Comparison

Five seeds were used with 100 fitness evaluations.

| Algorithm     | Average Fitness | Average Correct Cubes |
| ------------- | --------------: | --------------------: |
| Random Search |       -0.020047 |                  24.8 |
| Hill Climbing |       -0.034333 |                  26.6 |
| Hybrid Search |       -0.050206 |                  28.6 |

Hybrid Search performed best among these three
algorithms under the tested evaluation budget.

## 4. Hybrid Search Budget Comparison

| Evaluations | Average Fitness | Average Correct Cubes |
| ----------- | --------------: | --------------------: |
| 100         |       -0.050206 |                  28.6 |
| 300         |       -0.067666 |                  30.8 |

Increasing the evaluation budget improved the
average fitness and number of correctly positioned
cubes across the five tested seeds.

## 5. Target-Distance Heuristics

| Algorithm                | Average Fitness | Average Correct Cubes |
| ------------------------ | --------------: | --------------------: |
| Standard Hybrid          |       -0.050206 |                  28.6 |
| Target-Guided Hybrid     |       -0.043857 |                  27.8 |
| Assignment-Guided Hybrid |       -0.047031 |                  28.2 |

Both target-aware variants reduced their respective
geometric distance measurements, but neither
outperformed standard Hybrid Search in average
ESA fitness.

## 6. Legal-Aware Mutation Experiments

The legal-aware search retained an optimized prefix
and regenerated a suffix with legal movements.

Using smaller mutations improved the best saved
solution from 32 to 34 correctly positioned cubes.

Three suffix-mutation ranges were subsequently tested:

| Mutation Size  | Average Fitness | Average Correct Cubes |
| -------------- | --------------: | --------------------: |
| 1–5 commands   |       -0.095708 |                 34.33 |
| 5–10 commands  |       -0.095708 |                 34.33 |
| 10–20 commands |       -0.095708 |                 34.33 |

The three strategies produced identical average
results over three seeds. No strategy can be declared
superior based on this experiment.

A middle-mutation experiment with 299 attempts
did not improve the best saved solution.

## 7. Best Verified ISS Solution

- Correctly positioned cubes: 35 / 148
- Official ESA fitness: -0.10099941211052317
- Successful movements: 61
- Rejected movements: 39
- Chromosome length: 201
- Movement commands: 100

Saved chromosome:
`results/best_iss_mutation.npy`

Visualization:
`results/iss_best_configuration.png`

All 14 automated tests passed.

## 8. Limitations

The complete target configuration was not reached.

Some movement commands were rejected by the
simulator, reducing the effectiveness of the
generated sequences.

Results are based on a limited number of seeds
and evaluation budgets. More experiments would
be needed to establish statistically reliable
performance differences.

## 9. Conclusion

Hybrid Search provided stronger average results
than Random Search and Hill Climbing in the tested
baseline comparison.

Further improvement was achieved through
legal-aware suffix mutations.

The experiments demonstrate how algorithm design,
mutation strategy, search budget, and movement
constraints affect optimization performance.
