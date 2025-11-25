# Testing Classical and Hybrid Quantum Solvers for Special and Euclidean Traveling Salesman Problem Instances
## A Comparative Study of a Classical Algorithm, Heuristics, and Hybrid Quantum Annealers

**Jedidiah T. Ramos**

## Abstract
A [classical algorithm](/TSPArithmeticSeriesPartialSolver.py) is tested against hybrid quantum annealers for special cases of the Traveling Salesman Problem where the weights of the edges in a graph form an arithmetic progression. The classical algorithm, Christofides, Nearest Neighbor, Simulated Annealing, Ant Colony Optimization, Genetic Algorithm, and D-Wave hybrid quantum annealers are also tested on the Euclidean Traveling Salesman Problem. D-Wave never outperformed the classical algorithm within its specified scope but outperformed all classical algorithms and heuristics for the Euclidean Traveling Salesman Problem before being overtaken at larger problem sizes.

## How the Classical Algorithm Works
Given a symmetric adjacency matrix for an n-vertex undirected graph with positive edge weights that form an arithmetic series, as well as a boundary choice of either 1 or 2, the classical algorithm first pre-computes the factorials 0! until n!. If the instance is small enough depending on the boundary choice, it is solved by brute force. Otherwise, the algorithm relabels the vertices to make an adjusted adjacency matrix by letting the first relabeled vertex be one that is incident to the edge with the minimum weight, then the next relabeled vertex is the nearest neighbor, and then the nearest neighbor's nearest neighbor, and so on. The code implementation for finding nearest neighbors in both the [classical algorithm](/TSPArithmeticSeriesPartialSolver.py) and the [Nearest Neighbor heuristic](/NearestNeighborHeuristics.py) uses a doubly linked list in the form of an array to remove each visited vertex in constant time and to search through remaining vertices more quickly. The algorithm then reads the adjusted matrix diagonally to collect the edge weights and then sorts the edge weights. An array of mileposts is used to track sub-arrays of duplicate edge weights in the sorted list. Using binary search on the sorted edge weights, the initially unsorted edge weights are rewritten as a permutation of {0, 1, ..., n - 1} so that [Bonet's algorithm](https://bonetblai.github.io/reports/AAAI08-ws10-ranking.pdf) can be used to lexicographically rank the permutation. If the rank of the permutation exceeds the maximum value allowed by the boundary formula depending on the boundary choice, then the optimal tour is unknown. Otherwise, the shortest tour among tours of rank 0 or 1 or (n - 2)! - 1 is the optimal tour for the adjusted adjacency matrix. The final tour is re-adjusted for the initial adjacency matrix.

## Two Phases of Experiments
There are two phases of experiments.

In the first phase, the [classical algorithm](/TSPArithmeticSeriesForExperiment.py) is tested against D-Wave's LeapHybridNLSampler.

In the [second phase](/quantumtsp.py), the [classical algorithm](/EuclideanTSPArithmeticSeriesForExperiment.py), [Christofides](/ChristofidesAlgorithm.py), [Nearest Neighbor](/NearestNeighborHeuristics.py), [Simulated Annealing](/SimulatedAnnealing.py), [Ant Colony Optimization](/AntColonyOptimization.py), [Genetic Algorithm](/TSPGeneticAlgorithm.py), and D-Wave's LeapHybridNLSampler are tested against each other on the [Euclidean Traveling Salesman Problem](/EuclideanTSPHeuristics.py), where n points in two dimensions are [randomly generated](/RandomPointsGenerator.py), with every coordinate being an integer at least 0 and at most 5000. For more experimental data in the second phase, the average difference, variance of differences, and standard deviation of differences between consecutive sorted edge weights are [computed](/ArithmeticSeriesMeasurement.py).

## Code Implementations
The code implementations for D-Wave, Prim's algorithm (for [1-tree lower bounds](/OneTreeLowerBound.py)), the Christofides algorithm, Simulated Annealing, Ant Colony Optimization, and Genetic Algorithm are from the following GitHub repositories.

**DWAVE Traveling Salesperson Example:**
https://docs.ocean.dwavesys.com/en/stable/examples/nl_tsp.html

**Prim's Algorithm:**
https://www.w3schools.com/dsa/dsa_algo_mst_prim.php

**Christofides Algorithm:**
https://github.com/Retsediv/ChristofidesAlgorithm

**Simulated Annealing:**
https://github.com/chncyhn/simulated-annealing-tsp

**Ant Colony Optimization:**
https://github.com/ppoffice/ant-colony-tsp

**Genetic Algorithm:**
https://github.com/hassanzadehmahdi/Traveling-Salesman-Problem-using-Genetic-Algorithm

The code implementations were modified for this project.

Christofides is run 5 times because its code implementation is not deterministic. Odd-degree vertices are randomly shuffled to find minimum weight perfect matchings.

Nearest Neighbor is run n times to try every vertex as a starting point.

Simulated Annealing runs until it reaches the stopping temperature or stopping iteration of n * 100.

Ant Colony Optimization runs with 20 ants for 10 generations. In the first generation, the first three ants are initialized with the best initial tour from the classical algorithm for arithmetic series, the Christofides algorithm, and the Nearest Neighbor algorithm, where the sequence of vertices is rotated for some ants. For some variables in the code, errors can happen if their values become too large, so they are set to the maximum float value in those cases.

Genetic Algorithm runs with n chromosomes for 100 generations. In the first generation, the first three chromosomes are initialized with the best initial tour from the classical algorithm for arithmetic series, the Christofides algorithm, and the Nearest Neighbor algorithm, where the sequence of vertices is rotated for some chromosomes.

## Experimental Data
Experimental results are available in the following files in the form of original text files and organized spreadsheets.

**Special TSP (Arithmetic Series):**
- Text file of arithmetic series TSP data
- [Spreadsheet of arithmetic series TSP data](/ExperimentalData/ArithmeticSeriesTSPData.xlsx)

**Euclidean TSP**
- Text file of Euclidean TSP data
- [Spreadsheet of Euclidean TSP data](/ExperimentalData/EuclideanTSPData.xlsx)
