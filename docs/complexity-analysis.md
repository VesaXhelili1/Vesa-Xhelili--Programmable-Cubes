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
