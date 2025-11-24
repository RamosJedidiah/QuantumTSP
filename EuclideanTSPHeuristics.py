from timeit import default_timer as timer
from RandomPointsGenerator import generate_random_points, build_adjacency_matrix
from ArithmeticSeriesMeasurement import measure_arithmetic_series
from OneTreeLowerBound import best_1_tree_lower_bound
from ChristofidesAlgorithm import christofides
from EuclideanTSPArithmeticSeriesForExperiment import solve_tsp, distance_of_tour
from NearestNeighborHeuristics import random_source_nearest_neighbors, all_sources_nearest_neighbors, closest_sources_nearest_neighbors
from SimulatedAnnealing import start_annealing
from AntColonyOptimization import start_ant_colony
from TSPGeneticAlgorithm import start_genetic_algorithm


def test_all(n):
    print("NUMBER OF VERTICES:", n)

    tsp_points = generate_random_points(n)
    
    DISTANCE_MATRIX = build_adjacency_matrix(tsp_points, n)

    print()
    measure_arithmetic_series(n, DISTANCE_MATRIX)

    # 1-TREE LOWER BOUND
    start = timer()
    one_tree_lower_bound = best_1_tree_lower_bound(n, DISTANCE_MATRIX)
    end = timer()
    duration = end - start
    print("1-TREE LOWER BOUND COMPUTATION ELAPSED TIME:", duration, "s")

    # CHRISTOFIDES ALGORITHM
    christofides_tour, christofides_distance, christofides_duration = christofides(tsp_points, n)
    print("CHRISTOFIDES APPROXIMATION RATIO:", (christofides_distance / one_tree_lower_bound))
    print("CHRISTOFIDES ELAPSED TIME:", christofides_duration, "s")

    # TSP ARITHMETIC SERIES PARTIAL SOLVER
    partial_solver_tour, partial_solver_distance, partial_solver_duration = solve_tsp(
        n, DISTANCE_MATRIX, 2)
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER APPROXIMATION RATIO:",
          (partial_solver_distance / one_tree_lower_bound))
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER ELAPSED TIME:", duration, "s")

    # RANDOM SOURCE NEAREST NEIGHBOR HEURISTIC
    start = timer()
    rs_nn_distance = random_source_nearest_neighbors(n, DISTANCE_MATRIX)
    end = timer()
    duration = end - start
    print("RANDOM SOURCE NEAREST NEIGHBOR APPROXIMATION RATIO:", (rs_nn_distance / one_tree_lower_bound))
    print("RANDOM SOURCE NEAREST NEIGHBOR ELAPSED TIME:", duration, "s")

    # ALL SOURCES NEAREST NEIGHBOR HEURISTIC
    start = timer()
    alls_nn_tour, alls_nn_distance = all_sources_nearest_neighbors(n, DISTANCE_MATRIX)
    end = timer()
    alls_nn_duration = end - start
    print("ALL SOURCES NEAREST NEIGHBOR APPROXIMATION RATIO:", (alls_nn_distance / one_tree_lower_bound))
    print("ALL SOURCES NEAREST NEIGHBOR ELAPSED TIME:", alls_nn_duration, "s")

    # CLOSEST SOURCES NEAREST NEIGHBOR HEURSTIC
    start = timer()
    cs_nn_distance = closest_sources_nearest_neighbors(n, DISTANCE_MATRIX)
    end = timer()
    duration = end - start
    print("CLOSEST SOURCES NEAREST NEIGHBOR APPROXIMATION RATIO:", (cs_nn_distance / one_tree_lower_bound))
    print("CLOSEST SOURCES NEAREST NEIGHBOR ELAPSED TIME:", duration, "s")

    # COMPARE INITIAL HEURISTIC TOURS
    best_initial_heuristic_distance = christofides_distance
    best_initial_heuristic_tour = christofides_tour
    best_initial_heuristic_duration = christofides_duration
    best_initial_heuristic_label = "CHRISTOFIDES HEURISTIC"
    if partial_solver_distance < best_initial_heuristic_distance:
        best_initial_heuristic_distance = partial_solver_distance
        best_initial_heuristic_tour = partial_solver_tour
        best_initial_heuristic_duration = partial_solver_duration
        best_initial_heuristic_label = "TSP ARITHMETIC SERIES PARTIAL SOLVER"
    if alls_nn_distance < best_initial_heuristic_distance:
        best_initial_heuristic_distance = alls_nn_distance
        best_initial_heuristic_tour = alls_nn_tour
        best_initial_heuristic_duration = alls_nn_duration
        best_initial_heuristic_label = "ALL SOURCES NEAREST NEIGHBOR HEURISTIC"
    print("BEST INITIAL HEURISTIC:", best_initial_heuristic_label)
    print("BEST INITIAL HEURISTIC APPROXIMATION RATIO:",
          (best_initial_heuristic_distance / one_tree_lower_bound))

    # SIMULATED ANNEALING
    sim_tour, sim_distance, sim_duration = start_annealing(tsp_points, n, best_initial_heuristic_tour,
                                   best_initial_heuristic_distance)
    print("SIMULATED ANNEALING APPROXIMATION RATIO:", (sim_distance / one_tree_lower_bound))
    print("SIMULATED ANNEALING ELAPSED TIME:", sim_duration, "s")

    # ANT COLONY OPTIMIZATION
    aco_tour, aco_distance, aco_duration = start_ant_colony(tsp_points, n, best_initial_heuristic_tour,
                                    best_initial_heuristic_distance)
    print("ANT COLONY OPTIMIZATION APPROXIMATION RATIO:", (aco_distance / one_tree_lower_bound))
    print("ANT COLONY OPTIMIZATION ELAPSED TIME:", aco_duration, "s")

    # GENETIC ALGORITHM
    ga_tour, ga_distance, ga_duration = start_genetic_algorithm(tsp_points, n, best_initial_heuristic_tour,
                                                       best_initial_heuristic_distance)
    print("GENETIC ALGORITHM APPROXIMATION RATIO:", (ga_distance / one_tree_lower_bound))
    print("GENETIC ALGORITHM ELAPSED TIME:", ga_duration, "s")

    # COMPARE FINAL HEURISTIC TOURS
    best_final_heuristic_distance = sim_distance
    best_final_heuristic_tour = sim_tour
    best_final_heuristic_duration = sim_duration
    best_final_heuristic_label = "SIMULATED ANNEALING"
    if aco_distance < best_final_heuristic_distance:
        best_final_heuristic_distance = aco_distance
        best_final_heuristic_tour = aco_tour
        best_final_heuristic_duration = aco_duration
        best_final_heuristic_label = "ANT COLONY OPTIMIZATION"
    if ga_distance < best_final_heuristic_distance:
        best_final_heuristic_distance = ga_distance
        best_final_heuristic_tour = ga_tour
        best_final_heuristic_duration = ga_duration
        best_final_heuristic_label = "GENETIC ALGORITHM"
    print("BEST FINAL HEURISTIC:", best_final_heuristic_label)
    print("BEST FINAL HEURISTIC APPROXIMATION RATIO:",
          (best_final_heuristic_distance / one_tree_lower_bound))
    print("BEST CLASSICAL HEURISTIC TOTAL DURATION:", best_initial_heuristic_duration + best_final_heuristic_duration, "s")

    return DISTANCE_MATRIX
