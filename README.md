# Testing Classical and Hybrid Quantum Solvers for Special and Euclidean Traveling Salesman Problem Instances
## A Comparative Study of a Classical Algorithm, Heuristics, and Hybrid Quantum Annealers

**Jedidiah T. Ramos**

## Abstract
A [classical algorithm](docs/TSPArithmeticSeriesPartialSolver.py) is tested against hybrid quantum annealers for special cases of the Traveling Salesman Problem where the weights of the edges in a graph form an arithmetic progression. The classical algorithm, Christofides, Nearest Neighbor, Simulated Annealing, Ant Colony Optimization, Genetic Algorithm, and hybrid quantum annealers are also tested on the Euclidean Traveling Salesman Problem. The hybrid quantum annealers never outperformed the classical algorithm within its specified scope but outperformed all classical algorithms and heuristics for the Euclidean Traveling Salesman Problem before being overtaken at larger problem sizes.

## Code Implementation Sources
The code implementations for D-Wave, Prim's algorithm (for 1-tree lower bounds), the Christofides algorithm, Simulated Annealing, Ant Colony Optimization, and Genetic Algorithm are from the following GitHub repositories.

**DWAVE Traveling Salesperson Example**
https://docs.ocean.dwavesys.com/en/stable/examples/nl_tsp.html

**Prim's Algorithm**
https://www.w3schools.com/dsa/dsa_algo_mst_prim.php

**Christofides Algorithm**
https://github.com/Retsediv/ChristofidesAlgorithm

**Simulated Annealing**
https://github.com/chncyhn/simulated-annealing-tsp

**Ant Colony Optimization**
https://github.com/ppoffice/ant-colony-tsp

**Genetic Algorithm**
https://github.com/hassanzadehmahdi/Traveling-Salesman-Problem-using-Genetic-Algorithm
