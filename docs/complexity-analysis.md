# Algorithm Complexity Analysis — ISS

## 1. Definitions

- n: Number of movement commands in a chromosome
- k: Number of candidate solutions evaluated
- m: Number of mutations per iteration
- c: Number of cubes in the ISS configuration
- a: Number of movement attempts during legal generation
- F(n, c): Cost of evaluating a chromosome using ESA's simulator
- V(c): Cost of validating and applying one attempted movement

For ISS:

- c = 148 cubes
- n = 100 commands in our main experiments

The simulator's internal operations are treated separately
because their exact complexity depends on ESA's implementation.

## 2. Random Search

Random Search generates k chromosomes and evaluates each one.

Chromosome generation requires O(n) time.

Time complexity:
O(k × (n + F(n, c)))

Auxiliary space complexity:
O(n), excluding simulator storage.

## 3. Hill Climbing

Hill Climbing begins with one chromosome, then repeatedly
mutates and evaluates candidate solutions.

Each mutation changes up to m commands.

Time complexity:
O(n + F(n, c) + k × (n + m + F(n, c)))

Auxiliary space complexity:
O(n), excluding simulator storage.

## 4. Legal-Move Search

Legal-Move Search generates movement commands while checking
whether each movement is valid in the current configuration.

If a movement attempt requires V(c) time:

Generation time:
O(a × V(c) + n)

Including one official fitness evaluation:
O(a × V(c) + n + F(n, c))

Auxiliary storage:
O(n + c), excluding simulator-internal temporary storage.

## 5. Hybrid Search

Hybrid Search combines legal initialization with
Hill Climbing-style mutations.

Time complexity:
O(a × V(c) + n + k × (n + m + F(n, c)))

Auxiliary space complexity:
O(n + c), excluding simulator storage.

## 6. Target-Distance Heuristic

The nearest-target heuristic compares cubes against
target positions of matching types.

A direct all-pairs implementation requires at most:

Time complexity:
O(c²)

Additional working space:
O(c), when distances are calculated without storing
the full pairwise distance matrix.

## 7. Assignment-Distance Heuristic

The assignment-based heuristic constructs distance
matrices and solves a minimum-cost assignment problem.

Using a cubic upper bound for square assignment problems:

Time complexity:
O(c³)

Space complexity:
O(c²)

This explains why assignment-guided search introduces
additional computational work.

## 8. Legal-Aware Suffix Mutations

Legal-Aware Hybrid Search retains an existing prefix and
regenerates the remaining commands using valid movements.

If each iteration makes a movement attempts:

Time per candidate:
O(n + a × V(c) + F(n, c))

For k iterations:
O(k × (n + a × V(c) + F(n, c)))

Auxiliary space complexity:
O(n + c), excluding simulator storage.

## 9. Discussion

Random Search provides a simple baseline.

Hill Climbing uses previous solutions to guide exploration.

Hybrid Search combines valid initial configurations with
iterative improvement.

Legal-Aware Hybrid Search uses the simulator's movement
constraints while constructing replacement commands.

Theoretical complexity alone does not determine which
algorithm produces the best solution. Solution quality
also depends on the fitness landscape, mutation strategy,
search budget, and movement constraints.

The complexity estimates are expressed using simulator
costs rather than assuming that all ESA operations take
constant time.

---

# JWST — Algorithm Complexity Analysis

## 1. Problem Size and Representation

The JWST scenario contains 643 cubes belonging to six cube types.

A candidate solution consists of a sequence of movement commands. Each command contains a cube identifier and a movement direction.

For a chromosome containing \(L\) commands, the representation contains \(2L+1\) elements, including the termination marker `-1`.

The experiments primarily used \(L=300\) movement commands.

For complexity analysis, define:

- \(L\): Number of movement commands in a chromosome.
- \(E\): Number of fitness evaluations.
- \(k\): Number of commands selected for mutation.
- \(A\): Total number of movement attempts during legal chromosome generation.
- \(F(L)\): Computational cost of evaluating a chromosome using ESA's simulator.
- \(S\): Number of independent optimization runs.

The simulator's cost is represented separately because its internal operations may depend on the cube configuration and movement outcomes.

## 2. Random Search

Random Search generates candidate chromosomes and evaluates them independently.

Generating a chromosome with \(L\) commands requires \(O(L)\) time and space.

For \(E\) evaluated candidates, the total time complexity is:

\[
O(E(L+F(L)))
\]

The chromosome storage requirement is \(O(L)\), excluding simulator memory and stored experiment history.

## 3. Hill Climbing

Hill Climbing begins with an initial chromosome and repeatedly evaluates mutated candidates.

Each mutation creates a copy of the chromosome, which costs \(O(L)\) time. Changing \(k\) selected commands adds mutation work.

For \(E\) fitness evaluations, the total time complexity is:

\[
O(E(L+F(L)))
\]

This expression assumes \(k\leq L\) and a bounded number of modifications per selected command.

The algorithm retains a current chromosome and candidate chromosome, requiring \(O(L)\) additional chromosome storage.

## 4. Legal Move Search

Legal Move Search attempts movement commands using ESA's simulator and retains accepted movements.

Let \(A\) be the number of attempted movements required to construct a chromosome with up to \(L\) accepted commands.

If \(U\) represents the cost of one simulator movement attempt, chromosome construction requires approximately:

\[
O(AU+L)
\]

The number of attempts may exceed the number of accepted commands because the simulator can reject illegal movements.

Therefore, legal move generation may require more simulator operations than ordinary random chromosome generation.

## 5. Hybrid Search

Hybrid Search combines legal move generation with iterative mutation and fitness evaluation.

The initialization cost depends on the number of legal movement attempts.

The subsequent search performs fitness evaluations on mutated chromosomes.

For one optimization run:

\[
O(AU+L+E(L+F(L)))
\]

For \(S\) independent runs of comparable size:

\[
O(S(AU+L+E(L+F(L))))
\]

This complexity explains why evaluation budget and legal-move generation cost should both be considered when comparing algorithms.

## 6. Checkpoint-Based Refinement

Checkpoint-Based Refinement starts from an existing optimized chromosome instead of generating a new random chromosome.

Each iteration:

1. Copies the current chromosome.
2. Selects \(k\) movement commands.
3. Modifies the selected commands.
4. Evaluates the candidate using the official fitness function.
5. Accepts the candidate if it improves fitness.
6. Saves newly discovered global-best solutions.

The per-evaluation cost is:

\[
O(L+F(L))
\]

Therefore, for \(E\) refinement evaluations:

\[
O(E(L+F(L)))
\]

For \(M\) mutation-size strategies, each receiving \(E\) evaluations:

\[
O(ME(L+F(L)))
\]

The implementation stores fitness histories, requiring an additional \(O(ME)\) space for the recorded statistics.

Checkpoint files require \(O(L)\) storage per saved chromosome.

## 7. Experimental Complexity and Interpretation

The larger JWST experiments used:

| Experiment                  | Evaluations |
| --------------------------- | ----------: |
| Kaggle Hybrid Search 1      |         900 |
| Kaggle Hybrid Search 2      |       3,000 |
| Checkpoint-Based Refinement |         900 |

The total evaluation count for these three experiments was 4,800.

This excludes earlier local experiments, initialization movement attempts, and final verification evaluations.

An equal number of fitness evaluations does not necessarily imply an equal computational workload, since legal movement generation and simulator operations may differ.

## 8. Summary

All implemented search approaches are heuristic methods.

Their computational requirements depend strongly on the number of candidate evaluations and the cost of ESA's simulator.

Random Search explores independent chromosomes, Hill Climbing searches neighboring solutions, Hybrid Search incorporates legal-move construction, and Checkpoint-Based Refinement improves a previously saved candidate.

The experiments provide empirical performance evidence but do not establish global optimality or guarantee that fitness will improve with every additional evaluation.
