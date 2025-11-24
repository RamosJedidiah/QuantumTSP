# Testing Classical and Hybrid Quantum Solvers for Special and Euclidean Traveling Salesman Problem Instances
## A Comparative Study of a Classical Algorithm, Heuristics, and Hybrid Quantum Annealers

**Jedidiah T. Ramos**

## Abstract
A [classical algorithm](./TSPArithmeticSeriesPartialSolver.py) is tested against hybrid quantum annealers for special cases of the Traveling Salesman Problem where the weights of the edges in a graph form an arithmetic progression. The classical algorithm, Christofides, Nearest Neighbor, Simulated Annealing, Ant Colony Optimization, Genetic Algorithm, and hybrid quantum annealers are also tested on the Euclidean Traveling Salesman Problem. The hybrid quantum annealers never outperformed the classical algorithm within its specified scope but outperformed all classical algorithms and heuristics for the Euclidean Traveling Salesman Problem before being overtaken at larger problem sizes.

## How the Classical Algorithm Works
Given a symmetric adjacency matrix for an n-vertex undirected graph with positive edge weights that form an arithmetic series, as well as a boundary choice of either 1 or 2, the classical algorithm first pre-computes the first n + 1 factorials. If the instance is small enough depending on the boundary choice, it is solved by brute force. Otherwise, the algorithm relabels the vertices to make an adjusted adjacency matrix by letting the first relabeled vertex be one that is incident to the edge with the minimum weight, then the next relabeled vertex is the nearest neighbor, and then the next nearest neighbor, and so on. The code implementation for finding nearest neighbors in both the classical algorithm and the Nearest Neighbor heuristic uses a doubly linked list in the form of an array to remove each visited vertex in constant time and to search through remaining vertices more quickly. The algorithm then reads the adjusted matrix diagonally to collect the edge weights and then sorts the edge weights. An array of mileposts is used to track sub-arrays of duplicate edge weights in the sorted list. Using binary search on the sorted edge weights, the initially unsorted edge weights are rewritten as a permutation of {0, 1, ..., n - 1} so that Bonet's algorithm can be used to lexicographically rank the permutation. If the rank of the permutation exceeds the maximum value allowed by the boundary formula depending on the boundary choice, then the optimal tour is unknown. Otherwise, the shortest tour among tours of rank 0 or 1 or (n - 2)! - 1 is the optimal tour for the adjusted adjacency matrix. The final tour is re-adjusted for the initial adjacency matrix.

## Code Implementation Sources
The code implementations for D-Wave, Prim's algorithm (for 1-tree lower bounds), the Christofides algorithm, Simulated Annealing, Ant Colony Optimization, and Genetic Algorithm are from the following GitHub repositories.

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
