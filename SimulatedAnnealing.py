import math
import random
from timeit import default_timer as timer


class SimAnneal(object):
    def __init__(self, coords, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.coords = coords
        self.N = len(coords)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
        self.best_iteration = 0

        self.nodes = [i for i in range(self.N)]

        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []

        self.worst_accepted_minus_current_fitness = -1
        self.worst_accepted_minus_current_distance = -1
        self.worst_accepted_minus_current_iteration = 0

        self.worst_accepted_minus_current_best_fitness = -1
        self.worst_accepted_minus_current_best_distance = -1
        self.worst_accepted_minus_current_best_iteration = 0

    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
        """
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.nodes)
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))  # nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return solution, cur_fit

    def dist(self, node_0, node_1):
        """
        Euclidean distance between two nodes.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

    def fitness(self, solution):
        """
        Total distance of the current solution path.
        """
        cur_fit = 0
        for i in range(self.N):
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N])
        return cur_fit

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept(..) if candidate is worse.
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
                self.best_iteration = self.iteration
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate
                candidate_minus_current_fitness = candidate_fitness - self.cur_fitness
                if candidate_minus_current_fitness > self.worst_accepted_minus_current_fitness:
                    self.worst_accepted_minus_current_fitness = candidate_minus_current_fitness
                    self.worst_accepted_minus_current_distance = candidate_fitness
                    self.worst_accepted_minus_current_iteration = self.iteration
                candidate_minus_current_best_fitness = candidate_fitness - self.best_fitness
                if candidate_minus_current_best_fitness > self.worst_accepted_minus_current_best_fitness:
                    self.worst_accepted_minus_current_best_fitness = candidate_minus_current_best_fitness
                    self.worst_accepted_minus_current_best_distance = candidate_fitness
                    self.worst_accepted_minus_current_best_iteration = self.iteration

    def anneal(self, initial_heuristic_tour, initial_heuristic_distance):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        #self.cur_solution, self.cur_fitness = self.initial_solution()
        # INITIALIZE WITH BEST INITIAL HEURISTIC SOLUTION
        self.best_solution = self.cur_solution = initial_heuristic_tour
        self.best_fitness = self.cur_fitness = initial_heuristic_distance

        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        #print("Best fitness obtained: ", self.best_fitness)
        #improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        #print(f"Improvement over greedy heuristic: {improvement : .2f}%")

    def batch_anneal(self, times=10):
        """
        Execute simulated annealing algorithm `times` times, with random initial solutions.
        """
        for i in range(1, times + 1):
            print(f"Iteration {i}/{times} -------------------------------")
            self.T = self.T_save
            self.iteration = 1
            self.cur_solution, self.cur_fitness = self.initial_solution()
            self.anneal()


def start_annealing(data, n, initial_heuristic_tour, initial_heuristic_distance):
    coords = []
    for i in range(n):
        coords.append([float(data[i][0]), float(data[i][1])])

    start = timer()
    sa = SimAnneal(coords, stopping_iter=(n * 100))
    sa.anneal(initial_heuristic_tour, initial_heuristic_distance)
    end = timer()
    duration = end - start

    iteration_count = sa.iteration - 1

    print("SIMULATED ANNEALING TOUR:")
    print(sa.best_solution)
    print("SIMULATED ANNEALING TOUR DISTANCE:", sa.best_fitness)
    print("SIMULATED ANNEALING BEST TOUR FOUND AT ITERATION", sa.best_iteration)
    print("SIMULATED ANNEALING ITERATION COUNT:", iteration_count)
    print("BEST ITERATION OVER ITERATION COUNT RATIO:", (sa.best_iteration / iteration_count))

    print("WORST ACCEPTED MINUS CURRENT FITNESS:", sa.worst_accepted_minus_current_fitness)
    print("WORST ACCEPTED MINUS CURRENT FITNESS TOUR DISTANCE:", sa.worst_accepted_minus_current_distance)
    print("WORST ACCEPTED MINUS CURRENT FITNESS FOUND AT ITERATION",
          sa.worst_accepted_minus_current_iteration)
    print("WORST ACCEPTED MINUS CURRENT FITNESS ITERATION OVER ITERATION COUNT RATIO:",
          (sa.worst_accepted_minus_current_iteration / iteration_count))

    print("WORST ACCEPTED MINUS CURRENT BEST FITNESS:", sa.worst_accepted_minus_current_best_fitness)
    print("WORST ACCEPTED MINUS CURRENT BEST FITNESS TOUR DISTANCE:",
          sa.worst_accepted_minus_current_best_distance)
    print("WORST ACCEPTED MINUS CURRENT BEST FITNESS FOUND AT ITERATION",
          sa.worst_accepted_minus_current_best_iteration)
    print("WORST ACCEPTED MINUS CURRENT BEST FITNESS ITERATION OVER ITERATION COUNT RATIO:",
          (sa.worst_accepted_minus_current_best_iteration / iteration_count))

    return sa.best_solution, sa.best_fitness, duration
