import random
import math
import sys
from timeit import default_timer as timer


class Graph(object):
    def __init__(self, cost_matrix: list, rank: int):
        """
        :param cost_matrix:
        :param rank: rank of the cost matrix
        """
        self.matrix = cost_matrix
        self.rank = rank
        # noinspection PyUnusedLocal
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, rho: float, q: int,
                 strategy: int):
        """
        :param ant_count:
        :param generations:
        :param alpha: relative importance of pheromone
        :param beta: relative importance of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy

    def _update_pheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    # noinspection PyProtectedMember
    def solve(self, graph: Graph, initial_heuristic_tour, initial_heuristic_distance):
        """
        :param graph:
        """
        # INITIALIZE WITH BEST INITIAL HEURISTIC SOLUTION
        best_cost = initial_heuristic_distance
        best_solution = initial_heuristic_tour
        best_generation = 0
        for gen in range(self.generations):
            # noinspection PyUnusedLocal
            ants = [_Ant(self, graph) for i in range(self.ant_count)]
            ant_index = 0
            for ant in ants:
                if gen == 0 and ant_index < 3:
                    # FIRST THREE ANTS
                    ant.allowed = [i for i in range(graph.rank)]
                    # SHIFT CITY INDEX
                    first_city = initial_heuristic_tour[ant_index]
                    ant.tabu = [first_city]
                    ant.current = first_city
                    ant.allowed.remove(first_city)
                    for i in range(1, graph.rank):
                        # SHIFT CITY INDEX
                        ith_city = initial_heuristic_tour[(i + ant_index) % graph.rank]
                        ant.allowed.remove(ith_city)
                        ant.tabu.append(ith_city)
                        ant.total_cost += ant.graph.matrix[ant.current][ith_city]
                        ant.current = ith_city
                else:
                    # OTHER ANTS
                    for i in range(graph.rank - 1):
                        ant._select_next()
                ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tabu
                    best_generation = gen + 1
                # update pheromone
                ant._update_pheromone_delta()
                ant_index += 1
            self._update_pheromone(graph, ants)
            # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
        return best_solution, best_cost, best_generation


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # tabu list
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(graph.rank)]  # nodes which are allowed for the next selection
        self.eta = [[0 if i == j else (sys.float_info.max if graph.matrix[i][j] == 0 else 1 / graph.matrix[i][j]) for j in range(graph.rank)] for i in
                    range(graph.rank)]  # heuristic information
        start = random.randint(0, graph.rank - 1)  # start from any node
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _select_next(self):
        denominator = 0
        for i in self.allowed:
            try:
                denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta
            except:
                denominator = sys.float_info.max
        # noinspection PyUnusedLocal
        probabilities = [0 for i in range(self.graph.rank)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                try:
                    probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                        self.eta[self.current][i] ** self.colony.beta / denominator
                except:
                    probabilities[i] = sys.float_info.max / denominator
            except ValueError:
                pass  # do nothing
        # select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    # noinspection PyUnusedLocal
    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                # noinspection PyTypeChecker
                self.pheromone_delta[i][j] = sys.float_info.max if self.graph.matrix[i][j] == 0 else self.colony.Q / self.graph.matrix[i][j]
            else:  # ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def start_ant_colony(data, n, initial_heuristic_tour, initial_heuristic_distance):
    cities = []
    points = []
    for i in range(n):
        cities.append(dict(index=int(i + 1), x=int(data[i][0]), y=int(data[i][1])))
        points.append((int(data[i][0]), int(data[i][1])))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)

    generation_count = 10

    start = timer()
    aco = ACO(20, generation_count, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost, best_generation = aco.solve(graph, initial_heuristic_tour, initial_heuristic_distance)
    end = timer()
    duration = end - start

    print("ANT COLONY OPTIMIZATION TOUR:")
    print(path)
    print("ANT COLONY OPTIMIZATION TOUR DISTANCE:", cost)
    print("ANT COLONY OPTIMIZATION BEST TOUR FOUND AT GENERATION", best_generation)
    print("BEST GENERATION OVER GENERATION COUNT RATIO:", (best_generation / generation_count))

    return path, cost, duration
