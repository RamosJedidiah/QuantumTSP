import random


def remove_visited(i, nexts, prevs):
    i_plus1 = i + 1
    # REMOVE DOUBLY LINKED LIST NODE
    nexts[prevs[i_plus1]] = nexts[i_plus1]
    prevs[nexts[i_plus1]] = prevs[i_plus1]


def find_nearest_neighbor(n, i, matrix, nexts):
    j = nexts[0] - 1
    min = matrix[i][j]
    minJ = j
    # TRAVERSE LINKED LIST
    while j < n:
        if matrix[i][j] < min:
            min = matrix[i][j]
            minJ = j
        j = nexts[j + 1] - 1
    return minJ


def nearest_neighbors(n, source, matrix, nexts, prevs, continue_at):
    tour = [0] * n
    tour[0] = source
    remove_visited(source, nexts, prevs)
    for i in range(continue_at, n - 1):
        next_neighbor = find_nearest_neighbor(n, tour[i], matrix, nexts)
        remove_visited(next_neighbor, nexts, prevs)
        tour[i + 1] = next_neighbor
    return tour


def tour_distance(n, matrix, tour):
    from_vertex = tour[0]
    to_vertex = tour[1]
    sum = matrix[from_vertex][to_vertex]
    for i in range(1, n - 1):
        from_vertex = tour[i]
        to_vertex = tour[i + 1]
        sum += matrix[from_vertex][to_vertex]
    # DISTANCE OF TOUR + RETURN TO STARTING VERTEX
    return sum + matrix[to_vertex][tour[0]]


def fixed_source_nearest_neighbors(n, source, matrix):
    # DOUBLY LINKED LIST
    nexts = [0] * (n + 2)
    prevs = [0] * (n + 2)
    for i in range(n + 1):
        nexts[i] = i + 1
        prevs[i + 1] = i
    tour = nearest_neighbors(n, source, matrix, nexts, prevs, 0)
    return tour, tour_distance(n, matrix, tour)


def random_source_nearest_neighbors(n, matrix):
    source = random.randint(0, n - 1)
    tour, distance = fixed_source_nearest_neighbors(n, source, matrix)
    print("RANDOM SOURCE NEAREST NEIGHBOR SOURCE VERTEX:", source)
    print("RANDOM SOURCE NEAREST NEIGHBOR SOURCE OVER VERTEX COUNT RATIO:", ((source + 1) / n))
    print("RANDOM SOURCE NEAREST NEIGHBOR TOUR:")
    print(tour)
    print("RANDOM SOURCE NEAREST NEIGHBOR TOUR DISTANCE:", distance)
    return distance


def all_sources_nearest_neighbors(n, matrix):
    min_tour, min_distance = fixed_source_nearest_neighbors(n, 0, matrix)
    # COMPARE TOURS
    for i in range(1, n):
        tour, distance = fixed_source_nearest_neighbors(n, i, matrix)
        if distance < min_distance:
            min_distance = distance
            min_tour = tour
    print("ALL SOURCES NEAREST NEIGHBOR BEST SOURCE VERTEX:", min_tour[0])
    print("ALL SOURCES NEAREST NEIGHBOR BEST SOURCE OVER VERTEX COUNT RATIO:", ((min_tour[0] + 1) / n))
    print("ALL SOURCES NEAREST NEIGHBOR TOUR:")
    print(min_tour)
    print("ALL SOURCES NEAREST NEIGHBOR TOUR DISTANCE:", min_distance)
    return min_tour, min_distance


def closest_sources_nearest_neighbors(n, matrix):
    min = matrix[0][1]
    min_i = 0
    min_j = 1

    # READ MATRIX WITH DIAGONAL VECTORIZATION
    edge = 0
    for i in range(1, n + 1):
        y = 0
        x = i
        for j in range(i, n):
            # FIND MINIMUM EDGE
            if matrix[y][x] < min:
                min = matrix[y][x]
                min_i = y
                min_j = x
            edge += 1
            # TRAVERSE THE MATRIX DIAGONALLY
            y += 1
            x += 1

    # DOUBLY LINKED LIST
    nexts = [0] * (n + 2)
    prevs = [0] * (n + 2)
    for i in range(n + 1):
        nexts[i] = i + 1
        prevs[i + 1] = i

    remove_visited(min_i, nexts, prevs)
    remove_visited(min_j, nexts, prevs)

    # DECIDE FIRST VERTICES
    i_neighbor = find_nearest_neighbor(n, min_i, matrix, nexts)
    j_neighbor = find_nearest_neighbor(n, min_j, matrix, nexts)
    if matrix[min_i][i_neighbor] < matrix[min_j][j_neighbor]:
        # SWAP
        temp = min_i
        min_i = min_j
        min_j = temp
        j_neighbor = i_neighbor
    remove_visited(j_neighbor, nexts, prevs)

    tour = nearest_neighbors(n, j_neighbor, matrix, nexts, prevs, 2)
    tour[0] = min_i
    tour[1] = min_j
    tour[2] = j_neighbor
    distance = tour_distance(n, matrix, tour)

    print("CLOSEST SOURCES NEAREST NEIGHBOR BEST SOURCE VERTEX:", min_i)
    print("CLOSEST SOURCES NEAREST NEIGHBOR BEST SOURCE OVER VERTEX COUNT RATIO:", ((min_i + 1) / n))
    print("CLOSEST SOURCES NEAREST NEIGHBOR TOUR:")
    print(tour)
    print("CLOSEST SOURCES NEAREST NEIGHBOR TOUR DISTANCE:", distance)
    return distance
