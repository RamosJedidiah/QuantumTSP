# Mahdi Hassanzadeh

import random
import math
from timeit import default_timer as timer


# get cities info
def getCity(points, n):
    cities = []
    for i in range(n):
        cities.append([i, float(points[i][0]), float(points[i][1])])
    return cities


# calculating distance of the cities
def calcDistance(cities):
    total_sum = 0
    for i in range(len(cities) - 1):
        cityA = cities[i]
        cityB = cities[i + 1]

        d = math.sqrt(
            math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2)
        )

        total_sum += d

    cityA = cities[0]
    cityB = cities[-1]
    d = math.sqrt(math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2))

    total_sum += d

    return total_sum


# selecting the population
def selectPopulation(cities, size):
    population = []

    for i in range(size):
        c = cities.copy()
        random.shuffle(c)
        distance = calcDistance(c)
        population.append([distance, c])
    fitest = sorted(population)[0]

    return population, fitest


# the genetic algorithm
def geneticAlgorithm(
    population,
    lenCities,
    TOURNAMENT_SELECTION_SIZE,
    MUTATION_RATE,
    CROSSOVER_RATE,
    GENERATIONS,
):
    best_generation = 0
    best_so_far = 0
    gen_number = 0
    for i in range(GENERATIONS):
        new_population = []

        # selecting two of the best options we have (elitism)
        new_population.append(sorted(population)[0])
        new_population.append(sorted(population)[1])

        for i in range(int((len(population) - 2) / 2)):
            # CROSSOVER
            random_number = random.random()
            if random_number < CROSSOVER_RATE:
                parent_chromosome1 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_SIZE)
                )[0]

                parent_chromosome2 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_SIZE)
                )[0]

                point = random.randint(0, lenCities - 1)

                child_chromosome1 = parent_chromosome1[1][0:point]
                for j in parent_chromosome2[1]:
                    if (j in child_chromosome1) == False:
                        child_chromosome1.append(j)

                child_chromosome2 = parent_chromosome2[1][0:point]
                for j in parent_chromosome1[1]:
                    if (j in child_chromosome2) == False:
                        child_chromosome2.append(j)

            # If crossover not happen
            else:
                child_chromosome1 = random.choices(population)[0][1]
                child_chromosome2 = random.choices(population)[0][1]

            # MUTATION
            if random.random() < MUTATION_RATE:
                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)
                child_chromosome1[point1], child_chromosome1[point2] = (
                    child_chromosome1[point2],
                    child_chromosome1[point1],
                )

                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)
                child_chromosome2[point1], child_chromosome2[point2] = (
                    child_chromosome2[point2],
                    child_chromosome2[point1],
                )

            new_population.append([calcDistance(child_chromosome1), child_chromosome1])
            new_population.append([calcDistance(child_chromosome2), child_chromosome2])

        population = new_population

        gen_number += 1

        best_of_current_gen = sorted(population)[0][0]

        if gen_number == 1:
            best_so_far = best_of_current_gen

        if best_of_current_gen < best_so_far:
            best_so_far = best_of_current_gen
            best_generation = gen_number

    answer = sorted(population)[0]

    return answer, best_generation


def start_genetic_algorithm(data, n, initial_heuristic_tour, initial_heuristic_distance):
    # initial values
    POPULATION_SIZE = n
    TOURNAMENT_SELECTION_SIZE = 4
    MUTATION_RATE = 0.1
    CROSSOVER_RATE = 0.9
    GENERATIONS = 100

    cities = getCity(data, n)

    start = timer()
    firstPopulation, firstFittest = selectPopulation(cities, POPULATION_SIZE)
    # INSERT BEST INITIAL HEURISTIC SOLUTION
    for c in range(3):
        # FIRST THREE CHROMOSOMES
        firstPopulation[c][0] = initial_heuristic_distance
        for i in range(n):
            # SHIFT CITY INDEX
            city_index = initial_heuristic_tour[(i + c) % n]
            ith_city = cities[city_index]
            firstPopulation[c][1][i] = ith_city

    answer, bestGeneration = geneticAlgorithm(
        firstPopulation,
        n,
        TOURNAMENT_SELECTION_SIZE,
        MUTATION_RATE,
        CROSSOVER_RATE,
        GENERATIONS
    )
    end = timer()
    duration = end - start

    print("GENETIC ALGORITHM TOUR:")
    tour = []
    for i in range(n):
        tour.append(answer[1][i][0])
    print(tour)
    print("GENETIC ALGORITHM TOUR DISTANCE: " + str(answer[0]))
    print("FITTEST CHROMOSOME FOUND AT GENERATION " + str(bestGeneration))
    print("FITTEST GENERATION OVER GENERATION COUNT RATIO:", (bestGeneration / GENERATIONS))

    return tour, answer[0], duration
