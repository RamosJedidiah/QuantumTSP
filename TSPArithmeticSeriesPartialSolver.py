def PreComputeFactorials(n):
    factorials = [1 for x in range(n + 1)]
    for i in range(1, n + 1):
        factorials[i] = i * factorials[i - 1]
    return factorials

def UnrankPermutation(permutationRank, n, factorials):
    # GET FACTORIAL DIGITS
    factorialDigits = [0 for x in range(n)]
    rank = permutationRank
    for i in range(n - 1):
        f = factorials[n - i - 1]
        factorialDigits[i] = rank // f
        rank %= f
    # COMPUTE ceil(log n)
    bits = n
    found1 = False
    foundMany1s = False
    k = 0
    while bits != 0:
        if (bits & 1) == 1:
            if found1:
                foundMany1s = True
            found1 = True
        bits = bits >> 1
        k += 1
    if found1 and not foundMany1s:
        # n IS A POWER OF 2
        k -= 1
    l = 1 << k
    heapSize = (l << 1) - 1
    heap = [0 for x in range(heapSize)]
    m = 1
    for i in range(k + 1):
        for j in range(m):
            heap[m + j - 1] = 1 << (k - i)
        m = m << 1
    permutation = [0 for x in range(n)]
    # UNRANK PERMUTATION
    for i in range(n):
        digit = factorialDigits[i]
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

def TourDistance(V, matrix, tour):
    fromVertex = tour[0]
    toVertex = tour[1]
    sum = matrix[fromVertex][toVertex]
    for i in range(1, V - 1):
        fromVertex = tour[i]
        toVertex = tour[i + 1]
        sum += matrix[fromVertex][toVertex]
    # DISTANCE OF TOUR + RETURN TO STARTING VERTEX
    return sum + matrix[toVertex][tour[0]]

def BruteForce(V, matrix, factorials):
    tour = UnrankPermutation(0, V, factorials)
    minDistance = TourDistance(V, matrix, tour)
    minTour = [tour[x] for x in range(V)]
    f = factorials[V - 1]
    # EXHAUSTIVE SEARCH
    for i in range(1, f):
        tour = UnrankPermutation(i, V, factorials)
        distance = TourDistance(V, matrix, tour)
        if distance < minDistance:
            minDistance = distance
            minTour = [tour[x] for x in range(V)]
    print("THE OPTIMAL TOUR IS")
    print(minTour)
    print("THE MINIMUM DISTANCE IS")
    print(minDistance)
    return minDistance

def RemoveVisited(i, nexts, prevs):
    iPlus1 = i + 1
    # REMOVE DOUBLY LINKED LIST NODE
    nexts[prevs[iPlus1]] = nexts[iPlus1]
    prevs[nexts[iPlus1]] = prevs[iPlus1]

def FindNearestNeighbor(V, i, matrix, nexts):
    head = 0
    j = nexts[head] - 1
    min = matrix[i][j]
    minJ = j
    # TRAVERSE LINKED LIST
    while j < V:
        if matrix[i][j] < min:
            min = matrix[i][j]
            minJ = j
        j = nexts[j + 1] - 1
    return minJ

def AdjustMatrix(V, relabeledVertices, matrix, relabeledMatrix):
    min = matrix[0][1]
    minI = 0
    minJ = 1

    # READ MATRIX WITH DIAGONAL VECTORIZATION
    edge = 0
    for i in range(1, V + 1):
        y = 0
        x = i
        for j in range(i, V):
            # FIND MINIMUM EDGE
            if matrix[y][x] < min:
                min = matrix[y][x]
                minI = y
                minJ = x
            edge += 1
            # TRAVERSE THE MATRIX DIAGONALLY
            y += 1
            x += 1

    # DOUBLY LINKED LIST
    nexts = [0 for x in range(V + 2)]
    prevs = [0 for x in range(V + 2)]
    for i in range(V + 1):
        nexts[i] = i + 1
        prevs[i + 1] = i
    RemoveVisited(minI, nexts, prevs)
    RemoveVisited(minJ, nexts, prevs)

    # DECIDE FIRST VERTICES
    iNeighbor = FindNearestNeighbor(V, minI, matrix, nexts)
    jNeighbor = FindNearestNeighbor(V, minJ, matrix, nexts)
    if matrix[minI][iNeighbor] < matrix[minJ][jNeighbor]:
        # SWAP
        temp = minI
        minI = minJ
        minJ = temp
        jNeighbor = iNeighbor
    RemoveVisited(jNeighbor, nexts, prevs)

    relabeledVertices[0] = minI
    relabeledVertices[1] = minJ
    relabeledVertices[2] = jNeighbor

    # RELABEL VERTICES
    for i in range(2, V - 1):
        j = FindNearestNeighbor(V, relabeledVertices[i], matrix, nexts)
        RemoveVisited(j, nexts, prevs)
        relabeledVertices[i + 1] = j

    # TRAVERSE THE MATRIX WITH LEFT TO RIGHT VECTORIZATION
    edge = 0
    for i in range(V):
        for j in range(i + 1, V):
            oldI = relabeledVertices[i]
            oldJ = relabeledVertices[j]
            # RELABEL MATRIX
            relabeledMatrix[i][j] = matrix[oldI][oldJ]
            relabeledMatrix[j][i] = matrix[oldJ][oldI]
            edge += 1

def BinarySearchIndex(array, mileposts, lower, upper, item):
    low = lower
    high = upper
    while low <= high:
        mid = low + ((high - low) >> 1)
        midItem = array[mid]
        if item == midItem:
            # ITEM FOUND
            if mid == 0 or midItem != array[mid - 1]:
                # START OF ARRAY OR SUBARRAY
                return mid
            else:
                # IS A DUPLICATE
                return mileposts[mid]
        elif item < midItem:
            # SEARCH LEFT
            high = mid - 1
        else:
            # SEARCH RIGHT
            low = mid + 1
    return -1

def RankPermutation(permutation, n):
    # COMPUTE ceil(log n)
    bits = n
    found1 = False
    foundMany1s = False
    k = 0
    while bits != 0:
        if (bits & 1) == 1:
            if found1:
                foundMany1s = True
            found1 = True
        bits = bits >> 1
        k += 1
    if found1 and not foundMany1s:
        # n IS A POWER OF 2
        k -= 1
    l = 1 << k
    heapSize = (l << 1) - 1
    heap = [0 for x in range(heapSize)]
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

def Boundary(n, i, factorials):
    if i == 1:
        if n == 5:
            return 32
        if n > 5:
            return factorials[n - 1] + Boundary(n - 1, i, factorials)
    if i == 2:
        if n == 7:
            return 5910
        if n > 7:
            return factorials[n] + Boundary(n - 1, i, factorials)

def SolveTSP(matrix, iBoundary):
    print("Adjacency Matrix:")
    for row in matrix:
        print(row)

    # NUMBER OF VERTICES
    V = len(matrix)

    # PRE-COMPUTE FACTORIALS
    factorials = PreComputeFactorials(V)

    # TRIVIAL CASE
    if (iBoundary == 1 and V < 5) or (iBoundary == 2 and V < 7):
        return BruteForce(V, matrix, factorials)

    # NUMBER OF EDGES
    E = (V * (V - 1)) >> 1

    # RELABEL MATRIX
    relabeledVertices = [0 for x in range(V)]
    relabeledMatrix = [[0 for x in range(V)] for y in range(V)]
    AdjustMatrix(V, relabeledVertices, matrix, relabeledMatrix)

    # MAIN ALGORITHM
    edges = [0 for x in range(E)]

    # READ MATRIX WITH DIAGONAL VECTORIZATION
    edge = 0
    for i in range(1, V + 1):
        y = 0
        x = i
        for j in range(i, V):
            # COLLECT EDGE
            edges[edge] = relabeledMatrix[y][x]
            edge += 1
            # TRAVERSE THE MATRIX DIAGONALLY
            y += 1
            x += 1

    # SORT EDGE WEIGHT LIST
    sorted = [edges[x] for x in range(E)]
    sorted.sort()

    # MILEPOSTS FOR TRACKING SUBARRAYS OF DUPLICATES
    # (FOR GENERALIZING WHEN ARITHMETIC PROGRESSIONS ARE NO LONGER REQUIRED)
    mileposts = [0 for x in range(E)]
    i = 0
    while i < E:
        j = i
        while j < E and sorted[i] == sorted[j]:
            mileposts[j] = i
            j += 1
        i = j

    # MAKE PERMUTABLE FORMAT USING BINARY SEARCH ON SORTED EDGES
    permutation = [0 for x in range(E)]
    high = E - 1
    for i in range(E):
        index = BinarySearchIndex(sorted, mileposts, 0, high, edges[i])
        # REWRITE EDGE WEIGHT LIST WITH NEW PERMUTABLE FORMAT
        permutation[i] = mileposts[index]
        mileposts[index] += 1

    # RANK PERMUTATION
    rank = RankPermutation(permutation, E)

    # FINAL DECISION
    if rank > Boundary(V, iBoundary, factorials):
        print("THE OPTIMAL TOUR IS UNKNOWN")
        return -1

    # HAMILTONIAN CYCLE 0
    candidate0 = [relabeledVertices[x] for x in range(V)]

    # HAMILTONIAN CYCLE (V - 2)! - 1
    candidateV_2F_1 = [relabeledVertices[x] for x in range(V)]
    # REVERSE ENDING SUBARRAY
    mid = 3 + ((V - 3) >> 1)
    for i in range(2, mid):
        temp = candidateV_2F_1[i]
        candidateV_2F_1[i] = candidateV_2F_1[V - 1 - (i - 2)]
        candidateV_2F_1[V - 1 - (i - 2)] = temp

    # HAMILTONIAN CYCLE 1
    candidate1 = [relabeledVertices[x] for x in range(V)]
    # SWAP LAST TWO VERTICES
    temp = candidate1[V - 2]
    candidate1[V - 2] = candidate1[V - 1]
    candidate1[V - 1] = temp

    # COMPARE CANDIDATES
    distance0 = TourDistance(V, matrix, candidate0)
    distanceV_2F_1 = TourDistance(V, matrix, candidateV_2F_1)
    distance1 = TourDistance(V, matrix, candidate1)

    minDistance = distance0
    minTour = [candidate0[x] for x in range(V)]
    if distanceV_2F_1 < minDistance:
        minDistance = distanceV_2F_1
        minTour = [candidateV_2F_1[x] for x in range(V)]
    if distance1 < minDistance:
        minDistance = distance1
        minTour = [candidate1[x] for x in range(V)]

    print("THE OPTIMAL TOUR IS")
    print(minTour)
    print("THE MINIMUM DISTANCE IS")
    print(minDistance)
    return minDistance

if __name__ == '__main__':
    # INPUT A DISTANCE MATRIX WITH EDGES THAT FORM AN ARITHMETIC SERIES (e.g. 3.2, 5.2, 7.2, 9.2, ...)
    # WITH ANY POSITIVE FIRST TERM, ANY POSITIVE COMMON DIFFERENCE, AND ANY NUMBER OF VERTICES
    # IT MUST BE AN UNDIRECTED GRAPH
    graph = [
        [0, 2, 14, 24, 32, 38, 42],
        [2, 0, 4, 16, 26, 34, 40],
        [14, 4, 0, 6, 18, 28, 36],
        [24, 16, 6, 0, 8, 20, 30],
        [32, 26, 18, 8, 0, 10, 22],
        [38, 34, 28, 20, 10, 0, 12],
        [42, 40, 36, 30, 22, 12, 0]
    ]
    # CHOOSE 1 OR 2 AS THE SECOND ARGUMENT "iBoundary"
    # THE NUMBER OF SOLVABLE TSP INSTANCES DEPENDS ON THIS
    SolveTSP(graph, 2)
