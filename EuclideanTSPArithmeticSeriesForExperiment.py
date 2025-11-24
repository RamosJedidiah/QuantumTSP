import math
from timeit import default_timer as timer


def pre_compute_factorials(n):
    factorials = [1] * (n + 1)
    for i in range(1, n + 1):
        factorials[i] = i * factorials[i - 1]
    return factorials


def unrank_permutation(permutation_rank, n, factorials):
    # GET FACTORIAL DIGITS
    factorial_digits = [0] * n
    rank = permutation_rank
    for i in range(n - 1):
        f = factorials[n - i - 1]
        factorial_digits[i] = rank // f
        rank %= f
    # COMPUTE ceil(log n)
    bits = n
    found1 = False
    found_many1s = False
    k = 0
    while bits != 0:
        if (bits & 1) == 1:
            if found1:
                found_many1s = True
            found1 = True
        bits = bits >> 1
        k += 1
    if found1 and not found_many1s:
        # n IS A POWER OF 2
        k -= 1
    l = 1 << k
    heap_size = (l << 1) - 1
    heap = [0] * heap_size
    m = 1
    for i in range(k + 1):
        for j in range(m):
            heap[m + j - 1] = 1 << (k - i)
        m = m << 1
    permutation = [0] * n
    # UNRANK PERMUTATION
    for i in range(n):
        digit = factorial_digits[i]
        node = 1
        for j in range(k):
            heap[node - 1] -= 1
            node = node << 1
            if digit >= heap[node - 1]:
                digit -= heap[node - 1]
                node += 1
        heap[node - 1] = 0
        permutation[i] = node - l
    return permutation


def distance_of_tour(n, matrix, tour):
    from_vertex = tour[0]
    to_vertex = tour[1]
    sum = matrix[from_vertex][to_vertex]
    for i in range(1, n - 1):
        from_vertex = tour[i]
        to_vertex = tour[i + 1]
        sum += matrix[from_vertex][to_vertex]
    # DISTANCE OF TOUR + RETURN TO STARTING VERTEX
    return sum + matrix[to_vertex][tour[0]]


def brute_force(n, matrix, factorials):
    min_tour = unrank_permutation(0, n, factorials)
    min_distance = distance_of_tour(n, matrix, min_tour)
    rank = 0
    f = factorials[n - 1]
    # EXHAUSTIVE SEARCH
    for i in range(1, f):
        tour = unrank_permutation(i, n, factorials)
        distance = distance_of_tour(n, matrix, tour)
        if distance < min_distance:
            min_distance = distance
            min_tour = tour
            rank = i
    print("BEST CANDIDATE: ADJUSTED TOUR", rank)
    print("BEST SOURCE VERTEX:", 0)
    print("BEST SOURCE OVER VERTEX COUNT RATIO:", 0.0)
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER TOUR:")
    print(min_tour)
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER TOUR DISTANCE:", min_distance)
    return min_tour, min_distance


def remove_visited(i, nexts, prevs):
    i_plus1 = i + 1
    # REMOVE DOUBLY LINKED LIST NODE
    nexts[prevs[i_plus1]] = nexts[i_plus1]
    prevs[nexts[i_plus1]] = prevs[i_plus1]


def find_nearest_neighbor(n, i, matrix, nexts):
    j = nexts[0] - 1
    min = matrix[i][j]
    min_j = j
    # TRAVERSE LINKED LIST
    while j < n:
        if matrix[i][j] < min:
            min = matrix[i][j]
            min_j = j
        j = nexts[j + 1] - 1
    return min_j


def adjust_matrix(n, relabeled_vertices, matrix, relabeled_matrix):
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

    relabeled_vertices[0] = min_i
    relabeled_vertices[1] = min_j
    relabeled_vertices[2] = j_neighbor

    # RELABEL VERTICES
    for i in range(2, n - 1):
        j = find_nearest_neighbor(n, relabeled_vertices[i], matrix, nexts)
        remove_visited(j, nexts, prevs)
        relabeled_vertices[i + 1] = j

    # TRAVERSE THE MATRIX WITH LEFT TO RIGHT VECTORIZATION
    edge = 0
    for i in range(n):
        for j in range(i + 1, n):
            old_i = relabeled_vertices[i]
            old_j = relabeled_vertices[j]
            # RELABEL MATRIX
            relabeled_matrix[i][j] = matrix[old_i][old_j]
            relabeled_matrix[j][i] = matrix[old_j][old_i]
            edge += 1


def binary_search_index(array, mileposts, lower, upper, item):
    low = lower
    high = upper
    while low <= high:
        mid = low + ((high - low) >> 1)
        mid_item = array[mid]
        if item == mid_item:
            # ITEM FOUND
            if mid == 0 or mid_item != array[mid - 1]:
                # START OF ARRAY OR SUBARRAY
                return mid
            else:
                # IS A DUPLICATE
                return mileposts[mid]
        elif item < mid_item:
            # SEARCH LEFT
            high = mid - 1
        else:
            # SEARCH RIGHT
            low = mid + 1
    return -1


def rank_permutation(permutation, n):
    # COMPUTE ceil(log n)
    bits = n
    found1 = False
    found_many1s = False
    k = 0
    while bits != 0:
        if (bits & 1) == 1:
            if found1:
                found_many1s = True
            found1 = True
        bits = bits >> 1
        k += 1
    if found1 and not found_many1s:
        # n IS A POWER OF 2
        k -= 1
    l = 1 << k
    heap_size = (l << 1) - 1
    heap = [0] * heap_size
    # COMPUTE PERMUTATION RANK
    rank = 0
    for i in range(n):
        ctr = permutation[i]
        node = l + ctr
        for j in range(k):
            if (node & 1) == 1:
                ctr -= heap[((node >> 1) << 1) - 1]
            heap[node - 1] += 1
            node = node >> 1
        heap[node - 1] += 1
        rank = rank * (n - i) + ctr
    return rank


def boundary(n, i, factorials):
    if i == 1:
        if n == 5:
            return 32
        if n > 5:
            return factorials[n - 1] + boundary(n - 1, i, factorials)
    if i == 2:
        if n == 7:
            return 5910
        if n > 7:
            return factorials[n] + boundary(n - 1, i, factorials)


def solve_tsp(n, matrix, boundary_choice):
    start = timer()

    # PRE-COMPUTE FACTORIALS
    factorials = pre_compute_factorials(n)

    # TRIVIAL CASE
    if (boundary_choice == 1 and n < 5) or (boundary_choice == 2 and n < 7):
        print("TSP ARITHMETIC SERIES PARTIAL SOLVER USING BRUTE FORCE FOR SMALL TSP INSTANCE")
        tour, distance = brute_force(n, matrix, factorials)
        end = timer()
        duration = end - start
        return tour, distance, duration

    # NUMBER OF EDGES
    edge_count = (n * (n - 1)) >> 1

    # RELABEL MATRIX
    relabeled_vertices = [0] * n
    relabeled_matrix = [[0 for x in range(n)] for y in range(n)]
    adjust_matrix(n, relabeled_vertices, matrix, relabeled_matrix)

    # MAIN ALGORITHM
    edges = [0] * edge_count

    # READ ADJUSTED MATRIX WITH DIAGONAL VECTORIZATION
    edge = 0
    for i in range(1, n + 1):
        y = 0
        x = i
        for j in range(i, n):
            # COLLECT EDGE
            edges[edge] = relabeled_matrix[y][x]
            edge += 1
            # TRAVERSE THE MATRIX DIAGONALLY
            y += 1
            x += 1

    # SORT EDGE WEIGHT LIST
    sorted = [edges[x] for x in range(edge_count)]
    sorted.sort()

    # MILEPOSTS FOR TRACKING SUBARRAYS OF DUPLICATES
    # (FOR GENERALIZING WHEN ARITHMETIC PROGRESSIONS ARE NO LONGER REQUIRED)
    mileposts = [0] * edge_count
    i = 0
    while i < edge_count:
        j = i
        while j < edge_count and sorted[i] == sorted[j]:
            mileposts[j] = i
            j += 1
        i = j

    # MAKE PERMUTABLE FORMAT USING BINARY SEARCH ON SORTED EDGES
    permutation = [0] * edge_count
    high = edge_count - 1
    for i in range(edge_count):
        index = binary_search_index(sorted, mileposts, 0, high, edges[i])
        # REWRITE EDGE WEIGHT LIST WITH NEW PERMUTABLE FORMAT
        permutation[i] = mileposts[index]
        mileposts[index] += 1

    # RANK PERMUTATION
    rank = rank_permutation(permutation, edge_count)

    # FINAL DECISION
    boundary2 = boundary(n, boundary_choice, factorials)
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER BOUNDARY 2 EXCEEDED?", end=" ")
    if rank > boundary2:
        print("YES")
    else:
        print("NO")
    print("BINARY LOGARITHM OF ADJUSTED CONFIGURATION RANK:", (math.log(rank, 2)))

    # HAMILTONIAN CYCLE 0
    candidate0 = [relabeled_vertices[x] for x in range(n)]

    # HAMILTONIAN CYCLE (n - 2)! - 1
    candidate_n_2f_1 = [relabeled_vertices[x] for x in range(n)]
    # REVERSE ENDING SUBARRAY
    mid = 3 + ((n - 3) >> 1)
    for i in range(2, mid):
        temp = candidate_n_2f_1[i]
        candidate_n_2f_1[i] = candidate_n_2f_1[n - 1 - (i - 2)]
        candidate_n_2f_1[n - 1 - (i - 2)] = temp

    # HAMILTONIAN CYCLE 1
    candidate1 = [relabeled_vertices[x] for x in range(n)]
    # SWAP LAST TWO VERTICES
    temp = candidate1[n - 2]
    candidate1[n - 2] = candidate1[n - 1]
    candidate1[n - 1] = temp

    # COMPARE CANDIDATES
    distance0 = distance_of_tour(n, matrix, candidate0)
    distance_n_2f_1 = distance_of_tour(n, matrix, candidate_n_2f_1)
    distance1 = distance_of_tour(n, matrix, candidate1)

    min_distance = distance0
    min_tour = candidate0
    min_tour_label = "0"
    if distance_n_2f_1 < min_distance:
        min_distance = distance_n_2f_1
        min_tour = candidate_n_2f_1
        min_tour_label = "(n - 2)! - 1"
    if distance1 < min_distance:
        min_distance = distance1
        min_tour = candidate1
        min_tour_label = "1"

    end = timer()
    duration = end - start

    print("BEST CANDIDATE: ADJUSTED TOUR", min_tour_label)
    print("BEST SOURCE VERTEX:", min_tour[0])
    print("BEST SOURCE OVER VERTEX COUNT RATIO:", ((min_tour[0] + 1) / n))
    print("TSP ARITHMETIC SERIES PARTIAL SOLVER TOUR:")
    print(min_tour)
    print("TSP ARITHMETIC SERIES PARTIAL SOVLER TOUR DISTANCE:", min_distance)

    return min_tour, min_distance, duration
